# -*- coding: utf-8 -*-
"""TRAM 模型：单研究适配 + 队列回归 + Excel 重建"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import spearmanr
from config import TRIGGERS, TRAM_DIMS, QUEUE_ALPHA, DIMENSIONS, judge, combine


# ============================================================
# 从 Excel 重建完整 rec（关键修复）
# ============================================================
def _find_excel():
    base = Path(__file__).parent / "data"
    if not base.is_dir():
        return None
    files = list(base.glob("*.xlsx")) + list(base.glob("*.xls"))
    return files[0] if files else None


def _load_excel_df():
    path = _find_excel()
    if not path:
        return None
    xls = pd.ExcelFile(path)
    sheet = "干细胞类型提取" if "干细胞类型提取" in xls.sheet_names else xls.sheet_names[0]
    raw = pd.read_excel(xls, sheet_name=sheet, header=None)
    hdr = 0
    for i in range(min(6, len(raw))):
        vals = [str(v) for v in raw.iloc[i].tolist()]
        if any("NCT Number" in v or "Study Title" in v for v in vals):
            hdr = i
            break
    df = pd.read_excel(xls, sheet_name=sheet, header=hdr)
    df.columns = [str(c).replace("\n", " ").replace("\r", " ").strip() for c in df.columns]
    return df


def build_rec_from_excel(nct, title):
    """从 Excel 查找并构建带完整判定的 rec"""
    try:
        df = _load_excel_df()
    except Exception:
        return None
    if df is None:
        return None

    nct_col = next((c for c in df.columns if "NCT Number" in c), None)
    title_col = next((c for c in df.columns if "Study Title" in c), None)

    matched = None
    for _, row in df.iterrows():
        rn = str(row.get(nct_col, "") or "").strip() if nct_col else ""
        rt = str(row.get(title_col, "") or "").strip() if title_col else ""
        if rn.lower() == "nan":
            rn = ""
        if rt.lower() == "nan":
            rt = ""

        if nct and rn and rn.lower() == nct.lower():
            matched = row
            break
        if title and rt and rt == title:
            matched = row
            break

    if matched is None:
        return None

    def find_col(kw):
        for c in df.columns:
            if kw in c:
                return c
        return None

    rec = {"nct": nct, "title": title, "dims": []}
    for dim in DIMENSIONS:
        d = {"name": dim["name"], "icon": dim["icon"],
             "tram": dim.get("tram"), "items": []}
        for item in dim["items"]:
            vals = []
            for ck in item["cols"]:
                col = find_col(ck)
                if col is None:
                    vals.append("")
                else:
                    v = str(matched.get(col, "") or "").strip()
                    if v.lower() == "nan":
                        v = ""
                    vals.append(v)

            if item["mode"] == "raw":
                status = "信息"
                detail = vals[0] if vals else ""
            else:
                status = combine([judge(v) for v in vals])
                detail = " | ".join(v for v in vals if v)

            d["items"].append({
                "label": item["label"],
                "status": status,
                "detail": detail[:500],
                "trigger": item.get("trigger")
            })
        rec["dims"].append(d)
    return rec


# ============================================================
# 单篇 ICF TRAM 剖面
# ============================================================
def compute_single_tram(rec):
    triggers = {k: 0 for k in TRIGGERS}
    trigger_note = {k: "" for k in TRIGGERS}

    for d in rec.get("dims", []):
        for it in d.get("items", []):
            tg = it.get("trigger")
            if not tg:
                continue
            if tg == "A":
                txt = (it.get("detail", "") or "").lower()
                if any(k in txt for k in ["异体", "allogeneic", "同种异体", "异基因"]):
                    triggers["A"] = 1
                    trigger_note["A"] = "细胞来源：" + it.get("detail", "")[:40]
            else:
                st = it.get("status", "")
                if st not in ("不适用", "信息", "未知", ""):
                    triggers[tg] = 1
                    trigger_note[tg] = "%s（%s）" % (it.get("label", ""), st)

    tcs = sum(triggers.values())

    def calc_score(items):
        applicable, disclosed = 0, 0.0
        for it in items:
            st = it.get("status", "")
            if st in ("不适用", "未知", "信息", ""):
                continue
            applicable += 1
            if st == "符合":
                disclosed += 1
            elif st == "部分符合":
                disclosed += 0.5
        return (disclosed / applicable * 100) if applicable > 0 else None

    scores = {k: None for k in TRAM_DIMS}
    for d in rec.get("dims", []):
        t = d.get("tram")
        if t in scores:
            scores[t] = calc_score(d.get("items", []))

    valid = [s for s in scores.values() if s is not None]
    overall = float(np.mean(valid)) if valid else 0.0
    mismatch = 100 - overall

    gaps = {k: [] for k in TRAM_DIMS}
    for d in rec.get("dims", []):
        t = d.get("tram")
        if t not in gaps:
            continue
        for it in d.get("items", []):
            st = it.get("status", "")
            if st in ("不适用", "未知", "信息", "符合", ""):
                continue
            gaps[t].append({"label": it.get("label", ""), "status": st})

    return {
        "triggers": triggers,
        "trigger_note": trigger_note,
        "tcs": tcs,
        "scores": scores,
        "overall_coverage": round(overall, 2),
        "mismatch": round(mismatch, 2),
        "gaps": gaps,
        "queue_alpha": QUEUE_ALPHA,
        "tram_dims": TRAM_DIMS,
    }


# ============================================================
# 队列层回归
# ============================================================
def run_cohort_regression(df, mode="manuscript"):
    d = df.copy()

    if "Start Year" in d.columns:
        if mode == "manuscript":
            d["Year_model"] = d["Start Year"].fillna(d["Start Year"].median())
        else:
            d["Year_model"] = d["Start Year"]

    outcomes = []
    for c in d.columns:
        lc = c.lower()
        if "risk transparency" in lc:
            outcomes.append(("Risk Transparency", c))
        elif "ongoing consent" in lc:
            outcomes.append(("Ongoing Consent", c))
        elif "governance" in lc:
            outcomes.append(("Data/Biospecimen Governance", c))

    mismatch_col = None
    for c in d.columns:
        if "mismatch" in c.lower():
            mismatch_col = c
            break

    if "TCS" not in d.columns:
        raise ValueError("Excel 缺少 TCS 列，无法运行队列回归")

    results = []

    def fit_one(label, col, group_col=None):
        sub = d[[col, "TCS"]].copy()
        if "Year_model" in d.columns:
            sub["Year_model"] = d.loc[sub.index, "Year_model"]
        if group_col and group_col in d.columns:
            sub["Group"] = d.loc[sub.index, group_col].astype(str)
            sub = sub.dropna()
            cols = ["TCS"]
            if "Year_model" in sub.columns:
                cols.append("Year_model")
            cols.append("Group")
            X = pd.get_dummies(sub[cols], columns=["Group"], drop_first=True, dtype=float)
        else:
            sub = sub.dropna()
            cols = ["TCS"]
            if "Year_model" in sub.columns:
                cols.append("Year_model")
            X = sub[cols].astype(float)
        X = sm.add_constant(X, has_constant="add")
        y = sub[col].astype(float)
        m = sm.RLM(y, X, M=sm.robust.norms.HuberT()).fit()
        beta = float(m.params["TCS"])
        se = float(m.bse["TCS"])
        p = float(m.pvalues["TCS"])
        rho, _ = spearmanr(sub["TCS"], y)
        return {
            "结局": label,
            "队列_alpha_TCS": round(beta, 3),
            "SE": round(se, 3),
            "95%CI_low": round(beta - 1.96 * se, 3),
            "95%CI_high": round(beta + 1.96 * se, 3),
            "p值": round(p, 5),
            "Spearman_rho": round(rho, 3),
            "n": int(len(sub)),
        }

    group_col = None
    for c in d.columns:
        if "cell" in c.lower() and "group" in c.lower():
            group_col = c
            break

    for label, col in outcomes:
        try:
            results.append(fit_one(label, col, group_col))
        except Exception as e:
            results.append({"结局": label, "错误": str(e)})

    if mismatch_col:
        try:
            results.append(fit_one("Mismatch", mismatch_col, group_col))
        except Exception as e:
            results.append({"结局": "Mismatch", "错误": str(e)})

    return results

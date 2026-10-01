# -*- coding: utf-8 -*-
"""TRAM 干细胞 ICF 评估系统 —— FastAPI 应用"""
from pathlib import Path
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from tram_model import (
    compute_single_tram,
    run_cohort_regression,
    build_rec_from_excel,
)

BASE = Path(__file__).parent
DATA_DIR = BASE / "data"
FRONTEND = BASE / "frontend"

app = FastAPI(title="TRAM 干细胞 ICF 评估系统", version="1.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "model": "TRAM v1.1"}


@app.post("/api/tram/single")
def tram_single(payload: dict):
    """
    接收前端 rec。
    如果 rec 的 nct / title 能在 Excel 里匹配到，
    则从 Excel 重建带完整判定的 rec（修复空壳问题）；
    否则回退使用前端传的 rec（用于"分析新 ICF"场景）。
    """
    nct = str(payload.get("nct", "") or "").strip()
    title = str(payload.get("title", "") or "").strip()

    rec = None
    if (nct and not nct.startswith("自定义")) or title:
        try:
            rec = build_rec_from_excel(nct, title)
        except Exception:
            rec = None

    if rec is None:
        rec = payload

    try:
        return compute_single_tram(rec)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/tram/cohort")
def tram_cohort(mode: str = "manuscript"):
    excel_files = list(DATA_DIR.glob("*.xlsx")) + list(DATA_DIR.glob("*.xls"))
    if not excel_files:
        raise HTTPException(status_code=404, detail="data 目录下未找到 Excel 文件")

    path = excel_files[0]
    try:
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

        results = run_cohort_regression(df, mode=mode)
        return {"mode": mode, "n_rows": len(df), "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if FRONTEND.is_dir():
    @app.get("/")
    def index():
        return FileResponse(FRONTEND / "index.html")

    app.mount("/static", StaticFiles(directory=str(FRONTEND)), name="static")

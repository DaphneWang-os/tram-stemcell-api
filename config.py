# -*- coding: utf-8 -*-
"""75 条目定义 + TRAM 触发映射（后端使用）"""

DIMENSIONS = [
    {"id": 1, "name": "维度一：技术披露", "icon": "🔬", "tram": None, "items": [
        {"label": "干细胞类型（BSC/iPSC/ASC/MSC）", "cols": ["干细胞类型判定"], "mode": "raw"},
        {"label": "细胞来源（自体/异体/胚胎/脐带）", "cols": ["备注"], "mode": "raw", "trigger": "A"},
        {"label": "处理方式（培养/基因编辑/分化）", "cols": ["处理方式判定"], "mode": "raw"},
        {"label": "自主程度（辅助/决策支持/替代）", "cols": ["自主程度判定"], "mode": "raw"},
        {"label": "偏离标准治疗（实验性/替代性）", "cols": ["偏离标准治疗判定"], "mode": "raw"},
        {"label": "患者交互方式（移植/注射/监测）", "cols": ["回输/移植"], "mode": "raw"},
        {"label": "研究阶段", "cols": ["研究阶段判定"], "mode": "raw"},
        {"label": "细胞操作流程逐项披露", "cols": ["操作流程完整性判定"], "mode": "judge", "type": "multi",
         "keys": ["分离","采集","扩增","培养","基因编辑","分化","冻存","复苏","质控","回输","移植"]},
        {"label": "供者与受试者角色分别告知", "cols": ["供者角色告知","受试者角色告知","采集与回输是否区分"], "mode": "judge"},
        {"label": "研究性质明示", "cols": ["研究性质明示"], "mode": "judge"},
        {"label": "细胞最终用途限定", "cols": ["用途限定综合判定"], "mode": "judge"},
        {"label": "体外操作时间与培养代数上限告知", "cols": ["体外操作时长告知"], "mode": "judge", "trigger": "E"},
        {"label": "冷冻保存及解冻后细胞状态告知", "cols": ["冷冻保存过程告知"], "mode": "judge", "trigger": "C"},
        {"label": "培养代数上限及传代次数告知", "cols": ["培养代数上限告知","传代次数告知"], "mode": "judge", "trigger": "E"},
        {"label": "剂量递增方案及 MTD 告知", "cols": ["剂量探索试验"], "mode": "judge", "trigger": "D"},
    ]},
    {"id": 2, "name": "维度二：风险获益沟通", "icon": "⚠️", "tram": "R", "items": [
        {"label": "临床风险（致瘤性/免疫排斥/GVHD）", "cols": ["临床风险告知"], "mode": "judge"},
        {"label": "隐私与伦理", "cols": ["隐私与伦理"], "mode": "judge"},
        {"label": "长期风险", "cols": ["长期风险"], "mode": "judge"},
        {"label": "获益披露", "cols": ["获益披露"], "mode": "judge"},
        {"label": "不确定性", "cols": ["不确定性"], "mode": "judge"},
        {"label": "治疗性误解防范", "cols": ["治疗性误解防范"], "mode": "judge"},
        {"label": "替代方案具体列举", "cols": ["替代方案具体列举"], "mode": "judge"},
        {"label": "风险发生率告知", "cols": ["风险发生率告知"], "mode": "judge"},
        {"label": "研究不等于治疗独立警示框", "cols": ["研究不等于治疗"], "mode": "judge"},
        {"label": "无疗效可能性告知", "cols": ["无疗效可能性告知"], "mode": "judge"},
        {"label": "免疫抑制方案风险逐项列出", "cols": ["免疫抑制方案风险"], "mode": "judge", "trigger": "I"},
        {"label": "长期随访必要性及时间表", "cols": ["长期随访必要性"], "mode": "judge", "trigger": "L"},
        {"label": "解冻后细胞功能衰减风险", "cols": ["解冻后细胞功能"], "mode": "judge"},
        {"label": "过度传代致效力降低风险", "cols": ["过度传代致治疗效力"], "mode": "judge"},
        {"label": "DLT 及停药规则告知", "cols": ["剂量限制性毒性"], "mode": "judge", "trigger": "D"},
    ]},
    {"id": 3, "name": "维度三：可读性与可访问性", "icon": "📖", "tram": None, "items": [
        {"label": "文档长度<=15,000字符", "cols": ["文档长度"], "mode": "judge", "type": "length"},
        {"label": "SMOG 可读性", "cols": ["SMOG"], "mode": "judge", "type": "smog"},
        {"label": "视觉辅助", "cols": ["视觉辅助"], "mode": "judge"},
        {"label": "分层结构", "cols": ["分层结构"], "mode": "judge"},
        {"label": "交互数字同意", "cols": ["交互数字同意"], "mode": "judge"},
        {"label": "阅读水平匹配", "cols": ["阅读水平匹配"], "mode": "judge"},
        {"label": "多语言适配", "cols": ["多语言适配"], "mode": "judge"},
        {"label": "风险摘要突出显示", "cols": ["风险摘要突出显示"], "mode": "judge"},
        {"label": "版本号与修订日期", "cols": ["知情同意书版本号"], "mode": "judge"},
        {"label": "视频辅助解释流程", "cols": ["视频辅助解释操作流程"], "mode": "judge"},
        {"label": "关键术语词汇表", "cols": ["关键术语词汇表"], "mode": "judge"},
        {"label": "风险/获益对比图", "cols": ["风险/获益对比图"], "mode": "judge"},
        {"label": "解冻-回输时间窗口图", "cols": ["解冻-回输时间窗口图示"], "mode": "judge"},
        {"label": "培养代数趋势图", "cols": ["培养代数与细胞状态变化趋势图"], "mode": "judge"},
        {"label": "剂量-毒性可视化图", "cols": ["剂量-毒性关系可视化图表"], "mode": "judge"},
    ]},
    {"id": 4, "name": "维度四：数据与样本治理", "icon": "🗄️", "tram": "G", "items": [
        {"label": "数据类型", "cols": ["数据类型"], "mode": "judge"},
        {"label": "存储方案", "cols": ["存储方案"], "mode": "judge"},
        {"label": "访问权限", "cols": ["访问权限"], "mode": "judge"},
        {"label": "保留期限", "cols": ["保留期限"], "mode": "judge"},
        {"label": "未来使用", "cols": ["未来使用"], "mode": "judge"},
        {"label": "法规引用", "cols": ["法规引用"], "mode": "judge"},
        {"label": "退出后选择", "cols": ["退出后选择"], "mode": "judge"},
        {"label": "剩余样本处置", "cols": ["剩余样本处置方式"], "mode": "judge"},
        {"label": "样本转运目的地", "cols": ["样本转运目的地"], "mode": "judge"},
        {"label": "样本库存储条件及再授权", "cols": ["生物样本库存储条件"], "mode": "judge"},
        {"label": "第三方共享再次同意", "cols": ["第三方共享前需获"], "mode": "judge"},
        {"label": "数据保留年限", "cols": ["数据保留年限"], "mode": "judge"},
        {"label": "冻存细胞标识与追溯", "cols": ["冻存细胞标识与追溯信息"], "mode": "judge"},
        {"label": "各代次质控数据记录", "cols": ["各代次细胞质量控制数据记录"], "mode": "judge"},
        {"label": "不良事件与剂量关联性", "cols": ["不良事件与剂量关联性记录"], "mode": "judge"},
    ]},
    {"id": 5, "name": "维度五：动态知情同意", "icon": "🔄", "tram": "O", "items": [
        {"label": "持续更新", "cols": ["持续更新"], "mode": "judge"},
        {"label": "咨询渠道", "cols": ["咨询渠道"], "mode": "judge"},
        {"label": "人员培训", "cols": ["人员培训"], "mode": "judge"},
        {"label": "退出管理", "cols": ["退出管理"], "mode": "judge"},
        {"label": "脆弱人群", "cols": ["脆弱人群"], "mode": "judge"},
        {"label": "伦理审查", "cols": ["伦理审查"], "mode": "judge"},
        {"label": "退出权保障", "cols": ["退出权保障"], "mode": "judge"},
        {"label": "研究变更时重新同意", "cols": ["研究变更时重新获取同意"], "mode": "judge"},
        {"label": "撤回同意即时生效", "cols": ["撤回同意后样本处理即时生效机制"], "mode": "judge"},
        {"label": "不良反应实时告知", "cols": ["不良反应实时告知与补充知情"], "mode": "judge"},
        {"label": "年度随访知情重申", "cols": ["年度随访期间知情重申"], "mode": "judge"},
        {"label": "儿童年龄过渡期重新知情", "cols": ["儿童受试者年龄过渡期重新知情"], "mode": "judge"},
        {"label": "解冻后效期变更告知", "cols": ["解冻后效期变更时重新告知"], "mode": "judge"},
        {"label": "传代接近上限提前告知", "cols": ["传代次数接近上限时提前告知"], "mode": "judge"},
        {"label": "剂量组 DLT 实时告知", "cols": ["剂量组发生DLT时实时告知"], "mode": "judge"},
    ]},
]

TRIGGERS = {"C": "冻存", "E": "体外培养/传代", "A": "异体来源",
            "I": "免疫抑制", "D": "剂量递增/DLT", "L": "长期随访"}

TRAM_DIMS = {
    "R": "风险透明度 (Risk Transparency)",
    "O": "持续知情同意 (Ongoing Consent)",
    "G": "数据/样本治理 (Data/Biospecimen Governance)",
}

QUEUE_ALPHA = {
    "R": {"value": 5.53,  "label": "正向",       "desc": "复杂度增加时风险透明度增强"},
    "O": {"value": -2.45, "label": "无明确正向", "desc": "未随复杂度同步增强"},
    "G": {"value": -0.82, "label": "无明确正向", "desc": "治理维度未同步增强"},
    "M": {"value": -5.93, "label": "负向",       "desc": "复杂度增加与不匹配下降相关，但绝对缺口仍高"},
}

NA_KEYS = ["不适用", "不涉及", "未涉及", "未操作", "未注册", "不改变"]
NEG_KEYS = ["未明确", "未提及", "不足", "缺失", "未检出", "无独立", "未声明", "未告知",
            "未引用", "未说明", "超标", "超阈", "需大学以上", "未在", "未区分", "未提供",
            "未详述", "未使用", "无（"]
MID_KEYS = ["部分", "基本充分", "有提及", "简略", "模糊", "少数", "略超", "在限内"]
POS_KEYS = ["充分", "明确告知", "明确", "符合", "已告知", "已声明", "已标注", "已区分",
            "有发生率数据", "有随机", "有机制", "有流程", "上限内", "水平以下", "有（", "是（"]
RANK = {"不符合": 0, "部分符合": 1, "符合": 2}


def judge(text):
    s = "" if text is None else str(text).strip()
    if not s or s.lower() in ("nan", "none", "--"):
        return "未知"
    if any(k in s for k in NA_KEYS):
        return "不适用"
    if "不明确" in s or s.startswith("待"):
        return "未知"
    if any(k in s for k in NEG_KEYS):
        return "不符合"
    if any(k in s for k in MID_KEYS):
        return "部分符合"
    if any(k in s for k in POS_KEYS):
        return "符合"
    return "部分符合"


def combine(statuses):
    valid = [s for s in statuses if s in RANK]
    if not valid:
        if statuses and all(s == "不适用" for s in statuses):
            return "不适用"
        return "未知"
    m = min(RANK[s] for s in valid)
    for k, v in RANK.items():
        if v == m:
            return k
    return "未知"

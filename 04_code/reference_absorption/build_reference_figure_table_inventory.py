"""Inventory every caption actually embedded in the reference PDF.

Descriptions below concern presentation roles only. Reference data and
numerical results are never imported into the project manuscript.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXTRACTION = Path(r"D:\work document\codex_work\f_reference_transfer\reference_pdf")
OUT = ROOT / "10_review/REFERENCE_FIGURE_TABLE_INVENTORY_v1.csv"

# number: question, type, demonstration, reasoning position, local equivalent,
# reproducible analogue from our evidence, relevant local source
FIG = {
    1: ("Overall", "流程图", "四问之间的数据与模型关系", "总体分析", "暂无总流程图", "是，可按本项目四问关系重绘", "08_paper/round8/FINAL_PAPER_OUTLINE_v1.md"),
    2: ("Q1", "流程图", "质量指标、冲突与配比模型的处理顺序", "问题分析", "有文字步骤，无图", "是，可按已确认流程重绘", "03_models/modeling_phase1/q1/round4/Q1_MODEL_SPEC_v1.md"),
    3: ("Q1", "分布/散点/条形组合", "预处理和指标定向的可视检查", "模型准备", "v3附录A1有字段合同，缺组合图", "是，已有独立补充Run的字段合同", "06_results/raw/Q1_TASK_REPAIR_20260925_v1/Q_FULL_FIELD_CONTRACT_v1.csv"),
    4: ("Q1", "小提琴图", "各领域质量摘要的分布差异", "模型求解", "v3图1五维画像及表3构造分", "是，限指定用途规则分与描述性分位", "06_results/raw/Q1_TASK_REPAIR_20260925_v1/Q_FULL_DOMAIN_RESULTS_v1.csv"),
    5: ("Q1", "对照/热图组合", "抽样和扩展域差及指标分歧", "模型求解", "v3表3、图1和冲突分类部分对应", "是，需保留非重叠ID与语义边界", "06_results/raw/Q1_TASK_REPAIR_20260925_v1/Q_FULL_DOMAIN_RESULTS_v1.csv"),
    6: ("Q1", "条形/热图/散点组合", "配比拟合与跨规模稳定性", "模型求解", "图2及扩写候选图10", "是，仅使用本项目A来源运行", "03_models/modeling_phase1/q1/round4/P_RESPONSE_VALIDATION_METRICS_v2.json"),
    7: ("Q2", "流程图", "规模律、质量与跨来源诊断的先后顺序", "问题分析", "有文字步骤，无图", "是，可按本模型证据层级重绘", "03_models/modeling_phase2/round5/Q2_LIMITATIONS_v1.md"),
    8: ("Q2", "双对数曲线", "规模律观测与拟合曲线", "模型求解", "FIG-Q2-R5-001已存在，未入Round8", "是，已有正式机器结果", "06_results/figures/round5/FIG-Q2-R5-001.png"),
    9: ("Q2", "质量响应曲线", "半合成质量项的表内拟合", "模型求解", "FIG-Q2-R5-004已存在，未入Round8", "是，仅作半合成诊断", "06_results/figures/round5/FIG-Q2-R5-004.png"),
    10: ("Q2", "边际曲线/热图", "弹性与等损失替代关系", "模型求解", "Round8图4", "是，已有正式机器结果", "06_results/figures/round5/FIG-Q2-R5-003.png"),
    11: ("Q2", "散点验证", "不同来源点与拟合量尺的偏差", "跨来源验证", "已有来源分开诊断数值，无此图", "是，须仅比较中心化形状", "06_results/raw/SCEN-Q2-R5-20260924-v3/external_shape_diagnostics.csv"),
    12: ("Q3", "流程图", "成本、约束、求解与敏感性链条", "问题分析", "有文字步骤，无图", "是，可按本项目机制重绘", "03_models/modeling_phase3/round6/Q3_MODEL_SPEC_v1.md"),
    13: ("Q3", "堆叠柱/转移图", "预算成本结构与活跃约束", "模型求解", "Round8图5有路径，缺成本份额", "是，需从本项目预算结果推导", "06_results/raw/EXP-Q3-BASE-R6-20260924-v1/budget_path.csv"),
    14: ("Q3", "多面板预算曲线", "N、D、Q随预算的配置变化", "模型求解", "Round8图5、图6对应", "是，已有完整51档预算和质量路径", "06_results/figures/round6/FIG-Q3-R6-001.png"),
    15: ("Q3", "成本/上下文敏感性曲线", "成本函数和上下文改变配置", "模型求解", "FIG-Q3-R6-004及图6对应", "是，已有正式情景结果", "06_results/figures/round6/FIG-Q3-R6-004.png"),
    16: ("Q4", "流程图", "能力前沿、桥接、分解与预测顺序", "问题分析", "有文字步骤，无图", "是，可按失败桥接后的实际路径重绘", "03_models/modeling_phase4/round7/Q4_FRONTIER_MODEL_SPEC_v1.md"),
    17: ("Q4", "散点图", "能力与参数规模的描述性关系", "模型求解", "Round8表10/图8部分对应", "是，限关联解释", "06_results/raw/EXP-Q4-R7-20260925-v1/decomposition_changes.csv"),
    18: ("Q4", "分解/桥接诊断组合", "规模关联分量及Loss桥接", "模型求解", "Round8图8；扩写候选图12", "是，但本项目桥接失败必须直示", "06_results/figures/round7/FIG-Q4-R7-003.png"),
    19: ("Q4", "时间序列/预测扇形", "历史前沿与未来条件预测", "模型求解", "Round8图9", "是，已有正式机器结果", "06_results/figures/round7/FIG-Q4-R7-005.png"),
    20: ("Q4", "任务条形对照", "六任务聚合的差异", "模型求解", "已计算六任务，Round8仅文字", "是，须以raw6原始得分重绘", "06_results/raw/EXP-Q4-R7-20260925-v1/frontier_family.csv"),
}

TAB = {
    1: ("Overall", "符号表", "变量与单位", "符号说明", "Round8表1", "是", "08_paper/round8/00_front.md"),
    2: ("Q1", "方法比较表", "综合评价候选的取舍", "模型准备", "扩写候选表13部分对应", "是，依据已运行DQ比较", "03_models/modeling_phase1/q1/round3/Q1_DESCRIPTIVE_QUALITY_COMPARISON_v1.md"),
    3: ("Q1", "结果表", "领域质量的摘要比较", "模型求解", "v3表3已列W0/W1/DQ0", "是，已有独立补充Run但只属构造评分", "06_results/raw/Q1_TASK_REPAIR_20260925_v1/Q_FULL_DOMAIN_RESULTS_v1.csv"),
    4: ("Q2", "方法比较表", "规模律候选的取舍", "模型准备", "Round8图3及扩写候选表13", "是，依据三类验证", "06_results/raw/EXP-Q2-ND-R5-20260924-v1/summary.json"),
    5: ("Q2", "参数表", "规模律参数的展示", "模型求解", "Round8表4", "是，仅用本项目估计", "06_results/raw/EXP-Q2-ND-R5-20260924-v1/summary.json"),
    6: ("Q3", "算法比较表", "求解器和解析法的用途", "模型准备", "扩写候选表13部分对应", "是，依据Q3数值QA", "07_validation/round6/Q3_VALIDATION_REPORT_v1.md"),
    7: ("Q3", "配置结果表", "预算代表点的N/D/Q/Loss", "模型求解", "Round8表7、表8", "是，已有正式配置结果", "06_results/raw/EXP-Q3-BASE-R6-20260924-v1/budget_path.csv"),
    8: ("Q4", "方法比较表", "前沿分析方法的适用性", "模型准备", "Round8表11及扩写候选表13", "是，依据已有滚动验证", "06_results/raw/EXP-Q4-R7-20260925-v1/rolling_metrics.csv"),
    9: ("Validation", "误差总结表", "各模型的检验数值", "集中模型检验", "扩写候选表14", "是，须分来源和检验对象", "07_validation/VALIDATION_REPORT.md"),
    10: ("Sensitivity", "灵敏度总结表", "因素变化与输出变化", "集中灵敏度", "扩写候选表15", "是，须区分参数与机制", "07_validation/round7/Q4_VALIDATION_REPORT_v1.md"),
    11: ("Appendix", "附件清单", "代码与中间结果索引", "附录", "Round8附录C为文字说明", "是，可登记本项目入口与Result ID", "04_code/paper_round8/build_paper.py"),
}


def main() -> None:
    data = json.loads((EXTRACTION / "structure_counts.json").read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    columns = ["Kind", "Figure No.", "Table No.", "Page", "Question", "Title", "Figure/Table type", "What it demonstrates", "Location in reasoning chain", "Whether our paper has equivalent", "Whether local data can reproduce analogous figure/table", "Local source"]
    with OUT.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for caption in data["captions"]:
            figure = caption["kind"] == "figure"
            meta = (FIG if figure else TAB)[caption["number"]]
            writer.writerow(dict(zip(columns, [
                "Figure" if figure else "Table",
                caption["number"] if figure else "",
                "" if figure else caption["number"],
                caption["page"], meta[0], caption["title"], *meta[1:],
            ])))
    print(f"figures={len(FIG)} tables={len(TAB)} rows={len(data['captions'])} output={OUT}")


if __name__ == "__main__":
    main()

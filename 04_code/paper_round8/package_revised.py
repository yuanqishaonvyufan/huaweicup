"""Build a compact, auditable supporting attachment for revised F paper."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'11_delivery/revised_v2';SRC=ROOT/'08_paper/revised_v2'
bm=json.loads((SRC/'BUILD_MANIFEST_v2.json').read_text(encoding='utf-8'))
sources=[
 '04_code/paper_round8/q1_task_repair.py','04_code/paper_round8/q4_task_repair.py',
 '04_code/paper_round8/revised_figures.py','04_code/paper_round8/build_paper.py',
 '04_code/paper_round8/qa_revised.py',
 '03_models/paper_repair/Q1_REPAIR_PREFIT_SPEC_v1.md',
 '03_models/paper_repair/Q1_TASK_REPAIR_RESULTS_v1.md',
 '03_models/paper_repair/Q4_REPAIR_PREFIT_SPEC_v1.md',
 '03_models/paper_repair/Q4_TASK_REPAIR_RESULTS_v1.md',
 '10_review/paper_repair/FINAL_TASK_FULFILLMENT_REPAIR_QA_v1.md',
 '10_review/paper_repair/FINAL_TASK_FULFILLMENT_REPAIR_QA_v1.json',
 '08_paper/revised_v2/FINAL_PAPER_EVIDENCE_MAP_v2.md',
 '11_delivery/revised_v2/DELIVERY_CHECKLIST_v2.md',
 '08_paper/revised_v2/BUILD_MANIFEST_v2.json',
 '08_paper/revised_v2/FINAL_EQUATION_REGISTRY_v2.json',
 '08_paper/revised_v2/FINAL_FIGURE_SELECTION_v2.json',
 '11_delivery/revised_v2/F_revised_draft_v2.md',
]
for rel in ['06_results/raw/Q1_TASK_REPAIR_20260925_v1','06_results/raw/Q4_TASK_REPAIR_20260925_v1']:
 sources.extend(str(p.relative_to(ROOT)).replace('\\','/') for p in (ROOT/rel).iterdir() if p.is_file())
sources.extend(str(p.relative_to(ROOT)).replace('\\','/') for p in (SRC/'figures').iterdir() if p.suffix in ['.png','.pdf','.json'])
tables={
 3:['Q1_TASK_REPAIR_20260925_v1/Q_FULL_DOMAIN_RESULTS_v1.csv','q1_task_repair.py'],
 4:['P_RESPONSE_VALIDATION_METRICS_v2.json','round4_validate_p_response.py'],
 5:['Q1_TASK_REPAIR_20260925_v1/A12_A15_EXTRAPOLATION_CHECK_v1.csv','q1_task_repair.py'],
 6:['EXP-Q2-ND-R5-20260924-v1/summary.json','round5_fit.py'],
 7:['EXP-Q2-ND-R5-20260924-v1/summary.json','round5_fit.py'],
 8:['SCEN-Q2-R5-20260924-v3/summary.json','round5_scenarios.py'],
 9:['EXP-Q3-BASE-R6-20260924-v1/budget_path.csv','round6_baseline.py'],
 10:['SCEN-Q3-R6-20260924-v1/quality_context_path.csv','round6_scenarios.py'],
 11:['EXP-Q4-R7-20260925-v1/bridge_validation.csv','round7_models.py'],
 12:['EXP-Q4-R7-20260925-v1/decomposition_changes.csv + robustness_variants.csv','round7_models.py'],
 13:['Q4_TASK_REPAIR_20260925_v1/summary.json','q4_task_repair.py'],
 14:['EXP-Q4-R7-20260925-v1/rolling_metrics.csv','round7_forecast.py'],
 15:['EXP-Q4-R7-20260925-v1/forecast_summary.json','round7_forecast.py'],
 16:['Q4_TASK_REPAIR_20260925_v1/EXOGENOUS_COMPUTE_SLOWDOWN_SCENARIOS_v1.csv','q4_task_repair.py'],
}
lines=['# 2稿图表与代码溯源','', '未列入压缩包的旧机器文件保留于完整仓库；原始附件由参赛队本地另行提供。','', '|表|正文任务|结果文件|程序|','|---:|---|---|---|']
for num,cap in enumerate(bm['table_captions'][:16],1):
 source,code=tables.get(num,['旧公式/来源定义','build_paper.py'])
 lines.append(f'|{num}|{cap}|{source}|{code}|')
lines+=['','|图|结果来源|图文件|','|---:|---|---|']
figs=json.loads((SRC/'FINAL_FIGURE_SELECTION_v2.json').read_text(encoding='utf-8'))
for f in figs:lines.append(f'|{f["number"]}|{f["paper_section"]}|{f["source"]}|')
lines+=['','公式1—24的逐式来源、符号、假设及正文位置见 `FINAL_EQUATION_REGISTRY_v2.json`。']
prov=SRC/'REVISED_PROVENANCE_v2.md';prov.write_text('\n'.join(lines)+'\n',encoding='utf-8')
sources.append(str(prov.relative_to(ROOT)).replace('\\','/'))
readme='''# F题2稿支撑附件

包含新增Q1/Q4的源码、输出、QA、公式图表追溯和4幅重新导出的图。论文PDF与DOCX在同级交付目录单独提供。

复算依赖仓库中原始只读附件、旧有效机器结果和Python numpy/pandas/scipy/matplotlib、生成DOCX用python-docx/latex2mathml。请先核对各摘要与此包清单的SHA256，再执行新增脚本；不得用估算外推或外生情景替代独立观测。旧冻结模型与结果需从同一Git提交取得，不包含在本压缩包内。

本包只是支撑资料候选，正式提交队伍仍需按竞赛系统规定填写身份及AI披露，并核对50MB限制。
'''
manifest={x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in sources}
zpath=OUT/'F_revised_support_v2.zip'
with ZipFile(zpath,'w',compression=ZIP_DEFLATED,compresslevel=6) as z:
 z.writestr('README.md',readme)
 z.writestr('SHA256_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2))
 for x in sources:z.write(ROOT/x,x)
with ZipFile(zpath) as z:
 assert z.testzip() is None
 for x,h in manifest.items():assert hashlib.sha256(z.read(x)).hexdigest()==h
assert zpath.stat().st_size<50*1024*1024
print(json.dumps({'zip':str(zpath),'bytes':zpath.stat().st_size,'files':len(sources),'sha256':hashlib.sha256(zpath.read_bytes()).hexdigest()},ensure_ascii=False))

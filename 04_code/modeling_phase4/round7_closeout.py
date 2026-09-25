from common import *
from round7_package import append_once
import importlib.metadata, platform, subprocess
def main():
    qa=json.loads((ROOT/'10_review/ROUND7_QA_v1.json').read_text('utf-8'))
    assert qa['verdict']=='PASS WITH DOCUMENT CORRECTIONS' and qa['pass_count']==qa['total']
    frozen=json.loads((ROOT/'02_analysis/consensus/Q3_TO_Q4_INTERFACE_FREEZE_v1.json').read_text('utf-8'))
    assert all(sha(ROOT/p)==h for p,h in frozen['files'].items()),'Inherited Gate4 frozen bytes changed'
    state='''# PROJECT_STATE

## 当前唯一权威状态 — Round7 / 2026-09-25

Q1/Q2/Q3/Q4: PROVISIONALLY CLOSED。Round7 COMPLETE；MODELING COMPLETE **WITH RESTRICTED EVIDENCE SCOPE**。Round8 PAPER INTEGRATION READY，仅允许受限结论进入正文。无Gate5流程；本轮不启动完整论文排版。

Round7 QA: PASS WITH DOCUMENT CORRECTIONS，42/42实现/证据链核查。新增缺陷P0/P1/P2=0/0/3，全部关闭；未解决实现缺陷0/0/0。无外部Opus/独立审稿者宣称。Gate4 PASS及Q1–Q3模型/接口原字节保持。

Q4主证据：853条C1/C8精确ID与参数核对、C9可用性筛选；C8 raw6等权能力，评测日期，28天窗口q90。历史36.45307→52.33272。主规格参数关联17.0233%、参数调整残差82.9767%，筛选/时间敏感性可反号；不是完整N–D贡献或因果技术比例。

Loss–Benchmark: NO RELIABLE BRIDGE，B0运行。完整N–D/真实compute-slowdown效应NOT IDENTIFIED。C1–C10全部审计，C8任务聚合完成；C3异口径历史不拼接，C4数据/算力/开放权重字段已审计，D覆盖不足。

Forecast origin2026-09-25，last evaluation2025-03-14，gap560天。2027-09-25条件中心79.75536，95%模型区间61.24205–90.40150；2028-09-25为87.12751，69.58019–95.56881。模型中心范围52.16860–83.77111 /52.33272–97.11295；不是CI。两期限EXTRAPOLATION-DOMINATED，只有4/13周回测，12/24月覆盖未经验证。三规模情景因S趋势非正而重合，不是现实算力约束无效的证据。

Q3仅条件N/D/源内Loss、活跃约束和等级；没有运输为历史或benchmark预测。B8、因果质量弹性、通用mix、1B运输、FLOPs货币成本、支持平台产业饱和全部禁入。Q1/Q2/Q3此前来源/识别/外推限制不变。

完成定义：可用数据上的审计、冻结规格、真实运算、负/不确定结论、受限论文包与QA完成；不表示所有题面因果量已识别，不升级为不受限FINAL模型或最终提交。Q4八项结果VALIDATED FOR RESTRICTED REPORTING。下一阶段保持上述限制，不因“MODELING COMPLETE”删除它们。

导航：03_models/modeling_phase4/round7/Q4_RESULTS_REPORT_v1.md；Q4_TO_PAPER_INTERFACE；07_validation/round7/Q4_VALIDATION_REPORT_v1.md；10_review/FINAL_MODELING_PRE_REVIEW_PACKAGE_v1.md；ROUND7_CHECKPOINT_LOG。CP0–CP3已远端核验，CP4及最终收据按日志/最终HEAD为准。
'''
    write(ROOT/'09_handoff/PROJECT_STATE.md',state)
    write(ROOT/'09_handoff/JOINT_CONTEXT.md',state.replace('# PROJECT_STATE','# JOINT_CONTEXT',1))
    write(ROOT/'09_handoff/NEXT_ACTION.md','''# NEXT_ACTION

ROUND8 — PAPER INTEGRATION READY（限定证据范围）。本轮Round7完成后停止，不开Gate5、不重开Q1–Q3。

先读 FINAL_MODELING_PRE_REVIEW_PACKAGE、Q4_TO_PAPER_INTERFACE、Q4_LIMITATIONS、42项QA。最多一次全文模型一致性单次核查，然后整合四问。保留“无可靠桥接 / 完整N–D与真实算力放缓不可识别 / 17%–83%不稳健 / 两期限远外推、覆盖未验证”。论文摘要不可写83%为真实技术贡献。使用真实登记结果和图表，区分C8 raw6与C1归一化分。Q1–Q3原受限等级保留。
''')
    write(ROOT/'09_handoff/SOL_CONTEXT.md','# SOL_CONTEXT\n\nRound7 researcher execution complete; see JOINT_CONTEXT for sole active state. No pending model run. Round8 integrate the qualified paper candidate only after user initiates next stage; current request ends at CP4 verified. No external-review claim.')
    write(ROOT/'09_handoff/OPUS_CONTEXT.md','# OPUS_CONTEXT\n\nNo Opus invocation or independent review occurred in Round7. Shared artifacts: JOINT_CONTEXT, FINAL_MODELING_PRE_REVIEW_PACKAGE, Q4_TO_PAPER_INTERFACE. Any later reviewer must preserve negative/inconclusive findings and need not reopen Q1–Q3 without a specific P0.')
    write(ROOT/'03_models/q4/MODEL_INTERFACE.md','''# Q4 MODEL_INTERFACE

ACTIVE / PROVISIONALLY CLOSED, R7-SPEC-001 and R7-CLOSE-001. Source spec: 03_models/modeling_phase4/round7/Q4_FRONTIER_MODEL_SPEC_v1.md and bridge spec. Run EXP-Q4-R7-20260925-v1, 42-check QA PASS WITH DOCUMENT CORRECTIONS.

INPUT: audited C1–C10, primary exact-ID C1/C8 and C9 screen; C3 comparability/C4 metadata; restricted Q3 mechanism only.
MODEL: 28-day raw6 q90 evaluation frontier; OLS parameter/type/family/time descriptive decomposition; logit dynamic selected at4/13week rolling horizons. Bridge B0 after high-stratum validation failure.
OUTPUT: descriptive N-only parameter share and residual with failed robustness; conditional 2027/2028 forecasts and separate statistical/model/scenario uncertainty. Full ND scale/non-scale and real compute slowdown NOT IDENTIFIED. No reliable Loss transport.
FINAL STATUS: restricted provisional reporting; no unrestricted causal/final benchmark claim. Paper interface and registry are authoritative. Q4 model package complete, manuscript integration remains Round8.
''')
    package='''# Final modeling pre-review package v1

ACTIVE — R7-CLOSE-001 / 2026-09-25. Q1–Q4 PROVISIONALLY CLOSED; MODELING COMPLETE WITH RESTRICTED EVIDENCE SCOPE; READY Round8. No Gate5. One optional single-pass whole-model consistency check at paper integration, not a new multi-round gate.

| Question | Accepted evidence | Mandatory limitation | Navigation |
|---|---|---|---|
| Q1 | descriptive quality/13-domain recipe model and held-out scale tests | quality-loss pairing absent;1M local,60M partial,1B failed | Gate2 consensus; Q1 frozen reports |
| Q2 | B1 source-internal N–D law and explicit quality/mixture scenarios | external Loss provenance unresolved; semi-synthetic quality not causal | modeling_phase2/round5/Q2_RESULTS_REPORT and LIMITATIONS |
| Q3 | conditional resource optima with costs/support/uncertainty | FLOPs proxy not money; support cap not industry saturation; no real quality elasticity | GATE4_CONSENSUS; frozen Q3_TO_Q4 |
| Q4 | audited raw6 frontier, parameter/residual accounting, short rolling validation, conditional long forecasts | NO RELIABLE BRIDGE; full ND/compute slowdown unidentified; share unstable;560-day gap | modeling_phase4/round7 reports; 42-check QA |

Q4 evidence path: official visible body + raw SHA → entity table/C8 task data → frozen specs/config → EXP-Q4-R7-20260925-v1 raw outputs → 07_validation/round7 → eight restricted registry results → Chinese paper candidate. All C files hashed; raw unchanged; Q1–Q3 not refitted or mutated. Eight PNG/SVG figures and seven tables with source manifests available.

QA verdict PASS WITH DOCUMENT CORRECTIONS;42/42 checks. Initial Q3 derived-copy precision failure saved separately, fixed by preserving source decimal strings without any model refit. New P0/P1/P2=0/0/3 all closed. Bridge predictivity and contribution stability did NOT pass: preserved as research findings, not converted to successful validation. Source data gaps remain scientific limitations, not solved defects.

2026-09-25 origin targets2027-09-25 and2028-09-25:79.75536[61.24205,90.40150] and87.12751[69.58019,95.56881], conditional diffusion95% PI only. Model central envelopes52.16860–83.77111 /52.33272–97.11295 separately. Raw6 scale not normalized C1. Positive parameter-growth scenarios collapse; do not infer compute slowdown harmless. Full causal technology percentages NOT IDENTIFIED. Any paper use must retain these conditions.

Next action: Round8 paper integration under Q4_TO_PAPER_INTERFACE. Do not start full layout in Round7. No external Opus, second account, or peer-review claim; single-agent execution plus independent arithmetic recomputation and visual inspection.
'''
    write(ROOT/'10_review/FINAL_MODELING_PRE_REVIEW_PACKAGE_v1.md',package)
    write(ROOT/'09_handoff/ROUND7_TO_ROUND8_HANDOFF_v1.md',package.replace('# Final modeling pre-review package v1','# Round7 to Round8 handoff v1',1))
    append_once(ROOT/'09_handoff/DECISION_LOG.md','## R7-CLOSE-001 — restricted provisional closure','42/42 lineage/arithmetic QA PASS WITH DOCUMENT CORRECTIONS. Q4 PROVISIONALLY CLOSED and MODELING COMPLETE only for the qualified model package; full ND/real compute-slowdown/causal technology remain unidentified. Bridge rejected, share unstable, long forecasts extrapolation-dominated; no unrestricted final-model promotion. Round8 READY, no Gate5. This is researcher execution within explicit user authorization, not external consensus.')
    append_once(ROOT/'09_handoff/STAGE_GATES.md','## Round7 superseding status','Q4 formulation/computation/qualified evidence package COMPLETE; QA42/42. MODELING COMPLETE WITH RESTRICTED EVIDENCE SCOPE; Q1–Q4 PROVISIONALLY CLOSED. Round8 manuscript integration READY, not executed. Negative/unidentified findings remain mandatory; earlier current-status paragraphs are historical.')
    append_once(ROOT/'09_handoff/OPEN_QUESTIONS.md','## Round7 disposition of Q4 questions','OQ-006 resolved as explicit filtering/evaluation-time/raw6 frontier specification. OQ-009 quantitative bridge rejected for operational forecasting; full source-unified mapping remains unsupported. Full ND contribution, actual compute slowdown and empirical long-horizon coverage remain NOT IDENTIFIED. These are retained paper limitations, not further Round7 fitting promises.')
    append_once(ROOT/'02_analysis/consensus/JOINT_WORK_LOG.md','## Round7 researcher execution','User-authorized end-to-end Round7; no independent Opus call. R7-AUTH-001 → audited data → R7-SPEC-001 freeze → CP2/CP3 runs → 42-item QA and visual checks → R7-CLOSE-001. Negative bridge and robustness results retained; Q1–Q3 frozen. Shared handoff updated for Round8.')
    append_once(ROOT/'07_validation/VALIDATION_REPORT.md','## Round7 current validation','QA-Q4-R7-20260925-v1: PASS WITH DOCUMENT CORRECTIONS;42/42 implementation/lineage checks. Three closed P2 corrections. Scope explicitly excludes reliable bridge, causal/full ND shares and empirical long-horizon coverage. See round7/Q4_VALIDATION_REPORT_v1.md. Modeling package complete; paper integration next.')
    readme=ROOT/'README.md';s=readme.read_text('utf-8');s=s.replace('\n','\n\n**当前 Round7 COMPLETE / Q4 PROVISIONALLY CLOSED（受限）/ MODELING COMPLETE WITH RESTRICTED EVIDENCE SCOPE；Round8 READY。** 42项QA通过，桥接不可靠、完整N–D贡献不可识别、分解不稳健、远期仅条件外推。详[结果](03_models/modeling_phase4/round7/Q4_RESULTS_REPORT_v1.md)和[总交接](10_review/FINAL_MODELING_PRE_REVIEW_PACKAGE_v1.md)。下面旧状态为历史。\n',1);write(readme,s)
    append_once(ROOT/'09_handoff/ROUND7_CHECKPOINT_LOG.md','CP3 VERIFIED: cc34495a2b1902b3a84adde8241847443161ac44 = remote main.','CP4 ready: paper-ready Q4,42/42 QA,8 figures,7 tables,registries and final-modeling handoff. Final receipt will record verified CP4 hash. Numerical outputs retained; Q3 derived copy corrected for exact decimal preservation only.')
    dump(ROOT/'10_review/ROUND7_VISUAL_QA_v1.json',{'status':'PASS','review':'view_image contact sheet of all8; individual002/008 after repair','findings_corrected':['dense date ticks on002','scenario figure uses increments not arbitrary absolute component partition'],'limits':'final embedded-paper size not checked until Round8','figure_manifest_sha256':sha(ROOT/'06_results/figures/round7/figure_manifest.json')})
    packages={p:importlib.metadata.version(p) for p in ['numpy','pandas','scipy','matplotlib','PyMuPDF','pyarrow']}
    code={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in (ROOT/'04_code/modeling_phase4').glob('*.py')}
    files={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for folder in [OUT,SPEC,ROOT/'06_results/figures/round7',ROOT/'06_results/tables/round7'] for p in folder.glob('*') if p.is_file()}
    dump(ROOT/'10_review/ROUND7_REPRODUCIBILITY_MANIFEST_v1.json',{'run':'EXP-Q4-R7-20260925-v1','python':platform.python_version(),'packages':packages,'seed':20260925,'code':code,'files':files,'raw_mapping_sha256':sha(AUD/'Q4_C1_C10_ROLE_MATRIX_v1.json'),'input_manifest_sha256':sha(DATA/'INPUT_MANIFEST_v1.json'),'config_sha256':sha(ROOT/'05_experiments/configs/Q4_R7_FROZEN_v1.json'),'inherited_gate4_verified':frozen['files'],'numerical_execution_code_git_refs':{'models':'10c30f90549fe85f9ef298d9e965c651dc887e50','forecast':'cc34495a2b1902b3a84adde8241847443161ac44'},'CP4_code_changes':'forecast Q3 copier preserves source decimal strings; no forecast numerical formula changed','qa':'42/42; per-check machine JSON','no_external_reviewer':True})
    cm=ROOT/'04_code/code_manifest.json';v=json.loads(cm.read_text('utf-8'));v['round7']={'scope':'qualified Q4 completed','entry':'04_code/modeling_phase4/round7_models.py','files':[{'path':p,'sha256':h,'core_appendix':p.endswith(('round7_models.py','round7_forecast.py'))} for p,h in code.items()],'full_manifest':'10_review/ROUND7_REPRODUCIBILITY_MANIFEST_v1.json'};dump(cm,v)
    print('Restricted closeout and complete handoff written; Gate4 frozen SHA verified')
if __name__=='__main__':main()

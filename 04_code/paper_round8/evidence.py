"""Read frozen outputs and prepare the final paper evidence package; no fitting.
AI-assisted authoring: Codex / GPT-6, OpenAI; release date not independently verified.
"""
from pathlib import Path
import json, csv, hashlib, subprocess, re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '08_paper/round8'
OUT.mkdir(parents=True, exist_ok=True)
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def rows(p): return list(csv.DictReader((ROOT/p).open(encoding='utf-8-sig', newline='')))
def write(name, text): (OUT/name).write_text(text, encoding='utf-8')
Q1='03_models/modeling_phase1/q1/round4/'
R='06_results/raw/'
q1=read(Q1+'P_RESPONSE_VALIDATION_METRICS_v2.json')
q2=read(R+'EXP-Q2-ND-R5-20260924-v1/summary.json')
qs=read(R+'SCEN-Q2-R5-20260924-v3/summary.json')
q3=read(R+'EXP-Q3-BASE-R6-20260924-v1/summary.json')
q4=read(R+'EXP-Q4-R7-20260925-v1/forecast_summary.json')
claims=[]
def add(cid,q,claim,value,formula,source,rid,run,grade,allowed,forbidden,section,support,selector):
 claims.append(dict(claim_id=cid,question=q,exact_claim=claim,numerical_value=value,formula=formula,source_file=source,result_id=rid,run=run,evidence_grade=grade,allowed_wording=allowed,forbidden_wording=forbidden,paper_section=section,figure_table_support=support,selector=selector,source_sha256=hashlib.sha256((ROOT/source).read_bytes()).hexdigest()))
def a(cid,q,claim,value,source,rid,grade,section,support,selector,formula='见公式登记',allowed='限附件内部及规定用途',forbidden='普适因果结论'):
 run=q1['run_id'] if q==1 else ('EXP-Q2-ND-R5-20260924-v1' if q==2 else 'EXP-Q3-BASE-R6-20260924-v1' if q==3 else q4['run_id'])
 if 'SCEN-' in source: run=source.split('/')[2]
 add(cid,q,claim,value,formula,source,rid,run,grade,allowed,forbidden,section,support,selector)
src=Q1+'P_RESPONSE_VALIDATION_METRICS_v2.json'
a('E01',1,'1M R0留出误差', {m:q1['metrics']['1M'][m]['R0_RMSE_raw'] for m in ['M0','M1']},src,'CAND-Q1-R4-VAL-001','PAPER CORE','5.3','图2 表3','metrics/1M/*/R0_RMSE_raw')
a('E02',1,'1M逐域误差及全部改善', {'M0':q1['metrics']['1M']['M0']['domain_RMSE_raw'],'M1':q1['metrics']['1M']['M1']['domain_RMSE_raw'],'improved':sum(a<b for a,b in zip(q1['metrics']['1M']['M1']['domain_RMSE_raw'],q1['metrics']['1M']['M0']['domain_RMSE_raw']))},src,'CAND-Q1-R4-VAL-002','PAPER CORE','5.3','图2 附录B','metrics/1M/*/domain_RMSE_raw')
a('E03',1,'中心化规模迁移误差比',{s:q1['metrics'][s]['M1']['R0_centered_RMSE_ratio_to_M0'] for s in ['60M','1B']},src,'CAND-Q1-R4-TRANSFER-001','PAPER CORE','5.4','表3','metrics/*/M1/R0_centered_RMSE_ratio_to_M0',allowed='60M部分中心化迁移；1B失败',forbidden='1B绝对预测通过')
a('E04',1,'经验支持分类',q1['support_counts'],src,'CAND-Q1-R4-SUPPORT-001','PAPER CORE','5.4','表3','support_counts',allowed='凸包和近邻支持',forbidden='真实供给可实施保证')
a('E05',1,'全22项角色与记录规模',read(Q1+'Q1_QUALITY_CLOSURE_METRICS_v1.json')['role_counts'],Q1+'Q1_QUALITY_CLOSURE_METRICS_v1.json','CAND-Q1-R4-QUAL-001','PAPER CORE','5.1','图1 附录A','role_counts')
a('E06',1,'确认语义冲突为0','0；统计分歧与域反转另列','01_data/audits/modeling_phase1/q1/QUALITY_CONFLICT_CANDIDATES_v1.md','AUDIT-Q1-SEMANTICS-CONFLICT-20260924-v1','PAPER SUPPORTING','5.2','图1','正式审计报告',allowed='已核候选未确认语义冲突',forbidden='负相关即语义冲突')
src=R+'EXP-Q2-ND-R5-20260924-v1/summary.json'
a('E07',2,'五参数加性幂律',q2['parameters'],src,'CAND-Q2-R5-ND-001','PAPER CORE','6.1','表4','parameters',formula='L∞+A N^(-α)+B D^(-β)；N,D均十亿')
a('E08',2,'三类分组验证',q2['validation'],src,'CAND-Q2-R5-VAL-001','PAPER CORE','6.2','图3 表5','validation',allowed='附件内部误差很低',forbidden='真实世界预测精度极高')
a('E09',2,'参数稳定性',q2['full_fit'],src,'CAND-Q2-R5-UNC-001','SENSITIVITY ONLY','6.2','表4','full_fit')
a('E10',2,'示例点导数弹性与替代',rows(R+'EXP-Q2-ND-R5-20260924-v1/marginal_effects.csv'),R+'EXP-Q2-ND-R5-20260924-v1/marginal_effects.csv','CAND-Q2-R5-MARG-001','PAPER CORE','6.3','图4','N=1,D=100',formula='εN=-αU/L；εD=-βV/L；dlnD/dlnN=-αU/(βV)')
src=R+'SCEN-Q2-R5-20260924-v3/summary.json'
a('E11',2,'B7半合成质量校准',{k:qs[k] for k in ['quality_common_g','quality_negative_cells','quality_cells','quality_centered_LOO_macro_RMSE']},src,'CAND-Q2-R5-QUAL-001','PAPER CORE','6.4','表6','quality_*',allowed='题目半合成质量表内校准',forbidden='真实因果质量弹性')
a('E12',2,'跨来源中心化形状诊断',qs['external_summary'],src,'CAND-Q2-R5-EXT-001','PAPER SUPPORTING','6.2','表6','external_summary',allowed='目标均值中心化的事后形状检查',forbidden='外部绝对Loss验证成功')
a('E13',2,'有限质量替代条件',rows(R+'SCEN-Q2-R5-20260924-v3/quality_substitution_scenarios.csv'),R+'SCEN-Q2-R5-20260924-v3/quality_substitution_scenarios.csv','SCEN-Q2-R5-SUB-001','SCENARIO ONLY','6.4','表6','N=1,D=100,lambda=1',allowed='假设量尺可运输时的条件替代',forbidden='真实资源节省')
src=R+'EXP-Q3-BASE-R6-20260924-v1/budget_path.csv'
a('E14',3,'三个预算配置',[x for x in rows(src) if float(x['Budget_FLOPs']) in [1e19,1e22,1e24]],src,'CAND-Q3-R6-BASE-001','PAPER CORE','7.2','图5 表7','Budget_FLOPs=1e19,1e22,1e24',allowed='题设成本与统计支持范围内最优',forbidden='现实产业最优')
a('E15',3,'支持约束结构转移',q3['transitions'],R+'EXP-Q3-BASE-R6-20260924-v1/summary.json','CAND-Q3-R6-SHIFT-001','PAPER CORE','7.2','图5','transitions',allowed='D上界先激活，两上界随后同时活跃',forbidden='数据300B后不再有价值')
a('E16',3,'解析与数值求解一致',{k:q3[k] for k in ['rows','numeric_starts','max_loss_gap','max_kkt']},R+'EXP-Q3-BASE-R6-20260924-v1/summary.json','CAND-Q3-R6-BASE-001','PAPER SUPPORTING','7.2','表7','rows/numeric_starts/max_loss_gap/max_kkt')
for cid,fn,rid,claim in [('E17','quality_scenarios.csv','SCEN-Q3-R6-QUAL-001','三类质量成本情景'),('E18','quality_break_even.csv','SCEN-Q3-R6-BREAK-001','局部与全局启动门槛'),('E19','context_baseline.csv','SCEN-Q3-R6-CTX-001','外生上下文比较')]:
 p=R+'SCEN-Q3-R6-20260924-v1/'+fn
 if (ROOT/p).exists(): a(cid,3,claim,rows(p),p,rid,'SCENARIO ONLY','7.3—7.5','图6 表8',fn,allowed='条件情景',forbidden='实测成本收益或窗口推荐')
a('E20',3,'联合参数传播','200联合向量；51000配置', '06_results/RESULTS_REGISTRY.md','SENS-Q3-R6-UNC-001','SENSITIVITY ONLY','7.6','图7','Round6 CP4',allowed='条件参数敏感性；情景包络另报',forbidden='情景包络是置信区间')
src=R+'EXP-Q4-R7-20260925-v1/decomposition_changes.csv'
a('E21',4,'参数关联与调整残差分解',rows(src),src,'Q4-R7-002','PAPER CORE','8.3','图8 表10','model=family',formula='ΔF=ΔS+ΔR',allowed='指定样本窗口下描述性分解',forbidden='82.98%由技术创新因果造成')
src=R+'EXP-Q4-R7-20260925-v1/bridge_validation.csv'
a('E22',4,'桥接未通过', [x for x in rows(src) if x['family']=='HIGH_pythia'],src,'Q4-R7-003','PAPER CORE','8.2','表9','HIGH_pythia/LOSO',allowed='无可靠桥接，能力直接预测',forbidden='弱定量桥接仍成立')
src=R+'EXP-Q4-R7-20260925-v1/rolling_metrics.csv'
a('E23',4,'短期限滚动回测',rows(src),src,'Q4-R7-004','PAPER CORE','8.4','表11','model=logit',allowed='4/13周回溯滚动验证',forbidden='12/24月预测已验证')
src=R+'EXP-Q4-R7-20260925-v1/forecast_summary.json'
a('E24',4,'两期限条件预测与区间',q4['forecast'],src,'Q4-R7-005;Q4-R7-007','PAPER CORE','8.5','图9 表12','forecast',allowed='远外推条件中心及模型区间；中心范围另报',forbidden='高可信确定预测')
a('E25',4,'数据截止与预测原点',{k:q4[k] for k in ['origin','last_data','gap_days']},src,'Q4-R7-005','PAPER CORE','8.5','图9 表12','origin,last_data,gap_days',allowed='560天空档；长期外推',forbidden='以最新产业观测为条件')
a('E26',4,'规模情景重合',q4['scale_slope_week'],src,'Q4-R7-008','SCENARIO ONLY','8.5','表12','scale_slope_week',formula='A(h)=max(0,bS h)=0',allowed='正增长情景不能区分',forbidden='真实算力放缓不影响能力')
src=R+'EXP-Q4-R7-20260925-v1/robustness_variants.csv'
a('E27',4,'筛选和时间窗口下分解反号',rows(src),src,'Q4-R7-006','PAPER CORE','8.3','表10','known_families/strict_license/start_2024_09/window_56d',allowed='分解比例不稳健',forbidden='稳健因果技术归因')
src=R+'EXP-Q4-R7-20260925-v1/frontier_family.csv'
fr=rows(src)
a('E28',4,'历史同口径前沿端点',[fr[0],fr[-1]],src,'Q4-R7-001','PAPER CORE','8.1','图8','first,last',formula='C8六维原始均值；28天q90；0—100分',allowed='评测群体高分位前沿',forbidden='全生态历史最高分')
write('FINAL_PAPER_EVIDENCE_MAP_v1.json',json.dumps(claims,ensure_ascii=False,indent=2))
lines=['# Final paper evidence map v1','', '起点 HEAD: '+subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'','只读取有效冻结产物；不重训、不修改机器结果。摘要核心结论必须携带所列限制。']
for x in claims:
 lines += ['','## '+x['claim_id']+' '+x['exact_claim']]+[f'- **{k}**: '+(json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else str(v)) for k,v in x.items() if k not in ['claim_id','exact_claim','numerical_value']]
 val=json.dumps(x['numerical_value'],ensure_ascii=False)
 lines += ['- **Numerical value**: '+(val if len(val)<3000 else '完整值与逐行记录见同名 JSON；源文件及选择器如上。')]
write('FINAL_PAPER_EVIDENCE_MAP_v1.md','\n'.join(lines)+'\n')
write('FINAL_RESULT_WHITELIST_v1.md','# Final result whitelist\n\n'+ '\n'.join(f"- {x['claim_id']} | {x['result_id']} | {x['evidence_grade']} | {x['allowed_wording']}；禁止：{x['forbidden_wording']}" for x in claims)+'\n\n## DO NOT USE AS MAIN CLAIM\n失败Q1验证v1、Q2情景v1/v2；B8隔离证据；被替代结果；外部Pythia普适定律；真实Q因果弹性；1B配比运输；全单纯形可实施最优；完整N–D因果技术贡献；实际算力放缓已识别；12/24月经验覆盖保证。\n')
write('FINAL_PAPER_OUTLINE_v1.md','''# 最终论文结构

封皮：保留官方模板四个标识，身份字段暂空。摘要页开始连续页码。
摘要：四问方法、真实数字、验证与边界；最后编写。
1 问题重述
2 问题分析
3 符号说明与模型假设
4 数据预处理与证据范围
5 问题一 多维质量与领域配比
6 问题二 来源分层的广义标度律
7 问题三 支持域约束下的资源配置
8 问题四 能力前沿分解与条件预测
9 模型评价与局限性
10 结论
参考文献
附录A 完整22项信号与处理
附录B 13领域留出误差
附录C 求解与复现说明及AI使用披露

不增加无信息公式或装饰图。核心验证和负结果留在正文。
官方AI规则优先于“删除工具痕迹”的内部泛化措辞；工具说明不含参赛者身份。
论文为FINAL CANDIDATE；未填写队伍信息、未经队员理解及改写确认前不能称已满足正式提交全部条件。
''')
symbols=[('N','模型参数量','十亿参数'),('D','同口径训练token数','十亿token'),('C','题设总算力预算','FLOPs'),('c','C/10^18','归一化预算'),('L_ctx','外生上下文长度','token'),('L_B','B1来源的交叉熵Loss','附件原表量尺'),('L_m','A来源第m验证领域Loss','A原表量尺'),('L∞,A,B,α,β','幂律截距、幅度、指数','幅度对应N/D十亿单位；指数无量纲'),('p','17维领域配比','非负且和为1'),('u,DQ0','五维描述分位与等权摘要','[0,1]；不等同Q'),('Q,Q0','半合成质量情景刻度及参考值','[0.5,1]，Q0=0.5'),('g(Q),r(Q)','题设质量成本及增量/10^9','FLOPs/token；归一化'),('h_Q','条件质量收益幅度','B1 Loss/单位Q'),('η','注意力成本系数','0.0002/token'),('μ','归一预算乘子','Loss/10^18 FLOPs'),('y,F','C8六维综合得分与群体q90','0—100分'),('S,R','参数关联分量与调整残差','分'),('θ_N','Q4对lnN的回归系数','分/lnN，区别于β'),('t,h','历史时间与未来期限','历史回归年；预测h周，逐式注明')]
write('FINAL_SYMBOL_TABLE_v1.md','# 最终符号表\n\n|符号|定义|单位及限制|\n|---|---|---|\n'+'\n'.join('|'+ '|'.join(s)+'|' for s in symbols)+'\n')
frozen_dirs=['01_data','02_analysis/consensus','03_models','05_experiments','06_results','07_validation']
snapshot=subprocess.check_output(['git','ls-tree','-r','HEAD','--',*frozen_dirs],cwd=ROOT,text=True)
write('FROZEN_MODEL_GIT_TREE_v1.txt',snapshot)
print(f'Prepared {len(claims)} claims; no model code executed.')

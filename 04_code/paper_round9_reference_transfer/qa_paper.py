"""Read-only manuscript and frozen-result QA. Does not train or optimize.
AI-assisted code: Codex / GPT-6, OpenAI; release date independently unverified.
"""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from pypdf import PdfReader
import re,json,csv,hashlib,subprocess,math,sys
ROOT=Path(__file__).resolve().parents[2];S=ROOT/'08_paper/round9_reference_transfer';O=ROOT/'11_delivery/round9_reference_transfer';Q=ROOT/'10_review/round9_reference_transfer';Q.mkdir(exist_ok=True)
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def csvs(p):return list(csv.DictReader((ROOT/p).open(encoding='utf-8-sig',newline='')))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
text=(O/'F_reference_transfer_v1.md').read_text(encoding='utf-8');checks=[]
def check(name,ok,detail=''):checks.append(dict(check=name,pass_=bool(ok),detail=detail))
def token(value,decimals,source,label):
 formatted=f'{value:.{decimals}f}'
 ok=formatted in text.replace('−','-')
 check(label,ok,dict(display=formatted,value=value,source=source))
q1p='03_models/modeling_phase1/q1/round4/P_RESPONSE_VALIDATION_METRICS_v2.json';q1=load(q1p)
for m in ['M0','M1']:token(q1['metrics']['1M'][m]['R0_RMSE_raw'],4,q1p,'Q1_R0_'+m)
for sc,dp in [('60M',4),('1B',3)]:token(q1['metrics'][sc]['M1']['R0_centered_RMSE_ratio_to_M0'],dp,q1p,'Q1_transfer_'+sc)
check('Q1_13_of_13',sum(a<b for a,b in zip(q1['metrics']['1M']['M1']['domain_RMSE_raw'],q1['metrics']['1M']['M0']['domain_RMSE_raw']))==13 and '13/13' in text)
check('Q1_support_2_of_256',q1['support_counts']['1M']['IN_SUPPORT']==2 and q1['validation_counts']['1M']==256 and '2/256' in text)
q2p='06_results/raw/EXP-Q2-ND-R5-20260924-v1/summary.json';q2=load(q2p)
for k,v in q2['parameters'].items():token(v,8,q2p,'Q2_parameter_'+k)
for k in ['LONO','FORWARD','BLOCK2D']:token(q2['validation'][k]['S1']['macro_rmse'],12,q2p,'Q2_validation_'+k)
for k,vals in q2['parameter_conditional_interval'].items():
 for v in [vals[0],vals[-1]]:token(v,5 if k in ['E','B'] else 6,q2p,'Q2_interval_'+k)
sp='06_results/raw/SCEN-Q2-R5-20260924-v3/summary.json';s=load(sp)
token(-s['quality_common_g'],6,sp,'Q2_quality_slope')
check('Q2_45_negative_cells',s['quality_negative_cells']==s['quality_cells']==45 and '45/45' in text)
for k,v in s['external_summary'].items():
 if v['median_centered_ratio'] is not None:token(v['median_centered_ratio'],6,sp,'Q2_external_'+k)
q3p='06_results/raw/EXP-Q3-BASE-R6-20260924-v1/budget_path.csv';q3=csvs(q3p)
for r in q3:
 if float(r['Budget_FLOPs']) in [1e19,1e22,1e24]:
  for k in ['N_B','D_B','loss']:
   token(float(r[k]),3 if k=='D_B' and float(r[k])>299 else 6,q3p,f'Q3_{r["Budget_FLOPs"]}_{k}')
  N,D=float(r['N_B']),float(r['D_B']);v=q2['parameters'];val=v['E']+v['A']*N**(-v['alpha'])+v['B']*D**(-v['beta'])
  check('Q3_saved_target_arithmetic_'+r['Budget_FLOPs'],abs(val-float(r['loss']))<1e-10)
qp='06_results/raw/SCEN-Q3-R6-20260924-v1/quality_context_path.csv'
for r in csvs(qp):
 if float(r['Budget_FLOPs'])==1e19 and r['L_ctx']=='2048' and float(r['factor'])==1 and float(r['qcap'])==1:
  for k in ['N_B','D_B','Q','loss']:token(float(r[k]),6,qp,'Q3_quality_'+r['cost_family']+'_'+k)
q4p='06_results/raw/EXP-Q4-R7-20260925-v1/forecast_summary.json';q4=load(q4p)
for r in q4['forecast']:
 check('Q4_target_'+r['target'],r['target'] in text)
 for name,vs in [('central',[r['central']]),('PI',r['conditional_PI95']),('model_range',r['model_range'])]:
  for j,v in enumerate(vs):token(v,2,q4p,f'Q4_{r["target"]}_{name}_{j}')
check('Q4_560_day_gap',q4['gap_days']==560 and '560' in text)
dp='06_results/raw/EXP-Q4-R7-20260925-v1/decomposition_changes.csv';d=next(x for x in csvs(dp) if x['model']=='family')
for k,nd in [('delta_S',6),('delta_R',6),('beta_logN',6)]:token(float(d[k]),nd,dp,'Q4_decomposition_'+k)
for k in ['parameter_share','residual_share']:token(float(d[k])*100,4,dp,'Q4_decomposition_'+k)
check('Q4_additive_identity',abs(float(d['delta_F'])-float(d['delta_S'])-float(d['delta_R']))<1e-12)
bp='06_results/raw/EXP-Q4-R7-20260925-v1/bridge_validation.csv'
for r in csvs(bp):
 if r['family']=='HIGH_pythia' and r['split']=='LOSO':token(float(r['rmse']),6,bp,'Q4_bridge_'+r['method'])
rp='06_results/raw/EXP-Q4-R7-20260925-v1/rolling_metrics.csv'
for r in csvs(rp):token(float(r['MAE']),6,rp,'Q4_rolling_'+r['model']+'_'+r['horizon_weeks'])
vp='06_results/raw/EXP-Q4-R7-20260925-v1/robustness_variants.csv'
for r in csvs(vp):
 if r['variant'] in ['known_families','strict_license','start_2024_09'] and r['target']=='2027-09-25':token(float(r['parameter_share'])*100,2,vp,'Q4_reversal_'+r['variant'])
# All copied claims still point to byte-identical sources.
claims=load('08_paper/round9_reference_transfer/FINAL_PAPER_EVIDENCE_MAP_v2.json')
check('evidence_sources_unchanged',all(hashlib.sha256((ROOT/x['source_file']).read_bytes()).hexdigest()==x['source_sha256'] for x in claims))
snap=(S/'FROZEN_MODEL_GIT_TREE_v1.txt').read_text(encoding='utf-8')
now=subprocess.check_output(['git','ls-tree','-r','HEAD','--','01_data','02_analysis/consensus','03_models','05_experiments','06_results','07_validation'],cwd=ROOT,text=True)
check('all_frozen_models_results_and_data_unchanged',snap==now)
check('no_model_code_modified',not subprocess.check_output(['git','diff','029b51e','--','04_code/modeling_phase1','04_code/modeling_phase2','04_code/modeling_phase3','04_code/modeling_phase4'],cwd=ROOT,text=True))
eq=load('08_paper/round9_reference_transfer/FINAL_EQUATION_REGISTRY_v1.json');fig=load('08_paper/round9_reference_transfer/FINAL_FIGURE_SELECTION_v1.json');bm=load('08_paper/round9_reference_transfer/BUILD_MANIFEST_v1.json')
check('equations_1_to_24', [e['number'] for e in eq]==list(range(1,25)))
check('figure_count_and_sources',len(fig)==13 and all(hashlib.sha256((ROOT/f['source']).read_bytes()).hexdigest()==f['sha256'] for f in fig))
check('tables_15_main_2_appendix',bm['tables']==17)
for n in range(1,14):check('figure_reference_'+str(n),bool(re.search('图'+str(n)+r'(?!\d)',re.sub(r'!\[.*?\]\(.*?\)','',text))))
for n in range(1,16):check('table_reference_'+str(n),len(re.findall('表'+str(n)+r'(?!\d)',text))>=2)
# Explicit scientific boundary review: negatives are intentional, not banned-word deletion.
required=['1B迁移失败','桥接未通过','统计支持上限','半合成','560','不能解释为','不能推出真实算力放缓','不具有抽样置信区间','没有概率覆盖含义']
compact=re.sub(r'\s+','',text)
for phrase in required:check('boundary_'+phrase,phrase in compact)
check('no_internal_workflow_prose',not re.search(r'Gate\s*[1-4]|Round\s*[1-8]|handoff|registry|GitHub|P0级|Sol /',text))
check('reference_order', [int(x) for x in re.findall(r'^\[(\d+)\]',text,re.M)]==[1,2,3,4])
for n in range(1,5):check('reference_cited_'+str(n),f'[{n}]' in text.split('# 参考文献')[0])
with ZipFile(O/'F_reference_transfer_v1.docx') as z:
 xml=etree.fromstring(z.read('word/document.xml'));ns={'m':'http://schemas.openxmlformats.org/officeDocument/2006/math','w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
 check('OMML_no_empty_nary_operands',all(len(n.find('m:e',ns))>0 for n in xml.findall('.//m:nary',ns)))
 check('no_track_changes_or_comments',not any(xml.findall('.//w:'+name,ns) for name in ['ins','del','commentRangeStart','commentReference']))
 core=etree.fromstring(z.read('docProps/core.xml'))
 check('metadata_author_empty',not core.xpath('//*[local-name()="creator" or local-name()="lastModifiedBy"]/text()'))
 check('no_template_hidden_docvars',b'docVars' not in z.read('word/settings.xml'))
 check('no_personal_paths_in_package',not any(re.search(r'86136|yuanqishaonvyufan|xwechat_files|D:\\codex|C:\\Users',z.read(n).decode('utf-8','ignore')) for n in z.namelist() if n.endswith('.xml')))
 check('official_cover_four_media_unchanged',all(bm['template_media_preservation'].values()) and len(bm['template_media_preservation'])==4)
 # Header parts contain no text; no styled empty header that can draw a rule.
 check('no_header_content',all(not etree.fromstring(z.read(n)).xpath('//*[local-name()="t" or local-name()="pStyle"]') for n in z.namelist() if re.match(r'word/header\d+\.xml',n)))
pdfpath=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'tmp/round9_reference_transfer/render_v1/F_reference_transfer_v1.pdf'
if pdfpath.exists():
 reader=PdfReader(pdfpath);pages=[p.extract_text() for p in reader.pages]
 check('PDF_no_empty_pages',all(len(t.strip())>35 for t in pages))
 check('PDF_no_formula_placeholders',not any('❑' in t or '□' in t or '\ufffd' in t for t in pages))
 check('PDF_cover_unidentified',all(x not in ''.join(pages) for x in ['86136','yuanqishaonvyufan','xwechat_files']))
 footers=[]
 for i,p in enumerate(reader.pages):
  found=[]
  def visit(t,cm,tm,font,size):
   if t.strip() and 0<=tm[5]<65:found.append(t.strip())
  p.extract_text(visitor_text=visit);footers.append(found)
 # LibreOffice extracts PAGE first in reading order; verify numbers there as backup.
 check('PDF_numbering_from_abstract',all(str(i) in re.findall(r'\b\d+\b',pages[i][:12]) for i in range(1,len(pages))))
 a=next(i for i,t in enumerate(pages) if '附录 A 完整质量信号处理' in t)
 b=next(i for i,t in enumerate(pages) if '1 问题重述' in t)
 stats=dict(total_pages=len(pages),cover_pages=1,abstract_pages=b-1,body_pages_including_references=a-b,appendix_pages=len(pages)-a,body_physical_page_range=[b+1,a],equations=24,figures=13,tables=17)
else:stats={}
failed=[x for x in checks if not x['pass_']]
report=dict(status='PASS' if not failed else 'NEEDS_CORRECTION',passed=len(checks)-len(failed),total=len(checks),checks=checks,counts=stats,visual_qa='separate visual review required',submission_readiness='FINAL CANDIDATE; team identity and AI version/date records still require team completion')
save(Q/'CONSISTENCY_QA_v1.json',report)
print(json.dumps(dict(status=report['status'],passed=report['passed'],total=len(checks),failures=failed,counts=stats),ensure_ascii=False,indent=2))

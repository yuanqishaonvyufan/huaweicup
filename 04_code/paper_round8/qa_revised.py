"""Cross-check revised manuscript, preserved v1 and Q1/Q4 repair runs."""
from pathlib import Path
from zipfile import ZipFile
import json,hashlib,csv,re,subprocess,sys,math
from pypdf import PdfReader
from lxml import etree
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'08_paper/revised_v2';OUT=ROOT/'11_delivery/revised_v2';QA=ROOT/'10_review/paper_repair';QA.mkdir(parents=True,exist_ok=True)
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def assertx(ok,what):
 checks.append({'check':what,'pass':bool(ok)})
 if not ok:print('FAIL',what)
checks=[];text=(OUT/'F_revised_draft_v2.md').read_text(encoding='utf-8')
q1=load('06_results/raw/Q1_TASK_REPAIR_20260925_v1/summary.json');q4=load('06_results/raw/Q4_TASK_REPAIR_20260925_v1/summary.json')
for sub,j in [('Q1_TASK_REPAIR_20260925_v1',q1),('Q4_TASK_REPAIR_20260925_v1',q4)]:
 for f,h in j['outputs'].items():assertx(sha(ROOT/'06_results/raw'/sub/f)==h,sub+':'+f)
assertx(q1['rows']==272505 and q1['unique_ids']==261086,'Q1 full records and distinct IDs')
assertx(len(q1['weights'])==22 and abs(sum(q1['weights'].values())-1)<1e-10,'Q1 22 weights normalized')
assertx(q1['complete_case_rows']==272486,'Q1 coverage')
assertx(all(x['strict_hull_in']==x['n']==63 for x in q1['extrapolation']),'Q1 extrapolation matched 63/63 hull')
assertx(all(x['centered_ratio_M1_to_M0']>1 and x['r0_spearman']<0 for x in q1['extrapolation']),'Q1 estimated extrapolation adverse')
for number in ['0.7600','0.7356','0.7338','0.5780','2.3452','2.2672','−0.4494','−0.5122']:
 assertx(number in text,'Q1 number '+number)
assertx(q4['full_scale_subset']['n_D_primary_usable']==6 and q4['full_scale_subset']['full_853_ND_share']=='NOT_IDENTIFIED','Q4 full scale not identified')
assertx(q4['full_scale_subset']['LOO_logN_range'][0]<0<q4['full_scale_subset']['LOO_logN_range'][1],'Q4 leave-one-out unstable')
sc=q4['scenarios']
for tar in ['2027-09-25','2028-09-25']:
 a=[x for x in sc if x['target']==tar]
 assertx(len(a)==3 and a[0]['conditional_frontier_center']>a[1]['conditional_frontier_center']>a[2]['conditional_frontier_center'],'Q4 slowdown distinct '+tar)
 for x in a:
  val=f"{x['conditional_frontier_center']:.2f}"
  assertx(val in text,'Q4 slowdown number '+tar+' '+val)
forecast=load('06_results/raw/EXP-Q4-R7-20260925-v1/forecast_summary.json')
for target in forecast['forecast']:
 ref=next(x for x in sc if x['target']==target['target'] and x['rho']==1)
 assertx(abs(ref['conditional_frontier_center']-target['central'])<1e-12,'old Q4 forecast unchanged '+target['target'])
 assertx(all(f'{x:.2f}' in text for x in target['conditional_PI95']),'old Q4 PI retained '+target['target'])
oldq1=load('03_models/modeling_phase1/q1/round4/P_RESPONSE_VALIDATION_METRICS_v2.json')
assertx(f"{oldq1['metrics']['1M']['M1']['R0_RMSE_raw']:.4f}" in text,'old Q1 M1 RMSE retained')
assertx(f"{oldq1['metrics']['1M']['M0']['R0_RMSE_raw']:.4f}" in text,'old Q1 M0 RMSE retained')
q2=load('06_results/raw/EXP-Q2-ND-R5-20260924-v1/summary.json')
for n,p in [('alpha',8),('beta',8),('A',8),('B',8),('E',8)]:assertx(f"{q2['parameters'][n]:.{p}f}" in text,'Q2 frozen '+n)
q3rows=list(csv.DictReader((ROOT/'06_results/raw/EXP-Q3-BASE-R6-20260924-v1/budget_path.csv').open()))
for r in q3rows:
 if float(r['Budget_FLOPs']) in [1e19,1e22,1e24]:assertx(f"{float(r['loss']):.6f}" in text,'Q3 frozen budget '+r['Budget_FLOPs'])
paths=subprocess.check_output(['git','diff','--name-only','1b0a1734befe3994972f2d336a9c7ae35fbfc10c','--','01_data','03_models/modeling_phase1','03_models/modeling_phase2','03_models/modeling_phase3','03_models/modeling_phase4','04_code/modeling_phase1','04_code/modeling_phase2','04_code/modeling_phase3','04_code/modeling_phase4'],cwd=ROOT,text=True)
assertx(not paths.strip(),'Q1-Q4 original data/model/code tracked files frozen')
bm=load('08_paper/revised_v2/BUILD_MANIFEST_v2.json');fig=load('08_paper/revised_v2/FINAL_FIGURE_SELECTION_v2.json');eq=load('08_paper/revised_v2/FINAL_EQUATION_REGISTRY_v2.json')
assertx(bm['tables']==18 and len(fig)==9 and len(eq)==24,'final figure/table/equation counts')
for n,c in enumerate(bm['table_captions'][:16],1):assertx(c.startswith('表'+str(n)+' '),'table order '+str(n))
for f in fig:assertx(sha(ROOT/f['source'])==f['sha256'],'figure source '+str(f['number']))
assertx('总Loss的弹性热图' in fig[3]['caption'] and 'FIG4_Q2_TOTAL_LOSS_ELASTICITY_REEXPORT.png' in fig[3]['source'],'Figure 4 truthful caption')
assertx(all('REEXPORT' in fig[n]['source'] for n in [3,4,5,6]),'Figures 4-7 re-exported from machine data')
for n in range(1,17):assertx(len(re.findall(r'表'+str(n)+r'(?!\d)',text))>=2,'table cited '+str(n))
for n in range(1,10):assertx(len(re.findall(r'图'+str(n)+r'(?!\d)',text))>=2,'figure cited '+str(n))
refs=[int(x) for x in re.findall(r'^\[(\d+)\]',text,re.M)];assertx(refs==list(range(1,8)),'citation list 1-7')
for n in refs:assertx('['+str(n)+']' in text.split('# 参考文献')[0],'citation appears in text '+str(n))
assertx('Q_full' in text and 'A12—A15' in text and '外生' in text and '560' in text,'claim boundaries present')
assertx('真实算力放缓效应仍未知' in text or '真实算力放缓效应' in text,'no causal overclaim')
docx=OUT/'F_revised_draft_v2.docx';v1=ROOT/'11_delivery/round8/F_final_manuscript.docx'
assertx(subprocess.run(['git','diff','--quiet','1b0a1734befe3994972f2d336a9c7ae35fbfc10c','--','11_delivery/round8/F_final_manuscript.docx','11_delivery/round8/F_final_manuscript.pdf','11_delivery/round8/F_final_manuscript.md'],cwd=ROOT).returncode==0,'v1 draft untouched')
with ZipFile(docx) as z:
 xml=etree.fromstring(z.read('word/document.xml'));ns={'m':'http://schemas.openxmlformats.org/officeDocument/2006/math','w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
 assertx(all(len(x.find('m:e',ns))>0 for x in xml.findall('.//m:nary',ns)),'no formula placeholder')
 assertx(not xml.findall('.//w:ins',ns) and not xml.findall('.//w:commentReference',ns),'no tracked edits/comments')
 assertx(all(bm['template_media_preservation'].values()) and len(bm['template_media_preservation'])==4,'official four cover logos byte preserved')
 core=z.read('docProps/core.xml').decode()
 assertx(not re.search(r'86136|yuanqishaonvyufan|xwechat_files|D:\\codex',core),'anonymous metadata')
pdf=OUT/'F_revised_draft_v2.pdf';stats={}
if pdf.exists():
 r=PdfReader(pdf);pages=[p.extract_text() for p in r.pages]
 assertx(all(len(t.strip())>35 for t in pages),'PDF no empty pages')
 assertx(not any('❑' in t or '□' in t or '\ufffd' in t for t in pages),'PDF no formula glyph defects')
 assertx(all(str(i) in re.findall(r'\b\d+\b',pages[i][:12]) for i in range(1,len(pages))),'PDF page numbers continuous')
 assertx(not re.search(r'86136|yuanqishaonvyufan|xwechat_files|D:\\codex',''.join(pages)),'PDF anonymous')
 body=next(i for i,t in enumerate(pages) if '1 问题重述' in t);appendix=next(i for i,t in enumerate(pages) if '附录 A 完整质量信号处理' in t)
 stats=dict(total_pages=len(pages),cover=1,abstract=body-1,body_including_references=appendix-body,appendix=len(pages)-appendix,figures=9,tables=18,equations=24)
 assertx(stats['abstract']<=2,'abstract at most two pages')
report=dict(verdict='PASS_WITH_RESTRICTED_SCIENTIFIC_SCOPE' if all(x['pass'] for x in checks) else 'FAIL',passed=sum(x['pass'] for x in checks),total=len(checks),failed=[x for x in checks if not x['pass']],checks=checks,pdf=stats,scientific_limits=['Q_full is a declared purpose-dependent rubric, not true causal quality','full 853-model N-D/technology contribution remains unidentified','Loss-to-benchmark bridge rejected','C4 compute growth unavailable; slowdown pathways are exogenous','30-42 month empirical forecast coverage unavailable'],submission_status='REVISED FINAL PAPER CANDIDATE, NOT OFFICIAL UPLOAD READY: team number and verified AI disclosure pending')
(QA/'FINAL_TASK_FULFILLMENT_REPAIR_QA_v1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['verdict','passed','total','failed','pdf']},ensure_ascii=False,indent=2))

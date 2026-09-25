"""Final Q3 candidate package integrity checks; does not rerun optimizers."""
from pathlib import Path
import json,hashlib
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    r=ROOT;m=r/'03_models/modeling_phase3/round6';checks={}
    names=['Q3_COST_MODEL_v1.md','Q3_MODEL_SPEC_v1.md','Q3_SUPPORT_CONSTRAINTS_v1.md','Q3_BASELINE_OPTIMIZATION_v1.md','Q3_GENERALIZED_OPTIMIZATION_v1.md','Q3_RESULTS_REPORT_v1.md','Q3_LIMITATIONS_v1.md','Q3_DELIVERY_FIGURE_TABLE_PLAN_v1.md','Q3_TO_Q4_INTERFACE_v1.json']
    checks['required_docs']=all((m/f).is_file() and (m/f).stat().st_size>100 for f in names)
    checks['paper_equals_report']=(m/'Q3_RESULTS_REPORT_v1.md').read_bytes()==(r/'08_paper/sections/Q3_ROUND6_PAPER_CANDIDATE_v1.md').read_bytes()
    t=(m/'Q3_RESULTS_REPORT_v1.md').read_text(encoding='utf-8');bs=chr(92)
    checks['latex_commands']=all(bs+x in t for x in ['frac','qquad','eta','inf'])
    checks['no_control_characters']=not any(ord(c)<32 and c not in '\n\r\t' for c in t)
    checks['math_block_delimiters']=all(line.strip()=='$$' for line in t.splitlines() if '$$' in line)
    fm=json.loads((r/'06_results/figures/round6/figure_manifest.json').read_text(encoding='utf-8'))
    checks['six_figures_hashes']=len(fm['figures'])==6 and all(sha(r/f['path'])==f['sha256'] for x in fm['figures'] for f in x['paths'])
    checks['figure_source_hash']=sha(r/'04_code/visualization/round6_figures.py')==fm['script_sha256']
    checks['visible_text_bounds']=all(y['inside'] for x in fm['figures'] for y in x['text_checks'])
    checks['nine_paper_tables']=len(list((r/'06_results/tables/round6').glob('TABLE-*.csv')))==9
    cm=json.loads((r/'04_code/code_manifest.json').read_text());entries=[x for x in cm['files'] if 'round6' in x['path']]
    checks['r6_code_manifest']=len(entries)>=8 and all(sha(r/x['path'])==x['sha256'] for x in entries)
    checks['Q4_not_started']=not json.loads((m/'Q3_TO_Q4_INTERFACE_v1.json').read_text())['Q4_started']
    checks['gate4_not_approved']='NOT DECIDED' in (r/'10_review/GATE4_PRE_REVIEW_PACKAGE_v1.md').read_text()
    s=r/'06_results/raw/SCEN-Q3-R6-20260924-v1';q=pd.read_csv(s/'quality_context_path.csv');be=pd.read_csv(s/'quality_break_even.csv');qb=q[(q.L_ctx==2048)&(q.qcap==1)].merge(be,on=['Budget_FLOPs','cost_family']);h=qb.factor*.36199528619528604
    checks['global_threshold_matches_activation']=bool(((h<=qb.global_threshold_h+1e-8)|(qb.Q>.5+1e-7)).all() and ((h>=qb.global_threshold_h-1e-8)|(qb.Q<=.5+1e-7)).all())
    checks['baseline_quantity_accounting']=np.allclose(pd.read_csv(r/'06_results/tables/round6/BASELINE_DOMAIN_TOKEN_ACCOUNTING.csv').iloc[:,1:].sum(axis=1),pd.read_csv(r/'06_results/raw/EXP-Q3-BASE-R6-20260924-v1/budget_path.csv').D_B)
    result={'status':'PASS' if all(checks.values()) else 'FAIL','scope':'Round6 CP5 package, not Gate4','checks':{k:bool(v) for k,v in checks.items()},'code_sha256':sha(__file__)}
    (r/'10_review/R6_PACKAGE_QA_v1.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2));assert all(checks.values())
if __name__=='__main__':main()

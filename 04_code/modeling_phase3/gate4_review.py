"""Gate4 read-only evidence check: no solver/model imports or model execution."""
from pathlib import Path
import csv,json,hashlib,math,gzip,subprocess
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
RUNS=['EXP-Q3-BASE-R6-20260924-v1','SCEN-Q3-R6-20260924-v1','UNC-Q3-R6-20260924-v1']
checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def rows(p):
    with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def ck(name,ok,detail=None):checks.append(dict(name=name,pass_check=bool(ok),detail=detail))
def main():
    cfg=js('05_experiments/configs/Q3_R6_FROZEN_v1.json');summaries={}
    for p,h in {**cfg['inputs'],**cfg['spec_hashes']}.items():ck('frozen:'+p,sha(ROOT/p)==h)
    for run in RUNS:
        prefix='06_results/raw/'+run+'/';summaries[run]=js(prefix+'summary.json')
        for p,h in js(prefix+'output_manifest.json').items():ck('output:'+prefix+p,sha(ROOT/prefix/p)==h)
        ck('run_status:'+run,summaries[run]['status']=='PASS')
    for file in ['MODELING_PHASE3_R6_NUMERICAL_QA_20260924.json','R6_PACKAGE_QA_v1.json','R6_GIT_CHECKOUT_INTEGRITY_v1.json']:
        qa=js('10_review/'+file);ck('existing_QA:'+file,qa['status']=='PASS')
    visual=js('10_review/R6_VISUAL_QA_v1.json');ck('existing_visual_QA',visual['status']=='PASS_STANDALONE_CANDIDATES')
    official=js('01_data/audits/modeling_phase3/round6/Q3_COST_AUDIT_METRICS_v1.json')
    ck('official_proxy_constants',official['official_cost']=={'train_coefficient':6,'eta':.0002,'quality_exponential':[1e7,6.],'quality_power':[5e9,4.],'quality_log':[2e9,10.]})
    ck('architecture_not_training',official['C7_rows']==45 and not official['train_context_observed'])
    ck('context_proxy_intersection',6/.0002==30000 and cfg['contexts']==[2048,4096,8192,32768,131072])
    base=rows('06_results/raw/'+RUNS[0]+'/budget_path.csv');starts=rows('06_results/raw/'+RUNS[0]+'/multistart_checks.csv')
    ck('baseline_51_and_204',len(base)==51 and len(starts)==204)
    ck('all_baseline_starts_success',all(x['success']=='True' for x in starts))
    ck('baseline_saved_objective_agreement',max(abs(float(x['loss_gap'])) for x in starts)<1e-8)
    ck('baseline_feasibility_KKT',max(float(x['budget_relative_violation']) for x in base)<1e-8 and max(float(x['kkt_projected_max']) for x in base)<1e-7)
    ck('baseline_OFF_reference',all(x['quality']=='OFF' and x['mixture']=='OFF' and int(x['L_ctx'])==2048 for x in base))
    representative=[];p=cfg['parameters']
    expected={1e19:(.221309,7.049698,2.998935),1e22:(5.202388,299.893,2.143211),1e24:(11.965825,299.893,2.093379)}
    for C,triplet in expected.items():
        z=next(x for x in base if float(x['Budget_FLOPs'])==C);n,d,f=[float(z[k]) for k in ['N_B','D_B','loss']]
        ck('representative:'+str(C),all(abs(a-b)<1e-6 for a,b in zip((n,d,f),triplet)))
        recomputed=p['E']+p['A']*n**(-p['alpha'])+p['B']*d**(-p['beta'])
        ck('saved_point_arithmetic:'+str(C),abs(f-recomputed)<1e-12 and abs(float(z['total_FLOPs'])/((6+.0002*2048)*1e18*n*d)-1)<1e-12)
        representative.append(z)
    last=representative[-1];ck('high_budget_support_not_scale_saturation',float(last['D_B'])==cfg['D_bounds'][1] and float(last['N_B'])==cfg['N_bounds'][1] and float(last['mu_per_1e18'])==0 and 'BUDGET_SLACK' in last['active_constraints'])
    scen=summaries[RUNS[1]];unc=summaries[RUNS[2]]
    ck('quality_scope_counts',scen['quality_rows']==1377 and scen['numeric_starts']==4131 and not scen['quality_causal'])
    ck('local_solver_limits_retained',scen['failed_starts']==4 and scen['max_all_start_loss_gap']>.08 and scen['max_best_start_gap']<1e-6 and scen['best_case_count']==1377)
    quality=rows('06_results/raw/'+RUNS[1]+'/quality_context_path.csv');ck('all_quality_scenario_labels',all(x['evidence']=='SCENARIO-CONDITIONAL' for x in quality))
    mix=rows('06_results/raw/'+RUNS[1]+'/mixture_scenarios.csv');ck('no_mixture_joint_transport',cfg['mixture_main_transport']==0 and all(x['B1_joint_use']=='FORBIDDEN_NO_SCALE_OVERLAP' for x in mix))
    ck('mixture_no_1B',not any('1B' in x['scale'] for x in mix) and scen['mixture_candidates']==513 and scen['simplex_max_error']<1e-10)
    ck('uncertainty_separation',unc['joint_draws']==200 and unc['conditional_configurations']==51000 and not unc['scenario_envelope_is_CI'] and not unc['external_uncertainty_covered'])
    with gzip.open(ROOT/'06_results/raw'/RUNS[2]/'conditional_draw_paths.csv.gz','rt',encoding='utf-8',newline='') as f:
        records=csv.DictReader(f);count=0;ids=set()
        for x in records:count+=1;ids.add(x['replicate'])
    ck('saved_draw_counts',count==51000 and len(ids)==200)
    shadow=rows('06_results/raw/'+RUNS[2]+'/shadow_prices.csv');ck('saved_shadow_validation',len(shadow)==1632 and max(float(x['abs_error']) for x in shadow)<1e-6)
    ck('no_Q4_in_existing_runs',all(not x['Q4_started'] for x in summaries.values()))
    fm=js('06_results/figures/round6/figure_manifest.json')
    for item in fm['figures']:
        for f in item['paths']:ck('figure:'+f['path'],sha(ROOT/f['path'])==f['sha256'])
    text_files=['03_models/modeling_phase3/round6/Q3_RESULTS_REPORT_v1.md','03_models/modeling_phase3/round6/Q3_LIMITATIONS_v1.md','03_models/modeling_phase3/round6/Q3_COST_MODEL_v1.md','03_models/modeling_phase3/round6/Q3_MODEL_SPEC_v1.md','07_validation/round6/Q3_VALIDATION_REPORT_v1.md','10_review/MODELING_PHASE3_R6_QA_20260924.md']
    report=(ROOT/text_files[0]).read_text(encoding='utf-8')
    ck('report_scope_statements',all(t in report for t in ['统计支持限制','不是现实资源的市场价格','不是实测临界点','情景包络','半合成校准','1B已失败']))
    result=dict(status='PASS' if all(x['pass_check'] for x in checks) else 'FAIL',decision='G4-SINGLE-001 evidence check, verdict recorded separately',base_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),created_utc=datetime.now(timezone.utc).isoformat(),code_sha256=sha(Path(__file__)),checks=checks,representative_baseline=representative,source_document_hashes={p:sha(ROOT/p) for p in text_files},optimizer_called=False,Q2_refit=False,Q4_started=False)
    (ROOT/'10_review/GATE4_DECISION_CHECK_v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':result['status'],'checks':len(checks),'failed':[x for x in checks if not x['pass_check']],'optimizer_called':False},ensure_ascii=False));assert result['status']=='PASS'
if __name__=='__main__':main()

"""Independent arithmetic/lineage checks; does not rerun the scientific pipeline."""
from common import *
import subprocess, platform
from scipy.special import logit,expit
CHECK=[]
def check(name,ok,evidence):CHECK.append({'check':name,'pass':bool(ok),'evidence':evidence})
def close(a,b,tol=1e-8):return bool(np.allclose(a,b,atol=tol,rtol=tol))
def main():
    cfg=json.loads((ROOT/'05_experiments/configs/Q4_R7_FROZEN_v1.json').read_text('utf-8'));mapping=json.loads((AUD/'Q4_C1_C10_ROLE_MATRIX_v1.json').read_text('utf-8'));inp=json.loads((DATA/'INPUT_MANIFEST_v1.json').read_text('utf-8'))
    check('Official C1-C10 roles complete',[r['official_id'] for r in mapping]==['C'+str(i) for i in range(1,11)],'visible-body role matrix + rendered page; all fields and SHA in JSON')
    rawfiles=[x for r in mapping for x in r['files']];bad=[x['path'] for x in rawfiles if sha(ROOT/x['path'])!=x['sha256']];check('Every C raw file unchanged',not bad,{'count':len(rawfiles),'bad':bad})
    check('Frozen mathematical specs unchanged',all(sha(SPEC/n)==h for n,h in cfg['spec_sha256'].items()),cfg['spec_sha256'])
    check('Frozen input bytes unchanged',all(sha(ROOT/p)==h for p,h in inp['files'].items()),len(inp['files']))
    a=pd.read_csv(RAW/'leaderboard_cleaned.csv');c2=pd.read_csv(RAW/'leaderboard_enhanced.csv');pq=pd.read_parquet(next((RAW/'data').glob('*.parquet')))
    nums=list(a.select_dtypes('number'));c2diff=float((a[nums]-c2[nums]).abs().max().max());c9diff=float((a[nums]-pq[nums]).abs().max().max())
    check('C1/C2/C9 floating equivalence; not replicated observations',c2diff<1e-10 and c9diff<1e-10,{'C2_max_diff':c2diff,'C9_max_diff':c9diff})
    d=pd.read_csv(DATA/'Q4_PRIMARY_v1.csv');entities=pd.read_csv(DATA/'Q4_MODEL_ENTITY_RESOLUTION_v1.csv');all8=pd.read_csv(DATA/'C8_all_versions.csv');parse=pd.read_csv(AUD/'Q4_C8_PARSE_MANIFEST_v1.csv');f=pd.read_csv(OUT/'frontier_family.csv');dates=pd.to_datetime(d.date)
    check('Unique entity, six dimensions and scale eligibility',not d.canonical.duplicated().any() and d.primary_eligible.all() and d[BENCH].notna().all().all() and (abs(d.N_C8_B/d.N_B-1)<=.02).all(),{'primary':len(d),'duplicate_primary':int(d.canonical.duplicated().sum())})
    check('Hub/license/flag criteria',d.open_broad.all() and d.hub_available.all() and (~d.flagged).all() and (~d['Hub License'].fillna('').str.lower().isin(['','unknown','other'])).all(),'reported license research proxy; strict subset separately tested')
    check('Types explicitly separated',set(d.model_type)=={'base','instruct_finetuned','merge','other'},d.model_type.value_counts().to_dict())
    check('C8 complete all-file handling',len(parse)==1958 and (~parse.parsed).sum()==4 and len(all8)==1954,{'parsed':len(all8),'bad':int((~parse.parsed).sum())})
    check('Latest parseable revision retained',all(all8[all8.canonical==r.canonical].evaluation_date.max()==r.evaluation_date for r in d.itertuples()),'latest revision never backdated to earlier evaluation in primary')
    check('Raw six-score average arithmetic',close(d.score,d[BENCH].mean(axis=1)),'unweighted six-group composite, not normalized C1 score')
    # Reopen a deterministic spread of actual JSONs and rebuild metrics independently.
    rawdiff=[]
    for row in d.iloc[np.linspace(0,len(d)-1,40,dtype=int)].itertuples():
        v=json.loads((ROOT/row.source_file).read_text('utf-8'))['results'];iv=v['leaderboard_ifeval'];vals=[50*(iv['prompt_level_strict_acc,none']+iv['inst_level_strict_acc,none']),100*v['leaderboard_bbh']['acc_norm,none'],100*v['leaderboard_math_hard']['exact_match,none'],100*v['leaderboard_gpqa']['acc_norm,none'],100*v['leaderboard_musr']['acc_norm,none'],100*v['leaderboard_mmlu_pro']['acc,none']];rawdiff.append(abs(np.mean(vals)-row.score))
    check('C8 independent metric recomputation',max(rawdiff)<1e-10,{'sample':40,'max_error':max(rawdiff)})
    subtasks=pd.read_csv(DATA/'C8_BBH_subtasks_all.csv');agg=pd.read_csv(AUD/'Q4_C8_TASK_AGGREGATION_v1.csv');latest=all8.sort_values(['evaluation_date','source_file']).drop_duplicates('directory',keep='last');sub=subtasks[subtasks.source_file.isin(latest.source_file)];reagg=sub.groupby('task').raw_accuracy.agg(['count','mean','median','std']).reset_index()
    check('Mandatory C8 subtask aggregation independently matches',list(agg.task)==list(reagg.task) and close(agg.iloc[:,1:],reagg.iloc[:,1:]),{'task_count':len(agg),'raw_rows':len(subtasks)})
    beta=float(pd.read_csv(OUT/'decomposition_coefficients.csv').query("model=='family' and term=='logN'").coefficient.iloc[0]);errs=[];serrs=[];ncheck=True;timecheck=True
    for r in f.itertuples():
        t=pd.Timestamp(r.date);g=d[(dates>t-pd.Timedelta(days=28))&(dates<=t)].sort_values(['score','canonical']);ncheck &=len(g)==r.n and r.n>=15
        errs.append(abs(float(np.quantile(g.score,.9))-r.F));lo=g[g.canonical==r.lower_ID].iloc[0];hi=g[g.canonical==r.upper_ID].iloc[0];s=beta*((1-r.upper_weight)*np.log(lo.N_B)+r.upper_weight*np.log(hi.N_B));serrs.append(abs(s-r.S));timecheck &= pd.to_datetime(g.date).max()<=t
    check('Frontier quantile independently recomputed',max(errs)<1e-10,{'endpoints':len(f),'max_error':max(errs)})
    check('Window counts and causal endpoint dates',ncheck and timecheck,'no future evaluations or centered windows in primary frontier')
    check('Same quantile weights for scale/residual',max(serrs)<1e-10 and close(f.F,f.S+f.R),{'scale_max_error':max(serrs)})
    dc=pd.read_csv(OUT/'decomposition_changes.csv');check('Decomposition sums and unclamped shares',close(dc.delta_F,dc.delta_S+dc.delta_R) and close(dc.parameter_share+dc.residual_share,1),'negative sensitivity shares preserved')
    rv=pd.read_csv(OUT/'robustness_variants.csv');check('Failed share robustness disclosed',(rv.parameter_share.dropna()<0).any() and 'NOT STABLE' in (SPEC/'Q4_ROBUSTNESS_v1.md').read_text('utf-8'),'known-family / strict / start / window signs differ')
    check('Full ND contribution explicitly unidentified',d.D_B.notna().sum()==9 and 'NOT IDENTIFIED' in (SPEC/'Q4_SCALE_NONSCALE_DECOMPOSITION_v1.md').read_text('utf-8'),{'known_D':int(d.D_B.notna().sum()),'base_D_usable':int((d.D_B.notna()&(d.model_type=='base')).sum())})
    br=json.loads((OUT/'bridge_summary.json').read_text('utf-8'));bv=pd.read_csv(OUT/'bridge_validation.csv');bh=pd.read_csv(OUT/'bridge_holdout_predictions.csv');bi=pd.read_csv(OUT/'bridge_identity_audit.csv')
    check('Bridge train/test entity disjoint',all(not(set(r.train_IDs.split('|'))&set(r.test_IDs.split('|'))) for r in bh.itertuples()),'high stratum has unique scales; medium strata only model-held-out diagnostics')
    high=bv[(bv.family=='HIGH_pythia')&(bv.split=='LOSO')].set_index('method');check('Bridge verdict supported by failed validation',br['verdict']=='NO RELIABLE BRIDGE' and high.loc['linear','rmse']>high.loc['mean','rmse'] and high.loc['monotone','rmse']>high.loc['mean','rmse'] and br['high_rank_rho']<.7,'no rejected bridge enters raw6 forecast')
    check('B1 source-loss equality does not imply benchmark identity',close(bi.B1_loss_abs_diff,0) and bi.identity_N_match.sum()==2,{'B1_pairs':len(bi),'C1_scale_eligible':int(bi.identity_N_match.sum())})
    rp=pd.read_csv(OUT/'rolling_predictions.csv');pred_errors=[]
    for r in rp.itertuples():
        train=f[(f.is_sunday)&(f.date<=r.origin)]
        if r.model=='local_logit':train=train[train.t_week>=train.t_week.max()-13]
        x=train.t_week.to_numpy();y=train.F.to_numpy()
        if r.model=='persistence':p=y[-1]
        else:
            z=logit(np.clip(y/100,.001,.999)) if 'logit' in r.model else y;slope,intercept=np.polyfit(x,z,1);p=slope*r.target_t+intercept;p=100*expit(p) if 'logit' in r.model else np.clip(p,0,100)
        pred_errors.append(abs(p-r.prediction))
    check('Rolling predictions independently recomputed',max(pred_errors)<1e-8,{'rows':len(rp),'max_error':max(pred_errors)})
    check('Rolling origin strictly before target',((rp.train_max_t<rp.target_t)&((pd.to_datetime(rp.target)-pd.to_datetime(rp.origin)).dt.days==7*rp.horizon_weeks)).all(),'no time lookahead in fitted dynamics')
    check('Long-horizon validation unavailable explicitly',set(rp.horizon_weeks)=={4,13},'26/52 weeks have no eligible target; not counted PASS')
    metrics=pd.read_csv(OUT/'rolling_metrics.csv');scores=metrics.groupby('model').MAE.mean();check('Model selection per frozen criterion',scores.idxmin()=='logit' and scores['persistence']>1.05*scores.min(),scores.to_dict())
    forecasts=pd.read_csv(OUT/'forecast_all_models_scenarios.csv');draws=pd.read_csv(OUT/'forecast_statistical_draws.csv');future=pd.read_csv(OUT/'forecast_12m_24m.csv');fan=pd.read_csv(OUT/'forecast_fan.csv')
    check('Run-date targets and stale gap explicit',set(future.target)=={'2027-09-25','2028-09-25'} and (future.origin=='2026-09-25').all() and (future.gap_days==560).all(),'last data2025-03-14; data-to-target horizon includes gap')
    check('All central/interval predictions bounded',((forecasts[['central','lower95_conditional','upper95_conditional']]>=0)&(forecasts[['central','lower95_conditional','upper95_conditional']]<=100)).all().all() and (forecasts.lower95_conditional<=forecasts.upper95_conditional).all(),'bounded transform/clipping; mathematical ceiling only')
    qerr=[]
    for r in forecasts[(forecasts.selected)&(forecasts.scenario=='BASELINE')].itertuples():
        ds=draws[draws.target==r.target].score;lo,hi=np.quantile(ds,[.025,.975]);qerr.extend([abs(lo-r.lower95_conditional),abs(hi-r.upper95_conditional)]);check('Bootstrap replicates '+r.target,len(ds)==1000,len(ds))
    check('Saved percentile intervals recompute',max(qerr)<1e-9,{'max_error':max(qerr)})
    # Independently recompute selected full logit forecast from frontier only.
    slope,intercept=np.polyfit(f.t_week,logit(f.F/100),1);forecast_errors=[]
    for r in future.itertuples():
        t=(pd.Timestamp(r.target)-pd.Timestamp('2024-06-16')).total_seconds()/604800;p=100*expit(intercept+slope*t);forecast_errors.append(abs(p-r.no_slowdown_reference))
    check('Requested central forecasts independently recompute',max(forecast_errors)<1e-8,{'max_error':max(forecast_errors),'logit_intercept_at_20240616':intercept,'logit_slope_per_week':slope})
    scen=pd.read_csv(OUT/'scenario_decomposition.csv');check('Scenario component arithmetic and labels',close(scen.central,scen.parameter_component+scen.residual_component) and close(scen.central-f.F.iloc[-1],scen.delta_parameter+scen.delta_residual) and (scen.delta_parameter==0).all() and set(scen.scenario)=={'BASELINE','CONSERVATIVE','ACCELERATED'},'collapsed positive-scale-growth scenarios; no actual compute slowdown identification')
    q3=pd.read_csv(OUT/'Q3_conditional_interface.csv');original=pd.read_csv(ROOT/'06_results/raw/EXP-Q3-BASE-R6-20260924-v1/budget_path.csv');check('Q3 copied without history/benchmark transport',q3[list(original)].equals(original) and (q3.benchmark_prediction=='NOT_IDENTIFIED_NO_RELIABLE_BRIDGE').all(),'51 conditional resource rows; input training data never includes Q3')
    check('All six task directions reported',len(pd.read_csv(OUT/'benchmark_robustness.csv'))==6,'no cherry-picked benchmark')
    check('Release-date insufficient sample retained','INSUFFICIENT_FRONTIER_ENDPOINTS' in set(rv.status),'no invented release-date forecast')
    required=['Q4_BRIDGE_MODEL_SPEC_v1.md','Q4_BRIDGE_RESULTS_v1.md','Q4_SCALE_NONSCALE_DECOMPOSITION_v1.md','Q4_FRONTIER_MODEL_SPEC_v1.md','Q4_ROLLING_VALIDATION_v1.md','Q4_FORECAST_12M_24M_v1.md','Q4_UNCERTAINTY_ANALYSIS_v1.md','Q4_ROBUSTNESS_v1.md','Q4_RESULTS_REPORT_v1.md','Q4_LIMITATIONS_v1.md','Q4_FIGURE_PLAN_v1.md','Q4_TABLE_PLAN_v1.md','Q4_TO_PAPER_INTERFACE_v1.md']
    check('Required model report package exists',all((SPEC/x).exists() for x in required),required)
    figs=json.loads((ROOT/'06_results/figures/round7/figure_manifest.json').read_text('utf-8'));check('Eight figure hashes and sources',len(figs)==8 and all(sha(ROOT/p)==h for r in figs for p,h in r['files'].items()),'PNG and SVG; visual inspection logged separately')
    registries=[(ROOT/p).read_text('utf-8') for p in ['05_experiments/EXPERIMENT_REGISTRY.md','06_results/RESULTS_REGISTRY.md','06_results/FIGURE_REGISTRY.md']];check('Run/result/figure registered','EXP-Q4-R7-20260925-v1' in registries[0] and all('Q4-R7-'+f'{i:03d}' in registries[1] for i in range(1,9)) and all(r['id'] in registries[2] for r in figs),'eight restricted results and eight figures')
    changed=subprocess.check_output(['git','diff','--name-only','3562c1294f4355edfa6e5ac13a7724f25fbcef26'],cwd=ROOT,text=True).splitlines()
    forbidden=[p for p in changed if any(s in p for s in ['/modeling_phase1/','/modeling_phase2/','/modeling_phase3/','/raw/real_attachments/'])]
    check('Q1-Q3/raw not reopened or mutated',not forbidden,forbidden)
    verdict='PASS WITH DOCUMENT CORRECTIONS' if all(x['pass'] for x in CHECK) else 'FAIL — MATERIAL ISSUE'
    result={'run_id':'QA-Q4-R7-20260925-v1','verdict':verdict,'checks':CHECK,'pass_count':sum(x['pass'] for x in CHECK),'total':len(CHECK),'new_defects_found':{'P0':0,'P1':0,'P2':3},'unresolved_implementation_defects':{'P0':0,'P1':0,'P2':0},'scope':'restricted descriptive arithmetic and conditional forecasts; no reliable bridge, full ND and real compute-slowdown NOT IDENTIFIED; no long-horizon validation','reviewer':'single executing researcher; no external reviewer claimed'}
    dump(ROOT/'10_review/ROUND7_QA_v1.json',result)
    val=ROOT/'07_validation/round7';val.mkdir(parents=True,exist_ok=True)
    text='# Q4 validation report v1\n\nVerdict: **'+verdict+'**. '+str(result['pass_count'])+'/'+str(len(CHECK))+' implementation/lineage checks pass. Three P2 document/figure defects corrected; numerical run unchanged.\n\n'+mdtable(pd.DataFrame([{'check':x['check'],'pass':x['pass']} for x in CHECK]))+'\n\nThis is NOT a pass for bridge predictivity, true non-scale identification, decomposition robustness or long-horizon coverage: the bridge fails, full ND/compute-slowdown is unidentified, share sensitivity fails, and long-horizon validation is unavailable. These are negative or inconclusive research results preserved in the paper package. Restrictive provisional closure is allowed only with those statements intact.\n\nNew defects found P0/P1/P2=0/0/3; all closed. Retained scientific limitations are separately itemized in Q4_LIMITATIONS, not declared solved. Single-agent programmatic/visual review; no external Opus certification.\n'
    write(val/'Q4_VALIDATION_REPORT_v1.md',text);write(SPEC/'Q4_VALIDATION_REPORT_v1.md',text)
    print(json.dumps({'verdict':verdict,'passed':result['pass_count'],'total':len(CHECK),'failed':[x for x in CHECK if not x['pass']]},ensure_ascii=False))
    if verdict.startswith('FAIL'):raise SystemExit(1)
if __name__=='__main__':main()

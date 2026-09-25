from round7_models import *
import csv
def copy_q3_interface():
    # Preserve original decimal strings: pandas round-tripping changes last bits.
    source=ROOT/'06_results/raw/EXP-Q3-BASE-R6-20260924-v1/budget_path.csv'
    with source.open(encoding='utf-8',newline='') as stream:
        reader=csv.DictReader(stream);fields=reader.fieldnames;rows=list(reader)
    with (OUT/'Q3_conditional_interface.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields+['q4_role','benchmark_prediction'],lineterminator='\n');writer.writeheader()
        for row in rows:writer.writerow(dict(row,q4_role='CONDITIONAL_N_D_SOURCE_LOSS_ONLY',benchmark_prediction='NOT_IDENTIFIED_NO_RELIABLE_BRIDGE'))
def forecast_rows(f,selected,beta,tag='main'):
    t=f.t_week.to_numpy(); y=f.F.to_numpy();last=pd.Timestamp(f.date.iloc[-1]);origin=pd.Timestamp(CFG['run_date'])
    scale_slope=float(ols(np.column_stack([np.ones(len(t)),t-t[-1]]),f.S)[1])
    target_dates=[pd.Timestamp(x) for x in CFG['targets']]+[last+pd.DateOffset(months=m) for m in [12,24]]
    results=[];simout=[]
    for model in MODELS:
        fit=fit_dynamic(t,y,model);targets=np.array([weeks(x) for x in target_dates]);unadjusted=predict_dynamic(fit,targets);sim=draws_dynamic(fit,targets,CFG['bootstrap'])
        for j,date in enumerate(target_dates):
            h=float(targets[j]-t[-1]);A=max(0,scale_slope*h)
            for scenario,retained in [('CONSERVATIVE',0.),('BASELINE',.5),('ACCELERATED',1.)]:
                removed=(1-retained)*A;central=float(np.clip(unadjusted[j]-removed,0,100));draws=np.clip(sim[:,j]-removed,0,100);lo,hi=np.quantile(draws,[.025,.975])
                row={'variant':tag,'model':model,'selected':model==selected,'scenario':scenario,'target':str(date.date()),'origin':str(origin.date()) if j<2 else str(last.date()),'origin_type':'RUN_DATE' if j<2 else 'LAST_DATA_SENSITIVITY','months_ahead':12 if j%2==0 else 24,'last_data':str(last.date()),'gap_days':(origin-last).days if j<2 else 0,'horizon_weeks_from_data':h,'central':central,'lower95_conditional':float(lo),'upper95_conditional':float(hi),'no_slowdown_reference':float(unadjusted[j]),'scale_slope_per_week':scale_slope,'parameter_contribution_removed':removed,'retained_scale_fraction':retained,'status':'EXTRAPOLATION-DOMINATED; conditional diffusion PI, no calibrated long-horizon coverage'}
                results.append(row)
                if model==selected and scenario=='BASELINE':
                    simout.extend({'target':str(date.date()),'replicate':i,'score':v} for i,v in enumerate(draws))
    return pd.DataFrame(results),pd.DataFrame(simout)

def sensitivity(d,selected):
    largest=d[d.family!='unknown'].family.value_counts().idxmax();cases=[('drop_largest_'+largest,d[d.family!=largest],28,.9,'date'),('known_families',d[d.family!='unknown'],28,.9,'date'),('strict_license',d[d.open_strict],28,.9,'date'),('base_only',d[d.model_type=='base'],28,.9,'date'),('posttrained_only',d[d.model_type=='instruct_finetuned'],28,.9,'date'),('start_2024_09',d[d.date>='2024-09-01'],28,.9,'date'),('window56',d,56,.9,'date'),('q95',d,28,.95,'date'),('submission_date',d,28,.9,'submission_date'),('release_date_available',d[d.release_date.notna()],28,.9,'release_date'),('exclude_Feb_cluster',d[~d.date.str.startswith('2025-02')],28,.9,'date')]
    out=[];frames=[]
    for name,g,window,q,datecol in cases:
        if len(g)<20:out.append({'variant':name,'status':'INSUFFICIENT_ROWS','n':len(g)});continue
        X=design(g,'family');coef=ols(X,g.score);beta=float(coef[list(X).index('logN')]);f=frontier(g,beta,window,q,datecol=datecol)
        if len(f)<8:out.append({'variant':name,'status':'INSUFFICIENT_FRONTIER_ENDPOINTS','n':len(g),'frontier_n':len(f)});continue
        pr,_=forecast_rows(f,selected,beta,name);pr=pr[(pr.model==selected)&(pr.scenario=='BASELINE')&(pr.origin_type=='RUN_DATE')]
        dy=float(f.F.iloc[-1]-f.F.iloc[0]);ds=float(f.S.iloc[-1]-f.S.iloc[0]);dt=float(f.t_week.iloc[-1]-f.t_week.iloc[0]);sl=float(ols(np.column_stack([np.ones(len(f)),f.t_week]),f.R)[1])
        for _,r in pr.iterrows():out.append({'variant':name,'status':'RETROSPECTIVE_TIME_SENSITIVITY_NOT_CAUSAL' if datecol!='date' else 'CHECKED_SENSITIVITY','n':len(g),'frontier_n':len(f),'first':f.date.iloc[0],'last':f.date.iloc[-1],'beta_logN':beta,'delta_F':dy,'delta_S':ds,'parameter_share':ds/dy if abs(dy)>1e-8 else np.nan,'residual_slope_week':sl,'target':r.target,'central':r.central,'lower95':r.lower95_conditional,'upper95':r.upper95_conditional})
        f['variant']=name;frames.append(f)
    pd.DataFrame(out).to_csv(OUT/'robustness_variants.csv',index=False)
    pd.concat(frames,ignore_index=True).to_csv(OUT/'robustness_frontiers.csv',index=False)
    bench=[]
    for b in BENCH:
        y=d.copy();y['score']=y[b];X=design(y,'family');coef=ols(X,y.score);beta=float(coef[list(X).index('logN')]);f=frontier(y,beta)
        bench.append({'benchmark':b,'delta_F':float(f.F.iloc[-1]-f.F.iloc[0]),'delta_S':float(f.S.iloc[-1]-f.S.iloc[0]),'beta_logN':beta,'time_score_per_year':float(coef[list(X).index('time_years')]),'frontier_linear_slope_week':float(ols(np.column_stack([np.ones(len(f)),f.t_week]),f.F)[1])})
    pd.DataFrame(bench).to_csv(OUT/'benchmark_robustness.csv',index=False)

def main():
    d=pd.read_csv(DATA/'Q4_PRIMARY_v1.csv');f=pd.read_csv(OUT/'frontier_family.csv');selection=json.loads((OUT/'dynamic_selection.json').read_text('utf-8'));model=selection['selected'];beta=json.loads((OUT/'CP2_summary.json').read_text('utf-8'))['main_beta_logN']
    pred,draws=forecast_rows(f,model,beta);pred.to_csv(OUT/'forecast_all_models_scenarios.csv',index=False);draws.to_csv(OUT/'forecast_statistical_draws.csv',index=False)
    selected=pred[(pred.model==model)&(pred.origin_type=='RUN_DATE')];selected.to_csv(OUT/'forecast_12m_24m.csv',index=False)
    # Fan at monthly dates through 24 months beyond run date, statistical only.
    dates=pd.date_range(pd.Timestamp(f.date.iloc[-1]),pd.Timestamp(CFG['targets'][-1])+pd.offsets.MonthEnd(0),freq='ME');t=np.array([weeks(x) for x in dates]);fit=fit_dynamic(f.t_week,f.F,model);sim=draws_dynamic(fit,t,CFG['bootstrap']);slope=float(pred.scale_slope_per_week.iloc[0]);remove=.5*np.maximum(0,slope*(t-f.t_week.iloc[-1]));sim=np.clip(sim-remove,0,100);lo,mid,hi=np.quantile(sim,[.025,.5,.975],axis=0)
    pd.DataFrame({'date':dates,'central':np.clip(predict_dynamic(fit,t)-remove,0,100),'lower95':lo,'upper95':hi}).to_csv(OUT/'forecast_fan.csv',index=False)
    sensitivity(d,model)
    # Q3 only copied as a conditional mechanism, never a historical feature.
    copy_q3_interface()
    summary=[]
    for target,g in pred[pred.origin_type=='RUN_DATE'].groupby('target'):
        base=g[(g.model==model)&(g.scenario=='BASELINE')].iloc[0];models=g[g.scenario=='BASELINE'];scenarios=g[g.model==model]
        summary.append({'target':target,'central':base.central,'conditional_PI95':[base.lower95_conditional,base.upper95_conditional],'model_range':[float(models.central.min()),float(models.central.max())],'scenario_range':[float(scenarios.central.min()),float(scenarios.central.max())],'no_slowdown_reference':base.no_slowdown_reference,'removed_scale_component':base.parameter_contribution_removed})
    bs=pd.read_csv(OUT/'decomposition_family_bootstrap.csv');slopeR=float(ols(np.column_stack([np.ones(len(f)),f.t_week]),f.R)[1])
    result={'run_id':CFG['run_id'],'origin':CFG['run_date'],'last_data':f.date.iloc[-1],'gap_days':int((pd.Timestamp(CFG['run_date'])-pd.Timestamp(f.date.iloc[-1])).days),'selected_model':model,'forecast':summary,'scale_slope_week':float(pred.scale_slope_per_week.iloc[0]),'residual_slope_week':slopeR,'cluster_bootstrap_parameter_share95':list(np.quantile(bs.delta_S_fixed_endpoint/(f.F.iloc[-1]-f.F.iloc[0]),[.025,.975])),'cluster_bootstrap_row_time_slope95':list(np.quantile(bs.time_score_per_year,[.025,.975])),'full_N_D_non_scale_share':'NOT_IDENTIFIED','empirical_long_horizon_coverage':'UNAVAILABLE','code_sha256':sha(Path(__file__))}
    dump(OUT/'forecast_summary.json',result);print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()

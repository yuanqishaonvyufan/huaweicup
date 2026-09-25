from common import *
import collections, re, platform

def compact(x): return re.sub('[^a-z0-9]','',canon(x).split('/')[-1])
def main():
    c1=pd.read_csv(RAW/'leaderboard_cleaned.csv'); c2=pd.read_csv(RAW/'leaderboard_enhanced.csv'); c3=pd.read_csv(RAW/'leaderboard_extended_timeseries.csv'); c4=pd.read_csv(RAW/'epoch_all_ai_models.csv'); c5=pd.read_csv(RAW/'loss_benchmark_bridge.csv');c6=pd.read_csv(RAW/'loss_benchmark_bridge_expanded.csv')
    for d in [c1,c2,c3,c4,c5,c6]: d['canonical']=d.Model.map(canon)
    # Ambiguous snapshot variants are excluded, not averaged or selected by score.
    dup=set(c1.loc[c1.canonical.duplicated(False),'canonical'])
    c1['ambiguous_identity']=c1.canonical.isin(dup)
    d=c1.loc[~c1.ambiguous_identity].copy()
    d=d.rename(columns={'#Params (B)':'N_B','Submission Date':'submission_date','Average ⬆️':'score'})
    d['family']=d.canonical.map(family)
    d['family_confidence']=np.where(d.family=='unknown','unknown','name token only; ancestry unverified')
    d['model_type']=d.Type.map(lambda s:'base' if 'pretrained' in str(s) else ('merge' if 'merge' in str(s) or 'moerge' in str(s) else 'instruct_finetuned' if 'chat' in str(s) or 'fine-tuned' in str(s) else 'other'))
    license=d['Hub License'].fillna('').str.lower().str.strip()
    strict={'apache-2.0','mit','bsd-3-clause','bsd-2-clause','gpl-3.0','gpl-2.0','cc-by-4.0','cc-by-sa-4.0','cc0-1.0','unlicense'}
    d['open_strict']=license.isin(strict)
    d['open_broad']=~license.isin(['','unknown','other','not-for-all-audiences'])
    d['license_rule']='reported known license; research/open-weight proxy, not full open-source certification'
    d['release_date']=d.canonical.map(c2.drop_duplicates('canonical').set_index('canonical').Epoch_AI_Publication_Date)
    d['D_B']=np.nan;d['C4_compute_FLOP']=np.nan;d['C4_open_weights']='';d['C4_match']='unmatched';d['C4_model']=''
    c4['key']=c4.Model.map(compact); groups=c4.groupby('key')
    matches=[]
    for i,row in d.iterrows():
        k=compact(row.canonical)
        if k not in groups.groups: continue
        g=groups.get_group(k)
        if len(g)!=1:continue
        z=g.iloc[0]; n=pd.to_numeric(z.Parameters,errors='coerce')/1e9
        if not np.isfinite(n) or abs(n/row.N_B-1)>.10:continue
        d.loc[i,['C4_compute_FLOP','C4_open_weights','C4_match','C4_model']]=[pd.to_numeric(z['Training compute (FLOP)'],errors='coerce'),str(z['Open model weights?']),'unique namespace-stripped punctuation match AND N within 10%',z.Model]
        # Dataset-size field is unit-mixed; require explicit token wording in notes.
        note=str(z['Dataset size notes']); amount=pd.to_numeric(z['Training dataset size (total)'],errors='coerce')
        if re.search(r'token',note,re.I) and np.isfinite(amount): d.loc[i,'D_B']=amount/1e9
        matches.append({'canonical':row.canonical,'C4_model':z.Model,'N_C1_B':row.N_B,'N_C4_B':n,'dataset_size':str(z['Training dataset size (total)']),'dataset_notes':note,'compute_notes':str(z['Training compute notes']),'open_weights':str(z['Open model weights?'])})
    d['bridge_D_B']=d.canonical.map(c6.drop_duplicates('canonical').set_index('canonical').D_tokens_B)
    d['D_B']=d.D_B.fillna(d.bridge_D_B)
    d['D_primary_usable']=d.D_B.notna() & (d.model_type=='base')
    pd.DataFrame(matches).to_csv(AUD/'Q4_C4_ENTITY_MATCHES_v1.csv',index=False)
    # Parse every C8 file and retain every version for review; latest parseable per directory for primary.
    file_rows=[];detail=[];tasks=[]
    metric={'IFEval':('leaderboard_ifeval','inst_level_strict_acc,none'),'BBH':('leaderboard_bbh','acc_norm,none'),'MATH Lvl 5':('leaderboard_math_hard','exact_match,none'),'GPQA':('leaderboard_gpqa','acc_norm,none'),'MUSR':('leaderboard_musr','acc_norm,none'),'MMLU-PRO':('leaderboard_mmlu_pro','acc,none')}
    for f in sorted((RAW/'detailed_results').rglob('*.json')):
        fr={'path':str(f.relative_to(ROOT)).replace('\\','/'),'sha256':sha(f),'directory':f.parent.name}
        try: v=json.loads(f.read_text('utf-8'))
        except (json.JSONDecodeError,UnicodeDecodeError) as e:
            fr.update(parsed=False,error=str(e));file_rows.append(fr);continue
        fr['parsed']=True; file_rows.append(fr)
        cfg=v.get('config',{});name=v.get('model_name')
        if not name: name=re.search(r'pretrained=([^,]+)',str(cfg.get('model_args',''))).group(1)
        row={'canonical':canon(name),'directory':f.parent.name,'evaluation_date':f.stem.removeprefix('results_').split('T')[0],'version':str(cfg.get('model_revision','unknown')),'source_file':fr['path'],'N_C8_B':cfg.get('model_num_parameters',np.nan)/1e9 if cfg.get('model_num_parameters') is not None else np.nan}
        for b,(task,key) in metric.items():row[b]=v.get('results',{}).get(task,{}).get(key,np.nan)*100
        # IFEval leaderboard composite averages prompt-strict and instruction-strict.
        ife=v.get('results',{}).get('leaderboard_ifeval',{})
        row['IFEval']=(ife.get('inst_level_strict_acc,none',np.nan)+ife.get('prompt_level_strict_acc,none',np.nan))*50
        row['complete']=all(np.isfinite(row[b]) for b in BENCH)
        row['score_raw6']=np.mean([row[b] for b in BENCH]) if row['complete'] else np.nan
        detail.append(row)
        for task,vals in v.get('results',{}).items():
            if not task.startswith('leaderboard_bbh_'):continue
            if 'acc_norm,none' in vals:tasks.append({'source_file':fr['path'],'canonical':row['canonical'],'task':task,'raw_accuracy':vals['acc_norm,none']})
    pd.DataFrame(file_rows).to_csv(AUD/'Q4_C8_PARSE_MANIFEST_v1.csv',index=False)
    all8=pd.DataFrame(detail);all8.to_csv(DATA/'C8_all_versions.csv',index=False)
    latest=all8.sort_values(['evaluation_date','source_file']).drop_duplicates('directory',keep='last')
    pd.DataFrame(tasks).to_csv(DATA/'C8_BBH_subtasks_all.csv',index=False)
    tasksdf=pd.DataFrame(tasks); latesttasks=tasksdf[tasksdf.source_file.isin(latest.source_file)]
    latesttasks.groupby('task').raw_accuracy.agg(['count','mean','median','std']).to_csv(AUD/'Q4_C8_TASK_AGGREGATION_v1.csv')
    c8dup=set(latest.loc[latest.canonical.duplicated(False),'canonical'])
    latest=latest[~latest.canonical.isin(c8dup)]
    keep=['canonical','evaluation_date','version','source_file','N_C8_B','score_raw6','complete']+BENCH
    d=d.merge(latest[keep],on='canonical',how='left',suffixes=('','_raw'))
    d['scale_match_C8']=abs(d.N_C8_B/d.N_B-1)<=.02
    d['date']=pd.to_datetime(d.evaluation_date,errors='coerce')
    pq=pd.read_parquet(next((RAW/'data').glob('*.parquet')))
    pq['canonical']=pq.fullname.map(canon)
    pqidx=pq[~pq.canonical.duplicated(False)].set_index('canonical')
    d['hub_available']=d.canonical.map(pqidx['Available on the hub']).fillna(False).astype(bool)
    d['flagged']=d.canonical.map(pqidx['Flagged']).fillna(True).astype(bool)
    d['primary_eligible']=d.open_broad & d.hub_available & ~d.flagged & d.complete.fillna(False).astype(bool) & d.scale_match_C8 & d.date.notna() & d.N_B.gt(0)
    d['identity_confidence']=np.where(d.primary_eligible,'exact full ID and N within 2%; latest C8 revision','snapshot ID only / missing or mismatched evaluation')
    d['training_tokens_source']=np.where(d.bridge_D_B.notna(),'C6 provided; Pythia only',np.where(d.D_B.notna(),'C4 explicit token notes','missing'))
    d.to_csv(DATA/'Q4_MODEL_ENTITY_RESOLUTION_v1.csv',index=False)
    main=d[d.primary_eligible].copy();main['score']=main.score_raw6
    for b in BENCH:main[b]=main[b+'_raw']
    main.to_csv(DATA/'Q4_PRIMARY_v1.csv',index=False)
    c6['family']=c6.canonical.map(family);c6.to_csv(DATA/'C6_bridge_v1.csv',index=False)
    hist=c3[c3.Source!='Open LLM Leaderboard'].copy();hist['six_mean']=hist[['IFEval','BBH','MATH_Lvl5','GPQA','MUSR','MMLU_PRO']].mean(axis=1);hist['mean_mismatch']=abs(hist.Average-hist.six_mean)
    hist.to_csv(AUD/'Q4_C3_HISTORICAL_COMPARABILITY_v1.csv',index=False)
    macro=c4.copy();macro['year']=pd.to_datetime(macro['Publication date'],errors='coerce').dt.year;macro['compute']=pd.to_numeric(macro['Training compute (FLOP)'],errors='coerce');macro['data_size_numeric']=pd.to_numeric(macro['Training dataset size (total)'],errors='coerce')
    macro.groupby(['year','Open model weights?'],dropna=False).agg(models=('Model','size'),compute_n=('compute','count'),compute_median=('compute','median'),data_size_n=('data_size_numeric','count')).to_csv(AUD/'Q4_C4_MACRO_CONTEXT_v1.csv')
    # C9 is an equivalent snapshot, never appended as extra observations.
    stat={'run_id':'AUDIT-Q4-R7-20260925-v1','python':platform.python_version(),'C1_rows':len(c1),'C1_duplicate_IDs_excluded':len(dup),'C1_unique_unambiguous':len(d),'C1_average_max_diff':float(abs(c1['Average ⬆️']-c1[BENCH].mean(axis=1)).max()),'C1_C2_core_equal':bool(c1.drop(columns=['ambiguous_identity']).equals(c2[list(c1.drop(columns=['ambiguous_identity']))])),'C9_rows':len(pq),'C9_columns':list(pq),'C8_files':len(file_rows),'C8_parse_failures':sum(not x['parsed'] for x in file_rows),'C8_latest_directories':int(all8.directory.nunique()),'C8_latest_complete':int(all8.sort_values(['evaluation_date','source_file']).drop_duplicates('directory',keep='last').complete.sum()),'C8_unique_ambiguous_IDs':len(c8dup),'primary_rows':len(main),'primary_dates':[str(main.date.min().date()),str(main.date.max().date())],'primary_families':main.family.value_counts().to_dict(),'primary_D_known':int(main.D_B.notna().sum()),'C4_matches':len(matches),'C4_token_note_matches':int((d.training_tokens_source=='C4 explicit token notes').sum()),'C3_historical_rows':len(hist),'C3_historical_mean_mismatch_gt_1':int((hist.mean_mismatch>1).sum()),'C3_leaderboard_rows':int((c3.Source=='Open LLM Leaderboard').sum()),'C5_subset_C6':bool(set(c5.canonical)<=set(c6.canonical)),'C6_unique':int(c6.canonical.nunique()),'primary_score_range':[float(main.score.min()),float(main.score.max())]}
    dump(AUD/'Q4_DATA_AUDIT_METRICS_v1.json',stat)
    dump(DATA/'INPUT_MANIFEST_v1.json',{'raw_mapping_sha':sha(AUD/'Q4_C1_C10_ROLE_MATRIX_v1.json'),'code_sha':sha(Path(__file__)),'files':{str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in DATA.glob('*.csv')}})
    print(json.dumps(stat,ensure_ascii=False))
if __name__=='__main__':main()

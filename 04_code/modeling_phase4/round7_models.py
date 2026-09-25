from common import *
from scipy.stats import spearmanr
from scipy.special import expit, logit
CFG=json.loads((ROOT/'05_experiments/configs/Q4_R7_FROZEN_v1.json').read_text('utf-8'))
EPOCH=pd.Timestamp('2024-06-16')
MODELS=CFG['models']
def weeks(d): return (pd.to_datetime(d)-EPOCH).total_seconds()/604800
def ols(X,y):return np.linalg.lstsq(np.asarray(X,dtype=float),np.asarray(y,dtype=float),rcond=None)[0]
def bridge_predict(x,y,z,method):
    if method=='mean':return np.full(len(z),np.mean(y))
    if method=='linear':
        b=min(0,float(np.cov(x,y,ddof=0)[0,1]/np.var(x)));return np.mean(y)+b*(z-np.mean(x))
    order=np.argsort(x);xx=x[order];yy=-y[order];blocks=[]
    for i,v in enumerate(yy):
        blocks.append([i,i,float(v),1])
        while len(blocks)>1 and blocks[-2][2]/blocks[-2][3]>blocks[-1][2]/blocks[-1][3]:
            b=blocks.pop();a=blocks.pop();blocks.append([a[0],b[1],a[2]+b[2],a[3]+b[3]])
    fitted=np.empty(len(x))
    for a,b,s,n in blocks:fitted[a:b+1]=-s/n
    return np.interp(z,xx,fitted)

def bridge():
    d=pd.read_csv(DATA/'C6_bridge_v1.csv');high=d[d.Loss_Comparability.str.startswith('High')].sort_values('N_params_B')
    rows=[];residual=[];summary=[]
    for fam,g in [('HIGH_pythia',high)]+[(str(f),g) for f,g in d[~d.Loss_Comparability.str.startswith('High')].groupby('family') if len(g)>=4 and g.N_params_B.nunique()>=4]:
        g=g.sort_values('N_params_B').reset_index(drop=True);x=g.Val_Loss.to_numpy();y=g.LB_Average.to_numpy();n=len(g)
        splits=[('LOSO',str(i),[i]) for i in range(n)]+[('LOW_SCALE','lowest_two',[0,1]),('HIGH_SCALE','highest_two',[n-2,n-1])]
        for kind,fold,test in splits:
            train=np.array([i for i in range(n) if i not in test]);test=np.array(test)
            for m in ['mean','linear','monotone']:
                pred=bridge_predict(x[train],y[train],x[test],m)
                for i,p in zip(test,pred): rows.append({'family':fam,'split':kind,'fold':fold,'method':m,'canonical':g.canonical.iloc[i],'N_B':float(g.N_params_B.iloc[i]),'observed':y[i],'prediction':p,'error':p-y[i],'train_IDs':'|'.join(g.canonical.iloc[train]),'test_IDs':'|'.join(g.canonical.iloc[test])})
        fitted=bridge_predict(x,y,x,'linear')
        for i,p in enumerate(fitted):residual.append({'family':fam,'canonical':g.canonical.iloc[i],'Loss':x[i],'N_B':g.N_params_B.iloc[i],'observed':y[i],'fitted':p,'residual':y[i]-p})
        summary.append({'family':fam,'n':n,'spearman_minus_loss':float(spearmanr(-x,y).statistic),'loss_sd':float(np.std(x))})
    cv=pd.DataFrame(rows);cv.to_csv(OUT/'bridge_holdout_predictions.csv',index=False);pd.DataFrame(residual).to_csv(OUT/'bridge_residuals.csv',index=False)
    errors=cv.groupby(['family','split','method']).error.agg(rmse=lambda x:np.sqrt(np.mean(x*x)),mae=lambda x:np.mean(abs(x)),n='size').reset_index();errors.to_csv(OUT/'bridge_validation.csv',index=False)
    h=errors[errors.family=='HIGH_pythia'];pivot=h.pivot(index='split',columns='method',values='rmse');rho=summary[0]['spearman_minus_loss']
    passing=[m for m in ['linear','monotone'] if rho>=.7 and bool((pivot[m]<=pivot['mean']).all())]
    # Exact pair identity audit against C1 and B1, no recalibration of Q2.
    c1=pd.read_csv(RAW/'leaderboard_cleaned.csv');c1['canonical']=c1.Model.map(canon)
    b1=pd.read_csv(ROOT/'01_data/processed/modeling_phase2/round5/B1_v1.csv');pairs=[]
    for _,r in high.iterrows():
        z=c1[c1.canonical==r.canonical];identity=len(z)==1 and abs(z['#Params (B)'].iloc[0]/r.N_params_B-1)<=.02
        candidates=b1.loc[np.isclose(b1.N_params_B,r.N_params_B,rtol=.001)&np.isclose(b1.D_tokens_B,r.D_tokens_B,rtol=.001)]
        pairs.append({'canonical':r.canonical,'C1_rows':len(z),'identity_N_match':bool(identity),'C1_score_min_abs_diff':float(abs(z['Average ⬆️']-r.LB_Average).min()) if len(z) else None,'B1_final_rows':len(candidates),'B1_loss_abs_diff':float(abs(candidates.val_loss-r.Val_Loss).min()) if len(candidates) else None})
    paired=pd.DataFrame(pairs);paired.to_csv(OUT/'bridge_identity_audit.csv',index=False)
    raw=pd.read_csv(DATA/'Q4_MODEL_ENTITY_RESOLUTION_v1.csv'); rawcount=int(high.canonical.isin(raw[raw.score_raw6.notna()].canonical).sum())
    verdict='WEAK BRIDGE' if passing and paired.identity_N_match.all() else 'NO RELIABLE BRIDGE'
    result={'verdict':verdict,'operational':'B0 no quantitative transport into forecast','high_n':len(high),'high_families':1,'high_rank_rho':rho,'passing_methods':passing,'family_diagnostics':summary,'leave_one_family_out':'UNAVAILABLE: only one high-comparability family','temporal_holdout':'UNAVAILABLE: paired loss/evaluation dates absent','raw6_high_overlap':rawcount,'raw6_bridge':'UNAVAILABLE below 5 high exact pairs' if rawcount<5 else 'requires separate holdout, not transported','loss_provenance':'attachment-internal; external validation anchors remain unverified'}
    dump(OUT/'bridge_summary.json',result);return result

def design(d,mode='family'):
    out=pd.DataFrame({'intercept':1.,'logN':np.log(d.N_B)},index=d.index)
    if mode!='N_only':
        out['time_years']=(pd.to_datetime(d.date)-EPOCH).dt.days/365.25
        out=pd.concat([out,pd.get_dummies(d.model_type,prefix='type',drop_first=True,dtype=float)],axis=1)
    if mode=='family':out=pd.concat([out,pd.get_dummies(d.family,prefix='family',drop_first=True,dtype=float)],axis=1)
    return out

def frontier(d,beta=0.,window=28,q=.9,min_n=15,datecol='date',target='score'):
    d=d.copy();d['used_date']=pd.to_datetime(d[datecol],errors='coerce');d=d.dropna(subset=['used_date',target])
    dates=list(pd.date_range(d.used_date.min(),d.used_date.max(),freq='W-SUN'))
    if not dates or dates[-1]!=d.used_date.max():dates.append(d.used_date.max())
    out=[]
    for t in dates:
        g=d[(d.used_date>t-pd.Timedelta(days=window))&(d.used_date<=t)].sort_values([target,'canonical'])
        if len(g)<min_n:continue
        u=q*(len(g)-1);i=int(np.floor(u));j=int(np.ceil(u));w=u-i
        a=g.iloc[i];b=g.iloc[j];ln=(1-w)*np.log(a.N_B)+w*np.log(b.N_B);y=(1-w)*a[target]+w*b[target]
        out.append({'date':str(t.date()),'t_week':weeks(t),'n':len(g),'F':y,'S':beta*ln,'R':y-beta*ln,'frontier_logN':ln,'lower_ID':a.canonical,'upper_ID':b.canonical,'upper_weight':w,'max_input_date':str(g.used_date.max().date()),'min_input_date':str(g.used_date.min().date()),'is_sunday':t.weekday()==6,'known_family_share':float((g.family!='unknown').mean()),'largest_family_share':float(g.family.value_counts(normalize=True).max())})
    return pd.DataFrame(out)

def decompose(d):
    coeff=[];changes=[];trajs=[];main=None
    for mode in ['N_only','pooled','family']:
        X=design(d,mode);b=ols(X,d.score);beta=float(b[list(X).index('logN')]);f=frontier(d,beta)
        for name,v in zip(X,b):coeff.append({'model':mode,'term':name,'coefficient':v,'n':len(d),'rank':int(np.linalg.matrix_rank(X.astype(float))),'columns':len(X)})
        delta=f.iloc[-1]-f.iloc[0] if False else None
        dy=float(f.F.iloc[-1]-f.F.iloc[0]);ds=float(f.S.iloc[-1]-f.S.iloc[0]);dr=dy-ds
        changes.append({'model':mode,'start':f.date.iloc[0],'end':f.date.iloc[-1],'delta_F':dy,'delta_S':ds,'delta_R':dr,'parameter_share':ds/dy if abs(dy)>1e-8 else np.nan,'residual_share':dr/dy if abs(dy)>1e-8 else np.nan,'beta_logN':beta,'time_score_per_year':float(b[list(X).index('time_years')]) if 'time_years' in X else np.nan})
        f.to_csv(OUT/f'frontier_{mode}.csv',index=False)
        if mode=='family':main=f; mainbeta=beta
    for fam,g in d.groupby('family'):
        if fam=='unknown' or len(g)<20 or (pd.to_datetime(g.date).max()-pd.to_datetime(g.date).min()).days<90:continue
        X=design(g,'pooled');b=ols(X,g.score)
        trajs.append({'family':fam,'n':len(g),'beta_logN':float(b[list(X).index('logN')]),'time_score_per_year':float(b[list(X).index('time_years')])})
    pd.DataFrame(coeff).to_csv(OUT/'decomposition_coefficients.csv',index=False);pd.DataFrame(changes).to_csv(OUT/'decomposition_changes.csv',index=False);pd.DataFrame(trajs).to_csv(OUT/'same_family_trajectories.csv',index=False)
    # Cluster bootstrap at name-family level; unknown is one conservative cluster.
    rng=np.random.default_rng(CFG['seed']);families=d.family.unique();bs=[]
    for rep in range(400):
        sampled=rng.choice(families,len(families),replace=True);g=pd.concat([d[d.family==f] for f in sampled],ignore_index=True)
        X=design(g,'family');b=ols(X,g.score);beta=float(b[list(X).index('logN')]);bs.append({'replicate':rep,'beta_logN':beta,'time_score_per_year':float(b[list(X).index('time_years')]),'delta_S_fixed_endpoint':beta*(main.frontier_logN.iloc[-1]-main.frontier_logN.iloc[0])})
    pd.DataFrame(bs).to_csv(OUT/'decomposition_family_bootstrap.csv',index=False)
    return main,mainbeta,changes

def fit_dynamic(t,y,model):
    t=np.asarray(t,float);y=np.asarray(y,float)
    if model=='local_logit':mask=t>=t.max()-13;t=t[mask];y=y[mask]
    transformed=model in ['logit','local_logit'];z=logit(np.clip(y/100,.001,.999)) if transformed else y
    if model=='persistence':
        fitted=np.full(len(z),z[-1]);innov=z[4:]-z[:-4] if len(z)>4 else np.diff(z);sd=float(np.std(innov,ddof=1)) if len(innov)>1 else 0.
        return {'model':model,'t':t,'z':z,'coef':np.array([z[-1],0.]),'fitted':fitted,'residual':z-fitted,'sd':max(sd,1e-8),'transform':False}
    X=np.column_stack([np.ones(len(t)),t-t[-1]]);coef=ols(X,z);fit=X@coef;res=z-fit;sd=float(np.sqrt(np.sum(res**2)/max(1,len(z)-2)))
    return {'model':model,'t':t,'z':z,'coef':coef,'fitted':fit,'residual':res,'sd':max(sd,1e-8),'transform':transformed}
def predict_dynamic(f,target):
    z=f['coef'][0]+f['coef'][1]*(np.asarray(target)-f['t'][-1]);return 100*expit(z) if f['transform'] else np.clip(z,0,100)
def draws_dynamic(f,target,B=1000,seed=20260925):
    rng=np.random.default_rng(seed);t=f['t'];n=len(t);target=np.atleast_1d(target);h=np.maximum(0,target-t[-1]);block=4
    starts=rng.integers(0,n,size=(B,int(np.ceil(n/block))));ix=((starts[:,:,None]+np.arange(block))%n).reshape(B,-1)[:,:n]
    if f['model']=='persistence':pred=np.full((B,len(target)),f['z'][-1])
    else:
        z=f['fitted'][None,:]+f['residual'][ix];X=np.column_stack([np.ones(n),t-t[-1]]);coef=z@np.linalg.pinv(X).T;pred=coef[:,0,None]+coef[:,1,None]*(target-t[-1])
    pred+=rng.normal(size=pred.shape)*f['sd']*np.sqrt(1+h/4)
    return 100*expit(pred) if f['transform'] else np.clip(pred,0,100)

def rolling(f):
    f=f[f.is_sunday].reset_index(drop=True);rows=[]
    for i in range(CFG['rolling_min_train']-1,len(f)):
        train=f.iloc[:i+1];origin=train.t_week.iloc[-1]
        for h in CFG['rolling_horizons_weeks']:
            test=f[np.isclose(f.t_week,origin+h)]
            if len(test)!=1:continue
            obs=float(test.F.iloc[0]);date=test.date.iloc[0]
            for model in MODELS:
                fit=fit_dynamic(train.t_week,train.F,model);pred=float(predict_dynamic(fit,[origin+h])[0]);sim=draws_dynamic(fit,[origin+h],CFG['rolling_bootstrap'],CFG['seed']+i+h);lo,hi=np.quantile(sim[:,0],[.025,.975])
                rows.append({'model':model,'origin':train.date.iloc[-1],'target':date,'horizon_weeks':h,'train_n':len(train),'train_max_t':origin,'target_t':origin+h,'prediction':pred,'observed':obs,'error':pred-obs,'lower95':lo,'upper95':hi,'covered':bool(lo<=obs<=hi)})
    r=pd.DataFrame(rows);r.to_csv(OUT/'rolling_predictions.csv',index=False)
    m=r.groupby(['model','horizon_weeks']).agg(MAE=('error',lambda x:abs(x).mean()),RMSE=('error',lambda x:np.sqrt(np.mean(x*x))),coverage95=('covered','mean'),n=('error','size')).reset_index();m.to_csv(OUT/'rolling_metrics.csv',index=False)
    score=m.groupby('model').MAE.mean();best=score.idxmin();chosen='persistence' if score['persistence']<=1.05*score.min() else best
    dump(OUT/'dynamic_selection.json',{'selected':chosen,'scores':score.to_dict(),'horizons_available':sorted(r.horizon_weeks.unique().tolist()),'horizons_unavailable':[h for h in CFG['rolling_horizons_weeks'] if h not in set(r.horizon_weeks)],'selection':'equal-horizon MAE; persistence within 5% retained','independent_live_backtest':False})
    # Fixed midpoint broken slope diagnostic.
    x=f.t_week.to_numpy();y=f.F.to_numpy();mid=(x.min()+x.max())/2;X=np.column_stack([np.ones(len(x)),x-x[0]]);Xp=np.column_stack([X,np.maximum(x-mid,0)])
    b=ols(X,y);bp=ols(Xp,y);sse=float(np.sum((y-X@b)**2));ssep=float(np.sum((y-Xp@bp)**2))
    dump(OUT/'structural_diagnostics.json',{'midpoint_week':mid,'global_slope_per_week':b[1],'pre_slope':bp[1],'post_slope':bp[1]+bp[2],'linear_AIC':len(x)*np.log(sse/len(x))+4,'broken_AIC':len(x)*np.log(ssep/len(x))+6,'interpretation':'descriptive fixed-midpoint change; dependent overlapping windows; not causal break identification'})
    return chosen

def main():
    for name,h in CFG['spec_sha256'].items():assert sha(SPEC/name)==h
    manifest=json.loads((DATA/'INPUT_MANIFEST_v1.json').read_text('utf-8'))
    for p,h in manifest['files'].items():assert sha(ROOT/p)==h,p
    b=bridge();d=pd.read_csv(DATA/'Q4_PRIMARY_v1.csv');f,beta,changes=decompose(d);chosen=rolling(f)
    dump(OUT/'CP2_summary.json',{'bridge':b,'decomposition':[{k:(None if isinstance(v,float) and np.isnan(v) else v) for k,v in row.items()} for row in changes],'selected_dynamic':chosen,'main_beta_logN':beta,'n_frontier':len(f),'code_sha256':sha(Path(__file__))})
    print(json.dumps({'bridge':b['verdict'],'rho':b['high_rank_rho'],'chosen':chosen,'changes':changes},ensure_ascii=False))
if __name__=='__main__':main()

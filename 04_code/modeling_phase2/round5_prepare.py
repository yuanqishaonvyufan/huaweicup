"""Freeze audited Q2 inputs; raw attachments are read-only. No model fitting."""
from pathlib import Path
import hashlib,json,platform
from datetime import datetime,timezone
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'01_data/processed/modeling_phase2/round5'
RAW=ROOT/'01_data/raw/real_attachments'
SPEC=ROOT/'03_models/modeling_phase2/round5/Q2_ROUND5_SPEC_v1.md'
FILES={'B1':'pythia_training_log_existing.csv','B2':'cerebras_training_log.csv',
       'B4':'scaling_baseline.csv','B5':'published_scaling_data.csv',
       'B6':'supplementary_NQ_experiment.csv','B7':'supplementary_NQ_experiment_expanded.csv',
       'B9':'supplementary_large_models.csv','B10':'supplementary_large_baseline.csv'}
LEVEL={'B1':'ATTACHMENT-INTERNAL ESTIMATED','B2':'SEMI-SYNTHETIC CALIBRATED',
       'B4':'DIAGNOSTIC ONLY','B5':'DIAGNOSTIC ONLY','B6':'SEMI-SYNTHETIC CALIBRATED',
       'B7':'SEMI-SYNTHETIC CALIBRATED','B9':'DIAGNOSTIC ONLY','B10':'SCENARIO-CONDITIONAL'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def main():
    if OUT.exists():raise RuntimeError('Frozen input directory exists; create a new version, do not overwrite')
    manifest=pd.read_csv(ROOT/'01_data/raw/RAW_SHA256.csv')
    print('Raw manifest columns:',list(manifest),flush=True)
    OUT.mkdir(parents=True)
    records=[];data={}
    for label,fn in FILES.items():
        src=RAW/'B_scaling_laws'/fn
        digest=sha(src)
        # Require a matching recorded raw hash; do not assume a local schema column name.
        assert digest in manifest.astype(str).to_numpy().ravel(),(label,'raw hash not in original manifest')
        d=pd.read_csv(src); data[label]=d.copy()
        required=['N_params_B','D_tokens_B']+([] if label=='B9' else ['val_loss'])
        a=d[required].to_numpy(float)
        if label=='B9':
            assert np.isfinite(d.N_params_B).all() and (d.N_params_B>0).all()
            d['valid_for_ND_scenario']=np.isfinite(d.D_tokens_B)&d.D_tokens_B.gt(0)
        else:assert np.isfinite(a).all() and (a>0).all(),label
        assert not d.duplicated().any(),label
        d.insert(0,'row_id',[f'{label}-{i:04d}' for i in range(len(d))])
        if label=='B1':
            assert digest=='529a59644b0f57bf3a76037838b614bfedc35e58bb26b93052e34ffc63e454c2'
            assert len(d)==1176 and d.N_params_B.nunique()==8 and d.D_tokens_B.nunique()==147
            assert not d.duplicated(['N_params_B','D_tokens_B']).any()
            d=d[['row_id','run_id']+required].sort_values(['N_params_B','D_tokens_B'])
            d['D_rank']=d.D_tokens_B.map({v:i for i,v in enumerate(sorted(d.D_tokens_B.unique()))})
        elif label=='B2':d=d[['row_id','N_params_B','D_tokens_B','val_loss']].sort_values(['N_params_B','D_tokens_B'])
        elif label in ['B6','B7']:
            assert not d.duplicated(['N_params_B','D_tokens_B','Q_score']).any()
            assert d.Q_score.between(0,1).all()
        dst=OUT/f'{label}_v1.csv'; d.to_csv(dst,index=False)
        records.append(dict(id=label,source=str(src.relative_to(ROOT)).replace('\\','/'),raw_sha256=digest,
            processed=str(dst.relative_to(ROOT)).replace('\\','/'),processed_sha256=sha(dst),
            rows_before=len(data[label]),rows_after=len(d),required_missing=int(d[required].isna().sum().sum()),nonpositive_D=int(d.D_tokens_B.le(0).sum()),imputed=0,evidence_level=LEVEL[label],
            N_range=[float(d.N_params_B.min()),float(d.N_params_B.max())],D_range=[float(d.D_tokens_B.min()),float(d.D_tokens_B.max())]))
    key=['N_params_B','D_tokens_B','Q_score']
    overlap=data['B6'].merge(data['B7'],on=key,suffixes=('_6','_7'),validate='one_to_one')
    assert len(overlap)==360 and np.array_equal(overlap.val_loss_6,overlap.val_loss_7)
    dump(OUT/'INPUT_MANIFEST_v1.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),
        specification_sha256=sha(SPEC),preprocessing_code_sha256=sha(__file__),inputs=records,
        B6_exact_subset_B7=360,python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,
        leakage_control='No learned transforms; deterministic trajectory and D rank splits; B8 unread'))
    print(json.dumps(records,ensure_ascii=False),flush=True)
if __name__=='__main__':main()

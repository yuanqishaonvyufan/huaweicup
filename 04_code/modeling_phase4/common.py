from pathlib import Path
import hashlib, json, re
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
RAW=ROOT/'01_data/raw/real_attachments/C_efficiency_evolution'
AUD=ROOT/'01_data/audits/modeling_phase4/round7'
DATA=ROOT/'01_data/processed/modeling_phase4/round7'
SPEC=ROOT/'03_models/modeling_phase4/round7'
OUT=ROOT/'06_results/raw/EXP-Q4-R7-20260925-v1'
for p in [AUD,DATA,SPEC,OUT]: p.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,obj):
    Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=lambda x:x.item() if isinstance(x,np.generic) else str(x),allow_nan=False)+'\n',encoding='utf-8',newline='\n')
def write(p,s): Path(p).write_text(s+'\n',encoding='utf-8',newline='\n')
def canon(x): return str(x).strip().lower()
def family(x):
    s=canon(x)
    for f in ['pythia','qwen','llama','gemma','mistral','mixtral','phi','falcon','deepseek','bloom','gpt-neox','gpt-neo','opt']:
        if re.search(r'(^|[/_\-])'+f,s): return f
    if re.search(r'(^|[/_\-])yi([\-./]|$)',s): return 'yi'
    return 'unknown'
BENCH=['IFEval','BBH','MATH Lvl 5','GPQA','MUSR','MMLU-PRO']

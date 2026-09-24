"""Targeted Q3 official-role and cost-input audit. No Q4 analysis."""
from pathlib import Path
import csv, hashlib, json, collections, zipfile, xml.etree.ElementTree as ET
import pymupdf

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'01_data/audits/modeling_phase3/round6'
RAW = ROOT/'01_data/raw/real_attachments'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p, v): p.write_text(json.dumps(v, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    hashes = {r['relative_path']:r['sha256'] for r in csv.DictReader((ROOT/'01_data/raw/RAW_SHA256.csv').open(encoding='utf-8-sig'))}
    pdf = ROOT/'00_problem/original/F_2026_data_description_user_supplied.pdf'
    assert sha(pdf)=='f5c851bbe4b3d8c9079609c37f2c3b0835244067711d6d761c66adeaa8357835'
    visible=[]
    with pymupdf.open(pdf) as doc:
        for page_no in [3,4,11,12]:
            spans=[]
            for block in doc[page_no].get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for s in line['spans']:
                        if not(s['color']>=0xf0f0f0 and s['size']<=5.1 and(s['bbox'][1]<30 or s['bbox'][1]>720)):
                            spans.append(s['text'])
            visible.append(dict(page=page_no+1,text='\n'.join(spans)))
    source=ROOT/'00_problem/original/F_2026_problem_user_supplied.docx'
    assert sha(source)=='b557526de9295a8acbeefa1c703cc0c0cf15b7f835b656e0f4efe077e5a82d5a'
    with zipfile.ZipFile(source) as z:
        tree=ET.fromstring(z.read('word/document.xml'))
    paras=[''.join(n.text or '' for n in p.iter() if n.tag.split('}')[-1]=='t') for p in tree.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')]
    full='\n'.join(paras)
    excerpt=full[full.index('问题三：算力'):full.index('问题四：技术')]+ '\n'+full[full.index('B.1数据质量成本'):full.index('B.2领域')]
    dump(OUT/'Q3_OFFICIAL_VISIBLE_SOURCE_v1.json',dict(docx_sha256=sha(source),pdf_sha256=sha(pdf),docx_Q3_appendix_B=excerpt,pdf_visible_pages=visible,exclusion='Established near-white small-font page-margin interference rule'))
    prefix='C_efficiency_evolution/'
    mapping=[('C1','排行榜主表','leaderboard_cleaned.csv','OBSERVED / mixed metadata'),('C2','排行榜增强','leaderboard_enhanced.csv','OBSERVED / merged metadata'),('C3','排行榜时序','leaderboard_extended_timeseries.csv','MIXED'),('C4','全模型元数据','epoch_all_ai_models.csv','PROVIDED metadata, some compute ESTIMATED'),('C5','Loss–Benchmark 桥接','loss_benchmark_bridge.csv','MIXED'),('C6','桥接扩展','loss_benchmark_bridge_expanded.csv','MIXED'),('C7','架构元数据含最大上下文','model_architecture_metadata.csv','PROVIDED architecture metadata'),('C8','逐任务评测 JSON','detailed_results/','OBSERVED evaluations; out of Q3 scope'),('C9','原始 Leaderboard Parquet','data/','OBSERVED; out of Q3 scope'),('C10','评测说明目录','pythia_*_eval_details/','PROVIDED documentation')]
    records=[]
    for oid,desc,name,grade in mapping:
        if oid=='C10': paths=[p for p in hashes if p.startswith(prefix+'pythia_') and p.endswith('/README.md')]
        elif name.endswith('/'): paths=[p for p in hashes if p.startswith(prefix+name)]
        else: paths=[prefix+name]
        files=[];fields=[];rows=None
        for path in paths:
            p=RAW/path
            # Out-of-scope Q4 collections use the immutable raw manifest, no task parsing.
            current=sha(p) if oid not in ['C8','C9','C10'] else hashes[path]
            assert current==hashes[path],path
            files.append(dict(path='01_data/raw/real_attachments/'+path,sha256=current,hash_checked_now=oid not in ['C8','C9','C10']))
        if len(paths)==1 and name.endswith('.csv'):
            with (RAW/paths[0]).open(encoding='utf-8-sig',newline='') as stream:
                reader=csv.DictReader(stream);fields=reader.fieldnames;rows=sum(1 for _ in reader)
        records.append(dict(official_id=oid,official_description=desc,official_visible_pages=[4,12,13],files=files,variables=fields,rows=rows,evidence_grade=grade,question_role='Q3 exogenous context sensitivity' if oid=='C7' else 'Q4/reserved; not a Q3 cost calibration',objective=False,constraints=oid=='C7',sensitivity_only=oid=='C7',units='max_position_embeddings: tokens; training_data_TB not token count' if oid=='C7' else 'native per-column units; not merged into Q3',unresolved='maximum context is not observed training context; no hardware utilization or supply-price curve' if oid=='C7' else 'Cross-source alignment/comparability not reopened in Q3'))
    dump(OUT/'Q3_OFFICIAL_DATA_ROLE_MATRIX_v1.json',records)
    lines=['# Q3 official data role matrix v1','','OFFICIAL_MAPPING_FIRST：以已排除页边干扰的说明第4/12/13页与题面附录A为准。所有完整路径、逐文件SHA、字段、单位、资格及未决事项见同名JSON。C8/C9/C10只引用既有原件manifest，不开展Q4解析。','','| ID | 官方说明 | 实际路径（C_efficiency_evolution/下） | 文件/行 | Q3目标 | Q3约束/敏感性 | 等级/未决 |','|---|---|---|---|---|---|---|']
    for r,m in zip(records,mapping):lines.append(f"| {r['official_id']} | {r['official_description']} | {m[2]} | {len(r['files'])} / {r['rows']} | NO | {'外生长度情景；非实训约束' if r['official_id']=='C7' else 'NO；Q4保留'} | {r['evidence_grade']}；{r['unresolved']} |")
    (OUT/'Q3_OFFICIAL_DATA_ROLE_MATRIX_v1.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    c7=list(csv.DictReader((RAW/(prefix+'model_architecture_metadata.csv')).open(encoding='utf-8')))
    levels=collections.Counter(int(r['max_position_embeddings']) for r in c7)
    dump(OUT/'Q3_COST_AUDIT_METRICS_v1.json',dict(run_id='AUDIT-Q3-COST-R6-20260924-v1',basis_commit='219a8182af34b503c37da3016ed1d9dd52fb1016',code_sha256=sha(Path(__file__)),C7_rows=len(c7),C7_unique_models=len({r['model_name'] for r in c7}),context_levels_counts=dict(sorted(levels.items())),pythia_context=sorted({int(r['max_position_embeddings']) for r in c7 if 'pythia' in r['model_name'].lower()}),train_context_observed=False,official_cost=dict(train_coefficient=6,eta=.0002,quality_exponential=[1e7,6.0],quality_power=[5e9,4.0],quality_log=[2e9,10.0]),context_equal_cost_threshold=6/.0002,quality_curve_grade='PROVIDED mathematical proxy, not measured real costs',missing_inputs=['actual training context','hardware efficiency / monetary price','real domain procurement prices / supply caps','empirical quality-to-cost calibration','DQ0 to B7 Q_score mapping'],Q4_started=False))
    print(json.dumps(dict(rows=len(c7),levels=dict(levels),mapping='C1-C10 complete; only C7 enters Q3 scenarios'),ensure_ascii=False))

if __name__=='__main__': main()

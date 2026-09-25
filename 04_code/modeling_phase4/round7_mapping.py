from common import *
import csv, pymupdf, zipfile, xml.etree.ElementTree as ET
def main():
    prior=json.loads((ROOT/'01_data/audits/modeling_phase3/round6/Q3_OFFICIAL_DATA_ROLE_MATRIX_v1.json').read_text('utf-8'))
    hashes={r['relative_path']:r['sha256'] for r in csv.DictReader((ROOT/'01_data/raw/RAW_SHA256.csv').open(encoding='utf-8-sig'))}
    pdf=ROOT/'00_problem/original/F_2026_data_description_user_supplied.pdf'
    assert sha(pdf)=='f5c851bbe4b3d8c9079609c37f2c3b0835244067711d6d761c66adeaa8357835'
    visible=[]
    with pymupdf.open(pdf) as doc:
        for i in [3,4,11,12]:
            spans=[s for b in doc[i].get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans']]
            visible.append({'page':i+1,'text':'\n'.join(s['text'] for s in spans if not(s['color']>=0xf0f0f0 and s['size']<=5.1 and(s['bbox'][1]<30 or s['bbox'][1]>720)))})
        doc[3].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(str(AUD/'official_C_mapping.png'))
    source=ROOT/'00_problem/original/F_2026_problem_user_supplied.docx'
    with zipfile.ZipFile(source) as z: tree=ET.fromstring(z.read('word/document.xml'))
    paras=[''.join(n.text or '' for n in p.iter() if n.tag.split('}')[-1]=='t') for p in tree.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')]
    full='\n'.join(paras); a=full.index('问题四：')
    dump(AUD/'Q4_OFFICIAL_VISIBLE_SOURCE_v1.json',{'pdf_sha256':sha(pdf),'docx_sha256':sha(source),'Q4':full[a:full.index('附录 B：',a)],'visible_pages':visible,'interference_excluded':True})
    records=[]
    roles=['primary snapshot, submission cohorts','same snapshot + release-date sensitivity','mixed-time comparability audit; historical rows excluded from primary','macro compute/data/open-weight audit; conservative exact metadata matching','bridge subset cross-check','primary stratified bridge','architecture context only; TB is not training tokens','mandatory task aggregation and evaluation-date sensitivity','equivalent snapshot audit, no double counting','documentation only']
    for r,role in zip(prior,roles):
        files=[]
        for f in r['files']:
            p=ROOT/f['path']; h=sha(p); rel=str(p.relative_to(ROOT/'01_data/raw/real_attachments')).replace('\\','/')
            assert h==hashes[rel],rel
            files.append({'path':f['path'],'sha256':h,'bytes':p.stat().st_size})
        fields=r['variables']; rows=r['rows']
        if r['official_id']=='C9':
            d=pd.read_parquet(ROOT/files[0]['path']);fields=list(d);rows=len(d)
        if r['official_id']=='C8': rows=len(files);fields=['results','config','model_name','date','task_hashes','versions']
        if r['official_id']=='C10': rows=len(files);fields=['README text']
        records.append(dict(official_id=r['official_id'],official_description=r['official_description'],files=files,rows=rows,fields=fields,time_variable={'C1':'Submission Date','C2':'Submission Date; Epoch_AI_Publication_Date','C3':'Year (mixed)','C4':'Publication date; Last modified','C8':'evaluation filename timestamp'}.get(r['official_id'],'absent'),model_identity='exact normalized full model ID; no fuzzy auto-merge',benchmark_identity='six leaderboard dimensions; C3 historical comparability unverified',family_identity='conservative token rule; unknown retained',loss_availability=r['official_id'] in ['C5','C6'],evidence_type=r['evidence_grade'],q4_role=role,limitations='Snapshot/revision/license metadata do not establish historical availability; source evidence grade retained'))
    dump(AUD/'Q4_C1_C10_ROLE_MATRIX_v1.json',records)
    lines=['# Q4 C1–C10 role matrix v1','','ACTIVE / CHECKED. OFFICIAL_MAPPING_FIRST; visible PDF pp.4,5,12,13 and official Q4 appendix. Full file hashes, fields and all requested role attributes are in the adjacent JSON; C8 individual hashes are included. Raw files unchanged.','','| ID | Official description | Actual path under C_efficiency_evolution | Files / rows | Time | Q4 role |','|---|---|---|---|---|---|']
    for r in records: lines.append(f"| {r['official_id']} | {r['official_description']} | {r['files'][0]['path'].split('C_efficiency_evolution/')[1]} | {len(r['files'])} / {r['rows']} | {r['time_variable']} | {r['q4_role']} |")
    write(AUD/'Q4_C1_C10_ROLE_MATRIX_v1.md','\n'.join(lines))
    print([(r['official_id'],len(r['files']),r['rows']) for r in records])
if __name__=='__main__':main()

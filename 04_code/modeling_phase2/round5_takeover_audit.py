"""Verify saved Round 5 artifacts; optionally restore hash-proven checkout EOLs.

No fitting, validation prediction generation, or scenario execution is performed.
The restore option accepts only a byte sequence matching an existing SHA-256.
"""
import argparse
import csv
import hashlib
import io
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = '06_results/raw/EXP-Q2-ND-R5-20260924-v1'
SCEN = '06_results/raw/SCEN-Q2-R5-20260924-v3'
AUDIT = ROOT / '10_review/ROUND5_TAKEOVER_INTEGRITY_v1.json'
RESTORE = ROOT / '10_review/ROUND5_CHECKOUT_BYTE_RESTORATION_v1.json'


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def digest(value):
    return hashlib.sha256(value).hexdigest()


def targets():
    found = {}

    def add(path, expected):
        path = path.replace('\\', '/')
        if path in found and found[path] != expected:
            raise ValueError('Conflicting recorded hashes: ' + path)
        found[path] = expected

    for directory in [BASE, SCEN]:
        for name, expected in read(directory + '/output_manifest.json').items():
            add(directory + '/' + name, expected)
    config = read('05_experiments/configs/Q2_R5_v1.json')
    add(config['spec'], config['spec_sha256'])
    add('04_code/modeling_phase2/round5_fit.py', config['fit_code_sha256'])
    add('01_data/processed/modeling_phase2/round5/INPUT_MANIFEST_v1.json', config['input_manifest_sha256'])
    for directory, code, cfg in [
        (BASE, 'round5_fit.py', 'Q2_R5_v1.json'),
        (SCEN, 'round5_scenarios.py', 'Q2_R5_SCEN_v3.json'),
    ]:
        summary = read(directory + '/summary.json')
        add('04_code/modeling_phase2/' + code, summary['code_sha256'])
        add('05_experiments/configs/' + cfg, summary['config_sha256'])
    manifest = read('01_data/processed/modeling_phase2/round5/INPUT_MANIFEST_v1.json')
    add('04_code/modeling_phase2/round5_prepare.py', manifest['preprocessing_code_sha256'])
    for item in manifest['inputs']:
        add(item['source'], item['raw_sha256'])
        add(item['processed'], item['processed_sha256'])
    for path, expected in read('05_experiments/configs/Q2_R5_SCEN_v3.json')['inputs'].items():
        add(path, expected)
    for item in read('04_code/code_manifest.json')['files']:
        add(item['path'], item['sha256'])
    figures = read('06_results/figures/round5/figure_manifest.json')
    add('04_code/visualization/round5_figures.py', figures['script_sha256'])
    for figure in figures['figures']:
        for item in figure['paths']:
            add(item['path'], item['sha256'])
    old_qa = read('10_review/MODELING_PHASE2_R5_NUMERICAL_QA_20260924.json')
    add('04_code/modeling_phase2/round5_qa.py', old_qa['script_sha256'])
    return dict(sorted(found.items()))


def restore(expected):
    if RESTORE.exists():
        raise RuntimeError('Restoration already recorded; run read-only audit instead.')
    planned = []
    attrs = ['# Exact checkout formats required by frozen Round 5 SHA-256 records.',
             '# Four mixed-newline CSVs are byte-preserved, including quoted fields.',
             '# Raw attachments remain ignored and are never rewritten.']
    for path, sha in expected.items():
        original = (ROOT / path).read_bytes()
        candidate, method = original, 'unchanged'
        if digest(original) != sha:
            if path.startswith('01_data/raw/'):
                raise RuntimeError('Raw attachment mismatch: ' + path)
            lf = original.replace(b'\r\n', b'\n')
            variants = [('LF', lf), ('CRLF', lf.replace(b'\n', b'\r\n'))]
            if path.endswith('.csv'):
                output = io.StringIO(newline='')
                csv.writer(output, lineterminator='\r\n').writerows(
                    csv.reader(io.StringIO(lf.decode('utf-8'), newline='')))
                variants.append(('CSV_CRLF_records_LF_quoted_field', output.getvalue().encode('utf-8')))
            matches = [(name, data) for name, data in variants if digest(data) == sha]
            if not matches:
                raise RuntimeError('No hash-proven EOL restoration: ' + path)
            method, candidate = matches[0]
        if not path.startswith('01_data/raw/'):
            if path.endswith(('.png', '.pdf')):
                attribute = '-text'
            elif b'\r\n' in candidate and b'\n' in candidate.replace(b'\r\n', b''):
                attribute = '-text'
            else:
                attribute = 'text eol=' + ('crlf' if b'\r\n' in candidate else 'lf')
            attrs.append('/' + path + ' ' + attribute)
        planned.append((path, original, candidate, method, sha))
    # All candidates must match original recorded digests before any writes occur.
    records = []
    for path, original, candidate, method, sha in planned:
        if original != candidate:
            (ROOT / path).write_bytes(candidate)
        records.append(dict(path=path, before_sha256=digest(original), expected_sha256=sha,
                            after_sha256=digest(candidate), method=method))
    (ROOT / '.gitattributes').write_bytes(('\n'.join(attrs) + '\n').encode('utf-8'))
    RESTORE.write_bytes((json.dumps(dict(created_utc=datetime.now(timezone.utc).isoformat(),
        source_commit='47b88843c43b55e1fd822ac0b5344ba1387e9fb9',
        scope='Hash-proven byte restoration only; no numerical changes or model runs',
        records=records), ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--restore-checkout', action='store_true')
    args = parser.parse_args()
    expected = targets()
    if args.restore_checkout:
        restore(expected)
    checks = []

    def check(name, passed, detail=None):
        checks.append(dict(check=name, passed=bool(passed), detail=detail))

    for path, sha in expected.items():
        check('strict_sha256:' + path, digest((ROOT / path).read_bytes()) == sha)
    config = read('05_experiments/configs/Q2_R5_v1.json')
    base = read(BASE + '/summary.json')
    scenario = read(SCEN + '/summary.json')
    manifest = read('01_data/processed/modeling_phase2/round5/INPUT_MANIFEST_v1.json')
    check('recorded_freeze_precedes_result', manifest['created_utc'] < config['created_utc'] < base['created_utc'],
          'Recorded timestamps and frozen hash agreement; not an independently timestamped pre-fit Git commit.')
    old_qa = read('10_review/MODELING_PHASE2_R5_NUMERICAL_QA_20260924.json')
    check('existing_numerical_QA_retained', old_qa['status'] == 'PASS' and len(old_qa['checks']) == 59
          and all(c['passed'] for c in old_qa['checks']), 'Reused saved QA, no repeat fitting or validation.')
    check('18_saved_splits', len(read(BASE + '/splits.json')) == 18)
    check('multistart_and_bootstrap', base['full_fit']['successful_starts'] == 12
          and base['bootstrap_valid'] == 200 and not base['upgrade_trigger'])
    check('failed_scenarios_retained', all((ROOT / f'06_results/raw/SCEN-Q2-R5-20260924-v{v}/FAILED.md').exists() for v in [1, 2]))
    check('valid_scenario_and_guards', scenario['run_id'].endswith('-v3') and scenario['TYPE_E'] == 0
          and not scenario['Q3_started'] and scenario['B8'] == 'QUARANTINED_UNREAD')
    figure_manifest = read('06_results/figures/round5/figure_manifest.json')
    check('4_figures_and_sources', len(figure_manifest['figures']) == 4 and all(
        (ROOT / path.replace('\\', '/')).exists() for figure in figure_manifest['figures'] for path in figure['source']))
    report = (ROOT / '03_models/modeling_phase2/round5/Q2_RESULTS_REPORT_v1.md').read_text(encoding='utf-8')
    paper = (ROOT / '08_paper/sections/Q2_ROUND5_PAPER_CANDIDATE_v1.md').read_text(encoding='utf-8')
    check('paper_matches_result_report', report == paper)
    interface = read('03_models/modeling_phase2/round5/Q2_TO_Q3_INTERFACE_v1.json')
    check('interface_parameter_identity', interface['parameters'] == base['parameters'])
    check('no_promotion_or_Q3', not interface['active_final'] and not interface['Q3_started'])
    expected_admission = dict(A='ENTER Q3', B='SENSITIVITY ONLY', C='ENTER Q3', D='ENTER Q3',
        E='ENTER Q3 AS SCENARIO', F='ENTER Q3 AS SCENARIO', G='ENTER Q3', H='ENTER Q3',
        I='DO NOT ENTER Q3', J='DO NOT ENTER Q3')
    check('interface_A_to_J', {r['category']: r['classification'] for r in interface.get('admission', [])}
          == expected_admission and interface.get('admission_effective_after') == 'Gate3 approval')
    check('figure_table_plan_exists', (ROOT / '03_models/modeling_phase2/round5/Q2_DELIVERY_FIGURE_TABLE_PLAN_v1.md').is_file())
    check('five_table_pairs', len(list((ROOT / '06_results/tables/round5').glob('TABLE-*.csv'))) == 5
          and len(list((ROOT / '06_results/tables/round5').glob('TABLE-*.md'))) == 5)
    for path in ['01_data/processed/modeling_phase2/round5/B9_v1.csv',
                 '01_data/processed/modeling_phase2/round5/B10_v1.csv',
                 SCEN + '/B9_extrapolation_scope.csv', SCEN + '/B10_source_diagnostic.csv']:
        prior = subprocess.check_output(['git', 'show', '47b88843c43b55e1fd822ac0b5344ba1387e9fb9:' + path], cwd=ROOT)
        def rows(data):
            return list(csv.reader(io.StringIO(data.decode('utf-8').replace('\r\n', '\n'), newline='')))
        check('restored_csv_cells_unchanged:' + path, rows(prior) == rows((ROOT / path).read_bytes()))
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode('utf-8').split('\0')
    check('raw_and_caches_not_tracked', not any(p.startswith('01_data/raw/real_attachments/')
          or '__pycache__/' in p or p.endswith(('.pyc', '.pyo')) for p in tracked))
    result = dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',
        created_utc=datetime.now(timezone.utc).isoformat(), scope='Takeover integrity only; no Gate3 decision',
        source_commit='47b88843c43b55e1fd822ac0b5344ba1387e9fb9',
        script_sha256=digest(Path(__file__).read_bytes()), strict_hash_count=len(expected), checks=checks)
    AUDIT.write_bytes((json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    print(json.dumps(dict(status=result['status'], checks=len(checks), strict_hashes=len(expected),
        failed=[c for c in checks if not c['passed']]), ensure_ascii=False))
    if result['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()

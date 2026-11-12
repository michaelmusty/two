"""D136 independent byte/provenance review and lossless P6400 CM adapter.

No production arithmetic is imported. Synthetic high digits do not certify
new harmonic/CM precision. The adapter references existing certified bytes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
STORE = DATA/'dyadic_rowjournal_P6400_col00_d132'
OUT = DATA/'dyadic_target_chart_review_d136.json'
ADAPTER = DATA/'dyadic_CM_P6400_col00_d136.json'
PATHS = {Path(__file__),ROOT/'dembele/certificates/dyadic-target-charts-d136.md'}
CACHE = {}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    if path not in CACHE:
        h = hashlib.sha256()
        with path.open('rb') as f:
            while raw := f.read(1 << 20):
                h.update(raw)
        CACHE[path] = {'path':str(path),'sha256':h.hexdigest()}
    return CACHE[path]


def match(records):
    for record in records:
        assert source(record['path']) == record,record['path']


def read(stem):
    p = DATA/(stem+'.json')
    PATHS.add(p)
    r = json.loads(p.read_text())
    assert r['status']=='pass',stem
    return r


def envelope(name):
    p = STORE/name
    PATHS.add(p)
    d = json.loads(p.read_text())
    canonical = json.dumps(d['value'],sort_keys=True,separators=(',',':')).encode()
    assert hashlib.sha256(canonical).hexdigest()==d['sha256']
    return d['value']


def receipt(ref, metadata):
    match([ref,metadata])
    r = json.loads(Path(ref['path']).read_text())
    assert r['status']=='pass' and r['exit_code']==0
    assert r['timeout_seconds']==180 and r['timeout_terminates_process_group']
    match([r['driver'],r['log'],*r['sources']])
    markers = [json.loads(s.split('|',1)[1]) for s in Path(r['log']['path']).read_text().splitlines() if s.startswith('PHASE_METADATA|')]
    assert markers==[metadata]
    return r


def publish_adapter(cm, current):
    values,errors = [],None
    refs = {Path(__file__),STORE/'CURRENT.json',STORE/'pool_CM.json',STORE/'SEALED.json',
            DATA/'dyadic_precision6400_review_d133.json',
            DATA/'dyadic_staged_P6400_col00_d133_seal.json'}
    for ci in range(17):
        coeffs,local_errors = [],[]
        for order in range(4):
            stem = f'dyadic_staged_P6400_col00_d133_coarse_c{ci:02d}_o{order}'
            r = read(stem)
            assert r['request']['chart']==ci and r['request']['order']==order
            c = r['certificates']
            assert c['old_overlap_checked']
            coeffs.append(c['coarse_value_beta'])
            local_errors.append(c['error_beta'])
            refs.add(DATA/(stem+'.json'))
        if errors is None:
            errors=local_errors
        assert local_errors==errors
        values.append({'CM_index':ci,'chart':'A','coarse_coefficients_beta':coeffs})
    assert errors==[12832,12848,12832,12864]
    binary=source(STORE/cm['name'])
    assert binary['sha256']==cm['sha256']
    refs.add(STORE/cm['name'])
    adapter={'status':'pass','milestone':'D136','kind':'lossless_metadata_adapter_of_reviewed_D133_CM',
             'working_precision_pi':6400,'harmonic_basis_column':0,
             'weighted_input_used':True,'verified_state_metadata':source(DATA/'dyadic_staged_P6400_col00_d133_seal.json'),
             'state_generation':current['tag'],'CM_charts_checked':17,
             'moment_chunks':[{'first_chart':0,'last_chart':16,'file':binary}],
             'checkpoint_files':[binary],'chunked_moment_payload_bytes':cm['bytes'],
             'duplicate_assembled_binary_written':False,
             'CM_moment_scalar_coefficients':17*12800*8,
             'coarse_orders':[0,1,2,3],'coarse_error_beta':errors,'CM_values':values,
             'arithmetic_precision_beta':12864,'kernel_gains_beta':[32,48,32,64],
             'full_sixteen_column_bank_precision_pi':800,
             'actual_harmonic_precision_increased':False,'actual_CM_precision_increased':False,
             'candidate_identification_proved':False,
             'sources':[source(p) for p in sorted(refs)]}
    text=json.dumps(adapter,indent=2)+'\n'
    if ADAPTER.exists():
        assert ADAPTER.read_text()==text
    else:
        with ADAPTER.open('x') as f:
            f.write(text)
    return source(ADAPTER)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    tick=time.monotonic()
    prior=read('dyadic_bank_recost_review_d135')
    inherited={r['path']:r['sha256'] for r in prior['sources']}
    assert len(inherited)==93928
    match(prior['sources'])
    completion=read('dyadic_bank_recost_completion_d135')
    assert completion['fixed_review']==source(DATA/'dyadic_bank_recost_review_d135.json')
    match(completion['review_receipts'])
    summary=read('dyadic_target_chart_controls_d136_completed')
    assert summary['completed_jobs']==17 and summary['workers']<=3
    match([summary['coordinator'],summary['driver']])
    current=envelope('CURRENT.json')
    cm=envelope('pool_CM.json')
    envelope('SEALED.json')
    assert current['tag']=='ready096' and cm['complete']
    cmfile=STORE/cm['name']
    assert source(cmfile)['sha256']==cm['sha256']==inherited[str(cmfile)]
    charts=read('dyadic_target_transports_d121')['CM_charts']
    charts=[c for c in charts if c['chart']=='A']
    rows=[]
    for job in summary['jobs']:
        ci=job['chart']
        r=receipt(job['receipt'],job['metadata'])
        meta=json.loads(Path(job['metadata']['path']).read_text())
        match(meta['sources'])
        match([meta['target_binary']])
        assert meta['chart']==ci and meta['working_precision_pi']==10552
        assert meta['seed_precision_pi']==6400 and meta['column']==0
        assert meta['prior_fixed_review']==source(DATA/'dyadic_bank_recost_review_d135.json')
        assert meta['two_composed_children_same_process'] and len(meta['child_seconds'])==2
        assert meta['all_old_CM_overlap_scalars']==12800*8
        for flag in ('actual_harmonic_precision_increased','actual_CM_precision_increased',
                     'candidate_identification_proved','full_bank_launch_admitted'):
            assert meta[flag] is False
        assert meta['input_kind']=='synthetic_high_digits_preserving_reviewed_P6400_weighted_rows'
        assert job['peak_rss_bytes']==meta['peak_rss_bytes']<=2*(1<<30)
        assert job['seconds']==r['wall_seconds']<=180
        for row in meta['old_weighted_inputs']:
            assert row['row_sha256']==current['state']['row_sha256'][row['state']]
        raw=Path(meta['target_binary']['path']).read_bytes()
        assert len(raw)==21104*8*165==meta['target_binary_bytes']
        assert all(byte<128 for byte in raw[164::165]),'unused top bits must be zero'
        with cmfile.open('rb') as f:
            f.seek(ci*cm['row_bytes'])
            old=f.read(cm['row_bytes'])
        assert hashlib.sha256(old).hexdigest()==cm['row_sha256'][ci]==meta['old_CM_row_sha256']
        assert len(old)==12800*8*100
        for index in range(12800*8):
            assert raw[index*165:index*165+100]==old[index*100:(index+1)*100]
        mass=int(charts[ci]['zeroth_moments'][0])% (1<<1319)
        assert int.from_bytes(raw[:165],'little')==mass
        assert raw[165:8*165]==bytes(7*165)
        rows.append({'chart':ci,'seconds':r['wall_seconds'],'peak_rss_bytes':meta['peak_rss_bytes'],
                     'target_binary':meta['target_binary'],'old_CM_scalars_checked':12800*8})
        del raw,old
    assert sorted(r['chart'] for r in rows)==list(range(17))
    rss=max(r['peak_rss_bytes'] for r in rows)
    conservative=sum(sorted((r['peak_rss_bytes'] for r in rows),reverse=True)[:3])
    assert conservative<=6*(1<<30)
    assert rss==summary['maximum_job_RSS_bytes']
    assert conservative==summary['conservative_concurrent_RSS_sum_bytes']
    adapter=publish_adapter(cm,current)
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    assert peak<=2*(1<<30)
    record={'status':'pass','milestone':'D136','independent_finite_review_complete':True,
            'prior_fixed_review':source(DATA/'dyadic_bank_recost_review_d135.json'),
            'prior_hash_count':len(inherited),'all_inherited_hashes_preserved':True,
            'passing_input_jobs':17,'failed_input_jobs':0,'charts':rows,
            'all_old_CM_overlap_scalars_checked':17*12800*8,
            'maximum_control_RSS_bytes':rss,'conservative_three_worker_RSS_sum_bytes':conservative,
            'longest_control_seconds':max(r['seconds'] for r in rows),
            'synthetic_target_inputs_not_new_arithmetic_precision':True,
            'published_P6400_CM_adapter':adapter,
            'all_17_integrated_chart_resource_controls_pass':True,
            'future_data_dependent_resources_still_require_admission_checks':True,
            'actual_harmonic_precision_increased':False,'candidate_identification_proved':False,
            'field_polynomial_constructed':False,'full_bank_launch_admitted':False,
            'resource_caps_changed':False,
            'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':peak,
            'sources':[source(p) for p in sorted(PATHS)]}
    now={r['path']:r['sha256'] for r in record['sources']}
    assert all(now.get(path)==sha for path,sha in inherited.items())
    if args.check:
        saved=json.loads(OUT.read_text())
        for key in record:
            if key not in ('wall_seconds','peak_rss_bytes'):
                assert record[key]==saved[key],key
    else:
        assert not OUT.exists()
        with OUT.open('x') as f:
            f.write(json.dumps(record,indent=2)+'\n')
        print('PHASE_METADATA|'+json.dumps(source(OUT)),flush=True)
    print('PASS|563_DYADIC_TARGET_CHART_REVIEW',flush=True)


if __name__=='__main__':
    main()

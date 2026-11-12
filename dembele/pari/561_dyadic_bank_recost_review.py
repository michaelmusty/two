"""D135 independent finite review of the planning model and inherited hashes.

Does not import source 560 or any production arithmetic. Checks exact counts,
storage arithmetic and measured totals; extrapolation assumptions stay empirical.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'dyadic_bank_recost_review_d135.json'
PATHS = {Path(__file__), ROOT / 'dembele/certificates/dyadic-bank-recost-d135.md'}
CACHE = {}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    if path not in CACHE:
        sha = hashlib.sha256()
        with path.open('rb') as f:
            while raw := f.read(1 << 20):
                sha.update(raw)
        CACHE[path] = {'path': str(path), 'sha256': sha.hexdigest()}
    return CACHE[path]


def read(name):
    path = DATA / (name + '.json')
    PATHS.add(path)
    result = json.loads(path.read_text())
    assert result['status'] == 'pass'
    return result


def match(records):
    for row in records:
        assert source(row['path']) == row, row['path']


def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-6), (a, b)


def weighted(P):
    # Sum integer byte widths directly, independently of source560's formula.
    width = 33 * 8 * ((P // 8 + 7) // 8)
    for degree in range(33, P):
        for basis in range(8):
            numerator = P - degree - basis
            bits = max(0, -(-numerator // 8))
            width += -(-bits // 8)
    return 174 * width


def counts(S, P):
    # A separate closed-form phase census. Initial/final phases total438;
    # each seed/correction has243 non-digit jobs, plus3 per low digit.
    corrections = (P - S - 1) // 33
    digit_count = -(-(P // 8) // 200)
    for step in range(corrections):
        bits = P // 8 - (S + 33 * step) // 8
        digit_count += -(-bits // 200)
    phases = 438 + 243 * (corrections + 1) + 3 * digit_count
    return corrections, phases, phases + corrections + 1 + 24 + 2


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    start = time.monotonic()
    prior = read('arithmetic_cover_criterion_review_d134')
    inherited = {r['path']:r['sha256'] for r in prior['sources']}
    assert len(inherited) == 93912
    match(prior['sources'])
    model = read('dyadic_bank_recost_d135')
    match(model['sources'])
    assert model['prior_fixed_review'] == source(DATA / 'arithmetic_cover_criterion_review_d134.json')
    assert model['certified_seeds'] == {'0':6400,'1':1600,'2_through_15':800}
    assert model['model_is_empirical_not_runtime_or_allocation_bound']
    for flag in ('actual_harmonic_precision_increased','candidate_identification_proved',
                 'field_polynomial_constructed','full_bank_launch_admitted','resource_caps_changed'):
        assert model[flag] is False
    receipt = read('dyadic_bank_recost_d135_attempt02.job')
    assert receipt['exit_code'] == 0 and receipt['timeout_seconds'] == 180
    assert receipt['timeout_terminates_process_group']
    match([receipt['driver'],receipt['log'],*receipt['sources']])
    metadata = [json.loads(s.split('|',1)[1]) for s in Path(receipt['log']['path']).read_text().splitlines() if s.startswith('PHASE_METADATA|')]
    assert metadata == [source(DATA / 'dyadic_bank_recost_d135.json')]
    # Preserve the diagnosed development failure and its original source bytes.
    failed_path = DATA / 'dyadic_bank_recost_d135_attempt01.job.json'
    PATHS.add(failed_path)
    failed = json.loads(failed_path.read_text())
    assert failed['status'] == 'failed' and failed['exit_code'] == 1
    match([failed['log'],failed['failed_driver_snapshot'],*failed['sources']])
    assert failed['driver']['sha256'] == failed['failed_driver_snapshot']['sha256']
    assert 'KeyError' in Path(failed['log']['path']).read_text()

    actual = read('dyadic_staged_P6400_col00_d133_completed')
    archive_secs = sum(json.loads(Path(r['receipt']['path']).read_text())['wall_seconds'] for r in actual['metadata_archives'])
    audit = read('dyadic_precision6400_audit_plan_d133_completed')
    audit_secs = sum(json.loads(Path(r['receipt']['path']).read_text())['wall_seconds'] for r in audit['jobs'])
    completion = read('dyadic_precision6400_completion_d133')
    match(completion['review_receipts'])
    reviews = sum(json.loads(Path(r['path']).read_text())['wall_seconds'] for r in completion['review_receipts'])
    total = sum(r['seconds'] for r in actual['jobs']) + archive_secs + audit_secs + reviews
    measured = model['measured_D133']
    close(total, measured['total_worker_seconds_with_reviews'])
    close(archive_secs, measured['archive_seconds'])
    close(audit_secs, measured['audit_worker_seconds'])
    close(reviews, measured['review_seconds'])
    assert measured['passing_jobs_including_reviews'] == 24456 + 97 + 24 + 2
    # Independently identify phase families from stable job keys.
    phase_totals = Counter()
    for row in actual['jobs']:
        key = row['key']
        if key.startswith(('operator','rhs')):
            phase = 'operator' if key.startswith('operator') else 'rhs'
        elif key.startswith('prepare') and key[7:10].isdigit():
            phase = 'prepare-rows'
        elif key.startswith('low_'):
            phase = '-'.join(key.split('_')[:2])
        elif key.startswith('coarse'):
            phase = 'coarse'
        elif '_e' in key:
            phase = key.split('_e')[0]
        else:
            if key.rsplit('_',1)[-1].isdigit():
                key = key.rsplit('_',1)[0]
            phase = key.replace('_','-')
        phase_totals[phase] += row['seconds']
    for phase,value in phase_totals.items():
        close(value, measured['phase_timings'][phase]['seconds'])

    expected_stages = {
        'full_bank_staged':[(800,1600,14),(1600,3200,15),(3200,6400,15),(6400,10552,16)],
        'full_bank_skip1600':[(800,3200,14),(1600,3200,1),(3200,6400,15),(6400,10552,16)],
        'full_bank_direct':[(800,10552,14),(1600,10552,1),(6400,10552,1)],
        'full_bank_1600_checkpoint':[(800,1600,14)],
        'one_target_column_pilot':[(6400,10552,1)],
    }
    legacy = read('dyadic_staged_lifetime_inventory_d132')['certificates']['schedules']
    known_inventory = {(r['seed_precision_pi'],r['precision_pi']):r for r in legacy}
    verified_schedules = []
    for schedule in model['schedules']:
        name = schedule['name']
        stages = [(r['seed'],r['target'],r['columns']) for r in schedule['stages']]
        assert stages == expected_stages[name]
        jobs = sum(n * counts(S,P)[2] for S,P,n in stages)
        assert jobs == schedule['total_jobs_including_archives_audits_reviews']
        assert schedule['approximate_external_record_files'] == 3 * jobs
        assert schedule['production_launch_admitted'] is False
        assert schedule['incremental_reviews_implemented_or_admitted'] is False
        for scenario in schedule['timing_scenarios']:
            work = scenario['full_frame_and_quadric_worker_seconds_allowance'] + scenario['cumulative_review_growth_seconds_allowance']
            active = work
            for stage in scenario['stages']:
                S,P,n = stage['seed'],stage['target'],stage['columns']
                inv = stage['inventory']
                corr, phases, count = counts(S,P)
                assert inv['corrections'] == corr and inv['production_jobs'] == phases
                assert sum(inv['phase_counts'].values()) == phases
                assert stage['jobs_per_column'] == count
                assert inv['weighted_bytes'] == weighted(P)
                K = P // 8
                cm = 17 * 2 * P * 8 * -(-K // 8)
                final_u = S + 33 * corr
                residual = 174 * max(33, P-final_u) * 8 * -(-(K-final_u//8) // 8)
                assert inv['CM_bytes'] == cm
                assert inv['sealed_payload_bytes'] == weighted(P) + cm + residual + 174 * 32
                if (S,P) in known_inventory:
                    assert inv['largest_working_store']['bytes'] == known_inventory[S,P]['maximum_bound']['total_bytes']
                close(stage['worker_seconds'],sum(stage['worker_seconds_by_phase'].values()))
                close(stage['three_worker_active_seconds'],sum(stage['active_seconds_by_phase'].values()))
                assert stage['worker_seconds']/3 <= stage['three_worker_active_seconds'] <= stage['worker_seconds']
                work += n*stage['worker_seconds']
                active += n*stage['three_worker_active_seconds']
            close(work/3600,scenario['worker_hours'])
            close(work/(3*86400),scenario['ideal_three_worker_days'])
            close(active/86400,scenario['dependency_aware_active_days'])
        if name == 'full_bank_direct':
            assert len(schedule['store_cap_failures']) == 2
            for fail in schedule['store_cap_failures']:
                S,P = fail['seed'],fail['target']
                K = P//8
                r0 = 174*(P-S)*8*-(-(K-S//8)//8)
                r1 = 174*(P-S-33)*8*-(-(K-(S+33)//8)//8)
                assert weighted(P)+r0+r1+64*(1<<20) > 2*(1<<30)
        else:
            assert not schedule['store_cap_failures']
        storage = schedule['storage']
        payload = sum(n*(weighted(P)+17*2*P*8*-(-(P//8)//8)+174*32+
                            174*max(33,P-(S+33*counts(S,P)[0]))*8*-(-(P//8-(S+33*counts(S,P)[0])//8)//8))
                      for S,P,n in stages)
        assert storage['payload_bytes'] == payload
        assert storage['external_20KiB_per_job_allowance_bytes'] == 20480*jobs
        saved = storage['cumulative_review_catalogue_allowance_bytes']-storage['incremental_review_catalogue_scenario_bytes']
        assert schedule['additional_allocated_bytes_measured_ratio_scenario']-saved == schedule['incremental_review_additional_bytes_measured_scenario']
        assert schedule['additional_bytes_allowance_scenario']-saved == schedule['incremental_review_additional_bytes_allowance_scenario']
        free = model['filesystem_observation']['filesystem']['free']
        reserve = schedule['proposed_free_space_reserve_bytes']
        for key,required in [('incremental_review_shortfall_measured_scenario_bytes','incremental_review_additional_bytes_measured_scenario'),
                             ('incremental_review_shortfall_allowance_scenario_bytes','incremental_review_additional_bytes_allowance_scenario')]:
            assert schedule[key] == max(0,schedule[required]+reserve-free)
        verified_schedules.append({'name':name,'jobs':jobs,'correction_columns':sum(n*counts(S,P)[0] for S,P,n in stages)})

    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    assert peak <= 2*(1<<30)
    record = {'status':'pass','milestone':'D135','independent_finite_review_complete':True,
              'prior_fixed_review':source(DATA/'arithmetic_cover_criterion_review_d134.json'),
              'prior_hash_count':len(inherited),'passing_input_jobs':1,'resolved_failed_development_jobs':1,
              'verified_schedules':verified_schedules,'timing_extrapolation_remains_empirical':True,
              'all_inherited_hashes_preserved':True,'full_bank_launch_admitted':False,
              'actual_harmonic_precision_increased':False,'candidate_identification_proved':False,
              'field_polynomial_constructed':False,'resource_caps_changed':False,
              'wall_seconds':time.monotonic()-start,'peak_rss_bytes':peak,
              'sources':[source(p) for p in sorted(PATHS)]}
    now = {r['path']:r['sha256'] for r in record['sources']}
    assert all(now.get(path) == sha for path,sha in inherited.items())
    if args.check:
        saved = json.loads(OUT.read_text())
        for key in record:
            if key not in ('wall_seconds','peak_rss_bytes'):
                assert record[key] == saved[key],key
        print('PASS|561_DYADIC_BANK_RECOST_REVIEW',flush=True)
    else:
        assert not OUT.exists()
        with OUT.open('x') as f:
            f.write(json.dumps(record,indent=2)+'\n')
        print('PHASE_METADATA|'+json.dumps(source(OUT)),flush=True)
        print('PASS|561_DYADIC_BANK_RECOST_REVIEW',flush=True)


if __name__ == '__main__':
    main()

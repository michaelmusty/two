"""D130 fixed finite review, preserving all D129 hashes and failure history."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'dyadic_target_feasibility_review_d130.json'
PREFIX = 'dyadic_target_feasibility_review_d130'
PATHS, CACHE = {Path(__file__)}, {}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    if path not in CACHE:
        sha = hashlib.sha256()
        with path.open('rb') as f:
            while block := f.read(1 << 20):
                sha.update(block)
        CACHE[path] = {'path': str(path), 'sha256': sha.hexdigest()}
    return CACHE[path]


def checked(rows):
    for row in rows:
        assert source(row['path']) == row, row['path']


def read(stem):
    path = DATA / (stem + '.json')
    PATHS.add(path)
    packet = json.loads(path.read_text())
    assert packet['status'] == 'pass'
    return packet


def coeffs(value):
    assert len(value) == 8
    return tuple(int(v) & MASK for v in value)


MASK = (1 << 1319) - 1


def add(a, b):
    return tuple((x + y) & MASK for x, y in zip(a, b))


def sub(a, b):
    return tuple((x - y) & MASK for x, y in zip(a, b))


def mul(a, b):
    # Separate ordinary multiplication in Z[x]/(x^8-8x^6+20x^4-16x^2+2).
    ans = [0] * 15
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            ans[i + j] += x * y
    for k in range(14, 7, -1):
        z = ans[k]
        for i, coefficient in ((0, -2), (2, 16), (4, -20), (6, 8)):
            ans[k - 8 + i] += z * coefficient
    return tuple(x & MASK for x in ans[:8])


def valuation(a):
    return min([10552] + [8 * ((x & -x).bit_length() - 1) + i for i, x in enumerate(a) if x])


def weighted_bound_inputs():
    data = read('dyadic_target_transports_d121')
    transitions = data['transitions']
    vals, distinct, counts = [], set(), Counter()
    for e in transitions:
        for ch in e['children']:
            assert ch['normalized_error_pi'] >= 10552
            a, b, c = [coeffs(x) for x in ch['normalized_center'][:3]]
            delta = sub(a, mul(b, c))
            vals.append((valuation(c), valuation(delta)))
            assert min(vals[-1]) >= 1
            distinct.add((a, b, c))
            counts['b_zero' if not any(b) else 'b_nonzero'] += 1
            counts['c_zero' if not any(c) else 'c_nonzero'] += 1
    assert len(vals) == 348 and len(distinct) == 165
    assert counts == {'b_nonzero': 253, 'b_zero': 95, 'c_nonzero': 275, 'c_zero': 73}
    one = (1,) + (0,) * 7
    cm = []
    for chart in data['CM_charts']:
        if chart['chart'] != 'A':
            continue
        assert chart['normalized_error_pi'] >= 10552
        A, B, C = [coeffs(x) for x in chart['normalized_center'][:3]]
        outer_delta = sub(A, mul(B, C))
        for child in transitions[chart['target_edge']]['children']:
            a, b, c = [coeffs(x) for x in child['normalized_center'][:3]]
            denominator = add(one, mul(C, b))
            c_numerator = add(c, mul(C, a))
            delta_numerator = mul(outer_delta, sub(a, mul(b, c)))
            row = (valuation(denominator), valuation(c_numerator), valuation(delta_numerator))
            assert row[0] == 0 and min(row[1:]) >= 1
            cm.append(row)
    assert len(cm) == 34
    return {'original_children_checked': 348, 'CM_compositions_checked': 34,
            'all_denominators_units_and_c_delta_divisible_by_pi': True,
            'ordinary_integer_quotient_arithmetic': True,
            'original_minimum_c_delta_valuations': [min(x[i] for x in vals) for i in (0, 1)],
            'CM_minimum_c_delta_valuations': [min(x[i] for x in cm) for i in (1, 2)],
            'weighted_only_fixed_point_replay_or_production_driver_implemented': False}


def finite_review():
    agg = read('dyadic_target_audit_aggregate_d130')['certificates']
    assert agg['map_control_jobs'] == 74 and agg['complete_backend_comparison_pairs'] == 26
    assert agg['complete_backend_scalar_comparisons'] == 1698208
    assert agg['additional_single_backend_cost_controls'] == 22
    assert agg['actual_old_extension_sum_scalar_overlaps'] == 25600
    assert agg['complete_CM_direct_Horner_value_comparisons'] == 4
    assert agg['low_profile_first_column_matches_for_all_165_groups']
    assert not agg['actual_precision_increased']
    low = read('dyadic_target_audit_low_d130')['certificates']
    assert [s['bits'] for s in low['stages']] == [200,400,600,800,1000,1200,1319]
    assert [s['correction_bits'] for s in low['stages']] == [200]*6 + [119]
    assert all(s['complete_production_original_equations'] == 44544 for s in low['stages'])
    assert low['all_stage_prefix_scalar_comparisons'] == 267264
    assert low['independent_ordinary_low_equation_scalar_checks'] == 5376
    for label in ('full0','full83','rhs0','extend0','correction0','cm0','aggregate','low','bridge','quadrics_c00','quadrics_c08','quadrics_c16'):
        p = read('dyadic_target_audit_' + label + '_d130')
        assert p['production_arithmetic_not_imported']
    inv = read('dyadic_compact_inventory_d130')['certificates']
    assert inv['target_16_column_uniform_plus_CM_bytes'] == 46354513920
    assert inv['target_16_column_existing_four_payload_plus_CM_bytes'] == 104611284096
    target = [r for r in inv['layouts'] if r['P'] == 10552 and r['seed'] == 6400][0]
    assert target['uniform_bytes'] == 174 * 10552 * 8 * 165 == 2423583360 > 2**31
    assert target['weighted_bytes'] == 1217418840
    assert target['inherited_conservative_scratch_total_bytes'] == 15944609416
    assert not target['fits_D129_2GiB_scratch_limit']
    assert not inv['integrated_target_scratch_protocol_implemented']
    working = target['weighted_bytes'] + 2 * target['largest_scaled_residual_bytes']
    assert working == 1968764760 and 2**31 - working == 178718888
    assert 16 * (target['weighted_bytes'] + target['CM_bytes_per_column']) == 27055881600
    for phase in ('zero', 'target_row', 'inventory'):
        assert not read('dyadic_compact_' + phase + '_d130')['actual_harmonic_precision_increased']
    for phase in ('manifest', 'rows', 'target'):
        read('dyadic_stream_auth_' + phase + '_d130')
    model = read('dyadic_target_schedule_budget_d130')
    assert model['model_is_empirical_not_a_runtime_bound'] and not model['complete_costed_field_construction']
    assert len(model['scenarios']) == 16
    for r in model['scenarios']:
        expected = 4592 if r['schedule'] == 'staged' else 4623
        assert r['correction_column_steps'] == expected
        assert sum(s['columns'] * ((s['target'] - s['seed'] - 1) // 33) for s in r['stages']) == expected
        assert abs(sum(r['modeled_process_seconds_by_phase'].values()) / 3600 - r['modeled_process_hours']) < 1e-8
        assert abs(r['modeled_process_hours'] / 72 - r['ideal_three_worker_days_excluding_extra_IO']) < 1e-8
        assert not r['admitted_production_schedule']
    bridge = read('dyadic_target_audit_bridge_d130')['certificates']
    poly = [2,0,-16,0,20,0,-8,0,1]
    assert bridge['base_field_polynomial'] == poly
    assert sum(a * (-1)**i for i,a in enumerate(poly)) == bridge['norm_delta'] == -1
    assert sum(a * 27**i for i,a in enumerate(poly)) % 31 == 0
    assert sum(i*a * 27**(i-1) for i,a in enumerate(poly) if i) % 31 == 12
    assert (1+27) % 31 == 20**2 % 31 == 28 and 2*20 % 31 == 9
    assert not bridge['candidate_twist_identified_or_disproved']
    return {'aggregate_controls': agg, 'low_lift': low,
            'weighted_representation_coefficient_bounds': weighted_bound_inputs(),
            'prospective_weighted_plus_two_residual_bytes': working,
            'prospective_layout_is_not_an_integrated_scratch_certificate': True,
            'empirical_scenario_count': 16, 'global_twist_witness_independently_recomputed': True,
            'synthetic_controls_do_not_raise_actual_precision': True}


def build():
    prior = read('dyadic_precision3200_review_d129')
    assert prior['independent_finite_review_complete'] and len(prior['sources']) == 15600
    checked(prior['sources'])
    for stem in ('dyadic_precision3200_review_d129_attempt01','dyadic_precision3200_review_d129_recheck01'):
        packet = read(stem + '.job')
        checked(packet['sources'] + [packet['driver'], packet['log']])
    finite = finite_review()
    planned = set()
    counts = {'map':57, 'low':26, 'CM':9, 'storage_comparison':12,
              'dense_schedule':14, 'auth':3, 'audit':12}
    for name, count in counts.items():
        planpath = DATA / ('dyadic_target_' + name + '_plan_d130.json')
        plan = json.loads(planpath.read_text())
        summary = read(planpath.stem + '_completed')
        checked([summary['plan'], summary['coordinator']])
        assert summary['completed_jobs'] == len(plan['jobs']) == count
        assert 1 <= summary['worker_limit'] <= 3
        if name in ('low','auth'):
            assert summary['worker_limit'] == 1
        assert {j['stem'] for j in summary['jobs']} == {j['stem'] for j in plan['jobs']}
        for spec, row in zip(plan['jobs'], summary['jobs']):
            assert spec['stem'] == row['stem'] and row['stem'] not in planned
            planned.add(row['stem'])
            checked([row['receipt'], row['metadata']])
            job = json.loads(Path(row['receipt']['path']).read_text())
            assert job['command'] == ['python3', str(ROOT/spec['driver'])] + spec['args'] + ['--output', spec['stem']]
    jobs, failures, categories, peaks, successful_stems = [], [], Counter(), [], set()
    for path in sorted(DATA.glob('*d130*')):
        if path.is_dir() or path.name.startswith(PREFIX) or path.name.startswith('dyadic_target_feasibility_completion_d130'):
            continue
        PATHS.add(path)
        if path.suffix == '.log':
            assert path.with_suffix('.job.json').exists()
        if path.suffix != '.json':
            continue
        packet = json.loads(path.read_text())
        checked([s for s in packet.get('sources', []) if isinstance(s, dict) and 'sha256' in s])
        if 'peak_rss_bytes' in packet:
            peaks.append(packet['peak_rss_bytes'])
        if not path.name.endswith('.job.json'):
            continue
        assert packet['timeout_seconds'] == 180 and packet['timeout_terminates_process_group']
        checked([packet['log']])
        if packet['status'] != 'pass':
            assert path.name == 'dyadic_target_schedule_budget_d130_attempt01.job.json'
            checked([packet['failed_driver_snapshot']])
            assert packet['failed_driver_snapshot']['sha256'] == packet['driver']['sha256']
            assert 'TypeError' in Path(packet['log']['path']).read_text()
            failures.append({'receipt': str(path), 'driver_snapshot': packet['failed_driver_snapshot'],
                             'resolved_by': 'dyadic_target_schedule_budget_d130_attempt02.job.json'})
            continue
        assert packet['exit_code'] == 0
        checked([packet['driver']])
        command = packet['command']
        stem = command[command.index('--output') + 1]
        assert stem not in successful_stems
        successful_stems.add(stem)
        output = DATA / (stem + '.json')
        read(stem)
        bindings = [json.loads(line.split('|',1)[1]) for line in Path(packet['log']['path']).read_text().splitlines()
                    if line.startswith('PHASE_METADATA|')]
        assert bindings == [source(output)]
        driver = Path(packet['driver']['path']).name
        categories[driver] += 1
        jobs.append({'receipt': path.name, 'driver': driver, 'wall_seconds': packet['wall_seconds']})
    assert len(jobs) == 137 and len(failures) == 1
    assert dict(categories) == {
        '533_dyadic_target_operation_controls.py':74, '534_dyadic_target_low_lift.py':26,
        '535_dyadic_target_CM_comparison_controls.py':12, '536_dyadic_compact_retention_control.py':9,
        '537_dyadic_streaming_authentication_control.py':3, '538_dyadic_target_independent_review.py':12,
        '539_dyadic_target_schedule_budget.py':1}
    assert successful_stems - planned == {'dyadic_target_full_e000_b0_adaptive_d130',
        'dyadic_target_full_e000_b0_gmp_d130', 'dyadic_target_extend3200_e000_b0_adaptive_d130',
        'dyadic_target_schedule_budget_d130'}
    stats = {'passed':len(jobs), 'failed_attempts_retained_and_resolved':len(failures),
             'sum_passing_wall_seconds':sum(j['wall_seconds'] for j in jobs),
             'maximum_passing_wall_seconds':max(j['wall_seconds'] for j in jobs),
             'maximum_single_process_input_peak_rss_bytes':max(peaks)}
    ledgerpath = DATA / 'dyadic_target_feasibility_sources_d130.json'
    ledger = json.loads(ledgerpath.read_text())
    assert ledger['execution_status'] == 'complete'
    for key, value in stats.items():
        assert abs(value - ledger['bounded_input_jobs'][key]) < 1e-6, key
    PATHS.update([ledgerpath, ROOT/'dembele/certificates/dyadic-target-feasibility-d130.md',
                  ROOT/'dembele/certificates/arithmetic-construction-d130.md',
                  ROOT/'dembele/certificates/stocktake-2026-09-28.md', ROOT/'dembele/pari/run_d130_batch.py'])
    manifest = [source(p) for p in sorted(PATHS)]
    assert {(r['path'],r['sha256']) for r in prior['sources']} <= {(r['path'],r['sha256']) for r in manifest}
    return {'status':'pass', 'milestone':'D130', 'independent_finite_review_complete':True,
            'production_arithmetic_not_imported_by_reviewer':True, 'inherited_D129_hashes_preserved':15600,
            'finite_certificates':finite, 'input_job_categories':dict(categories),
            'bounded_input_jobs':jobs, 'retained_failed_attempts':failures, 'input_job_statistics':stats,
            'full_bank_precision_pi':800, 'actual_column_precisions':{'0':3200,'1':1600},
            'actual_precision_increased':False, 'candidate_identification_proved':False,
            'target_field_polynomial_constructed':False, 'full_target_production_admitted':False,
            'sources':manifest}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    if args.check:
        result = json.loads(OUT.read_text())
        assert result['status'] == 'pass' and result['independent_finite_review_complete']
        checked(result['sources'])
    else:
        assert not OUT.exists()
        result = build()
        OUT.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'sources':len(result['sources']), 'passing_inputs':len(result['bounded_input_jobs']),
                      'retained_failed_attempts':len(result['retained_failed_attempts'])}), flush=True)
    print('PASS|540_DYADIC_TARGET_FEASIBILITY_REVIEW', flush=True)

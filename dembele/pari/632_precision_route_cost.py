"""D152 bounded precision/height cost assessment; no bank is computed.

Exact sufficient thresholds and inventories, with empirical per-job
allowances inherited from D139. Run only through run_dyadic_capped.py.
"""
from datetime import datetime, timezone
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'precision_route_cost_d152.json'
PATHS = {Path(__file__)}
CAP = 2*(1 << 30)


def source(path):
    p = Path(path).resolve()
    PATHS.add(p)
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def module(name, filename):
    p = ROOT / 'dembele/pari' / filename
    source(p)
    spec = importlib.util.spec_from_file_location(name, p)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


logs = module('d152_logs', '447_cm_disk_vanishing_budget.py')
inventory = module('d152_inventory', '560_dyadic_bank_recost.py')


def read(stem):
    p = DATA / (stem + '.json')
    source(p)
    obj = json.loads(p.read_text())
    assert obj['status'] == 'pass', stem
    return obj


def encoded(interval):
    return list(map(str, interval))


def conditional_bounds(P, n):
    return 2*P+3310-33*n, 2*P+2784-296*n


def phase_count(inv, phase):
    if phase == 'archive':
        return inv['archive_jobs']
    if phase == 'receipt-discovery':
        return inv['production_jobs']
    if phase == 'independent-audits':
        return 24
    if phase == 'fixed-review-and-replay':
        return 2
    return inv['phase_counts'][phase]


def plan(name, targets, baseline, parameters):
    inventories = [(S, P, columns, inventory.inventory(P, S)) for S, P, columns in targets]
    jobs = sum(n*(i['production_jobs']+i['archive_jobs']+26) for S, P, n, i in inventories)
    payload = sum(n*i['sealed_payload_bytes'] for S, P, n, i in inventories)
    meta = sum(n*i['sealed_metadata_logical_allowance_bytes'] for S, P, n, i in inventories)
    extra = max(max(0, i['largest_working_store']['bytes']-i['sealed_payload_bytes']) for S, P, n, i in inventories)
    catalogue = 4*jobs*220
    measured = math.ceil(payload+meta*parameters['store_metadata_allocation_ratio']
                         +jobs*parameters['external_allocated_bytes_per_job']+catalogue+extra)
    allowance = payload+meta+jobs*20480+catalogue+extra
    scenarios = []
    for b in baseline['timing_scenarios']:
        details = []
        phase_totals = {}
        for S, P, n, inv in inventories:
            old = next(x for x in b['stages'] if x['seed'] == S)
            assert P <= old['target'] and S == old['seed']
            active, worker = {}, {}
            for phase in old['active_seconds_by_phase']:
                numerator = phase_count(inv, phase)
                denominator = phase_count(old['inventory'], phase)
                assert 0 < numerator <= denominator
                ratio = numerator/denominator
                active[phase] = old['active_seconds_by_phase'][phase]*ratio
                worker[phase] = old['worker_seconds_by_phase'][phase]*ratio
                phase_totals[phase] = phase_totals.get(phase, 0)+n*active[phase]
            details.append({'seed': S, 'target': P, 'columns': n,
                            'inventory': inv, 'active_seconds_per_column': sum(active.values()),
                            'worker_seconds_per_column': sum(worker.values()),
                            'active_seconds_by_phase': active, 'worker_seconds_by_phase': worker})
        # Retain the complete baseline bank review and comparison allowances.
        # No credit for lower arithmetic size, lower third-jet work, or a
        # supposedly faster unmeasured integrated production coordinator.
        review = b['graph_review_seconds_allowance']
        comparison = b['common_comparison_seconds_allowance']
        active = sum(x['columns']*x['active_seconds_per_column'] for x in details)+review+comparison
        worker = sum(x['columns']*x['worker_seconds_per_column'] for x in details)+review+comparison
        scenarios.append({'scenario': b['scenario'], 'active_days': active/86400,
                          'active_hours': active/3600, 'worker_hours': worker/3600,
                          'retained_graph_review_seconds_allowance': review,
                          'retained_common_comparison_seconds_allowance': comparison,
                          'active_seconds_by_phase_all_columns': phase_totals,
                          'stages': details})
    return {'name': name, 'total_jobs_including_archives_audits_reviews': jobs,
            'additional_allocated_bytes_measured_ratio_scenario': measured,
            'additional_bytes_allowance_scenario': allowance,
            'recommended_free_bytes_including_10GiB_reserve': allowance+10*(1 << 30),
            'storage_components': {'payload_bytes': payload, 'metadata_logical_bytes': meta,
                                   'incremental_catalogue_allowance_bytes': catalogue,
                                   'largest_active_extra_bytes': extra},
            'all_stages_fit_2GiB_logical_store_cap': all(i['fits_2GiB_store_cap'] for S, P, n, i in inventories),
            'timing_scenarios': scenarios}


def calculate():
    inherited = read('summed_transfer_review_d151')
    assert inherited['finite_rational_witness_search_parked']
    assert inherited['best_current_proved_relation_height_upper'] == 15237
    budget = read('cm_arithmetic_height_budget_d118')['budgets']
    recognized = read('dyadic_P1600_recognition_review_d140')
    assert recognized['recognition_complete'] and recognized['same_saturated_integer_lattice_as_candidate']
    current = read('dyadic_integral_quadrics1600_d138')
    recost = read('dyadic_indexed_bank_recost_r2_d139')
    # Bind the direct proof sources, not just their rounded conclusions.
    for filename in ['construction-reassessment-d120.md', 'dyadic-P1600-recognition-d140.md',
                     'dyadic-target-charts-d136.md', 'dyadic-indexed-recost-d139.md']:
        source(ROOT / 'dembele/certificates' / filename)
    heights = read('P1600_proof_gap_diagnostics_r2_d141')['section_budget_diagnostics']
    assert heights['best_recognized_max_coefficient_l1'] == 29299
    old_L = budget['maximum_quadric_coefficient_l1_norm']
    assert old_L == 42550
    thresholds = []
    for row in budget['thresholds']:
        n = row['order']
        F = tuple(map(Q, row['upper_bound_expression_interval']))
        # (16N_n(P)+A_n(P))/272 = P/8+(55744-824*n)/272.
        constant = Q(55744-824*n, 272)
        critical = (8*(F[0]/logs.LOG2[1]-constant), 8*(F[1]/logs.LOG2[0]-constant))
        rounded = 8*((critical[1]/8).__floor__()+1)
        assert rounded-8 <= critical[0] < critical[1] < rounded
        shortF = logs.plus(F, logs.log(Q(29299, old_L)))
        shortcritical = (8*(shortF[0]/logs.LOG2[1]-constant), 8*(shortF[1]/logs.LOG2[0]-constant))
        shortP = 8*((shortcritical[1]/8).__floor__()+1)
        assert shortP-8 <= shortcritical[0] < shortcritical[1] < shortP
        samples = []
        for P in [1600, 3200, 6400, 10480, 10552]:
            N, A = conditional_bounds(P, n)
            Z = logs.scale(logs.LOG2, Q(16*N+A, 272))
            margin = logs.plus(Z, logs.scale(F, -1))
            assert margin[1] < 0 or margin[0] > 0
            samples.append({'precision_pi': P, 'conditional_nonanchor_beta': N,
                            'conditional_anchor_beta': A, 'margin_interval': encoded(margin),
                            'sufficient_if_future_enclosures_contain_zero': margin[0] > 0})
        observed = current['comparison_with_sufficient_bounds'][n-1]
        N, A = conditional_bounds(1600, n)
        assert observed['degree16_achieved_lower_beta'] >= N
        assert observed['anchor_achieved_lower_beta'] >= A
        thresholds.append({'order': n, 'critical_P_interval': encoded(critical),
                           'sufficient_P_multiple_of_8': rounded,
                           'shorter_basis_critical_P_interval': encoded(shortcritical),
                           'shorter_basis_sufficient_P_multiple_of_8': shortP,
                           'sample_margins': samples,
                           'observed_P1600_nonanchor_gain_over_uniform_design': observed['degree16_achieved_lower_beta']-N,
                           'observed_P1600_anchor_gain_over_uniform_design': observed['anchor_achieved_lower_beta']-A})
    assert [r['sufficient_P_multiple_of_8'] for r in thresholds] == [10416, 10480, 10552]
    baselines = {p['name']: p for p in recost['schedules']}
    baseline = baselines['remaining_staged_conditional_target']
    full = plan('rank45_P10480_staged_bank', [(1600,3200,15), (3200,6400,15), (6400,10480,16)], baseline, recost['cost_parameters'])
    unchanged = plan('P10552_reconstruction_control', [(1600,3200,15), (3200,6400,15), (6400,10552,16)], baseline, recost['cost_parameters'])
    for key in ['total_jobs_including_archives_audits_reviews', 'storage_components',
                'additional_allocated_bytes_measured_ratio_scenario', 'additional_bytes_allowance_scenario',
                'recommended_free_bytes_including_10GiB_reserve']:
        assert unchanged[key] == baseline[key], key
    for a, b in zip(unchanged['timing_scenarios'], baseline['timing_scenarios']):
        assert abs(a['active_days']-b['active_days']) < 1e-10
        assert abs(a['worker_hours']-b['worker_hours']) < 1e-10
    pilot = plan('one_column_P3200_timing_pilot', [(1600,3200,1)], baselines['next_P3200_checkpoint'], recost['cost_parameters'])
    # Keep the entire bank-level review allowance for this one-column pilot.
    direct = inventory.inventory(10480, 1600)
    assert not direct['fits_2GiB_store_cap']
    savings = {'jobs': baseline['total_jobs_including_archives_audits_reviews']-full['total_jobs_including_archives_audits_reviews'],
               'retention_allowance_bytes': baseline['additional_bytes_allowance_scenario']-full['additional_bytes_allowance_scenario'],
               'active_hours_by_scenario': [24*(old['active_days']-new['active_days']) for old, new in zip(baseline['timing_scenarios'], full['timing_scenarios'])]}
    return {'status': 'pass', 'milestone': 'D152',
            'uniform_design_thresholds': thresholds,
            'rank45_two_positive_order_sufficient_P': 10480,
            'four_coefficient_sufficient_P': 10552,
            'P10480_sufficiency_is_conditional_on_new_certified_zero_enclosures': True,
            'rank45_identification_step_is_companion_proof': True,
            'observed_extra_digits_not_extrapolated': True,
            'proved_relation_height_upper': 15237, 'P1600_sufficient_relation_height_target': 623,
            'D148_relation_height_is_not_substituted_for_D118_section_height': True,
            'schedules': [full, pilot], 'P10552_baseline': baseline,
            'P10552_model_reconstruction_passed': True, 'savings_against_P10552': savings,
            'direct_P1600_to_P10480_rejected_inventory': direct,
            'all_16_columns_required_by_current_full_frame_evaluator': True,
            'times_are_empirical_allowances_not_runtime_bounds': True,
            'P10480_cost_method': 'Retain D139 P10552 per-phase mean job costs and all bank review/comparison allowances; adjust only exact phase counts. No credit for smaller arithmetic size or omitting order three.',
            'new_precision_bank_admitted': False, 'actual_harmonic_precision_increased': False,
            'candidate_identification_proved': False, 'positive_exact_quadric_vanishing_proved': False,
            'field_polynomial_constructed': False, 'resource_caps_changed': False,
            'next_recommended_preparation': 'Prepare a separately reviewed one-column P1600-to-P3200 integrated timing pilot using an already reviewed column-2 seed and the D139 indexed coordinator; do not launch it or a bank in this cost assessment.'}


if __name__ == '__main__':
    assert __debug__ and not OUT.exists()
    tick = time.monotonic()
    result = calculate()
    disk = shutil.disk_usage(ROOT)
    result['filesystem_observation'] = {'observed_utc': datetime.now(timezone.utc).isoformat(), **disk._asdict(),
                                       'not_a_reservation': True}
    result['free_space_shortfalls_at_observation_bytes'] = {
        row['name']: max(0, row['recommended_free_bytes_including_10GiB_reserve']-disk.free)
        for row in result['schedules']}
    result['wall_seconds'] = time.monotonic()-tick
    result['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    assert result['peak_rss_bytes'] < CAP
    result['sources'] = [source(p) for p in sorted(PATHS)]
    with OUT.open('x') as out:
        out.write(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'thresholds': [r['sufficient_P_multiple_of_8'] for r in result['uniform_design_thresholds']],
                      'shorter_basis_thresholds': [r['shorter_basis_sufficient_P_multiple_of_8'] for r in result['uniform_design_thresholds']],
                      'free_GiB': disk.free/(1 << 30),
                      'schedules': [{'name': s['name'], 'jobs': s['total_jobs_including_archives_audits_reviews'],
                                     'active_hours': [x['active_hours'] for x in s['timing_scenarios']],
                                     'storage_GiB': [s['additional_allocated_bytes_measured_ratio_scenario']/(1 << 30), s['additional_bytes_allowance_scenario']/(1 << 30)],
                                     'free_GiB_with_reserve': s['recommended_free_bytes_including_10GiB_reserve']/(1 << 30)} for s in result['schedules']],
                      'savings': result['savings_against_P10552']}), flush=True)
    print('PHASE_METADATA|'+json.dumps(source(OUT)), flush=True)
    print('PASS|632_PRECISION_ROUTE_COST', flush=True)

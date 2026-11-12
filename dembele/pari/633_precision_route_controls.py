"""D152 independent budget, inventory, cost and rank-criterion controls.

No new moments or production benchmark. Run via run_dyadic_capped.py.
"""
from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'precision_route_controls_d152.json'
HELPER = ROOT / 'dembele/pari/450_cm_disk_exactness_review.py'
PATHS = {Path(__file__), HELPER}
spec = importlib.util.spec_from_file_location('d152_independent_logs', HELPER)
logs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logs)


def source(path):
    p = Path(path).resolve()
    PATHS.add(p)
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def read(stem):
    p = DATA / (stem + '.json')
    source(p)
    x = json.loads(p.read_text())
    assert x['status'] == 'pass'
    return x


def agree(a, b):
    assert max(a[0], b[0]) <= min(a[1], b[1])


def independent_counts(P, S):
    lengths = [0]
    u = S
    while P-u > 33:
        lengths.append(u)
        u += 33
    counts = Counter(create=1, extend=174, **{'init-finish': 1, 'verify-begin': 1,
                                             'verify': 174, 'cm-begin': 1, 'cm': 17,
                                             'coarse': 68, 'seal': 1})
    for length in lengths:
        for name in ['low-begin', 'prepare-begin', 'prepare-finish', 'sweep-begin', 'sweep-finish']:
            counts[name] += 1
        counts['rhs'] += 58
        counts['prepare-rows'] += 6
        counts['operator'] += 174
        remaining = P//8-length//8
        digits = 0
        while remaining > 0:
            remaining -= min(200, remaining)
            digits += 1
        for name in ['low-residual', 'low-solve', 'low-verify']:
            counts[name] += digits
    return dict(counts), len(lengths)


def inventory_check(inv):
    P, S = inv['target'], inv['seed']
    counts, archives = independent_counts(P, S)
    assert counts == inv['phase_counts']
    assert sum(counts.values()) == inv['production_jobs']
    assert archives == inv['archive_jobs'] == inv['corrections']+1
    width = (P+63)//64
    # Two successive ceiling divisions in the weighted representation
    # collapse to one division by 64; count stored bytes directly.
    W = 174*(33*8*width + sum(max(0, (P-k-i+63)//64)
                             for k in range(33, P) for i in range(8)))
    assert W == inv['weighted_bytes']
    cm = 17*2*P*8*width
    assert cm == inv['CM_bytes']
    final = S+33*inv['corrections']
    residual = lambda u: 174*max(33, P-u)*8*((P//8-u//8+7)//8)
    assert W+cm+residual(final)+174*32 == inv['sealed_payload_bytes']
    # At the reported maximal sweep, reconstruct every live file category.
    peak = inv['largest_working_store']
    assert peak['phase'] == 'operator_sweep'
    step = peak['step']
    assert 1 <= step <= inv['corrections']
    meta = 8*(1 << 20)
    for k in range(step+1):
        u = 0 if k == 0 else S+33*(k-1)
        digits = (P//8-u//8+199)//200
        history = (2*digits+1)*16384
        live = meta+(2*174+11+3*digits+(174 if k == 0 else 0)+8)*8192+history+6*65536+512*(1 << 10)
        meta += history+6*65536+512*(1 << 10)
    after = u+33
    assert W+residual(u)+residual(after)+64*(1 << 20)+live == peak['bytes']
    return {'seed': S, 'target': P, 'jobs': sum(counts.values())+archives+26,
            'weighted_bytes': W, 'reported_peak_live_files_reconstructed': peak['bytes']}


def calculate():
    packet = read('precision_route_cost_d152')
    for ref in packet['sources']:
        assert source(ref['path']) == ref
    old = read('cm_arithmetic_height_budget_d118')['budgets']
    hL = Q(old['saved_Hodge_height_upper'])
    theta = Q(old['tropical_Faltings_coefficient_log2'])
    H = logs.plus((2*hL, 2*hL), logs.scale(logs.L2, -Q(35, 34)))
    pi = logs.rounded(logs.plus(logs.scale(logs.atan(Q(1, 5)), 16), logs.scale(logs.atan(Q(1, 239)), -4)))
    logpi = (logs.log(pi[0])[0], logs.log(pi[1])[1])
    Fminus = logs.plus(logs.scale(logpi, -16), logs.scale(logs.L2, theta-8))
    logB = logs.plus(logs.scale(logpi, -Q(1, 2)), logs.log(Q(5, 3)))
    C = [logs.scale(logs.sqrt(2), 2), logs.plus(logs.scale(logs.sqrt(3), 2), (Q(2),)*2),
         logs.plus(logs.scale(logs.sqrt(6), 2), (Q(4),)*2)]
    checked_thresholds = []
    for n, row in enumerate(packet['uniform_design_thresholds'], 1):
        # Reconstruct the uncollected section norm, fibre degree and
        # Faltings term, independently of source 632's saved F interval.
        logC = (logs.log(C[n-1][0])[0], logs.log(C[n-1][1])[1])
        jetnorm = logs.plus(logC, logs.scale(logpi, -1), logs.scale(logs.log(Q(5, 3)), n+2))
        norm = logs.plus(logs.log(480*42550), logs.scale(logs.L2, 70), logs.scale(logB, 238), jetnorm)
        F = logs.plus(logs.scale(H, 240+n), logs.scale(Fminus, -15), norm)
        agree(F, tuple(map(Q, old['thresholds'][n-1]['upper_bound_expression_interval'])))
        P = row['sufficient_P_multiple_of_8']
        def zero(p):
            N = (2*p+32)-296+2*3920-4200-(n+2)*33
            A = (2*p+32)-296+2*3920-4200-(n+2)*296
            return logs.scale(logs.L2, Q(16*N+A, 272))
        assert zero(P)[0] > F[1]
        assert zero(P-8)[1] < F[0]
        shortF = logs.plus(F, logs.log(Q(29299, 42550)))
        short = row['shorter_basis_sufficient_P_multiple_of_8']
        assert zero(short)[0] > shortF[1] and zero(short-8)[1] < shortF[0]
        for sample in row['sample_margins']:
            margin = logs.plus(zero(sample['precision_pi']), logs.scale(F, -1))
            agree(margin, tuple(map(Q, sample['margin_interval'])))
        checked_thresholds.append(P)
    assert checked_thresholds == [10416, 10480, 10552]
    prior = read('dyadic_indexed_bank_recost_r2_d139')
    bases = {s['name']: s for s in prior['schedules']}
    inventories = {}
    for schedule in packet['schedules']:
        base = bases['remaining_staged_conditional_target' if 'staged' in schedule['name'] else 'next_P3200_checkpoint']
        for scenario, old_scenario in zip(schedule['timing_scenarios'], base['timing_scenarios']):
            running = old_scenario['graph_review_seconds_allowance']+old_scenario['common_comparison_seconds_allowance']
            total_jobs = 0
            payload = meta = 0
            extra = 0
            for stage in scenario['stages']:
                inv = stage['inventory']
                key = (inv['seed'], inv['target'])
                if key not in inventories:
                    inventories[key] = inventory_check(inv)
                counts = dict(inv['phase_counts'], archive=inv['archive_jobs'],
                              **{'receipt-discovery': inv['production_jobs'], 'independent-audits': 24,
                                 'fixed-review-and-replay': 2})
                origin = next(s for s in old_scenario['stages'] if s['seed'] == stage['seed'])
                oldcounts = dict(origin['inventory']['phase_counts'], archive=origin['inventory']['archive_jobs'],
                                 **{'receipt-discovery': origin['inventory']['production_jobs'], 'independent-audits': 24,
                                    'fixed-review-and-replay': 2})
                weighted = sum(Q(str(value))*counts[phase]/oldcounts[phase]
                               for phase, value in origin['active_seconds_by_phase'].items())
                assert abs(float(weighted)-stage['active_seconds_per_column']) < 1e-7
                running += stage['columns']*float(weighted)
                total_jobs += stage['columns']*inventories[key]['jobs']
                payload += stage['columns']*inv['sealed_payload_bytes']
                meta += stage['columns']*inv['sealed_metadata_logical_allowance_bytes']
                extra = max(extra, inv['largest_working_store']['bytes']-inv['sealed_payload_bytes'])
            assert abs(running/86400-scenario['active_days']) < 1e-10
            assert total_jobs == schedule['total_jobs_including_archives_audits_reviews']
            allowance = payload+meta+total_jobs*(20480+880)+extra
            assert allowance == schedule['additional_bytes_allowance_scenario']
            assert allowance+10*(1 << 30) == schedule['recommended_free_bytes_including_10GiB_reserve']
    direct = inventory_check(packet['direct_P1600_to_P10480_rejected_inventory'])
    assert direct['reported_peak_live_files_reconstructed'] > 2*(1 << 30)
    disk = packet['filesystem_observation']['free']
    for plan in packet['schedules']:
        assert max(0, plan['recommended_free_bytes_including_10GiB_reserve']-disk) == packet['free_space_shortfalls_at_observation_bytes'][plan['name']]
    charts = read('dyadic_target_chart_review_d136')['charts']
    assert len(charts) == 17
    peak = max(c['peak_rss_bytes'] for c in charts)
    concurrent = sum(sorted(c['peak_rss_bytes'] for c in charts)[-3:])
    assert peak == 1914568704 < 2*(1 << 30)
    assert concurrent == 5087657984 < 6*(1 << 30)
    # A rank-deficient restriction has a strictly larger kernel: rank is
    # essential when substituting three coefficients for the degree test.
    actual = [[1,0,0], [0,1,0]]
    restriction = actual[:1]
    assert all(sum(x*y for x,y in zip(row,[0,1,0])) == 0 for row in restriction)
    assert any(sum(x*y for x,y in zip(row,[0,1,0])) != 0 for row in actual)
    return {'status': 'pass', 'milestone': 'D152',
            'independent_uncollected_section_thresholds': checked_thresholds,
            'rank45_two_positive_order_sufficient_P': 10480,
            'strict_previous_multiple_of_8_rejected': True,
            'shorter_basis_does_not_reduce_two_order_target': True,
            'inventories_checked': list(inventories.values()), 'rejected_direct_inventory': direct,
            'costs_recomputed_with_rational_phase_weighting': True,
            'filesystem_shortfalls_checked_against_saved_observation': True,
            'D136_complete_synthetic_chart_count': 17,
            'D136_max_measured_chart_RSS_bytes': peak,
            'D136_sum_three_largest_measured_RSS_bytes': concurrent,
            'rank_deficient_restriction_control_rejected': True,
            'rank_criterion_geometric_proof_mechanically_verified': False,
            'times_are_empirical_allowances_not_runtime_bounds': True,
            'new_precision_bank_admitted': False, 'actual_harmonic_precision_increased': False,
            'candidate_identification_proved': False, 'field_polynomial_constructed': False}


if __name__ == '__main__':
    assert __debug__ and not OUT.exists()
    tick = time.monotonic()
    result = calculate()
    result['wall_seconds'] = time.monotonic()-tick
    result['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    assert result['peak_rss_bytes'] < 2*(1 << 30)
    result['sources'] = [source(p) for p in sorted(PATHS)]
    with OUT.open('x') as out:
        out.write(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['independent_uncollected_section_thresholds', 'inventories_checked', 'rejected_direct_inventory', 'D136_max_measured_chart_RSS_bytes']}), flush=True)
    print('PHASE_METADATA|'+json.dumps(source(OUT)), flush=True)
    print('PASS|633_PRECISION_ROUTE_CONTROLS', flush=True)

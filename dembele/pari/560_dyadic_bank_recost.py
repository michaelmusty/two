"""D135: empirical bank schedules from the completed D133 receipts.

This is a planning calculation, not a harmonic refinement or launch admission.
It uses no production arithmetic and never changes a frozen input. Projected
times and filesystem allocation are scenarios, not guaranteed bounds or ETAs.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import heapq
import json
import math
from pathlib import Path
import resource
import shutil
import statistics
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
PRIOR = 'arithmetic_cover_criterion_review_d134'
BASE = 'dyadic_staged_P6400_col00_d133'
N, FINAL, CAP = 174, 10552, 2 * (1 << 30)
PATHS = {Path(__file__)}
KNOWN = {}


def digest(path):
    path = Path(path).resolve()
    h = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            h.update(raw)
    return {'path': str(path), 'sha256': h.hexdigest()}


def read(stem, inherited=True):
    path = DATA / (stem + '.json')
    raw = path.read_bytes()
    if inherited:
        assert KNOWN[str(path)] == hashlib.sha256(raw).hexdigest(), stem
    PATHS.add(path)
    value = json.loads(raw)
    assert value['status'] == 'pass', stem
    return value


def bound_read(record):
    raw = Path(record['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == record['sha256']
    assert KNOWN[record['path']] == record['sha256']
    value = json.loads(raw)
    assert value['status'] == 'pass'
    return value


def interpolate(points, x):
    """Linear interpolation with a nonzero smallest-job floor, no extrapolation."""
    points = sorted(points)
    if x <= points[0][0]:
        return points[0][1]
    assert x <= points[-1][0], (x, points[-1])
    for (a, va), (b, vb) in zip(points, points[1:]):
        if a <= x <= b:
            return va + (vb - va) * (x - a) / (b - a)
    return points[-1][1]


def pool_seconds(durations, workers=3):
    """Deterministic queue simulation with the coordinator's group barriers."""
    heap = [0.0] * workers
    for seconds in durations:
        heapq.heappush(heap, heapq.heappop(heap) + seconds)
    return max(heap)


@lru_cache(None)
def weighted_bytes(P):
    return N * sum((max(0, (P - k - i + 7) // 8) + 7) // 8
                   if k > 32 else (P // 8 + 7) // 8
                   for k in range(P) for i in range(8))


def inventory(P, S):
    """Independent integer transcription of the D132 live-file inventory.

    Unlike the historical admission function, return rejected schedules too.
    External records and sealed retention are separate from the store cap.
    """
    assert 400 <= S < P <= FINAL and S % 8 == P % 8 == 0
    W, K, reserve = weighted_bytes(P), P // 8, 64 * (1 << 20)
    row = W // N
    residual = lambda u: N * max(33, P - u) * 8 * ((K - u // 8 + 7) // 8)
    low = lambda bits: N * 32 * 8 * ((bits + 7) // 8)
    meta = 8 * (1 << 20)
    largest = {'phase': 'initial_row_pool', 'step': 0,
               'bytes': W + N + reserve + meta + N * 8192}
    steps = (P - S - 1) // 33
    phase_counts = Counter({'create': 1, 'extend': N, 'init-finish': 1,
                            'verify-begin': 1, 'verify': N, 'cm-begin': 1,
                            'cm': 17, 'coarse': 68, 'seal': 1})
    def consider(phase, step, payload, metadata):
        nonlocal largest
        total = payload + reserve + metadata
        if total > largest['bytes']:
            largest = {'phase': phase, 'step': step, 'bytes': total}
    for step in range(steps + 1):
        u = 0 if step == 0 else S + 33 * (step - 1)
        bits = K - u // 8
        digits = list(range(200, bits, 200)) + [bits]
        oldR = N if step == 0 else residual(u)
        # D132 deliberately budgets one-state RHS jobs, larger than production's
        # three-state chunks. This is a conservative *logical* metadata budget.
        jobs = 2 * N + 11 + 3 * len(digits) + (N if step == 0 else 0)
        history = (2 * len(digits) + 1) * 16384
        live_meta = meta + (jobs + 8) * 8192 + history + 6 * 65536 + 512 * (1 << 10)
        old = 0
        for new in digits:
            consider('low_residual_solve_verify', step,
                     W + oldR + low(bits) + low(old) + low(new-old) + low(new), live_meta)
            old = new
        consider('journal_prepare', step, W + oldR + 2 * low(bits) + 2 * row + 2 * (oldR // N), live_meta)
        after = S if step == 0 else u + 33
        consider('operator_sweep', step, W + oldR + residual(after), live_meta)
        meta += history + 6 * 65536 + 512 * (1 << 10)
        for phase in ('low-begin', 'prepare-begin', 'prepare-finish', 'sweep-begin', 'sweep-finish'):
            phase_counts[phase] += 1
        phase_counts['rhs'] += N // 3
        phase_counts['prepare-rows'] += N // 29
        phase_counts['operator'] += N
        for phase in ('low-residual', 'low-solve', 'low-verify'):
            phase_counts[phase] += len(digits)
    cm = 17 * 2 * P * 8 * ((K + 7) // 8)
    final_meta = meta + (N + 17 + 68 + 10) * 8192 + 2 * 65536
    after = S + 33 * steps
    sealed_payload = W + cm + residual(after) + N * 32
    consider('weighted_verification_CM_publication', steps, sealed_payload, final_meta)
    return {'seed': S, 'target': P, 'corrections': steps,
            'production_jobs': sum(phase_counts.values()), 'phase_counts': dict(phase_counts),
            'archive_jobs': steps + 1, 'independent_audit_jobs_allowance': 24,
            'review_jobs_allowance': 2, 'largest_working_store': largest,
            'fits_2GiB_store_cap': largest['bytes'] < CAP,
            'weighted_bytes': W, 'CM_bytes': cm, 'sealed_payload_bytes': sealed_payload,
            'sealed_metadata_logical_allowance_bytes': final_meta}


def measure():
    actual = read(BASE + '_completed')
    assert actual['completed_jobs'] == 24456 and len(actual['metadata_archives']) == 97
    by_phase, by_step, lows = defaultdict(list), defaultdict(list), defaultdict(list)
    wrapper_overheads, phase_stats = [], {}
    groups = []
    last_group = None
    def add_group(key, duration, serial=False):
        nonlocal last_group
        if serial or last_group != key:
            groups.append([])
        groups[-1].append(duration)
        last_group = None if serial else key
    for row in actual['jobs']:
        meta, receipt = bound_read(row['metadata']), bound_read(row['receipt'])
        assert receipt['exit_code'] == 0 and receipt['timeout_seconds'] == 180
        assert receipt['timeout_terminates_process_group']
        assert receipt['wall_seconds'] == row['seconds']
        q, c = meta['request'], meta['certificates']
        phase, step, seconds = q['phase'], q['step'], row['seconds']
        assert q['key'] == row['key']
        assert meta['peak_rss_bytes'] == row['peak_rss_bytes'] <= CAP
        by_phase[phase].append(seconds)
        if step is not None:
            by_step[phase, step].append(seconds)
        if not row['reused_receipt']:
            wrapper_overheads.append(max(0, row['coordinator_interval'][1] - row['coordinator_interval'][0] - seconds))
        if phase.startswith('low-') and phase != 'low-begin':
            old = c.get('old_bits', 0)
            new = c.get('new_bits', c.get('bits'))
            if phase == 'low-solve':
                x = c['factor_bits']
            else:
                x = new
            lows[phase, bool(q['digit'])].append((x, seconds))
        add_group((phase, step), seconds, phase == 'prepare-rows')
    overhead = statistics.median(wrapper_overheads)
    archives = [bound_read(r['receipt'])['wall_seconds'] for r in actual['metadata_archives']]
    audit = read('dyadic_precision6400_audit_plan_d133_completed')
    audit_seconds = [bound_read(r['receipt'])['wall_seconds'] for r in audit['jobs']]
    completion = read('dyadic_precision6400_completion_d133', inherited=False)
    assert KNOWN[completion['fixed_review']['path']] == completion['fixed_review']['sha256']
    review_seconds = []
    for record in completion['review_receipts']:
        # A review cannot include its own later wrapper receipt. Bind these
        # through the completion record and verify their log/driver directly.
        assert digest(record['path']) == record
        receipt = read(Path(record['path']).stem, inherited=False)
        assert receipt['exit_code'] == 0 and receipt['timeout_seconds'] == 180
        assert receipt['timeout_terminates_process_group']
        for key in ('driver', 'log'):
            assert digest(receipt[key]['path']) == receipt[key]
            PATHS.add(Path(receipt[key]['path']))
        assert KNOWN[receipt['driver']['path']] == receipt['driver']['sha256']
        review_seconds.append(receipt['wall_seconds'])
    for phase, values in by_phase.items():
        phase_stats[phase] = {'jobs': len(values), 'seconds': sum(values),
                              'maximum_seconds': max(values), 'mean_seconds': statistics.mean(values)}
    # Target digit costs already measured through the same staged driver.
    for phase in ('low-residual', 'low-solve', 'low-verify'):
        for digit in range(7):
            stem = f'dyadic_staged_low1319_d132_{phase.replace("-", "_")}_000_{digit:02d}'
            meta = read(stem)
            receipt = read(stem + '_attempt01.job')
            c = meta['certificates']
            new = c.get('new_bits', c.get('bits'))
            x = c['factor_bits'] if phase == 'low-solve' else new
            # For solve at >800 bits, retain its separate publication-size cost
            # as an upper anchor; the factor width itself is still at most 200.
            lows[phase, bool(digit)].append((x, receipt['wall_seconds']))
    compact_lows = {}
    for key, points in lows.items():
        bucket = defaultdict(list)
        for x, seconds in points:
            bucket[x].append(seconds)
        compact_lows[key] = [(x, statistics.median(v)) for x, v in sorted(bucket.items())]
    profiles = {}
    for phase in ('operator', 'rhs'):
        profiles[phase] = [(6400 - (3200 + 33 * (step - 1)), sum(by_step[phase, step]))
                           for step in range(1, 97)]
    summaries = {'phase_timings': phase_stats, 'archive_seconds': sum(archives),
                 'audit_worker_seconds': sum(audit_seconds), 'review_seconds': sum(review_seconds),
                 'total_worker_seconds_with_reviews': sum(sum(v) for v in by_phase.values()) + sum(archives) + sum(audit_seconds) + sum(review_seconds),
                 'median_observed_per_job_coordinator_overhead_seconds': overhead,
                 'reconstructed_complete_stage_three_worker_seconds': sum(pool_seconds([v + overhead for v in group]) for group in groups) + sum(archives) + sum(review_seconds) + audit['wall_seconds'],
                 'resumed_coordinator_monotonic_seconds': actual['wall_seconds'],
                 'resumed_seconds_exclude_earlier_execution_and_are_not_calendar_elapsed': True,
                 'passing_jobs_including_reviews': 24579,
                 'max_arithmetic_RSS_bytes': actual['max_single_job_peak_rss_bytes']}
    return by_phase, by_step, compact_lows, profiles, summaries, statistics.mean(archives), audit_seconds, review_seconds, overhead


def allocation():
    """Observe logical and allocated bytes; sparse/reserved bytes stay distinct."""
    groups = {}
    for label, paths in [('external', DATA.glob(BASE + '*')),
                         ('sealed_store', (DATA / 'dyadic_rowjournal_P6400_col00_d132').rglob('*'))]:
        counters = Counter()
        for path in paths:
            if path.is_file():
                st = path.stat()
                counters['files'] += 1
                counters['logical_bytes'] += st.st_size
                counters['allocated_bytes'] += st.st_blocks * 512
        groups[label] = dict(counters)
    groups['observed_utc'] = datetime.now(timezone.utc).isoformat()
    groups['filesystem'] = shutil.disk_usage(ROOT)._asdict()
    return groups


def main():
    global KNOWN
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = DATA / (args.output + '.json')
    assert not out.exists()
    tick = time.monotonic()
    prior = read(PRIOR, inherited=False)
    KNOWN = {r['path']: r['sha256'] for r in prior['sources']}
    assert len(KNOWN) == 93912
    d134 = read('arithmetic_cover_criterion_completion_d134', inherited=False)
    assert d134['fixed_review'] == digest(DATA / (PRIOR + '.json'))
    for name in ('553_dyadic_staged_archiving_coordinator.py', '554_dyadic_resumable_staged_production.py',
                 '552_dyadic_staged_target_controls.py', '539_dyadic_target_schedule_budget.py'):
        p = ROOT / 'dembele/pari' / name
        assert KNOWN[str(p)] == digest(p)['sha256']
        PATHS.add(p)
    by_phase, by_step, low, profiles, measured, archive_mean, audits, reviews, overhead = measure()
    observed = allocation()
    old_inv = read('dyadic_staged_lifetime_inventory_d132')['certificates']['schedules']
    for row in old_inv:
        inv = inventory(row['precision_pi'], row['seed_precision_pi'])
        assert inv['largest_working_store']['bytes'] == row['maximum_bound']['total_bytes']
        assert inv['weighted_bytes'] == row['weighted_bytes'] and inv['CM_bytes'] == row['CM_bytes']
    assert inventory(6400, 3200)['production_jobs'] == 24456
    map_points = defaultdict(list)
    target_rss = []
    for path in sorted(DATA.glob('dyadic_target_*_d130.json')):
        packet = json.loads(path.read_text())
        c = packet.get('certificates', {})
        if c.get('backend') == 'GMP' and c.get('state_or_CM_index') == 83 and c.get('mode') in ('correction', 'correction-rhs'):
            packet = read(path.stem)
            map_points[c['mode']].append((c['input_moment_count'], c['prepare_seconds'] + c['apply_seconds']))
        if c.get('mode') == 'cm' and c.get('backend') == 'GMP':
            packet = read(path.stem)
            target_rss.append({'input': path.name, 'peak_rss_bytes': packet['peak_rss_bytes']})
    frame = read('dyadic_target_synthetic_frame_d130')['wall_seconds']
    quad = max(read(f'dyadic_target_synthetic_quadrics_c{c:02d}_d130')['wall_seconds'] for c in (0, 8, 16))
    quad_audit = max(read(f'dyadic_target_audit_quadrics_c{c:02d}_d130')['wall_seconds'] for c in (0, 8, 16))
    common_tail = frame + 17 * (quad + quad_audit)
    external_unit = observed['external']['allocated_bytes'] / (24456 + 97)
    store_metadata_actual = observed['sealed_store']['allocated_bytes'] - inventory(6400, 3200)['sealed_payload_bytes']
    metadata_scale = store_metadata_actual / inventory(6400, 3200)['sealed_metadata_logical_allowance_bytes']
    schedules = {
        'full_bank_staged': [(800, 1600, 14), (1600, 3200, 15), (3200, 6400, 15), (6400, FINAL, 16)],
        'full_bank_skip1600': [(800, 3200, 14), (1600, 3200, 1), (3200, 6400, 15), (6400, FINAL, 16)],
        'full_bank_direct': [(800, FINAL, 14), (1600, FINAL, 1), (6400, FINAL, 1)],
        'full_bank_1600_checkpoint': [(800, 1600, 14)],
        'one_target_column_pilot': [(6400, FINAL, 1)],
    }
    def correction_cost(phase, active):
        if active <= 3200:
            return interpolate(profiles[phase], active)
        # The only saved GMP correction-shape series is sampled state 83.
        # It scales the all-state D133 anchor; it does not bound unseen maps.
        points = map_points['correction' if phase == 'operator' else 'correction-rhs']
        return interpolate(profiles[phase], 3200) * interpolate(points, active) / interpolate(points, 3200)

    def stage(S, P, exponent, multiplier):
        inv = inventory(P, S)
        parts, wall_parts = Counter(), Counter()
        count_jobs = 0
        def add(phase, seconds, jobs, serial=False):
            nonlocal count_jobs
            # Mean-job queue scheduling, retaining every serial dependency.
            seconds *= multiplier
            count_jobs += jobs
            duration = seconds + jobs * overhead
            parts[phase] += duration
            wall_parts[phase] += duration if serial else duration * math.ceil(jobs / 3) / jobs
        full_scale = (P / 6400) ** exponent
        row_scale = weighted_bytes(P) / weighted_bytes(6400) * (P / 6400) ** (exponent - 2)
        for phase in ('create', 'init-finish', 'verify-begin', 'cm-begin', 'seal'):
            add(phase, sum(by_phase[phase]) * max(1, row_scale), 1, True)
        add('extend', sum(by_phase['extend']) * full_scale * (S / P) / .5, N)
        for step in range(inv['corrections'] + 1):
            u = 0 if step == 0 else S + 33 * (step - 1)
            active, bits = P - u, P // 8 - u // 8
            digits = list(range(200, bits, 200)) + [bits]
            for phase in ('low-begin', 'prepare-begin', 'prepare-finish', 'sweep-begin', 'sweep-finish'):
                add(phase, statistics.mean(by_phase[phase]) * max(1, row_scale), 1, True)
            for phase in ('rhs', 'operator'):
                jobs = N // 3 if phase == 'rhs' else N
                if step == 0:
                    sec = sum(by_step[phase, 0]) * full_scale
                    if phase == 'operator':
                        sec *= ((P-S)/P) / .5
                else:
                    sec = correction_cost(phase, active)
                add(phase, sec, jobs)
            old = 0
            for digit, new in enumerate(digits):
                for phase in ('low-residual', 'low-solve', 'low-verify'):
                    x = new-old if phase == 'low-solve' else new
                    points = low[phase, bool(digit)]
                    add(phase, interpolate(points, x), 1, True)
                old = new
            add('prepare-rows', statistics.mean(by_phase['prepare-rows']) * 6 * row_scale, 6, True)
            add('archive', archive_mean * (1 + 3*len(digits)/(2*N)), 1, True)
        for phase, jobs in [('verify', N), ('cm', 17), ('coarse', 68)]:
            add(phase, sum(by_phase[phase]) * full_scale, jobs)
        add('independent-audits', sum(audits) * max(1, full_scale), 24)
        add('fixed-review-and-replay', sum(reviews), 2, True)
        expected = inv['production_jobs'] + inv['archive_jobs'] + 26
        assert count_jobs == expected, (count_jobs, expected)
        # File-growth review costs are estimated separately at bank scope.
        return {'seed': S, 'target': P, 'jobs_per_column': count_jobs,
                'worker_seconds': sum(parts.values()), 'three_worker_active_seconds': sum(wall_parts.values()),
                'worker_seconds_by_phase': dict(parts), 'active_seconds_by_phase': dict(wall_parts),
                'inventory': inv}

    results = []
    for name, stages in schedules.items():
        storage = Counter()
        total_jobs, failed_stores = 0, []
        details = []
        for S, P, columns in stages:
            inv = inventory(P, S)
            jobs = inv['production_jobs'] + inv['archive_jobs'] + 26
            total_jobs += columns * jobs
            if not inv['fits_2GiB_store_cap']:
                failed_stores.append({'seed': S, 'target': P, 'bytes': inv['largest_working_store']['bytes']})
            storage['payload_bytes'] += columns * inv['sealed_payload_bytes']
            storage['measured_ratio_metadata_bytes'] += math.ceil(columns * inv['sealed_metadata_logical_allowance_bytes'] * metadata_scale)
            storage['logical_metadata_allowance_bytes'] += columns * inv['sealed_metadata_logical_allowance_bytes']
            storage['measured_allocation_external_bytes'] += math.ceil(columns * jobs * external_unit)
            storage['external_20KiB_per_job_allowance_bytes'] += columns * jobs * 20480
            details.append(dict(seed=S, target=P, columns=columns, corrections_per_column=inv['corrections'], jobs_per_column=jobs))
        # Growing cumulative manifests can duplicate catalogue entries at each
        # column checkpoint. Bound the scenario by retaining one complete
        # catalogue per new column-stage; implementation can instead shard it.
        cumulative = len(KNOWN)
        manifest_bytes = 0
        for detail in details:
            for _ in range(detail['columns']):
                cumulative += 3 * detail['jobs_per_column']
                manifest_bytes += cumulative * 220
        storage['cumulative_review_catalogue_allowance_bytes'] = manifest_bytes
        incremental_manifest = (cumulative - len(KNOWN)) * 220
        storage['incremental_review_catalogue_scenario_bytes'] = incremental_manifest
        # Monolithic rehashing repeatedly reads the prior bank. This empirical
        # surcharge scales observed review time with catalogue growth only;
        # it does not include unknown payload-byte/hash-throughput effects.
        review_growth_seconds = manifest_bytes / (93912 * 220) * sum(reviews)
        largest_active_extra = max(max(0, inventory(P,S)['largest_working_store']['bytes'] - inventory(P,S)['sealed_payload_bytes']) for S,P,_ in stages)
        measured_total = storage['payload_bytes'] + storage['measured_ratio_metadata_bytes'] + storage['measured_allocation_external_bytes'] + manifest_bytes + largest_active_extra
        allowance_total = storage['payload_bytes'] + storage['logical_metadata_allowance_bytes'] + storage['external_20KiB_per_job_allowance_bytes'] + manifest_bytes + largest_active_extra
        incremental_measured = measured_total - manifest_bytes + incremental_manifest
        incremental_allowance = allowance_total - manifest_bytes + incremental_manifest
        # 10 GiB is a proposed free-space reserve, not a changed resource cap.
        headroom = 10 * (1 << 30)
        scenarios = []
        for exponent, multiplier in [(2, 1.0), (3, 1.25)]:
            components = [dict(stage(S,P,exponent,multiplier), columns=n) for S,P,n in stages]
            work = sum(x['columns']*x['worker_seconds'] for x in components)
            wall = sum(x['columns']*x['three_worker_active_seconds'] for x in components)
            # Actual full-frame work is not charged to a single-column pilot.
            tail = 0 if name == 'one_target_column_pilot' else common_tail
            work += tail + review_growth_seconds
            wall += tail + review_growth_seconds
            scenarios.append({'full_shape_scaling_exponent': exponent, 'future_job_multiplier': multiplier,
                              'worker_hours': work/3600, 'ideal_three_worker_days': work/(3*86400),
                              'dependency_aware_active_days': wall/86400,
                              'full_frame_and_quadric_worker_seconds_allowance': tail,
                              'cumulative_review_growth_seconds_allowance': review_growth_seconds,
                              'stages': components})
        results.append({'name':name, 'stages':details, 'total_jobs_including_archives_audits_reviews':total_jobs,
                        'approximate_external_record_files':3*total_jobs,
                        'timing_scenarios':scenarios, 'storage':dict(storage),
                        'additional_allocated_bytes_measured_ratio_scenario':measured_total,
                        'additional_bytes_allowance_scenario':allowance_total,
                        'incremental_review_additional_bytes_measured_scenario':incremental_measured,
                        'incremental_review_additional_bytes_allowance_scenario':incremental_allowance,
                        'incremental_reviews_implemented_or_admitted':False,
                        'proposed_free_space_reserve_bytes':headroom,
                        'free_space_shortfall_measured_scenario_bytes':max(0, measured_total+headroom-observed['filesystem']['free']),
                        'free_space_shortfall_allowance_scenario_bytes':max(0, allowance_total+headroom-observed['filesystem']['free']),
                        'incremental_review_shortfall_measured_scenario_bytes':max(0, incremental_measured+headroom-observed['filesystem']['free']),
                        'incremental_review_shortfall_allowance_scenario_bytes':max(0, incremental_allowance+headroom-observed['filesystem']['free']),
                        'store_cap_failures':failed_stores, 'production_launch_admitted':False})
    result = {'status':'pass', 'milestone':'D135', 'kind':'empirical_bank_recost',
              'prior_fixed_review':digest(DATA/(PRIOR+'.json')), 'prior_hash_count':len(KNOWN),
              'certified_seeds':{'0':6400,'1':1600,'2_through_15':800},
              'measured_D133':measured, 'filesystem_observation':observed,
              'target_CM_single_child_RSS_controls':target_rss,
              'largest_observed_target_CM_single_child_RSS_bytes':max(x['peak_rss_bytes'] for x in target_rss),
              'target_CM_integrated_peak_from_quadratic_extrapolation_bytes':math.ceil(measured['max_arithmetic_RSS_bytes']*(FINAL/6400)**2),
              'schedules':results, 'conditional_sufficient_common_precision':FINAL,
              'model_is_empirical_not_runtime_or_allocation_bound':True,
              'assumptions':[
                  'One column-stage at a time; at most three jobs run within each parallel phase, with all serial barriers retained.',
                  'Correction jobs at active length <=3200 interpolate all-state D133 end-to-end phase sums; the smallest observed job supplies a nonzero floor.',
                  'Larger correction bands scale the D133 anchor using the sole saved GMP correction-shape series, sampled state83. No unseen-map bound is implied.',
                  'Seed/full/CM/coarse shapes use quadratic or cubic size scaling; the second scenario also adds25percent to future job durations.',
                  'Low-digit phases interpolate D133 and the D132 seven-digit control; no larger factor, multi-column factor sharing or concurrency gain is assumed.',
                  'Preparation follows weighted payload size, with an extra size factor in the cubic scenario. Per-job coordinator overhead is measured from newly run D133 jobs.',
                  'Phase queue makespans use mean durations and barrier counts; sustained contention, sleep and power management are unmeasured.',
                  'I/O already present in D133 end-to-end job times is not added a second time.',
                  'All new intermediate stages and every old frozen artifact are retained; no deletions, compression or off-host archive is assumed.',
                  'Allocated-file estimates use actual D133 st_blocks, plus a20KiB/job alternative; metadata ceilings are logical sizes and are not filesystem allocation bounds.',
                  'Cumulative catalogues assume220bytes per entry and three external records per job; sharded reviews could reduce duplication but are not implemented.',
                  'The10GiB free-space reserve is a planning recommendation, not an automatic reservation or changed cap.',
                  'Final frame/quadric timings are synthetic target-size controls. Actual arithmetic CM inputs, exact-zero checks and admission remain required.'
              ],
              'remaining_execution_gates':[
                  'Publish reviewed seed/CM metadata adapters for the sealed weighted stage; current seal metadata is a state seed but lacks the CM_reference interface.',
                  'Measure complete target CM chart jobs within2GiB RSS; smaller single-child controls do not admit a two-child chart.',
                  'Shard enlarged finite reviews to retain the180second per-process cap; scaling the current monolithic catalogue is not admitted.',
                  'Resolve bank retention against measured free disk and preserve every frozen file.',
                  'Create reviewed configurations, global worker coordination, per-stage audits and final full-frame exactness checks before admitting a bank.'
              ],
              'actual_harmonic_precision_increased':False,'candidate_identification_proved':False,
              'field_polynomial_constructed':False,'full_bank_launch_admitted':False,
              'resource_caps_changed':False,
              'wall_seconds':time.monotonic()-tick,
              'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
              'sources':[digest(p) for p in sorted(PATHS)]}
    assert result['peak_rss_bytes'] <= CAP
    with out.open('x') as f:
        f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(digest(out)),flush=True)
    print('PASS|560_DYADIC_BANK_RECOST',flush=True)


if __name__ == '__main__':
    main()

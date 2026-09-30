"""D130 reproducible empirical schedule model and exact resource obstructions.

Timings are scenarios interpolated from bounded controls, not runtime bounds
or permission to launch production. Every certificate phase is accounted for
either by a stated model or an explicit unresolved cost/admission gate.
"""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
PATHS = {Path(__file__)}
PFINAL = 10552


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    sha = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            sha.update(raw)
    return {'path': str(path), 'sha256': sha.hexdigest()}


@lru_cache(maxsize=None)
def read(stem):
    path = DATA / (stem + '.json')
    PATHS.add(path)
    packet = json.loads(path.read_text())
    assert packet['status'] == 'pass'
    return packet


def interpolate(points, x):
    """Piecewise linear scenario, including an explicit zero-size anchor."""
    points = sorted(points)
    assert points[0][0] <= x <= points[-1][0], (points, x)
    for (a, va), (b, vb) in zip(points, points[1:]):
        if a <= x <= b:
            return va + (vb - va) * (x - a) / (b - a)
    return points[-1][1]


def maps():
    rows = []
    for path in sorted(DATA.glob('*d130.json')):
        packet = json.loads(path.read_text())
        c = packet.get('certificates', {})
        if 'prepare_seconds' in c:
            assert packet['status'] == 'pass'
            PATHS.add(path)
            rows.append(c)
    assert len(rows) == 74
    return rows


MAPS = maps()


def cost(mode, P, active=None, sample=0, backend='ADAPTIVE', seed=None):
    if mode.startswith('correction'):
        points = [(0, 0)]
        for r in MAPS:
            if r['mode'] == mode and r['state_or_CM_index'] == sample and r['backend'] == backend:
                points.append((r['input_moment_count'], r['prepare_seconds'] + r['apply_seconds']))
        # Repeated sizes are absent in the actual controls used here.
        assert len({a for a, _ in points}) == len(points)
        return interpolate(points, active)
    if mode == 'extend':
        dense = [r for r in MAPS if r['mode'] == mode and r['state_or_CM_index'] == 0
                 and r['branch'] == 0 and r['backend'] == 'ADAPTIVE']
        points = [(0, 0)] + [(r['seed_precision_pi'], r['prepare_seconds'] + r['apply_seconds']) for r in dense]
        points.append((PFINAL, cost('full', PFINAL, sample=0)))
        value = interpolate(points, seed * PFINAL / P) * (P / PFINAL) ** 2
        if sample == 83:
            actual = [r for r in MAPS if r['mode'] == 'extend' and r['state_or_CM_index'] == 83
                      and r['backend'] == 'ADAPTIVE'][0]
            value *= (actual['prepare_seconds'] + actual['apply_seconds']) / interpolate(points, 3200)
        return value
    r = [r for r in MAPS if r['mode'] == mode and r['working_precision_pi'] == PFINAL
         and r['state_or_CM_index'] == sample and r['branch'] == 0 and r['backend'] == backend]
    assert len(r) == 1, (mode, sample, backend)
    return (r[0]['prepare_seconds'] + r[0]['apply_seconds']) * (P / PFINAL) ** 2


def low_tables():
    stages = (200, 400, 600, 800, 1000, 1200, 1319)
    table = {}
    for bits in stages:
        solve = read(f'dyadic_target_low_c01_bits{bits}_d130_solve')['certificates']
        verify = read(f'dyadic_target_low_c01_bits{bits}_d130_verify')['certificates']
        t = verify['timings'][0]
        table[bits] = (t['coefficient_block_seconds'], t['multiply_seconds'])
        assert solve['factor_blocks_decoded'] == 1226
    factor = [(1, read('dyadic_target_low_c01_bits200_d130_solve')['certificates']['factor_solve_seconds_including_decode'])]
    for columns in (2, 16):
        factor.append((columns, read(f'dyadic_factor_stream_b200_n{columns}_d126')['certificates']['solve_seconds_including_decode']))
    profiles = {}
    for columns in (1, 16):
        ts = [read(f'dyadic_target_low_profile_c{columns:02d}_g{a:03d}_{a+55:03d}_d130')['certificates']['timings'][0]
              for a in (0, 55, 110)]
        profiles[columns] = {k: sum(t[k] for t in ts) for k in ('coefficient_block_seconds', 'multiply_seconds')}
    return table, factor, profiles


LOW, FACTOR, PROFILES = low_tables()


def low_operator(bits, columns):
    bits = max(200, bits)  # Charge the measured 200-bit cost for smaller solves.
    make = interpolate([(a, b[0]) for a, b in LOW.items()], bits)
    multiply = interpolate([(a, b[1]) for a, b in LOW.items()], bits)
    ratio = PROFILES[16]['multiply_seconds'] / PROFILES[1]['multiply_seconds']
    return make + multiply * (1 + (columns - 1) * (ratio - 1) / 15)


def low_solve(bits, columns):
    ends = list(range(200, bits, 200)) + [bits]
    total = 0
    for i, end in enumerate(ends):
        step = end - (ends[i - 1] if i else 0)
        total += interpolate(FACTOR, columns) + low_operator(step, columns)
        # Independent phase rebuilding every original low equation after
        # each digit. A later digit also forms an exactly divisible residual.
        total += (2 if i else 1) * low_operator(end, columns)
    return total, len(ends), 3 * len(ends) - 1


@lru_cache(maxsize=None)
def weighted(P):
    return 174 * sum((max(0, (P - i if k <= 32 else P - k - i) + 7) // 8 + 7) // 8
                     for k in range(P) for i in range(8))


def schedule(name, batch, sample):
    if name == 'direct':
        stages = [(800, 10552, 14), (1600, 10552, 1), (3200, 10552, 1)]
    else:
        stages = [(800, 1600, 14), (1600, 3200, 15), (3200, 6400, 16), (6400, 10552, 16)]
    parts = Counter()
    correction_columns = factor_digits = child_actions = model_jobs = io_bytes = 0
    details = []
    row = read('dyadic_compact_target_row_d130')['certificates']
    serial_pass = 174 * (row['serialization_seconds'] + row['read_decode_seconds'] + row['weighted_projection_seconds'])
    for seed, P, columns in stages:
        us = list(range(seed, P - 33, 33))
        assert len(us) == (P - seed - 1) // 33
        groups = [min(batch, columns - i) for i in range(0, columns, batch)]
        parts['seed_extension'] += columns * 348 * cost('extend', P, sample=sample, seed=seed)
        parts['seed_low_rhs'] += columns * 348 * cost('rhs', P, sample=sample)
        parts['seed_original_residual'] += columns * 348 * cost('full', P, sample=sample)
        parts['GMP_reconstruction_and_original_verification'] += columns * 696 * cost('full', P, sample=sample, backend='GMP')
        for n in groups:
            secs, digits, jobs = low_solve(P // 8, n)
            parts['exact_low_factor_lifts_and_all_original_low_checks'] += secs
            factor_digits += digits
            model_jobs += jobs
        child_actions += columns * 348 * 5
        model_jobs += columns * (4 * 174 + math.ceil(174 / 4) + 6)
        for u in us:
            active = P - u
            bits = P // 8 - u // 8
            for mode in ('correction-rhs', 'correction'):
                secs = cost(mode, P, active, sample)
                parts[mode] += columns * 348 * secs
                # Cost-based chunk proposal only; no target worker enforces it.
                chunk = max(1, min(29, int(90 / max(.001, 2 * cost(mode, P, active, 0)))))
                model_jobs += columns * math.ceil(174 / chunk)
            for n in groups:
                secs, digits, jobs = low_solve(bits, n)
                parts['exact_low_factor_lifts_and_all_original_low_checks'] += secs
                factor_digits += digits
                model_jobs += jobs
            child_actions += columns * 696
            model_jobs += columns * 2
            residual = 174 * active * 8 * ((bits + 7) // 8)
            io_bytes += columns * 6 * (weighted(P) + residual)
        correction_columns += columns * len(us)
        # Four serial row-equivalent passes per correction and eight per
        # stage, at quadratic scaled size; a planning allowance, not a bound.
        parts['row_decoding_projection_updates_and_serialization'] += columns * (4 * len(us) + 8) * serial_pass * (P / PFINAL) ** 2
        uniform = 174 * P * 8 * ((P // 8 + 7) // 8)
        io_bytes += columns * 8 * uniform
        details.append({'seed': seed, 'target': P, 'columns': columns, 'corrections_per_column': len(us),
                        'last_residual_lower_pi': seed + 33 * len(us)})
    cm = [r for r in MAPS if r['mode'] == 'cm' and r['backend'] == 'GMP']
    # All production CM maps use the slower sampled composed-map time.
    parts['final_CM_composed_maps'] = 16 * 34 * max(r['prepare_seconds'] + r['apply_seconds'] for r in cm)
    for method in ('direct', 'horner'):
        parts['coarse_CM_' + method] = 16 * 17 * sum(read(f'dyadic_target_coarse_c00_n{n}_{method}_d130')['wall_seconds'] for n in range(4))
    parts['frame'] = read('dyadic_target_synthetic_frame_d130')['wall_seconds']
    parts['all_6188_quadric_enclosures'] = 17 * max(read(f'dyadic_target_synthetic_quadrics_c{ci:02d}_d130')['wall_seconds'] for ci in (0, 8, 16))
    parts['independent_all_quadric_coefficient_recomputations'] = 17 * max(read(f'dyadic_target_audit_quadrics_c{ci:02d}_d130')['wall_seconds'] for ci in (0, 8, 16))
    audit = sum(read('dyadic_target_audit_' + name + '_d130')['wall_seconds'] for name in ('full0', 'full83', 'rhs0', 'extend0', 'correction0', 'cm0'))
    parts['independent_sampled_ordinary_state_and_CM_audits'] = 16 * audit
    parts['final_all_weighted_coordinates_and_old_overlaps'] = 16 * serial_pass * 3
    model_jobs += 16 * (17 + 17 * 4 * 2 + 6 + 6) + 17 * 2 + 1
    # Explicit sensitivity assumptions for receipts/review/startup, not measured
    # throughput of the future coordinator or its enlarged fixed manifest.
    parts['job_startup_receipts_and_fixed_review_allowance'] = model_jobs * .25 + 120
    inventory = read('dyadic_compact_inventory_d130')['certificates']
    io_bytes += 2 * inventory['target_16_column_uniform_plus_CM_bytes']
    total = sum(parts.values())
    return {'schedule': name, 'factor_batch_columns': batch, 'map_sample_state': sample,
            'map_preparations_not_shared_across_columns_in_model': True,
            'stages': details, 'correction_column_steps': correction_columns,
            'factor_digit_solves': factor_digits, 'state_child_map_actions': child_actions,
            'proposed_job_count': model_jobs, 'modeled_process_seconds_by_phase': dict(parts),
            'modeled_process_hours': total / 3600,
            'ideal_three_worker_days_excluding_extra_IO': total / (3 * 86400),
            'single_worker_days_excluding_extra_IO': total / 86400,
            'modeled_logical_checkpoint_and_final_IO_bytes': io_bytes,
            'additional_serial_IO_hours_at_assumed_MBps': {str(rate): io_bytes / (rate * 1000000 * 3600) for rate in (25, 100, 500)},
            'admitted_production_schedule': False}


def census():
    packet = read('dyadic_target_transports_d121')
    mask = (1 << 1319) - 1
    kinds, distinct = Counter(), set()
    for e in packet['transitions']:
        for c in e['children']:
            assert c['normalized_error_pi'] >= PFINAL
            pars = tuple(tuple(int(v) & mask for v in row) for row in c['normalized_center'][:3])
            distinct.add(pars)
            kinds['b_zero' if not any(pars[1]) else 'b_nonzero'] += 1
            kinds['c_zero' if not any(pars[2]) else 'c_nonzero'] += 1
    assert sum(kinds[k] for k in ('b_zero', 'b_nonzero')) == 348
    return {'children': 348, 'distinct_maps_mod_2_to_1319': len(distinct), 'counts_at_this_modulus': dict(kinds),
            'zero_at_finite_precision_not_asserted_exact_global_zero': True}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = DATA / (args.output + '.json')
    assert not out.exists()
    tick = time.monotonic()
    rows = [schedule(s, batch, sample) for s in ('direct', 'staged') for batch in (1, 2, 4, 16) for sample in (83, 0)]
    inv = read('dyadic_compact_inventory_d130')['certificates']
    for layout in inv['layouts']:
        assert weighted(layout['P']) == layout['weighted_bytes']
    result = {'status': 'pass', 'milestone': 'D130', 'phase': 'complete_phase_budget_model',
        'model_is_empirical_not_a_runtime_bound': True, 'scenarios': rows,
        'measured_low_profiles': PROFILES, 'measured_factor_seconds': FACTOR,
        'map_census': census(), 'storage_inventory': inv,
        'phase_coverage': 'All identification certificate phases modeled; unresolved costs/gates below prohibit an unconditional full runtime or admission certificate.',
        'assumptions': [
            'Each of 348 children is assigned the same sampled map cost in a scenario; actual maps vary.',
            'Correction costs are linearly interpolated in active length, with zero-size anchor; finite modulus alignment and data density can change cost.',
            'Non-target full/RHS/extension costs use quadratic precision scaling, not measured complete stages.',
            'Multiple RHS factor times and low residual multiplication are interpolated from 1/2/16-column observations.',
            'Serial row work uses four row-equivalent passes per correction and eight per stage.',
            'Logical checkpoint IO uses six weighted-plus-scaled-residual payload lengths per correction, eight uniform lengths per stage.',
            'IO bandwidths 25/100/500 MB/s are sensitivity assumptions, not sustained measurements; adding all IO separately can double-count observed cached IO.',
            'A quarter second per proposed job and 120 seconds for review are unvalidated scheduling allowances.',
            'Ideal three-worker division omits dependencies, contention and single-worker critical paths; it is not an ETA.'
        ],
        'unresolved_cost_and_admission_gates': [
            'Integrated generation/chunk storage and safe retirement under unchanged 2 GiB scratch cap; uniform target column alone exceeds cap.',
            'Target multi-digit and original-map jobs integrated with row-authentication manifests and resumable independent phases.',
            'Aggregate resident memory, actual concurrent throughput, sustained checkpoint IO, and resource-admitted multi-column reuse.',
            'Full target-map census performance, coordinator/receipt overhead at proposed job counts, complete final manifest/review time.',
            'Marked arithmetic double cover and Y section model; combined genus64/degree51 torsion and global F256 action; polynomial recognition bounds.'
        ],
        'decision': 'Do not launch another actual precision stage with the inherited driver. First redesign the residual/checkpoint algorithm under unchanged caps, and resolve the arithmetic cover interface as a separate mathematical task.',
        'actual_harmonic_precision_increased': False, 'candidate_identification_proved': False,
        'complete_costed_field_construction': False, 'new_resource_limit_authorized': False,
        'wall_seconds': time.monotonic() - tick, 'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'sources': [source(path) for path in sorted(PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print('PHASE_METADATA|' + json.dumps(source(out)), flush=True)
    print(json.dumps([{k: r[k] for k in ('schedule', 'factor_batch_columns', 'map_sample_state', 'correction_column_steps', 'modeled_process_hours', 'ideal_three_worker_days_excluding_extra_IO')} for r in rows]), flush=True)
    print('PASS|539_DYADIC_TARGET_SCHEDULE_BUDGET', flush=True)


if __name__ == '__main__':
    main()

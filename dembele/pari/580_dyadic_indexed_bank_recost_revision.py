"""D139 revised recost with measured per-job floors, not global phase multipliers.

Retains D135's measured higher-precision arithmetic scenarios; replaces its
archive/discovery assumptions and excludes the now completed P1600 stage.
These are planning scenarios, not runtime, allocation or correctness bounds.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import heapq
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import shutil
import statistics
import sys
import time
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
PATHS = {Path(__file__)}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    h = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            h.update(raw)
    return {'path': str(path), 'sha256': h.hexdigest()}


def read(stem):
    p = DATA / (stem + '.json')
    source(p)
    d = json.loads(p.read_text())
    assert d['status'] == 'pass'
    return d


def module(name, filename):
    path = ROOT / 'dembele/pari' / filename
    source(path)
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def pooled(values):
    heap = [0.0] * 3
    for value in values:
        heapq.heappush(heap, heapq.heappop(heap) + value)
    return max(heap)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = DATA / (args.output + '.json')
    assert not out.exists()
    tick = time.monotonic()
    superseded = read('dyadic_indexed_bank_recost_d139')
    source(ROOT / 'dembele/pari/579_dyadic_indexed_bank_recost.py')
    old = read('dyadic_bank_recost_d135')
    prior = read('dyadic_precision1600_review_d138')
    prior_ref = source(DATA / 'dyadic_precision1600_review_d138.json')
    known = {r['path']: r['sha256'] for r in prior['sources']}
    parent = prior['inherited_catalogues'][0]
    assert source(parent['path']) == parent
    known.update({r['path']: r['sha256'] for r in json.loads(Path(parent['path']).read_text())['sources']})
    old_ref = source(DATA / 'dyadic_bank_recost_d135.json')
    assert known[old_ref['path']] == old_ref['sha256']
    look = read('dyadic_receipt_lookup_controls_d139')['certificates']
    archive = read('dyadic_indexed_archive_controls_d139')['certificates']
    archive_seconds = archive['synthetic_stores'][0]['archive']['wall_seconds']
    query_seconds = 2 * max(t for x in look['completed_column_checks'] for t in x['exact_sample_seconds'])
    scan_per_entry = max(x['one_scan_seconds'] / x['directory_entries'] for x in look['completed_column_checks'])
    legacy = next(x for x in old['schedules'] if x['name'] == 'full_bank_staged')
    invmod = module('inventory_d139', '560_dyadic_bank_recost.py')
    coordinator = module('schedule_d139', 'run_d139_indexed_production.py')
    measured, phase_samples, intervals = [], {}, []
    external = Counter()
    prefixes = {f'dyadic_staged_P1600_col{c:02d}_r2_d137': c for c in range(2, 16)}
    with os.scandir(DATA) as entries:
        directory_entries = 0
        for entry in entries:
            directory_entries += 1
            if any(entry.name.startswith(p + '_') for p in prefixes) and entry.is_file():
                st = entry.stat()
                external['files'] += 1
                external['logical_bytes'] += st.st_size
                external['allocated_bytes'] += st.st_blocks * 512
    store_allocations = []
    for prefix, col in prefixes.items():
        completed = read(prefix + '_completed')
        ref = source(DATA / (prefix + '_completed.json'))
        assert known[ref['path']] == ref['sha256']
        cfg = json.loads(Path(completed['config']['path']).read_text())
        assert source(completed['config']['path']) == completed['config']
        groups = list(coordinator.schedule(cfg))
        rows = {r['key']: r for r in completed['jobs']}
        assert len(rows) == 6588 == sum(map(len, groups))
        overhead = statistics.median(max(0, r['coordinator_interval'][1] - r['coordinator_interval'][0] - r['seconds']) for r in rows.values())
        intervals.append(overhead)
        phases = Counter()
        for group in groups:
            for spec in group:
                phases[spec['phase']] += rows[spec['key']]['seconds']
        for phase, seconds in phases.items():
            phase_samples.setdefault(phase, []).append(seconds)
        old_archives = []
        for record in completed['metadata_archives']:
            assert source(record['receipt']['path']) == record['receipt']
            old_archives.append(json.loads(Path(record['receipt']['path']).read_text())['wall_seconds'])
        active = sum(pooled([rows[s['key']]['seconds'] + overhead for s in group]) for group in groups)
        new_archives = len(old_archives) * (archive_seconds + .15 + overhead)
        discovery = len(rows) * query_seconds + 2 * directory_entries * scan_per_entry
        measured.append({'column': col, 'recorded_production_coordinator_seconds': completed['wall_seconds'],
                         'arithmetic_worker_seconds': sum(phases.values()), 'old_archive_seconds': sum(old_archives),
                         'median_wrapper_overhead_seconds': overhead,
                         'reconstructed_groups_without_directory_discovery_seconds': active,
                         'indexed_archive_allowance_seconds': new_archives,
                         'indexed_discovery_allowance_seconds': discovery,
                         'counterfactual_indexed_production_seconds': active + new_archives + discovery,
                         'counterfactual_is_not_a_new_production_measurement': True})
        stats = Counter()
        for path in (DATA / cfg['namespace']).iterdir():
            if path.is_file():
                stat = path.stat()
                stats['files'] += 1
                stats['logical_bytes'] += stat.st_size
                stats['allocated_bytes'] += stat.st_blocks * 512
        store_allocations.append({'column': col, **dict(stats)})
    old_overhead = old['measured_D133']['median_observed_per_job_coordinator_overhead_seconds']
    new_overhead = max(intervals)
    old_1600 = legacy['timing_scenarios'][0]['stages'][0]
    inv1600 = invmod.inventory(1600, 800)
    floors = {phase: statistics.median(values) / inv1600['phase_counts'][phase]
              for phase, values in phase_samples.items()}
    # A small phase includes fixed import/journal costs. Its measured mean is
    # a per-job floor; multiplying a separately measured large-precision
    # phase by the small-stage forecast error would count those costs twice.
    old_storage = legacy['storage']
    old_jobs = legacy['total_jobs_including_archives_audits_reviews']
    external_unit = max(old_storage['measured_allocation_external_bytes'] / old_jobs,
                        external['allocated_bytes'] / (14 * 6613))
    metadata_ratio = max(old_storage['measured_ratio_metadata_bytes'] / old_storage['logical_metadata_allowance_bytes'],
                         max(max(0, s['allocated_bytes'] - inv1600['sealed_payload_bytes']) /
                             inv1600['sealed_metadata_logical_allowance_bytes'] for s in store_allocations))
    done = read('dyadic_precision1600_completion_d138')
    assert done['fixed_review'] == prior_ref
    replay_ref = done['review_receipts'][1]
    assert source(replay_ref['path']) == replay_ref
    replay_seconds = json.loads(Path(replay_ref['path']).read_text())['wall_seconds']
    plans = {'next_P3200_checkpoint': [(1600, 3200, 15)],
             'remaining_staged_conditional_target': [(1600, 3200, 15), (3200, 6400, 15), (6400, 10552, 16)],
             'one_target_column_pilot': [(6400, 10552, 1)]}
    schedules = []
    for name, plan in plans.items():
        jobs = sum(n * (invmod.inventory(P, S)['production_jobs'] + invmod.inventory(P, S)['archive_jobs'] + 26) for S, P, n in plan)
        payload = sum(n * invmod.inventory(P, S)['sealed_payload_bytes'] for S, P, n in plan)
        meta = sum(n * invmod.inventory(P, S)['sealed_metadata_logical_allowance_bytes'] for S, P, n in plan)
        active_extra = max(max(0, invmod.inventory(P, S)['largest_working_store']['bytes'] - invmod.inventory(P, S)['sealed_payload_bytes']) for S, P, n in plan)
        catalogue = 4 * jobs * 220  # Includes receipts, metadata, logs and store references.
        measured_bytes = math.ceil(payload + meta * metadata_ratio + jobs * external_unit + catalogue + active_extra)
        allowance_bytes = payload + meta + jobs * 20480 + catalogue + active_extra
        scenario_rows = []
        for scenario, inherited_scenario in enumerate(legacy['timing_scenarios']):
            details = []
            for S, P, n in plan:
                inherited = next(x for x in inherited_scenario['stages'] if x['seed'] == S and x['target'] == P)
                inv = invmod.inventory(P, S)
                assert inv == inherited['inventory']
                worker, active = {}, {}
                for phase, seconds in inherited['worker_seconds_by_phase'].items():
                    if phase == 'archive':
                        continue
                    count = inv['phase_counts'].get(phase, 24 if phase == 'independent-audits' else 2)
                    correction = count * max(0, new_overhead - old_overhead)
                    empirical_floor = count * (floors.get(phase, 0) + new_overhead)
                    worker[phase] = max(seconds + correction, empirical_floor)
                    ratio = inherited['active_seconds_by_phase'][phase] / seconds
                    active[phase] = worker[phase] * ratio
                # Account conservatively for larger record bodies and seven-digit target sweeps.
                digit_count = math.ceil((P // 8) / 200)
                max_records = 422 + 3 * (digit_count - 1)
                per_archive = (archive_seconds * (P / 1600) * max_records / 422 + .15 + new_overhead) * (1 + scenario)
                worker['archive'] = active['archive'] = inv['archive_jobs'] * per_archive
                future_entries = directory_entries + 3 * jobs
                discovery = inv['production_jobs'] * query_seconds + 2 * future_entries * scan_per_entry
                worker['receipt-discovery'] = active['receipt-discovery'] = discovery * (1 + scenario)
                details.append({'seed': S, 'target': P, 'columns': n, 'inventory': inv,
                                'jobs_per_column': inherited['jobs_per_column'],
                                'worker_seconds_by_phase': worker, 'active_seconds_by_phase': active,
                                'worker_seconds': sum(worker.values()), 'active_seconds': sum(active.values()),
                                'archive_seconds_per_job_scenario': per_archive})
            final_precision = max(P for S, P, n in plan)
            # One graph replay allowance per bank checkpoint; payload growth is
            # charged quadratically as well as catalogue-file count growth.
            review_allowance = replay_seconds * (1 + 3 * jobs / prior['unique_inherited_file_hashes']) * (final_precision / 1600) ** 2 * (1 + .5 * scenario)
            tail = 0 if name == 'one_target_column_pilot' else inherited_scenario['full_frame_and_quadric_worker_seconds_allowance']
            active = sum(x['columns'] * x['active_seconds'] for x in details) + review_allowance + tail
            worker = sum(x['columns'] * x['worker_seconds'] for x in details) + review_allowance + tail
            scenario_rows.append({'scenario': scenario, 'inherited_scaling_exponent': inherited_scenario['full_shape_scaling_exponent'],
                                  'active_hours': active / 3600, 'active_days': active / 86400,
                                  'worker_hours': worker / 3600, 'graph_review_seconds_allowance': review_allowance,
                                  'common_comparison_seconds_allowance': tail, 'stages': details})
        schedules.append({'name': name, 'total_jobs_including_archives_audits_reviews': jobs,
                          'additional_allocated_bytes_measured_ratio_scenario': measured_bytes,
                          'additional_bytes_allowance_scenario': allowance_bytes,
                          'recommended_free_bytes_including_10GiB_reserve': allowance_bytes + 10 * (1 << 30),
                          'storage_components': {'payload_bytes': payload, 'metadata_logical_bytes': meta,
                                                 'incremental_catalogue_allowance_bytes': catalogue,
                                                 'largest_active_extra_bytes': active_extra},
                          'timing_scenarios': scenario_rows})
    result = {'status': 'pass', 'milestone': 'D139', 'prior_fixed_review': prior_ref,
              'current_full_bank_precision_pi': 1600, 'current_column0_precision_pi': 6400,
              'conditional_sufficient_target_precision_pi': 10552,
              'measured_completed_columns': measured, 'observed_external_allocation': dict(external),
              'observed_sealed_store_allocations': store_allocations,
              'archive_422_records_measured_seconds': archive_seconds,
              'measured_P1600_worker_seconds_per_job_floors': floors,
              'superseded_cost_model': source(DATA / 'dyadic_indexed_bank_recost_d139.json'),
              'revision_reason': 'Use measured small-job floors without multiplying already measured large-job costs.',
              'cost_parameters': {'old_wrapper_overhead_seconds': old_overhead,
                                  'new_wrapper_overhead_seconds': new_overhead,
                                  'receipt_query_seconds_allowance': query_seconds,
                                  'directory_scan_seconds_per_entry': scan_per_entry,
                                  'directory_entries': directory_entries,
                                  'external_allocated_bytes_per_job': external_unit,
                                  'store_metadata_allocation_ratio': metadata_ratio,
                                  'D138_transitive_replay_seconds': replay_seconds},
              'schedules': schedules, 'filesystem': shutil.disk_usage(ROOT)._asdict(),
              'observed_utc': datetime.now(timezone.utc).isoformat(),
              'model_is_empirical_not_runtime_or_allocation_bound': True,
              'counterfactuals_are_not_measured_optimized_production_runs': True,
              'remaining_execution_gates': ['User selects the precision scope.',
                  'New stage-specific admission/replay and column-1 CM adapter.',
                  'Independent next-stage audit/review and bounded graph-replay shards.',
                  'First-column checkpoint to validate integrated timing before continuing the chosen bank.'],
              'actual_harmonic_precision_increased': False, 'candidate_identification_proved': False,
              'field_polynomial_constructed': False, 'next_precision_bank_admitted': False,
              'resource_caps_changed': False, 'wall_seconds': time.monotonic() - tick,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
              'sources': [source(p) for p in sorted(PATHS)]}
    assert result['peak_rss_bytes'] < 2 * (1 << 30)
    with out.open('x') as f:
        f.write(json.dumps(result, indent=2) + '\n')
    print('PHASE_METADATA|' + json.dumps(source(out)), flush=True)
    print('PASS|580_DYADIC_INDEXED_BANK_RECOST_REVISION', flush=True)


if __name__ == '__main__':
    main()

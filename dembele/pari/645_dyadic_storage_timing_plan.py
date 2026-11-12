"""D156 retained-storage plan and one higher-stage timing-pilot budget.

Local finite planning only. Existing data are never moved or removed.
Allocation and time figures are scenarios, not guarantees or reservations.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'dyadic_storage_timing_plan_d156.json'
GIB = 1 << 30
PATHS = {Path(__file__)}
CACHE = {}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    if path not in CACHE:
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            while raw := stream.read(1 << 20):
                digest.update(raw)
        CACHE[path] = {'path': str(path), 'sha256': digest.hexdigest()}
    return CACHE[path]


def read(stem):
    path = DATA / (stem + '.json')
    source(path)
    value = json.loads(path.read_text())
    assert value['status'] == 'pass'
    return value


def module(name):
    path = ROOT / 'dembele/pari' / name
    source(path)
    spec = importlib.util.spec_from_file_location('d156_' + name[:3], path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def calculate():
    cost = read('precision_route_cost_d152')
    measured = read('dyadic_pilot_timing_d154')
    proof = read('proof_criterion_completion_d155')
    assert proof['conditional_two_order_sufficient_P'] == 10480
    assert (proof['full_sixteen_column_bank_precision_pi'], proof['column0_precision_pi'],
            proof['column2_precision_pi']) == (1600, 6400, 3200)
    inventory = module('560_dyadic_bank_recost.py')
    bounded = module('567_dyadic_checkpoint_admission_revision.py')
    coordinator = module('run_d139_indexed_production.py')
    full = cost['schedules'][0]
    stages = []
    for index, (seed, target, columns) in enumerate(((1600, 3200, 14), (3200, 6400, 15), (6400, 10480, 16))):
        inv = inventory.inventory(target, seed)
        live = bounded.inventory(target, seed)
        assert inv['largest_working_store']['bytes'] == live['maximum_bound']['total_bytes'] < 2 * GIB
        cfg = {'precision_pi': target, 'seed_precision_pi': seed,
               'digit_bits': 200, 'state_chunk': 1, 'rhs_chunk': 3, 'CM_chunk': 1}
        specs = [item for group in coordinator.schedule(cfg) for item in group]
        assert len(specs) == inv['production_jobs']
        assert dict(Counter(item['phase'] for item in specs)) == inv['phase_counts']
        assert len({item['key'] for item in specs}) == len(specs)
        jobs = inv['production_jobs'] + inv['archive_jobs'] + 26
        retained = inv['sealed_payload_bytes'] + inv['sealed_metadata_logical_allowance_bytes'] + jobs * (20480 + 4 * 220)
        extra = max(0, inv['largest_working_store']['bytes'] - inv['sealed_payload_bytes'])
        scenario_seconds = []
        for scenario in full['timing_scenarios']:
            old = scenario['stages'][index]
            assert (old['seed'], old['target']) == (seed, target)
            assert old['inventory'] == inv
            scenario_seconds.append(old['active_seconds_per_column'])
        stages.append({'seed': seed, 'target': target, 'remaining_columns': columns,
                       'inventory': inv, 'column_jobs': jobs,
                       'retained_allowance_per_column_bytes': retained,
                       'active_extra_bytes': extra,
                       'single_column_free_bytes_with_reserve': retained + extra + 10 * GIB,
                       'modeled_column_seconds': scenario_seconds})
    retained = sum(row['remaining_columns'] * row['retained_allowance_per_column_bytes'] for row in stages)
    extra = max(row['active_extra_bytes'] for row in stages)
    required = retained + extra + 10 * GIB
    assert required == measured['conditional_remaining_free_bytes_including_10GiB_reserve']
    assert sum(row['remaining_columns'] * row['column_jobs'] for row in stages) == measured['remaining_full_route_job_count'] == 1047369
    prefixes = []
    for count in range(1, 4):
        rows = stages[:count]
        prefixes.append({'through_precision_pi': rows[-1]['target'],
                         'free_bytes_with_reserve': sum(row['remaining_columns'] * row['retained_allowance_per_column_bytes'] for row in rows)
                         + max(row['active_extra_bytes'] for row in rows) + 10 * GIB,
                         'columns_or_stage_admitted': False})
    # Retain the larger D139 one-target-column provenance allowance. This is
    # conservative shared planning overhead, not an integrated measurement.
    recost = read('dyadic_indexed_bank_recost_r2_d139')
    baseline = next(row for row in recost['schedules'] if row['name'] == 'one_target_column_pilot')
    chosen = stages[1]
    timings = []
    for index, scenario in enumerate(baseline['timing_scenarios']):
        common = full['timing_scenarios'][index]['retained_common_comparison_seconds_allowance']
        graph = scenario['graph_review_seconds_allowance']
        cycle = chosen['modeled_column_seconds'][index]
        timings.append({'scenario': scenario['scenario'], 'column_cycle_seconds': cycle,
                        'graph_review_seconds_allowance': graph,
                        'common_comparison_seconds_allowance': common,
                        'total_active_hours': (cycle + graph + common) / 3600})
    return {'status': 'pass', 'milestone': 'D156', 'stages': stages,
            'all_existing_frozen_files_retained': True,
            'deletion_relocation_compression_or_clone_savings_assumed': False,
            'remaining_column_jobs': 1047369,
            'remaining_retained_allowance_bytes': retained,
            'largest_active_extra_bytes': extra, 'planning_reserve_bytes': 10 * GIB,
            'required_remaining_free_bytes': required,
            'rounded_full_bank_free_gate_bytes': ((required + GIB - 1) // GIB) * GIB,
            'cumulative_stage_storage_scenarios': prefixes,
            'conditional_remaining_active_days': [row['remaining_total_active_days'] for row in measured['conditional_remaining_scenarios']],
            'pilot': {'column': 2, 'seed': 3200, 'target': 6400,
                      'production_jobs': chosen['inventory']['production_jobs'],
                      'archive_jobs': chosen['inventory']['archive_jobs'],
                      'independent_audit_jobs': 24, 'column_review_jobs': 2,
                      'column_jobs': chosen['column_jobs'],
                      'working_store_bound_bytes': chosen['inventory']['largest_working_store']['bytes'],
                      'retained_allowance_bytes': chosen['retained_allowance_per_column_bytes'],
                      'active_extra_bytes': chosen['active_extra_bytes'],
                      'recommended_free_bytes_including_10GiB_reserve': chosen['single_column_free_bytes_with_reserve'],
                      'rounded_free_gate_bytes': ((chosen['single_column_free_bytes_with_reserve'] + GIB - 1) // GIB) * GIB,
                      'timing_scenarios': timings,
                      'retained_overhead_source': 'D139 one-target-column graph allowance plus D152 common comparison allowance',
                      'timing_is_not_a_bound_or_deadline': True,
                      'does_not_measure_P10480_cost': True},
            'space_gate_policy': 'Refresh free space immediately before launch; require the rounded pilot gate for the single column and the separately rounded remaining-route gate before a full-bank commitment. Preserve frozen data.',
            'storage_destination': str(ROOT), 'alternate_volume_selected': False,
            'alternate_volume_requires_separate_path_and_provenance_review': True,
            'new_precision_or_pilot_admitted_by_cost_packet': False,
            'actual_harmonic_precision_increased': False, 'candidate_identification_proved': False,
            'field_polynomial_constructed': False, 'resource_caps_changed': False}


if __name__ == '__main__':
    assert __debug__ and not OUT.exists()
    tick = time.monotonic()
    result = calculate()
    disk = shutil.disk_usage(ROOT)
    volumes = []
    mount_root = Path('/Volumes')
    if mount_root.is_dir():
        for path in sorted(mount_root.iterdir()):
            volumes.append({'path': str(path), 'resolved_path': str(path.resolve()),
                            'same_device_as_workspace': path.stat().st_dev == ROOT.stat().st_dev})
    result['filesystem_observation'] = {'observed_utc': datetime.now(timezone.utc).isoformat(),
                                       **disk._asdict(), 'workspace_device': ROOT.stat().st_dev,
                                       'visible_volume_entries': volumes, 'not_a_reservation': True}
    result['modeled_full_bank_shortfall_bytes'] = max(0, result['required_remaining_free_bytes'] - disk.free)
    result['rounded_full_bank_gate_shortfall_bytes'] = max(0, result['rounded_full_bank_free_gate_bytes'] - disk.free)
    result['pilot_fits_observed_rounded_gate'] = disk.free >= result['pilot']['rounded_free_gate_bytes']
    result['wall_seconds'] = time.monotonic() - tick
    result['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    assert result['peak_rss_bytes'] < 2 * GIB
    result['sources'] = [source(path) for path in sorted(PATHS)]
    with OUT.open('x') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print('PHASE_METADATA|' + json.dumps(source(OUT)), flush=True)
    print('PASS|645_DYADIC_STORAGE_TIMING_PLAN', flush=True)

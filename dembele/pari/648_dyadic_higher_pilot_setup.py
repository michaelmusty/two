"""D156 exact P3200-to-P6400 column-2 input bridge and configuration.

Preparation only; the initial create preflight is a separate capped job.
"""
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
CONFIG = 'dyadic_staged_P6400_col02_config_d156'
BASE = 'dyadic_staged_P6400_col02_d156'
BRIDGE = 'dyadic_higher_pilot_seed_bridge_d156'
PLAN = 'dyadic_higher_pilot_col02_audit_plan_d156'
ADMISSION = 'dyadic_higher_pilot_preparation_review_d156'
OUT = 'dyadic_higher_pilot_setup_d156'
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
    spec = importlib.util.spec_from_file_location('d156_setup_' + name[:3], path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def save(stem, value):
    path = DATA / (stem + '.json')
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')
    return source(path)


def setup():
    parent_stems = ['dyadic_precision1600_review_d138', 'dyadic_pilot_col02_review_d153']
    parents = [read(stem) for stem in parent_stems]
    known = {}
    for parent in parents:
        for ref in parent['sources']:
            assert ref['path'] not in known or known[ref['path']] == ref['sha256']
            known[ref['path']] = ref['sha256']
    seed_stem = 'dyadic_staged_P3200_col02_d153_seal'
    cm_stem = 'dyadic_CM_P3200_col02_d153'
    seed, cm = read(seed_stem), read(cm_stem)
    assert seed['working_precision_pi'] == cm['working_precision_pi'] == 3200
    assert seed['harmonic_basis_column'] == cm['harmonic_basis_column'] == 2
    assert seed['weighted_input'] and seed['certificate'] == {'original_weighted_fixed_point': True, 'all_fixed_masses': True}
    assert cm['coarse_error_beta'] == [6432, 6448, 6432, 6464]
    engine = module('554_dyadic_resumable_staged_production.py')
    dependencies = engine.immutable_dependencies() | {
        DATA / (seed_stem + '.json'), DATA / (cm_stem + '.json'), Path(seed['state_file']['path']),
        DATA / 'dyadic_target_transports_d121.json', DATA / 'dyadic_harmonic_certificate_d111.json',
        *(Path(chunk['file']['path']) for chunk in cm['moment_chunks'])}
    refs = [source(path) for path in sorted(dependencies)]
    for ref in refs:
        assert known[ref['path']] == ref['sha256'], ref['path']
    inv = module('567_dyadic_checkpoint_admission_revision.py').inventory(6400, 3200)
    assert inv['maximum_bound']['total_bytes'] == 973167872
    cost = read('dyadic_storage_timing_plan_d156')
    pilot = cost['pilot']
    free = shutil.disk_usage(ROOT).free
    assert free >= pilot['rounded_free_gate_bytes']
    cfg = {'status': 'pass', 'milestone': 'D132', 'execution_milestone': 'D156',
           'namespace': 'dyadic_rowjournal_P6400_col02_d156_d132', 'output_prefix': BASE,
           'precision_pi': 6400, 'seed_precision_pi': 3200, 'column': 2,
           'seed': seed_stem, 'CM_reference': cm_stem, 'prior_review': BRIDGE,
           'admission_review': ADMISSION, 'admission_replay_receipt': ADMISSION + '_recheck01.job',
           'digit_bits': 200, 'state_chunk': 1, 'rhs_chunk': 3, 'CM_chunk': 1,
           'audit_plan': PLAN, 'CM_output': 'dyadic_CM_P6400_col02_d156',
           'column_review': 'dyadic_higher_pilot_col02_review_d156',
           'working_store_bound_bytes': 973167872,
           'launch_free_space_gate_bytes': pilot['rounded_free_gate_bytes'],
           'purpose': 'One column-2 P3200-to-P6400 integrated timing pilot; reassess after all audits and reviews. No other column, P10480 stage or bank.'}
    assert not (DATA / cfg['namespace']).exists()
    oldplan = read('dyadic_precision6400_audit_plan_d133')
    jobs = []
    for previous in oldplan['jobs']:
        label = previous['stem'].removeprefix('dyadic_precision6400_').removesuffix('_d133')
        jobs.append({'driver': 'dembele/pari/646_dyadic_higher_pilot_independent.py',
                     'stem': 'dyadic_higher_pilot_col02_' + label + '_d156',
                     'marker': 'PASS|646_DYADIC_HIGHER_PILOT_INDEPENDENT',
                     'args': previous['args'] + ['--config', CONFIG]})
    assert len(jobs) == 24
    bridge = {'status': 'pass', 'milestone': 'D156', 'kind': 'direct_seed_native_dependency_bridge',
              'inherited_reviews': [source(DATA / (stem + '.json')) for stem in parent_stems],
              'all_sources_directly_bound_by_inherited_reviews': True,
              'working_precision_pi': 3200, 'harmonic_basis_column': 2, 'weighted_seed': True,
              'native_dependency_closure_complete': True, 'production_schedule_admitted_by_this_bridge': False,
              'sources': refs}
    save(BRIDGE, bridge)
    save(CONFIG, cfg)
    save(PLAN, {'status': 'pass', 'milestone': 'D137', 'execution_milestone': 'D156',
                'legacy_harness_schema_retained': True, 'kind': 'bounded_job_plan', 'config': CONFIG,
                'requires_completed_and_sealed_actual_column': True, 'maximum_workers': 3, 'jobs': jobs})
    return {'status': 'pass', 'milestone': 'D156', 'config': source(DATA / (CONFIG + '.json')),
            'seed_bridge': source(DATA / (BRIDGE + '.json')), 'audit_plan': source(DATA / (PLAN + '.json')),
            'inventory': inv, 'direct_seed_native_bindings': len(refs), 'planning_scenario': pilot,
            'filesystem_observation': {'observed_at': datetime.now(timezone.utc).isoformat(), 'free_bytes': free},
            'new_moments_evaluated': False, 'production_schedule_launched': False,
            'candidate_identification_proved': False, 'field_polynomial_constructed': False}


if __name__ == '__main__':
    assert __debug__ and not (DATA / (OUT + '.json')).exists()
    tick = time.monotonic()
    result = setup()
    result.update(wall_seconds=time.monotonic() - tick,
                  peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
                  sources=[source(path) for path in sorted(PATHS)])
    assert result['peak_rss_bytes'] <= 2 * (1 << 30)
    print('PHASE_METADATA|' + json.dumps(save(OUT, result)), flush=True)
    print('PASS|648_DYADIC_HIGHER_PILOT_SETUP', flush=True)

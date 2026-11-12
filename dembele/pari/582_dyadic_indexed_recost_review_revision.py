"""D139 revision 2 independent review; correct numbered barrier phase parsing.

Standard library only: neither production arithmetic nor the new lookup or
cost model is imported. The D138 provenance graph is rehashed transitively.
Empirical scenarios are checked as calculations, not certified predictions.
"""
import argparse
import ast
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import resource
import statistics
import sys
import time
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'dyadic_indexed_recost_review_r2_d139.json'
PATHS = {Path(__file__), ROOT / 'dembele/certificates/dyadic-indexed-recost-d139.md'}
CACHE = {}


def raw_source(path):
    path = Path(path).resolve()
    h = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            h.update(raw)
    return {'path': str(path), 'sha256': h.hexdigest()}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    if path not in CACHE:
        CACHE[path] = raw_source(path)
    return CACHE[path]


def checked(refs):
    for ref in refs:
        assert source(ref['path']) == ref, ref['path']


def read(stem):
    path = DATA / (stem + '.json')
    source(path)
    value = json.loads(path.read_text())
    assert value['status'] == 'pass'
    return value


def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-6), (a, b)


def graph(ref):
    assert raw_source(ref['path']) == ref
    prior = json.loads(Path(ref['path']).read_text())
    assert prior['status'] == 'pass' and prior['sixteen_column_checkpoint_complete']
    # Keep the inheritance graph compact in this review's own source list.
    for item in prior['sources']:
        assert raw_source(item['path']) == item, item['path']
    inherited = {}
    occurrences = 0
    for catalogue in prior['inherited_catalogues']:
        assert raw_source(catalogue['path']) == catalogue
        for item in json.loads(Path(catalogue['path']).read_text())['sources']:
            path, digest = item['path'], item['sha256']
            if path in inherited:
                assert inherited[path] == digest
            else:
                assert raw_source(path) == item, path
                inherited[path] = digest
            occurrences += 1
    assert occurrences == prior['catalogue_hash_replays'] == 380188
    assert len(inherited) == prior['unique_inherited_file_hashes'] == 379923
    for item in prior['sources']:
        if item['path'] in inherited:
            assert inherited[item['path']] == item['sha256']
        inherited[item['path']] = item['sha256']
    return prior, inherited, occurrences


def receipt(stem, driver, args):
    packet = read(stem)
    row = read(stem + '_attempt01.job')
    checked([row['driver'], row['log'], *row['sources'], *packet['sources']])
    assert row['driver'] == source(ROOT / 'dembele/pari' / driver)
    assert row['command'] == ['python3', row['driver']['path']] + args
    assert row['status'] == 'pass' and row['exit_code'] == 0
    assert row['wall_seconds'] < 180 and row['timeout_seconds'] == 180
    assert row['timeout_terminates_process_group']
    marks = [json.loads(line.split('|', 1)[1]) for line in Path(row['log']['path']).read_text().splitlines()
             if line.startswith('PHASE_METADATA|')]
    assert marks == [source(DATA / (stem + '.json'))]
    assert packet['peak_rss_bytes'] + packet.get('child_peak_rss_bytes', 0) < 2 * (1 << 30)
    return packet, row


def envelope(path):
    source(path)
    packet = json.loads(Path(path).read_text())
    raw = json.dumps(packet['value'], sort_keys=True, separators=(',', ':')).encode()
    assert set(packet) == {'value', 'sha256'}
    assert hashlib.sha256(raw).hexdigest() == packet['sha256']
    return packet['value']


def counts(S, P):
    corrections = (P - S - 1) // 33
    digits = math.ceil((P // 8) / 200)
    for step in range(corrections):
        digits += math.ceil((P // 8 - (S + 33 * step) // 8) / 200)
    phases = 438 + 243 * (corrections + 1) + 3 * digits
    return corrections, phases, phases + corrections + 27


def phase_of(key):
    if key.startswith(('operator', 'rhs')):
        return 'operator' if key.startswith('operator') else 'rhs'
    if key.startswith('prepare') and key[7:10].isdigit():
        return 'prepare-rows'
    if key.startswith(('prepare_begin_', 'prepare_finish_', 'sweep_begin_', 'sweep_finish_')):
        return '-'.join(key.split('_')[:2])
    if key.startswith('low_'):
        return '-'.join(key.split('_')[:2])
    if key.startswith('coarse_'):
        return 'coarse'
    if key.startswith(('extend_', 'verify_e', 'cm_e')):
        return key.split('_')[0]
    return key.replace('_', '-')


def code_review():
    old_path = ROOT / 'dembele/pari/run_d137_production_r2.py'
    new_path = ROOT / 'dembele/pari/run_d139_indexed_production.py'
    checked([source(old_path), source(new_path)])
    old, new = ast.parse(old_path.read_text()), ast.parse(new_path.read_text())
    def function(tree, name):
        return next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)
    same = ['schedule', 'run_window', 'checked', 'source', 'save']
    for name in same:
        assert ast.dump(function(old, name), include_attributes=False) == ast.dump(function(new, name), include_attributes=False)
    calls = [n for n in ast.walk(new) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
             and isinstance(n.func.value, ast.Name) and n.func.value.id == 'inventory']
    assert Counter(n.func.attr for n in calls) == {'preflight': 1, 'register': 2, 'reconcile': 1}
    text = new_path.read_text()
    for guard in ("admission['indexed_receipt_coordinator_admitted']", "source(cp) in admission['permitted_configs']",
                  "replay['timeout_seconds']==180", "assert 1<=a.workers<=3", "assert rss<=2*(1<<30)",
                  "assert bound<=6*(1<<30)", "assert not out.exists(),'completed coordinator must not be rerun'"):
        assert guard in text
    assert "DATA.glob(stem+'_attempt" not in text
    assert "archive_driver='dembele/pari/577_dyadic_indexed_metadata_archive.py'" in text
    # The exact probe includes both endpoints of the frozen two-digit pattern.
    lookup_path = ROOT / 'dembele/pari/576_dyadic_receipt_lookup.py'
    source(lookup_path)
    lookup = lookup_path.read_text()
    assert 'for n in range(100)' in lookup and 'os.path.lexists' in lookup
    assert "suffix.endswith('.log')" in lookup and 'current.names == self.names' in lookup
    return {'unchanged_function_ASTs': same, 'separate_admission_gate': True,
            'prefix_inventory_reconciled_before_completion': True}


def build():
    tick = time.monotonic()
    prior_ref = source(DATA / 'dyadic_precision1600_review_d138.json')
    prior, inherited, occurrences = graph(prior_ref)
    failed_path = DATA / 'dyadic_indexed_recost_review_d139_attempt01.job.json'
    source(failed_path)
    failed = json.loads(failed_path.read_text())
    assert failed['status'] == 'failed' and failed['exit_code'] == 1
    assert failed['wall_seconds'] < 180
    checked([failed['driver'], failed['log'], failed['failed_driver_snapshot'], *failed['sources']])
    assert failed['driver']['sha256'] == failed['failed_driver_snapshot']['sha256']
    assert "KeyError: 'prepare-begin-000'" in Path(failed['log']['path']).read_text()
    assert not (DATA / 'dyadic_indexed_recost_review_d139.json').exists()
    controls = {}
    for phase, stem in [('lookup', 'dyadic_receipt_lookup_controls_d139'), ('archive', 'dyadic_indexed_archive_controls_d139')]:
        controls[phase], _ = receipt(stem, '578_dyadic_receipt_lookup_controls.py',
                                    ['--phase', phase, '--output', stem])
    lookup, archive = controls['lookup']['certificates'], controls['archive']['certificates']
    assert lookup['synthetic_stem_cases'] == 8 and lookup['actual_receipts_checked'] == 13176
    assert lookup['failure_partial_duplicate_and_resume_controls_pass'] and lookup['old_glob_matches_preserved']
    for row in lookup['completed_column_checks']:
        assert row['column'] in (2, 15) and row['all_production_receipts_checked'] == 6588
        assert len(row['legacy_sample_seconds']) == len(row['exact_sample_seconds']) == 4
        close(row['median_legacy_lookup_seconds'], statistics.median(row['legacy_sample_seconds']))
        close(row['median_exact_lookup_seconds'], statistics.median(row['exact_sample_seconds']))
    original_path = DATA / 'dyadic_rowjournal_P1600_col15_r2_d132/archive_sweep_finish_000.json'
    original_ref = source(original_path)
    assert inherited[original_ref['path']] == original_ref['sha256']
    original = envelope(original_path)
    assert len(original['items']) == 422
    for row in archive['synthetic_stores']:
        packet = envelope(row['archive']['archive']['path'])
        selected = original['items'] if row['mode'] == 'complete' else original['items'][:3]
        assert packet['items'] == selected and len(selected) == row['copied_records']
        assert packet['external_records_remain_frozen'] and not packet['arithmetic_payloads_removed']
        assert packet['source'] == source(ROOT / 'dembele/pari/577_dyadic_indexed_metadata_archive.py')
        folder = Path(row['archive']['archive']['path']).parent
        assert (folder / 'SEALED.json').exists()
        assert not any((folder / item['name']).exists() for item in selected)
        checked(row['sentinels_preserved'])
        if row['mode'] != 'complete':
            assert row['intentional_exit'] == 73
            assert row['remaining_at_interruption'] == (3 if row['mode'] == 'archive_intent' else 2)
        for item in selected:
            checked([item['external_metadata'], item['passing_receipt']])
            raw = Path(item['external_metadata']['path']).read_text()
            d = json.loads(raw)
            encoded = json.dumps({'value': d, 'sha256': hashlib.sha256(json.dumps(d, sort_keys=True, separators=(',', ':')).encode()).hexdigest()}, sort_keys=True, separators=(',', ':')).encode()
            assert len(encoded) == item['bytes'] and hashlib.sha256(encoded).hexdigest() == item['internal_sha256']
    model, _ = receipt('dyadic_indexed_bank_recost_r2_d139', '580_dyadic_indexed_bank_recost_revision.py',
                       ['--output', 'dyadic_indexed_bank_recost_r2_d139'])
    superseded, _ = receipt('dyadic_indexed_bank_recost_d139', '579_dyadic_indexed_bank_recost.py',
                            ['--output', 'dyadic_indexed_bank_recost_d139'])
    assert model['superseded_cost_model'] == source(DATA / 'dyadic_indexed_bank_recost_d139.json')
    assert model['prior_fixed_review'] == prior_ref
    assert model['current_full_bank_precision_pi'] == 1600 and model['current_column0_precision_pi'] == 6400
    assert model['conditional_sufficient_target_precision_pi'] == 10552
    for flag in ('actual_harmonic_precision_increased', 'candidate_identification_proved', 'field_polynomial_constructed',
                 'next_precision_bank_admitted', 'resource_caps_changed'):
        assert model[flag] is False
    assert model['model_is_empirical_not_runtime_or_allocation_bound']
    old = read('dyadic_bank_recost_d135')
    old_ref = source(DATA / 'dyadic_bank_recost_d135.json')
    assert inherited[old_ref['path']] == old_ref['sha256']
    legacy = next(s for s in old['schedules'] if s['name'] == 'full_bank_staged')
    assert {phase_of(k) for k in ['prepare_begin_000', 'prepare_finish_048', 'sweep_begin_000', 'sweep_finish_048']} == {'prepare-begin', 'prepare-finish', 'sweep-begin', 'sweep-finish'}
    phase_samples, phase_counts, overheads = {}, None, []
    for observation in model['measured_completed_columns']:
        col = observation['column']
        completed = read(f'dyadic_staged_P1600_col{col:02d}_r2_d137_completed')
        production_ref = source(DATA / f'dyadic_staged_P1600_col{col:02d}_r2_d137_completed.json')
        assert inherited[production_ref['path']] == production_ref['sha256']
        totals, census = Counter(), Counter()
        for row in completed['jobs']:
            phase = phase_of(row['key'])
            totals[phase] += row['seconds']
            census[phase] += 1
        assert sum(census.values()) == 6588
        if phase_counts is not None:
            assert phase_counts == census
        phase_counts = census
        for phase, seconds in totals.items():
            phase_samples.setdefault(phase, []).append(seconds)
        close(sum(totals.values()), observation['arithmetic_worker_seconds'])
        close(completed['wall_seconds'], observation['recorded_production_coordinator_seconds'])
        overhead = statistics.median(max(0, r['coordinator_interval'][1] - r['coordinator_interval'][0] - r['seconds']) for r in completed['jobs'])
        close(overhead, observation['median_wrapper_overhead_seconds'])
        overheads.append(overhead)
        close(observation['counterfactual_indexed_production_seconds'],
              observation['reconstructed_groups_without_directory_discovery_seconds'] +
              observation['indexed_archive_allowance_seconds'] + observation['indexed_discovery_allowance_seconds'])
    assert [x['column'] for x in model['measured_completed_columns']] == list(range(2, 16))
    for phase, samples in phase_samples.items():
        close(model['measured_P1600_worker_seconds_per_job_floors'][phase], statistics.median(samples) / phase_counts[phase])
    parameters = model['cost_parameters']
    close(parameters['new_wrapper_overhead_seconds'], max(overheads))
    close(parameters['old_wrapper_overhead_seconds'], old['measured_D133']['median_observed_per_job_coordinator_overhead_seconds'])
    close(parameters['receipt_query_seconds_allowance'], 2 * max(t for row in lookup['completed_column_checks'] for t in row['exact_sample_seconds']))
    archive_seconds = archive['synthetic_stores'][0]['archive']['wall_seconds']
    close(model['archive_422_records_measured_seconds'], archive_seconds)
    plans = {'next_P3200_checkpoint': [(1600, 3200, 15)],
             'remaining_staged_conditional_target': [(1600, 3200, 15), (3200, 6400, 15), (6400, 10552, 16)],
             'one_target_column_pilot': [(6400, 10552, 1)]}
    checked_schedules = []
    for schedule in model['schedules']:
        plan = plans[schedule['name']]
        total_jobs = sum(n * counts(S, P)[2] for S, P, n in plan)
        assert total_jobs == schedule['total_jobs_including_archives_audits_reviews']
        storage = schedule['storage_components']
        close(storage['incremental_catalogue_allowance_bytes'], 4 * total_jobs * 220)
        for scenario, timing in enumerate(schedule['timing_scenarios']):
            inherited_timing = legacy['timing_scenarios'][scenario]
            payload, metadata, extra = 0, 0, 0
            for stage, (S, P, n) in zip(timing['stages'], plan):
                assert (stage['seed'], stage['target'], stage['columns']) == (S, P, n)
                previous = next(x for x in inherited_timing['stages'] if (x['seed'], x['target']) == (S, P))
                inv = stage['inventory']
                assert inv == previous['inventory'] and inv['fits_2GiB_store_cap']
                corrections, phases, per_column = counts(S, P)
                assert inv['corrections'] == corrections and inv['production_jobs'] == phases
                assert stage['jobs_per_column'] == per_column
                assert inv['largest_working_store']['bytes'] < 2 * (1 << 30)
                payload += n * inv['sealed_payload_bytes']
                metadata += n * inv['sealed_metadata_logical_allowance_bytes']
                extra = max(extra, max(0, inv['largest_working_store']['bytes'] - inv['sealed_payload_bytes']))
                for phase, seconds in previous['worker_seconds_by_phase'].items():
                    if phase == 'archive':
                        continue
                    count = inv['phase_counts'].get(phase, 24 if phase == 'independent-audits' else 2)
                    adjusted = seconds + count * max(0, parameters['new_wrapper_overhead_seconds'] - parameters['old_wrapper_overhead_seconds'])
                    floor = count * (model['measured_P1600_worker_seconds_per_job_floors'].get(phase, 0) + parameters['new_wrapper_overhead_seconds'])
                    expected = max(adjusted, floor)
                    close(stage['worker_seconds_by_phase'][phase], expected)
                    close(stage['active_seconds_by_phase'][phase], expected * previous['active_seconds_by_phase'][phase] / seconds)
                digits = math.ceil((P // 8) / 200)
                per_archive = (archive_seconds * P / 1600 * (422 + 3 * (digits - 1)) / 422 + .15 + parameters['new_wrapper_overhead_seconds']) * (1 + scenario)
                close(stage['archive_seconds_per_job_scenario'], per_archive)
                close(stage['active_seconds_by_phase']['archive'], inv['archive_jobs'] * per_archive)
                discovery = (phases * parameters['receipt_query_seconds_allowance'] +
                             2 * (parameters['directory_entries'] + 3 * total_jobs) * parameters['directory_scan_seconds_per_entry']) * (1 + scenario)
                close(stage['active_seconds_by_phase']['receipt-discovery'], discovery)
                close(stage['worker_seconds'], sum(stage['worker_seconds_by_phase'].values()))
                close(stage['active_seconds'], sum(stage['active_seconds_by_phase'].values()))
            assert storage['payload_bytes'] == payload and storage['metadata_logical_bytes'] == metadata
            assert storage['largest_active_extra_bytes'] == extra
            review_allowance = parameters['D138_transitive_replay_seconds'] * (1 + 3 * total_jobs / 379923) * (max(P for S, P, n in plan) / 1600) ** 2 * (1 + .5 * scenario)
            close(timing['graph_review_seconds_allowance'], review_allowance)
            tail = 0 if schedule['name'] == 'one_target_column_pilot' else inherited_timing['full_frame_and_quadric_worker_seconds_allowance']
            close(timing['common_comparison_seconds_allowance'], tail)
            active = sum(s['columns'] * s['active_seconds'] for s in timing['stages']) + tail + review_allowance
            worker = sum(s['columns'] * s['worker_seconds'] for s in timing['stages']) + tail + review_allowance
            close(timing['active_hours'], active / 3600)
            close(timing['active_days'], active / 86400)
            close(timing['worker_hours'], worker / 3600)
        allowance = payload + metadata + total_jobs * 20480 + storage['incremental_catalogue_allowance_bytes'] + extra
        measured = math.ceil(payload + metadata * parameters['store_metadata_allocation_ratio'] + total_jobs * parameters['external_allocated_bytes_per_job'] + storage['incremental_catalogue_allowance_bytes'] + extra)
        assert schedule['additional_bytes_allowance_scenario'] == allowance
        assert schedule['additional_allocated_bytes_measured_ratio_scenario'] == measured
        assert schedule['recommended_free_bytes_including_10GiB_reserve'] == allowance + 10 * (1 << 30)
        checked_schedules.append({'name': schedule['name'], 'jobs': total_jobs,
                                  'active_hours': [s['active_hours'] for s in schedule['timing_scenarios']],
                                  'additional_bytes': [measured, allowance],
                                  'recommended_free_bytes': allowance + 10 * (1 << 30)})
    code = code_review()
    for path, ref in CACHE.items():
        if str(path) in inherited:
            assert inherited[str(path)] == ref['sha256']
    return {'status': 'pass', 'milestone': 'D139', 'independent_finite_review_complete': True,
            'inherited_review': prior_ref, 'catalogue_graph_is_transitive': True,
            'inherited_catalogue_hash_occurrences': occurrences, 'unique_inherited_file_hashes': 379923,
            'all_inherited_bindings_preserved': True, 'completed_input_jobs': 4, 'failed_input_jobs': 0,
            'preserved_failed_review_builds': 1, 'failed_review_receipt': source(failed_path),
            'review_parser_regressions': {k: phase_of(k) for k in ['prepare_begin_000', 'prepare_finish_048', 'sweep_begin_000', 'sweep_finish_048']},
            'receipt_discovery_controls': {'synthetic_cases': 8, 'actual_receipts': 13176},
            'archive_control': {'exact_original_items': 422, 'measured_seconds': archive_seconds,
                                'both_interruption_points_pass': True}, 'coordinator_code_review': code,
            'reviewed_cost_model': source(DATA / 'dyadic_indexed_bank_recost_r2_d139.json'),
            'reviewed_schedules': checked_schedules, 'estimates_are_empirical_scenarios': True,
            'full_bank_precision_pi': 1600, 'column0_precision_pi': 6400,
            'positive_exact_quadric_vanishing_proved': False, 'candidate_identification_proved': False,
            'field_polynomial_constructed': False, 'indexed_receipt_coordinator_admitted': False,
            'next_precision_bank_admitted': False, 'resource_caps_changed': False,
            'wall_seconds': time.monotonic() - tick,
            'sources': [source(p) for p in sorted(PATHS)]}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    tick = time.monotonic()
    if args.check:
        saved = json.loads(OUT.read_text())
        assert saved['status'] == 'pass' and saved['independent_finite_review_complete']
        checked(saved['sources'])
        _, _, occurrences = graph(saved['inherited_review'])
        assert occurrences == saved['inherited_catalogue_hash_occurrences']
    else:
        assert not OUT.exists()
        saved = build()
        saved['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
        assert saved['peak_rss_bytes'] < 2 * (1 << 30)
        with OUT.open('x') as f:
            f.write(json.dumps(saved, indent=2) + '\n')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    assert peak < 2 * (1 << 30)
    print('D139_REVIEW_RESOURCES|' + json.dumps({'seconds': time.monotonic() - tick, 'peak_rss_bytes': peak}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(OUT)), flush=True)
    print('PASS|582_DYADIC_INDEXED_RECOST_REVIEW_REVISION', flush=True)

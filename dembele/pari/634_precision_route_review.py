"""D152 fixed review, transitive replay, source ledger and completion."""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
REPORT = ROOT / 'dembele/certificates/precision-route-cost-d152.md'
OUT = DATA / 'precision_route_review_d152.json'
LEDGER = DATA / 'precision_route_sources_d152.json'
COMPLETION = DATA / 'precision_route_completion_d152.json'
HELPER = ROOT / 'dembele/pari/631_summed_transfer_review.py'
PATHS = {Path(__file__), HELPER}


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


prior = module(HELPER, 'd152_inherited_provenance')


def raw_source(path):
    p = Path(path).resolve()
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def source(path):
    p = Path(path).resolve()
    PATHS.add(p)
    return raw_source(p)


def checked(refs):
    for ref in refs:
        assert raw_source(ref['path']) == ref, ref['path']


def read(stem):
    p = DATA / (stem + '.json')
    source(p)
    obj = json.loads(p.read_text())
    assert obj['status'] == 'pass', stem
    return obj


def graph():
    parent = read('summed_transfer_review_d151')
    assert parent['independent_finite_review_complete']
    checked(parent['sources'])
    assert len(parent['sources']) == 20
    inherited = prior.graph()
    assert parent['finite_rational_witness_search_parked']
    assert not parent['candidate_identification_proved']
    return {'D151_direct_bindings': 20, **inherited}


def validate_job(row, driver, output_ref, args=()):
    checked([row['driver'], row['log'], *row['sources']])
    assert row['driver'] == source(ROOT / 'dembele/pari' / driver)
    assert row['command'] == ['python3', row['driver']['path']] + list(args)
    assert row['status'] == 'pass' and row['exit_code'] == 0
    assert 0 < row['wall_seconds'] < row['timeout_seconds'] == 180
    assert row['private_process_group'] > 0 and row['timeout_terminates_process_group']
    lines = Path(row['log']['path']).read_text().splitlines()
    marks = [json.loads(s.split('|', 1)[1]) for s in lines if s.startswith('PHASE_METADATA|')]
    assert marks == [output_ref]
    assert any(s.startswith('PASS|' + driver[:3] + '_') for s in lines)


def validate_inputs():
    packets, receipts = [], []
    for stem, driver in [
        ('precision_route_cost_d152', '632_precision_route_cost.py'),
        ('precision_route_controls_d152', '633_precision_route_controls.py'),
    ]:
        packet = read(stem)
        checked(packet['sources'])
        row = read(stem + '_attempt01.job')
        validate_job(row, driver, source(DATA / (stem + '.json')))
        assert packet['peak_rss_bytes'] < 2*(1 << 30)
        code = ROOT / 'dembele/pari' / driver
        ast.parse(code.read_text())
        replay = module(code, 'd152_replay_' + driver[:3]).calculate()
        assert all(packet[k] == v for k, v in replay.items())
        receipts.append({'receipt': source(DATA / (stem + '_attempt01.job.json')),
                         'wall_seconds': row['wall_seconds'], 'peak_rss_bytes': packet['peak_rss_bytes']})
        packets.append(packet)
    first, second = packets
    assert first['rank45_two_positive_order_sufficient_P'] == second['rank45_two_positive_order_sufficient_P'] == 10480
    assert first['four_coefficient_sufficient_P'] == 10552
    assert second['independent_uncollected_section_thresholds'] == [10416, 10480, 10552]
    full, pilot = first['schedules']
    assert full['total_jobs_including_archives_audits_reviews'] == 1059939
    assert pilot['total_jobs_including_archives_audits_reviews'] == 12570
    assert first['free_space_shortfalls_at_observation_bytes'][full['name']] > 0
    assert first['free_space_shortfalls_at_observation_bytes'][pilot['name']] == 0
    assert second['D136_complete_synthetic_chart_count'] == 17
    for p in packets:
        assert p['times_are_empirical_allowances_not_runtime_bounds']
        for key in ['new_precision_bank_admitted', 'actual_harmonic_precision_increased',
                    'candidate_identification_proved', 'field_polynomial_constructed']:
            assert not p[key]
    return receipts


def local_links(path, text, allowed_missing=()):
    results = []
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if link.startswith(('https://', 'http://', '#')):
            continue
        p = (path.parent / link.split('#', 1)[0]).resolve()
        assert p.is_file() or p in allowed_missing, (path, link)
        results.append(p)
    return results


def build():
    inherited = graph()
    print('D152_TRANSITIVE_GRAPH_PASS', flush=True)
    completion = read('summed_transfer_completion_d151')
    parent_ref = source(DATA / 'summed_transfer_review_d151.json')
    assert completion['fixed_review'] == parent_ref
    assert completion['successful_bounded_jobs'] == 5 and completion['failed_bounded_jobs'] == 0
    for i, ref in enumerate(completion['review_receipts']):
        checked([ref])
        source(ref['path'])
        validate_job(json.loads(Path(ref['path']).read_text()), HELPER.name, parent_ref,
                     [] if i == 0 else ['--check'])
    parent_finish = read('summed_transfer_completion_d151_attempt01.job')
    validate_job(parent_finish, HELPER.name, source(DATA / 'summed_transfer_completion_d151.json'), ['--finish'])
    receipts = validate_inputs()
    links = local_links(REPORT, REPORT.read_text(), (OUT, LEDGER, COMPLETION))
    reports = sorted({p for p in links if p.suffix == '.md'})
    ledger = {'status': 'pass', 'milestone': 'D152',
              'scope': 'Bounded cost assessment of the established precision/height route, combining the D120 uniform section precision with the D140 actual rank-45 restriction.',
              'external_sources': [],
              'source_policy': 'Reuse inspected local certificates and their inherited theorem/provenance chains; no new external theorem or current hardware benchmark is claimed.',
              'inspected_reports': [source(p) for p in reports],
              'P10480_rank_refinement_is_companion_argument': True,
              'sufficient_precision_distinguished_from_achieved_precision': True,
              'empirical_time_and_storage_distinguished_from_proved_bounds': True,
              'geometric_rank_implication_not_mechanically_verified': True,
              'no_precision_launch_admission': True, 'sources': [source(REPORT)]}
    assert not LEDGER.exists()
    with LEDGER.open('x') as out:
        out.write(json.dumps(ledger, indent=2)+'\n')
    source(LEDGER)
    cost = read('precision_route_cost_d152')
    return {'status': 'pass', 'milestone': 'D152', 'independent_finite_review_complete': True,
            'inherited_review': parent_ref, 'catalogue_graph_is_transitive': True, **inherited,
            'input_receipts': receipts, 'completed_input_jobs': 2, 'preserved_failed_input_jobs': 0,
            'rank45_two_positive_order_sufficient_P': 10480,
            'four_coefficient_sufficient_P': 10552,
            'P10480_sufficiency_requires_future_certified_zero_enclosures': True,
            'uniform_error_law_and_rank_implication_checked': True,
            'full_target_job_count': 1059939, 'pilot_job_count': 12570,
            'full_target_modeled_active_days': [s['active_days'] for s in cost['schedules'][0]['timing_scenarios']],
            'pilot_modeled_active_hours': [s['active_hours'] for s in cost['schedules'][1]['timing_scenarios']],
            'full_target_free_bytes_with_reserve': cost['schedules'][0]['recommended_free_bytes_including_10GiB_reserve'],
            'observed_free_bytes': cost['filesystem_observation']['free'],
            'full_target_space_shortfall_bytes': cost['free_space_shortfalls_at_observation_bytes'][cost['schedules'][0]['name']],
            'direct_seed_to_target_exceeds_store_cap': True,
            'D136_complete_CM_memory_controls_reused': True,
            'times_and_storage_are_empirical_scenarios': True,
            'finite_rational_transfer_search_remains_parked': True,
            'candidate_identification_proved': False, 'positive_exact_quadric_vanishing_proved': False,
            'field_polynomial_constructed': False,
            'best_current_proved_relation_height_upper': 15237, 'P1600_sufficient_height_target': 623,
            'actual_harmonic_precision_increased': False, 'next_precision_bank_admitted': False,
            'pilot_launch_admitted': False, 'resource_caps_changed': False,
            'full_bank_precision_pi': 1600, 'column0_precision_pi': 6400,
            'inspected_report_count': len(reports), 'report_local_links_checked': len(links),
            'next_work': 'Prepare a concrete, separately reviewed P1600-to-P3200 timing pilot for column 2 using its existing reviewed seed/CM data and the D139 indexed coordinator. Preserve source-554 direct dependency admission, independent audits, bounded provenance, and all caps. No launch follows from this cost checkpoint; the multiweek bank also needs about 20 GiB more free space.',
            'sources': [source(p) for p in sorted(PATHS)]}


def finish():
    saved = read(OUT.stem)
    checked(saved['sources'])
    review_ref = source(OUT)
    rows, resources = [], []
    for suffix, args in [('attempt01', []), ('recheck01', ['--check'])]:
        p = DATA / ('precision_route_review_d152_' + suffix + '.job.json')
        row = read(p.stem)
        validate_job(row, Path(__file__).name, review_ref, args)
        rows.append(source(p))
        marks = [json.loads(s.split('|', 1)[1]) for s in Path(row['log']['path']).read_text().splitlines()
                 if s.startswith('D152_REVIEW_RESOURCES|')]
        assert len(marks) == 1
        resources.append({'receipt_wall_seconds': row['wall_seconds'], **marks[0]})
    docs = ['HANDOFF.md', 'CLAUDE.md', 'README.md', 'DECISIONS.md', 'REFERENCES.md',
            'dembele/README.md', 'dembele/pari/README.md']
    links = []
    for name in docs:
        p = ROOT / name
        block = p.read_text().split('<!-- D152 precision cost checkpoint -->', 1)[1].split('<!-- End D152 precision cost checkpoint -->', 1)[0]
        assert all(s in block for s in ['10480', '10552', '15237', '623', 'source 635 is next unused'])
        assert 'pilot' in block and 'conditional' in block
        links.extend(local_links(p, block, (COMPLETION,)))
    assert len(links) == 28
    local_links(REPORT, REPORT.read_text(), (COMPLETION,))
    result = {k: v for k, v in saved.items() if k not in ['sources', 'wall_seconds', 'peak_rss_bytes']}
    result.update({'completed_at': datetime.now(timezone.utc).isoformat(), 'fixed_review': review_ref,
                   'report': source(REPORT), 'source_applicability_ledger': source(LEDGER),
                   'review_receipts': rows, 'review_resources': resources,
                   'successful_bounded_jobs': 5, 'input_bounded_jobs': 2, 'review_bounded_jobs': 2,
                   'completion_bounded_jobs': 1, 'failed_bounded_jobs': 0,
                   'completion_job_receipt_path': str(DATA / 'precision_route_completion_d152_attempt01.job.json'),
                   'entry_documents_updated': docs, 'current_artifact_links_checked': len(links),
                   'direct_source_bindings': len(saved['sources']), 'next_unused_source': 635,
                   'entry_document_hashes_intentionally_not_frozen': True, 'all_D152_jobs_sequential': True})
    with COMPLETION.open('x') as out:
        out.write(json.dumps(result, indent=2)+'\n')
    assert all(p.is_file() for p in links)


if __name__ == '__main__':
    assert __debug__
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--check', action='store_true')
    modes.add_argument('--finish', action='store_true')
    args = parser.parse_args()
    tick = time.monotonic()
    output = OUT
    if args.finish:
        finish()
        output = COMPLETION
    elif args.check:
        saved = read(OUT.stem)
        checked(saved['sources'])
        inherited = graph()
        assert all(saved[k] == v for k, v in inherited.items())
        assert validate_inputs() == saved['input_receipts']
    else:
        assert not OUT.exists()
        saved = build()
        saved['wall_seconds'] = time.monotonic()-tick
        saved['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
        assert saved['peak_rss_bytes'] < 2*(1 << 30)
        with OUT.open('x') as out:
            out.write(json.dumps(saved, indent=2)+'\n')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    assert peak < 2*(1 << 30)
    print('D152_REVIEW_RESOURCES|'+json.dumps({'seconds': time.monotonic()-tick, 'peak_rss_bytes': peak}), flush=True)
    print('PHASE_METADATA|'+json.dumps(source(output)), flush=True)
    print('PASS|634_PRECISION_ROUTE_REVIEW', flush=True)

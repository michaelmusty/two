"""D151 fixed review, transitive replay, source ledger and completion."""
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
REPORT = ROOT / 'dembele/certificates/summed-transfer-obstruction-d151.md'
OUT = DATA / 'summed_transfer_review_d151.json'
LEDGER = DATA / 'summed_transfer_sources_d151.json'
COMPLETION = DATA / 'summed_transfer_completion_d151.json'
HELPER = ROOT / 'dembele/pari/628_structural_identification_review.py'
PATHS = {Path(__file__), HELPER}


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


prior = module(HELPER, 'd151_inherited_provenance')


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
    item = json.loads(p.read_text())
    assert item['status'] == 'pass', stem
    return item


def graph():
    parent = read('structural_identification_review_d150')
    assert parent['independent_finite_review_complete']
    checked(parent['sources'])
    assert len(parent['sources']) == 32
    inherited = prior.graph()
    assert parent['best_current_proved_relation_height_upper'] == 15237
    assert not parent['candidate_identification_proved']
    return {'D150_direct_bindings': 32, **inherited}


def validate_job(row, driver, output_ref, args=()):
    checked([row['driver'], row['log'], *row['sources']])
    assert row['driver'] == source(ROOT / 'dembele/pari' / driver)
    assert row['command'] == ['python3', row['driver']['path']] + list(args)
    assert row['status'] == 'pass' and row['exit_code'] == 0
    assert 0 < row['wall_seconds'] < row['timeout_seconds'] == 180
    assert row['private_process_group'] > 0 and row['timeout_terminates_process_group']
    lines = Path(row['log']['path']).read_text().splitlines()
    metadata = [json.loads(s.split('|', 1)[1]) for s in lines if s.startswith('PHASE_METADATA|')]
    assert metadata == [output_ref]
    assert any(s.startswith('PASS|' + driver[:3] + '_') for s in lines)


def validate_inputs():
    packets, receipts = [], []
    for stem, driver in [
        ('summed_transfer_obstruction_d151', '629_summed_transfer_obstruction.py'),
        ('summed_transfer_controls_d151', '630_summed_transfer_controls.py'),
    ]:
        packet = read(stem)
        checked(packet['sources'])
        row = read(stem + '_attempt01.job')
        validate_job(row, driver, source(DATA / (stem + '.json')))
        assert packet['peak_rss_bytes'] < 2 * (1 << 30)
        code = ROOT / 'dembele/pari' / driver
        ast.parse(code.read_text())
        replay = module(code, 'd151_replay_' + driver[:3]).calculate()
        assert all(packet[k] == v for k, v in replay.items())
        receipts.append({'receipt': source(DATA / (stem + '_attempt01.job.json')),
                         'wall_seconds': row['wall_seconds'],
                         'peak_rss_bytes': packet['peak_rss_bytes']})
        packets.append(packet)
    first, second = packets
    for key in ['gradient_at_V0_power_coordinates', 'cleared_residual_total_degree',
                'scalar_input_count', 'nonzero_gradient_coordinate_zero_based']:
        assert first[key] == second[key]
    assert first['selected_coarse_order'] == second['selected_coarse_order'] == 1
    assert first['cleared_residual_total_degree'] == 240
    assert first['scalar_input_count'] == 288
    assert first['obstruction_functionals_are_discontinuous']
    assert second['gradient_checked_by_exact_central_difference']
    assert second['explicit_leaf_count_partitions_checked'] == 9
    assert not second['infinite_functional_construction_mechanically_verified']
    for p in packets:
        assert p['finite_rational_transfer_certificate_excluded_for_selected_residual_by_companion_proof']
        for key in ['actual_bounded_measure_uniqueness_refuted', 'candidate_identification_proved',
                    'candidate_refuted', 'positive_exact_quadric_vanishing_proved',
                    'new_precision_bank_admitted', 'actual_harmonic_precision_increased']:
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
    print('D151_TRANSITIVE_GRAPH_PASS', flush=True)
    completion = read('structural_identification_completion_d150')
    parent_ref = source(DATA / 'structural_identification_review_d150.json')
    assert completion['fixed_review'] == parent_ref
    assert completion['successful_bounded_jobs'] == 5 and completion['failed_bounded_jobs'] == 0
    for i, ref in enumerate(completion['review_receipts']):
        checked([ref])
        source(ref['path'])
        validate_job(json.loads(Path(ref['path']).read_text()), HELPER.name, parent_ref,
                     [] if i == 0 else ['--check'])
    parent_finish = read('structural_identification_completion_d150_attempt01.job')
    validate_job(parent_finish, HELPER.name,
                 source(DATA / 'structural_identification_completion_d150.json'), ['--finish'])
    receipts = validate_inputs()
    report_links = local_links(REPORT, REPORT.read_text(), (OUT, LEDGER, COMPLETION))
    reports = sorted({p for p in report_links if p.suffix == '.md'})
    ledger = {'status': 'pass', 'milestone': 'D151',
              'scope': 'Test the D150 finite rational summed-transfer certificate on the first positive CM coefficient of saved candidate quadric zero; give a principal-part functional obstruction and park that witness search.',
              'external_sources': [
                  {'title': 'Franc and Masdeu, Computing fundamental domains for the Bruhat-Tits tree for GL2(Qp), p-adic automorphic forms, and the canonical embedding of Shimura curves',
                   'url': 'https://arxiv.org/pdf/1201.0356', 'checked_on': '2026-10-09',
                   'role': 'Section 4.2 distinguishes finite additive distributions from integration of continuous/analytic functions using boundedness and convergent series. D113 supplies the direct ramified boundedness argument. The D151 obstruction is a companion derivation, not attributed to the paper.'}],
              'inspected_reports': [source(p) for p in reports],
              'principal_part_functional_construction_is_companion_proof': True,
              'actual_bounded_measures_distinguished_from_discontinuous_functionals': True,
              'nonconstant_formal_residual_distinguished_from_actual_nonvanishing': True,
              'finite_checks_do_not_mechanically_verify_infinite_or_geometric_proofs': True,
              'candidate_not_refuted': True, 'sources': [source(REPORT)]}
    assert not LEDGER.exists()
    with LEDGER.open('x') as out:
        out.write(json.dumps(ledger, indent=2) + '\n')
    source(LEDGER)
    return {'status': 'pass', 'milestone': 'D151', 'independent_finite_review_complete': True,
            'inherited_review': parent_ref, 'catalogue_graph_is_transitive': True, **inherited,
            'input_receipts': receipts, 'completed_input_jobs': 2, 'preserved_failed_input_jobs': 0,
            'selected_quadric_index_zero_based': 0, 'selected_CM_index_zero_based': 0,
            'selected_coarse_order': 1, 'nonzero_gradient_coordinate_zero_based': 0,
            'cleared_residual_total_degree': 240, 'scalar_input_count': 288,
            'finite_rational_transfer_certificate_excluded_for_selected_residual_by_companion_proof': True,
            'summed_cancellations_allowed_in_obstruction': True,
            'all_polynomial_moments_preserved_by_obstruction_functionals': True,
            'obstruction_functionals_are_discontinuous': True,
            'finite_rational_witness_search_parked': True,
            'actual_bounded_measure_uniqueness_refuted': False,
            'candidate_identification_proved': False, 'candidate_refuted': False,
            'positive_exact_quadric_vanishing_proved': False,
            'field_polynomial_constructed': False,
            'best_current_proved_relation_height_upper': 15237, 'sufficient_height_target': 623,
            'height_bound_at_most_623_proved': False, 'height_bound_at_most_623_disproved': False,
            'actual_harmonic_precision_increased': False, 'next_precision_bank_admitted': False,
            'resource_caps_changed': False, 'full_bank_precision_pi': 1600, 'column0_precision_pi': 6400,
            'inspected_report_count': len(reports),
            'report_local_links_checked_including_pending_packet_outputs': len(report_links),
            'next_work': 'End the finite rational witness search. Any further identification attempt must name additional analytic or geometric input, or reassess the cost of the established sufficient precision/height route without admitting a larger bank. Preserve rank-45/order-four and downstream marking obligations.',
            'sources': [source(p) for p in sorted(PATHS)]}


def finish():
    saved = read(OUT.stem)
    checked(saved['sources'])
    review_ref = source(OUT)
    rows, resources = [], []
    for suffix, args in [('attempt01', []), ('recheck01', ['--check'])]:
        path = DATA / ('summed_transfer_review_d151_' + suffix + '.job.json')
        row = read(path.stem)
        validate_job(row, Path(__file__).name, review_ref, args)
        rows.append(source(path))
        marks = [json.loads(s.split('|', 1)[1]) for s in Path(row['log']['path']).read_text().splitlines()
                 if s.startswith('D151_REVIEW_RESOURCES|')]
        assert len(marks) == 1
        resources.append({'receipt_wall_seconds': row['wall_seconds'], **marks[0]})
    docs = ['HANDOFF.md', 'CLAUDE.md', 'README.md', 'DECISIONS.md', 'REFERENCES.md',
            'dembele/README.md', 'dembele/pari/README.md']
    links = []
    for name in docs:
        path = ROOT / name
        block = path.read_text().split('<!-- D151 summed transfer checkpoint -->', 1)[1].split('<!-- End D151 summed transfer checkpoint -->', 1)[0]
        assert all(s in block for s in ['15237', '623', '240', '288', 'source 632 is next unused'])
        assert 'discontinuous' in block and 'parked' in block
        links.extend(local_links(path, block, (COMPLETION,)))
    assert len(links) == 28
    local_links(REPORT, REPORT.read_text(), (COMPLETION,))
    result = {k: v for k, v in saved.items() if k not in ['sources', 'wall_seconds', 'peak_rss_bytes']}
    result.update({'completed_at': datetime.now(timezone.utc).isoformat(), 'fixed_review': review_ref,
                   'report': source(REPORT), 'source_applicability_ledger': source(LEDGER),
                   'review_receipts': rows, 'review_resources': resources,
                   'successful_bounded_jobs': 5, 'input_bounded_jobs': 2, 'review_bounded_jobs': 2,
                   'completion_bounded_jobs': 1, 'failed_bounded_jobs': 0,
                   'completion_job_receipt_path': str(DATA / 'summed_transfer_completion_d151_attempt01.job.json'),
                   'entry_documents_updated': docs, 'current_artifact_links_checked': len(links),
                   'direct_source_bindings': len(saved['sources']), 'next_unused_source': 632,
                   'entry_document_hashes_intentionally_not_frozen': True,
                   'all_D151_jobs_sequential': True})
    with COMPLETION.open('x') as out:
        out.write(json.dumps(result, indent=2) + '\n')
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
        saved['wall_seconds'] = time.monotonic() - tick
        saved['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
        assert saved['peak_rss_bytes'] < 2 * (1 << 30)
        with OUT.open('x') as out:
            out.write(json.dumps(saved, indent=2) + '\n')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    assert peak < 2 * (1 << 30)
    print('D151_REVIEW_RESOURCES|' + json.dumps({'seconds': time.monotonic()-tick, 'peak_rss_bytes': peak}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(output)), flush=True)
    print('PASS|631_SUMMED_TRANSFER_REVIEW', flush=True)

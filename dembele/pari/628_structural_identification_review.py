"""D150 fixed review, transitive replay, source ledger and completion."""
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
REPORT = ROOT / 'dembele/certificates/structural-identification-audit-d150.md'
OUT = DATA / 'structural_identification_review_d150.json'
LEDGER = DATA / 'structural_identification_sources_d150.json'
COMPLETION = DATA / 'structural_identification_completion_d150.json'
HELPER = ROOT / 'dembele/pari/625_P1600_primitive_frame_review.py'
PATHS = {Path(__file__), HELPER}


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


prior = module(HELPER, 'd150_inherited_provenance')


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
    p = DATA / 'P1600_primitive_frame_review_d149.json'
    parent = read(p.stem)
    assert parent['independent_finite_review_complete']
    checked(parent['sources'])
    assert len(parent['sources']) == 38
    inherited = prior.graph(parent['inherited_review'])
    assert parent['best_current_proved_relation_height_upper'] == 15237
    assert not parent['candidate_identification_proved']
    return {'D149_direct_bindings': 38, **inherited}


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
    packets = []
    receipts = []
    for stem, driver in [
        ('structural_identification_audit_d150', '626_structural_identification_audit.py'),
        ('structural_transfer_controls_d150', '627_structural_transfer_controls.py'),
    ]:
        packet = read(stem)
        checked(packet['sources'])
        row = read(stem + '_attempt01.job')
        validate_job(row, driver, source(DATA / (stem + '.json')))
        assert packet['peak_rss_bytes'] < 2 * (1 << 30)
        # Replay the finite calculations without invoking either file's main
        # or writing any completed output again.
        code = ROOT / 'dembele/pari' / driver
        ast.parse(code.read_text())
        replay = module(code, 'd150_replay_' + driver[:3]).calculate()
        assert all(packet[k] == v for k, v in replay.items())
        receipts.append({'receipt': source(DATA / (stem + '_attempt01.job.json')),
                         'wall_seconds': row['wall_seconds'],
                         'peak_rss_bytes': packet['peak_rss_bytes']})
        packets.append(packet)
    first, second = packets
    assert first['strict_contracting_branches'] == second['branches_checked'] == 348
    assert first['distinct_target_nonaffine_branch_count'] == second['distinct_target_nonaffine_branch_count'] == 275
    assert first['reachable_cycle']['cycle_determinant_valuation_pi'] == 4
    assert second['alternative_cycle_determinant_valuation_pi'] == 6
    for p in packets:
        assert not p['summed_transfer_cancellations_excluded']
        assert not p['exact_candidate_transfer_identity_constructed']
        assert not p['candidate_identification_proved']
        assert not p['new_precision_bank_admitted']
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
    print('D150_TRANSITIVE_GRAPH_PASS', flush=True)
    completion = read('P1600_primitive_frame_completion_d149')
    parent_ref = source(DATA / 'P1600_primitive_frame_review_d149.json')
    assert completion['fixed_review'] == parent_ref
    assert completion['successful_bounded_jobs'] == 5 and completion['failed_bounded_jobs'] == 0
    for i, ref in enumerate(completion['review_receipts']):
        checked([ref])
        source(ref['path'])
        validate_job(json.loads(Path(ref['path']).read_text()), HELPER.name, parent_ref,
                     [] if i == 0 else ['--check'])
    parent_finish = read('P1600_primitive_frame_completion_d149_attempt01.job')
    validate_job(parent_finish, HELPER.name,
                 source(DATA / 'P1600_primitive_frame_completion_d149.json'), ['--finish'])
    receipts = validate_inputs()
    report_links = local_links(REPORT, REPORT.read_text(), (OUT, LEDGER, COMPLETION))
    reports = sorted({p for p in report_links if p.suffix == '.md'})
    ledger = {'status': 'pass', 'milestone': 'D150',
              'scope': 'Audit the saved actual/candidate structural comparison; certify finite hypotheses for the branchwise rational-closure obstruction and state an uninstantiated summed-transfer identity criterion.',
              'external_sources': [
                  {'title': 'van Bommel, Costa, Poonen, Srinivasan, Curve equations from expansions of 1-forms at a nonrational point',
                   'url': 'https://arxiv.org/pdf/2506.14026', 'checked_on': '2026-10-09',
                   'role': 'Lemma 4.1 and Corollary 4.2 give the divisor-degree zero test assuming exact arithmetic expansions. D88 supplies the rank refinement; the paper supplies no evaluator for this datum.'},
                  {'title': 'Franc and Masdeu, Computing fundamental domains for the Bruhat-Tits tree for GL2(Qp), p-adic automorphic forms, and the canonical embedding of Shimura curves',
                   'url': 'https://arxiv.org/pdf/1201.0356', 'checked_on': '2026-10-09',
                   'role': 'Introduction and section 6.2 distinguish numerical equation recognition from proof. D113 provides the direct ramified scalar contraction; D150 pole-orbit and tensor identities are companion derivations.'}],
              'inspected_reports': [source(p) for p in reports],
              'actual_and_candidate_claims_distinguished_in_report': True,
              'branchwise_closure_obstruction_is_companion_proof': True,
              'summed_transfer_identity_is_sufficient_not_instantiated': True,
              'no_general_impossibility_of_identification_claimed': True,
              'finite_checks_do_not_mechanically_verify_geometric_proofs': True,
              'sources': [source(REPORT)]}
    assert not LEDGER.exists()
    with LEDGER.open('x') as f:
        f.write(json.dumps(ledger, indent=2) + '\n')
    source(LEDGER)
    return {'status': 'pass', 'milestone': 'D150', 'independent_finite_review_complete': True,
            'inherited_review': parent_ref, 'catalogue_graph_is_transitive': True, **inherited,
            'input_receipts': receipts, 'completed_input_jobs': 2, 'preserved_failed_input_jobs': 0,
            'structural_inventory_complete_for_named_packets': True,
            'strict_contracting_branches_checked': 348,
            'distinct_target_nonaffine_branches_checked': 275,
            'reachable_cycle_determinant_valuations_pi': [4, 6],
            'ordinary_moment_cutoff_is_not_exact': True,
            'branchwise_finite_rational_closure_excluded_by_companion_proof': True,
            'summed_transfer_cancellations_excluded': False,
            'exact_candidate_transfer_identity_constructed': False,
            'positive_exact_quadric_vanishing_proved': False,
            'candidate_identification_proved': False, 'field_polynomial_constructed': False,
            'best_current_proved_relation_height_upper': 15237, 'sufficient_height_target': 623,
            'height_bound_at_most_623_proved': False, 'height_bound_at_most_623_disproved': False,
            'actual_harmonic_precision_increased': False, 'next_precision_bank_admitted': False,
            'resource_caps_changed': False, 'full_bank_precision_pi': 1600, 'column0_precision_pi': 6400,
            'inspected_report_count': len(reports),
            'report_local_links_checked_including_pending_packet_outputs': len(report_links),
            'next_work': 'Test whether summed transfer relations and actual quaternionic symmetries yield a finite exact identity for one cleared positive-order candidate residual, or a multiplication-compatible geometric comparison. Branchwise rational closure is excluded; summed cancellations are not. No unbounded witness search or precision increase is admitted. A height alternative needs new actual-curve input.',
            'sources': [source(p) for p in sorted(PATHS)]}


def finish():
    saved = read(OUT.stem)
    checked(saved['sources'])
    review_ref = source(OUT)
    rows, resources = [], []
    for suffix, args in [('attempt01', []), ('recheck01', ['--check'])]:
        path = DATA / ('structural_identification_review_d150_' + suffix + '.job.json')
        row = read(path.stem)
        validate_job(row, Path(__file__).name, review_ref, args)
        rows.append(source(path))
        marks = [json.loads(s.split('|', 1)[1]) for s in Path(row['log']['path']).read_text().splitlines()
                 if s.startswith('D150_REVIEW_RESOURCES|')]
        assert len(marks) == 1
        resources.append({'receipt_wall_seconds': row['wall_seconds'], **marks[0]})
    docs = ['HANDOFF.md', 'CLAUDE.md', 'README.md', 'DECISIONS.md', 'REFERENCES.md',
            'dembele/README.md', 'dembele/pari/README.md']
    links = []
    for name in docs:
        path = ROOT / name
        block = path.read_text().split('<!-- D150 structural identification checkpoint -->', 1)[1].split('<!-- End D150 structural identification checkpoint -->', 1)[0]
        assert all(s in block for s in ['15237', '623', '348', '275', 'source 629 is next unused'])
        assert 'summed' in block and 'not constructed' in block
        links.extend(local_links(path, block, (COMPLETION,)))
    assert len(links) == 28
    local_links(REPORT, REPORT.read_text(), (COMPLETION,))
    result = {k: v for k, v in saved.items() if k not in ['sources', 'wall_seconds', 'peak_rss_bytes']}
    result.update({'completed_at': datetime.now(timezone.utc).isoformat(), 'fixed_review': review_ref,
                   'report': source(REPORT), 'source_applicability_ledger': source(LEDGER),
                   'review_receipts': rows, 'review_resources': resources,
                   'successful_bounded_jobs': 5, 'input_bounded_jobs': 2, 'review_bounded_jobs': 2,
                   'completion_bounded_jobs': 1, 'failed_bounded_jobs': 0,
                   'completion_job_receipt_path': str(DATA / 'structural_identification_completion_d150_attempt01.job.json'),
                   'entry_documents_updated': docs, 'current_artifact_links_checked': len(links),
                   'direct_source_bindings': len(saved['sources']), 'next_unused_source': 629,
                   'entry_document_hashes_intentionally_not_frozen': True,
                   'all_D150_jobs_sequential': True,
                   'system_wide_process_listing_unavailable_in_sandbox': True})
    with COMPLETION.open('x') as f:
        f.write(json.dumps(result, indent=2) + '\n')
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
        with OUT.open('x') as f:
            f.write(json.dumps(saved, indent=2) + '\n')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    assert peak < 2 * (1 << 30)
    print('D150_REVIEW_RESOURCES|' + json.dumps({'seconds': time.monotonic()-tick, 'peak_rss_bytes': peak}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(output)), flush=True)
    print('PASS|628_STRUCTURAL_IDENTIFICATION_REVIEW', flush=True)

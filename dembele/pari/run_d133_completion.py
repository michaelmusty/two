"""Continue D133 through audits/review, then the conditional D134 criterion.

This standard-library coordinator performs no mathematical arithmetic.
It waits for the active production lock to be released and requires a
completed, sealed column. It never resumes or launches production, raises
caps, starts a full bank, overwrites a receipt, or retries a failed job.
Only this coordinator may admit mathematical jobs after production ends.
"""
from collections import Counter, defaultdict
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
CERT = ROOT / 'dembele/certificates'
BASE = 'dyadic_staged_P6400_col00_d133'
AUDIT = 'dyadic_precision6400_audit_plan_d133'
REVIEW133 = 'dyadic_precision6400_review_d133'
REVIEW134 = 'arithmetic_cover_criterion_review_d134'
INPUT134 = 'arithmetic_cover_criterion_d134'
DOCS = ('HANDOFF.md', 'DECISIONS.md', 'REFERENCES.md', 'README.md',
        'CLAUDE.md', 'dembele/README.md', 'dembele/pari/README.md')


def source(path):
    path = Path(path).resolve()
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while raw := stream.read(1 << 20):
            h.update(raw)
    return {'path': str(path), 'sha256': h.hexdigest()}


def read(stem):
    packet = json.loads((DATA / (stem + '.json')).read_text())
    assert packet['status'] == 'pass', stem
    return packet


def put(path, text):
    """Create once, or accept identical content during a safe resumption."""
    if path.exists():
        assert path.read_text() == text, ('inspect existing artifact', str(path))
    else:
        with path.open('x') as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())


def put_json(stem, packet):
    put(DATA / (stem + '.json'), json.dumps(packet, indent=2) + '\n')


def passing(receipt, command=None):
    packet = json.loads(receipt.read_text())
    assert packet['status'] == 'pass' and packet['exit_code'] == 0, str(receipt)
    assert packet['timeout_seconds'] == 180 and packet['timeout_terminates_process_group']
    if command is not None:
        assert packet['command'] == command
    assert source(packet['driver']['path']) == packet['driver']
    assert source(packet['log']['path']) == packet['log']
    return packet


def capped(driver, stem, marker, extra=()):
    receipt = DATA / (stem + '.job.json')
    command = ['python3', str(ROOT / driver), *extra]
    if not receipt.exists():
        assert not (DATA / (stem + '.log')).exists(), ('inspect interrupted attempt', stem)
        print('CONTINUATION_START|' + stem, flush=True)
        result = subprocess.run(['python3', 'dembele/pari/run_dyadic_capped.py',
                                 driver, stem, marker, *extra], cwd=ROOT,
                                capture_output=True, text=True)
        if result.returncode:
            print(result.stdout + result.stderr, flush=True)
            raise RuntimeError('bounded job failed: ' + stem)
    packet = passing(receipt, command)
    print('CONTINUATION_PASS|' + stem, flush=True)
    return packet


def wait_for_production():
    lock = (DATA / (BASE + '.lock')).open('a+b')
    previous = None
    while True:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except BlockingIOError:
            completed = sorted(DATA.glob(BASE + '_sweep_finish_[0-9][0-9][0-9].json'))
            last = completed[-1].stem if completed else 'initialization'
            if last != previous:
                print('CONTINUATION_WAIT|' + last, flush=True)
                previous = last
            time.sleep(15)
    actual = read(BASE + '_completed')
    assert actual['all_phases_complete'] and actual['maximum_workers'] == 3
    assert (DATA / 'dyadic_rowjournal_P6400_col00_d132/SEALED.json').is_file()
    # Retain the lock until the continuation has finished. All production
    # worker pools have drained before its original owner releases it.
    return lock


def audit():
    if not (DATA / (AUDIT + '_completed.json')).exists():
        print('CONTINUATION_START|D133_independent_audits', flush=True)
        subprocess.run(['python3', 'dembele/pari/run_d133_audits.py',
                        '--plan', AUDIT, '--workers', '3'], cwd=ROOT, check=True)
    summary = read(AUDIT + '_completed')
    assert summary['completed_jobs'] == 24 and summary['worker_limit'] == 3
    assert summary['plan'] == source(DATA / (AUDIT + '.json'))
    assert summary['coordinator'] == source(ROOT / 'dembele/pari/run_d133_audits.py')


def prepare_d133_documents():
    actual, audit_summary = read(BASE + '_completed'), read(AUDIT + '_completed')
    assert actual['completed_jobs'] == 24456 and len(actual['metadata_archives']) == 97
    items = actual['jobs'] + actual['metadata_archives'] + audit_summary['jobs']
    assert len(items) == 24577
    records, durations, peaks = [], [], []
    timings = defaultdict(list)
    for item in items:
        record = item['receipt']
        assert source(record['path']) == record
        row = passing(Path(record['path']))
        records.append(record)
        durations.append(row['wall_seconds'])
        metadata = json.loads(Path(item['metadata']['path']).read_text())
        assert source(item['metadata']['path']) == item['metadata']
        assert metadata['status'] == 'pass'
        if 'peak_rss_bytes' in metadata:
            peaks.append(metadata['peak_rss_bytes'])
        if 'request' in metadata:
            timings[metadata['request']['phase']].append(row['wall_seconds'])
    assert len({row['path'] for row in records}) == len(records)
    assert max(durations) <= 180 and max(peaks) <= 2 * (1 << 30)
    observed = {str(path.resolve()) for path in DATA.glob('*d133*_attempt*.job.json')
                if not path.name.startswith(REVIEW133)}
    assert observed == {row['path'] for row in records}, 'unexpected D133 input receipt'
    ledger = {
        'status': 'pass', 'milestone': 'D133',
        'execution_status': 'actual_column_and_audits_complete_pending_fixed_review',
        'source_numbers': [556, 557], 'passing_input_jobs': len(items), 'failed_bounded_jobs': 0,
        'actual_phases': 24456, 'metadata_archive_jobs': 97, 'independent_audit_jobs': 24,
        'prior_fixed_review': 'dyadic_staged_integration_review_d132.json', 'prior_hash_count': 18589,
        'sum_input_wall_seconds': sum(durations), 'maximum_input_wall_seconds': max(durations),
        'maximum_recorded_successful_arithmetic_RSS_bytes': max(peaks),
        'production_phase_timings': {key: {'jobs': len(values), 'summed_seconds': sum(values),
                                         'maximum_seconds': max(values)}
                                     for key, values in sorted(timings.items())},
        'actual_column_precisions_after_review': {'0': 6400, '1': 1600}, 'full_bank_precision_pi': 800,
        'report': 'dembele/certificates/dyadic-precision6400-d133.md',
        'actual_summary': source(DATA / (BASE + '_completed.json')),
        'audit_summary': source(DATA / (AUDIT + '_completed.json')),
        'completion_coordinator': source(Path(__file__)),
        'positive_exact_zero_proved': False, 'candidate_identification_proved': False,
        'field_polynomial_constructed': False, 'full_bank_launch_admitted': False,
        'runtime_scope': 'Complete measured one-column stage; no extrapolated bank ETA or automatic next launch.',
        'next_task': 'Review the conditional D134 cover criterion, then recost before selecting a bank schedule.'}
    put_json('dyadic_precision6400_sources_d133', ledger)
    phase_rows = '\n'.join(f'| {phase} | {len(values)} | {sum(values):.3f} | {max(values):.3f} |'
                           for phase, values in sorted(timings.items()))
    report = f'''# D133: one actual weighted P=6400 harmonic column

The actual column and its independent audits are complete. Final acceptance
requires both saved source-557 review receipts; their result is recorded in
the [completion record](../data/computed/dyadic_precision6400_completion_d133.json).
This report records the completed input evidence and is frozen by that review.

Column 0 advances from P=3200 to P=6400 after final acceptance. The full
sixteen-column bank remains P=800 and column 1 remains P=1600. No positive
exact quadric zero, candidate identification or original-kernel polynomial
is proved. P=10552 remains a conditional sufficient design.

## Execution and precise arithmetic scope

Frozen source 554 and coordinator 553 execute 24,456 phases, a seed sweep
and 96 corrections, with 97 verified metadata archives. All 176 receipts
from the planned initialization pause are reused. The seed low solve has
digits 200,400,600,800; every digit stage checks all 44,544 original low
equations. Final production checks cover all 8,908,800 original weighted
fixed-point scalars, all 174 masses, 1,740,800 CM scalars and 68 coarse values.
The coarse errors in beta valuation are [12832,12848,12832,12864].

The weighted deduction TQ=T and QT(w)=w certifies the uniform fixed point
T(w) without retaining another uniform binary. Review 557 checks the full
phase list and certificates, all generation transitions, retained full and
row hashes, retired-payload history, and archive/receipt/log bindings.
Historical overwritten payload hashes are not claims of retained files.

Source 556 supplies 24 separately capped independent audits. Complete
comparisons cover 4,454,400 old weighted coordinates, 174 masses, all final
zero residual rows, 870,400 old CM coordinates and all 68 old coarse
overlaps. Separate ordinary-arithmetic samples check 72 original state
scalars and 72 CM scalars at degrees 1,2,3; these are not a complete second
operator evaluation. Six reverse-Horner sums independently check 96 beta
scalars, at charts 0,8,16 and orders 0,3. Production arithmetic is not
imported by these independent checks.

## Resources and measured complete-stage costs

All {len(items):,} input receipts pass; no failed bounded input is present.
The two final review receipts are additional to that input count.
Summed input job durations are {sum(durations):.3f} seconds, and the longest
input takes {max(durations):.3f} seconds. The largest recorded successful
arithmetic-worker peak is {max(peaks):,} bytes. The resumed production
coordinator takes {actual['wall_seconds']:.3f} seconds; the audit coordinator
takes {audit_summary['wall_seconds']:.3f}. The resumed wall interval excludes
the original initialization pause/run, although its job durations are
included once in the summed input durations.

| Production phase | Jobs | Summed seconds | Longest seconds |
|---|---:|---:|---:|
{phase_rows}

All mathematical jobs retain the 180-second private-process-group cap,
assertions and one BLAS thread. At most three workers run globally.
RAM admission uses measured peaks up to 2 GiB per successful job and a
conservative 6 GiB sum for three workers. This is not OS enforcement or a
claim about free physical RAM. The working-store inventory bound is
973,167,872 bytes, including the reserve, below the unchanged 2 GiB cap.
Review 557 checks observed storage against that bound. Permanent external
receipts/logs and inherited frozen stores are accounted separately.

The final state is ready096, epoch194, with zero residual authority
(u,count,bits)=(6368,33,4). Its weighted state has 449,407,200 bytes and
the CM payload has 174,080,000 bytes. Only authorized obsolete working
payloads and verified duplicate internal metadata retire; external records
and every prior freeze remain retained.

Frozen coordinator 553 submits the whole current group to its worker pool.
On failure that queued group may drain before it stops. No failure occurs
in these inputs. The new audit coordinator instead maintains a submission
window of at most three jobs and checks failures before adding work.

## Review, continuation and reference roles

The [ledger](../data/computed/dyadic_precision6400_sources_d133.json),
[fixed review](../data/computed/dyadic_precision6400_review_d133.json) and
completion record distinguish input completion from final acceptance.
The fixed review preserves all 18,589 D132 hashes and adds the actual
sealed store, complete receipts and independent audits.

These complete-stage timings are available for a new schedule comparison;
they are not a full-bank estimate. D130's 9--14 ideal-worker-day model is
a pre-redesign baseline. No automatic bank or next precision run follows.
The authorized continuation next reviews D134's conditional arithmetic
cover criterion. Marked-base identification, P32/B3, exact global Y or
its arithmetic sections, the combined torsion backend, global F256 action
and the original-kernel polynomial remain open.

The operator/weighted deduction, target transports and stable-lattice
inputs are inherited from D121/D130/D132. The independent integer quotient
uses source 486. No new external theorem is claimed by this precision run.
'''
    put(CERT / 'dyadic-precision6400-d133.md', report)


def review(milestone):
    if milestone == 133:
        driver, stem, marker = ('dembele/pari/557_dyadic_precision6400_review.py',
                               REVIEW133, 'PASS|557_DYADIC_PRECISION6400_REVIEW')
    else:
        driver, stem, marker = ('dembele/pari/559_arithmetic_cover_criterion_review.py',
                               REVIEW134, 'PASS|559_ARITHMETIC_COVER_CRITERION_REVIEW')
    capped(driver, stem + '_attempt01', marker)
    packet = read(stem)
    assert packet['independent_finite_review_complete']
    capped(driver, stem + '_recheck01', marker, ['--check'])
    return packet


def checkpoint_docs(milestone, packet):
    marker = f'<!-- D{milestone} reviewed continuation checkpoint -->'
    base_text = (f'D{milestone} is reviewed. The full bank remains P800; column 0 is now '
                 'certified at P6400 and column 1 at P1600. No positive exact zero, '
                 'base identification or field polynomial is proved. ')
    if milestone == 133:
        base_text += (f'All {packet["passing_input_jobs"]:,} D133 input jobs and both reviews pass. '
                      f'The fixed review binds {len(packet["sources"]):,} hashes. '
                      'The completion coordinator next runs the D134 finite replay and review; '
                      'inspect its live session and receipts before starting any other mathematical job. ')
        report = 'dyadic-precision6400-d133.md'
        completion = 'dyadic_precision6400_completion_d133.json'
    else:
        base_text += (f'The D134 replay and both reviews pass; its fixed review binds '
                      f'{len(packet["sources"]):,} hashes and preserves the D133 catalogue. '
                      'The conditional route uses the odd canonical Jacobian order to fix the '
                      'F-rational branch half, then D77 cubic inertia to fix its scalar. '
                      'The marked-base and canonical Hecke hypotheses remain essential. '
                      'The continuation coordinator has no further mathematical jobs after this checkpoint. ')
        report = 'arithmetic-twist-classification-d134.md'
        completion = 'arithmetic_cover_criterion_completion_d134.json'
    base_text += ('Re-cost the complete measured stage before selecting a full-bank schedule; '
                  'no new bank is automatically admitted. Source 560 is next unused. '
                  'All earlier next-task statements below are historical; retain every frozen artifact.')
    for name in DOCS:
        path = ROOT / name
        original = path.read_text()
        if marker in original:
            continue
        prefix = 'dembele/' if '/' not in name else '../' if name == 'dembele/pari/README.md' else ''
        note = (marker + '\n\n' + f'**Current reviewed checkpoint: D{milestone}.**\n\n' + base_text +
                f'\n\nSee the [report]({prefix}certificates/{report}) and '
                f'[completion record]({prefix}data/computed/{completion}).\n\n')
        if name == 'DECISIONS.md':
            point = original.index('*Maintenance note:')
            changed = original[:point] + note + original[point:]
        else:
            end = original.index('\n') + 1
            tail = original[end:].lstrip('\n')
            tail = tail.replace('## ACTIVE — D133 one actual P=6400 column',
                                '## Historical D133 execution checkpoint — one actual P=6400 column', 1)
            tail = tail.replace('**Current checkpoint: D132 reviewed; D133 P=6400 column active',
                                '**Historical checkpoint: D132 reviewed; D133 P=6400 column active', 1)
            tail = tail.replace('**Current reviewed checkpoint: D133.**',
                                '**Previous reviewed checkpoint: D133.**', 1)
            changed = original[:end] + '\n' + note + tail
        # Mutable entry documents only; numbered sources/reports/receipts
        # are never overwritten by this maintenance step.
        with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, prefix='.continuation-', delete=False) as stream:
            stream.write(changed)
            stream.flush()
            os.fsync(stream.fileno())
            temp = Path(stream.name)
        os.replace(temp, path)


def complete(milestone, packet):
    stem = REVIEW133 if milestone == 133 else REVIEW134
    target = 'dyadic_precision6400_completion_d133' if milestone == 133 else 'arithmetic_cover_criterion_completion_d134'
    report = 'dyadic-precision6400-d133.md' if milestone == 133 else 'arithmetic-twist-classification-d134.md'
    ledger = 'dyadic_precision6400_sources_d133' if milestone == 133 else 'arithmetic_cover_criterion_sources_d134'
    checkpoint_docs(milestone, packet)
    result = {
        'status': 'pass', 'milestone': f'D{milestone}',
        'fixed_review': source(DATA / (stem + '.json')), 'fixed_review_source_count': len(packet['sources']),
        'review_receipts': [source(DATA / (stem + suffix + '.job.json')) for suffix in ('_attempt01', '_recheck01')],
        'passing_input_jobs': packet['passing_input_jobs'], 'passing_review_jobs': 2,
        'total_passing_jobs': packet['passing_input_jobs'] + 2, 'failed_bounded_jobs': 0,
        'full_bank_precision_pi': 800, 'actual_column_precisions': {'0': 6400, '1': 1600},
        'positive_exact_zero_proved': False, 'candidate_identification_proved': False,
        'arithmetic_cover_identification_proved': False, 'field_polynomial_constructed': False,
        'full_bank_launch_admitted': False, 'next_unused_source': 560,
        'entry_documents_updated': list(DOCS), 'documentation_updated': True,
        'frozen_report_sources': [source(CERT / report), source(DATA / (ledger + '.json'))],
        'completion_coordinator': source(Path(__file__)),
        'next_task': ('Review conditional D134 cover criterion; retain global three-worker limit.' if milestone == 133
                      else 'Recost the full-bank schedule from the completed D133 stage; marked-base and Y construction remain open.')}
    put_json(target, result)
    print('CONTINUATION_COMPLETED|' + target, flush=True)


def d134():
    capped('dembele/pari/558_arithmetic_cover_criterion.py', INPUT134 + '_attempt01',
           'PASS|558_ARITHMETIC_COVER_CRITERION', ['--output', INPUT134])
    packet = read(INPUT134)
    receipt = passing(DATA / (INPUT134 + '_attempt01.job.json'))
    assert packet['peak_rss_bytes'] <= 2 * (1 << 30)
    prior = read(REVIEW133)
    ledger = {
        'status': 'pass', 'milestone': 'D134', 'execution_status': 'finite_replay_complete_pending_fixed_review',
        'source_numbers': [558, 559], 'passing_input_jobs': 1, 'failed_bounded_jobs': 0,
        'prior_fixed_review': REVIEW133 + '.json', 'prior_hash_count': len(prior['sources']),
        'input': source(DATA / (INPUT134 + '.json')),
        'input_receipt': source(DATA / (INPUT134 + '_attempt01.job.json')),
        'input_wall_seconds': receipt['wall_seconds'], 'input_peak_rss_bytes': packet['peak_rss_bytes'],
        'canonical_Hecke_order_P16_at32': packet['canonical_Hecke_order_P16_at32'],
        'conditional_rational_branch_half_uniqueness': True, 'D77_conditional_scalar_twist_uniqueness_restored': True,
        'marked_base_and_canonical_Hecke_hypotheses_remain_required': True,
        'report': 'dembele/certificates/arithmetic-twist-classification-d134.md',
        'actual_marked_base_identified': False, 'actual_arithmetic_cover_identified': False,
        'full_bank_precision_pi': 800, 'actual_column_precisions': {'0': 6400, '1': 1600},
        'positive_exact_zero_proved': False, 'field_polynomial_constructed': False,
        'reference_roles': packet['references'],
        'freeze': '558/559, passing replay/review bindings and merged D77 catalogue, preserving all D133 hashes.'}
    put_json('arithmetic_cover_criterion_sources_d134', ledger)
    complete(134, review(134))


def main():
    with (DATA / 'dyadic_precision6400_completion_d133.lock').open('a+b') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        production_lock = wait_for_production()
        try:
            audit()
            prepare_d133_documents()
            complete(133, review(133))
            d134()
        finally:
            production_lock.close()
    print('CONTINUATION_DONE|D133_and_D134_reviewed_no_bank_launch', flush=True)


if __name__ == '__main__':
    main()

"""D157 regression controls for the two D156 reviewer checkpoint guards.

Malformed packets below are in-memory fixtures. All real artifacts remain
unchanged, including the failed source-647 attempt and its source snapshot.
"""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
CONFIG='dyadic_staged_P6400_col02_config_d156'
OLD=ROOT/'dembele/pari/647_dyadic_higher_pilot_column_review.py'
NEW=ROOT/'dembele/pari/651_dyadic_higher_pilot_column_review_revision.py'
OUT=DATA/'dyadic_higher_pilot_review_controls_d157.json'

def main():
    assert __debug__ and not OUT.exists();tick=time.monotonic()
    spec=importlib.util.spec_from_file_location('revised_review',NEW)
    r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
    r.PATHS.add(Path(__file__))
    text=OLD.read_text()
    changes=[
        ('D156 incremental higher-stage pilot review; indexed archive and weighted seed audit support.',
         'D157 revision of the D156 higher-stage pilot review; checkpoint guards corrected.'),
        ("if EXECUTION == 'D153':", "if EXECUTION in ('D153', 'D156'):"),
        ("packet['execution_milestone'] == 'D153'", "packet['execution_milestone'] == EXECUTION"),
        ('PASS|647_DYADIC_HIGHER_PILOT_COLUMN_REVIEW',
         'PASS|651_DYADIC_HIGHER_PILOT_COLUMN_REVIEW_REVISION')]
    for before,after in changes:
        assert text.count(before)==(2 if before.startswith('PASS|') else 1)
        text=text.replace(before,after)
    assert NEW.read_text()==text
    r.source(OLD);r.source(NEW)
    failed_path=DATA/'dyadic_higher_pilot_col02_review_d156_attempt01.job.json'
    failed=json.loads(failed_path.read_text());r.source(failed_path)
    assert failed['status']=='failed' and failed['exit_code']==1
    assert failed['timeout_seconds']==180 and failed['timeout_terminates_process_group']
    r.checked([failed['driver'],failed['failed_driver_snapshot'],failed['log']]+failed['sources'])
    assert failed['driver']==r.source(OLD)
    assert failed['failed_driver_snapshot']['sha256']==failed['driver']['sha256']
    assert "assert packet['execution_milestone'] == 'D153' and packet['weighted_seed_supported']" in Path(failed['log']['path']).read_text()
    r.configure(CONFIG);assert r.EXECUTION=='D156'
    paths,cert=r.audit_review();assert len(paths)==24
    original_receipt=r.receipt
    rejected=[]
    def reject_audit(label,mutate):
        def fixture_receipt(*args):
            row,packet=original_receipt(*args)
            packet=copy.deepcopy(packet);mutate(packet)
            return row,packet
        r.receipt=fixture_receipt
        try:
            r.audit_review()
        except (AssertionError,KeyError):
            rejected.append(label)
        else:
            raise AssertionError('accepted malformed audit fixture: '+label)
        finally:
            r.receipt=original_receipt
    reject_audit('previous_execution_label',lambda p:p.update(execution_milestone='D153'))
    reject_audit('unknown_execution_label',lambda p:p.update(execution_milestone='D999'))
    reject_audit('missing_execution_label',lambda p:p.pop('execution_milestone'))
    reject_audit('unsupported_weighted_seed',lambda p:p.update(weighted_seed_supported=False))
    # Execute the exact indexed-summary guard extracted from the production
    # review. It must run for the D156 path, not just the earlier D153 path.
    tree=ast.parse(NEW.read_text())
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='execution_review')
    guards=[n for n in function.body if isinstance(n,ast.If) and 'EXECUTION' in ast.unparse(n.test)]
    assert len(guards)==1
    guard=compile(ast.Module(body=guards,type_ignores=[]),str(NEW),'exec')
    summary=r.read(r.BASE+'_completed')
    def run_guard(value,execution='D156'):
        exec(guard,{'EXECUTION':execution,'summary':value,'source':r.source,'ROOT':ROOT})
    run_guard(summary);run_guard(summary,'D153')
    for label,mutate in [
        ('wrong_indexed_summary_milestone',lambda s:s.update(milestone='D137')),
        ('unreconciled_receipt_inventory',lambda s:s['receipt_inventory'].update(reconciled=False)),
        ('wrong_receipt_lookup_source',lambda s:s['receipt_inventory']['source'].update(sha256='0'*64))]:
        fixture=copy.deepcopy(summary);mutate(fixture)
        try:run_guard(fixture)
        except AssertionError:rejected.append(label)
        else:raise AssertionError('accepted malformed indexed-summary fixture: '+label)
    assert len(rejected)==7
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    assert peak<=2*(1<<30)
    result={'status':'pass','milestone':'D157','config':r.source(DATA/(CONFIG+'.json')),
        'previous_reviewer':r.source(OLD),'revised_reviewer':r.source(NEW),
        'only_two_guard_changes_plus_docstring_and_pass_markers':True,
        'production_and_audit_arithmetic_unchanged':True,
        'complete_actual_D156_audits_accepted':24,'actual_audit_certificate':cert,
        'indexed_summary_guard_accepts_actual_D156_and_D153_schema':True,
        'malformed_in_memory_fixtures_rejected':rejected,
        'failed_review_receipt':r.source(failed_path),'failed_attempt_and_snapshot_preserved':True,
        'no_production_or_audit_jobs_rerun':True,'no_other_column_admitted':True,
        'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':peak,
        'sources':[r.source(p) for p in sorted(r.PATHS)]}
    with OUT.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(r.source(OUT)),flush=True)
    print('PASS|652_DYADIC_HIGHER_PILOT_REVIEW_CONTROLS',flush=True)

if __name__=='__main__':main()

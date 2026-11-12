"""D153 bounded weighted-seed, archive-format, schedule and known-answer controls.

Synthetic extension/archive fixtures are not new actual harmonic data.
"""
import ast
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
CONFIG='dyadic_staged_P3200_col02_config_d153'
OUT=DATA/'dyadic_pilot_controls_d153.json'
PATHS={Path(__file__)};CACHE={}

def source(path):
    p=Path(path).resolve();PATHS.add(p)
    if p not in CACHE:
        h=hashlib.sha256()
        with p.open('rb') as f:
            while raw:=f.read(1<<20):h.update(raw)
        CACHE[p]={'path':str(p),'sha256':h.hexdigest()}
    return CACHE[p]

def read(stem):
    p=DATA/(stem+'.json');source(p);v=json.loads(p.read_text());assert v['status']=='pass';return v

def module(name):
    p=ROOT/'dembele/pari'/name;source(p)
    s=importlib.util.spec_from_file_location('d153_control_'+name[:3],p)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def reject(fn):
    try:fn()
    except (AssertionError,KeyError,ValueError):return
    raise AssertionError('corrupt or unsupported fixture was accepted')

def ast_controls():
    def functions(name):
        p=ROOT/'dembele/pari'/name;source(p)
        return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_text()).body
                if isinstance(n,ast.FunctionDef)}
    old,new=functions('564_dyadic_checkpoint_independent.py'),functions('635_dyadic_pilot_independent.py')
    names=['decode','stored','recurrence','ordinary_state','cm_rows','ordinary_cm','coarse_horner','current']
    assert all(old[n]==new[n] for n in names)
    before,after=functions('568_dyadic_checkpoint_column_review.py'),functions('636_dyadic_pilot_column_review.py')
    preserved=['expected_groups','receipt','phase_certificate','full_file','envelope']
    assert all(before[n]==after[n] for n in preserved)
    return {'unchanged_independent_arithmetic_functions':names,'unchanged_review_core_functions':preserved}

def weighted_controls():
    audit=module('635_dyadic_pilot_independent.py')
    engine=module('554_dyadic_resumable_staged_production.py')
    cfg=read(CONFIG);seal=read(cfg['seed']);ref=seal['state_file'];assert source(ref['path'])==ref
    inputs=json.loads((DATA/cfg['namespace']/'INPUTS.json').read_text())['value']
    # The immutable seed is in the reviewed D138 graph. Compare the new
    # independent byte decoder to the existing native reader on actual rows.
    manifest=inputs['seed'];assert manifest['weighted'] and manifest['count']==1600
    native=engine.v.Reader(manifest);rows={}
    for e in (0,83,173):
        rows[e]=audit.reference(ref,e,1600,200,True)
        assert rows[e]==[tuple(row) for row in native.row(e)]
    native.close()
    def pack(values,P,weighted):
        out=bytearray()
        for k,row in enumerate(values):
            for i,value in enumerate(row):
                # Count allowed binary exponents by their pi valuation,
                # independently of the decoder's ceiling formula.
                bit=P//8 if not weighted or k<=32 else len(range(i,max(i,P-k),8))
                assert 0<=value<1<<bit
                out.extend(value.to_bytes((bit+7)//8,'little'))
        return bytes(out)
    rejected=0
    with tempfile.TemporaryDirectory(prefix='d153_weighted_') as tmp:
        folder=Path(tmp)
        for e,row in rows.items():
            raw=pack(row,1600,True)
            assert hashlib.sha256(raw).hexdigest()==manifest['row_sha256'][e]
            uniform=pack(row,1600,False);p=folder/f'uniform{e}.bin';p.write_bytes(uniform)
            assert audit.reference(audit.source(p),0,1600,200)==row
            assert audit.decode(raw,1600,200,True)==row
            reject(lambda:audit.decode(raw[:-1],1600,200,True));rejected+=1
        bad=bytearray(pack(rows[0],1600,True));bad[-1]=255
        reject(lambda:audit.decode(bad,1600,200,True));rejected+=1
        reject(lambda:audit.reference(ref|{'sha256':'0'*64},0,1600,200,True));rejected+=1
        reject(lambda:audit.reference(ref,173,1600,200,False));rejected+=1
        # Exercise the entire changed states() overlap path on a clearly
        # synthetic lift, including the packed tail and both seed formats.
        audit.P=3200;audit.S=1600;audit.K=400;audit.SK=200;audit.COLUMN=2;audit.STORE=folder
        harmonic=read('dyadic_harmonic_certificate_d111');row=list(rows[0])+[(0,)*8]*1600
        row[0]=(harmonic['harmonic_basis'][2][0]%(1<<400),)+(0,)*7
        def write_state(values):
            raw=pack(values,3200,True);(folder/'synthetic_state.bin').write_bytes(raw)
            return {'name':'synthetic_state.bin','bytes':len(raw),'row_bytes':len(raw),
                    'row_sha256':[hashlib.sha256(raw).hexdigest()]}
        zeros=bytes(33*8);(folder/'synthetic_residual.bin').write_bytes(zeros)
        cur={'state':write_state(row),'aux':{'name':'synthetic_residual.bin','bytes':len(zeros),
                'row_bytes':len(zeros),'row_sha256':[hashlib.sha256(zeros).hexdigest()]},'authority':{'bits':1}}
        audit.current=lambda:cur
        audit.read=lambda stem:harmonic if stem=='dyadic_harmonic_certificate_d111' else None
        fixture={'seed':{'payload':ref,'count':1600,'weighted':True}}
        audit.env=lambda name:fixture
        good=audit.states(0,0);assert good['complete_old_weighted_overlap_scalars']==12800
        fixture['seed']={'payload':audit.source(folder/'uniform0.bin'),'count':1600,'weighted':False}
        assert audit.states(0,0)==good
        fixture['seed']={'payload':ref,'count':1600,'weighted':True}
        changed=list(row);v=list(changed[100]);v[0]^=1;changed[100]=tuple(v);cur['state']=write_state(changed)
        reject(lambda:audit.states(0,0));rejected+=1
        cur['state']=write_state(row);fixture['seed']['weighted']='true'
        reject(lambda:audit.states(0,0));rejected+=1
    return {'actual_weighted_seed_rows_compared_to_native_reader':[0,83,173],
            'synthetic_weighted_and_uniform_old_overlap_paths_pass':True,
            'wrong_overlap_flag_digest_length_and_top_bits_rejected':rejected,
            'actual_new_moments_computed':False}

def archive_controls():
    review=module('636_dyadic_pilot_column_review.py')
    review.configure('dyadic_staged_P1600_col02_config_r2_d137')
    original=review.STORE;expected=read('dyadic_checkpoint_col02_review_r2_d137')['certificates']['store']
    archiver=ROOT/'dembele/pari/577_dyadic_indexed_metadata_archive.py';source(archiver)
    with tempfile.TemporaryDirectory(prefix='d153_archive_') as tmp:
        folder=Path(tmp);archives=[]
        for p in original.iterdir():
            q=folder/p.name
            if p.name.startswith('archive_') and p.suffix=='.json':
                obj=json.loads(p.read_text());obj['value']['source']=review.source(archiver)
                obj['sha256']=hashlib.sha256(review.canonical(obj['value'])).hexdigest()
                q.write_bytes(review.canonical(obj));archives.append(q)
            else:q.symlink_to(p)
        review.STORE=folder;review.ARCHIVER=archiver
        history,archived,store=review.inspect_store()
        assert len(archives)==25 and store['archived_duplicate_records']==expected['archived_duplicate_records']
        assert store['retained_payload_bytes']==expected['retained_payload_bytes']
        q=archives[0];obj=json.loads(q.read_text())
        obj['value']['source']=review.source(ROOT/'dembele/pari/551_dyadic_staged_metadata_archive.py')
        obj['sha256']=hashlib.sha256(review.canonical(obj['value'])).hexdigest();q.write_bytes(review.canonical(obj))
        reject(review.inspect_store)
    return {'synthetic_indexed_archive_store_accepted':True,'wrong_archiver_source_rejected':True,
            'retained_external_archive_records_checked':len(archived),'old_sealed_store_never_written':True}

def calculate():
    cfg=read(CONFIG);setup=read('dyadic_pilot_setup_d153')
    review=module('636_dyadic_pilot_column_review.py');review.configure(CONFIG)
    prod=module('run_d139_indexed_production.py');groups=list(prod.schedule(cfg))
    assert groups==list(review.expected_groups())
    specs=[x for group in groups for x in group];counts=Counter(x['phase'] for x in specs)
    assert len(specs)==12495 and counts['sweep-finish']==49 and len({x['key'] for x in specs})==len(specs)
    assert tuple(p.name if isinstance(p,Path) else p for p in review.execution_paths(3200,1600,2))==(
        'D153','run_d139_indexed_production.py','577_dyadic_indexed_metadata_archive.py','635_dyadic_pilot_independent.py')
    reject(lambda:review.execution_paths(3200,1600,1))
    inv=module('567_dyadic_checkpoint_admission_revision.py').inventory(3200,1600)
    assert inv==setup['inventory'] and inv['maximum_bound']['total_bytes']==304049792
    pairs=[('states','states_e000_028'),('cm','cm_c00_02'),('ordinary_state','ordinary_state_e083'),
           ('ordinary_cm','ordinary_cm_c08'),('horner','horner_c16_o3')]
    for name,old in pairs:
        new=read('dyadic_pilot_'+name+'_control_d153');prior=read('dyadic_precision6400_'+old+'_d133')
        assert new['certificates']==prior['certificates'] and new['production_arithmetic_not_imported']
    oldreview=read('dyadic_pilot_review_control_d153')
    assert oldreview['known_completed_schedule_and_store_match'] and oldreview['passing_production_and_archive_receipts']==24553
    plan=read(cfg['audit_plan']);oldplan=read('dyadic_precision6400_audit_plan_d133')
    assert len(plan['jobs'])==24
    for spec,old in zip(plan['jobs'],oldplan['jobs']):
        assert spec['args']==old['args']+['--config',CONFIG]
        assert spec['driver']=='dembele/pari/635_dyadic_pilot_independent.py'
        assert spec['marker']=='PASS|635_DYADIC_PILOT_INDEPENDENT'
    lookup=read('dyadic_receipt_lookup_controls_d139');archives=read('dyadic_indexed_archive_controls_d139')
    assert archives['certificates']['both_interruption_points_resume_idempotently']
    return {'status':'pass','milestone':'D153','production_jobs':len(specs),'phase_counts':dict(counts),
            'archive_jobs':49,'audit_jobs':24,'column_review_jobs':2,'total_pilot_jobs':12570,
            'schedule_matches_independent_review':True,'working_store_bound_bytes':304049792,
            'known_answer_arithmetic_phases':5,'known_complete_column_receipts':24553,
            'immutable_D139_lookup_and_interruption_controls_reused':True,
            **ast_controls(),**weighted_controls(),**archive_controls()}

if __name__=='__main__':
    assert __debug__ and not OUT.exists();tick=time.monotonic();result=calculate()
    result.update(wall_seconds=time.monotonic()-tick,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
        sources=[source(p) for p in sorted(PATHS)])
    assert result['peak_rss_bytes']<=2*(1<<30)
    with OUT.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(OUT)),flush=True)
    print('PASS|638_DYADIC_PILOT_CONTROLS',flush=True)

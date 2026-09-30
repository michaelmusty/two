"""D131 integrate a full actual r=32 correction with the new row journal.

Recompute the first frozen P=1600 column-0 correction from u=800 to833.
RHS, low solve and original sparse checks are fresh; GMP operator chunks
write their freshly calculated residual rows into the reserved store.
All reference data remain read-only; this is a protocol/arithmetic control,
not a new precision stage. Run phases via the unchanged capped wrapper.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
def module(name,file):
    s=importlib.util.spec_from_file_location(name,ROOT/'dembele/pari'/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
j=module('journal','543_dyadic_row_journal.py')
v=module('weighted','541_dyadic_weighted_certificate.py')
b,l,p,c=v.b,v.l,v.p,v.w.c
STORE=DATA/'dyadic_rowjournal_arithmetic_d131'
P,N,R,SHIFT,COUNT,NEXT,NEWSHIFT=1600,174,32,100,800,767,104
PATHS={Path(__file__),Path(j.__file__),Path(v.__file__),Path(c.__file__),Path(b.__file__),Path(l.__file__),Path(p.__file__)}
CACHE={}


def source(path):
    path=Path(path).resolve();PATHS.add(path)
    if path not in CACHE:
        sha=hashlib.sha256()
        with path.open('rb') as f:
            while raw:=f.read(1<<20):sha.update(raw)
        CACHE[path]={'path':str(path),'sha256':sha.hexdigest()}
    return CACHE[path]


# Replace only this new process's hash callback; frozen module files stay
# unchanged. FactorReader's large payload authentication now also streams.
c.h.source=source


def read(stem):
    path=DATA/(stem+'.json');PATHS.add(path);d=json.loads(path.read_text());assert d['status']=='pass';return d


def reference(record,e,width):
    with Path(record['path']).open('rb') as f:f.seek(e*width);raw=f.read(width)
    assert len(raw)==width;return raw


def chunks(record,width):
    with Path(record['path']).open('rb') as f:
        for _ in range(N):
            raw=f.read(width);assert len(raw)==width;yield raw
        assert not f.read(1)


def decode(raw,count,bits,weighted=False):
    if not weighted:return b.unpack(raw,1,count,bits)[0]
    out=[];at=0
    for bs in v.layout(count,bits,True):
        row=[]
        for bit in bs:
            width=(bit+7)//8;value=int.from_bytes(raw[at:at+width],'little');at+=width;assert value<1<<bit;row.append(value)
        out.append(tuple(row))
    assert at==len(raw);return out


def init():
    prior=read('dyadic_target_feasibility_review_d130');known={x['path']:x['sha256'] for x in prior['sources']}
    old=read('dyadic_weighted_P1600_col00_seed_d124');prep=read('dyadic_weighted_P1600_col00_step01_prepared_d124');after=read('dyadic_weighted_P1600_col00_step01_d124')
    refs={'state':old['state_file'],'residual':old['residual_file'],'prepared_state':prep['state_file'],
          'correction':prep['operator_input_file'],'new_residual':after['residual_file']}
    for record in refs.values():assert known[record['path']]==record['sha256'] and source(record['path'])==record
    sw=Path(refs['state']['path']).stat().st_size//N
    store=j.Store(STORE,create=True);store._put('CONTROL.json',{'references':refs,'state_width':sw})
    store.initialize(N,sw,COUNT*8*13,chunks(refs['state'],sw),chunks(refs['residual'],COUNT*8*13),
                     {'actual_frozen_seed_metadata':source(DATA/'dyadic_weighted_P1600_col00_seed_d124.json')})
    return {'initialized_actual_states':N,'copied_reference_payload_bytes':N*(sw+COUNT*8*13),
            'prospectively_transient_generation':store.current(),'peak_observed_logical_scratch_bytes':store.peak}


def params():
    packet=read('dyadic_target_transports_d121');out=[]
    for edge in packet['transitions']:
        children=[]
        for child in edge['children']:
            assert child['normalized_error_pi']>=P
            children.append((child['target_edge'],tuple(tuple(int(x)&((1<<100)-1) for x in row) for row in child['normalized_center'][:3])))
        out.append(children)
    return out


def prepare():
    store=j.Store(STORE);initial=store.current();assert initial['tag']=='initial'
    control=store._get('CONTROL.json');refs=control['references'];sw=control['state_width']
    for key in ('prepared_state','correction'):assert source(refs[key]['path'])==refs[key]
    ring=p.Ring(100);parameters=params();rhs=[];tick=time.monotonic()
    for e in range(N):
        total=[b.ZERO]*33
        for child,pars in parameters[e]:
            values=decode(store.read_row('aux',child,'initial'),COUNT,100)
            assert values[:33]==[b.ZERO]*33
            plan=l.Plan(ring,*pars,COUNT,33);total=ring.padd(total,plan.apply(values));del plan
        assert total[0]==b.ZERO;rhs.append([[x] for x in total[1:]])
    rhs_seconds=time.monotonic()-tick;tick=time.monotonic()
    factor=c.FactorReader(100);algebra=b.Algebra(100);answer=factor.solve(rhs,algebra)
    assert factor.decoded_blocks==1226;factor.close();solve_seconds=time.monotonic()-tick
    groups={}
    for e,children in enumerate(parameters):
        for child,pars in children:groups.setdefault(pars,[]).append((e,child))
    applied=list(answer);tick=time.monotonic()
    for pars,dests in groups.items():
        block=b.coefficients(pars,R,algebra)
        for e,child in dests:applied[e]=algebra.sub(applied[e],algebra.mul(block,answer[child]))
        del block
    assert applied==rhs;check_seconds=time.monotonic()-tick
    store.begin_prepare('prepared',{'low_equations_checked':N*R*8,'source':source(Path(__file__))})
    for e in range(N):
        values=decode(store._readrow(initial['aux'],e),COUNT,100)
        values[1:33]=[x[0] for x in answer[e]]
        correction=b.pack([values],100);assert correction==reference(refs['correction'],e,COUNT*8*13)
        state=decode(store._readrow(initial['state'],e),P,200,True)
        for k in range(COUNT):state[k]=tuple(x+(d<<SHIFT) for x,d in zip(state[k],values[k]))
        raw=v.encode(state,v.layout(P,200,True));assert raw==reference(refs['prepared_state'],e,sw)
        store.prepare_row(e,raw,correction)
    current=store.finish_prepare()
    assert current['state']['sha256']==refs['prepared_state']['sha256'] and current['aux']['sha256']==refs['correction']['sha256']
    PATHS.update(c.h.PATHS)
    return {'original_RHS_child_actions':348,'factor_blocks_decoded':1226,'original_sparse_low_equation_scalars':44544,
            'complete_prepared_weighted_scalar_comparisons':N*P*8,'complete_correction_scalar_comparisons':N*COUNT*8,
            'RHS_seconds':rhs_seconds,'factor_solve_seconds':solve_seconds,'original_sparse_check_seconds':check_seconds,
            'all_low_equations_zero':True,'prospectively_transient_generation':current,
            'peak_observed_logical_scratch_bytes':store.peak,'factor_authentication_streams':True}


def begin():
    store=j.Store(STORE);store.begin_sweep('finished',NEXT*8*12,{'before_pi':800,'after_pi':833})
    return {'all_original_operator_rows_reserved':N,'reserved_new_residual_bytes':N*NEXT*8*12,
            'peak_observed_logical_scratch_bytes':store.peak}


def operator(first,last):
    assert 0<=first<=last<N and last-first<29
    store=j.Store(STORE);control=store._get('CONTROL.json');ref=control['references']['new_residual'];assert source(ref['path'])==ref
    parameters=params();ring=p.Ring(100);masks=[tuple((1<<bit)-1 for bit in bs) for bs in v.layout(P,200,True)]
    hashes=[]
    for e in range(first,last+1):
        total=[b.ZERO]*NEXT
        for child,pars in parameters[e]:
            values=decode(store.read_row('aux',child,'prepared',operator=True),COUNT,100)
            plan=l.Plan(ring,*pars,COUNT,NEXT);total=ring.padd(total,plan.apply(values));del plan
        low=decode(store.read_row('aux',e,'prepared',operator=True),COUNT,100)[:33]
        assert total[:33]==low;total[:33]=[b.ZERO]*33
        projected=[tuple((x<<SHIFT)&mask for x,mask in zip(row,ms)) for row,ms in zip(total,masks)]
        assert l.value([projected],P)>=833
        assert all(x%(1<<NEWSHIFT)==0 for row in projected for x in row)
        raw=b.pack([[tuple(x>>NEWSHIFT for x in row) for row in projected]],96)
        assert raw==reference(ref,e,NEXT*8*12)
        store.sweep_row(e,raw);hashes.append({'state':e,'sha256':hashlib.sha256(raw).hexdigest()})
    return {'first_state':first,'last_state':last,'GMP_original_child_actions':2*(last-first+1),
            'new_residual_scalar_comparisons':(last-first+1)*NEXT*8,
            'original_low_equation_scalar_comparisons':(last-first+1)*33*8,
            'known_residual_lower_pi':833,'rows':hashes,'peak_observed_logical_scratch_bytes':store.peak}


def finish():
    store=j.Store(STORE);control=store._get('CONTROL.json');refs=control['references']
    current=store.finish_sweep()
    assert current['state']['sha256']==refs['prepared_state']['sha256']
    assert current['aux']['sha256']==refs['new_residual']['sha256']
    store.seal();PATHS.update(store.path.iterdir())
    return {'all_states':N,'complete_actual_correction_recomputed':True,'before_pi':800,'after_pi':833,
            'original_low_solve_and_GMP_operator_both_recomputed':True,
            'final_weighted_reference_bytes':current['state']['bytes'],'final_residual_reference_bytes':current['aux']['bytes'],
            'sealed_generation':current,'peak_observed_logical_scratch_bytes':store.peak,
            'full_target_or_new_precision_stage_implemented':False}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--phase',choices=('init','prepare','begin','operator','finish'),required=True)
    ap.add_argument('--first',type=int);ap.add_argument('--last',type=int);ap.add_argument('--output',required=True)
    a=ap.parse_args();out=DATA/(a.output+'.json');assert not out.exists();tick=time.monotonic()
    cert=operator(a.first,a.last) if a.phase=='operator' else {'init':init,'prepare':prepare,'begin':begin,'finish':finish}[a.phase]()
    PATHS.update(c.h.PATHS)
    packet={'status':'pass','milestone':'D131','phase':a.phase,'certificates':cert,
            'actual_harmonic_precision_increased':False,'wall_seconds':time.monotonic()-tick,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
            'sources':[source(x) for x in sorted(PATHS)]}
    out.write_text(json.dumps(packet,indent=2)+'\n');print('PHASE_METADATA|'+json.dumps(source(out)),flush=True)
    print(json.dumps({'phase':a.phase,'wall_seconds':packet['wall_seconds'],'peak_rss_bytes':packet['peak_rss_bytes']}),flush=True)
    print('PASS|545_DYADIC_JOURNAL_ARITHMETIC_CONTROL',flush=True)

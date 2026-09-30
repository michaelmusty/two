"""D124 compute CM moments directly from a certified weighted state.

Compose each integral CM map with each contracting original child map.
The composite still has c and delta divisible by pi. Thus weighted
input moments suffice directly, avoiding the 3P state-moment extension.
All output moments are compared with the separately computed CM bank.
Independent integer quotient arithmetic checks each normalization and
determinant identity. This is a control, not an extra harmonic column.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
def module(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/'dembele/pari'/file)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
w=module('weighted','497_dyadic_weighted_chunks.py')
r=module('independent','486_dyadic_precision400_independent.py')
h=w.h;b=w.b;ONE=b.ONE;ZERO=b.ZERO


def build(P):
    start=time.monotonic();assert P in (800,1600)
    verified_stem='dyadic_staged_P800_col00_verified_d123' if P==800 else 'dyadic_weighted_P1600_col00_verified_d124'
    state,statepath=h.read(verified_stem);assert state['certificate']['original_full_residual_zero']
    if P==800:
        packet,packetpath=h.read('dyadic_shrinking_P800_col00_step12_d123')
    else:
        packetpath=Path(state['weighted_state_metadata']['path']);assert h.source(packetpath)==state['weighted_state_metadata']
        packet,_=h.read(packetpath.stem)
    values=w.weighted_state(packet);uniform=h.binary(state['state_file'],174,P,P//8)
    assert w.project(uniform,P)==values
    cmstem='dyadic_staged_CM_P800_col00_d123' if P==800 else 'dyadic_CM_P1600_col00_d124'
    cm,cmpath=h.read(cmstem);assert cm['working_precision_pi']==P
    expected=h.binary(cm['checkpoint_files'][0],17,2*P,P//8)
    transport,path=h.read('dyadic_target_transports_d121');maps=transport['transitions']
    charts=[x for x in transport['CM_charts'] if x['chart']=='A'];assert len(charts)==17
    ring=w.f.Ring(P//8);ind=r.Quotient(r.FP,P);outputs=[];checks=[];two=(2,)+(0,)*7
    for ci,chart in enumerate(charts):
        assert chart['CM_index']==ci and chart['normalized_error_pi']>=P
        A,B,C=[tuple(int(c)&ring.mask for c in x) for x in chart['normalized_center'][:3]]
        assert ind.value(C)>=1;total=[ZERO]*(2*P)
        for branch,child in enumerate(maps[chart['target_edge']]['children']):
            assert child['normalized_error_pi']>=P
            a,bv,c=[tuple(int(t)&ring.mask for t in x) for x in child['normalized_center'][:3]]
            d=ring.add(ONE,ring.mul(C,bv));inverse=ONE
            for _ in range(P.bit_length()):inverse=ring.mul(inverse,ring.add(two,ring.neg(ring.mul(d,inverse))))
            assert ring.mul(d,inverse)==ONE
            aa=ring.mul(ring.add(ring.mul(A,a),ring.mul(B,c)),inverse)
            bb=ring.mul(ring.add(ring.mul(A,bv),B),inverse)
            cc=ring.mul(ring.add(c,ring.mul(C,a)),inverse)
            # Separate multiplication and valuation implementation.
            assert ind.mul(d,aa)==ind.add(ind.mul(A,a),ind.mul(B,c))
            assert ind.mul(d,bb)==ind.add(ind.mul(A,bv),B)
            assert ind.mul(d,cc)==ind.add(c,ind.mul(C,a))
            delta=ind.sub(aa,ind.mul(bb,cc));parent=ind.sub(A,ind.mul(B,C));child_delta=ind.sub(a,ind.mul(bv,c))
            assert ind.mul(ind.mul(d,d),delta)==ind.mul(parent,child_delta)
            assert ind.value(d)==0 and ind.value(cc)>=1 and ind.value(delta)>=1
            plan=w.l.Plan(ring,aa,bb,cc,P,2*P)
            total=ring.padd(total,plan.apply(values[child['target_edge']]))
            checks.append({'CM_index':ci,'branch':branch,'target_state':child['target_edge'],
                'denominator_valuation_pi':ind.value(d),'c_valuation_pi':ind.value(cc),'delta_valuation_pi':ind.value(delta)})
        assert total==expected[ci];outputs.append(total)
        print(f'COMPOSED_CM|P={P}; charts={ci+1}; seconds={time.monotonic()-start:.3f}',flush=True)
    stem=f'dyadic_composed_CM_P{P}_d124';file=w.scaled_file(stem,'moments',outputs,P,0)
    h.PATHS.update([Path(__file__),Path(w.__file__),Path(r.__file__)])
    return {'status':'pass','milestone':'D124','working_precision_pi':P,'harmonic_basis_column':0,
        'CM_charts_checked':17,'composed_child_maps_checked':34,'input_count':P,'output_count':2*P,
        'all_scalar_moment_comparisons':17*2*P*8,'weighted_input_used':True,
        'uniform_reconstruction_and_3P_state_extension_not_used_for_calculation':True,
        'uniform_reference_used_only_to_check_weighted_input':True,
        'independent_composition_normalization_and_determinant_checks':checks,
        'verified_state_metadata':h.source(statepath),'weighted_state_metadata':h.source(packetpath),
        'independently_computed_CM_metadata':h.source(cmpath),'checkpoint_files':[file],
        'wall_seconds':time.monotonic()-start,'peak_rss_bytes':w.peak_rss(),
        'full_sixteen_column_bank_precision_pi':400,'new_harmonic_column_computed':False,
        'sources':[h.source(path) for path in sorted(h.PATHS)]}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--precision',type=int,default=800);args=parser.parse_args()
    out=DATA/f'dyadic_composed_CM_P{args.precision}_d124.json';assert not out.exists()
    result=build(args.precision);out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['sources','independent_composition_normalization_and_determinant_checks']}),flush=True)
    print('PASS|500_DYADIC_COMPOSED_CM_CONTROL',flush=True)

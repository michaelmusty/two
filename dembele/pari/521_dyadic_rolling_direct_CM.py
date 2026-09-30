"""D127 direct CM values from the sealed rolling P=1600 column, using selective reads."""
import argparse
import importlib.util
import json
from math import comb
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
def module(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/'dembele/pari'/file)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
w=module('bank','519_dyadic_rolling_precision_chunks.py')
r=module('independent','486_dyadic_precision400_independent.py')
c=module('coarse','475_dyadic_actual_CM_column.py')
h=w.h;b=w.b;ONE=b.ONE;ZERO=b.ZERO


def build(column):
    start=time.monotonic();P=1600;assert column==1
    state,statepath=h.read(f'dyadic_rolling_P1600_col{column:02d}_verified_d127')
    assert state['certificate']['original_full_residual_zero'] and state['harmonic_basis_column']==column
    packetpath=Path(state['weighted_state_metadata']['path']);assert h.source(packetpath)==state['weighted_state_metadata']
    packet,_=h.read(packetpath.stem)
    summary,_=h.read('dyadic_rolling_pilot_P1600_col01_d127')
    assert summary['verified_checkpoint']==h.source(statepath)
    assert (w.DATA/'SEALED.json').is_file()
    values=w.q.StateReader(packet['state_file'],P,P//8,weighted_precision=P)
    uniform=w.q.StateReader(state['state_file'],P,P//8)
    for e in range(174):assert w.project([uniform.row(e)],P)==[values.row(e)]
    uniform.close()
    oldstem=f'dyadic_direct_CM_P800_col{column:02d}_d125'
    old,oldpath=h.read(oldstem);oldbin=DATA/(oldstem+'_moments.bin');h.PATHS.add(oldbin)
    assert h.source(oldbin)==old['checkpoint_files'][0]
    oldvalues=b.unpack(oldbin.read_bytes(),17,1600,100)
    transport,path=h.read('dyadic_target_transports_d121');maps=transport['transitions']
    charts=[x for x in transport['CM_charts'] if x['chart']=='A'];assert len(charts)==17
    # Engine initialization verifies all adaptive kernel source/library hashes.
    engine=w.Engine(P);ring=w.a.Ring(P//8);ind=r.Quotient(r.FP,P);outputs=[];checks=[];two=(2,)+(0,)*7
    for ci,chart in enumerate(charts):
        assert chart['CM_index']==ci and chart['normalized_error_pi']>=P
        A,B,C=[tuple(int(c)&ring.mask for c in x) for x in chart['normalized_center'][:3]]
        assert ind.value(C)>=1;total=[ZERO]*(2*P)
        for branch,child in enumerate(maps[chart['target_edge']]['children']):
            assert child['normalized_error_pi']>=P
            a,bv,cv=[tuple(int(t)&ring.mask for t in x) for x in child['normalized_center'][:3]]
            d=ring.add(ONE,ring.mul(C,bv));inverse=ONE
            for _ in range(P.bit_length()):inverse=ring.mul(inverse,ring.add(two,ring.neg(ring.mul(d,inverse))))
            assert ring.mul(d,inverse)==ONE
            aa=ring.mul(ring.add(ring.mul(A,a),ring.mul(B,cv)),inverse)
            bb=ring.mul(ring.add(ring.mul(A,bv),B),inverse)
            cc=ring.mul(ring.add(cv,ring.mul(C,a)),inverse)
            assert ind.mul(d,aa)==ind.add(ind.mul(A,a),ind.mul(B,cv))
            assert ind.mul(d,bb)==ind.add(ind.mul(A,bv),B)
            assert ind.mul(d,cc)==ind.add(cv,ind.mul(C,a))
            delta=ind.sub(aa,ind.mul(bb,cc));parent=ind.sub(A,ind.mul(B,C));child_delta=ind.sub(a,ind.mul(bv,cv))
            assert ind.mul(ind.mul(d,d),delta)==ind.mul(parent,child_delta)
            assert ind.value(d)==0 and ind.value(cc)>=1 and ind.value(delta)>=1
            plan=w.l.Plan(ring,aa,bb,cc,P,2*P)
            total=ring.padd(total,plan.apply(values.row(child['target_edge'])))
            checks.append({'CM_index':ci,'branch':branch,'target_state':child['target_edge'],
                'denominator_valuation_pi':ind.value(d),'c_valuation_pi':ind.value(cc),'delta_valuation_pi':ind.value(delta)})
        assert total[0]==(chart['zeroth_moments'][column]&ring.mask,)+(0,)*7
        assert b.reduce([total[:1600]],(1<<100)-1)==[oldvalues[ci]]
        outputs.append(total)
    values.close();cm_seconds=time.monotonic()-start
    cm=c.Ring(2*P+64);pi=cm.add(cm.scale(cm.mul(c.BETA,c.BETA),-1),cm.scale(c.ONE,-2))
    powers=cm.powers(pi,7);q=cm.add(tuple(c.MP[1:]),cm.scale(c.BETA,-1));assert cm.mul(c.BETA,q)==pi
    qp=cm.powers(q,2*P-1);kernels=[];errors=[];gains=[]
    for order in range(4):
        n=2*order+2;gain=16*min(k+(comb(n,k)&-comb(n,k)).bit_length()-1 for k in range(1,n+1))
        kernel=[cm.scale(qp[k],c.coefficient(n,k)) for k in range(2*P)]
        assert all(cm.value(x)>=min(cm.precision,k+gain) for k,x in enumerate(kernel))
        kernels.append(kernel);gains.append(gain);errors.append(min(cm.precision,2*P+gain))
    rows=[]
    for ci,moments in enumerate(outputs):
        embedded=[]
        for m in moments:
            value=c.ZERO
            for coefficient,power in zip(m,powers):value=cm.add(value,cm.scale(power,coefficient))
            embedded.append(value)
        jets=[];valuations=[]
        for order,kernel in enumerate(kernels):
            value=c.ZERO
            for a,m in zip(kernel,embedded):value=cm.add(value,cm.mul(a,m))
            prior=tuple(old['CM_values'][ci]['coarse_coefficients_beta'][order])
            assert cm.value(cm.add(value,cm.scale(prior,-1)))>=old['coarse_error_beta'][order]
            jets.append(list(value));v=cm.value(value);valuations.append(v if v<errors[order] else None)
        rows.append({'CM_index':ci,'coarse_coefficients_beta':jets,'certified_valuations_beta':valuations})
    assert errors==[3232,3248,3232,3264]
    stem=f'dyadic_rolling_CM_P1600_col{column:02d}_d127'
    binary=DATA/(stem+'_moments.bin');assert not binary.exists()
    binary.write_bytes(b.pack(outputs,P//8));file=h.source(binary)
    h.PATHS.update(w.c.h.PATHS)
    h.PATHS.update([Path(__file__),Path(w.__file__),Path(r.__file__),Path(c.__file__)])
    return {'status':'pass','milestone':'D127','working_precision_pi':P,'harmonic_basis_column':column,
        'CM_charts_checked':17,'composed_child_maps_checked':34,'input_count':P,'CM_cutoff':2*P-1,
        'CM_moment_scalar_coefficients':17*2*P*8,'old_CM_moment_scalar_coefficients_checked':17*P*8,
        'old_coarse_values_checked':68,'weighted_input_used':True,'state_extension_3P_not_used':True,
        'independent_composition_checks':checks,'verified_state_metadata':h.source(statepath),
        'weighted_state_metadata':h.source(packetpath),'checkpoint_files':[file],
        'arithmetic_precision_beta':cm.precision,'coarse_orders':[0,1,2,3],'kernel_gains_beta':gains,
        'coarse_error_beta':errors,'CM_values':rows,'direct_CM_seconds':cm_seconds,
        'wall_seconds':time.monotonic()-start,'peak_rss_bytes':w.peak_rss(),
        'full_sixteen_column_bank_precision_pi':800,'candidate_identification_proved':False,
        'sources':[h.source(path) for path in sorted(h.PATHS)]}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--column',type=int,required=True);args=parser.parse_args()
    out=DATA/f'dyadic_rolling_CM_P1600_col{args.column:02d}_d127.json';assert not out.exists()
    result=build(args.column);out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['sources','CM_values','independent_composition_checks']}),flush=True)
    print('PASS|521_DYADIC_ROLLING_DIRECT_CM',flush=True)

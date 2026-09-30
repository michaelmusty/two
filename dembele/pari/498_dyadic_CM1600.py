"""D124 extend the verified P=1600 column to CM charts and coarse coefficients."""
import argparse
import importlib.util
import json
from math import comb
from pathlib import Path
import time
import resource
import sys

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
def module(name,filename):
    s=importlib.util.spec_from_file_location(name,ROOT/'dembele/pari'/filename)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=module('staged','489_dyadic_staged_lift.py');c=module('coarse','475_dyadic_actual_CM_column.py')
f,b,l=h.f,h.b,h.l


def build(args):
    begin=time.monotonic();packet,path=h.read(args.previous);P=packet['working_precision_pi'];column=packet['harmonic_basis_column'];assert P==1600 and column==0
    H=3*P-2;C=2*P-1;ring=f.Ring(P//8);trans,transpath=h.read('dyadic_target_transports_d121')
    charts=[row for row in trans['CM_charts'] if row['chart']=='A'];assert len(charts)==17
    result={'status':'pass','milestone':'D124','phase':args.phase,'working_precision_pi':P,
        'harmonic_basis_column':column,'state_cutoff':H,'CM_cutoff':C,'actual_moment_precision_increased':True,
        'actual_harmonic_columns_refined':1,'full_sixteen_column_bank_precision_pi':400,'candidate_identification_proved':False}
    if args.phase=='extend':
        assert packet['certificate']['original_full_residual_zero'] and packet['actual_moment_precision_increased']
        state=h.state(packet);targets,params,parampath=b.parameters(P);h.PATHS.add(parampath)
        required=sorted({row['target_edge'] for row in charts});assert len(required)==9
        values=[];plans={}
        for e in required:
            total=[b.ZERO]*(H+1)
            for branch,j in enumerate(targets[e]):
                pars=params[e][branch]
                if pars not in plans:plans[pars]=l.Plan(ring,*pars,P,H+1)
                total=ring.padd(total,plans[pars].apply(state[j]))
            assert total[:P]==state[e];values.append(total)
        file=h.save_binary(args.output,'states',values,P)
        result.update(extended_target_states=required,checkpoint_files=[file],verified_state_metadata=h.source(path))
    elif args.phase=='charts':
        assert packet['phase']=='extend' and 0<=args.first<=args.last<17
        extended=h.binary(packet['checkpoint_files'][0],9,H+1,P//8)
        states=dict(zip(packet['extended_target_states'],extended));values=[]
        oldstem='dyadic_staged_CM_P800_col00_d123'
        old,oldpath=h.read(oldstem)
        oldbin=DATA/(oldstem+'_moments.bin');oldvalues=b.unpack(oldbin.read_bytes(),17,1600,100);h.PATHS.add(oldbin)
        for ci in range(args.first,args.last+1):
            row=charts[ci];assert row['CM_index']==ci and row['normalized_error_pi']>=P
            pars=[tuple(int(x)&ring.mask for x in a) for a in row['normalized_center'][:3]]
            got=l.Plan(ring,*pars,H+1,C+1).apply(states[row['target_edge']])
            assert got[0]==(row['zeroth_moments'][column]&ring.mask,)+(0,)*7
            assert b.reduce([got[:1600]],(1<<100)-1)==[oldvalues[ci]]
            values.append(got)
        file=h.save_binary(args.output,'moments',values,P)
        result.update(first_CM=args.first,last_CM=args.last,checkpoint_files=[file],extension_metadata=h.source(path),
            old_CM_scalar_overlaps_checked=len(values)*1600*8)
    elif args.phase=='finish':
        assert packet['phase']=='extend';values=[];cursor=0
        for file in sorted(DATA.glob(args.chunks+'_c[0-9][0-9]_[0-9][0-9].json')):
            row,_=h.read(file.stem)
            assert row['extension_metadata']==h.source(path) and row['first_CM']==cursor
            assert row['working_precision_pi']==P and row['harmonic_basis_column']==column
            count=row['last_CM']-cursor+1;assert count>0
            values+=h.binary(row['checkpoint_files'][0],count,C+1,P//8);cursor+=count
        assert cursor==17
        cm=c.Ring(2*P+64);pi=cm.add(cm.scale(cm.mul(c.BETA,c.BETA),-1),cm.scale(c.ONE,-2))
        powers=cm.powers(pi,7);q=cm.add(tuple(c.MP[1:]),cm.scale(c.BETA,-1));assert cm.mul(c.BETA,q)==pi
        qp=cm.powers(q,C);kernels=[];errors=[];gains=[]
        for order in range(4):
            n=2*order+2
            gain=16*min(k+(comb(n,k)&-comb(n,k)).bit_length()-1 for k in range(1,n+1))
            kernel=[cm.scale(qp[r],c.coefficient(n,r)) for r in range(C+1)]
            assert all(cm.value(x)>=min(cm.precision,r+gain) for r,x in enumerate(kernel))
            kernels.append(kernel);gains.append(gain);errors.append(min(cm.precision,2*P+gain,C+1+gain))
        oldstem='dyadic_staged_CM_P800_col00_d123'
        old,_=h.read(oldstem);rows=[]
        for ci,moments in enumerate(values):
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
        file=h.save_binary(args.output,'moments',values,P)
        result.update(CM_charts_checked=17,CM_moment_scalar_coefficients=17*(C+1)*8,
            extended_target_states=packet['extended_target_states'],coarse_orders=[0,1,2,3],
            arithmetic_precision_beta=cm.precision,kernel_gains_beta=gains,coarse_error_beta=errors,
            CM_values=rows,old_coarse_values_checked=68,old_CM_moment_scalar_coefficients_checked=17*1600*8,
            checkpoint_files=[file])
    else:raise AssertionError(args.phase)
    h.PATHS.update([Path(__file__),Path(h.__file__),Path(c.__file__),Path(f.__file__),f.LIBRARY])
    result.update(wall_seconds=time.monotonic()-begin,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),sources=[h.source(x) for x in sorted(h.PATHS)])
    print('STAGED_CM|'+json.dumps({k:v for k,v in result.items() if k not in ['sources','CM_values','checkpoint_files']}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--phase',choices=['extend','charts','finish'],required=True)
    parser.add_argument('--previous',required=True);parser.add_argument('--output',required=True)
    parser.add_argument('--first',type=int);parser.add_argument('--last',type=int);parser.add_argument('--chunks');args=parser.parse_args()
    out=DATA/(args.output+'.json');assert not out.exists()
    out.write_text(json.dumps(build(args),indent=2)+'\n');print('PASS|498_DYADIC_CM1600',flush=True)

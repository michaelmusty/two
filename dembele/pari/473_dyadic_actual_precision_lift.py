"""D121 checkpointed actual P=400 lift of one harmonic column.

Each seed, correction or original-residual verification is a separately
capped job. Saved coefficients are exact residues, with certified common
pi-error supplied by contraction and the original equations.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import time
import numpy as np

ROOT=Path(__file__).resolve().parents[2]; DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('mp_low',ROOT/'dembele/pari/472_dyadic_multiprecision_low_factor.py')
b=importlib.util.module_from_spec(s);s.loader.exec_module(b)
p=b.p; ZERO,ONE=b.ZERO,b.ONE
P,R=400,32


class Plan(p.Plan):
    def power(self, which, n):
        # Low-row actions may have far more inputs than outputs. Construct
        # only retained coefficients, before indexing geometric powers.
        key=which,n
        if key not in self.cache:
            ring=self.ring; ans=[]; binomial=1
            for k in range(min(n+1,self.rows)):
                if which=='D': value=self.geometric[k] if k%2==0 else ring.neg(self.geometric[k])
                else: value=ring.mul(self.scalar_powers[0][n-k],self.scalar_powers[1][k])
                ans.append(tuple((binomial*x)&ring.mask for x in value))
                numerator=binomial*(n-k)
                assert numerator%(k+1)==0
                binomial=numerator//(k+1)
            self.cache[key]=ans
        return self.cache[key]


def value(bank,precision):
    ans=precision
    for edge in bank:
        for row in edge:
            for i,x in enumerate(row):
                if x:
                    ans=min(ans,8*((x&-x).bit_length()-1)+i)
                    if ans==0:return 0
    return ans


def controls():
    ring=p.Ring(50);count=39
    a,bv,c=b.k.data(1,3,50,'truncated-plan')[0]
    moments=b.k.data(1,count,50,'truncated-moments')[0]
    rows=[ONE]+[ZERO]*(count-1);expected=[]
    for n in range(9):
        acc=ZERO
        for x,y in zip(rows,moments): acc=ring.add(acc,p.f.slow_product([x],[y],ring.mod)[0])
        expected.append(acc)
        nextrow=[ring.mul(bv,rows[0])]
        for k in range(1,count):
            nextrow.append(ring.add(ring.add(ring.mul(bv,rows[k]),ring.mul(a,rows[k-1])),
                                    ring.neg(ring.mul(c,nextrow[-1]))))
        rows=nextrow
    for length in (1,3,9): assert Plan(ring,a,bv,c,count,length).apply(moments)==expected[:length]
    return {'independent_truncated_output_lengths':[1,3,9],'input_count':39,'modulus_bits':50}


class Engine:
    def __init__(self):
        self.targets,self.params,self.transport_path=b.parameters(P)
        self.algebra=b.Algebra(P//8);self.times=[];self.paths=[]

    def factors(self,bits):
        if bits<=25:
            path=DATA/f'dyadic_sparse_low_r{R}_d121.npz';self.paths.append(path)
            data=np.load(path);mask=(1<<bits)-1;order=data['order'].tolist()
            def convert(a):return [[tuple(int(c)&mask for c in x) for x in row] for row in a]
            D={i:convert(a) for i,a in enumerate(data['diagonal'])}
            L={tuple(key):convert(a) for key,a in zip(data['lower_keys'].tolist(),data['lower'])}
            U={tuple(key):convert(a) for key,a in zip(data['upper_keys'].tolist(),data['upper'])}
        else:
            meta=DATA/f'dyadic_low_factor_P{P}_r{R}_d121.json'
            path=meta.with_suffix('.bin');self.paths += [meta,path]
            data=json.loads(meta.read_text());order=data['order'];mask=(1<<bits)-1
            assert data['modulus_bits']>=bits
            size=R*R*8*data['binary_coefficient_width_bytes'];D,L,U={},{},{}
            with path.open('rb') as file:
                for kind,i,j in data['binary_block_order']:
                    a=b.reduce(b.unpack(file.read(size),R,R,data['modulus_bits']),mask)
                    if kind=='D':D[i]=a
                    else:(L if kind=='L' else U)[i,j]=a
                assert file.read()==b''
        return order,D,L,U

    def low_solve(self,moment,bits):
        cut=8*bits;start=time.monotonic();algebra=b.Algebra(bits);ring=algebra.ring
        if cut<=R+1 and all(row[0]==ZERO for row in moment):
            return [[ZERO]*R for _ in range(174)]
        order,D,L,U=self.factors(bits)
        high=[[x if k==0 or k>R else ZERO for k,x in enumerate(row[:cut])] for row in moment]
        rhs=[];plans={}
        for e in range(174):
            total=[ZERO]*(R+1)
            for branch,j in enumerate(self.targets[e]):
                pars=tuple(tuple(x&ring.mask for x in a) for a in self.params[e][branch])
                if pars not in plans:plans[pars]=Plan(ring,*pars,cut,R+1)
                total=ring.padd(total,plans[pars].apply(high[j]))
            rhs.append([[x] for x in total[1:]])
        answer=b.solve(rhs,order,D,L,U,algebra)
        out=[[row[0] for row in edge] for edge in answer]
        self.times.append({'operation':'low_solve','modulus_bits':bits,'seconds':time.monotonic()-start})
        print('ACTUAL_LOW_SOLVE|'+json.dumps(self.times[-1]),flush=True)
        return out

    def apply(self,moment,rows=P):
        start=time.monotonic();gain=value(moment,P)
        if gain==P:return [[ZERO]*rows for _ in range(174)]
        shift=gain//8;bits=P//8-shift;cut=8*bits;ring=p.Ring(bits)
        assert all(not (x&((1<<shift)-1)) for edge in moment for row in edge for x in row)
        reduced=[[tuple(x>>shift for x in row) for row in edge[:cut]] for edge in moment]
        if all(x==ZERO for edge in reduced for x in edge):return [[ZERO]*rows for _ in range(174)]
        plans={};out=[]
        for e in range(174):
            total=[ZERO]*rows
            for branch,j in enumerate(self.targets[e]):
                pars=tuple(tuple(x&ring.mask for x in a) for a in self.params[e][branch])
                if pars not in plans:plans[pars]=Plan(ring,*pars,cut,rows)
                total=ring.padd(total,plans[pars].apply(reduced[j]))
            out.append([tuple(x<<shift for x in row) for row in total])
            if e%60==0:
                print(f'ACTUAL_ACTION|states={e+1}/174; bits={bits}; seconds={time.monotonic()-start:.3f}',flush=True)
        self.times.append({'operation':'original_transport','input_valuation_pi':gain,
            'modulus_bits':bits,'input_count':cut,'output_count':rows,'seconds':time.monotonic()-start})
        return out


def checkpoint(stem):
    path=DATA/(stem+'.json');data=json.loads(path.read_text())
    assert data['status']=='pass' and data['working_precision_pi']==P and data['eliminated_positive_moments']==R
    for item in data['checkpoint_files']:assert p.f.source(item['path'])==item
    state=b.unpack((DATA/(stem+'_state.bin')).read_bytes(),174,P,P//8)
    residual=b.unpack((DATA/(stem+'_residual.bin')).read_bytes(),174,P,P//8)
    assert value(residual,P)==data['residual_lower_bound_pi']
    return data,state,residual,path


def run(phase,previous,column,outstem):
    start=time.monotonic();engine=Engine();paths=[];certificate={};history=[]
    if phase=='seed':
        assert previous is None and 0<=column<16
        certificate['truncated_plan_controls']=controls()
        bankpath=DATA/'dyadic_precision200_d115.json';bank=json.loads(bankpath.read_text())
        state=[[tuple(m[column]) for m in row[:P]] for row in bank['state_moments_power_basis']]
        harmonicpath=DATA/'dyadic_harmonic_certificate_d111.json';harmonic=json.loads(harmonicpath.read_text())
        masses=harmonic['harmonic_basis'][column]
        for e in range(174): state[e][0]=(masses[e]&engine.algebra.mask,)+(0,)*7
        assert all(sum(masses[j] for j in engine.targets[e])==masses[e] for e in range(174))
        low=engine.low_solve(state,P//8)
        for e in range(174):state[e][1:R+1]=low[e]
        assert [[tuple(c&((1<<25)-1) for c in x) for x in row] for row in state]==[
            [tuple(m[column]) for m in row[:P]] for row in bank['state_moments_power_basis']]
        residual=engine.algebra.sub(engine.apply(state),state)
        assert all(x==ZERO for row in residual for x in row[:R+1])
        assert value(residual,P)>=200
        paths += [bankpath,harmonicpath]
    else:
        data,state,residual,path=checkpoint(previous);paths.append(path)
        paths += [Path(x['path']) for x in data['checkpoint_files']]
        column=data['harmonic_basis_column'];history=data['correction_history']
        if phase=='step':
            before=value(residual,P);assert 200<=before<P
            shift=before//8;bits=P//8-shift
            assert all(x==ZERO for row in residual for x in row[:R+1])
            reduced=[[tuple(c>>shift for c in x) for x in row] for row in residual]
            assert all(not(c&((1<<shift)-1)) for row in residual for x in row for c in x)
            low=engine.low_solve(reduced,bits)
            for e in range(174):reduced[e][1:R+1]=low[e]
            correction=[[tuple(c<<shift for c in x) for x in row] for row in reduced]
            state=engine.algebra.add(state,correction)
            residual=engine.apply(correction)
            assert all(row[0]==ZERO for row in residual)
            for row in residual:row[1:R+1]=[ZERO]*R
            after=value(residual,P);assert after>=min(P,before+R+1)
            history=history+[{'before_pi':before,'after_pi':after}]
            print('ACTUAL_PRECISION_GAIN|'+json.dumps(history[-1]),flush=True)
        elif phase=='verify':
            assert value(residual,P)==P
            checked=engine.apply(state);assert checked==state
            bankpath=DATA/'dyadic_precision200_d115.json';bank=json.loads(bankpath.read_text());paths.append(bankpath)
            assert b.reduce(state,(1<<25)-1)==[[tuple(m[column]) for m in row[:P]] for row in bank['state_moments_power_basis']]
            certificate={'original_full_residual_zero':True,'scalar_coefficients_checked':174*P*8,
                'all_P200_seed_coefficients_agree':True,'actual_new_precision_pi':P}
        else:raise AssertionError(phase)
    statepath=DATA/(outstem+'_state.bin');respath=DATA/(outstem+'_residual.bin')
    assert not statepath.exists() and not respath.exists()
    statepath.write_bytes(b.pack(state,P//8));respath.write_bytes(b.pack(residual,P//8))
    paths += engine.paths+[Path(__file__),Path(b.__file__),Path(p.__file__),engine.transport_path]
    result={'status':'pass','milestone':'D121','phase':phase,'working_precision_pi':P,
        'eliminated_positive_moments':R,'harmonic_basis_column':column,
        'residual_lower_bound_pi':value(residual,P),'correction_history':history,'certificate':certificate,
        'actual_moment_precision_increased':phase=='verify','full_sixteen_column_bank_refined':False,
        'timings':engine.times,'wall_seconds':time.monotonic()-start,
        'checkpoint_files':[p.f.source(x) for x in [statepath,respath]],
        'sources':[p.f.source(x) for x in sorted(set(paths))]}
    print('ACTUAL_PHASE_RESULT|'+json.dumps({k:v for k,v in result.items() if k not in ('sources','checkpoint_files')}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=['seed','step','verify'],required=True)
    parser.add_argument('--previous');parser.add_argument('--column',type=int,default=0)
    parser.add_argument('--output',required=True);args=parser.parse_args()
    out=DATA/(args.output+'.json');assert not out.exists()
    out.write_text(json.dumps(run(args.phase,args.previous,args.column,args.output),indent=2)+'\n')
    print('PASS|473_DYADIC_ACTUAL_PRECISION_LIFT',flush=True)

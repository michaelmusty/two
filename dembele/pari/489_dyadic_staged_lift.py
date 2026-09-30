"""D123 configurable Schur lifts with immutable chunks of original sweeps.

The seed first extends the old low bank using T itself. Unknown high seed
moments must not simply be declared zero to the old precision. Every
assembly verifies disjoint complete state coverage and input hashes.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('fast',ROOT/'dembele/pari/477_dyadic_polynomial_kernel_control.py')
f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
l,b,p=f.l,f.b,f.p;ZERO,ONE=b.ZERO,b.ONE;R=32
PATHS=set()


def source(path):return p.f.source(Path(path))


def read(stem):
    assert re.fullmatch(r'[A-Za-z0-9_-]+',stem)
    path=DATA/(stem+'.json');packet=json.loads(path.read_text());PATHS.add(path)
    assert packet['status']=='pass'
    for row in packet.get('checkpoint_files',[]):
        assert source(row['path'])==row;PATHS.add(Path(row['path']))
    return packet,path


def binary(row,nr,nc,bits):
    assert source(row['path'])==row;PATHS.add(Path(row['path']))
    result=b.unpack(Path(row['path']).read_bytes(),nr,nc,bits)
    assert all(0<=c<1<<bits for edge in result for x in edge for c in x)
    return result


def save_binary(stem,label,values,P):
    path=DATA/(stem+'_'+label+'.bin');assert not path.exists()
    path.write_bytes(b.pack(values,P//8));return source(path)


def metadata(P,column,seed):
    return {'status':'pass','milestone':'D123','working_precision_pi':P,
        'eliminated_positive_moments':R,'harmonic_basis_column':column,
        'seed_precision_pi':seed,'actual_moment_precision_increased':False,
        'full_sixteen_column_bank_refined':False}


class Engine:
    def __init__(self,P):
        self.P=P;self.targets,self.params,path=b.parameters(P);PATHS.add(path);self.times=[]
        PATHS.update([Path(b.__file__),Path(p.__file__),Path(l.__file__),Path(f.__file__),f.CSOURCE,f.LIBRARY,b.k.LIBRARY])
    def factors(self,bits):
        P=400 if bits<=50 else self.P
        stem=f'dyadic_low_factor_P{P}_r32_'+('d121' if P==400 else 'd123')
        packet,path=read(stem);rawpath=path.with_suffix('.bin');PATHS.add(rawpath)
        assert packet['modulus_bits']>=bits
        expected=[x for x in packet['sources'] if Path(x['path']).resolve()==rawpath.resolve()]
        assert len(expected)==1 and source(rawpath)==expected[0]
        D,L,U={},{},{};size=R*R*8*packet['binary_coefficient_width_bytes'];mask=(1<<bits)-1
        with rawpath.open('rb') as file:
            for kind,i,j in packet['binary_block_order']:
                block=b.reduce(b.unpack(file.read(size),R,R,packet['modulus_bits']),mask)
                if kind=='D':D[i]=block
                else:(L if kind=='L' else U)[i,j]=block
            assert not file.read()
        return packet['order'],D,L,U
    def low_solve(self,moment,bits):
        started=time.monotonic();cut=min(len(moment[0]),8*bits)
        if 8*bits<=R+1 and all(row[0]==ZERO for row in moment):return [[ZERO]*R for _ in range(174)]
        order,D,L,U=self.factors(bits);algebra=b.Algebra(bits);ring=f.Ring(bits)
        high=[[x if k==0 or k>R else ZERO for k,x in enumerate(row[:cut])] for row in moment]
        plans={};rhs=[]
        for e in range(174):
            total=[ZERO]*(R+1)
            for branch,j in enumerate(self.targets[e]):
                pars=tuple(tuple(c&ring.mask for c in x) for x in self.params[e][branch])
                if pars not in plans:plans[pars]=l.Plan(ring,*pars,cut,R+1)
                total=ring.padd(total,plans[pars].apply(high[j]))
            rhs.append([[x] for x in total[1:]])
        answer=b.solve(rhs,order,D,L,U,algebra)
        self.times.append({'operation':'low_solve','modulus_bits':bits,'seconds':time.monotonic()-started})
        return [[row[0] for row in edge] for edge in answer]
    def apply(self,moment,first,last,backend):
        start=time.monotonic();P=self.P;gain=l.value(moment,P)
        if gain==P:return [[ZERO]*P for _ in range(first,last+1)]
        shift=gain//8;bits=P//8-shift;cut=min(len(moment[0]),8*bits)
        assert all(not(c&((1<<shift)-1)) for edge in moment for row in edge for c in row)
        reduced=[[tuple(c>>shift for c in x) for x in edge[:cut]] for edge in moment]
        ring=(p.Ring if backend=='GMP' else f.Ring)(bits);plans={};out=[]
        for e in range(first,last+1):
            total=[ZERO]*P
            for branch,j in enumerate(self.targets[e]):
                pars=tuple(tuple(c&ring.mask for c in x) for x in self.params[e][branch])
                if pars not in plans:plans[pars]=l.Plan(ring,*pars,cut,P)
                total=ring.padd(total,plans[pars].apply(reduced[j]))
            assert len(total)==P
            out.append([tuple(c<<shift for c in x) for x in total])
        self.times.append({'operation':'original_transport_chunk','backend':backend,'first_state':first,'last_state':last,
            'input_valuation_pi':gain,'modulus_bits':bits,'input_count':cut,'output_count':P,
            'distinct_prepared_maps':len(plans),'seconds':time.monotonic()-start})
        return out


def state(packet):
    return binary(packet['state_file'],174,packet['working_precision_pi'],packet['working_precision_pi']//8)


def original_seed(packet):
    old,_=read(packet['seed_stem']);P=old['working_precision_pi']
    return old,binary(old['checkpoint_files'][0],174,P,P//8)


def check_old_low(packet,values):
    old,bank=original_seed(packet);oldP=old['working_precision_pi'];mask=(1<<(oldP//8))-1
    assert b.reduce([row[:oldP] for row in values],mask)==bank
    return 174*oldP*8


def assemble(previous,prefix,backend):
    packet,previouspath=read(previous);P=packet['working_precision_pi']
    paths=sorted(DATA.glob(prefix+'_e[0-9][0-9][0-9]_[0-9][0-9][0-9].json'))
    assert paths,('no sweep chunks',prefix)
    total=[];cursor=0;seconds=0
    for path in paths:
        row,_=read(path.stem)
        assert row['kind']=='operator_chunk' and row['input_metadata']==source(previouspath)
        assert row['working_precision_pi']==P and row['backend']==backend
        assert row['first_state']==cursor and row['last_state']<174
        count=row['last_state']-cursor+1;assert count>0
        total+=binary(row['checkpoint_files'][0],count,P,P//8)
        cursor+=count;seconds+=row['timings'][0]['seconds']
    assert cursor==174 and len(total)==174
    return total,{'chunks':len(paths),'states':cursor,'summed_transport_seconds':seconds,'input_metadata':source(previouspath)}


def run(args):
    start=time.monotonic();outstem=args.output;phase=args.phase;times=[]
    if phase=='init':
        old,oldpath=read(args.seed);seed=old['working_precision_pi'];P=args.precision;column=old['harmonic_basis_column']
        assert old['certificate']['original_full_residual_zero'] and 400<=seed<P<=10552 and P%8==0
        values=binary(old['checkpoint_files'][0],174,seed,seed//8)
        harmonicpath=DATA/'dyadic_harmonic_certificate_d111.json';harmonic=json.loads(harmonicpath.read_text());PATHS.add(harmonicpath)
        for e,mass in enumerate(harmonic['harmonic_basis'][column]):values[e][0]=(mass% (1<<(P//8)),)+(0,)*7
        result=metadata(P,column,seed);inputfile=save_binary(outstem,'input',values,P)
        result.update(kind='operator_input',purpose='seed_extend',input_count=seed,operator_input_file=inputfile,
            checkpoint_files=[inputfile],seed_stem=args.seed,correction_history=[],truncated_plan_controls=l.controls())
    else:
        previous,previouspath=read(args.previous);P=previous['working_precision_pi'];column=previous['harmonic_basis_column']
        result=metadata(P,column,previous['seed_precision_pi']);result['seed_stem']=previous['seed_stem']
        result['correction_history']=previous['correction_history'];engine=Engine(P)
        if phase=='sweep':
            assert 0<=args.first<=args.last<174
            if previous['kind']=='checkpoint':
                assert previous['residual_lower_bound_pi']==P and args.backend=='GMP'
                values=state(previous);purpose='verify'
            else:
                assert previous['kind']=='operator_input' and args.backend=='FLINT'
                values=binary(previous['operator_input_file'],174,previous['input_count'],P//8);purpose=previous['purpose']
            answer=engine.apply(values,args.first,args.last,args.backend)
            output=save_binary(outstem,'operator',answer,P)
            result.update(kind='operator_chunk',purpose=purpose,first_state=args.first,last_state=args.last,
                input_metadata=source(previouspath),backend=args.backend,checkpoint_files=[output])
        elif phase=='seed-low':
            assert previous['purpose']=='seed_extend'
            values,inventory=assemble(args.previous,args.chunks,'FLINT')
            low=engine.low_solve(values,P//8)
            for e in range(174):values[e][1:R+1]=low[e]
            check_old_low(result,values)
            output=save_binary(outstem,'state',values,P)
            result.update(kind='operator_input',purpose='seed_residual',state_file=output,operator_input_file=output,
                input_count=P,checkpoint_files=[output],seed_extension_prefix=args.chunks,
                seed_input_stem=args.previous,assembled_sweep=inventory)
        elif phase in ('finish-seed','finish-step'):
            purpose='seed_residual' if phase=='finish-seed' else 'correction'
            assert previous['purpose']==purpose
            values=state(previous);applied,inventory=assemble(args.previous,args.chunks,'FLINT')
            if phase=='finish-seed':
                residual=b.Algebra(P//8).sub(applied,values)
                assert all(x==ZERO for row in residual for x in row[:R+1])
                assert l.value(residual,P)>=previous['seed_precision_pi']
            else:
                correction=binary(previous['operator_input_file'],174,P,P//8)
                assert all(row[0]==ZERO for row in applied)
                assert all(row[1:R+1]==correction[e][1:R+1] for e,row in enumerate(applied))
                residual=applied
                for row in residual:row[:R+1]=[ZERO]*(R+1)
                before=previous['before_pi'];after=l.value(residual,P);assert after>=min(P,before+R+1)
                result['correction_history']=previous['correction_history']+[{'before_pi':before,'after_pi':after}]
            sf=save_binary(outstem,'state',values,P);rf=save_binary(outstem,'residual',residual,P)
            result.update(kind='checkpoint',state_file=sf,residual_file=rf,checkpoint_files=[sf,rf],
                residual_lower_bound_pi=l.value(residual,P),assembled_sweep=inventory,
                seed_extension_prefix=previous['seed_extension_prefix'],seed_input_stem=previous['seed_input_stem'])
        elif phase=='prepare-step':
            assert previous['kind']=='checkpoint';values=state(previous)
            residual=binary(previous['residual_file'],174,P,P//8);before=l.value(residual,P)
            assert before==previous['residual_lower_bound_pi'] and previous['seed_precision_pi']<=before<P
            assert all(x==ZERO for row in residual for x in row[:R+1])
            shift=before//8;bits=P//8-shift
            assert all(not(c&((1<<shift)-1)) for row in residual for x in row for c in x)
            reduced=[[tuple(c>>shift for c in x) for x in row] for row in residual]
            low=engine.low_solve(reduced,bits)
            for e in range(174):reduced[e][1:R+1]=low[e]
            correction=[[tuple(c<<shift for c in x) for x in row] for row in reduced]
            values=b.Algebra(P//8).add(values,correction)
            sf=save_binary(outstem,'state',values,P);cf=save_binary(outstem,'correction',correction,P)
            result.update(kind='operator_input',purpose='correction',state_file=sf,operator_input_file=cf,
                input_count=P,before_pi=before,checkpoint_files=[sf,cf],
                seed_extension_prefix=previous['seed_extension_prefix'],seed_input_stem=previous['seed_input_stem'])
        elif phase=='finish-verify':
            assert previous['kind']=='checkpoint' and previous['residual_lower_bound_pi']==P
            values=state(previous);applied,inventory=assemble(args.previous,args.chunks,'GMP');assert applied==values
            old_count=check_old_low(result,values)
            extended,_=assemble(previous['seed_input_stem'],previous['seed_extension_prefix'],'FLINT')
            mask=(1<<(previous['seed_precision_pi']//8))-1
            assert b.reduce(values,mask)==b.reduce(extended,mask)
            sf=save_binary(outstem,'state',values,P);rf=save_binary(outstem,'residual',[[ZERO]*P for _ in range(174)],P)
            result.update(kind='checkpoint',state_file=sf,residual_file=rf,checkpoint_files=[sf,rf],
                residual_lower_bound_pi=P,assembled_sweep=inventory,actual_moment_precision_increased=True,
                seed_extension_prefix=previous['seed_extension_prefix'],seed_input_stem=previous['seed_input_stem'],
                certificate={'original_full_residual_zero':True,'actual_new_precision_pi':P,
                    'scalar_coefficients_checked':174*P*8,'frozen_old_low_scalar_overlaps_checked':old_count,
                    'old_precision_extended_scalar_overlaps_checked':174*P*8,
                    'full_residual_uses_different_polynomial_backend_from_lift':True})
        else:raise AssertionError(phase)
        times=engine.times
    PATHS.update([Path(__file__),Path(l.__file__),Path(f.__file__),Path(b.__file__),Path(p.__file__),f.LIBRARY])
    result.update(phase=phase,timings=times,wall_seconds=time.monotonic()-start,
        sources=[source(x) for x in sorted(PATHS)])
    print('STAGED_PHASE|'+json.dumps({k:result[k] for k in ['phase','working_precision_pi','wall_seconds']}|
        {k:result[k] for k in ['residual_lower_bound_pi','before_pi','assembled_sweep'] if k in result}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',required=True,choices=['init','sweep','seed-low','finish-seed','prepare-step','finish-step','finish-verify'])
    parser.add_argument('--precision',type=int,default=800);parser.add_argument('--seed')
    parser.add_argument('--previous');parser.add_argument('--chunks');parser.add_argument('--output',required=True)
    parser.add_argument('--first',type=int);parser.add_argument('--last',type=int)
    parser.add_argument('--backend',choices=['FLINT','GMP'],default='FLINT');args=parser.parse_args()
    assert re.fullmatch(r'[A-Za-z0-9_-]+',args.output)
    out=DATA/(args.output+'.json');assert not out.exists()
    out.write_text(json.dumps(run(args),indent=2)+'\n')
    print('PASS|489_DYADIC_STAGED_LIFT',flush=True)

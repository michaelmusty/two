"""D123 shrink the active correction band on the actual P=800 pilot.

Low moments 0..32 retain full precision. Higher moment k is stored modulo
pi^(P-k). Corrections of valuation u need only high indices k<P-u;
after low elimination the next active band ends at P-u-33. All phases
compare their result with the frozen uniform calculation, after computing
it. The saved P=800 seed is an input: this costs the correction stage,
not a replacement seed construction or a complete target-size solve.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('staged',ROOT/'dembele/pari/489_dyadic_staged_lift.py')
h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
P,R=800,32


def bits(k,i):return P//8 if k<=R else max(0,(P-k-i+7)//8)
MASKS=[tuple((1<<bits(k,i))-1 for i in range(8)) for k in range(P)]


def project(values):
    return [[tuple(c&m for c,m in zip(x,MASKS[k])) for k,x in enumerate(edge)] for edge in values]


def write_state(stem,values):
    path=DATA/(stem+'_state.bin');assert not path.exists()
    raw=b''.join(c.to_bytes((bits(k,i)+7)//8,'little')
        for edge in values for k,row in enumerate(edge) for i,c in enumerate(row))
    path.write_bytes(raw);return h.source(path)


def read_state(packet):
    file=packet['state_file'];assert h.source(file['path'])==file;h.PATHS.add(Path(file['path']))
    raw=Path(file['path']).read_bytes();offset=0;values=[]
    for e in range(174):
        edge=[]
        for k in range(P):
            row=[]
            for i in range(8):
                width=(bits(k,i)+7)//8;c=int.from_bytes(raw[offset:offset+width],'little')
                assert c<=MASKS[k][i];offset+=width;row.append(c)
            edge.append(tuple(row))
        values.append(edge)
    assert offset==len(raw);return values


def write_residual(stem,values,u):
    shift=u//8;bitcount=P//8-shift
    assert h.l.value(values,P)>=u
    assert all(c&((1<<shift)-1)==0 for edge in values for x in edge for c in x)
    reduced=[[tuple(c>>shift for c in x) for x in edge] for edge in values]
    path=DATA/(stem+'_residual.bin');assert not path.exists()
    path.write_bytes(h.b.pack(reduced,bitcount))
    return h.source(path),shift,bitcount


def read_residual(packet):
    values=h.binary(packet['residual_file'],174,packet['active_moment_count'],packet['residual_modulus_bits'])
    return [[tuple(c<<packet['residual_power_of_two_shift'] for c in x) for x in edge] for edge in values]


def apply_band(engine,correction,count):
    started=time.monotonic();u=h.l.value(correction,P);shift=u//8;bitcount=P//8-shift
    cut=min(len(correction[0]),8*bitcount);ring=h.f.Ring(bitcount);plans={};result=[]
    reduced=[[tuple(c>>shift for c in x) for x in edge[:cut]] for edge in correction]
    assert all(c&((1<<shift)-1)==0 for edge in correction for x in edge for c in x)
    for e in range(174):
        total=[h.ZERO]*count
        for branch,j in enumerate(engine.targets[e]):
            pars=tuple(tuple(c&ring.mask for c in x) for x in engine.params[e][branch])
            if pars not in plans:plans[pars]=h.l.Plan(ring,*pars,cut,count)
            total=ring.padd(total,plans[pars].apply(reduced[j]))
        result.append([tuple(c<<shift for c in x) for x in total])
    engine.times.append({'operation':'shrinking_original_transport','backend':'FLINT',
        'input_valuation_pi':u,'modulus_bits':bitcount,'input_count':cut,'output_count':count,
        'distinct_prepared_maps':len(plans),'seconds':time.monotonic()-started})
    return result


def reference_check(values,residual,step):
    stem='dyadic_staged_P800_col00_'+('seed' if step==0 else f'step{step:02d}')+'_d123'
    packet,path=h.read(stem);reference=h.state(packet)
    assert project(reference)==values
    count=len(residual[0]);saved=h.binary(packet['residual_file'],174,P,P//8)
    assert project([edge[:count] for edge in saved])==residual
    return {'reference':h.source(path),'state_scalar_overlaps':174*P*8,
        'residual_scalar_overlaps':174*count*8}


def run(args):
    started=time.monotonic();engine=h.Engine(P);step=0
    result={'status':'pass','milestone':'D123','phase':args.phase,'working_precision_pi':P,
        'eliminated_positive_moments':R,'harmonic_basis_column':0,
        'uses_frozen_uniform_seed':True,'new_precision_beyond_existing_P800_column':False,
        'full_sixteen_column_bank_precision_pi':400,'target_field_polynomial_constructed':False}
    if args.phase=='init':
        packet,path=h.read('dyadic_staged_P800_col00_seed_d123')
        u=packet['residual_lower_bound_pi'];assert u==400
        values=project(h.state(packet));count=P-u
        original=h.binary(packet['residual_file'],174,P,P//8)
        residual=project([edge[:count] for edge in original])
        assert all(x==h.ZERO for edge in residual for x in edge[:R+1])
        history=[];result['seed_metadata']=h.source(path)
    else:
        previous,path=h.read(args.previous);values=read_state(previous)
        result['previous_metadata']=h.source(path);step=previous['correction_steps']
        u=previous['weighted_residual_lower_bound_pi'];count=previous['active_moment_count']
        residual=read_residual(previous);assert h.l.value(residual,P)>=u
        assert all(x==h.ZERO for edge in residual for x in edge[:R+1])
        assert count==max(R+1,P-u)
        history=previous['correction_history']
        if args.phase=='step':
            assert count>R+1
            shift=u//8;bitcount=P//8-shift
            reduced=[[tuple(c>>shift for c in x) for x in edge] for edge in residual]
            low=engine.low_solve(reduced,bitcount)
            for e in range(174):reduced[e][1:R+1]=low[e]
            correction=[[tuple(c<<shift for c in x) for x in edge] for edge in reduced]
            assert h.l.value(correction,P)>=u
            for e in range(174):
                for k,x in enumerate(correction[e]):
                    values[e][k]=tuple((a+c)&m for a,c,m in zip(values[e][k],x,MASKS[k]))
            newu=min(P,u+R+1);newcount=max(R+1,P-newu)
            applied=apply_band(engine,correction,newcount)
            assert all(edge[:R+1]==correction[e][:R+1] for e,edge in enumerate(applied))
            for edge in applied:edge[:R+1]=[h.ZERO]*(R+1)
            residual=project(applied);assert h.l.value(residual,P)>=newu
            history=history+[{'before_pi':u,'after_pi':newu,'input_moments':count,'output_moments':newcount}]
            step+=1;u=newu;count=newcount
        elif args.phase=='finish':
            assert count==R+1 and u+R+1>=P and step==12
            assert all(x==h.ZERO for edge in residual for x in edge)
            reconstructed=engine.apply(values,0,173,'GMP')
            assert project(reconstructed)==values
            final,finalpath=h.read('dyadic_staged_P800_col00_verified_d123')
            assert final['certificate']['original_full_residual_zero'] and reconstructed==h.state(final)
            file=h.save_binary(args.output,'reconstructed',reconstructed,P)
            result.update(correction_steps=step,correction_history=history,
                weighted_residual_condition_checked=True,full_precision_reconstruction_equals_verified_column=True,
                reconstructed_scalar_coefficients_checked=174*P*8,original_operator_backend='GMP',
                frozen_reference_metadata=h.source(finalpath),checkpoint_files=[file],
                final_active_moment_count=count,final_weighted_residual_lower_bound_pi=u)
        else:raise AssertionError(args.phase)
    if args.phase!='finish':
        comparison=reference_check(values,residual,step)
        statefile=write_state(args.output,values);residualfile,shift,bitcount=write_residual(args.output,residual,u)
        result.update(correction_steps=step,correction_history=history,active_moment_count=count,
            weighted_residual_lower_bound_pi=u,state_file=statefile,residual_file=residualfile,
            state_layout='full P for moments 0..32; pi^(P-k) for k>=33; coordinate-specific bit masks',
            residual_power_of_two_shift=shift,residual_modulus_bits=bitcount,
            checkpoint_files=[statefile,residualfile],frozen_uniform_comparison=comparison,
            state_bytes=Path(statefile['path']).stat().st_size,residual_bytes=Path(residualfile['path']).stat().st_size)
    h.PATHS.update([Path(__file__),Path(h.__file__)])
    result.update(timings=engine.times,wall_seconds=time.monotonic()-started,
        sources=[h.source(path) for path in sorted(h.PATHS)])
    print('SHRINKING_PHASE|'+json.dumps({k:result[k] for k in ['phase','correction_steps','wall_seconds']}|
        {k:result[k] for k in ['active_moment_count','weighted_residual_lower_bound_pi'] if k in result}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--phase',choices=['init','step','finish'],required=True)
    parser.add_argument('--previous');parser.add_argument('--output',required=True);args=parser.parse_args()
    out=DATA/(args.output+'.json');assert not out.exists()
    out.write_text(json.dumps(run(args),indent=2)+'\n');print('PASS|493_DYADIC_SHRINKING_SCHUR',flush=True)

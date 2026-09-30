"""D127 actual P=1600 column-1 refinement with explicitly transient payloads.

Arithmetic follows frozen 505. Sweeps selectively decode child states;
low solves stream 1226 factor blocks and prepare one map at a time.
Only the new marked scratch namespace is mutable. Permanent phase metadata,
logs and receipts remain frozen; retired payload hashes are historical.
Serial assembly/preparation still decode their needed complete arrays;
this pilot is not a target-size RAM or full-solve cost certificate.
"""
import argparse
import fcntl
import os
import re
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

ROOT=Path(__file__).resolve().parents[2];META=ROOT/'dembele/data/computed'
DATA=META/'dyadic_rolling_scratch_col01_d127';CAP=512*(1<<20)
s=importlib.util.spec_from_file_location('staged',ROOT/'dembele/pari/489_dyadic_staged_lift.py')
h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
b,l,f,p=h.b,h.l,h.f,h.p;R=32;ZERO=b.ZERO
s=importlib.util.spec_from_file_location('adaptive',ROOT/'dembele/pari/503_dyadic_adaptive_kernel_control.py')
a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
s=importlib.util.spec_from_file_location('streamed',ROOT/'dembele/pari/516_dyadic_factor_and_map_controls.py')
c=importlib.util.module_from_spec(s);s.loader.exec_module(c);q=c.q


def scratch_bytes():
    assert DATA.is_dir() and not DATA.is_symlink()
    assert not (DATA/'SEALED.json').exists()
    owner=json.loads((DATA/'OWNER.json').read_text())
    assert owner['namespace']=='D127-column1' and owner['driver']==h.source(Path(__file__))
    paths=list(DATA.iterdir());assert all(p.is_file() and not p.is_symlink() for p in paths)
    return sum(p.stat().st_size for p in paths)


def budget_write(path,raw):
    assert path.parent==DATA and path.suffix=='.bin' and not path.exists()
    with (DATA/'.write.lock').open('a+b') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        before=scratch_bytes();assert before+len(raw)<=CAP,(before,len(raw),CAP)
        with path.open('xb') as file:
            file.write(raw);file.flush();os.fsync(file.fileno())
        assert path.stat().st_size==len(raw) and scratch_bytes()<=CAP



def peak_rss():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)


def bits(P,k,i):return P//8 if k<=R else max(0,(P-k-i+7)//8)


@lru_cache(None)
def masks(P):return [tuple((1<<bits(P,k,i))-1 for i in range(8)) for k in range(P)]


def project(values,P):
    mask=masks(P)
    return [[tuple(c&m for c,m in zip(x,mask[k])) for k,x in enumerate(edge)] for edge in values]


def weighted_file(stem,values,P):
    path=DATA/(stem+'_state.bin');assert not path.exists();raw=bytearray()
    for edge in values:
        assert len(edge)==P
        for k,row in enumerate(edge):
            for i,c in enumerate(row):
                assert 0<=c<1<<bits(P,k,i);raw.extend(c.to_bytes((bits(P,k,i)+7)//8,'little'))
    budget_write(path,raw);return h.source(path)


def weighted_state(packet):
    P=packet['working_precision_pi'];file=packet['state_file']
    assert h.source(file['path'])==file;h.PATHS.add(Path(file['path']))
    raw=Path(file['path']).read_bytes();offset=0;values=[]
    for e in range(174):
        edge=[]
        for k in range(P):
            row=[]
            for i in range(8):
                bitcount=bits(P,k,i);width=(bitcount+7)//8
                c=int.from_bytes(raw[offset:offset+width],'little');offset+=width
                assert c<1<<bitcount;row.append(c)
            edge.append(tuple(row))
        values.append(edge)
    assert offset==len(raw);return values


def scaled_file(stem,label,values,P,shift):
    assert 0<=shift<P//8
    assert all(c&((1<<shift)-1)==0 for edge in values for x in edge for c in x)
    reduced=[[tuple(c>>shift for c in x) for x in edge] for edge in values]
    path=DATA/(stem+'_'+label+'.bin');assert not path.exists()
    budget_write(path,b.pack(reduced,P//8-shift));return h.source(path)


def scaled_values(file,nr,nc,P,shift):
    values=h.binary(file,nr,nc,P//8-shift)
    return [[tuple(c<<shift for c in x) for x in edge] for edge in values]


def seed_file(packet):
    file=packet.get('state_file',packet['checkpoint_files'][0])
    assert Path(file['path']).name.endswith('_state.bin')
    assert packet['certificate']['original_full_residual_zero']
    return file


class Engine(h.Engine):
    def __init__(self,P):
        assert P==1600
        super().__init__(P)
        controls,_=h.read('dyadic_adaptive_kernel_control_d124')
        for path in (Path(a.__file__),a.CSOURCE,a.LIBRARY):
            expected=[row for row in controls['sources'] if Path(row['path'])==path.resolve()]
            assert len(expected)==1 and h.source(path)==expected[0]
            h.PATHS.add(path)

    def solve_rhs(self,rhs,bitcount):
        started=time.monotonic();reader=c.FactorReader(bitcount)
        answer=reader.solve(rhs,b.Algebra(bitcount));reader.close()
        assert reader.decoded_blocks==1226
        h.PATHS.update(c.h.PATHS)
        self.times.append({'operation':'streamed_low_solve','modulus_bits':bitcount,
            'factor_blocks_decoded':1226,'maximum_decoded_factor_blocks':1,
            'factor_read_decode_seconds':reader.read_seconds,'seconds':time.monotonic()-started})
        return answer

    def low_solve(self,moment,bitcount):
        started=time.monotonic();cut=min(len(moment[0]),8*bitcount)
        if 8*bitcount<=R+1 and all(row[0]==ZERO for row in moment):return [[ZERO]*R for _ in range(174)]
        ring=a.Ring(bitcount);groups={};totals=[[ZERO]*(R+1) for _ in range(174)]
        for e in range(174):
            for branch,j in enumerate(self.targets[e]):
                pars=tuple(tuple(v&ring.mask for v in x) for x in self.params[e][branch])
                groups.setdefault(pars,[]).append((e,j))
        for pars,destinations in groups.items():
            plan=l.Plan(ring,*pars,cut,R+1)
            for e,j in destinations:
                values=[x if k==0 or k>R else ZERO for k,x in enumerate(moment[j][:cut])]
                totals[e]=ring.padd(totals[e],plan.apply(values))
            del plan
        rhs=[[[x] for x in edge[1:]] for edge in totals]
        answer=self.solve_rhs(rhs,bitcount)
        self.times.append({'operation':'low_solve_with_rhs','backend':'ADAPTIVE','modulus_bits':bitcount,
            'distinct_maps':len(groups),'maximum_prepared_maps_held':1,'seconds':time.monotonic()-started})
        return [[row[0] for row in edge] for edge in answer]

    def apply_selective(self,file,count,weighted,shift,rows,first,last,backend,zero_low=False):
        started=time.monotonic();P=self.P;bitcount=P//8-shift;cut=min(count,8*bitcount)
        assert not weighted or shift==0
        reader=q.StateReader(file,count,bitcount,weighted_precision=P if weighted else None)
        ring=(p.Ring if backend=='GMP' else a.Ring)(bitcount);out=[];prepared=0
        for e in range(first,last+1):
            total=[ZERO]*rows
            for branch,j in enumerate(self.targets[e]):
                values=reader.row(j,cut)
                if zero_low:values[1:R+1]=[ZERO]*min(R,max(0,cut-1))
                pars=tuple(tuple(v&ring.mask for v in x) for x in self.params[e][branch])
                plan=l.Plan(ring,*pars,cut,rows);prepared+=1
                total=ring.padd(total,plan.apply(values));del plan,values
            assert len(total)==rows;out.append([tuple(v<<shift for v in x) for x in total])
        reader.close();h.PATHS.update(c.h.PATHS)
        self.times.append({'operation':'selective_original_operator_chunk','backend':backend,
            'first_state':first,'last_state':last,'known_binary_shift':shift,'modulus_bits':bitcount,
            'input_count':cut,'output_count':rows,'zero_positive_low_inputs':zero_low,
            'maximum_decoded_input_rows':1,'maximum_prepared_maps_held':1,'prepared_maps':prepared,
            'reader_statistics':reader.stats(),'seconds':time.monotonic()-started})
        return out,shift


def assemble(previous,prefix,purpose,backend):
    packet,path=h.read(previous);P=packet['working_precision_pi'];answer=[];cursor=0;seconds=0;count=None
    files=sorted(META.glob(prefix+'_e[0-9][0-9][0-9]_[0-9][0-9][0-9].json'));assert files
    for file in files:
        row,_=h.read(file.stem)
        assert row['kind']=='operator_chunk' and row['input_metadata']==h.source(path)
        assert row['purpose']==purpose and row['backend']==backend and row['working_precision_pi']==P
        assert row['first_state']==cursor and cursor<=row['last_state']<174
        if count is None:count=row['output_count']
        assert row['output_count']==count
        nr=row['last_state']-cursor+1
        answer+=scaled_values(row['checkpoint_files'][0],nr,count,P,row['operator_power_of_two_shift'])
        cursor+=nr;seconds+=row['timings'][0]['seconds']
    assert cursor==174
    return answer,{'chunks':len(files),'states':cursor,'output_count':count,'purpose':purpose,
        'summed_operator_seconds':seconds,'input_metadata':h.source(path)}


def check_old(packet,values):
    old,_=h.read(packet['seed_stem']);oldP=old['working_precision_pi'];mask=(1<<(oldP//8))-1
    original=h.binary(seed_file(old),174,oldP,oldP//8)
    assert b.reduce([edge[:oldP] for edge in values],mask)==original
    return 174*oldP*8


def baseline(result,previous):
    for key in ['working_precision_pi','seed_precision_pi','harmonic_basis_column','seed_stem','correction_history',
                'seed_input_stem','seed_extension_prefix']:
        if key in previous:result[key]=previous[key]


def residual_file(result,stem,values,u):
    P=result['working_precision_pi'];assert l.value(values,P)>=u
    shift=u//8;file=scaled_file(stem,'residual',values,P,shift)
    result.update(residual_file=file,residual_power_of_two_shift=shift,active_moment_count=len(values[0]),
        weighted_residual_lower_bound_pi=u)
    return file


def run(args):
    start=time.monotonic();phase=args.phase;stem=args.output;initial_bytes=scratch_bytes()
    result={'status':'pass','milestone':'D127','phase':phase,'eliminated_positive_moments':R,
        'actual_moment_precision_increased':False,'full_sixteen_column_bank_precision_pi':800}
    if phase=='init':
        old,path=h.read(args.seed);oldP=old['working_precision_pi'];P=args.precision
        assert P==1600 and oldP==800 and old['certificate']['original_full_residual_zero']
        values=h.binary(seed_file(old),174,oldP,oldP//8)
        masses,masspath=h.read('dyadic_harmonic_certificate_d111');column=old['harmonic_basis_column']
        assert column==1
        for e,mass in enumerate(masses['harmonic_basis'][column]):values[e][0]=(mass&((1<<(P//8))-1),)+(0,)*7
        file=scaled_file(stem,'input',values,P,0)
        result.update(working_precision_pi=P,seed_precision_pi=oldP,harmonic_basis_column=column,seed_stem=args.seed,
            seed_input_stem=stem,kind='initial_input',input_count=oldP,operator_input_file=file,
            correction_history=[],checkpoint_files=[file],verified_seed_metadata=h.source(path))
        engine=None
    else:
        previous,previouspath=h.read(args.previous);baseline(result,previous);P=result['working_precision_pi'];engine=Engine(P)
        result['previous_metadata']=h.source(previouspath)
        if phase=='sweep':
            assert 0<=args.first<=args.last<174;purpose=args.purpose
            backend='GMP' if purpose in ('reconstruct','verify') else 'ADAPTIVE'
            weighted=False;zero_low=False;shift=0
            if purpose=='extend':
                assert previous['kind']=='initial_input'
                file=previous['operator_input_file'];count=previous['input_count'];rows=P
            elif purpose in ('seed-low-rhs','seed-residual'):
                assert previous['kind']==('weighted_seed' if purpose=='seed-low-rhs' else 'weighted_low_seed')
                file=previous['state_file'];count=P;weighted=True;zero_low=purpose=='seed-low-rhs'
                rows=R+1 if zero_low else max(R+1,P-previous['seed_precision_pi'])
            elif purpose=='correction':
                assert previous['kind']=='prepared_correction'
                file=previous['operator_input_file'];count=previous['input_count']
                shift=previous['correction_power_of_two_shift'];rows=previous['next_active_moment_count']
            elif purpose=='reconstruct':
                assert previous['kind']=='checkpoint' and previous['active_moment_count']==R+1
                file=previous['state_file'];count=P;weighted=True;rows=P
            elif purpose=='verify':
                assert previous['kind']=='reconstructed'
                file=previous['state_file'];count=P;rows=P
            else:raise AssertionError(purpose)
            applied,shift=engine.apply_selective(file,count,weighted,shift,rows,args.first,args.last,backend,zero_low)
            file=scaled_file(stem,'operator',applied,P,shift)
            result.update(kind='operator_chunk',purpose=purpose,input_metadata=h.source(previouspath),backend=backend,
                first_state=args.first,last_state=args.last,output_count=rows,operator_power_of_two_shift=shift,
                checkpoint_files=[file])
        elif phase=='seed-assemble':
            assert previous['kind']=='initial_input'
            applied,inventory=assemble(args.previous,args.chunks,'extend','ADAPTIVE');assert inventory['output_count']==P
            check_old(result,applied);values=project(applied,P);file=weighted_file(stem,values,P)
            result.update(kind='weighted_seed',state_file=file,checkpoint_files=[file],assembled_sweep=inventory,
                seed_extension_prefix=args.chunks)
        elif phase=='seed-low-finish':
            assert previous['kind']=='weighted_seed'
            rhs,inventory=assemble(args.previous,args.chunks,'seed-low-rhs','ADAPTIVE');assert inventory['output_count']==R+1
            started=time.monotonic()
            answer=engine.solve_rhs([[[x] for x in edge[1:]] for edge in rhs],P//8)
            engine.times.append({'operation':'seed_low_solve_from_saved_rhs','seconds':time.monotonic()-started})
            values=weighted_state(previous)
            for e in range(174):values[e][1:R+1]=[row[0] for row in answer[e]]
            check_old(result,values);file=weighted_file(stem,values,P)
            result.update(kind='weighted_low_seed',state_file=file,checkpoint_files=[file],assembled_sweep=inventory)
        elif phase=='finish-seed':
            assert previous['kind']=='weighted_low_seed'
            applied,inventory=assemble(args.previous,args.chunks,'seed-residual','ADAPTIVE')
            values=weighted_state(previous);count=max(R+1,P-previous['seed_precision_pi'])
            assert inventory['output_count']==count
            residual=project(b.Algebra(P//8).sub(applied,[edge[:count] for edge in values]),P)
            assert all(x==ZERO for edge in residual for x in edge[:R+1])
            rf=residual_file(result,stem,residual,previous['seed_precision_pi']);sf=previous['state_file']
            result.update(kind='checkpoint',state_file=sf,checkpoint_files=[sf,rf],assembled_sweep=inventory)
        elif phase=='prepare-step':
            assert previous['kind']=='checkpoint';u=previous['weighted_residual_lower_bound_pi'];count=previous['active_moment_count']
            assert count==max(R+1,P-u) and count>R+1
            residual=scaled_values(previous['residual_file'],174,count,P,previous['residual_power_of_two_shift'])
            assert l.value(residual,P)>=u and all(x==ZERO for edge in residual for x in edge[:R+1])
            shift=u//8;bitcount=P//8-shift
            reduced=[[tuple(c>>shift for c in x) for x in edge] for edge in residual]
            low=engine.low_solve(reduced,bitcount)
            for e in range(174):reduced[e][1:R+1]=low[e]
            correction=[[tuple(c<<shift for c in x) for x in edge] for edge in reduced]
            assert l.value(correction,P)>=u
            values=weighted_state(previous);mask=masks(P)
            for e in range(174):
                for k,x in enumerate(correction[e]):values[e][k]=tuple((a+c)&m for a,c,m in zip(values[e][k],x,mask[k]))
            sf=weighted_file(stem,values,P);cf=scaled_file(stem,'correction',correction,P,shift)
            result.update(kind='prepared_correction',state_file=sf,operator_input_file=cf,input_count=count,
                before_pi=u,after_pi=min(P,u+R+1),next_active_moment_count=max(R+1,P-u-R-1),
                correction_power_of_two_shift=shift,checkpoint_files=[sf,cf])
        elif phase=='finish-step':
            assert previous['kind']=='prepared_correction'
            applied,inventory=assemble(args.previous,args.chunks,'correction','ADAPTIVE')
            correction=scaled_values(previous['operator_input_file'],174,previous['input_count'],P,previous['correction_power_of_two_shift'])
            assert inventory['output_count']==previous['next_active_moment_count']
            assert all(edge[:R+1]==correction[e][:R+1] for e,edge in enumerate(applied))
            for edge in applied:edge[:R+1]=[ZERO]*(R+1)
            residual=project(applied,P);u=previous['after_pi']
            rf=residual_file(result,stem,residual,u);sf=previous['state_file']
            history=previous['correction_history']+[{'before_pi':previous['before_pi'],'after_pi':u,
                'input_moments':previous['input_count'],'output_moments':previous['next_active_moment_count']}]
            result.update(kind='checkpoint',state_file=sf,checkpoint_files=[sf,rf],correction_history=history,assembled_sweep=inventory)
        elif phase=='finish-reconstruct':
            assert previous['kind']=='checkpoint' and previous['active_moment_count']==R+1
            assert previous['weighted_residual_lower_bound_pi']+R+1>=P
            applied,inventory=assemble(args.previous,args.chunks,'reconstruct','GMP');assert inventory['output_count']==P
            values=weighted_state(previous);assert project(applied,P)==values
            old_count=check_old(result,applied)
            extended,old_inventory=assemble(previous['seed_input_stem'],previous['seed_extension_prefix'],'extend','ADAPTIVE')
            mask=(1<<(previous['seed_precision_pi']//8))-1;assert b.reduce(applied,mask)==b.reduce(extended,mask)
            file=scaled_file(stem,'state',applied,P,0)
            result.update(kind='reconstructed',state_file=file,checkpoint_files=[file],assembled_sweep=inventory,
                weighted_state_metadata=h.source(previouspath),weighted_residual_condition_checked=True,
                weighted_residual_scalar_checks=174*P*8,old_low_scalar_overlaps_checked=old_count,
                old_extended_scalar_overlaps_checked=174*P*8)
        elif phase=='finish-verify':
            assert previous['kind']=='reconstructed' and previous['weighted_residual_condition_checked']
            applied,inventory=assemble(args.previous,args.chunks,'verify','GMP');values=h.binary(previous['state_file'],174,P,P//8)
            assert inventory['output_count']==P and applied==values
            masses,_=h.read('dyadic_harmonic_certificate_d111')
            for e,mass in enumerate(masses['harmonic_basis'][previous['harmonic_basis_column']]):
                assert values[e][0]==(mass&((1<<(P//8))-1),)+(0,)*7
            residual=DATA/(stem+'_residual.bin');assert not residual.exists();length=174*P*8*((P//8+7)//8)
            budget_write(residual,bytes(length))
            rf=h.source(residual);sf=previous['state_file']
            result.update(kind='verified',state_file=sf,residual_file=rf,checkpoint_files=[sf,rf],
                residual_lower_bound_pi=P,actual_moment_precision_increased=True,assembled_sweep=inventory,
                weighted_state_metadata=previous['weighted_state_metadata'],
                certificate={'original_full_residual_zero':True,'actual_new_precision_pi':P,
                    'scalar_coefficients_checked':174*P*8,'weighted_residual_condition_checked':True,
                    'old_low_scalar_overlaps_checked':previous['old_low_scalar_overlaps_checked'],
                    'old_extended_scalar_overlaps_checked':previous['old_extended_scalar_overlaps_checked'],
                    'exact_masses_checked':174,'full_residual_uses_different_polynomial_backend_from_lift':True})
        else:raise AssertionError(phase)
    h.PATHS.update(c.h.PATHS)
    h.PATHS.update([Path(__file__),Path(h.__file__),Path(a.__file__),a.CSOURCE,a.LIBRARY,
        Path(c.__file__),Path(q.__file__),META/'dyadic_resource_controls_review_d126.json'])
    result.update(timings=engine.times if engine else [],wall_seconds=time.monotonic()-start,peak_rss_bytes=peak_rss(),
        scratch_bytes_before=initial_bytes,scratch_bytes_after=scratch_bytes(),scratch_limit_bytes=CAP,
        checkpoint_payloads_prospectively_transient=True,
        sources=[h.source(path) for path in sorted(h.PATHS) if not path.resolve().is_relative_to(DATA.resolve())])
    print('WEIGHTED_CHUNK_PHASE|'+json.dumps({k:result[k] for k in ['phase','working_precision_pi','wall_seconds','peak_rss_bytes']}|
        {k:result[k] for k in ['weighted_residual_lower_bound_pi','active_moment_count','before_pi'] if k in result}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',required=True,choices=['init','sweep','seed-assemble','seed-low-finish','finish-seed',
        'prepare-step','finish-step','finish-reconstruct','finish-verify'])
    parser.add_argument('--output',required=True);parser.add_argument('--previous');parser.add_argument('--chunks')
    parser.add_argument('--precision',type=int,default=1600);parser.add_argument('--seed')
    parser.add_argument('--purpose',choices=['extend','seed-low-rhs','seed-residual','correction','reconstruct','verify'])
    parser.add_argument('--first',type=int);parser.add_argument('--last',type=int);args=parser.parse_args()
    assert re.fullmatch(r'[A-Za-z0-9_-]+',args.output)
    out=META/(args.output+'.json');assert not out.exists()
    result=run(args);out.write_text(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(h.source(out)),flush=True)
    print('PASS|519_DYADIC_ROLLING_PRECISION_CHUNKS',flush=True)

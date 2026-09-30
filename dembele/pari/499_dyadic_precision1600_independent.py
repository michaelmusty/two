"""D124 bounded independent reviews of the actual P=1600 column.

Import only the separate integer quotient arithmetic/recurrence audit,
never the production solver or polynomial backend. Phases split costly
seed-tail recurrences, coarse values, and all weighted checkpoints.
"""
import argparse
import importlib.util
import json
from math import comb
from pathlib import Path
import resource
import sys
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('audit',ROOT/'dembele/pari/491_dyadic_staged_pilot_independent.py')
a=importlib.util.module_from_spec(s);s.loader.exec_module(a);r=a.r
PATHS={Path(__file__),Path(a.__file__),Path(r.__file__)};P=1600;R=32


def read(stem):
    path=DATA/(stem+'.json');PATHS.add(path);packet=json.loads(path.read_text());assert packet['status']=='pass'
    for file in packet.get('checkpoint_files',[]):assert r.source(file['path'])==file;PATHS.add(Path(file['path']))
    return packet


def uniform(file,nr,nc,bitcount):
    assert r.source(file['path'])==file;PATHS.add(Path(file['path']))
    values=a.binary(file['path'],nr,nc,8*bitcount)
    assert all(c<1<<bitcount for edge in values for row in edge for c in row)
    return values


def weighted(file):
    assert r.source(file['path'])==file;path=Path(file['path']);PATHS.add(path)
    raw=path.read_bytes();offset=0;out=[]
    for e in range(174):
        edge=[]
        for k in range(P):
            precision=P if k<=R else P-k;row=[]
            for i in range(8):
                needed=max(0,-((i-precision)//8));width=-(-needed//8)
                c=int.from_bytes(raw[offset:offset+width],'little');offset+=width
                assert c<1<<needed;row.append(c)
            edge.append(tuple(row))
        out.append(edge)
    assert offset==len(raw);return out


def states():
    packet=read('dyadic_weighted_P1600_col00_verified_d124');cert=packet['certificate']
    assert cert['original_full_residual_zero'] and cert['actual_new_precision_pi']==P
    assert cert['full_residual_uses_different_polynomial_backend_from_lift']
    values=uniform(packet['state_file'],174,P,P//8)
    path=Path(packet['residual_file']['path']);raw=path.read_bytes();assert len(raw)==174*P*8*25 and not any(raw)
    old=read('dyadic_staged_P800_col00_verified_d123');seed=uniform(old['state_file'],174,800,100)
    mask=(1<<100)-1;assert [[tuple(c&mask for c in x) for x in edge[:800]] for edge in values]==seed
    harmonic=read('dyadic_harmonic_certificate_d111')['harmonic_basis'][0];ring=r.Quotient(r.FP,P)
    for e,mass in enumerate(harmonic):assert values[e][0]==(mass&ring.mask,)+(0,)*7
    maps=read('dyadic_target_transports_d121')['transitions'];mapchecks=0
    for state in maps:
        for child in state['children']:
            aa,b,c=[ring.norm(x) for x in child['normalized_center'][:3]]
            assert child['normalized_error_pi']>=P
            assert ring.value(c)>=1 and ring.value(ring.sub(aa,ring.mul(b,c)))>=1;mapchecks+=1
    checked=0
    for e in (0,17,61,98,173):
        for n,x in a.recurrence(ring,maps,values,e,(1,2,33,64),P).items():assert x==values[e][n];checked+=8
    sweeps={}
    for path in DATA.glob('dyadic_weighted_P1600_col00_*_e[0-9][0-9][0-9]_[0-9][0-9][0-9].json'):
        row=read(path.stem);key=(row['input_metadata']['path'],row['purpose'])
        assert r.source(row['input_metadata']['path'])==row['input_metadata']
        sweeps.setdefault(key,[]).append((row['first_state'],row['last_state']))
    assert len(sweeps)==29
    for rows in sweeps.values():
        cursor=0
        for first,last in sorted(rows):assert first==cursor and last>=first;cursor=last+1
        assert cursor==174
    return {'production_full_original_residual_scalar_checks':174*P*8,'old_P800_low_scalar_overlaps':174*800*8,
        'exact_masses_checked':174,'independent_original_recurrence_scalar_checks':checked,
        'child_column_divisibility_checks':mapchecks,'complete_disjoint_sweeps_checked':len(sweeps)}


def seed_tail():
    old=read('dyadic_staged_P800_col00_verified_d123');seed=uniform(old['state_file'],174,800,100)
    packet=read('dyadic_weighted_P1600_col00_verified_d124');values=uniform(packet['state_file'],174,P,P//8)
    maps=read('dyadic_target_transports_d121')['transitions'];ring=r.Quotient(r.FP,800)
    degrees=(800,1199,1599);result=a.recurrence(ring,maps,seed,0,degrees,800)
    for n,x in result.items():assert x==ring.norm(values[0][n])
    # All reconstructed old-precision seed moments, beyond the sampled recurrence.
    cursor=0;count=0
    for path in sorted(DATA.glob('dyadic_weighted_P1600_col00_extend_d124_e[0-9][0-9][0-9]_[0-9][0-9][0-9].json')):
        row=read(path.stem);assert row['first_state']==cursor and row['operator_power_of_two_shift']==0
        nr=row['last_state']-cursor+1;extended=uniform(row['checkpoint_files'][0],nr,P,P//8)
        for i,edge in enumerate(extended):
            for k,x in enumerate(edge):assert ring.norm(x)==ring.norm(values[cursor+i][k]);count+=8
        cursor+=nr
    assert cursor==174
    return {'independent_high_seed_degrees':list(degrees),'independent_high_seed_scalar_checks':24,
        'all_old_precision_extended_seed_scalar_overlaps':count}


def coarse():
    cm=read('dyadic_CM_P1600_col00_d124');assert cm['coarse_error_beta']==[3232,3248,3232,3264]
    values=uniform(cm['checkpoint_files'][0],17,2*P,P//8)
    old=read('dyadic_staged_CM_P800_col00_d123');prior=uniform(old['checkpoint_files'][0],17,1600,100)
    mask=(1<<100)-1;assert [[tuple(c&mask for c in x) for x in edge[:1600]] for edge in values]==prior
    ring=r.Quotient(r.MP,3264);pi=ring.sub(ring.scale(ring.one,-2),ring.mul(ring.beta,ring.beta))
    q=ring.sub(tuple(r.MP[1:]),ring.beta);assert ring.mul(q,ring.beta)==pi
    powers=[ring.one]
    for _ in range(7):powers.append(ring.mul(powers[-1],pi))
    kernels=[]
    for order in range(4):
        n=2*order+2
        kernels.append([0]+[-sum(comb(n,i)*comb(n+k-i-1,k-i) for i in range(min(n,k)+1)) for k in range(1,2*P)])
    checked=0
    for ci,edge in enumerate(values):
        embedded=[]
        for row in edge:
            x=ring.zero
            for c,power in zip(row,powers):x=ring.add(x,ring.scale(power,c))
            embedded.append(x)
        for order,cs in enumerate(kernels):
            x=ring.zero
            for c,m in reversed(list(zip(cs,embedded))):x=ring.add(ring.mul(x,q),ring.scale(m,c))
            assert x==tuple(cm['CM_values'][ci]['coarse_coefficients_beta'][order])
            oldvalue=tuple(old['CM_values'][ci]['coarse_coefficients_beta'][order])
            assert ring.value(ring.sub(x,oldvalue))>=old['coarse_error_beta'][order];checked+=1
    return {'independent_coarse_values_checked':checked,'coarse_error_beta':cm['coarse_error_beta'],
        'old_CM_scalar_overlaps':17*1600*8,'new_CM_scalar_coefficients':17*2*P*8,'old_coarse_values_checked':68}


def weighted_review():
    packet=read('dyadic_weighted_P1600_col00_verified_d124');values=uniform(packet['state_file'],174,P,P//8)
    ring=r.Quotient(r.FP,P);state_checks=residual_checks=0;counts=[]
    for step in range(25):
        suffix='seed' if step==0 else f'step{step:02d}'
        row=read(f'dyadic_weighted_P1600_col00_{suffix}_d124');u=800+33*step
        assert row['weighted_residual_lower_bound_pi']==u
        nc=max(R+1,P-u);assert row['active_moment_count']==nc;counts.append(nc)
        center=weighted(row['state_file'])
        for e,edge in enumerate(center):
            assert edge[0]==values[e][0]
            for k,x in enumerate(edge):
                target=min(P,u+33) if k<=R else min(u,P-k)
                assert ring.value(ring.sub(x,values[e][k]))>=target,(step,e,k,target)
                state_checks+=8
        shift=row['residual_power_of_two_shift'];assert shift==u//8
        residual=uniform(row['residual_file'],174,nc,P//8-shift)
        for edge in residual:
            assert all(x==ring.zero for x in edge[:R+1])
            for x in edge:
                assert ring.value(tuple(c<<shift for c in x))>=u;residual_checks+=8
        if step%6==0:print(f'P1600_WEIGHTED_REVIEW|checkpoints={step+1}; state scalars={state_checks}',flush=True)
    assert counts[-1]==33 and all(x==ring.zero for edge in residual for x in edge)
    for e,edge in enumerate(center):
        for k,x in enumerate(edge):
            assert ring.value(ring.sub(x,values[e][k]))>=(P if k<=R else P-k)
    pilot=read('dyadic_weighted_pilot_P1600_col00_d124');assert pilot['correction_steps']==24 and pilot['completed_phases']==228
    before=800
    for step in pilot['correction_history']:
        assert step['before_pi']==before and step['after_pi']==before+33;before=step['after_pi']
    assert before==1592
    return {'all_weighted_state_scalar_checks':state_checks,'all_scaled_residual_scalar_checks':residual_checks,
        'weighted_checkpoints_checked':25,'active_moment_counts':counts,'uniform_low_error_gain_verified':33,
        'final_weighted_reference_scalar_checks':174*P*8,'all_twenty_four_correction_gains_checked':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--phase',required=True,choices=['states','seed','coarse','weighted']);args=parser.parse_args()
    out=DATA/f'dyadic_precision1600_audit_{args.phase}_d124.json';assert not out.exists();start=time.monotonic()
    cert={'states':states,'seed':seed_tail,'coarse':coarse,'weighted':weighted_review}[args.phase]()
    result={'status':'pass','milestone':'D124','phase':args.phase,'working_precision_pi':P,
        'full_sixteen_column_bank_precision_pi':400,'production_arithmetic_not_imported':True,'certificates':cert,
        'positive_exact_quadric_vanishing_proved':False,'candidate_identification_proved':False,
        'target_field_polynomial_constructed':False,'wall_seconds':time.monotonic()-start,
        'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
        'sources':[r.source(path) for path in sorted(PATHS)]}
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='sources'}),flush=True)
    print('PASS|499_DYADIC_PRECISION1600_INDEPENDENT',flush=True)

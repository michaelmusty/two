"""D127 independent finite arithmetic audit of the rolling P=1600 column.

Imports only separate integer quotient arithmetic. Retired intermediate
payloads are explicitly not replayed: final masses and original residual
supply the iteration-independent certificate proved in D125.
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
PATHS={Path(__file__),Path(a.__file__),Path(r.__file__)};P=1600;R=32;COL=1


def read(stem,retained=True):
    path=DATA/(stem+'.json');PATHS.add(path);packet=json.loads(path.read_text());assert packet['status']=='pass'
    if retained:
        for file in packet.get('checkpoint_files',[]):assert r.source(file['path'])==file;PATHS.add(Path(file['path']))
    else:assert packet['checkpoint_payloads_prospectively_transient']
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
    packet=read(f'dyadic_rolling_P1600_col{COL:02d}_verified_d127');cert=packet['certificate']
    assert cert['original_full_residual_zero'] and cert['actual_new_precision_pi']==P
    assert cert['full_residual_uses_different_polynomial_backend_from_lift']
    values=uniform(packet['state_file'],174,P,P//8)
    path=Path(packet['residual_file']['path']);raw=path.read_bytes();assert len(raw)==174*P*8*25 and not any(raw)
    old=read(f'dyadic_weighted_P800_col{COL:02d}_verified_d125');seed=uniform(old['state_file'],174,800,100)
    mask=(1<<100)-1;assert [[tuple(c&mask for c in x) for x in edge[:800]] for edge in values]==seed
    harmonic=read('dyadic_harmonic_certificate_d111')['harmonic_basis'][COL];ring=r.Quotient(r.FP,P)
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
    for path in DATA.glob(f'dyadic_rolling_P1600_col{COL:02d}_*_e[0-9][0-9][0-9]_[0-9][0-9][0-9].json'):
        row=read(path.stem,retained=False);key=(row['input_metadata']['path'],row['purpose'])
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
    old=read('dyadic_weighted_P800_col01_verified_d125')
    seed=uniform(old['state_file'],174,800,100)
    packet=read('dyadic_rolling_P1600_col01_verified_d127')
    values=uniform(packet['state_file'],174,P,P//8)
    maps=read('dyadic_target_transports_d121')['transitions'];ring=r.Quotient(r.FP,800)
    degrees=(800,1199,1599);result=a.recurrence(ring,maps,seed,0,degrees,800)
    for n,x in result.items():assert x==ring.norm(values[0][n])
    assert packet['certificate']['old_extended_scalar_overlaps_checked']==2227200
    return {'independent_high_seed_degrees':list(degrees),'independent_high_seed_scalar_checks':24,
        'production_old_extended_scalar_overlaps':2227200,
        'retired_seed_extension_payloads_replayed':False}


def coarse():
    cm=read(f'dyadic_rolling_CM_P1600_col{COL:02d}_d127');assert cm['coarse_error_beta']==[3232,3248,3232,3264]
    values=uniform(cm['checkpoint_files'][0],17,2*P,P//8)
    oldstem=f'dyadic_direct_CM_P800_col{COL:02d}_d125';old=read(oldstem)
    prior=uniform(old['checkpoint_files'][0],17,1600,100)
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
    # Independent formal-series recurrence for sampled composed CM maps.
    state=read(f'dyadic_rolling_P1600_col{COL:02d}_verified_d127')
    actual=uniform(state['state_file'],174,P,P//8)
    transports=read('dyadic_target_transports_d121');maps=transports['transitions']
    charts=[x for x in transports['CM_charts'] if x['chart']=='A']
    small=r.Quotient(r.FP,P);cmchecks=0
    for ci in (0,8,16):
        A,B,C=[small.norm(x) for x in charts[ci]['normalized_center'][:3]]
        children=[]
        for child in maps[charts[ci]['target_edge']]['children']:
            aa,bb,cc=[small.norm(x) for x in child['normalized_center'][:3]]
            d=small.add(small.one,small.mul(C,bb));iv=small.one
            for _ in range(P.bit_length()):iv=small.mul(iv,small.sub(small.scale(small.one,2),small.mul(d,iv)))
            assert small.mul(d,iv)==small.one
            pars=[small.mul(small.add(small.mul(A,aa),small.mul(B,cc)),iv),
                small.mul(small.add(small.mul(A,bb),B),iv),small.mul(small.add(cc,small.mul(C,aa)),iv)]
            assert small.value(pars[2])>=1 and small.value(small.sub(pars[0],small.mul(pars[1],pars[2])))>=1
            children.append({'normalized_center':pars,'target_edge':child['target_edge']})
        totals=a.recurrence(small,[{'children':children}],actual,0,(1,2,7),P)
        for n,x in totals.items():assert x==values[ci][n];cmchecks+=8
    return {'independent_coarse_values_checked':checked,'coarse_error_beta':cm['coarse_error_beta'],
        'independent_CM_recurrence_scalar_checks':cmchecks,'old_CM_scalar_overlaps':17*1600*8,'new_CM_scalar_coefficients':17*2*P*8,'old_coarse_values_checked':68}


def weighted_review():
    packet=read('dyadic_rolling_P1600_col01_verified_d127')
    values=uniform(packet['state_file'],174,P,P//8);ring=r.Quotient(r.FP,P)
    row=read('dyadic_rolling_P1600_col01_step24_d127');center=weighted(row['state_file'])
    assert row['active_moment_count']==33 and row['weighted_residual_lower_bound_pi']==1592
    checks=0
    for e,edge in enumerate(center):
        assert edge[0]==values[e][0]
        for k,x in enumerate(edge):
            assert ring.value(ring.sub(x,values[e][k]))>=(P if k<=R else P-k)
            checks+=8
    residual=uniform(row['residual_file'],174,33,1)
    assert row['residual_power_of_two_shift']==199
    assert all(x==ring.zero for edge in residual for x in edge)
    pilot=read('dyadic_rolling_pilot_P1600_col01_d127')
    assert pilot['correction_steps']==24 and pilot['completed_phases']==228
    before=800
    for item in pilot['correction_history']:
        assert item['before_pi']==before and item['after_pi']==before+33;before=item['after_pi']
    assert before==1592
    counts=[]
    for step in range(25):
        suffix='seed' if step==0 else f'step{step:02d}'
        historical=read(f'dyadic_rolling_P1600_col01_{suffix}_d127',retained=False)
        u=800+33*step
        assert historical['weighted_residual_lower_bound_pi']==u
        assert historical['active_moment_count']==max(33,P-u)
        counts.append(historical['active_moment_count'])
    return {'final_weighted_reference_scalar_checks':checks,
        'final_scaled_residual_scalar_checks':174*33*8,'checkpoint_metadata_checked':25,
        'recorded_correction_gains_checked':24,'active_moment_counts':counts,
        'retired_intermediate_payloads_rechecked':False,
        'final_fixed_mass_original_residual_is_iteration_independent':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',required=True,choices=['states','seed','coarse','weighted']);args=parser.parse_args()
    out=DATA/f'dyadic_rolling_audit_{args.phase}_d127.json';assert not out.exists();start=time.monotonic()
    cert={'states':states,'seed':seed_tail,'coarse':coarse,'weighted':weighted_review}[args.phase]()
    result={'status':'pass','milestone':'D127','phase':args.phase,'working_precision_pi':P,'harmonic_basis_column':1,
        'full_sixteen_column_bank_precision_pi':800,'production_arithmetic_not_imported':True,'certificates':cert,
        'positive_exact_quadric_vanishing_proved':False,'candidate_identification_proved':False,
        'target_field_polynomial_constructed':False,'wall_seconds':time.monotonic()-start,
        'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
        'sources':[r.source(path) for path in sorted(PATHS)]}
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='sources'}),flush=True)
    print('PASS|522_DYADIC_ROLLING_INDEPENDENT',flush=True)

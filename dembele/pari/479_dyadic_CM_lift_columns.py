"""D122 CM charts and four coarse coefficients for a verified P=400 column."""
import argparse
import importlib.util
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
def module(name,file):
    s=importlib.util.spec_from_file_location(name,ROOT/'dembele/pari'/file)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
f=module('fast','477_dyadic_polynomial_kernel_control.py')
cmodule=module('coarse','475_dyadic_actual_CM_column.py')
l,p,b=f.l,f.p,f.b


def build(column):
    assert 1<=column<16
    begin=time.monotonic();P=400;H=1198;C=799
    previous=f'dyadic_actual_P400_col{column:02d}_verified_d122'
    saved,state,_,statepath=l.checkpoint(previous)
    assert saved['actual_moment_precision_increased'] and saved['harmonic_basis_column']==column
    assert saved['certificate']['full_residual_uses_different_polynomial_backend_from_lift']
    packet=json.loads((DATA/'dyadic_target_transports_d121.json').read_text())
    charts=[row for row in packet['CM_charts'] if row['chart']=='A'];assert len(charts)==17
    targets,params,transportpath=b.parameters(P);ring=f.Ring(50)
    required=sorted({row['target_edge'] for row in charts});extended={};plans={}
    bankpath=DATA/'dyadic_precision200_d115.json';old=json.loads(bankpath.read_text());mask=(1<<25)-1
    for e in required:
        total=[b.ZERO]*(H+1)
        for branch,j in enumerate(targets[e]):
            pars=params[e][branch]
            if pars not in plans:plans[pars]=l.Plan(ring,*pars,P,H+1)
            total=ring.padd(total,plans[pars].apply(state[j]))
        assert total[:P]==state[e]
        assert [tuple(c&mask for c in row) for row in total[:599]]==[
            tuple(m[column]) for m in old['state_moments_power_basis'][e]]
        extended[e]=total
    values=[]
    for ci,row in enumerate(charts):
        assert row['CM_index']==ci and row['normalized_error_pi']>=P
        pars=[tuple(int(c)&ring.mask for c in a) for a in row['normalized_center'][:3]]
        got=l.Plan(ring,*pars,H+1,C+1).apply(extended[row['target_edge']])
        assert got[0]==(row['zeroth_moments'][column]&ring.mask,)+(0,)*7
        assert [tuple(c&mask for c in a) for a in got[:400]]==[
            tuple(m[column]) for m in old['CM_A_chart_moments'][ci]['moments_power_basis']]
        values.append(got)
    cm=cmodule.Ring();ZERO,ONE,BETA=cmodule.ZERO,cmodule.ONE,cmodule.BETA
    pi=cm.add(cm.scale(cm.mul(BETA,BETA),-1),cm.scale(ONE,-2));powers=cm.powers(pi,7)
    q=cm.add(tuple(cmodule.MP[1:]),cm.scale(BETA,-1));assert cm.mul(BETA,q)==pi
    qp=cm.powers(q,C)
    kernels=[[cm.scale(qp[r],cmodule.coefficient(2*order+2,r)) for r in range(C+1)] for order in range(4)]
    errors=[832,848,832,864]
    jetpath=DATA/'dyadic_third_coarse_jet_d116.json';oldjets=json.loads(jetpath.read_text());results=[]
    for ci,moments in enumerate(values):
        embedded=[]
        for m in moments:
            x=ZERO
            for c,a in zip(m,powers):x=cm.add(x,cm.scale(a,c))
            embedded.append(x)
        jets=[];valuations=[]
        for order,kernel in enumerate(kernels):
            value=ZERO
            for a,m in zip(kernel,embedded):value=cm.add(value,cm.mul(a,m))
            prior=tuple(oldjets['CM_values'][ci]['coarse_coefficients_beta'][order][column])
            assert cm.value(cm.add(value,cm.scale(prior,-1)))>=oldjets['coarse_error_beta'][order]
            jets.append(list(value));v=cm.value(value);valuations.append(v if v<errors[order] else None)
        results.append({'CM_index':ci,'coarse_coefficients_beta':jets,'certified_valuations_beta':valuations})
    chartfile=DATA/f'dyadic_actual_CM_P400_col{column:02d}_d122_moments.bin';assert not chartfile.exists()
    chartfile.write_bytes(b.pack(values,50))
    paths=[Path(__file__),Path(f.__file__),Path(l.__file__),Path(cmodule.__file__),f.LIBRARY,
        statepath,transportpath,bankpath,jetpath,chartfile]
    paths += [Path(x['path']) for x in saved['checkpoint_files']]
    result={'status':'pass','milestone':'D122','harmonic_basis_column':column,'working_precision_pi':P,
        'state_cutoff':H,'CM_cutoff':C,'extended_target_states':required,'CM_charts_checked':17,
        'CM_moment_scalar_coefficients':17*800*8,'coarse_orders':[0,1,2,3],
        'arithmetic_precision_beta':864,'kernel_gains_beta':[32,48,32,64],'coarse_error_beta':errors,
        'CM_values':results,'old_coarse_values_checked':68,'old_CM_moment_scalar_coefficients_checked':17*400*8,
        'actual_moment_precision_increased':True,'actual_harmonic_columns_refined':1,
        'candidate_identification_proved':False,'wall_seconds':time.monotonic()-begin,
        'sources':[p.f.source(x) for x in paths]}
    print('CM_COLUMN_COMPLETE|'+json.dumps({'column':column,'errors_beta':errors,'seconds':result['wall_seconds']}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--column',type=int,required=True);args=parser.parse_args()
    out=DATA/f'dyadic_actual_CM_P400_col{args.column:02d}_d122.json';assert not out.exists()
    out.write_text(json.dumps(build(args.column),indent=2)+'\n');print('PASS|479_DYADIC_CM_LIFT_COLUMNS',flush=True)

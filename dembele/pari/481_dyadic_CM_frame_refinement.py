"""D122 refine the certified CM roots and algebraic residue frame.

No harmonic moments or geometric labels are inferred here. Hensel balls
overlap their original certified branches beyond all root separations.
"""
import argparse
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('balls',ROOT/'dembele/pari/480_dyadic_multiprecision_balls.py')
f=importlib.util.module_from_spec(s);s.loader.exec_module(f)


def source(path):
    import hashlib
    path=Path(path).resolve();return {'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def build(precision):
    assert precision>=1024 and precision%16==0
    begin=time.monotonic()
    priorpath=DATA/'dyadic_cm_matching_review_d112.json';prior=json.loads(priorpath.read_text())['certificates']['roots_and_frame']
    proposalpath=DATA/'dyadic_cm_root_proposals_d112.json';proposal=json.loads(proposalpath.read_text())
    basispath=DATA/'cm_field_recognition.json';basis=json.loads(basispath.read_text())['field_basis']['trace_centered_basis_power_coordinates'][1:]
    assert len(basis)==16
    shifts=[max((Q(c).denominator&-Q(c).denominator).bit_length()-1 for c in row) for row in basis]
    work=16*((precision+32*max(shifts)+1024+15)//16);ring=f.Ring(work);out=f.Ring(precision)
    poly=proposal['root_polynomial'];assert len(poly)==18
    derivative=[i*poly[i] for i in range(1,len(poly))]
    def evaluate(cs,x):
        value=f.ZERO
        for c in reversed(cs):value=ring.add(ring.mul(value,x),ring.scale(f.ONE,c))
        return value
    roots=[];certificates=[]
    for index,oldrow in enumerate(proposal['root_centers']):
        old=ring.rational_integral(oldrow);x=old
        d=ring.value(evaluate(derivative,x));error=ring.value(evaluate(poly,x))-d
        original=prior['root_certificates'][index]
        assert d==original['derivative_valuation_beta']
        assert error>=original['root_error_valuation_beta']
        history=[error]
        while error<work-d:
            residual=evaluate(poly,x);der=evaluate(derivative,x)
            assert ring.value(der)==d and ring.value(residual)>2*d
            correction=ring.mul(ring.divide_beta(residual,d),ring.unit_inverse(ring.divide_beta(der,d)))
            x=ring.add(x,ring.scale(correction,-1))
            new=ring.value(evaluate(poly,x))-d
            assert new>error and new>=min(work-d,2*error-d)
            error=new;history.append(error)
        overlap=ring.value(ring.add(x,ring.scale(old,-1)))
        assert overlap>=original['root_error_valuation_beta']>prior['maximum_root_separation_valuation_beta']
        roots.append(x);certificates.append({'root_index':index,'derivative_valuation_beta':d,
            'successive_root_errors_beta':history,'new_error_beta':error,'old_center_overlap_beta':overlap,
            'new_residual_lower_beta':ring.value(evaluate(poly,x))})
    values=[];bounds=[]
    for item in prior['CM_point_root_matching']:
        index=item['dyadic_root_index'];x=roots[index];row=[]
        for polynomial,shift in zip(basis,shifts):
            cs=[]
            for c in polynomial:
                q=Q(c)*(1<<shift);assert q.denominator&1
                cs.append(q.numerator*pow(q.denominator,-1,ring.mod)%ring.mod)
            scaled=evaluate(cs,x)
            assert all(c%(1<<shift)==0 for c in scaled)
            bound=min(work,certificates[index]['new_error_beta'])-16*shift
            assert bound>=precision
            row.append([str((c>>shift)&out.mask) for c in scaled]);bounds.append(bound)
        values.append(row)
    assert len(values)==17
    overlap=[]
    for current,old in zip(values,prior['rational_residue_frame_values']):
        for x,y in zip(current,old):
            difference=out.add(tuple(map(int,x)),out.scale(out.rational_integral(y),-1))
            overlap.append(out.value(difference));assert overlap[-1]>=prior['rational_residue_frame_error_beta']
    assert all(sum(int(values[i][j][k]) for i in range(17))%out.mod==0 for j in range(16) for k in range(16))
    assert out.value(tuple(map(int,values[0][0])))==prior['anchor_eta1_valuation_beta']==112
    assert all(out.value(tuple(map(int,row[0])))==1 for row in values[1:])
    result={'status':'pass','milestone':'D122','root_polynomial':poly,'CM_polynomial':list(f.MP),
        'work_precision_beta':work,'root_centers':[[str(c) for c in x] for x in roots],
        'root_certificates':certificates,'all_original_Hensel_branches_preserved':True,
        'CM_point_root_matching':prior['CM_point_root_matching'],
        'rational_residue_frame_values':values,'rational_residue_frame_error_beta':precision,
        'minimum_frame_error_before_export_beta':min(bounds),'minimum_old_frame_overlap_beta':min(overlap),
        'basis_dyadic_denominator_exponents':shifts,'trace_centered_sums_checked':16,
        'actual_harmonic_moments_changed':False,'candidate_identification_proved':False,
        'wall_seconds':time.monotonic()-begin,
        'sources':[source(x) for x in [Path(__file__),Path(f.__file__),priorpath,proposalpath,basispath]]}
    print('CM_FRAME_REFINED|'+json.dumps({k:result[k] for k in ['work_precision_beta',
        'rational_residue_frame_error_beta','minimum_frame_error_before_export_beta','minimum_old_frame_overlap_beta','wall_seconds']}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--precision',type=int,default=21168);args=parser.parse_args()
    out=DATA/f'dyadic_CM_frame_beta{args.precision}_d122.json';assert not out.exists()
    out.write_text(json.dumps(build(args.precision),indent=2)+'\n');print('PASS|481_DYADIC_CM_FRAME_REFINEMENT',flush=True)

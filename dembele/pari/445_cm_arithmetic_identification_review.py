"""D116 final audit: integral lattices, direct quadric jets, bounds and provenance."""
import argparse
from fractions import Fraction as Q
import importlib.util
import json
from math import comb
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'cm_arithmetic_identification_review_d116.json'

def module(name,filename):
    s=importlib.util.spec_from_file_location(name,ROOT/'dembele/pari'/filename)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

review=module('review','440_cm_exactness_review.py');f=review.f;r=review.r

def third_coarse_review():
    old=module('old_coarse','416_dyadic_coarse_review.py')
    packet=json.loads((DATA/'dyadic_third_coarse_jet_d116.json').read_text())
    bank=json.loads((DATA/'dyadic_precision200_d115.json').read_text())
    M=old.FieldQuotient(448);beta=old.BETA
    pi=M.add(M.scale(M.mul(beta,beta),-1),M.scale(old.MO,-2))
    q=M.add(M.norm(old.MP[1:]),M.scale(beta,-1));assert M.mul(beta,q)==pi
    qp=M.powers(q,399);embed=np.array(M.powers(pi,7),dtype=np.int64)
    kernels=[old.MZ]
    # Multiply (1+X)^8 and the binomial expansion of (1-X)^(-8).
    for degree in range(1,400):
        scalar=-sum(comb(8,i)*comb(8+degree-i-1,degree-i) for i in range(min(8,degree)+1))
        assert scalar%16==0
        kernels.append(M.scale(qp[degree],scalar))
    assert packet['coarse_error_beta']==[432,448,432,448]
    assert 16*max(M.mods)**2+max(M.mods)<2**63
    checked=0
    for ci,chart in enumerate(bank['CM_A_chart_moments']):
        moments=(np.array(chart['moments_power_basis'],dtype=np.int64)@embed)%M.mods
        answer=np.zeros((16,16),dtype=np.int64)
        for degree,c in enumerate(kernels):
            answer=(answer+M.matrix(c)@moments[degree].T)%np.array(M.mods)[:,None]
        assert answer.T.tolist()==packet['CM_values'][ci]['coarse_coefficients_beta'][3]
        for n in range(3):
            for x,y in zip(packet['CM_values'][ci]['coarse_coefficients_beta'][n],bank['CM_values'][ci]['coarse_coefficients_beta'][n]):
                assert M.val(M.add(x,M.scale(y,-1)))>=bank['coarse_error_beta'][n]
        checked+=16
    return {'third_coarse_entries_checked':checked,'independent_integer_quotient_and_kernel_expansion':True,
            'coarse_error_beta':[432,448,432,448],'moment_precision_increased':False}

def scale(x,c):
    if not c:return f.Ball()
    extra=16*((abs(c)&-abs(c)).bit_length()-1)
    return f.Ball(f.R.scale(x.u,c),x.v if x.u!=f.Z else 0,x.error+extra)

def quadric_jet_review():
    coarse=json.loads((DATA/'dyadic_third_coarse_jet_d116.json').read_text())
    computed=json.loads((DATA/'dyadic_integral_quadric_jets_d116.json').read_text())
    comparison=json.loads((DATA/'dyadic_comparison200_d115.json').read_text())
    candidate=json.loads((DATA/'cm_frame_curve_candidate.json').read_text())
    matrix=[[r.series.restore(x) for x in row] for row in comparison['change_of_basis']]
    pairs=candidate['monomial_pairs'];checked=0;minimums=[]
    for ci,row in enumerate(coarse['CM_values']):
        x,v,w,t=f.multiply([[f.center(cs,coarse['coarse_error_beta'][n]) for cs in row['coarse_coefficients_beta'][n]] for n in range(4)],matrix)
        second_squares=[v[i]*v[j] for i,j in pairs]
        point_min=[10**9]*3
        for quadric,saved in zip(candidate['quadrics'],computed['CM_values'][ci]['all_91_quadric_coefficients']):
            gx=[f.Ball() for _ in range(16)];gv=[f.Ball() for _ in range(16)];Qv=f.Ball()
            for c,(i,j),square in zip(quadric,pairs,second_squares):
                if not c:continue
                gx[i]=gx[i]+scale(x[j],c);gx[j]=gx[j]+scale(x[i],c)
                gv[i]=gv[i]+scale(v[j],c);gv[j]=gv[j]+scale(v[i],c)
                Qv=Qv+scale(square,c)
            values=[f.dot(gx,v),f.dot(gx,w)+Qv,f.dot(gx,t)+f.dot(gv,w)]
            for n,value in enumerate(values,1):
                expected=r.series.restore(saved[n]['coarse_coefficient'])
                assert not value.known_nonzero() and not (value-expected).known_nonzero()
                assert value.lower()>=expected.lower(),(ci,n,value.lower(),expected.lower())
                m=computed['CM_values'][ci]['fibre_generator_valuation_beta']
                shift=2*3920-4200-(n+2)*m
                assert saved[n]['conditional_intrinsic_jet_lower_beta']==expected.lower()+shift
                assert saved[n]['required_exact_vanishing_already_proved']==(n==1)
                point_min[n-1]=min(point_min[n-1],expected.lower()+shift);checked+=1
        minimums.append(point_min)
    assert minimums[0]==[3576,3248,2984]
    nonanchor=[min(row[n] for row in minimums[1:]) for n in range(3)]
    assert nonanchor==[3794,3745,3728]
    return {'independent_gradient_and_polar_form_coefficients_checked':checked,
       'degree16_lower_beta':nonanchor,'anchor_lower_beta':minimums[0],
       'higher_intrinsic_jets_require_previous_exact_zeros':True,'exact_vanishing_proved':False}

def direct_budget_review():
    pencil=module('pencil_controls','441_cm_integral_quadrics.py')
    compound=module('compound_controls','444_cm_quadric_compound_bound.py')
    old=json.loads((DATA/'cm_integral_quadrics_d116.json').read_text())
    packet=json.loads((DATA/'cm_quadric_compound_bound_d116.json').read_text())
    assert pencil.controls()==old['controls'] and compound.controls()==packet['polynomial_controls']
    g=16;L=max(sum(abs(x) for x in q) for q in json.loads((DATA/'cm_frame_curve_candidate.json').read_text())['quadrics'])
    bound=2*(g*g-g)*L*2**(70+20*(g*g-g-2));b=packet['direct_quadric_budgets']
    assert bound==int(b['tensor_norm_bound_integer']) and 2**4854<=bound<2**4855
    x=Q(1,3);lo=2*sum(x**(2*k+1)/Q(2*k+1) for k in range(64))
    hi=lo+2*x**129/(129*(1-x*x))
    thresholds=[]
    for n,row in enumerate(b['thresholds'],1):
        assert row['requires_previous_jets_exactly_zero']==list(range(n))
        alpha=Q((240+n)*41,10);beta=4855+row['jet_functional_binary_exponent']+720
        assert Q(row['height_bound_alpha'])==alpha and row['height_bound_beta_log2']==beta
        for key,correction in [('degree16_sufficient_lower_beta_without_anchor',Q(0)),
           ('degree16_sufficient_lower_beta_with_anchor',Q(row['certified_anchor_lower_beta'],272))]:
            N=row[key];B=beta-correction
            assert (N-17*B)*lo>17*alpha and (N-1-17*B)*hi<17*alpha
        thresholds.append(row['degree16_sufficient_lower_beta_with_anchor'])
    assert thresholds==[119806,120284,120758]
    # Strict derivative-functional constants, using pi>3 and rational radical bounds.
    assert 8<9 and 2*Q(7,4)+2<6 and 4+2*Q(5,2)<12
    return {'integral_polynomial_controls_replayed':True,'tensor_norm_binary_exponent':4855,
       'independent_atanh_log_series_terms':64,'degree16_sufficient_integral_jet_lower_beta':thresholds,
       'bounds_are_sufficient_not_necessary':True,'third_jet_requires_first_two_exactly_zero':True}

def calculations():
    result={'lattices_ranks_and_ratio_bounds':review.calculations(),
            'third_coarse_jet':third_coarse_review(),'integral_quadric_jets':quadric_jet_review(),
            'direct_vanishing_bounds':direct_budget_review()}
    print('ARITHMETIC_IDENTIFICATION_REVIEW|integral lattices, actual rank 33, all third coarse jets and 4641 direct coefficients pass',flush=True)
    return result

def build(certificates):
    prior_path=DATA/'dyadic_strategy_review_d115.json';prior=json.loads(prior_path.read_text())
    assert prior['status']=='pass' and len(prior['sources'])==814
    paths=f.coarse.checked(prior['sources'])+[prior_path,Path(__file__),
          ROOT/'dembele/certificates/cm-compound-height-d116.md',DATA/'cm_compound_sources_d116.json']
    for number in range(432,445):
        matches=list((ROOT/'dembele/pari').glob(f'{number}_*.py'));assert len(matches)==1;paths+=matches
    jobs=[]
    for path in sorted(DATA.glob('*d116*')):
        if path.name.startswith('cm_arithmetic_identification_review_d116'):continue
        paths.append(path)
        if path.suffix=='.json':
            packet=json.loads(path.read_text())
            hashes=[x for x in packet.get('sources',[]) if isinstance(x,dict) and 'sha256' in x]
            paths+=f.coarse.checked(hashes)
            if path.name.endswith('.job.json'):
                assert packet['status']=='pass' and packet['timeout_seconds']==180 and packet['timeout_terminates_process_group']
                paths+=f.coarse.checked([packet['driver'],packet['log']])
                jobs.append({'receipt':path.name,'status':packet['status'],'wall_seconds':packet['wall_seconds']})
    assert len(jobs)==13
    return {'status':'pass','milestone':'D116','D115_source_hashes_checked_unchanged':814,
       'certificates':certificates,'bounded_jobs':jobs,'actual_J3_rank_lower_bound':33,
       'stable_integral_harmonic_basis_via_companion_proof':True,'third_actual_coarse_jet_computed':True,
       'sufficient_degree16_beta_errors_ratio_orders_1_2':[132444,524481],
       'sufficient_degree16_integral_quadric_jet_valuations_beta':[119806,120284,120758],
       'actual_integral_quadric_jet_lower_beta':[3794,3745,3728],
       'actual_J3_rank_45_certified':False,'positive_quadric_jet_exact_vanishing_proved':False,
       'candidate_identification_proved':False,'CM_horizontal_residue_map_index_computed':False,
       'target_field_polynomial_constructed':False,
       'sources':[f.coarse.source(x) for x in sorted(set(p.resolve() for p in paths))]}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--probe',action='store_true');parser.add_argument('--check',action='store_true');a=parser.parse_args()
    result=calculations()
    if not a.probe:
        result=build(result)
        if a.check:
            previous=json.loads(OUT.read_text());f.coarse.checked(previous['sources']);assert result==previous
        else:assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'status':'pass','sources':len(result['sources']),'D115_preserved':814}),flush=True)
    print('PASS|445_CM_ARITHMETIC_IDENTIFICATION_REVIEW',flush=True)

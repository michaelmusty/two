"""D118: independent finite-fibre, tropical-moment and height-budget audit."""
import argparse
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'cm_finite_height_review_d118.json'
s=importlib.util.spec_from_file_location('independent_logs',ROOT/'dembele/pari/450_cm_disk_exactness_review.py')
r=importlib.util.module_from_spec(s);s.loader.exec_module(r)

def read(name):return json.loads((DATA/(name+'.json')).read_text())
def v2(n):
    n=abs(int(n));assert n;return (n&-n).bit_length()-1

def fibre_review():
    raw=read('dyadic_precision200_d115');packet=read('cm_composite_differential_d118')
    contents=[];entries=0
    for i,(saved,row) in enumerate(zip(packet['CM_fibres'],raw['CM_values'])):
        values=[]
        for coordinates in row['coarse_coefficients_beta'][0]:
            valuation=min(16*v2(c)+j for j,c in enumerate(coordinates) if c)
            assert valuation<raw['coarse_error_beta'][0];values.append(valuation);entries+=1
        m=min(values);assert m==saved['coarse_fibre_exponent_beta']
        # D_lambda=z*d/dz=(1-w^2)/2*d/dw. Thus D_lambda^2(w^2)|0=1/2.
        coefficient=Q(1,2);assert v2(coefficient.denominator)==16//16
        assert saved['composite_ramification_derivative_valuation_beta']==m-16
        contents.append(m-16)
    assert contents==[280]+[17]*16 and entries==272
    total=sum(contents);assert total==packet['sum_composite_valuations_beta']==552
    assert Q(total,272)==Q(packet['normalized_dyadic_finite_zero_degree_coefficient_log2'])==Q(69,34)
    # Direct coordinate differentiation, independent of 451's polynomial control.
    # z=beta is a root of (z-beta), and differentiating
    # z*du/dz=4*beta*z*(z-beta)/(z+beta)^3 there gives 1/(2*beta).
    for beta in (Q(-7),Q(2,3),Q(5)):
        D2u=beta*(4*beta*beta)/(2*beta)**3
        assert D2u==Q(1,2)
    return {'leading_coefficients_revalued':entries,'fibre_exponents':[296]+[33]*16,
            'combined_dyadic_contents_beta':contents,'normalized_content_coefficient_log2':'69/34',
            'Hodge_lattice_identification_requires_companion_proof':True,
            'individual_Hodge_and_ramification_parts_computed':False}

def tropical_review():
    packet=read('cm_tropical_faltings_d118');p=packet['graph'];old=read('hyperellipticity_graph_review_d99')
    assert p['vertices']==old['stable_vertices']
    edges=[(u,v,Q(w)) for u,v,w in p['edges']]
    assert edges==[(u,v,Q(w)) for u,v,w in old['stable_edges']]
    vertices=p['vertices'];idx={v:i for i,v in enumerate(vertices)};n=len(vertices)
    L=[[Q(0)]*(n-1) for _ in range(n-1)]
    for u,v,ell in edges:
        incidence=[int(a==u)-int(a==v) for a in vertices[:-1]]
        for i in range(n-1):
            for j in range(n-1):L[i][j]+=Q(incidence[i]*incidence[j],ell)
    inv=[list(map(Q,row)) for row in p['grounded_laplacian_inverse']]
    assert all(sum(L[i][k]*inv[k][j] for k in range(n-1))==int(i==j) for i in range(n-1) for j in range(n-1))
    G=[row+[Q(0)] for row in inv]+[[Q(0)]*n]
    R=[[G[i][i]+G[j][j]-G[i][j]-G[j][i] for j in range(n)] for i in range(n)]
    assert R==[list(map(Q,row)) for row in p['effective_resistances']]
    taus=[]
    for q in range(n):
        tau=Q(0)
        for u,v,ell in edges:
            i,j=idx[u],idx[v];difference=R[j][q]-R[i][q];amplitude=ell-R[i][j]
            at0=(difference+amplitude)/(2*ell)
            atmid=difference/(2*ell);at1=(difference-amplitude)/(2*ell)
            # Exact Simpson integration of the quadratic square of the
            # linear derivative of r(x,q)/2 on this edge.
            tau+=ell*(at0*at0+4*atmid*atmid+at1*at1)/6
        taus.append(tau)
    assert taus==list(map(Q,p['all_vertex_tau_values'])) and len(set(taus))==1
    ell=sum(e[2] for e in edges);moment=ell/8-taus[0]/2
    assert ell==76 and taus[0]==Q(67889,27075) and moment==Q(223268,27075)
    theta=moment/8;assert theta==Q(55817,54150)
    assert theta==Q(packet['dyadic_tropical_Faltings_contribution_coefficient_log2'])
    return {'inverse_checked_by_matrix_identity':True,'resistance_derivatives_integrated_by_exact_Simpson_rule':True,
            'basepoints_checked':n,'length':'76','tau':str(taus[0]),'tropical_moment':str(moment),
            'normalized_Faltings_contribution_coefficient_log2':str(theta)}

def budget_review():
    hodge=Q(read('cm_intrinsic_height_review_d104')['independent_analytic']['Hodge_height_interval'][1])
    H=r.plus((2*hodge,)*2,r.scale(r.L2,-Q(35,34)));assert H[1]<Q(8,3)
    pi=r.rounded(r.plus(r.scale(r.atan(Q(1,5)),16),r.scale(r.atan(Q(1,239)),-4)))
    lp=(r.log(pi[0])[0],r.log(pi[1])[1]);C=[r.scale(r.sqrt(2),2),r.plus(r.scale(r.sqrt(3),2),(Q(2),)*2),r.plus(r.scale(r.sqrt(6),2),(Q(4),)*2)]
    theta=Q(55817,54150);newFal=r.plus(r.scale(lp,-16),r.scale(r.L2,theta-8))
    candidate=read('cm_frame_curve_candidate');L=max(sum(abs(c) for c in q) for q in candidate['quadrics']);assert L==42550
    result=[]
    for name,coefficient,expected in [
        ('cm_corrected_height_budget_d118',Q(310),[27633,27747,27854]),
        ('cm_arithmetic_height_budget_d118',190-15*theta,[25330,25444,25551])]:
        p=read(name)['budgets'];thresholds=[];limits=[]
        h_saved=tuple(map(Q,p['coarse_CM_fibre_height_upper_interval']))
        assert max(H[0],h_saved[0])<=min(H[1],h_saved[1])
        for n,row in enumerate(p['thresholds'],1):
            logC=(r.log(C[n-1][0])[0],r.log(C[n-1][1])[1])
            pieces={'CM_fibre_degree':r.scale(H,240+n),
                    'frame_vector_and_Faltings_log2':r.scale(r.L2,coefficient),
                    'net_pi_factor':r.scale(lp,120),'quadric_and_path_constant':r.log(480*L),
                    'jet_constant':logC,'disk_radius':r.scale(r.log(Q(5,3)),240+n)}
            for key,iv in pieces.items():
                saved=tuple(map(Q,row['upper_bound_pieces'][key]))
                assert max(iv[0],saved[0])<=min(iv[1],saved[1])
            total=r.plus(*pieces.values());ideal=r.plus(*(v for k,v in pieces.items() if k!='disk_radius'))
            A=[3576,3248,2984][n-1];Nactual=[3794,3745,3728][n-1]
            assert row['certified_anchor_lower_beta']==A and row['achieved_degree16_lower_beta']==Nactual
            for iv,key in [(total,'degree16_sufficient_integral_jet_lower_beta'),(ideal,'optimistic_radius_one_same_bound_threshold_beta')]:
                lo=17*iv[0]/r.L2[1]-Q(A,16);hi=17*iv[1]/r.L2[0]-Q(A,16);N=row[key]
                assert N-1<lo<hi<N
            assert row['previous_exact_zero_orders_required']==list(range(n))
            assert row['valuation_gap']==row['degree16_sufficient_integral_jet_lower_beta']-Nactual
            thresholds.append(row['degree16_sufficient_integral_jet_lower_beta']);limits.append(row['optimistic_radius_one_same_bound_threshold_beta'])
            if name=='cm_arithmetic_height_budget_d118':
                # Recheck the saved absolute sensitivity threshold using
                # the new formula and its newly proved Faltings lower bound.
                needed=r.plus(newFal,r.scale(r.plus(total,r.scale(r.L2,-Q(16*Nactual+A,272))),Q(1,15)))
                saved=tuple(map(Q,row['h_Fal_lower_bound_needed_if_only_that_input_changes_interval']))
                assert max(needed[0],saved[0])<=min(needed[1],saved[1])
                sufficient=row['h_Fal_lower_bound_needed_sufficient_integer']
                assert sufficient-1<needed[0]<needed[1]<sufficient
        assert thresholds==expected
        result.append({'packet':name,'sufficient_beta_valuations':thresholds,'radius_one_fixed_input_limits':limits})
    assert result[-1]['radius_one_fixed_input_limits']==[22310,22412,22506]
    return {'independent_log_series':'256-term -log(1-t) with rational remainders',
            'coarse_CM_height_upper_below':'8/3','budgets':result,
            'h_Fal_only_sensitivity_sufficient_integers':[36,36,37],
            'sensitivity_is_not_a_proved_bound':True,'exact_vanishing_proved':False}

def calculations():
    result={'composite_fibre':fibre_review(),'tropical_graph':tropical_review(),'height_budgets':budget_review()}
    print('FINITE_HEIGHT_REVIEW|272 leading coefficients, differential contents, graph inverse, tau integrals and budgets pass',flush=True)
    return result

def build(certificates):
    prior_path=DATA/'cm_disk_exactness_review_d117.json';prior=json.loads(prior_path.read_text())
    assert prior['status']=='pass' and len(prior['sources'])==891
    paths=r.checked(prior['sources'])+[prior_path,Path(__file__),
        ROOT/'dembele/certificates/cm-finite-height-d118.md',DATA/'cm_finite_height_sources_d118.json']
    for number in range(451,455):
        matches=list((ROOT/'dembele/pari').glob(f'{number}_*.py'));assert len(matches)==1;paths+=matches
    jobs=[]
    for path in sorted(DATA.glob('*d118*')):
        if path.name.startswith('cm_finite_height_review_d118'):continue
        paths.append(path)
        if path.suffix!='.json':continue
        p=json.loads(path.read_text());paths+=r.checked([x for x in p.get('sources',[]) if isinstance(x,dict) and 'sha256' in x])
        if path.name.endswith('.job.json'):
            assert p['status']=='pass' and p['timeout_seconds']==180 and p['timeout_terminates_process_group']
            paths+=r.checked([p['driver'],p['log']])
            jobs.append({'receipt':path.name,'status':p['status'],'wall_seconds':p['wall_seconds']})
    assert len(jobs)==4
    return {'status':'pass','milestone':'D118','D117_source_hashes_checked_unchanged':891,
            'certificates':certificates,'bounded_jobs':jobs,
            'combined_dyadic_CM_height_correction_coefficient_log2':'69/34',
            'tropical_Faltings_contribution_coefficient_log2':'55817/54150',
            'sufficient_degree16_integral_quadric_jet_valuations_beta':[25330,25444,25551],
            'actual_integral_quadric_jet_lower_beta':[3794,3745,3728],
            'actual_moment_precision_increased':False,'positive_quadric_jet_exact_vanishing_proved':False,
            'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
            'sources':[r.source(p) for p in sorted(set(p.resolve() for p in paths))]}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--probe',action='store_true');parser.add_argument('--check',action='store_true');a=parser.parse_args()
    result=calculations()
    if not a.probe:
        result=build(result)
        if a.check:
            previous=json.loads(OUT.read_text());r.checked(previous['sources']);assert result==previous
        else:
            assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'status':'pass','sources':len(result['sources']),'D117_preserved':891}),flush=True)
    print('PASS|455_CM_FINITE_HEIGHT_REVIEW',flush=True)

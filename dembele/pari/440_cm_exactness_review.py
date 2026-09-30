"""D116 final review: exact lattice witnesses, finite contents, budgets and provenance."""
import argparse
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('prior_review',ROOT/'dembele/pari/435_cm_compound_review.py')
p=importlib.util.module_from_spec(s);s.loader.exec_module(p);f=p.f;r=p.r
OUT=DATA/'cm_exactness_review_d116.json'

def lattice_review():
    harmonic=json.loads((DATA/'dyadic_harmonic_certificate_d111.json').read_text())
    saturation=json.loads((DATA/'dyadic_harmonic_saturation_d116.json').read_text())
    B=harmonic['harmonic_basis'];a=[row[:] for row in B];U=[[int(i==j) for j in range(16)] for i in range(16)]
    for op in saturation['Smith_unimodular_operations']:
        kind,*args=op
        if kind=='rs':
            i,j=args;a[i],a[j]=a[j],a[i];U[i],U[j]=U[j],U[i]
        elif kind=='cs':
            i,j=args
            for row in a:row[i],row[j]=row[j],row[i]
        elif kind=='ra':
            i,j,q=args;assert i!=j
            for matrix in [a,U]:matrix[i]=[x+q*y for x,y in zip(matrix[i],matrix[j])]
        elif kind=='ca':
            i,j,q=args;assert i!=j
            for row in a:row[i]+=q*row[j]
        else:
            assert kind=='rn';i,=args
            for matrix in [a,U]:matrix[i]=[-x for x in matrix[i]]
    assert a==[[int(i==j) for j in range(174)] for i in range(16)]
    assert U==saturation['row_unimodular_transform']
    assert all(sum(u*b for u,b in zip(row,column))==value
               for row,expected in zip(U,saturation['saturated_integer_harmonic_basis'])
               for column,value in zip(zip(*B),expected))
    assert all(sum(x*y for x,y in zip(relation,row))==0 for row in B for relation in harmonic['harmonic_relations'])
    graph=json.loads((DATA/'dyadic_graph_residues_d116.json').read_text())
    edges=graph['quotient_edges'];cycles=graph['fundamental_integer_cycles'];T=[[Q(x) for x in row] for row in graph['harmonic_to_cycle_coordinates']]
    Ti=p.exact_inverse(T);assert all(x.denominator==1 for row in Ti+T for x in row)
    assert all(cycle[e]==int(i==j) for i,cycle in enumerate(cycles) for j,e in enumerate(graph['chord_edges']))
    for edge in edges:
        slot=edge['representative_slot'];e=harmonic['edges'][slot]
        assert [edge['source'],edge['target']]==[e['source_class'],e['target_class']]
        perms=harmonic['ideal_checks'][e['source_class']]['stabilizer_permutations']
        assert edge['edge_stabilizer_order']==sum(perm[e['line']]==e['line'] for perm in perms)
    for i,cycle in enumerate(cycles):
        assert all(sum(x*(int(e['source']==v)-int(e['target']==v)) for x,e in zip(cycle,edges))==0 for v in range(58))
        for j,edge in enumerate(edges):
            assert sum(T[i][k]*cycles[k][j] for k in range(16))==Q(B[i][edge['representative_slot']],edge['edge_stabilizer_order'])
    return {'Smith_operations_replayed':len(saturation['Smith_unimodular_operations']),
        'all_16_Smith_factors_one':True,'weighted_cycle_change_and_inverse_integral':True,
        'graph_cycle_rank':16,'stable_model_interpretation_is_companion_mathematical_proof':True}

def content_review():
    integral=json.loads((DATA/'dyadic_integral_frame_d116.json').read_text())
    content=json.loads((DATA/'cm_finite_content_d116.json').read_text())
    comparison=json.loads((DATA/'dyadic_comparison200_d115.json').read_text())
    coarse=json.loads((DATA/'dyadic_precision200_d115.json').read_text())
    change=[[r.series.restore(x) for x in row] for row in comparison['change_of_basis']]
    determinant=sum(x['valuation_beta'] for x in comparison['evaluation_pivots'])
    cofactors=[determinant]+[determinant+r.series.restore(x).v for x in comparison['frame_relation']]
    assert cofactors==integral['evaluation_cofactor_valuations_beta']==[280]+[245]*16
    delta=sum(cofactors);factor=delta-determinant
    assert [delta,factor,min(cofactors)]==[4200,3920,245]
    # beta is a global algebraic integer with norm 2; its unique dyadic prime is principal.
    assert f.coarse.MP[0]==2 and len(f.coarse.MP)==17
    first=[];second=[]
    for ci,row in enumerate(coarse['CM_values']):
        m=min(row['certified_valuations_beta'][0]);assert m==integral['canonical_fibre_coarse_generator_valuations_beta'][ci]
        jet=f.multiply([[f.center(cs,coarse['coarse_error_beta'][n]) for cs in row['coarse_coefficients_beta'][n]] for n in range(3)],change)
        a,a1,a2=[row[0] for row in jet]
        G=a*jet[1][1]-jet[0][1]*a1
        Gp=f.TWO*(a*jet[2][1]-jet[0][1]*a2)
        gaussians=[a*jet[1][j]-jet[0][j]*a1 for j in range(1,16)]
        first.append(2*factor-delta+min(x.lower() for x in gaussians)-3*m)
        den=16+delta+3*(2*factor-delta+G.lower()-3*m)
        saved=content['thresholds'][1]['common_content_beta_at_17_CM_points'][ci]
        assert den>=saved
        lows=[]
        for j,H in enumerate(gaussians,1):
            Hp=f.TWO*(a*jet[2][j]-jet[0][j]*a2)
            # Independent D106 Gaussian derivative expression, rather than a 3-by-3 determinant.
            numerator=a*a*(G*Hp-H*Gp)
            bound=6*factor-2*delta+numerator.lower()-9*m
            assert bound>=saved,(ci,j,bound,saved)
            lows.append(bound)
        second.append(saved)
    assert first==content['thresholds'][0]['common_content_beta_at_17_CM_points']==[3577]+[3694]*16
    assert second==[14881]+[15298]*16
    n=256;lo=sum(Q(1,k*2**k) for k in range(1,n+1));hi=lo+Q(1,(n+1)*2**n)
    budgets=[]
    for row,values in zip(content['thresholds'],[first,second]):
        assert Q(row['subtracted_coefficient_of_log2'])==Q(sum(values),272)
        A=Q(row['difference_height_bound_alpha']);B=Q(row['difference_height_bound_beta_log2']);N=row['degree16_sufficient_beta_error']
        assert (N-17*B)*lo>17*A and (N-1-17*B)*hi<17*A
        alpha=Q(row['actual_height_bound_alpha']);beta=Q(row['actual_height_bound_beta_log2']);bound=row['actual_height_strict_integer_upper']
        assert bound-1<alpha+beta*lo<alpha+beta*hi<bound
        budgets.append({'order':row['order'],'actual_height_strict_upper':bound,'degree16_beta_threshold':N})
    assert [x['degree16_beta_threshold'] for x in budgets]==[132444,524481]
    return {'first_common_content_beta':first,'second_common_content_beta':second,
            'independent_Gaussian_derivative_numerator_checks':255,'budgets':budgets,
            'CM_principal_dyadic_prime_and_Hilbert_class_field_splitting_via_report':True}

def calculations():
    result={'compound_and_rank':p.calculations(),'lattices':lattice_review(),'finite_content':content_review()}
    print('EXACTNESS_REVIEW|saturated harmonic and weighted-cycle lattices; stable fibre/cofactor contents; beta budgets 132444/524481',flush=True)
    return result

def build(certificates):
    prior_path=DATA/'dyadic_strategy_review_d115.json';prior=json.loads(prior_path.read_text())
    assert prior['status']=='pass' and len(prior['sources'])==814
    paths=f.coarse.checked(prior['sources'])+[prior_path,Path(__file__),
        ROOT/'dembele/certificates/cm-compound-height-d116.md',DATA/'cm_compound_sources_d116.json']
    for number in range(432,440):
        matches=list((ROOT/'dembele/pari').glob(f'{number}_*.py'));assert len(matches)==1;paths+=matches
    jobs=[]
    for path in sorted(DATA.glob('*d116*')):
        if path.name.startswith('cm_exactness_review_d116'):continue
        paths.append(path)
        if path.suffix=='.json':
            packet=json.loads(path.read_text())
            hashes=[x for x in packet.get('sources',[]) if isinstance(x,dict) and 'sha256' in x]
            paths+=f.coarse.checked(hashes)
            if path.name.endswith('.job.json'):
                assert packet['status']=='pass' and packet['timeout_seconds']==180 and packet['timeout_terminates_process_group']
                paths+=f.coarse.checked([packet['driver'],packet['log']])
                jobs.append({'receipt':path.name,'status':packet['status'],'wall_seconds':packet['wall_seconds']})
    assert len(jobs)==8
    return {'status':'pass','milestone':'D116','D115_source_hashes_checked_unchanged':814,
       'certificates':certificates,'bounded_jobs':jobs,'actual_J3_rank_lower_bound':33,
       'stable_integral_harmonic_basis_via_companion_proof':True,
       'sufficient_degree16_beta_errors_orders_1_2':[132444,524481],
       'actual_J3_rank_45_certified':False,'candidate_identification_proved':False,
       'CM_horizontal_residue_map_index_computed':False,'target_field_polynomial_constructed':False,
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
    print('PASS|440_CM_EXACTNESS_REVIEW',flush=True)

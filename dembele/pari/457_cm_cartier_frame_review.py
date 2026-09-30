"""D119: independent quotient-arithmetic audit of the actual Cartier residue frame."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'cm_cartier_frame_review_d119.json'
s=importlib.util.spec_from_file_location('quotient_review',ROOT/'dembele/pari/416_dyadic_coarse_review.py')
r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
Z=r.MZ;O=r.MO;B=r.BETA;P=64

def read(name):return json.loads((DATA/(name+'.json')).read_text())
def source(p):return {'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def checked(rows):
    paths=[]
    for row in rows:
        p=Path(row['path']);assert source(p)==row;paths.append(p)
    return paths

def divide_beta(x,n,precision):
    """Exact quotient of an integral center, reducing its precision each step."""
    work=r.FieldQuotient(precision);x=work.norm(x)
    for _ in range(n):
        assert x[0]%2==0
        c=x[0]//2
        precision-=1;work=r.FieldQuotient(precision)
        x=work.norm([(x[i+1] if i<15 else 0)-c*r.MP[i+1] for i in range(16)])
    return x

def divide_power_two(x,n,precision):
    work=r.FieldQuotient(precision);x=work.norm(x);d=1<<n
    assert all(c%d==0 for c in x)
    return r.FieldQuotient(precision-16*n).norm([c//d for c in x])

def inverse_unit(x,work):
    assert work.val(x)==0
    ans=O
    for _ in range((work.precision-1).bit_length()):
        ans=work.mul(ans,work.add(work.scale(O,2),work.scale(work.mul(x,ans),-1)))
    assert work.mul(x,ans)==O
    return ans

def smith(matrix,precision=P):
    """Successive common-factor extraction and unit-pivot Schur complements.

    Unlike 456's balls and valuation-bearing pivot divisions, every stage
    works in one integer quotient ring. No absent digit is used as a zero.
    """
    a=[row[:] for row in matrix];answer=[];cumulative=0
    while a and a[0]:
        work=r.FieldQuotient(precision)
        v,i,j=min((work.val(x),i,j) for i,row in enumerate(a) for j,x in enumerate(row))
        assert v<precision,('unresolved Smith stage',len(answer))
        if v:
            a=[[divide_beta(x,v,precision) for x in row] for row in a]
            precision-=v;cumulative+=v;work=r.FieldQuotient(precision)
        a[0],a[i]=a[i],a[0]
        for row in a:row[0],row[j]=row[j],row[0]
        unit=inverse_unit(a[0][0],work);answer.append(cumulative)
        coefficients=[work.mul(row[0],unit) for row in a[1:]]
        a=[[work.add(x,work.scale(work.mul(c,y),-1)) for x,y in zip(row[1:],a[0][1:])]
           for row,c in zip(a[1:],coefficients)]
    return answer

def restore(row,work):
    assert row['error_beta']>=work.precision
    e=row['beta_exponent'];assert e is not None and e>=0
    return work.mul(work.norm(row['unit_beta']),work.powers(B,e)[-1])

def model_review():
    d=read('dyadic_quotient_export_d111');g=read('hyperellipticity_graph_review_d99')
    # Independent use of D99's recorded stable paths: ordinary CM components
    # have two incident noninverted edges on a single stable edge.
    edges=g['quotient_edges'][:73];paths=g['stable_paths'];witnesses=[]
    for vertex in range(51,59):
        incident=[j for j,e in enumerate(edges) if vertex in e[:2]]
        assert len(incident)==2
        matches=[p for p in paths if set(incident)<=set(p['original_edge_ids'])]
        assert len(matches)==1 and matches[0]['weight']=='2'
        witnesses.append({'component':vertex,'stable_edge':matches[0]['edge'],
                          'incident_original_edges':incident,'stable_length_pi':2})
    # Anchor's tail joins component 6; that component lies inside the length-12
    # stable edge. The point of tail attachment is away from its two nodes.
    anchor_paths=[p for p in paths if p['weight']=='12'];assert len(anchor_paths)==1
    assert anchor_paths[0]['edge']==[9,10]
    packet=read('cm_cartier_principal_parts_d119')
    tail=packet['geometry']['tail_contractions']
    assert [v for v,_,_ in tail]==[1,5,4,2,3,35,36,37,38]
    location=5
    for v,w,_ in tail:
        if location==v:location=w
    assert location==6
    # Reversed ordinary edge has full setwise stabilizer C2, since its
    # endpoint stabilizer is trivial. Its quotient parameter is x-y.
    for index,vertex in zip(range(152,174,3),range(50,58)):
        row=d['edges'][index]
        assert row['source_class']==row['target_class']==vertex
        assert d['stabilizers'][vertex]==1
    return {'eight_distinct_ordinary_components_on_stable_chains':witnesses,
            'anchor_attaches_to_component':6,'anchor_stable_edge':[9,10],
            'intersection_length_each_ordinary_pair_beta':33,
            'all_other_pairwise_intersections_on_minimal_regular_model':0,
            'normalization_index_beta':264,'discriminant_beta':528,
            'geometric_application_requires_companion_proof':True}

def calculations():
    geometry=model_review();packet=read('cm_cartier_principal_parts_d119')
    raw=read('dyadic_precision200_d115');precision=raw['coarse_error_beta'][0]
    assert precision==432
    q=r.FieldQuotient(P);big=r.FieldQuotient(precision)
    values=[p['coarse_coefficients_beta'][0] for p in raw['CM_values']]
    matrix=[[q.norm(divide_beta(x,296,precision)) for x in values[0]]]
    for i in range(1,17,2):
        # (h_plus+h_minus)/(16 beta^2) and h_plus/(4 beta).
        combined=[big.add(x,y) for x,y in zip(values[i],values[i+1])]
        divided=[q.norm(divide_beta(divide_power_two(x,4,precision),2,precision-64)) for x in combined]
        plus=[q.norm(divide_beta(divide_power_two(x,2,precision),1,precision-32)) for x in values[i]]
        matrix.extend([divided,plus])
    assert matrix==[[restore(x,q) for x in row] for row in packet['restriction_matrix_N_dual']]
    factors=smith(matrix);assert factors==[0]*9+[2]*7
    assert factors==[x['valuation_beta'] for x in packet['restriction_Smith_pivots']]
    assert sum(factors)==packet['cohomology_torsion_length_beta']==14
    cofactors=[sum(smith(matrix[:i]+matrix[i+1:])) for i in range(17)]
    assert cofactors==packet['restriction_cofactor_valuations_beta']==[16]+[14]*16
    primitive=[restore(x,q) for x in packet['primitive_principal_part_coefficients']]
    assert min(q.val(x) for x in primitive)==0
    def total(xs):
        ans=Z
        for x in xs:ans=q.add(ans,x)
        return ans
    assert all(total([q.mul(primitive[i],matrix[i][j]) for i in range(17)])==Z for j in range(16))
    d=q.scale(B,4);a_values=[primitive[0]];residue=[[q.mul(primitive[0],x) for x in matrix[0]]]
    for i in range(1,17,2):
        a,b=primitive[i:i+2];ap=q.add(a,q.mul(d,b));a_values.extend([ap,a])
        # Multiplication by a+b*s in R[s]/(s^2-d*s), transposed on the dual.
        residue.append([q.add(q.mul(a,x),q.mul(b,y)) for x,y in zip(matrix[i],matrix[i+1])])
        residue.append([q.mul(ap,y) for y in matrix[i+1]])
    assert a_values==[restore(x,q) for x in packet['primitive_principal_part_values']]
    valuations=[q.val(x) for x in a_values];assert valuations==[2]+[0]*16
    # Evaluation on 1 in A is anchor plus the first coordinate in each pair.
    assert all(total([residue[i][j] for i in [0]+list(range(1,17,2))])==Z for j in range(16))
    residue_factors=smith(residue[1:]);assert residue_factors==[0]*8+[2]*8
    assert sum(residue_factors)==sum(factors)+sum(valuations)==packet['residue_map_index_beta']==16
    # Check the finite algebra trace/codifferent identity in its pair basis.
    # Trace Gram matrix of {1,s} is [[2,d],[d,d^2]], determinant d^2.
    discriminant=q.mul(d,d);assert q.val(d)==33
    # d^2 lies beyond this review's precision: use a separate 96-digit ring.
    q96=r.FieldQuotient(96);dd=q96.scale(B,4)
    assert q96.val(q96.mul(dd,dd))==66
    assert 8*66==packet['divisor_algebra_discriminant_beta']==528
    # Further separating each pair takes 33 smooth-point blowups at each
    # marked section. This changes the model-dependent terms, not the curve.
    k=[0]+[33]*16;K=sum(k);old=[280]+[245]*16
    split_cofactors=[v+K-t for v,t in zip(old,k)]
    split_T=min(split_cofactors);split_principal=[v-split_T for v in split_cofactors]
    assert (split_T,sum(split_principal),split_T+sum(split_principal))==(740,68,808)
    print('CARTIER_REVIEW|272 restrictions, 17 minors, integral kernel, residue map and model controls pass',flush=True)
    print('RESIDUE_SMITH|8 units and 8 beta^2 factors; local cokernel killed by beta^2',flush=True)
    return {'model':geometry,'quotient_precision_beta':P,'restriction_entries_checked':272,
        'maximal_minors_checked':17,'restriction_Smith_valuations_beta':factors,
        'cohomology_torsion_length_beta':14,'principal_part_norm_beta':2,
        'primitive_principal_part_values_beta':valuations,
        'residue_map_Smith_valuations_beta':residue_factors,'residue_map_index_beta':16,
        'residue_cokernel_annihilator_beta':2,
        'separated_model_control':{'blowups_per_pair':33,'T_length_beta':740,
            'principal_part_norm_beta':68,'residue_map_index_beta':808,
            'is_a_different_model_and_lattice':True},
        'independent_arithmetic':'integer polynomial quotients, common-factor extraction and unit Schur complements',
        'global_replacement_height_bound_proved':False}

def build(certificate):
    priorpath=DATA/'cm_finite_height_review_d118.json';prior=json.loads(priorpath.read_text())
    assert prior['status']=='pass' and len(prior['sources'])==911
    paths=checked(prior['sources'])+[priorpath,Path(__file__),
        ROOT/'dembele/certificates/cm-cartier-frame-d119.md',DATA/'cm_cartier_frame_sources_d119.json']
    jobs=[]
    for p in sorted(DATA.glob('*d119*')):
        if p.name.startswith('cm_cartier_frame_review_d119'):continue
        paths.append(p)
        if p.suffix!='.json':continue
        data=json.loads(p.read_text())
        paths+=checked([x for x in data.get('sources',[]) if isinstance(x,dict) and 'sha256' in x])
        if p.name.endswith('.job.json'):
            assert data['timeout_seconds']==180 and data['timeout_terminates_process_group']
            paths+=checked([data['log']])
            if data['status']=='pass':paths+=checked([data['driver']])
            else:
                assert data['status']=='failed'
                snapshot=data['failed_driver_snapshot'];paths+=checked([snapshot])
                assert snapshot['sha256']==data['driver']['sha256']
            jobs.append({'receipt':p.name,'status':data['status'],'wall_seconds':data['wall_seconds']})
    assert len(jobs)==2 and sorted(x['status'] for x in jobs)==['failed','pass']
    return {'status':'pass','milestone':'D119','D118_source_hashes_checked_unchanged':911,
        'certificate':certificate,'bounded_jobs':jobs,
        'local_Cartier_divisor_and_dyadic_residue_index_proved_via_companion_report':True,
        'global_principal_parts_frame_bound_proved':False,
        'sufficient_integral_quadric_jet_valuations_beta_unchanged':[25330,25444,25551],
        'actual_integral_quadric_jet_valuations_beta_unchanged':[3794,3745,3728],
        'positive_quadric_jet_exact_vanishing_proved':False,'candidate_identification_proved':False,
        'target_field_polynomial_constructed':False,
        'sources':[source(p) for p in sorted(set(p.resolve() for p in paths))]}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--probe',action='store_true');parser.add_argument('--check',action='store_true');a=parser.parse_args()
    result=calculations()
    if not a.probe:
        result=build(result)
        if a.check:
            previous=json.loads(OUT.read_text());checked(previous['sources']);assert previous==result
        else:
            assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'status':'pass','sources':len(result['sources']),'D118_preserved':911}),flush=True)
    print('PASS|457_CM_CARTIER_FRAME_REVIEW',flush=True)

"""D119: actual dyadic principal parts on the intersecting Cartier CM divisor.

The model, adjunction and local quotient arguments are in the companion report.
Only frozen actual harmonic values are used; no candidate equations are read.
"""
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('local_balls',ROOT/'dembele/pari/427_dyadic_second_order_comparison.py')
f=importlib.util.module_from_spec(s);s.loader.exec_module(f)

def read(name):return json.loads((DATA/(name+'.json')).read_text())

def smith_values(matrix):
    """DVR pivoting using integral elementary row/column operations."""
    a=[row[:] for row in matrix];m=len(a);n=len(a[0]);pivots=[]
    for k in range(n):
        good=[(a[i][j].v,i,j) for i in range(k,m) for j in range(k,n) if a[i][j].known_nonzero()]
        assert good,('unresolved rank',k)
        v,i,j=min(good)
        assert all(a[r][c].lower()>=v for r in range(k,m) for c in range(k,n))
        a[k],a[i]=a[i],a[k]
        for row in a:row[k],row[j]=row[j],row[k]
        pivot=a[k][k];pivots.append(pivot.summary())
        for i in range(k+1,m):
            ratio=a[i][k]/pivot;assert ratio.lower()>=0
            for j in range(k+1,n):a[i][j]=a[i][j]-ratio*a[k][j]
        # Remaining entries in the pivot row/column can be cleared integrally.
        # Their finite centers are never treated as exact zeros in another step.
    return pivots

def graph_data():
    d=read('dyadic_quotient_export_d111');old=read('hyperellipticity_fresh_brandt_d99')
    assert d['matrix']==old['matrix'] and d['stabilizers']==old['stabilizers']
    edges=[14,152,155,158,161,164,167,170,173]
    vertices=[d['edges'][i]['source_class'] for i in edges]
    assert vertices==[4]+list(range(50,58))
    assert all(d['edges'][i]['target_class']==v for i,v in zip(edges,vertices))
    assert [d['stabilizers'][v] for v in vertices]==[32]+[1]*8
    # One-based labels agree with D99. Remove reversed edges, then prune tails.
    n=58;live={i+1 for i in range(n)}
    ordinary=[]
    for i in range(n):
        for j in range(i+1,n):
            if d['matrix'][i][j]:
                assert min(d['matrix'][i][j],d['matrix'][j][i])==1
                length=d['stabilizers'][i]//d['matrix'][j][i]
                assert length*d['matrix'][j][i]==d['stabilizers'][i]
                ordinary.append([i+1,j+1,length])
    contraction=[];anchor=5
    while True:
        neighbors={v:[] for v in live}
        for a,b,length in ordinary:
            neighbors[a].append((b,length));neighbors[b].append((a,length))
        leaves=[v for v in sorted(live) if len(neighbors[v])==1]
        if not leaves:break
        v=leaves[0];w,length=neighbors[v][0]
        contraction.append([v,w,length]);live.remove(v)
        ordinary=[e for e in ordinary if v not in e[:2]]
        if anchor==v:anchor=w
    assert anchor==6 and all(v in live for v in range(51,59))
    assert all(len(neighbors[v])==2 for v in [6]+list(range(51,59)))
    assert len(live)==49 and len(ordinary)==64
    return {'CM_inverted_edges':edges,'CM_components_one_based':[v+1 for v in vertices],
            'ordinary_endpoint_stabilizers':[1]*8,'tail_contractions':contraction,
            'anchor_component_after_tail_contraction':anchor,
            'ordinary_pair_components_retained':list(range(51,59)),
            'ordinary_pair_intersection_beta':33,'distinct_pairs_and_anchor_disjoint':True,
            'model_and_CM_specialization_require_companion_proof':True}

def build():
    geometry=graph_data();raw=read('dyadic_precision200_d115')
    rows=[[f.center(c,raw['coarse_error_beta'][0]) for c in p['coarse_coefficients_beta'][0]] for p in raw['CM_values']]
    fourbeta=f.rational(4)*f.BETA
    assert fourbeta.v==33
    # N at a pair has basis 1/F(t), (t+2 beta)/F(t), F=t^2+4(2+b).
    # Its dual restriction rows are (e_plus-e_minus)/(4 beta), e_plus.
    # dt/du is +4 beta at plus and -4 beta at minus.
    restriction=[[x/(f.BETA**296) for x in rows[0]]]
    pair_values=[]
    for i in range(1,17,2):
        plus=[x/fourbeta for x in rows[i]]
        minus=[-x/fourbeta for x in rows[i+1]]
        divided=[(a-b)/fourbeta for a,b in zip(plus,minus)]
        assert all(x.lower()>=0 for x in plus+minus+divided)
        restriction.extend([divided,plus]);pair_values.append((plus,minus))
    pivots=smith_values(restriction);tau=sum(x['valuation_beta'] for x in pivots)
    inv,detp,failed=f.inverse(restriction[1:]);assert failed is None
    detval=sum(x['valuation_beta'] for x in detp)
    assert detval==280-8*33==16
    q=f.multiply([restriction[0]],inv)[0]
    assert all(x.known_nonzero() for x in q)
    cofactor_values=[detval]+[detval+x.v for x in q]
    assert min(cofactor_values)==tau
    primitive=[f.BETA**(detval-tau)]+[-x*(f.BETA**(detval-tau)) for x in q]
    assert min(x.v for x in primitive)==0
    residual=f.multiply([primitive],restriction)[0]
    assert all(not x.known_nonzero() for x in residual)
    # Evaluate the actual principal part in A_K=K^17. The anchor's local
    # parameter is chosen with differential beta^296 du, a canonical unit.
    values=[primitive[0]]
    for i in range(1,17,2):
        a,b=primitive[i:i+2];values.extend([a+fourbeta*b,a])
    assert all(x.known_nonzero() and x.v>=0 for x in values)
    norm=sum(x.v for x in values);index=tau+norm
    # A embeds in R^17 with eight 2x2 blocks of determinant 4 beta.
    normalization_index=8*fourbeta.v
    # D102's split-evaluation cofactors and this model predict the same
    # kernel valuations, while the different changes the integral lattice.
    split=[280]+[245]*16
    expected=[split[0]-normalization_index-tau]+[
        v+fourbeta.v-normalization_index-tau for v in split[1:]]
    assert [x.v for x in values]==expected
    print('CARTIER_PRINCIPAL_PARTS|'+json.dumps({'Smith_beta':[p['valuation_beta'] for p in pivots],
        'T_length_beta':tau,'principal_norm_beta':norm,'residue_index_beta':index,
        'principal_part_values_beta':[x.v for x in values]}),flush=True)
    return {'status':'pass','milestone':'D119','geometry':geometry,
        'divisor_algebra':'R x product_(j=1)^8 R[t_j]/(t_j^2+4*(2+b))',
        'divisor_degree':17,'normalization_index_beta':normalization_index,
        'divisor_algebra_discriminant_beta':2*normalization_index,
        'restriction_matrix_N_dual':[[x.saved() for x in row] for row in restriction],
        'restriction_Smith_pivots':pivots,'cohomology_torsion_length_beta':tau,
        'restriction_cofactor_valuations_beta':cofactor_values,
        'anchor_deleted_determinant_valuation_beta':detval,
        'primitive_principal_part_coefficients':[x.saved() for x in primitive],
        'primitive_principal_part_values':[x.saved() for x in values],
        'primitive_principal_part_norm_beta':norm,'residue_map_index_beta':index,
        'kernel_residual_error_beta_min':min(x.error for x in residual),
        'finite_map_calculation_certified_from_frozen_actual_values':True,
        'model_and_adjunction_are_mathematical_proofs_not_machine_verified':True,
        'non_dyadic_residue_indices_computed':False,'global_replacement_height_bound_proved':False,
        'actual_moment_precision_increased':False,'candidate_identification_proved':False,
        'target_field_polynomial_constructed':False,
        'sources':[f.coarse.source(p) for p in [Path(__file__),Path(f.__file__),
            DATA/'dyadic_precision200_d115.json',DATA/'dyadic_quotient_export_d111.json',
            DATA/'hyperellipticity_fresh_brandt_d99.json',DATA/'dyadic_integral_frame_d116.json']]}

if __name__=='__main__':
    result=build();out=DATA/'cm_cartier_principal_parts_d119.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print('PASS|456_CM_CARTIER_PRINCIPAL_PARTS',flush=True)

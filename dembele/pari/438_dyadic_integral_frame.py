"""D116: local canonical-fibre and cofactor valuations in the integral harmonic basis.

The integral-basis and global-generation arguments are in the companion report.
This calculation does not identify the horizontal CM residue order or its index.
"""
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('series',ROOT/'dembele/pari/430_dyadic_ratio_series_review.py')
r=importlib.util.module_from_spec(s);s.loader.exec_module(r);f=r.f

def build():
    p=json.loads((DATA/'dyadic_comparison200_d115.json').read_text())
    raw=json.loads((DATA/'dyadic_precision200_d115.json').read_text())
    cycles=json.loads((DATA/'dyadic_graph_residues_d116.json').read_text())
    assert cycles['weighted_harmonic_lattice_equals_integer_cycle_lattice']
    graph=json.loads((DATA/'hyperellipticity_graph_review_d99.json').read_text())
    vertices=graph['stable_vertices'];edges=graph['stable_edges']
    # Every stable component has the full two-dimensional space of residue triples.
    for removed in vertices:
        others=set(vertices)-{removed};seen={min(others)};stack=list(seen)
        while stack:
            u=stack.pop()
            for a,b,_ in edges:
                if removed in [a,b]:continue
                if u not in [a,b]:continue
                v=b if u==a else a
                if v not in seen:seen.add(v);stack.append(v)
        assert seen==others
    transform=[[r.restore(x) for x in row] for row in p['change_of_basis']]
    scales=[min(row['certified_valuations_beta'][0]) for row in raw['CM_values']]
    determinant=sum(x['valuation_beta'] for x in p['evaluation_pivots'])
    q=[r.restore(x) for x in p['frame_relation']]
    assert all(x.known_nonzero() for x in q)
    cofactors=[determinant]+[determinant+x.v for x in q]
    delta=sum(cofactors);section_factor=delta-determinant
    assert scales==[296]+[33]*16
    assert cofactors==[280]+[245]*16 and delta==4200 and section_factor==3920
    lower_bounds=[]
    for ci,row in enumerate(raw['CM_values']):
        jet=[[f.center(cs,raw['coarse_error_beta'][n]) for cs in row['coarse_coefficients_beta'][n]] for n in range(2)]
        jet=f.multiply(jet,transform)
        gaussians=[jet[0][0]*jet[1][j]-jet[0][j]*jet[1][0] for j in range(1,16)]
        raw_lower=min(x.lower() for x in gaussians)
        reduced=2*section_factor-delta+raw_lower-3*scales[ci]
        lower_bounds.append({'CM_index':ci,'Gaussian_vector_coarse_lower_beta':raw_lower,
            'reduced_integral_Gaussian_vector_lower_beta':reduced,
            'pivot_coarse_valuation_beta':gaussians[0].v if gaussians[0].known_nonzero() else None})
    print('INTEGRAL_FRAME|fibre exponents 296/33; cofactors 280/245; evaluation defect 245; Delta 4200',flush=True)
    print('REDUCED_GAUSSIAN_CONTENT|'+json.dumps([x['reduced_integral_Gaussian_vector_lower_beta'] for x in lower_bounds]),flush=True)
    return {'status':'pass','milestone':'D116','stable_vertex_deletions_connected':len(vertices),
       'canonical_fibre_coarse_generator_valuations_beta':scales,
       'evaluation_cofactor_valuations_beta':cofactors,
       'evaluation_map_saturation_defect_valuation_beta':min(cofactors),
       'primitive_evaluation_relation_valuations_beta':[v-min(cofactors) for v in cofactors],
       'frame_determinant_valuation_beta':delta,
       'D103_sections_over_D115_frame_scalar_valuation_beta':section_factor,
       'reduced_Gaussian_content':lower_bounds,
       'stable_integral_basis_and_fibre_interpretation_via_companion_proof':True,
       'CM_horizontal_order_or_residue_map_index_computed':False,
       'global_common_zero_height_subtraction_applied':False,
       'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
       'sources':[f.coarse.source(x) for x in [Path(__file__),Path(r.__file__),Path(f.__file__),
          DATA/'dyadic_comparison200_d115.json',DATA/'dyadic_precision200_d115.json',
          DATA/'dyadic_graph_residues_d116.json',DATA/'hyperellipticity_graph_review_d99.json']]}

if __name__=='__main__':
    result=build();out=DATA/'dyadic_integral_frame_d116.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print('PASS|438_DYADIC_INTEGRAL_FRAME',flush=True)

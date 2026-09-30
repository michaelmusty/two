"""Conditioning audit for the CM-normalized generators of F(C).

Test rational Mobius choices of the global parameter X/Y and the weighted
plane relation supported on 17*i+18*j<=306. This bounded pilot exports no
algebraic equation and never forces a numerically unresolved rank.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import time

import mpmath as mp
import numpy as np
from scipy.linalg import qr, svdvals
from sage.all import matrix

HERE=Path(__file__).resolve().parent
DATA=HERE.parent/'data/computed'
spec=importlib.util.spec_from_file_location('pointed_model_cm',HERE/'92_cm_fibers.py')
cm=importlib.util.module_from_spec(spec)
spec.loader.exec_module(cm)


def weighted_columns(xunit,yunit,dunit,p,q,length):
    """Clear a common denominator before forming the weighted monomials."""
    if q != p+1 or p<2:
        raise ValueError('this pilot requires consecutive pole orders')
    ring=xunit.parent()
    u=ring.gen()
    support=[(i,j) for j in range(p+1) for i in range(q+1) if p*i+q*j<=p*q]
    powers=[]
    for value in [xunit,yunit,dunit]:
        sequence=[ring(1)]
        for _ in range(q):
            sequence.append((sequence[-1]*value).truncate(length))
        powers.append(sequence)
    columns=[]
    for i,j in support:
        product=(powers[0][i]*powers[1][j]).truncate(length)
        product=(product*powers[2][q-i-j]).truncate(length)
        columns.append((u**(p*q-p*i-q*j)*product).truncate(length))
    return support,columns


def triangular_relation(support,columns,p,q,length):
    """Fit distinct pole orders, then retain every unused coefficient to check.

    The coefficient of Y^p is one. All other monomials have distinct
    leading orders after clearing the pole p*q, making this interpolation
    triangular. Existence of a true relation still requires validation.
    Works over exact fields as well as the numerical ball field.
    """
    target=support.index((0,p))
    pivot_order=sorted((p*q-p*i-q*j,k) for k,(i,j) in enumerate(support) if k!=target)
    rows=[n for n,k in pivot_order]
    if len(set(rows))!=len(rows) or max(rows)>=length:
        raise ValueError('distinct leading orders and enough validation jets are required')
    field=columns[0].base_ring()
    coefficients=[field(0) for c in columns]
    coefficients[target]=field(1)
    residual=-columns[target]
    for row,index in pivot_order:
        if columns[index][row]==0:
            raise ValueError('zero leading monomial coefficient')
        coefficients[index]=residual[row]/columns[index][row]
        residual-=coefficients[index]*columns[index]
    return coefficients,-residual,rows


def balanced_relation(columns,training,length,radius,normalization_index):
    """Choose interpolation rows and columns after balancing, then solve in balls.

    Row weights select a coefficient window; they do not remove any of the
    unweighted validation rows. Column scales are undone before returning.
    Callers must first check that the numerical rank is one below full rank.
    """
    field=columns[0].base_ring()
    numeric=np.array([[complex(p[n].mid()) for p in columns] for n in range(training)])
    scaled=numeric*radius**np.arange(training)[:,None]
    peaks=np.max(abs(scaled),axis=0)
    if min(peaks)==0 or not np.isfinite(peaks).all():
        raise ArithmeticError('nonfinite or underflowed model column')
    scales=peaks*np.linalg.norm(scaled/peaks,axis=0)
    scaled/=scales
    _,_,order=qr(scaled,mode='economic',pivoting=True)
    pivots=[int(k) for k in order[:-1]]
    free=int(order[-1])
    ball_scales=[field(str(s)) for s in scales]
    full=matrix(field,[[p[n]*field(radius)**n/scale for p,scale in zip(columns,ball_scales)]
                       for n in range(length)])
    fitted,details=cm.pointed.precise.solve_relations(full,pivots,[free],training)
    coefficients=[field(0) for _ in columns]
    coefficients[free]=1/ball_scales[free]
    for row,index in enumerate(pivots):
        coefficients[index]=fitted[row,0]/ball_scales[index]
    leading=coefficients[normalization_index]
    if leading.contains_zero():
        raise ArithmeticError('chosen plane normalization has unresolved zero coefficient')
    coefficients=[c/leading for c in coefficients]
    residual=sum(c*p for c,p in zip(coefficients,columns))
    details.update({'row_radius':radius,'free_column':free,
                    'column_scales':[str(s) for s in scales]})
    return coefficients,residual,details


def relation_diagnostics(coefficients,residual,columns,fit_rows,training,length):
    """Validate in the original, unweighted coefficient rows."""
    values=[mp.mpc(*cm.pointed.precise.midpoint(c)) for c in coefficients]
    coefficient_norm=mp.sqrt(mp.fsum(abs(c)**2 for c in values))
    residuals=[]
    for n in range(length):
        envelope=mp.fsum(abs(mp.mpc(*cm.pointed.precise.midpoint(c*column[n]))) for c,column in zip(coefficients,columns))
        value=abs(mp.mpc(*cm.pointed.precise.midpoint(residual[n])))
        if not envelope and value:
            raise ArithmeticError('nonzero residual with zero contribution envelope')
        residuals.append(value/envelope if envelope else mp.mpf(0))
    unused=[n for n in range(training) if n not in fit_rows]
    maximum_unused=max(residuals[n] for n in unused)
    maximum_held=max(residuals[training:])
    passed=max(maximum_unused,maximum_held)<mp.mpf('1e-8')
    return {'normalization':'coefficient of the highest pure Y power is one',
            'fit_rows':fit_rows,'unused_training_rows':len(unused),'held_out_rows':length-training,
            'maximum_unused_scaled_residual':mp.nstr(maximum_unused,22),
            'maximum_held_out_scaled_residual':mp.nstr(maximum_held,22),
            'residual_scaling':'unweighted per-row sum of absolute monomial contributions; not a coefficient error bound',
            'coefficient_imaginary_relative_norm':mp.nstr(mp.sqrt(mp.fsum(c.imag**2 for c in values))/coefficient_norm,22),
            'status':'numerical candidate; exactness not established' if passed else 'rejected: unused or held-out residual exceeds 1e-8',
            'passes_empirical_residual_screen':passed,
            'coefficients':[cm.pointed.precise.midpoint(c) for c in coefficients]}


def coordinate_audit(source,normalization):
    xx=[mp.mpc(*v) for v in normalization['normalized_x_laurent_unit']]
    yy=[mp.mpc(*v) for v in normalization['normalized_y_laurent_unit']]
    psi=[]
    for n in range(16):
        psi.append((yy[n]-mp.fsum(xx[k]*psi[n-k] for k in range(1,n+1)))/xx[0])
    original=cm.pointed.precise.arithmetic.pointed.pullback(source,psi,16)
    center=int(mp.nint(-psi[1].real))
    trials=[]
    for shift in range(center-3,center+4):
        triangular=mp.matrix([[mp.binomial(n+1,k+1)*mp.mpf(shift)**(n-k) if n>=k else 0
                               for k in range(16)] for n in range(16)])
        changed=triangular*original
        for exponent in range(-5,6):
            scale=mp.mpf(2)**exponent
            jet=mp.matrix([[changed[n,k]/scale**(n+1) for k in range(16)] for n in range(16)])
            trials.append({'integer_shift':shift,'scale_power_of_two':exponent,
                           'jet_matrix_condition_double':float(np.linalg.cond(np.array(jet.tolist(),complex)))})
    best=min(trials,key=lambda t:t['jet_matrix_condition_double'])
    shifted=psi.copy()
    shifted[1]+=best['integer_shift']
    scaled=[z/(mp.mpf(2)**best['scale_power_of_two']) for z in shifted]
    jet=cm.pointed.precise.arithmetic.pointed.pullback(source,scaled,16)
    return {'parameter_formula':'2^e * X/(Y+c*X), with rational choices of c and 2^e',
            'unmodified_parameter_condition_double':float(np.linalg.cond(np.array(original.tolist(),complex))),
            'coefficient_of_u_in_u_over_t':cm.pointed.decimal(psi[1]),
            'trials':trials,'best':best,
            'best_infinity_norm_condition_at_working_precision':mp.nstr(mp.mnorm(jet,mp.inf)*mp.mnorm(jet**-1,mp.inf),22)}


def plane_audit(map_report,cm_report,key,length,training,y_shift=0):
    first=next(r for r in map_report['maps'] if r['current']['pole_order']==17)[key]
    second=next(r for r in map_report['maps'] if r['current']['pole_order']==18)[key]
    source_key='previous_source' if key=='previous' else 'current_source'
    path=Path(map_report[source_key]['source']['path'])
    gauge=map_report[source_key]['basis_gauge_kind']
    forms,provenance=cm.pointed.forms_from_source(path,length+30,80,gauge)
    if provenance['source']['sha256']!=map_report[source_key]['source']['sha256']:
        raise ValueError('native checkpoint has changed since the map reconstruction')
    ring,field=forms[0].parent(),forms[0].base_ring()
    def ball(pair):
        return field(pair[0],pair[1])
    def numerator(report):
        return sum(ball(c)*forms[i]*forms[j] for c,(i,j) in
                   zip(report['maps'][0]['numerator_coefficients'],report['numerator']['basis_pairs']))
    raw_x,raw_y=numerator(first),numerator(second)
    denominator=forms[15]**2
    norm=cm_report['canonical_cm_normalizations'][key]['normalization']
    mx,sx,my,beta,sy=(ball(norm[k]) for k in
        ['x_mean','x_scale','y_mean','y_projection_on_normalized_x','y_scale'])
    numerator_x=sx*(raw_x-mx*denominator)
    numerator_y=sy*(raw_y-my*denominator-beta*numerator_x)
    numerator_y+=y_shift*numerator_x
    units=[ring([polynomial[n+order] for n in range(length)]) for polynomial,order in
           [(numerator_x,13),(numerator_y,12),(denominator,30)]]
    support,columns=weighted_columns(*units,17,18,length)
    numeric=np.array([[complex(p[n].mid()) for p in columns] for n in range(training)])
    trials=[]
    for radius in [.25,.5,.75,1.]:
        scaled=numeric*radius**np.arange(training)[:,None]
        peaks=np.max(abs(scaled),axis=0)
        if min(peaks)==0 or not np.isfinite(peaks).all():
            raise ArithmeticError('nonfinite or underflowed model column')
        scaled/=peaks
        scaled/=np.linalg.norm(scaled,axis=0)
        singular=svdvals(scaled)
        ratios=singular/singular[0]
        rank=int(sum(ratios>1e-12))
        trials.append({'row_radius':radius,'observed_rank_at_1e_12':rank,
                       'expected_rank':len(support)-1,'relative_singular_values':ratios.tolist(),
                       'final_singular_gap':float(singular[-2]/max(singular[-1],np.finfo(float).tiny)),
                       'rank_resolved_at_1e_12':rank==len(support)-1})
    coefficients,residual,fit_rows=triangular_relation(support,columns,17,18,length)
    triangular=relation_diagnostics(coefficients,residual,columns,fit_rows,307,length)
    balanced=[]
    for trial in trials:
        if not trial['rank_resolved_at_1e_12']:
            continue
        coefficients,residual,details=balanced_relation(columns,training,length,trial['row_radius'],support.index((0,17)))
        diagnostics=relation_diagnostics(coefficients,residual,columns,details['interpolation_rows'],training,length)
        diagnostics['balanced_solve']=details
        balanced.append(diagnostics)
    candidate=any(f['passes_empirical_residual_screen'] for f in [triangular]+balanced)
    return {'source':provenance,'support':support,'monomial_count':len(support),
            'weighted_pole_bound':306,'common_coarse_vanishing_order_removed':234,
            'sampled_jets':training,'second_generator':f'Y + ({y_shift})*X',
            'trials':trials,'triangular_interpolation':triangular,'balanced_interpolations':balanced,
            'rank_resolved_at_1e_12':any(t['rank_resolved_at_1e_12'] for t in trials),
            'status':'numerical equation candidate; accuracy and exactness require further checks' if candidate
                     else 'all fitted plane equations rejected by unweighted unused or held-out rows'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cm-report',type=Path,default=DATA/'cm_pointed_maps_flag_16384.json')
    parser.add_argument('--length',type=int,default=512)
    parser.add_argument('--training',type=int,default=384)
    parser.add_argument('--y-shift',type=int,help='use Y+c*X; default is the best parameter shift')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not 307<=args.training<args.length:
        parser.error('require 307 <= training < length')
    mp.mp.dps=80
    start=time.monotonic()
    cr=json.loads(args.cm_report.read_text())
    map_path=Path(cr['map_source']['path'])
    if hashlib.sha256(map_path.read_bytes()).hexdigest()!=cr['map_source']['sha256']:
        raise ValueError('map report has changed since its CM evaluations')
    mr=json.loads(map_path.read_text())
    source,_=cm.pointed.precise.read_source(Path(mr['current_source']['source']['path']),32,50)
    coordinate=coordinate_audit(source,cr['canonical_cm_normalizations']['current'])
    print('Best rational parameter choice:',coordinate['best'],flush=True)
    planes={}
    y_shift=coordinate['best']['integer_shift'] if args.y_shift is None else args.y_shift
    for key in ['current','previous']:
        planes[key]=plane_audit(mr,cr,key,args.length,args.training,y_shift)
        print(key,planes[key]['status'],[(x['row_radius'],x['observed_rank_at_1e_12']) for x in planes[key]['trials']],flush=True)
        print(key,'triangular unused/held-out residuals:',planes[key]['triangular_interpolation']['maximum_unused_scaled_residual'],
              planes[key]['triangular_interpolation']['maximum_held_out_scaled_residual'],flush=True)
        for fitted in planes[key]['balanced_interpolations']:
            print(key,'balanced radius',fitted['balanced_solve']['row_radius'],fitted['status'],
                  fitted['maximum_unused_scaled_residual'],fitted['maximum_held_out_scaled_residual'],flush=True)
    new,old=([mp.mpc(*c) for c in planes[key]['triangular_interpolation']['coefficients']] for key in ['current','previous'])
    comparison={'coefficient_relative_difference':mp.nstr(mp.sqrt(mp.fsum(abs(a-b)**2 for a,b in zip(new,old)))/mp.sqrt(mp.fsum(abs(a)**2 for a in new)),22),
                'maximum_coefficient_magnitude_current':mp.nstr(max(map(abs,new)),22)}
    print('Triangular coefficient comparison:',comparison,flush=True)
    balanced_comparisons=[]
    for fitted in planes['current']['balanced_interpolations']:
        radius=fitted['balanced_solve']['row_radius']
        previous=next((f for f in planes['previous']['balanced_interpolations'] if f['balanced_solve']['row_radius']==radius),None)
        if previous is None:
            continue
        new,old=([mp.mpc(*c) for c in f['coefficients']] for f in [fitted,previous])
        balanced_comparisons.append({'row_radius':radius,
            'coefficient_relative_difference':mp.nstr(mp.sqrt(mp.fsum(abs(a-b)**2 for a,b in zip(new,old)))/mp.sqrt(mp.fsum(abs(a)**2 for a in new)),22),
            'maximum_coefficient_magnitude_current':mp.nstr(max(map(abs,new)),22)})
    print('Balanced coefficient comparisons:',balanced_comparisons,flush=True)
    rejected=all(not f['passes_empirical_residual_screen'] for plane in planes.values()
                 for f in [plane['triangular_interpolation']]+plane['balanced_interpolations'])
    report={'status':'conditioning pilot; all fitted plane equations rejected' if rejected
                    else 'conditioning pilot; numerical candidate only, no exact equation',
            'cm_report':{'path':str(args.cm_report),'sha256':hashlib.sha256(args.cm_report.read_bytes()).hexdigest()},
            'coordinate':coordinate,'plane':planes,'triangular_comparison':comparison,
            'balanced_comparisons':balanced_comparisons,'wall_seconds':time.monotonic()-start,
            'limitations':['singular values and conditions are numerical diagnostics',
                           'rejected coefficients are neither curve equations nor arithmetic height estimates',
                           'failure to resolve this monomial basis does not rule out the map or other representations']}
    text=json.dumps(report,indent=2,allow_nan=False)+'\n'
    args.output.write_text(text)
    args.output.with_suffix('.out').write_text(text)


if __name__=='__main__':
    main()

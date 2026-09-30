"""Test whether the seventeen order-two CM points form a fiber of a pointed map.

Uses the actual saved elliptic elements and native differential checkpoints.
Evaluate near each elliptic point in two denominator charts; circular
averages avoid division by the common zero of pulled-back differentials.
All accuracy and nonconstancy checks here are empirical.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import time

import mpmath as mp

HERE = Path(__file__).resolve().parent
DATA = HERE.parent/'data/computed'
def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE/filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

pointed = module('cm_fiber_pointed', '91_pointed_map.py')
native = module('cm_fiber_native', 'cm_acb.py')


def elliptic_points(orders=(2,)):
    path = DATA/'expansion_geometry.json'
    raw = json.loads(path.read_text(), parse_float=str)
    center = mp.mpc(*raw['cm'])
    result = []
    for index, (order, pair) in enumerate(zip(raw['elliptic_orders'], raw['elliptic_actions'])):
        if order not in orders:
            continue
        a,b = mp.mpc(*pair[0]),mp.mpc(*pair[1])
        aa,bb,cc = mp.conj(b),mp.conj(a)-a,-b
        roots = [(-bb+s*mp.sqrt(bb*bb-4*aa*cc))/(2*aa) for s in [1,-1]]
        inside = [z for z in roots if abs(z)<1]
        if len(inside) != 1:
            raise ArithmeticError('elliptic element must have exactly one fixed point in the disk')
        z = inside[0]
        w = (z-center)/(1-mp.conj(center)*z)
        result.append({'index': index, 'elliptic_order': order, 'w': w})
    return result, {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def value_in_charts(values, report, map_index=0):
    record = report['maps'][map_index]
    numerator = mp.fsum(mp.mpc(*c)*values[i]*values[j] for c,(i,j) in
                       zip(record['numerator_coefficients'], report['numerator']['basis_pairs']))
    other = mp.fsum(mp.mpc(*c)*values[i]*values[j] for c,(i,j) in
                   zip(record['other_numerator_coefficients'], report['other_numerator']['basis_pairs']))
    den_a, den_b = values[15]**2, values[14]**2
    if min(abs(den_a),abs(den_b)) == 0:
        raise ArithmeticError('zero differential denominator at a probe point')
    first,second = numerator/den_a,other/den_b
    # Report both, choosing only by denominator size after the fixed
    # arithmetic normalization. Neither is an error enclosure.
    chosen = first if abs(den_a)>=abs(den_b) else second
    return chosen, abs(first-second), min(abs(values[14]),abs(values[15]))/max(map(abs,values))


def evaluate_bank(path, details, points, radius, probe_size, count, second=None, basis_gauge='arithmetic'):
    backend = native.Backend(50)
    metadata = json.loads(path.with_suffix('.json').read_text())
    source = backend.read(path, metadata['n'], metadata['columns'])
    jets = source.to_mpmath(rows=32)
    if basis_gauge == 'arithmetic':
        change, _, _ = pointed.precise.arithmetic.arithmetic_change(
            jets.tolist(), list(range(16)), [(16,14,-1),(16,13,1)])
    else:
        change = jets[:16,:]**-1
    nodes, slices = [], []
    for point in points:
        u = (point['w']/radius)**32
        if abs(u)>=1:
            raise ValueError('CM representative lies outside the source evaluation circle')
        delta = min(probe_size, (1-abs(u))/8)
        for scale in [mp.mpf(1),mp.mpf('.5')]:
            start = len(nodes)
            nodes.extend(u+scale*delta*mp.exp(2j*mp.pi*k/count) for k in range(count))
            slices.append((point,delta*scale,start))
    values = native.evaluate(source, backend.vector(nodes)).to_mpmath()*change
    result = []
    for point,delta,start in slices:
        samples = [value_in_charts(list(values[start+k,:]), details) for k in range(count)]
        average = mp.fsum(s[0] for s in samples)/count
        result.append({'point_index': point['index'], 'probe_radius': mp.nstr(delta,20),
                       'average': pointed.decimal(average),
                       'maximum_two_chart_discrepancy': mp.nstr(max(s[1] for s in samples),22),
                       'minimum_denominator_relative_to_forms': mp.nstr(min(s[2] for s in samples),22)})
        if second is not None:
            samples = [value_in_charts(list(values[start+k,:]), second) for k in range(count)]
            result[-1]['second_map'] = {
                'average': pointed.decimal(mp.fsum(s[0] for s in samples)/count),
                'maximum_two_chart_discrepancy': mp.nstr(max(s[1] for s in samples),22)}
    return result


def trace_normalization(xs, ys):
    """Fix L(17P), then L(18P), by algebraic traces over the CM divisor.

    No complex conjugation or root extraction occurs. The construction
    is invariant under x -> a*x+b and y -> c*y+d*x+e.
    """
    if len(xs) != len(ys) or not xs:
        raise ValueError('equal nonempty evaluation lists are required')
    mean = lambda values: sum(values)/len(values)
    mx = mean(xs)
    centered = [x-mx for x in xs]
    m2, m3 = mean([x**2 for x in centered]), mean([x**3 for x in centered])
    if m2 == 0 or m3 == 0:
        raise ValueError('CM trace normalization has a zero second or third moment')
    sx = m2/m3
    xx = [sx*x for x in centered]
    my = mean(ys)
    beta = mean([(y-my)*x for y,x in zip(ys,xx)])/mean([x*x for x in xx])
    orthogonal = [y-my-beta*x for y,x in zip(ys,xx)]
    n2, n3 = mean([y*y for y in orthogonal]), mean([y**3 for y in orthogonal])
    if n2 == 0 or n3 == 0:
        raise ValueError('second CM trace normalization has a zero moment')
    sy = n2/n3
    yy = [sy*y for y in orthogonal]
    return xx, yy, {'x_mean': mx, 'x_scale': sx, 'y_mean': my,
                    'y_projection_on_normalized_x': beta, 'y_scale': sy,
                    'x_centered_moment2': m2, 'x_centered_moment3': m3,
                    'y_orthogonal_moment2': n2, 'y_orthogonal_moment3': n3}


def normalized_report(probes, half=True):
    rows = probes[1::2] if half else probes[0::2]
    xs = [mp.mpc(*r['average']) for r in rows]
    ys = [mp.mpc(*r['second_map']['average']) for r in rows]
    xx, yy, constants = trace_normalization(xs,ys)
    polynomial = [mp.mpc(1)]
    for x in xx:
        new = [mp.mpc(0)]*(len(polynomial)+1)
        for i,c in enumerate(polynomial):
            new[i]-=x*c
            new[i+1]+=c
        polynomial = new
    return {'normalization': {key:pointed.decimal(z) for key,z in constants.items()},
            'normalized_x_values': [pointed.decimal(z) for z in xx],
            'normalized_y_values': [pointed.decimal(z) for z in yy],
            'x_cm_value_polynomial_ascending': [pointed.decimal(z) for z in polynomial]}


def normalized_laurent(xs, ys, pole_x, pole_y, constants, length=32):
    """Units u^pole_x*X and u^pole_y*Y and t=X/Y, using exact ring operations."""
    if pole_y != pole_x+1 or min(len(xs),len(ys)) < length:
        raise ValueError('need consecutive pole orders and sufficiently many Laurent coefficients')
    mx,sx,my,beta,sy = (constants[k] for k in
        ['x_mean','x_scale','y_mean','y_projection_on_normalized_x','y_scale'])
    xx = [sx*(xs[i]-(mx if i==pole_x else 0)) for i in range(length)]
    yy = [sy*(ys[i]-(my if i==pole_y else 0)-(beta*xx[i-1] if i else 0)) for i in range(length)]
    if xx[0] == 0 or yy[0] == 0:
        raise ValueError('the functions must have exactly the stated pole orders')
    quotient=[]
    for n in range(length):
        quotient.append((xx[n]-sum(yy[k]*quotient[n-k] for k in range(1,n+1)))/yy[0])
    return xx,yy,[xx[0]*0]+quotient[:-1]


def map_parameter(first, second, normalization):
    constants={k:mp.mpc(*v) for k,v in normalization['normalization'].items()}
    xs=[mp.mpc(*v) for v in first['maps'][0]['raw_coordinate_laurent_coefficients']]
    ys=[mp.mpc(*v) for v in second['maps'][0]['raw_coordinate_laurent_coefficients']]
    xx,yy,t=normalized_laurent(xs,ys,17,18,constants)
    return {'x_laurent_shift':-17,'y_laurent_shift':-18,
            'normalized_x_laurent_unit':[pointed.decimal(z) for z in xx],
            'normalized_y_laurent_unit':[pointed.decimal(z) for z in yy],
            'global_uniformizer_series':[pointed.decimal(z) for z in t]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--map', type=Path, required=True, help='script 91 report containing pole order 17')
    parser.add_argument('--probe', default='0.00001')
    parser.add_argument('--samples', type=int, default=8)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.samples<4 or not mp.mpf(0)<mp.mpf(args.probe)<mp.mpf('.001'):
        parser.error('require at least four samples and a probe radius in (0,.001)')
    mp.mp.dps=80
    start=time.monotonic()
    report=json.loads(args.map.read_text())
    selected=next(r for r in report['maps'] if r['current']['pole_order']==17)
    second=next(r for r in report['maps'] if r['current']['pole_order']==18)
    points, geometry=elliptic_points()
    current_source=report['current_source']['source']
    previous_source=report['previous_source']['source']
    if current_source['radius']!=previous_source['radius']:
        raise ValueError('checkpoints must use the same coordinate radius')
    radius=mp.mpf(str(current_source['radius']))
    basis_gauge=report['current_source'].get('basis_gauge_kind','arithmetic')
    current=evaluate_bank(Path(current_source['path']),selected['current'],points,radius,mp.mpf(args.probe),args.samples,second['current'],basis_gauge)
    previous=evaluate_bank(Path(previous_source['path']),selected['previous'],points,radius,mp.mpf(args.probe),args.samples,second['previous'],basis_gauge)
    alternate=evaluate_bank(Path(current_source['path']),selected['alternate_fit'],points,radius,mp.mpf(args.probe),args.samples,second['alternate_fit'],basis_gauge)
    comparison=[]
    for i,point in enumerate(points):
        c,c2=current[2*i:2*i+2]
        old=previous[2*i+1]
        alt=alternate[2*i+1]
        value=mp.mpc(*c2['average'])
        discrepancies=[abs(value-mp.mpc(*q['average'])) for q in [c,old,alt]]
        discrepancies.append(mp.mpf(c2['maximum_two_chart_discrepancy']))
        comparison.append({'point_index':point['index'],'elliptic_order':point['elliptic_order'],
                           'w':pointed.decimal(point['w']), 'value':c2['average'],
                           'probe_radius_change':mp.nstr(discrepancies[0],22),
                           'cross_bank_change':mp.nstr(discrepancies[1],22),
                           'same_bank_fit_change':mp.nstr(discrepancies[2],22),
                           'two_chart_discrepancy':mp.nstr(discrepancies[3],22),
                           'maximum_empirical_discrepancy':mp.nstr(max(discrepancies),22)})
    values=[mp.mpc(*r['value']) for r in comparison]
    spread=max(abs(a-b) for a in values for b in values)
    error=max(mp.mpf(r['maximum_empirical_discrepancy']) for r in comparison)
    normalizations={name:normalized_report(probes,half) for name,probes,half in
        [('current',current,True),('larger_probe',current,False),('previous',previous,True),('alternate_fit',alternate,True)]}
    for name,n in normalizations.items():
        key='current' if name=='larger_probe' else name
        n.update(map_parameter(selected[key],second[key],n))
    normalized_comparisons={}
    for name,values in normalizations.items():
        if name=='current':
            continue
        normalized_comparisons[name]={key:mp.nstr(max(abs(mp.mpc(*a)-mp.mpc(*b)) for a,b in
            zip(normalizations['current'][key],values[key])),22) for key in
            ['normalized_x_values','normalized_y_values','x_cm_value_polynomial_ascending',
             'global_uniformizer_series']}
    result={'status':'numerical CM-fiber test; no exact divisor equivalence certified',
            'map_source':{'path':str(args.map),'sha256':hashlib.sha256(args.map.read_bytes()).hexdigest()},
            'geometry':geometry,'tested_divisor':'sum of the 17 order-two elliptic points minus 17*P32',
            'fiber_condition':'all 17 values must coincide for this divisor to be principal',
            'sample_count_per_circle':args.samples,'comparisons':comparison,
            'maximum_value_spread':mp.nstr(spread,25),'maximum_empirical_discrepancy':mp.nstr(error,25),
            'spread_over_empirical_discrepancy':mp.nstr(spread/error,20) if error else None,
            'consistent_with_one_fiber_at_empirical_accuracy':bool(spread<=10*error),
            'current_probes':current,'previous_probes':previous,'alternate_fit_probes':alternate,
            'canonical_cm_normalizations':normalizations,'canonical_cm_comparisons':normalized_comparisons,
            'canonical_functions':'X=sx*(x-mean(x)); Y=sy*(y-mean(y)-beta*X); t=X/Y is a global rational uniformizer at P',
            'limitations':['same-bank checks share the analytic checkpoint','circular averaging and sampled errors are not certified bounds'],
            'wall_seconds':time.monotonic()-start}
    output=json.dumps(result,indent=2,allow_nan=False)+'\n'
    args.output.write_text(output)
    args.output.with_suffix('.out').write_text(output)
    print('CM points:',len(points),'value spread:',result['maximum_value_spread'],flush=True)
    print('largest empirical discrepancy:',result['maximum_empirical_discrepancy'])
    print('one fiber:',result['consistent_with_one_fiber_at_empirical_accuracy'])
    print('CM-normalized map comparisons:',normalized_comparisons)


if __name__=='__main__':
    main()

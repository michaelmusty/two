"""Independent section-product diagnostics; no algebraic recognition is claimed."""
import argparse
import importlib
from itertools import combinations_with_replacement
import json
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.linalg import svd, subspace_angles

pilot = importlib.import_module('68_cm_differentials')
DATA = pilot.DATA


def products(c, length):
    return np.array([np.convolve(c[:,i], c[:,j])[:length]
                     for i in range(16) for j in range(i,16)]).T


def precise_generator_check(c, radius):
    """Every nonrotational side action, independent points, 50-digit geometry."""
    mp.mp.dps=50
    raw=json.loads((DATA/'expansion_geometry.json').read_text(),parse_float=str)
    rng=np.random.default_rng(71420)
    left,right,weights=[],[],[]
    for pair in raw['cm_actions']:
        a,b=mp.mpc(*pair[0]),mp.mpc(*pair[1])
        if abs(b)<mp.mpf('1e-10'):
            continue
        q=-b/a
        midpoint=q/(1+1/abs(a))
        perturb=mp.mpf('.005')*mp.sqrt(float(rng.random()))*mp.exp(2j*mp.pi*float(rng.random()))
        w=(midpoint+perturb)/(1+mp.conj(midpoint)*perturb)
        v=(a*w+b)/(mp.conj(b)*w+mp.conj(a))
        derivative=1/(mp.conj(b)*w+mp.conj(a))**2
        if max(abs(w),abs(v))>=radius:
            raise RuntimeError('independent side test leaves expansion circle')
        r=mp.mpf(str(radius))
        left.append(complex((w/r)**32))
        right.append(complex((v/r)**32))
        weights.append(complex(derivative*(v/w)**31))
    lhs=np.polynomial.polynomial.polyval(np.array(left),c).T
    rhs=np.array(weights)[:,None]*np.polynomial.polynomial.polyval(np.array(right),c).T
    residual=np.linalg.norm(lhs-rhs,axis=0)/np.maximum(np.linalg.norm(lhs,axis=0),np.linalg.norm(rhs,axis=0))
    return {'samples':len(left),'relative_residuals':residual.tolist()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--basis',type=Path,default=DATA/'cm_differentials_8192_refined.npz')
    parser.add_argument('--output',type=Path,default=DATA/'differential_audit.json')
    args=parser.parse_args()
    data=np.load(args.basis)
    c=data['coefficients']
    radius=float(data['radius'])
    transform=np.linalg.inv(np.linalg.qr(c[:256])[1])
    basis=c@transform
    product=products(basis[:512],512)
    _,singular,vh=svd(product[:256],full_matrices=False)
    product_rank=int(sum(singular>singular[0]*1e-7))
    quadrics=vh[product_rank:].conj().T
    validation=product[256:]@quadrics
    triples=list(combinations_with_replacement(range(16),3))
    triple_index={triple:i for i,triple in enumerate(triples)}
    pairs=list(combinations_with_replacement(range(16),2))
    multiples=np.zeros((len(triples),16*quadrics.shape[1]),dtype=complex)
    for variable in range(16):
        for index,pair in enumerate(pairs):
            multiples[triple_index[tuple(sorted((*pair,variable)))],
                      variable*quadrics.shape[1]:(variable+1)*quadrics.shape[1]]=quadrics[index]
    cubic_singular=svd(multiples,compute_uv=False)
    cubic_rank=int(sum(cubic_singular>cubic_singular[0]*1e-7))
    report={'basis':str(args.basis),'radius':radius,
            'product_singular_values':singular.tolist(),
            'product_rank_at_relative_1e_minus_7':product_rank,
            'expected_hyperelliptic_rank':31,
            'quadric_dimension':quadrics.shape[1],
            'linear_times_quadric_rank':cubic_rank,
            'degree3_quotient_dimension':len(triples)-cubic_rank,
            'expected_canonical_degree3_dimension':75,
            'linear_times_quadric_singular_values':cubic_singular.tolist(),
            'heldout_quadric_relative_frobenius_residual':float(np.linalg.norm(validation)/np.linalg.norm(product[256:])),
            'precise_generator_check':precise_generator_check(c,radius),
            'jet16_condition_number':float(np.linalg.cond(c[:16])),
            'comparisons':{}}
    for name in ['cm_differentials_4096_fullradius','cm_differentials_8192_eigen']:
        previous=np.load(DATA/(name+'.npz'))['coefficients']
        report['comparisons'][name]={'max_principal_angle_first128':float(max(subspace_angles(c[:128],previous[:128])))}
    # Control: differentials t^j h(s) ds for a formal hyperelliptic chart.
    # A nonlinear coordinate and common unit preserve the product rank 31.
    t=np.zeros(128); t[1:3]=[1,.1]
    h=np.zeros(128); h[0]=1
    for i in range(1,128):
        h[i]=h[i-1]*(-.5-i+1)/i*.1
    controls=[h]
    for i in range(15):
        controls.append(np.convolve(controls[-1],t)[:128])
    control=svd(products(np.array(controls).T,128),compute_uv=False)
    report['hyperelliptic_control_rank']=int(sum(control>control[0]*1e-10))
    assert report['hyperelliptic_control_rank']==31
    if max(report['precise_generator_check']['relative_residuals'])>1e-7:
        report['status']='FAIL: independent automorphy residual exceeds 1e-7'
    elif product_rank==45:
        report['status']='numerical product rank agrees with the exact D45 nonhyperellipticity obstruction; no algebraic recognition'
    elif product_rank!=31:
        report['status']='UNRESOLVED: unexpected product rank; numerical data only'
    else:
        report['status']='numerically consistent with hyperellipticity; no algebraic recognition or certification'
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    np.savez(args.output.with_suffix('.npz'),basis_transform=transform,quadrics=quadrics)
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()

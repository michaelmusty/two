"""Fix a CM jet/period gauge and recover real numerical canonical equations.

Algebraic recognition is a separate step: real floating-point coefficients
are not exact equations over a number field.
"""
import argparse
import json
from itertools import combinations_with_replacement
from pathlib import Path

import numpy as np
from scipy.linalg import qr, lstsq, svdvals

DATA=Path(__file__).resolve().parents[1]/'data/computed'
PAIRS=list(combinations_with_replacement(range(16),2))


def normalize(path, length=512):
    data=np.load(path)
    return normalize_coefficients(data['coefficients'][:length])


def normalize_coefficients(coefficients):
    length=len(coefficients)
    jet=coefficients[:16]
    h=coefficients[:length]@np.linalg.inv(jet)
    jet_roundoff=float(np.max(abs(h[:16]-np.eye(16))))
    # These entries are exact by the definition of the normalized basis.
    h[:16]=np.eye(16)
    alpha=3*h[16,15]
    if abs(alpha)<1e-6:
        raise RuntimeError('chosen period gauge is near zero')
    rows=np.arange(length)
    columns=np.arange(16)
    # G_i(v)=alpha^i H_i(v/alpha). Weight row n by |alpha|^n
    # to avoid magnifying coefficient sizes at large n.
    weighted=h*np.exp(-1j*np.angle(alpha)*rows)[:,None]*alpha**columns[None,:]
    jets=h[:64]*alpha**(columns[None,:]-rows[:64,None])
    return weighted,jets,alpha,jet_roundoff,float(np.linalg.cond(jet))


def gauge_control():
    """Independence of arbitrary basis changes and local-coordinate scaling."""
    rng=np.random.default_rng(7401)
    c=rng.normal(size=(64,16))+1j*rng.normal(size=(64,16))
    c[:16]=np.eye(16)
    c[16,15]=1/3
    change=np.linalg.qr(rng.normal(size=(16,16))+1j*rng.normal(size=(16,16)))[0]
    parameter_scale=np.exp(.271j)
    altered=(parameter_scale**np.arange(64))[:,None]*(c@change)
    original_jets=normalize_coefficients(c)[1]
    altered_jets=normalize_coefficients(altered)[1]
    difference=float(np.linalg.norm(original_jets-altered_jets)/np.linalg.norm(original_jets))
    assert difference<1e-11
    return difference


def products(series):
    return np.array([np.convolve(series[:,i],series[:,j])[:len(series)] for i,j in PAIRS]).T


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--basis',type=Path,default=DATA/'cm_differentials_10240_refined.npz')
    parser.add_argument('--comparison',type=Path,default=DATA/'cm_differentials_8192_refined.npz')
    parser.add_argument('--output',type=Path,default=DATA/'canonical_gauge.json')
    args=parser.parse_args()
    series,jets,alpha,roundoff,condition=normalize(args.basis)
    previous,previous_jets,previous_alpha,_,_=normalize(args.comparison)
    imaginary=float(np.linalg.norm(series.imag)/np.linalg.norm(series))
    if imaginary>1e-7:
        raise RuntimeError('period gauge does not give a numerically real series')
    full=products(series)
    train=full[:256].real
    scales=np.linalg.norm(train,axis=0)
    scaled=train/scales
    singular=svdvals(scaled)
    short=train[:61]/np.linalg.norm(train[:61],axis=0)
    short_singular=svdvals(short)
    rank=int(sum(singular>singular[0]*1e-8))
    if rank!=45:
        raise RuntimeError(f'product rank {rank}, expected 45 from prior audit')
    _,_,pivots=qr(scaled,mode='economic',pivoting=True)
    basis=pivots[:45]
    rest=pivots[45:]
    fit=lstsq(scaled[:,basis],scaled[:,rest],lapack_driver='gelsy')[0]
    fit=fit*scales[rest][None,:]/scales[basis][:,None]
    equations=np.zeros((136,91))
    equations[rest,np.arange(91)]=1
    equations[basis,:]=-fit
    normalized_equations=equations/np.linalg.norm(equations,axis=0)
    validation=full[256:]@normalized_equations
    comparison_products=products(previous)
    cross=comparison_products@normalized_equations
    old_train=comparison_products[:256].real
    old_fit=lstsq(old_train[:,basis]/scales[basis],
                  old_train[:,rest]/scales[rest],lapack_driver='gelsy')[0]
    old_fit=old_fit*scales[rest][None,:]/scales[basis][:,None]
    jet_difference=np.linalg.norm(jets-previous_jets)/np.linalg.norm(jets)
    report={'status':'real numerical canonical equations in a period-normalized jet gauge; not algebraically recognized',
            'basis_and_coordinate_invariance_control_relative_error':gauge_control(),
            'basis':str(args.basis),'comparison_basis':str(args.comparison),
            'alpha':[float(alpha.real),float(alpha.imag)],
            'alpha_absolute_value':float(abs(alpha)),
            'alpha_definition':'3 times the u^16 coefficient of the jet-normalized differential H_15(u)',
            'normalized_jet_16_15':[float(jets[16,15].real),float(jets[16,15].imag)],
            'jet16_condition_number':condition,'jet_normalization_roundoff':roundoff,
            'weighted_series_imaginary_relative_norm':imaginary,
            'normalized_jet_relative_difference_first64':float(jet_difference),
            'alpha_relative_difference':float(abs(alpha-previous_alpha)/abs(alpha)),
            'product_rank':rank,'scaled_product_singular_values':singular.tolist(),
            'first61_product_rank':int(sum(short_singular>short_singular[0]*1e-8)),
            'first61_singular_values_45_46':short_singular[44:46].tolist(),
            'pivot_product_condition_number':float(np.linalg.cond(scaled[:,basis])),
            'pivot_pairs':[PAIRS[i] for i in basis],
            'free_pairs':[PAIRS[i] for i in rest],
            'quadric_count':91,
            'max_absolute_quadric_coefficient':float(np.max(abs(equations))),
            'quadric_coefficient_relative_difference':float(np.linalg.norm(fit-old_fit)/np.linalg.norm(fit)),
            'quadric_coefficient_max_absolute_difference':float(np.max(abs(fit-old_fit))),
            'heldout_quadric_relative_frobenius_residual':float(np.linalg.norm(validation)/np.linalg.norm(full[256:])),
            'other_truncation_quadric_relative_frobenius_residual':float(np.linalg.norm(cross)/np.linalg.norm(comparison_products)),
            'nontrivial_normalized_jet_samples':[
                {'n':n,'i':i,'value':float(jets[n,i].real),
                 'truncation_difference':float(abs(jets[n,i]-previous_jets[n,i]))}
                for n,i in [(16,14),(16,13),(16,12),(17,15),(17,14),(18,15)]]}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    np.savez(args.output.with_suffix('.npz'),quadrics=equations,pairs=np.array(PAIRS),
             pivots=basis,free=rest,normalized_jets=jets,alpha=alpha,weighted_series=series)
    text=json.dumps(report,indent=2)
    args.output.with_suffix('.out').write_text(text+'\n')
    print(text)


if __name__=='__main__':
    main()

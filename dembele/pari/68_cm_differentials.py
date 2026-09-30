"""Numerical CM-centered differential pilot, using the order-32 stabilizer.

This is a diagnostic, not an algebraic model or a certified basis. Run with
Sage's Python (NumPy/SciPy). Forms have F(w)=w^31 H(w^32) in CM disk coordinates.
"""
import argparse
import json
from pathlib import Path
import time

import numpy as np
from scipy.linalg import svd, solve
from scipy.sparse.linalg import eigs

DATA = Path(__file__).resolve().parents[1] / 'data/computed'


def load_actions():
    geometry = json.loads((DATA / 'expansion_geometry.json').read_text())
    raw = np.asarray(geometry['cm_actions'])
    ab = raw[..., 0] + 1j * raw[..., 1]
    ab = ab[np.abs(ab[:, 1]) > 1e-10]  # rotations are handled exactly below
    a, b = ab.T
    q = -b / a
    phase = a / a.conjugate()
    delta = 1 / np.abs(a)**2  # avoid cancellation in 1-|q|^2
    return q, phase, delta


def reduce_points(points, actions, max_steps=100, words=None):
    q, phase, delta = actions
    w = np.asarray(points, dtype=complex).copy()
    derivative = np.ones(len(w), dtype=complex)
    steps = np.zeros(len(w), dtype=int)
    active = np.arange(len(w))
    step = 2 * np.pi / 32
    for _ in range(max_steps):
        if not len(active):
            break
        z = w[active]
        # Include all right rotations by the elliptic stabilizer without
        # explicitly expanding the side-generator list by a factor of 32.
        turns = np.rint((np.angle(q)[:, None] - np.angle(z)[None, :]) / step)
        rotation = np.exp(1j * step * turns)
        rotated = rotation * z[None, :]
        denominator = 1 - q.conjugate()[:, None] * rotated
        ratios = np.abs(denominator)**2 / delta[:, None]
        best = np.argmin(ratios, axis=0)
        slots = np.arange(len(z))
        move = ratios[best, slots] < 1 - 1e-10
        active = active[move]
        best = best[move]
        slots = slots[move]
        den = denominator[best, slots]
        rot = rotation[best, slots]
        zrot = rotated[best, slots]
        if words is not None:
            for index, generator, turn in zip(active, best, turns[best, slots]):
                words[index].append((int(generator), int(turn)))
        old_radius = np.abs(w[active])
        w[active] = phase[best] * (zrot - q[best]) / den
        derivative[active] *= rot * phase[best] * delta[best] / den**2
        steps[active] += 1
        if np.any(np.abs(w[active]) > old_radius + 1e-8):
            raise RuntimeError('reduction increased radius')
    else:
        raise RuntimeError('reduction step cap exceeded')
    metric = (1 - np.abs(w)**2) / (1 - np.abs(points)**2)
    error = float(np.max(np.abs(np.abs(derivative) / metric - 1)))
    return w, derivative, steps, error


def precise_nodes(points, words, radius, count, offset, digits, as_numpy=True):
    """Replay floating-point selected group words using exported 57-digit actions."""
    import mpmath as mp
    mp.mp.dps = digits
    geometry = json.loads((DATA/'expansion_geometry.json').read_text(), parse_float=str)
    ab = [(mp.mpc(*pair[0]), mp.mpc(*pair[1])) for pair in geometry['cm_actions']]
    ab = [(a,b) for a,b in ab if abs(b)>mp.mpf('1e-10')]
    actions = [(-b/a,a/mp.conj(a),1/abs(a)**2) for a,b in ab]
    rotations = [mp.exp(2j*mp.pi*k/32) for k in range(32)]
    r = mp.mpf(str(radius))
    xs, weights = [], []
    metric_error = mp.mpf(0)
    for index, word in enumerate(words):
        w = r*mp.exp(2j*mp.pi*(index+mp.mpf(str(offset)))/(32*count))
        v, derivative = w, mp.mpc(1)
        for generator, turn in word:
            q,phase,delta = actions[generator]
            rot = rotations[turn%32]
            z = rot*v
            den = 1-mp.conj(q)*z
            v = phase*(z-q)/den
            derivative *= rot*phase*delta/den**2
        metric_error=max(metric_error,abs(abs(derivative)*(1-abs(w)**2)/(1-abs(v)**2)-1))
        xs.append((v/r)**32)
        weights.append(derivative*(v/w)**31)
    if not as_numpy:
        return xs,weights,metric_error
    return np.array(xs,dtype=complex),np.array(weights,dtype=complex),float(metric_error)


def operator_from_nodes(n, nodes, weights, offset=0.37, order='C'):
    """Assemble the double operator, including from separately replayed nodes."""
    x, weight = np.asarray(nodes, dtype=complex), np.asarray(weights, dtype=complex)
    count = len(x)
    if n <= 0 or count < n or x.ndim != 1 or weight.shape != x.shape:
        raise ValueError('require one-dimensional nodes/weights and 0<n<=samples')
    # Assemble in column blocks to avoid retaining a samples-by-n matrix.
    matrix = np.empty((n,n),dtype=complex,order=order)
    rowphase=np.exp(-2j*np.pi*np.arange(n)*offset/count)/count
    for start in range(0,n,128):
        stop=min(start+128,n)
        values=np.vander(x,N=stop-start,increasing=True)*(weight*x**start)[:,None]
        matrix[:,start:stop]=np.fft.fft(values,axis=0)[:n]*rowphase[:,None]
    return matrix


def sampled_operator(n, radius, actions, oversample=2, offset=0.37, replay_digits=0):
    count = n * oversample
    theta = 2*np.pi*(np.arange(count)+offset)/count
    w = radius * np.exp(1j*theta/32)
    words = [[] for _ in w] if replay_digits else None
    v, derivative, steps, metric_error = reduce_points(w, actions, words=words)
    x = (v/radius)**32
    weight = derivative * (v/w)**31
    if replay_digits:
        x,weight,metric_error=precise_nodes(w,words,radius,count,offset,replay_digits)
    matrix = operator_from_nodes(n, x, weight, offset)
    stats = {'samples': count, 'radius': radius, 'max_reduced_radius': float(max(abs(v))),
             'max_steps': int(max(steps)), 'unmoved': int(np.count_nonzero(steps == 0)),
             'metric_relative_error': metric_error,
             'max_scaled_power': float(max(abs(x))),
             'max_reduced_scaled_monomial': float(max(abs(x))**n),
             'radius_power_32n_not_error_bound': float(radius**(32*n)),
             'replay_digits': replay_digits}
    return matrix, stats


def heldout(coefficients, radius, actions, seed=20260915, count=128):
    rng = np.random.default_rng(seed)
    # Different radii and arbitrary angles, independent of the Cauchy nodes.
    w = (radius - 0.00004*rng.random(count)) * np.exp(2j*np.pi*rng.random(count))
    v, derivative, steps, error = reduce_points(w, actions)
    lhs = np.vander((w/radius)**32, N=len(coefficients), increasing=True) @ coefficients
    rhs = (derivative*(v/w)**31)[:, None] * (
        np.vander((v/radius)**32, N=len(coefficients), increasing=True) @ coefficients)
    scale = np.maximum(np.linalg.norm(lhs, axis=0), np.linalg.norm(rhs, axis=0))
    residual = np.linalg.norm(lhs-rhs, axis=0)/np.maximum(scale, 1e-300)
    return {'relative_residuals': residual.tolist(), 'nontrivial_samples': int(np.count_nonzero(steps)),
            'metric_relative_error': error}


def generator_check(coefficients, radius, actions, seed=742, count=512):
    """Test actual side transformations at independent overlap points."""
    q, phase, delta = actions
    rng = np.random.default_rng(seed)
    which = rng.integers(len(q), size=count)
    q, phase, delta = q[which], phase[which], delta[which]
    midpoint = q/(1+np.sqrt(delta))
    perturb = .2*np.sqrt(rng.random(count))*np.exp(2j*np.pi*rng.random(count))
    w = (midpoint+perturb)/(1+midpoint.conjugate()*perturb)
    den = 1-q.conjugate()*w
    v = phase*(w-q)/den
    derivative = phase*delta/den**2
    keep = (abs(w)<radius*.999999) & (abs(v)<radius*.999999)
    w,v,derivative=w[keep],v[keep],derivative[keep]
    lhs = np.vander((w/radius)**32,N=len(coefficients),increasing=True)@coefficients
    rhs = (derivative*(v/w)**31)[:,None]*(np.vander((v/radius)**32,N=len(coefficients),increasing=True)@coefficients)
    scale=np.maximum(np.linalg.norm(lhs,axis=0),np.linalg.norm(rhs,axis=0))
    residual=np.linalg.norm(lhs-rhs,axis=0)/np.maximum(scale,1e-300)
    return {'samples':len(w),'relative_residuals':residual.tolist()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n', type=int, default=4096)
    parser.add_argument('--radius', type=float, default=0.99991)
    parser.add_argument('--geometry-only', action='store_true')
    parser.add_argument('--kernel-cutoff', type=float)
    parser.add_argument('--solver',choices=['svd','eigen','block','refine'],default='svd')
    parser.add_argument('--initial',type=Path)
    parser.add_argument('--replay-digits',type=int,default=0)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.n<64 or not 0<args.radius<1:
        parser.error('require n>=64 and 0<radius<1')
    if args.replay_digits and not 20<=args.replay_digits<=50:
        parser.error('replay precision must be zero or between 20 and 50 digits')
    started = time.monotonic()
    actions = load_actions()
    if args.geometry_only:
        report = []
        for r in [.999, .9993, .9995, .9997, .9998, .9999, .99995]:
            w = r*np.exp(2j*np.pi*(np.arange(2048)+.37)/(32*2048))
            v, d, steps, error = reduce_points(w, actions)
            report.append({'radius': r, 'max_reduced_radius': float(max(abs(v))),
                           'unmoved': int(np.count_nonzero(steps==0)), 'max_steps': int(max(steps)),
                           'metric_relative_error': error})
        print(json.dumps(report, indent=2))
        return
    matrix, stats = sampled_operator(args.n, args.radius, actions,replay_digits=args.replay_digits)
    print('Assembled', stats, flush=True)
    selection = {}
    if args.solver=='refine':
        if not args.initial:
            raise ValueError('refine requires an initial 16-dimensional basis')
        initial_data=np.load(args.initial)
        if float(initial_data['radius'])!=args.radius:
            raise ValueError('initial basis uses a different coefficient scaling radius')
        initial=initial_data['coefficients']
        if initial.shape[1]!=16 or initial.shape[0]>args.n:
            raise ValueError('initial basis must have 16 columns and at most n rows')
        if initial.shape[0]<args.n:
            initial=np.pad(initial,((0,args.n-initial.shape[0]),(0,0)))
        # Stabilize I-A on its approximate kernel instead of iterating A,
        # which also has unwanted eigenvalues of modulus greater than one.
        matrix *= -1
        matrix[np.diag_indices(args.n)] += 1
        for start in range(0,args.n,128):
            stop=min(args.n,start+128)
            matrix[:,start:stop] += initial@initial[start:stop].conj().T
        refined=solve(matrix,initial,overwrite_a=True,check_finite=False)
        # (I-A)refined = initial*(I-initial^*refined).
        defect=initial@(np.eye(16)-initial.conj().T@refined)
        coefficients,r=np.linalg.qr(refined)
        residual=np.linalg.norm(defect@np.linalg.inv(r),axis=0)
        singular=np.array([])
        selection={'operator_residuals_via_stabilized_equation':residual.tolist()}
    elif args.solver=='block':
        if args.initial:
            coefficients=np.load(args.initial)['coefficients']
            if coefficients.shape!=(args.n,16):
                raise ValueError('initial basis must have shape (n,16)')
        else:
            rng=np.random.default_rng(719)
            coefficients=np.linalg.qr(rng.normal(size=(args.n,16))+1j*rng.normal(size=(args.n,16)))[0]
        history=[]
        for iteration in range(160):
            projected=matrix@coefficients
            residual=np.linalg.norm(projected-coefficients,axis=0)
            history.append(float(max(residual)))
            if max(residual)<1e-11:
                break
            coefficients=np.linalg.qr(projected)[0]
        singular=np.array([])
        selection={'block_iterations':iteration+1,'block_residual_history':history,
                   'operator_residuals':residual.tolist()}
    elif args.solver=='eigen':
        rng=np.random.default_rng(719)
        eigenvalues,eigenvectors=eigs(matrix,k=32,which='LM',tol=1e-11,maxiter=3000,
                                      v0=rng.normal(size=args.n)+1j*rng.normal(size=args.n))
        order=np.argsort(abs(eigenvalues-1))
        coefficients=np.linalg.qr(eigenvectors[:,order[:16]])[0]
        singular=np.array([])
        selection={'eigenvalues':[[float(v.real),float(v.imag)] for v in eigenvalues[order]],
                   'operator_residuals':np.linalg.norm(matrix@coefficients-coefficients,axis=0).tolist()}
    else:
        _, singular, vh = svd(matrix-np.eye(args.n), full_matrices=False, check_finite=False)
        coefficients = vh[-16:].conj().T
    if args.kernel_cutoff is not None and args.solver=='svd':
        approximate = vh[singular < args.kernel_cutoff].conj().T
        if approximate.shape[1] < 16:
            raise RuntimeError('fewer than 16 candidate directions below cutoff')
        _, core_singular, core_vh = svd(approximate[:64], full_matrices=False)
        coefficients = approximate @ core_vh[:16].conj().T
        selection = {'kernel_cutoff':args.kernel_cutoff, 'candidate_dimension':approximate.shape[1],
                     'core_singular_values':core_singular.tolist()}
    report = {'n': args.n, 'solver':args.solver, **stats, 'smallest_singular_values': singular[-24:].tolist(),
              **selection,
              'heldout': heldout(coefficients, args.radius, actions),
              'generator_check': generator_check(coefficients,args.radius,actions),
              'wall_seconds': time.monotonic()-started}
    worst=max(report['heldout']['relative_residuals']+report['generator_check']['relative_residuals'])
    report['status']=('numerical candidate; inspect gap, stability and section-product audit'
                      if worst<1e-6 else 'insufficient accuracy or failed solver; do not use as a validated basis')
    print(json.dumps(report, indent=2), flush=True)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+'\n')
        np.savez(args.output.with_suffix('.npz'), coefficients=coefficients, radius=args.radius,
                 singular=singular)


if __name__ == '__main__':
    main()

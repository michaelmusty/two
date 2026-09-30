"""Bounded prototype: high-precision residuals with double LU corrections.

Uses an actual small Cauchy operator, but N=64 is NOT a genus-16 basis.
Tests the linear-solver mechanism only, not truncation or automorphy accuracy.
"""
import importlib
import json
from pathlib import Path
import time
import mpmath as mp
import numpy as np
from scipy.linalg import lu_factor,lu_solve

pilot=importlib.import_module('68_cm_differentials')
DATA=pilot.DATA

def cauchy_apply(vector,nodes,weights,offset):
    """Reference matrix-free operator: high-precision Horner and direct DFT.

    No conversion to double is allowed in this residual path. A compiled
    Horner/FFT replacement is needed for a full-size run.
    """
    values=[]
    for z,w in zip(nodes,weights):
        value=mp.mpc(0)
        for coefficient in reversed(list(vector)): value=value*z+coefficient
        values.append(w*value)
    count=len(nodes)
    return mp.matrix([sum(values[t]*mp.exp(-2j*mp.pi*k*(t+offset)/count)
                          for t in range(count))/count for k in range(len(vector))])

def main():
    started=time.monotonic()
    mp.mp.dps=50
    n=64; count=2*n; radius=.99991; offset=.37
    points=radius*np.exp(2j*np.pi*(np.arange(count)+offset)/(32*count))
    words=[[] for _ in points]
    pilot.reduce_points(points,pilot.load_actions(),words=words)
    nodes,weights,metric_error=pilot.precise_nodes(points,words,radius,count,offset,50,as_numpy=False)
    # Direct arbitrary-precision DFT. This intentionally small implementation
    # is a reference for a future fast matrix-free residual evaluator.
    powers=[[mp.mpc(1)] for _ in nodes]
    for row,x in zip(powers,nodes):
        for j in range(1,n): row.append(row[-1]*x)
    operator=mp.matrix(n,n)
    for k in range(n):
        phases=[weights[t]*mp.exp(-2j*mp.pi*k*(t+mp.mpf('.37'))/count)/count for t in range(count)]
        for j in range(n): operator[k,j]=sum(phases[t]*powers[t][j] for t in range(count))
    raw=np.load(DATA/'cm_differentials_10240_refined.npz')['coefficients'][:n]
    b=np.linalg.qr(raw)[0]
    B=mp.matrix([[mp.mpc(float(z.real),float(z.imag)) for z in row] for row in b])
    matrix=mp.eye(n)-operator+B*B.H
    rhs=B[:,0]
    def apply(v):
        return v-cauchy_apply(v,nodes,weights,mp.mpf('.37'))+B*(B.H*v)
    agreement=mp.norm(apply(rhs)-matrix*rhs)/mp.norm(matrix*rhs)
    assert agreement<mp.mpf('1e-45')
    low=np.array(matrix.tolist(),dtype=complex)
    factor=lu_factor(low)
    initial=lu_solve(factor,np.array(list(rhs),dtype=complex))
    x=mp.matrix([mp.mpc(float(z.real),float(z.imag)) for z in initial])
    history=[]
    for step in range(5):
        residual=rhs-apply(x)
        relative=mp.norm(residual)/mp.norm(rhs)
        history.append(mp.nstr(relative,12))
        if relative<mp.mpf('1e-44'): break
        # Normalize before conversion, so even tiny residuals retain their
        # relative precision when passed through the double-precision solve.
        scale=mp.norm(residual)
        correction=lu_solve(factor,np.array([complex(z/scale) for z in residual]))
        x+=scale*mp.matrix([mp.mpc(float(z.real),float(z.imag)) for z in correction])
    assert mp.mpf(history[-1])<mp.mpf('1e-40')
    # A misleading alternative: residuals from the rounded matrix converge
    # to the rounded problem, not the intended high-precision one.
    rounded=mp.matrix([[mp.mpc(float(z.real),float(z.imag)) for z in row] for row in low])
    rounded_solution=mp.lu_solve(rounded,rhs)
    rounded_true_residual=mp.norm(rhs-matrix*rounded_solution)/mp.norm(rhs)
    report={'status':'linear refinement prototype PASS; no validated differential basis',
            'n':n,'samples':count,'decimal_digits':50,
            'matrix_condition_2_double':float(np.linalg.cond(low)),
            'matrix_free_vs_explicit_relative_difference':mp.nstr(agreement,12),
            'high_precision_residual_history':history,
            'rounded_matrix_solution_true_residual':mp.nstr(rounded_true_residual,12),
            'geometry_metric_error':mp.nstr(metric_error,12),
            'wall_seconds':time.monotonic()-started,
            'limitations':['N=64 is intentionally insufficient for the target curve',
                'direct DFT assembly is not scalable to N=12288',
                'geometry input has only about 57 decimal digits',
                'no interval or truncation certification']}
    path=DATA/'mixed_precision_refinement.json'
    path.write_text(json.dumps(report,indent=2)+'\n')
    path.with_suffix('.out').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()

"""Try the hyperelliptic ansatz at an ordinary point, with a positive control.

High precision in this diagnostic does not add accuracy to numerical inputs.
"""
import json
from pathlib import Path
import mpmath as mp
import numpy as np

DATA=Path(__file__).resolve().parents[1]/'data/computed'
L=64

def mul(a,b):
    return [sum(a[j]*b[i-j] for j in range(i+1)) for i in range(L)]

def div(a,b):
    c=[]
    for i in range(L):
        c.append((a[i]-sum(b[j]*c[i-j] for j in range(1,i+1)))/b[0])
    return c

def power(a,k):
    r=[mp.mpf(1)]+[mp.mpf(0)]*(L-1)
    for _ in range(k): r=mul(r,a)
    return r

def normalize(c):
    return c*mp.inverse(c[:16,:])

def reconstruct(c):
    c=normalize(c)
    # Need L+15 source coefficients after dividing out vanishing orders.
    a=[c[i+14,14] for i in range(L)]
    b=[c[i+15,15] for i in range(L)]
    unit=div(b,a)
    x=[mp.mpf(0)]+unit[:-1]
    h=div(a,power(unit,14))
    columns=[h]
    for _ in range(15): columns.append(mul(columns[-1],x))
    predicted=normalize(mp.matrix(list(zip(*columns))))
    # Independent higher coefficients, after the first sixteen fitted jets.
    defects=[abs(predicted[n,i]-c[n,i]) for n in range(16,25) for i in range(16)]
    first=max(abs(predicted[16,i]-c[16,i]) for i in range(16))
    report={'first_unfitted_jet_max_defect':float(first),
            'first_unfitted_jet_input_scale':float(max(abs(c[16,i]) for i in range(16))),
            'jets_16_through_24_max_defect':float(max(defects))}
    if max(defects)>mp.mpf('1e-6'):
        report['status']='rejected: reconstructed hyperelliptic differential space fails unused jets'
        return report
    # For omega_0=h du=dx/y, reconstruct y^2 and solve f(x)=y^2.
    dx=[(i+1)*x[i+1] for i in range(L-1)]+[mp.mpf(0)]
    y2=power(div(dx,h),2)
    powers=[power(x,i) for i in range(45)]
    f=[]
    for n in range(45):
        f.append((y2[n]-sum(f[i]*powers[i][n] for i in range(n)))/powers[n][n])
    report['coefficients_35_through_44_max']=float(max(abs(v) for v in f[35:]))
    report['status']='hyperelliptic ansatz passes local diagnostic; not an exact model'
    return report

def main():
    mp.mp.dps=100
    # Known smooth genus-16 curve y^2=1+x+x^33 at x=0.
    # Its polynomial is squarefree: a repeated root would have x=-33/32
    # and x^32=-1/33, incompatible over Q.
    # Construct sufficiently many differential coefficients by sqrt recurrence.
    length=L+15
    f=[mp.mpf(int(i in (0,1,33))) for i in range(length)]
    root=[mp.mpf(1)]
    for n in range(1,length):
        root.append((f[n]-sum(root[j]*root[n-j] for j in range(1,n)))/2)
    inv=[mp.mpf(1)]
    for n in range(1,length): inv.append(-sum(root[j]*inv[n-j] for j in range(1,n+1)))
    control=mp.matrix([[inv[n-i] if n>=i else 0 for i in range(16)] for n in range(length)])
    positive=reconstruct(control)
    assert positive['jets_16_through_24_max_defect']<1e-50
    assert positive['coefficients_35_through_44_max']<1e-50
    # A nonlinear chart x=u/(1-u/10), including dx/du, and a nontrivial
    # invertible basis change must give the same successful diagnostic.
    s=mp.mpf('0.1')
    changed=mp.matrix([[sum(inv[m]*mp.binomial(n+1,m+i+1)*s**(n-m-i)
                           for m in range(n-i+1)) if n>=i else 0
                       for i in range(16)] for n in range(length)])
    change=mp.eye(16)
    for i in range(15): change[i,i+1]=i+1
    changed_positive=reconstruct(changed*change)
    assert changed_positive['jets_16_through_24_max_defect']<1e-45
    assert changed_positive['coefficients_35_through_44_max']<1e-45, changed_positive
    results={'method':'x=H15/H14; h=H14/x^14; test span(h*x^i), i=0..15',
             'precision_note':'100-digit arithmetic on double-precision input; not new input accuracy',
             'positive_control':positive,'changed_chart_and_basis_control':changed_positive,'target':{}}
    for n in (8192,10240):
        raw=np.load(DATA/f'cm_differentials_{n}_refined.npz')['coefficients'][:length]
        c=mp.matrix([[mp.mpc(float(z.real),float(z.imag)) for z in row] for row in raw])
        results['target'][str(n)]=reconstruct(c)
    path=DATA/'hyperelliptic_reconstruction.json'
    path.write_text(json.dumps(results,indent=2)+'\n')
    path.with_suffix('.out').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()

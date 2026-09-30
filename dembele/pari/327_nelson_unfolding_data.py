"""D91: exact cusp identification and unit classes in the saved CM shell.

The finite shell is a pilot subset, not a complete cutoff for the
unit-invariant Mellin sum. No candidate curve or differential bank is read.
"""
import hashlib
import json
from pathlib import Path
from collections import Counter
from sage.all import (AA, QQ, ZZ, NumberField, PolynomialRing, QuaternionAlgebra,
                      RealField, ComplexField, matrix, vector)

ROOT=Path(__file__).resolve().parents[2]; DATA=ROOT/"dembele/data/computed"


def source(p):
    return {"path":str(p.relative_to(ROOT)),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}


def main():
    inputs=[DATA/"cm_orbit.json",DATA/"nelson_cm_lattice_d90.json",DATA/"nelson_cm_shell_d90.json"]
    raw,local,shell=[json.loads(p.read_text()) for p in inputs]
    R=PolynomialRing(QQ,"s");s=R.gen();F=NumberField(s**8-8*s**6+20*s**4-16*s**2+2,"b");b=F.gen()
    B=QuaternionAlgebra(F,b-b*b,-1)
    def quat(v):return B([F([QQ(c) for c in v[8*j:8*(j+1)]]) for j in range(4)])
    def coords(q):return vector(QQ,sum([list(c.vector()) for c in q.coefficient_tuple()],[]))
    basis=[quat(v) for v in raw["quaternion_export"]["order_basis"]]
    O=matrix(QQ,[coords(q) for q in basis]).transpose();inv=O.inverse()
    beta=quat(local["arithmetic"]["CM_beta_power_coordinates"])
    pi=2+b;delta=16/pi;assert beta.reduced_norm()==pi
    dual=matrix(QQ,local["arithmetic"]["relative_dual_in_order_coordinates"])
    left=matrix(QQ,[inv*coords(beta**(-1)*q) for q in basis]).transpose()
    relation=dual.inverse()*left
    assert abs(relation.det())==1 and all(c in ZZ for c in relation.list())
    assert abs(left.det())==QQ(1)/4
    # Fix the original split matrix embedding and its CM point.
    places=sorted(F.embeddings(AA),key=lambda v:v(b));split=places[4]
    RF=RealField(200);CC=ComplexField(200);root=RF(split(b));sqrt_a=(root-root**2).sqrt()
    def real(x):return RF(split(x))
    def embed(q):
        a0,a1,a2,a3=[real(c) for c in q.coefficient_tuple()]
        return matrix(RF,[[a0+a1*sqrt_a,a2+a3*sqrt_a],[-a2+a3*sqrt_a,a0-a1*sqrt_a]])
    bb=embed(beta);x0=(bb[0,0]-bb[1,1])/(2*bb[1,0]);y0=real(pi).sqrt()/abs(bb[1,0])
    sigma=matrix(RF,[[y0.sqrt(),x0/y0.sqrt()],[0,1/y0.sqrt()]])
    def xy(q):
        m=sigma.inverse()*embed(q)*sigma
        return (CC(m[0,0]+m[1,1])+CC.gen()*(m[0,1]-m[1,0]))/2, \
               (CC(m[0,0]-m[1,1])+CC.gen()*(m[0,1]+m[1,0]))/2
    xb,yb=xy(beta);assert abs(yb)<RF(10)**(-45) and abs(xb.real())<RF(10)**(-45)
    # Use integral reduced coordinates for the finite enumeration.
    change=matrix(QQ,local["enumeration_pilot"]["reduction_change"])
    rb=[sum((change[j,k]*basis[j] for j in range(32)),B(0)) for k in range(32)]
    groups={};records=[];duplicates=[];norm_counts=Counter();discarded=Counter()
    for index,v in enumerate(shell["all_representatives_reduced_coordinates"]):
        q=sum((v[j]*rb[j] for j in range(32) if v[j]),B(0))
        n=q.reduced_norm();nn=ZZ(n.norm())
        if nn<=0:discarded['nonpositive_norm']+=1;continue
        if nn>64:discarded['norm_above_64']+=1;continue
        assert n.is_integral()
        norm_counts[int(nn)]+=1
        coefficients=q.coefficient_tuple();pivot=next(c for c in coefficients if c)
        projective=tuple(tuple(c/pivot) for c in coefficients)
        key=(projective,int(nn));matched=None
        for previous in groups.get(key,[]):
            ratio=pivot/previous["pivot"]
            if ratio.is_integral() and (1/ratio).is_integral():
                assert q==ratio*previous["q"] and abs(ratio.norm())==1
                matched=previous;break
        if matched is not None:
            duplicates.append({"shell_index":index,"representative_index":matched["index"],
                               "unit_power_coordinates":[str(c) for c in ratio.vector()]})
            continue
        parallel=(q+beta*q*beta**(-1))/2;u=parallel.reduced_norm()
        assert u and n
        invariant=nn*u/n
        A=real(invariant)
        X,Y=xy(q);rho=abs(Y/X)**2
        assert A>0 and abs(abs(X)**2-real(u))<RF(10)**(-35)
        assert abs(abs(X)**2-abs(Y)**2-real(n))<RF(10)**(-35)
        # The cusp change divides the multiplicative majorant by Norm(pi).
        qdual=beta**(-1)*q;Xd,Yd=xy(qdual)
        nd=qdual.reduced_norm();pd=(qdual+beta*qdual*beta**(-1))/2
        Ad=real(nd.norm()*pd.reduced_norm()/nd)
        assert abs(Ad/A-QQ(1)/2)<RF(10)**(-35)
        for degree in [0,1,3,5]:
            base=(X/abs(X))**(2+degree+1)*(Y.conjugate()/abs(X))**max(0,degree-1)
            after=(Xd/abs(Xd))**(2+degree+1)*(Yd.conjugate()/abs(Xd))**max(0,degree-1)
            if degree in [1,3,5]:assert abs(after-base)<RF(10)**(-35)
        record={"index":len(records),"shell_index":index,"norm_ideal_norm":int(nn),
                "quaternion_power_coordinates":[str(c) for c in coords(q)],
                "norm_generator":[str(c) for c in n.vector()],
                "multiplicative_majorant_field_element":[str(c) for c in invariant.vector()],
                "multiplicative_majorant":str(A),"rho":str(rho),
                "X":[str(X.real()),str(X.imag())],"Y":[str(Y.real()),str(Y.imag())],
                "mixed":bool(q!=parallel and parallel),
                "known_prime_support": int(nn)&(int(nn)-1)==0}
        records.append(record);groups.setdefault(key,[]).append({"pivot":pivot,"q":q,"index":record["index"]})
    assert records and duplicates
    result={"status":"pass: cusp identity and finite unit-class pilot",
            "cusp_dual_equals_beta_inverse_order":True,
            "cusp_basis_change_in_relative_dual":[[str(c) for c in row] for row in relation.rows()],
            "cusp_majorant_ratio":"1/2","odd_derivative_phase_sign":1,
            "CM_point":[str(x0),str(y0)],"positive_norm_ideal_bound":64,
            "half_shell_norm_counts":dict(sorted(norm_counts.items())),"discarded":dict(discarded),
            "unit_classes":records,"unit_duplicate_witnesses":duplicates,
            "complete_unit_invariant_cutoff":False,"Shimura_derivative_computed":False,
            "sources":[source(p) for p in [Path(__file__)]+inputs]}
    path=DATA/"nelson_unfolding_data_d91.json";assert not path.exists()
    path.write_text(json.dumps(result,indent=2)+"\n")
    print('Positive norm counts:',dict(sorted(norm_counts.items())))
    print('Unit classes:',len(records),'duplicates:',len(duplicates),'mixed classes:',sum(r['mixed'] for r in records))
    print('PASS|327_nelson_unfolding_data')


if __name__=="__main__":main()

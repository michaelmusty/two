"""D107 bounded exact probe of the CM real structure and embedding sign.

Uses the saved order and elliptic quaternion embeddings, not analytic evaluations.
The antiholomorphic map's identification with canonical conjugation is supplied
by D106 marked rigidity in the companion proof.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
from sage.all import AA, QQ, ZZ, NumberField, PolynomialRing, QuaternionAlgebra, matrix, vector

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"dembele/data/computed"
OUT=DATA/"cm_real_structure_d107.json"


def source(p):
    p=Path(p).resolve()
    return {"path":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}


def main():
    saved=json.loads((DATA/"cm_orbit.json").read_text())
    raw=saved["quaternion_export"]
    R=PolynomialRing(QQ,"x");x=R.gen()
    F=NumberField(x**8-8*x**6+20*x**4-16*x*x+2,"b");b=F.gen()
    B=QuaternionAlgebra(F,b-b*b,-1);I,J,K=B.gens()
    def quat(row):
        return B([F([QQ(c) for c in row[8*j:8*(j+1)]]) for j in range(4)])
    def coords(q):
        return vector(QQ,sum([list(c.vector()) for c in q.coefficient_tuple()],[]))
    basis=[quat(v) for v in raw["order_basis"]]
    O=matrix(QQ,[coords(z) for z in basis]).transpose();inverse=O.inverse()
    conjugation=matrix(QQ,[inverse*coords(I*z/I) for z in basis]).transpose()
    integral=all(c in ZZ for c in conjugation.list())
    assert integral and abs(conjugation.det())==1
    norm=I.reduced_norm()
    places=sorted(F.embeddings(AA),key=lambda p:p(b))
    signs=[int(p(norm).sign()) for p in places]
    assert signs==[1,1,1,1,-1,1,1,1]
    witness=-4*b**6+22*b**4-28*b*b+4*b+2
    betas=[2/witness*quat(v) for v in raw["elliptics"]]
    assert all(z*z==B(-2-b) for z in betas)
    base=betas[8]
    target=-I*base/I
    u=target+base
    assert u != B(0) and target*u==u*base and all(p(u.reduced_norm())>0 for p in places)
    M=NumberField(R(saved["CM_orbit"]["CM_polynomial_ascending"]),"beta")
    beta=M.gen();classes=M.class_group(proof=True)
    assert classes.order()==17
    old_generator=M.fractional_ideal([M([QQ(c) for c in row]) for row in saved["CM_orbit"]["class_generator_ideal_basis"]])
    generator_exponent=int(classes(old_generator).list()[0]);assert generator_exponent%17
    def label(ideal):
        return int(classes(ideal).list()[0])*pow(generator_exponent,-1,17)%17
    spec=importlib.util.spec_from_file_location("d59",ROOT/"dembele/pari/96_cm_orbit.py")
    d59=importlib.util.module_from_spec(spec);spec.loader.exec_module(d59)
    ib=M.integral_basis()
    def embed(z):
        return sum((B(c)*base**j for j,c in enumerate(z.list())),B(0))
    image=matrix(QQ,[coords(u*embed(z)) for z in ib]).transpose()
    columns=d59.preimage_lattice(inverse,image)
    gens=[sum((columns[j,k]*ib[j] for j in range(16)),M(0)) for k in range(16)]
    ideal=M.fractional_ideal(gens)
    expected=matrix(QQ,[z.vector() for z in ib]).transpose()*columns
    actual=matrix(QQ,[z.vector() for z in ideal.basis()]).transpose()
    change=expected.inverse()*actual
    assert abs(change.det())==1 and all(c in ZZ for c in change.list())
    assert ideal.norm()*u.reduced_norm().norm()==1
    reflection=label(ideal)
    # Rickards fdom.c: q -> [q0+q1*sqrt(a), -(q2+q3*sqrt(a));
    #                       q2-q3*sqrt(a), q0-q1*sqrt(a)].
    split=places[4];root=split(b);sqrt_a=(root-root*root).sqrt()
    c=split(base[2])-split(base[3])*sqrt_a
    sign=int(c.sign())
    labels=saved["CM_orbit"]["class_labels_in_point_order"]
    permutation=[labels.index((reflection-v)%17) for v in labels]
    fixed=[i for i,j in enumerate(permutation) if i==j]
    prime=M.ideal(31,beta-19);assert prime.norm()==31
    report={"status":"pass","milestone":"D107","negative_normalizer":"I; I^2=b-b^2",
            "normalizer_conjugation_in_order_basis":[[str(c) for c in row] for row in conjugation.rows()],
            "normalizer_determinant":str(conjugation.det()),"normalizer_reduced_norm":str(norm),
            "normalizer_norm_signs_in_increasing_b_order":signs,
            "normalizer_absolute_norm":str(norm.norm()),
            "reference_index":8,"conjugate_reference_oriented_beta":[str(c) for c in coords(target)],
            "positive_intertwiner":[str(c) for c in coords(u)],
            "intersection_ideal_basis_power_coordinates":[[str(c) for c in z.list()] for z in ideal.basis()],
            "ideal_norm":str(ideal.norm()),"norm_product":"1",
            "reflection_class_offset":reflection,"conjugation_point_permutation":permutation,
            "unique_real_point_index":fixed,
            "Rickards_lower_left_sign":sign,"CM_beta_imaginary_sign_at_reference":sign,
            "prime31_beta19_class_in_saved_generator":label(prime),
            "class_number_proved":17,
            "sources":[source(Path(__file__)),source(DATA/"cm_orbit.json"),
                       source(ROOT/"dembele/pari/96_cm_orbit.py"),
                       source(ROOT/"dembele/pari/94_cm_arithmetic.py"),
                       source(ROOT/"dembele/vendor/rickards-fdom/fdom.c")],
            "scope":"Exact normalizer, ideal class and algebraic real sign. Canonical real-structure identification uses D106 rigidity; no differential evaluation."}
    assert not OUT.exists()
    OUT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:report[k] for k in ["status","reflection_class_offset","unique_real_point_index","CM_beta_imaginary_sign_at_reference","prime31_beta19_class_in_saved_generator"]}),flush=True)
    print("PASS|D107_CM_REAL_STRUCTURE",flush=True)


if __name__=="__main__":
    main()

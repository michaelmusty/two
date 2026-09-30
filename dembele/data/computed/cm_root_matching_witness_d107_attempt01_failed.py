"""D107 finite witnesses for exact CM root matching.

Newton iterates only propose rational disk centers. Script 393 independently
certifies the disks and the algebraic equality by rational arithmetic and norms.
No curve differential or function value is read or computed.
"""
import hashlib
import json
from pathlib import Path
from sage.all import AA, QQ, ZZ, ComplexField, NumberField, PolynomialRing, QuaternionAlgebra, matrix, vector

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"dembele/data/computed"
OUT=DATA/"cm_root_matching_witness_d107.json"


def source(p):
    p=Path(p).resolve()
    return {"path":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}


def main():
    orbit=json.loads((DATA/"cm_orbit.json").read_text())
    real=json.loads((DATA/"cm_real_structure_d107.json").read_text())
    R=PolynomialRing(QQ,"x");x=R.gen()
    f=R([68,-2,-128,16,80,40,32,-80,-32,64,0,-16,16,8,0,0,-2,1])
    C=ComplexField(4096)
    fc=f.change_ring(C);fd=fc.derivative()
    denominator=ZZ(10)**1100
    centers=[]
    for re,im in orbit["field_root_action"]["complex_roots"]:
        z=C(re,im)
        for _ in range(8):
            z-=fc(z)/fd(z)
        centers.append([str(ZZ((z.real()*denominator).round())),
                        str(ZZ((z.imag()*denominator).round()))])
    F=NumberField(x**8-8*x**6+20*x**4-16*x*x+2,"b");b=F.gen()
    split=next(p for p in F.embeddings(AA) if 0<p(b)<1)
    b_approx=C.real_field()(split(b))
    beta_approx=C(0,-(2+b_approx).sqrt())
    beta_center=[str(ZZ((beta_approx.real()*denominator).round())),
                 str(ZZ((beta_approx.imag()*denominator).round()))]
    # Compact low-precision sign witnesses, independently checked by 393.
    small_denominator=ZZ(10)**80
    b_center=ZZ((b_approx*small_denominator).round())
    sqrt_center=ZZ(((b_approx-b_approx*b_approx).sqrt()*small_denominator).round())
    B=QuaternionAlgebra(F,b-b*b,-1);I,J,K=B.gens()
    def quat(row):
        return B([F([QQ(c) for c in row[8*j:8*(j+1)]]) for j in range(4)])
    def coords(q):
        return vector(QQ,sum([list(c.vector()) for c in q.coefficient_tuple()],[]))
    raw=orbit["quaternion_export"]
    O=matrix(QQ,[coords(quat(v)) for v in raw["order_basis"]]).transpose()
    Oinv=O.inverse()
    witness=-4*b**6+22*b**4-28*b*b+4*b+2
    base=2/witness*quat(raw["elliptics"][8])
    M=NumberField(R(orbit["CM_orbit"]["CM_polynomial_ascending"]),"beta")
    ideal=M.fractional_ideal([M([QQ(c) for c in row]) for row in real["intersection_ideal_basis_power_coordinates"]])
    generators=ideal.gens_reduced(proof=True)
    assert len(generators)==1
    generator=generators[0]
    assert M.fractional_ideal(generator)==ideal
    def embed(z):
        return sum((B(c)*base**j for j,c in enumerate(z.list())),B(0))
    u=quat(real["positive_intertwiner"])
    unit=u*embed(generator)
    assert all(c in ZZ for c in Oinv*coords(unit))
    assert all(c in ZZ for c in Oinv*coords(unit**(-1)))
    assert unit*base/unit==-I*base/I
    reflection=unit**(-1)*I
    assert reflection*base==-base*reflection
    assert reflection.reduced_trace()==0 and all(p(unit.reduced_norm())>0 for p in F.embeddings(AA))
    report={"status":"pass","milestone":"D107",
            "root_center_common_denominator":str(denominator),
            "root_centers_real_imaginary_numerators":centers,
            "beta_center_real_imaginary_numerators":beta_center,
            "proposed_root_disk_radius":"1/10^1080",
            "Newton_working_bits":4096,"Newton_iterations_per_root":8,
            "centers_are_proposals_pending_rational_Rouche_review":True,
            "small_sign_center_common_denominator":str(small_denominator),
            "split_b_center_numerator":str(b_center),
            "sqrt_b_minus_b_squared_center_numerator":str(sqrt_center),
            "small_sign_radius":"1/10^60",
            "reflection_ideal_principal_generator_power_coordinates":[str(c) for c in generator.list()],
            "positive_unit_quaternion":[str(c) for c in coords(unit)],
            "positive_unit_order_coordinates":[str(c) for c in Oinv*coords(unit)],
            "positive_unit_inverse_order_coordinates":[str(c) for c in Oinv*coords(unit**(-1))],
            "point_fixing_negative_normalizer":[str(c) for c in coords(reflection)],
            "point_fixing_normalizer_reduced_norm":[str(c) for c in reflection.reduced_norm().vector()],
            "point_fixing_normalizer_anticommutes_with_reference_beta":True,
            "sources":[source(Path(__file__)),source(DATA/"cm_orbit.json"),source(DATA/"cm_real_structure_d107.json")],
            "scope":"Finite root disk centers and exact normalizer witness; no Shimura tangent or jet evaluation."}
    assert not OUT.exists()
    OUT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":"pass","root_centers":17,"center_decimal_digits":1100,
                      "principal_reflection_ideal_generator_found":True,
                      "positive_unit_and_inverse_integral":True,
                      "negative_normalizer_anticommutator_zero":True}),flush=True)
    print("PASS|D107_CM_MATCHING_WITNESS",flush=True)


if __name__=="__main__":
    main()


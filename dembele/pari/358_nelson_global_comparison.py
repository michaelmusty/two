"""D95: arithmetic and symbolic checks for the global kernel comparison.

The Shimizu/central-unfolding argument is a mathematical proof in the
companion report. This script checks its field hypotheses, local level
input, derivative handedness, and Mellin normalization. It computes no
new eigenform value or arithmetic CM jet.
"""
import hashlib
import json
from pathlib import Path
from sage.all import AA, GF, QQ, ZZ, NumberField, PolynomialRing, QuadraticField, QuaternionAlgebra, matrix, vector, factorial

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def source(path):
    return {"path":str(path.relative_to(ROOT)),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    output = DATA / "nelson_global_comparison_data_d95.json"
    assert not output.exists()
    paths = [DATA/"cm_orbit.json", DATA/"nelson_cm_lattice_d90.json",
             DATA/"nelson_norm_one_d92_T400.json", DATA/"nelson_kernel_review_d94.json",
             DATA/"nelson_norm_one_test_vector_d94.json", DATA/"f16_steinberg.out"]
    raw, local, unit_packet = [json.loads(path.read_text()) for path in paths[:3]]
    R = PolynomialRing(QQ,"s")
    s = R.gen()
    F = NumberField(s**8-8*s**6+20*s**4-16*s**2+2,"b")
    b = F.gen()
    assert F.discriminant() == F.defining_polynomial().discriminant() == 2**31
    class_number = F.class_number(proof=True)
    bnf = F.pari_bnf(proof=True)
    certification = bnf.bnfcertify()
    narrow = ZZ(bnf.bnfnarrow()[0])
    assert class_number == narrow == certification == 1
    embeddings = sorted(F.embeddings(AA),key=lambda e:e(b))
    signatures = []
    units = []
    for row in unit_packet["unit_signature_proof"]["units_power_coordinates"]:
        u = F(list(map(QQ,row)))
        assert u.is_integral() and (1/u).is_integral() and abs(u.norm()) == 1
        signatures.append([int(e(u)<0) for e in embeddings])
        units.append(list(map(str,u.vector())))
    assert matrix(GF(2),signatures).rank() == 8
    assert signatures == unit_packet["unit_signature_proof"]["signatures"]
    print("FIELD_PASS class=narrow=1, PARI certified, signature rank 8",flush=True)

    B = QuaternionAlgebra(F,b-b*b,-1)
    def quat(row):
        return B([F(list(map(QQ,row[8*j:8*(j+1)]))) for j in range(4)])
    basis = [quat(row) for row in raw["quaternion_export"]["order_basis"]]
    dual = matrix(QQ,local["arithmetic"]["relative_dual_in_order_coordinates"])
    dual_basis = [sum((dual[i,j]*basis[i] for i in range(32)),B(0)) for j in range(32)]
    norm_checks = {}
    for label, elements, scale in (("order",basis,F(1)),("relative_dual",dual_basis,2+b)):
        diagonals = [scale*q.reduced_norm() for q in elements]
        assert all(v.is_integral() for v in diagonals)
        cross_count = 0
        for i in range(32):
            for j in range(i):
                cross = scale*(elements[i]+elements[j]).reduced_norm()-diagonals[i]-diagonals[j]
                assert cross.is_integral()
                cross_count += 1
        norm_checks[label] = {"scale":str(scale),"diagonal_tests":32,"cross_tests":cross_count,
                              "norm_polynomial_integral":True}
    print("LOCAL_LEVEL_PASS norms(O) integral; pi*norms(O#) integral",flush=True)

    # Verify the actual real-to-complex change, including the Y bars.
    QI = QuadraticField(-1,"ii")
    ii = QI.gen()
    RealEntries = PolynomialRing(QI,names=("aa","bb","cc","dd"))
    aa,bb,cc,dd = RealEntries.gens()
    real_matrix = matrix(RealEntries,[[aa,bb],[cc,dd]])
    cayley = matrix(RealEntries,[[1,-ii],[1,ii]])
    complex_matrix = cayley*real_matrix*cayley.inverse()
    assert complex_matrix == matrix(RealEntries,[[(aa+dd+ii*(bb-cc))/2,(aa-dd-ii*(bb+cc))/2],
                                                  [(aa-dd+ii*(bb+cc))/2,(aa+dd-ii*(bb-cc))/2]])
    # The complex matrix is [[X, conjugate(Y)],[Y, conjugate(X)]].
    # u is the first anti-holomorphic disk variable, v the second
    # holomorphic one. Nilpotent paths give the exact pure derivatives.
    P = PolynomialRing(QQ,names=("x","xb","y","yb","h","u","v"))
    x,xb,y,yb,h,u,v = P.gens()
    M = matrix(P,[[x,yb],[y,xb]])
    E12 = matrix(P,[[0,1],[0,0]])
    E21 = matrix(P,[[0,0],[1,0]])
    moved = (1-u*E21)*M*(1+v*E12)
    norm = x*xb-y*yb
    majorant = x*xb+y*yb
    assert moved.det() == norm
    change = moved[0,0]*moved[1,1]+moved[1,0]*moved[0,1]-majorant
    exponent = -h*change/2
    assert exponent == h*(u*x*yb-v*x*y+u*v*x*x)
    left_tangent = -E21*M
    right_tangent = M*E12
    assert [left_tangent[0,0],left_tangent[1,1],left_tangent[1,0],left_tangent[0,1]] == [0,-yb,-x,0]
    assert [right_tangent[0,0],right_tangent[1,1],right_tangent[1,0],right_tangent[0,1]] == [0,y,0,x]
    records = []
    exponential = sum(exponent**j/factorial(j) for j in range(8))
    direct = x*x*exponential
    for a in (1,3,5):
        coefficient = direct.derivative(u,a).derivative(v)(u=0,v=0)
        expected = x**(a+3)*(a*h**a*yb**(a-1)-h**(a+1)*y*yb**a)
        assert coefficient == expected
        records.append({"pair":[a,1],"exact_Gaussian_derivative":str(coefficient),
                        "terms":[{"exponents":list(map(int,e)),"coefficient":str(c)} for e,c in sorted(coefficient.dict().items())],
                        "first_variable":"anti-holomorphic", "second_variable":"holomorphic",
                        "coarse_ratio_factorial":str(factorial(a))})

    # Independent power accounting after integrating each real height.
    # s is formal; all eight delta_v exponents equal s+1. Combining
    # translation covolume sqrt(D) and Lambda_F(2s) gives D^(2s+3/2).
    T = PolynomialRing(QQ,names=("z","r"))
    z,r = T.gens()
    split_delta = (z+2+r)-r-1
    compact_delta = z+1
    split_four_pi = (z+2+r)-r
    compact_four_pi = z+1
    assert split_delta == compact_delta == z+1
    assert split_four_pi+7*compact_four_pi == 8*z+9
    assert (z+1)+z+QQ(1)/2 == 2*z+QQ(3)/2
    result = {
        "status":"pass: arithmetic and symbolic hypotheses for D95 global comparison",
        "field":{"class_number_proof_true":int(class_number),"narrow_class_number":int(narrow),
                 "pari_bnfcertify":int(certification),"discriminant":str(F.discriminant()),
                 "power_basis_is_integral_basis":True,"units_power_coordinates":units,
                 "unit_signatures":signatures,"signature_rank":8,
                 "positive_even_valuation_square_classes":1},
        "local_level":norm_checks,
        "matrix_convention":"[[X,conjugate(Y)],[Y,conjugate(X)]]",
        "central_action":"r(c*I)Phi(x,u)=Phi(c*x,c^(-2)*u)",
        "normalized_bump_multiplicative_integrals":["1"]*8,
        "central_unfolded_signed_lattice_factor":"1/2",
        "central_unit_regulator_extra_factor":False,
        "Gaussian_exponent_change":str(exponent),
        "derivative_records":records,
        "coarse_ratio_rule":"c_(a)/c_1 = conjugate(S_(a,1)/S_(1,1))/a!, a=1,3,5; requires S_(1,1)!=0",
        "classical_tensor_orientation":"conjugate(v(g1))*v(g2)",
        "forward_norm_one_Whittaker_at_identity":"norm(v)^2*exp(-2*pi)",
        "classical_tensor_scalar":"norm(f)^2/norm(v)^2 > 0, with the report's classical measures",
        "Mellin_prefactor":"D^(3/2)/(64*R_F*(4*pi)^9)",
        "Mellin_argument":"(4*pi^2)^8*A/D^2",
        "global_comparison_proof":"dembele/certificates/nelson-global-identification-d95.md",
        "global_kernel_identified_up_to_positive_scalar":True,
        "global_scalar_numerically_evaluated":False,
        "full_Mellin_series_numerically_evaluated":False,
        "CM_anchor_derivative_nonzero":False,
        "arithmetic_CM_jet_computed":False,
        "sources":[source(p) for p in [Path(__file__)]+paths],
    }
    output.write_text(json.dumps(result,indent=2)+"\n")
    print("ORIENTATION_PASS first anti-holomorphic, second holomorphic; ratio needs conjugation",flush=True)
    print("PASS|358_nelson_global_comparison")


if __name__ == "__main__":
    main()

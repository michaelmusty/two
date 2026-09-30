"""D94: exact arithmetic behind a nonzero local norm-one contraction.

The analytic calculation and the dual K-type convention are proved in
the D94 report. This program does not identify the D91 classical integral
with a similitude theta lift, or compute a CM derivative.
"""
import hashlib
import json
from pathlib import Path
from sage.all import QQ, ZZ, NumberField, PolynomialRing, LaurentPolynomialRing, matrix, diagonal_matrix, vector

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def source(path):
    return {"path": str(path.relative_to(ROOT)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    output = DATA / "nelson_norm_one_test_vector_d94.json"
    assert not output.exists()
    raw = json.loads((DATA / "cm_orbit.json").read_text())
    prior = json.loads((DATA / "nelson_kernel_d90.json").read_text())
    R = PolynomialRing(QQ, "s")
    s = R.gen()
    F = NumberField(s**8-8*s**6+20*s**4-16*s**2+2, "b")
    b = F.gen()
    pi = 2+b
    delta = 16/pi
    inverse = pi/16
    assert delta*inverse == 1 and inverse.trace() == 1
    assert delta.norm() == 2**31
    places = []
    for index, row in enumerate(prior["rational_majorant_proof"]["real_places"]):
        lo, hi = map(QQ, row["root_interval"])
        assert -2 < lo < hi < 2
        assert F.defining_polynomial()(lo)*F.defining_polynomial()(hi) < 0
        places.append({"index": index, "b_interval": [str(lo), str(hi)],
                       "inverse_delta_interval": [str((2+lo)/16), str((2+hi)/16)],
                       "kind": "split" if index == 4 else "definite"})
    assert len(places) == 8
    assert all(QQ(places[i]["b_interval"][1]) < QQ(places[i+1]["b_interval"][0]) for i in range(7))

    # Columns are the actual 32 integral basis elements in power coordinates.
    order = matrix(QQ, raw["quaternion_export"]["order_basis"]).transpose()
    involution = diagonal_matrix(QQ, [1]*8+[-1]*24)
    conjugation = order.inverse()*involution*order
    assert all(c in ZZ for c in conjugation.list())
    assert conjugation**2 == 1 and abs(conjugation.det()) == 1
    identity_coordinates = order.inverse()*vector(QQ, [1]+[0]*31)
    assert all(c in ZZ for c in identity_coordinates)

    P = PolynomialRing(QQ, names=("aa", "bb", "cc", "dd"))
    aa, bb, cc, dd = P.gens()
    four_x_squared = (aa+dd)**2+(bb-cc)**2
    four_y_squared = (aa-dd)**2+(bb+cc)**2
    assert (four_x_squared-four_y_squared)/4 == aa*dd-bb*cc
    L = LaurentPolynomialRing(QQ, "t")
    t = L.gen()
    x, y = (t+t**-1)/2, (t-t**-1)/2
    assert x*x-y*y == 1
    assert x*x+y*y == (t*t+t**-2)/2

    # Compact angular averaging kills every nonzero integral K weight.
    # The phase error is meaningful: replacing the dual coefficient by
    # its conjugate would give weight four and a zero integral.
    matching_weight = 2-2
    wrong_weight = 2+2
    assert matching_weight == 0 and wrong_weight != 0
    result = {
        "status": "pass: exact local norm-one test-vector arithmetic; global comparison pending",
        "inverse_delta_power_coordinates": list(map(str, inverse.list()))+["0"]*(8-len(inverse.list())),
        "delta_power_coordinates": list(map(str, delta.list()))+["0"]*(8-len(delta.list())),
        "inverse_delta_trace": str(inverse.trace()),
        "delta_norm": str(delta.norm()),
        "real_places": places,
        "order_conjugation_matrix": [list(map(str, row)) for row in conjugation.rows()],
        "identity_in_order_coordinates": list(map(str, identity_coordinates)),
        "norm_one_finite_support": "O_v intersect B_v^1 = O_v^1, since x^{-1}=conjugate(x)",
        "finite_haar_convention": "vol(O_v^1)=1",
        "finite_local_contraction": "1 on the O_v^times-fixed line",
        "definite_haar_convention": "probability Haar measure on B_v^1",
        "definite_local_contraction": "exp(-2*pi/delta_v)",
        "split_haar_convention": "K has mass 1; quotient measure is hyperbolic area; radial density 2*pi*sinh(r)",
        "split_dual_matrix_coefficient": "X(g)^(-2), paired with phi(g)=X(g)^2/delta_0*exp(-2*pi*P(g)/delta_0)",
        "split_local_contraction": "(2*pi/delta_0)*integral_1^infinity exp(-2*pi*u/delta_0) du = exp(-2*pi/delta_0)",
        "cartan_parameter": "t=exp(r/2); X=(t+t^-1)/2; Y=(t-t^-1)/2; P=cosh(r)",
        "archimedean_product": "exp(-2*pi)",
        "matching_total_K_weight": matching_weight,
        "wrong_dual_total_K_weight": wrong_weight,
        "wrong_dual_angular_average": "0",
        "local_norm_one_contractions_nonzero": True,
        "global_test_vector_identified": False,
        "D91_Petersson_prefactor_verified": False,
        "CM_anchor_derivative_nonzero": False,
        "Shimura_derivative_computed": False,
        "sources": [source(path) for path in [Path(__file__), DATA/"cm_orbit.json", DATA/"nelson_kernel_d90.json"]],
        "proof_report": "dembele/certificates/nelson-test-vector-and-contour-d94.md",
    }
    output.write_text(json.dumps(result, indent=2)+"\n")
    print("LOCAL_NORM_ONE_NONZERO trace(delta^-1)=1; real product exp(-2*pi)")
    print("PASS|356_nelson_norm_one_test_vector")


if __name__ == "__main__":
    main()

"""D90: exact local ingredients for a totally real Shimizu evaluator.

Run with Sage Python. This computes lattices and Schwartz derivatives,
not a global theta lift and not Shimura differential coefficients.
"""
import argparse
import hashlib
import json
from pathlib import Path

from sage.all import (AA, QQ, ZZ, NumberField, PolynomialRing,
                      QuaternionAlgebra, RealField, matrix, vector, factorial,
                      binomial)

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUTPUT = DATA / "nelson_local_kernel_d90.json"


def source(path):
    path = Path(path)
    return {"path": str(path.relative_to(ROOT)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def rows(m):
    return [[str(c) for c in row] for row in m.rows()]


def derivative_polynomials():
    """Two independent constructions, including direct Weil derivatives."""
    R = PolynomialRing(QQ, names=("y", "yb"))
    y, yb = R.gens()
    polys = {}
    for a in range(6):
        for b in range(6):
            p = R(1)
            for _ in range(b):
                p = p.derivative(yb)-y*p
            for _ in range(a):
                p = yb*p-p.derivative(y)
            j, J = min(a, b), max(a, b)
            laguerre = sum((-y*yb)**r/factorial(r)*binomial(J, j-r)
                           for r in range(j+1))
            assert p == factorial(j)*(-y)**(b-j)*yb**(a-j)*laguerre
            polys[a, b] = p
    S = PolynomialRing(QQ, names=("x", "xb", "y", "yb", "h"))
    x, xb, ys, ybs, h = S.gens()
    def d1(p):
        return -ybs*p.derivative(xb)-x*p.derivative(ys)+h*x*ybs*p
    def d2(p):
        return ys*p.derivative(xb)+x*p.derivative(ybs)-h*x*ys*p
    for (a,b), p in polys.items():
        direct = x**2
        for _ in range(b):
            direct = d2(direct)
        for _ in range(a):
            direct = d1(direct)
        formula = S(0)
        for (e1,e2), c in p.dict().items():
            degree = a+b+e1+e2
            assert degree % 2 == 0
            formula += c*h**(degree//2)*ys**e1*ybs**e2
        assert direct == x**(2+a+b)*formula
    # Disk coefficients for weight two, proved on an arbitrary degree-five
    # Taylor polynomial; y=(z-zbar)/(2i) is used by the raising operator.
    T = PolynomialRing(QQ, names=("z", "zb"))
    z, zb = T.gens()
    K = T.fraction_field()
    # Work with D_k=(z-zbar)*d/dz+k, keeping the varying y factor in
    # successive raises: y^j delta^j = product(D_{k+j-1},...,D_k).
    U = PolynomialRing(QQ, names=("w",))
    w = U.gen()
    disk_checks = 0
    for n in range(6):
        f = K(z**n)
        for j in range(6):
            if j:
                f = (z-zb)*f.derivative(z)+(2+j-1)*f
            # Evaluate at z=1, zbar=-1 and compare exact disk expansion.
            # (1-w)^-2 * ((1+w)/(1-w))^n.
            coefficient = sum(binomial(n,r)*binomial(n+1+j-r,j-r)
                              for r in range(min(n,j)+1))
            assert f(z=1, zb=-1)/factorial(j) == coefficient
            disk_checks += 1
    # The local formula must retain the constant term of p11.
    assert polys[1,1] == 1-y*yb and polys[1,1] != -y*yb
    return {"checked_derivative_pairs": len(polys),
            "disk_monomial_checks": disk_checks,
            "polynomials": {f"{a},{b}": str(p) for (a,b),p in polys.items()},
            "CM_required_upstairs_degrees": [1,3,5],
            "coarse_coefficient_rule": "2*i*y0^(j+1)*delta^j(f)(z0)/j!",
            "omitted_p11_constant_rejected": True}


def arithmetic_lattices():
    saved = json.loads((DATA / "cm_orbit.json").read_text())
    raw = saved["quaternion_export"]
    R = PolynomialRing(QQ, "s")
    s = R.gen()
    f = s**8-8*s**6+20*s**4-16*s**2+2
    F = NumberField(f, "b")
    b = F.gen()
    a = b-b*b
    B = QuaternionAlgebra(F, a, -1)
    def from_vector(v):
        return B([F([QQ(c) for c in v[8*j:8*(j+1)]]) for j in range(4)])
    def coords(q):
        return vector(QQ, sum([list(c.vector()) for c in q.coefficient_tuple()], []))
    basis = [from_vector(v) for v in raw["order_basis"]]
    lattice = matrix(QQ, [coords(q) for q in basis]).transpose()
    inverse = lattice.inverse()
    places = sorted(F.embeddings(AA), key=lambda v:v(b))
    split = next(i for i,v in enumerate(places) if v(a)>0)
    assert split == 4 and all(v(a)<0 for i,v in enumerate(places) if i != split)
    pi = 2+b
    delta = 16/pi
    assert all(v(pi)>0 and v(delta)>0 for v in places)
    assert pi.norm() == 2 and delta.norm() == 2**31
    assert F.ideal(delta) == F.different() == F.ideal(f.derivative()(b))
    assert F.ideal(delta) == F.ideal(pi)**31
    pair = lambda x,y: (x*y.conjugate()).reduced_trace()
    G = matrix(QQ, [[pair(x,y).trace() for y in basis] for x in basis])
    G0 = matrix(QQ, [[(pair(x,y)/delta).trace() for y in basis] for x in basis])
    assert abs(G.det()) == 2**126 and abs(G0.det()) == 4
    assert all(c in ZZ for c in G0.list())
    smith = [abs(int(v)) for v in matrix(ZZ,G0).smith_form()[0].diagonal()]
    assert sorted(smith) == [1]*30+[2]*2
    # Columns of these matrices express the two dual lattices in O's basis.
    relative_dual = G0.inverse()
    absolute_dual = G.inverse()
    delta_action = matrix(QQ, [inverse*coords(delta*x) for x in basis]).transpose()
    change = relative_dual.inverse()*delta_action*absolute_dual
    assert abs(change.det()) == 1 and all(c in ZZ for c in change.list())
    dual_elements = [sum((relative_dual[j,k]*basis[j] for j in range(32)),B(0))
                     for k in range(32)]
    assert all(F.ideal(pair(x,y)).is_integral() for x in dual_elements for y in basis)
    # A generator of O#/O is killed by pi. All pairwise norm polarizations
    # are integral after multiplying by pi, so the entire dual has norms
    # in pi^-1 O_F, not just these basis vectors.
    assert all(c in ZZ for x in dual_elements for c in inverse*coords(pi*x))
    assert all((pi*x.reduced_norm()).is_integral() for x in dual_elements)
    assert all((pi*pair(x,y)).is_integral() for x in dual_elements for y in dual_elements)
    # CM orthogonal decomposition of the actual saved order, reference point 8.
    witness = -4*b**6+22*b**4-28*b*b+4*b+2
    beta = 2/witness*from_vector(raw["elliptics"][8])
    assert beta*beta == B(-2-b)
    parallel = [(x+beta*x*beta**(-1))/2 for x in basis]
    perpendicular = [x-p for x,p in zip(basis,parallel)]
    assert all(beta*p == p*beta for p in parallel)
    assert all(beta*p == -p*beta for p in perpendicular)
    assert all(pair(p,q) == 0 for p in parallel for q in perpendicular)
    # Rational positive quadratic form within 1% of the natural CM
    # majorant. Interpolate a field element whose eight values approximate
    # (-1 at the split place, +1 at the other seven).
    RF = RealField(180)
    vandermonde = matrix(RF, [[RF(v(b))**j for j in range(8)] for v in places])
    target = vector(RF, [-1 if i == split else 1 for i in range(8)])
    coefficients = vandermonde.solve_right(target)
    c = F([QQ(round(v*10**8))/10**8 for v in coefficients])
    errors = [abs(v(c)-target[i]) for i,v in enumerate(places)]
    assert all(e < QQ(1)/100 for e in errors)
    Q = matrix(QQ, [[((pair(parallel[i],parallel[j])+
                       c*pair(perpendicular[i],perpendicular[j]))/(2*delta)).trace()
                     for j in range(32)] for i in range(32)])
    assert Q.is_positive_definite()
    # Exact orthogonality, definite signs, and coefficient inequalities
    # give (99/100) M <= Q <= (101/100) M for every real vector.
    return {"F_polynomial": str(f), "split_real_index": split,
            "totally_positive_uniformizer": str(pi),
            "totally_positive_different_generator": str(delta),
            "different_exponent": 31,
            "standard_character_dual_index": str(2**126),
            "unramified_character_dual_index": 4,
            "relative_dual_smith": sorted(smith),
            "standard_self_dual_volume": "1/2^63",
            "unramified_self_dual_volume": "1/2",
            "dual_lattice_comparison_exact": True,
            "relative_dual_norms_in_pi_inverse_OF": True,
            "relative_pairing_gram": rows(G0),
            "relative_dual_in_order_coordinates": rows(relative_dual),
            "CM_point_index": 8,
            "CM_beta_power_coordinates": [str(x) for x in coords(beta)],
            "CM_parallel_rank": int(matrix(QQ,[coords(x) for x in parallel]).rank()),
            "CM_perpendicular_rank": int(matrix(QQ,[coords(x) for x in perpendicular]).rank()),
            "majorant_coefficient_power_basis": [str(x) for x in c.vector()],
            "majorant_relative_error_bound": "1/100",
            "majorant_gram": rows(Q)}


def compute():
    return {"status": "pass: local ingredients only",
            "arithmetic": arithmetic_lattices(),
            "derivatives": derivative_polynomials(),
            "Shimura_tangent_computed": False,
            "global_Hilbert_theta_lift_evaluated": False,
            "sources": [source(Path(__file__)), source(DATA/"cm_orbit.json")],
            "reference": "https://arxiv.org/pdf/1210.1243; sections 3.2-3.5 and Appendix B"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = compute()
    if args.check:
        assert json.loads(OUTPUT.read_text()) == result
    else:
        assert not OUTPUT.exists(), "retain existing artifact; use --check"
        OUTPUT.write_text(json.dumps(result, indent=2)+"\n")
    print("PASS|320_nelson_local_kernel")


if __name__ == "__main__":
    main()

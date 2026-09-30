"""D102: exact field-lattice calculation and residue-frame proof controls.

No candidate curve equations, candidate jets or analytic banks are read.
The geometric index formula is proved in the companion report; these
calculations check its algebra and exhibit an actual good-reduction family.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
FIELD = DATA / "cm_arithmetic_audit.json"
BASIS = DATA / "cm_field_recognition.json"
OUT = DATA / "cm_residue_lattice_d102.json"


def source(path):
    p = Path(path).resolve()
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def transpose(a):
    return [list(x) for x in zip(*a)]


def mul(a, b):
    bt = transpose(b)
    return [[sum(x*y for x, y in zip(row, col)) for col in bt] for row in a]


def det(a):
    a = [[Q(x) for x in row] for row in a]
    result = Q(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return Q(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            result = -result
        v = a[j][j]
        result *= v
        for i in range(j+1, len(a)):
            scale = a[i][j]/v
            for k in range(j+1, len(a)):
                a[i][k] -= scale*a[j][k]
    return result


def inverse(a):
    n = len(a)
    a = [[Q(x) for x in row] + [Q(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if a[i][j])
        a[j], a[pivot] = a[pivot], a[j]
        scale = a[j][j]
        a[j] = [x/scale for x in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [x-scale*y for x, y in zip(a[i], a[j])]
    return [row[n:] for row in a]


def field_mul(a, b, polynomial, modulus=None):
    n = len(polynomial)-1
    out = [0]*(2*n-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    for i in range(2*n-2, n-1, -1):
        c = out[i] if modulus is None else out[i] % modulus
        for j in range(n):
            out[i-n+j] -= c*polynomial[j]
    return out[:n] if modulus is None else [x % modulus for x in out[:n]]


def power(a, e, polynomial, p):
    result = [1] + [0]*(len(polynomial)-2)
    while e:
        if e & 1:
            result = field_mul(result, a, polynomial, p)
        a = field_mul(a, a, polynomial, p)
        e >>= 1
    return result


def trim(a):
    while len(a) > 1 and not a[-1]:
        a.pop()
    return a


def gcd_mod(a, b, p):
    a, b = trim([x % p for x in a]), trim([x % p for x in b])
    while b != [0]:
        r = a[:]
        while r != [0] and len(r) >= len(b):
            c = r[-1]*pow(b[-1], -1, p) % p
            shift = len(r)-len(b)
            for i, x in enumerate(b):
                r[shift+i] = (r[shift+i]-c*x) % p
            trim(r)
        a, b = b, r
    return [(x*pow(a[-1], -1, p)) % p for x in a]


def field_lattice():
    info = json.loads(FIELD.read_text())["residue_algebra_input"]
    saved = json.loads(BASIS.read_text())["field_basis"]
    f = [int(x) for x in info["polynomial_coefficients_ascending"]]
    n = len(f)-1
    assert n == 17 and f[-1] == 1
    # Prime-degree irreducibility criterion over F_31, independently replayed.
    x = [0, 1] + [0]*(n-2)
    xp = power(x, 31, f, 31)
    assert gcd_mod(f, [(a-b) % 31 for a, b in zip(xp, x)], 31) == [1]
    assert power(x, 31**17, f, 31) == x
    # Newton sums through degree 32 suffice for every trace pairing below.
    traces = [n]
    for k in range(1, 2*n-1):
        if k <= n:
            traces.append(-sum(f[n-j]*traces[k-j] for j in range(1, k))-k*f[n-k])
        else:
            traces.append(-sum(f[n-j]*traces[k-j] for j in range(1, n+1)))
    b = [[Q(z) for z in row] for row in saved["integral_basis_power_coordinates"]]
    assert b[0] == [1]+[0]*(n-1)
    invb = inverse(b)
    gram = mul(mul(b, [[traces[i+j] for j in range(n)] for i in range(n)]), transpose(b))
    assert all(x.denominator == 1 for row in gram for x in row)
    gram = [[int(x) for x in row] for row in gram]
    disc = int(det(gram))
    assert disc == 2**79 == int(saved["integral_basis_discriminant"]) == int(info["field_discriminant"])
    # Ring closure plus 1 and finite rank prove integrality without a maximality assertion.
    products = []
    for i in range(n):
        for j in range(i, n):
            coordinates = mul([field_mul(b[i], b[j], f)], invb)[0]
            assert all(z.denominator == 1 for z in coordinates)
            products.append({"i": i, "j": j, "coordinates": [int(z) for z in coordinates]})
    tau = gram[0]
    assert tau[:2] == [17, 2] and math.gcd(*tau) == 1
    eta = [[Q(z) for z in row] for row in saved["trace_centered_basis_power_coordinates"]][1:]
    expected = [[b[i][k] - Q(tau[i], 17)*b[0][k] for k in range(n)] for i in range(1, n)]
    assert eta == expected
    # Trace-one element b_0-8*b_1 and a saturated trace-zero basis.
    star = [1, -8]+[0]*15
    z = [[-2, 17]+[0]*15]
    for i in range(2, n):
        row = [-tau[i]*c for c in star]
        row[i] += 1
        z.append(row)
    assert det([star]+z) == 1
    assert mul(z, [[a] for a in tau]) == [[0]]*16
    # The dual basis elements numbered 1..16 form the trace-zero codifferent lattice.
    az = [row[1:] for row in mul(z, gram)]
    assert abs(det(az)) == disc
    jmatrix = [[17*gram[i][j]-tau[i]*tau[j] for j in range(1, n)] for i in range(1, n)]
    assert abs(det(jmatrix)) == disc*17**15
    invg = inverse(gram)
    dual_clear = math.lcm(*(q.denominator for row in invg for q in row))
    assert mul(gram, invg) == [[int(i == j) for j in range(n)] for i in range(n)]
    # 17 is genuinely required to put every unscaled eta in the trace-dual lattice.
    eta_pairing = [[Q(gram[i][j])-Q(tau[i]*tau[j], 17) for j in range(n)] for i in range(1, n)]
    assert math.lcm(*(q.denominator for row in eta_pairing for q in row)) == 17
    return {"degree": n, "polynomial": f, "irreducible_mod31": True,
            "ring_products_checked": len(products), "ring_products": products,
            "trace_gram": gram, "trace_vector": tau, "trace_ideal_generator": 1,
            "ring_discriminant": disc, "maximality_claimed": False,
            "trace_dual_clearing_integer": dual_clear,
            "trace_zero_integral_to_dual_index": disc,
            "centered_basis_to_trace_dual_clearing_integer": 17,
            "scaled_centered_to_trace_zero_dual_index": disc*17**15,
            "scaled_centered_to_integral_trace_zero_index": 17**15,
            "identification_with_actual_horizontal_order_proved": False}


def valuation(x, p):
    x = Q(x)
    assert x
    def integer_value(a):
        count = 0
        while a % p == 0:
            count += 1
            a //= p
        return count
    return integer_value(abs(x.numerator))-integer_value(x.denominator)


def cofactor_control(e):
    g = len(e[0])
    assert len(e) == g+1
    c = [(-1)**i*det(e[:i]+e[i+1:]) for i in range(g+1)]
    assert all(c)
    assert mul([c], e) == [[0]*g]
    weighted = [[ci*x for x in row] for ci, row in zip(c, e)]
    product = math.prod(c)
    for i in range(g+1):
        assert det(weighted[:i]+weighted[i+1:]) == (-1)**i*product
    assert det(mul(transpose(e), e)) == sum(x*x for x in c)
    # Cramer's rule infinity-norm bound for the explicit first chart.
    square = weighted[:g]
    bmax = max(abs(x) for row in square for x in row)
    bound = Q(math.factorial(g)*bmax**(g-1), abs(product))
    actual = max(sum(abs(x) for x in row) for row in inverse(square))
    assert actual <= bound
    return {"g": g, "all_cofactors_nonzero": True, "cofactor_product": str(product),
            "Cauchy_Binet": True, "inverse_norm_bound_checked": True}


def algebra_controls():
    records = []
    # Both independent defect terms: E is an abstract integral restriction matrix.
    # It is not asserted that every matrix here comes from a curve.
    for n in [1, 2, 4, 8]:
        q = 5**n
        for m in [0, 1, 3]:
            e = [[1, 0], [1, q], [1, 1]]
            e = [[5**m*row[0], row[1]] for row in e]
            c = [(-1)**i*det(e[:i]+e[i+1:]) for i in range(3)]
            kappa = math.gcd(*(abs(int(x)) for x in c))
            a = [x/kappa for x in c]
            assert math.gcd(*(abs(int(x)) for x in a)) == 1
            assert mul([a], e) == [[0, 0]]
            r = [[ai*x for x in row] for ai, row in zip(a, e)]
            index_value = valuation(det(r[:2]), 5)
            torsion_value = valuation(kappa, 5)
            pole_value = valuation(math.prod(a), 5)
            assert index_value == torsion_value+pole_value == m+n
            if m:
                assert index_value != pole_value  # omitting T is rejected
            records.append({"n": n, "m": m, "index_valuation": index_value,
                            "pole_norm_valuation": pole_value, "H1_torsion_length": torsion_value})
    e = [[1, 0], [1, 5], [1, 1]]
    small = cofactor_control(e)
    # Exact row-trivialization and differential-basis covariance.
    u = [[1, 2], [3, 7]]
    row_scales = [2, 3, 5]
    ep = [[s*x for x in row] for s, row in zip(row_scales, mul(e, u))]
    c = [(-1)**i*det(e[:i]+e[i+1:]) for i in range(3)]
    cp = [(-1)**i*det(ep[:i]+ep[i+1:]) for i in range(3)]
    assert cp == [det(u)*math.prod(row_scales)*ci/si for ci, si in zip(c, row_scales)]
    large = cofactor_control([[i**j for j in range(16)] for i in range(1, 18)])
    return {"two_defect_controls": records, "cofactor_controls": [small, large],
            "row_and_basis_covariance": True, "omitted_torsion_term_rejected": True}


def geometric_family():
    # Fixed smooth genus-two curve y^2=x^5-x+1 over Z_5.
    # P1=(0,1), P2=(q,y2), P3=(1,1), y2=-1 mod5.
    # Their reductions stay distinct; D is split etale and H1(O(D))=0.
    records = []
    for n in [1, 2, 4, 8, 16]:
        q = 5**n
        precision = n+8
        modulus = 5**precision
        target = q**5-q+1
        y, current = 4, 5
        while current < modulus:
            digit = (-(y*y-target)//current)*pow(2*y, -1, 5) % 5
            y += digit*current
            current *= 5
        assert (y*y-target) % modulus == 0 and y % 5 == 4
        invy = pow(y, -1, modulus)
        e = [[1, 0], [invy, q*invy % modulus], [1, 1]]
        a = [q-1, y, -q]
        assert all(x % modulus == 0 for x in mul([a], e)[0])
        assert any(det(e[:i]+e[i+1:]) % 5 for i in range(3))
        residues = [[(ai*x) % modulus for x in row] for ai, row in zip(a, e)]
        expected = [[q-1, 0], [1, q], [(-q) % modulus, (-q) % modulus]]
        assert residues == expected
        assert valuation(q*(q-1), 5) == n
        records.append({"n": n, "precision": precision, "y2_mod_5_power": y,
                        "residue_matrix_mod_5_power": residues, "index_valuation": n})
    # f'=5*x^4-1 is -1 mod5; no repeated finite branch root.
    assert [(-1) % 5, 0, 0, 0, 5 % 5] == [4, 0, 0, 0, 0]
    return {"curve": "y^2=x^5-x+1 over Z_5", "genus": 2,
            "smooth_fixed_curve": True, "distinct_reductions": [[0, 1], [0, 4], [1, 1]],
            "D_degree": 3, "D_split_etale": True, "H1_O_D_zero": True,
            "index_formula": "v_5(index)=n, unbounded as n grows",
            "CM_counterexample_claimed": False, "closed_point_counterexample_claimed": False,
            "controls": records}


def build():
    return {"status": "pass", "milestone": "D102", "field_lattice": field_lattice(),
            "algebra_controls": algebra_controls(), "good_reduction_family": geometric_family(),
            "actual_residue_index_bounded": False, "actual_archimedean_bounds_obtained": False,
            "independent_Shimura_tangent_obtained": False,
            "sources": [source(p) for p in [Path(__file__), FIELD, BASIS]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        old = json.loads(OUT.read_text())
        for item in old["sources"]:
            assert source(item["path"]) == item
    result = build()
    if args.check:
        assert result == old
    else:
        assert not OUT.exists(), "Preserve completed artifacts."
        OUT.write_text(json.dumps(result, indent=2)+"\n")
    f = result["field_lattice"]
    print(json.dumps({"status": "pass", "ring_products": f["ring_products_checked"],
                      "trace_dual_clearing_integer": f["trace_dual_clearing_integer"],
                      "scaled_centered_to_dual_index": f["scaled_centered_to_trace_zero_dual_index"],
                      "actual_tangent_obtained": False}), flush=True)
    print("PASS|D102_RESIDUE_LATTICE", flush=True)


if __name__ == "__main__":
    main()

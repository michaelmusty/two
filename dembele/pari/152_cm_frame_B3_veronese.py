"""D76: split the recognized six-space by exact rational linear algebra.

The cubic singular on a Veronese surface has a rank-three polar at a
rational point. A tangent two-jet gives a rational point on its quotient
conic. Split that conic and recover three forms A,B,C with A*C=B^2.
Every step below is an exact identity, not a finite-precision inference.
"""
import ast
import importlib.util
from itertools import combinations_with_replacement
import json
from pathlib import Path
import re
import time

from sage.all import QQ, ZZ, PolynomialRing, matrix, vector, gcd, lcm

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


checks = module("veronese_checks", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")


def field(output, label):
    raw = re.search(r"^"+label+r"\|(.*?)(?=^[A-Z][A-Z_0-9]*\||\Z)",
                    output, re.M | re.S).group(1).strip()
    return ast.literal_eval(re.sub(r"(-?\d+/\d+)", r"'\1'", raw))


def primitive(row):
    ds = lcm([x.denominator() for x in row])
    vals = [ZZ(ds*x) for x in row]
    c = gcd(vals)
    first = next(x for x in vals if x)
    if first < 0:
        c = -c
    return vector(QQ, [x/c for x in vals])


def main():
    started = time.monotonic()
    job_path = DATA / "cm_frame_B3_exact_product_relations_job.json"
    checks.read_job(job_path, "PASS|151_CM_FRAME_B3_EXACT_PRODUCT_RELATIONS")
    output = (DATA / "cm_frame_B3_exact_product_relations.out").read_text()
    relations = matrix(QQ, [[QQ(x) for x in row] for row in field(output, "QUADRIC_RELATION_ROWS")])
    p = primitive(vector(QQ, [QQ(x) for x in field(output, "SURFACE_POINT")]))
    R = PolynomialRing(QQ, names=[f"y{i}" for i in range(6)])
    ys = list(R.gens())
    pairs = list(combinations_with_replacement(range(6), 2))
    mons2 = [ys[i]*ys[j] for i, j in pairs]
    mons3 = [ys[i]*ys[j]*ys[k] for i, j, k in combinations_with_replacement(range(6), 3)]
    quadrics = [sum(c*m for c, m in zip(row, mons2)) for row in relations]
    assert all(f(*p) == 0 for f in quadrics)
    annihilator = relations.right_kernel_matrix().transpose()

    def coefficients(f):
        return vector(QQ, [f.monomial_coefficient(m) for m in mons2])

    def in_relations(f):
        return coefficients(f)*annihilator == 0

    constraints = matrix(QQ, [sum((list(coefficients(m.derivative(y))*annihilator)
                                   for y in ys), []) for m in mons3])
    cubic_kernel = constraints.left_kernel_matrix()
    assert cubic_kernel.nrows() == 1
    cubic = sum(c*m for c, m in zip(primitive(cubic_kernel[0]), mons3))
    assert all(in_relations(cubic.derivative(y)) for y in ys)
    polar = sum(p[i]*cubic.derivative(ys[i]) for i in range(6))
    assert in_relations(polar)
    S = matrix(QQ, 6, 6)
    for c, (i, j) in zip(coefficients(polar), pairs):
        S[i, j] = S[j, i] = c if i == j else c/2
    assert S.rank() == 3
    B = S.row_space().basis_matrix()
    pivots = B.pivots()
    S3 = S.matrix_from_rows_and_columns(pivots, pivots)
    assert B.transpose()*S3*B == S and S3.det() != 0
    J = matrix(QQ, [[f.derivative(y)(*p) for y in ys] for f in quadrics])
    assert J.rank() == 3
    tangent = J.right_kernel_matrix()
    found = False
    for v in tangent:
        if matrix(QQ, [p, v]).rank() < 2:
            continue
        assert B*v == 0
        w = J.solve_right(-vector(QQ, [f(*v) for f in quadrics]))
        u = B*w
        if u and u*S3*u == 0:
            found = True
            break
    assert found
    assert all((J*w)[i]+quadrics[i](*v) == 0 for i in range(6))
    w_conic = next(vector(QQ, [int(i == j) for i in range(3)]) for j in range(3)
                   if (u*S3)[j])
    kappa = u*S3*w_conic
    w_conic -= (w_conic*S3*w_conic)/(2*kappa)*u
    assert w_conic*S3*w_conic == 0 and u*S3*w_conic == kappa
    z = matrix(QQ, [u*S3, w_conic*S3]).right_kernel_matrix()[0]
    eta = z*S3*z
    assert eta != 0
    basis = matrix(QQ, [u, z, w_conic]).transpose()
    abc = basis.inverse()*B
    A = sum(c*y for c, y in zip(abc[0], ys))
    Bform = sum(c*y for c, y in zip(abc[1], ys))
    C = -2*kappa/eta*sum(c*y for c, y in zip(abc[2], ys))
    assert in_relations(A*C-Bform**2)

    # Extend the three conic forms to the complete rank-one symmetric matrix.
    # D*C=E*B, D*B=E*A; choose the third independent solution beyond (A,B),(B,C).
    cross = matrix(QQ, [list(coefficients(y*C)*annihilator)
                        +list(coefficients(y*Bform)*annihilator) for y in ys]
                       +[list(coefficients(-y*Bform)*annihilator)
                         +list(coefficients(-y*A)*annihilator) for y in ys])
    syzygies = cross.left_kernel_matrix()
    assert syzygies.nrows() == 3
    def linear_row(f):
        return vector(QQ, [f.monomial_coefficient(y) for y in ys])
    span = matrix(QQ, [list(linear_row(A))+list(linear_row(Bform)),
                       list(linear_row(Bform))+list(linear_row(C))])
    de = next(v for v in syzygies if span.stack(matrix(QQ, [v])).rank() == 3)
    D = sum(c*y for c, y in zip(de[:6], ys))
    E = sum(c*y for c, y in zip(de[6:], ys))
    multC = matrix(QQ, [coefficients(y*C)*annihilator for y in ys])
    Frow = multC.solve_left(coefficients(E**2)*annihilator)
    F = sum(c*y for c, y in zip(Frow, ys))
    standard = [F, D, E, A, Bform, C]
    transform = matrix(QQ, [linear_row(f) for f in standard])
    assert transform.det() != 0
    exact_relations = [F*A-D**2, F*Bform-D*E, F*C-E**2,
                       D*Bform-E*A, D*C-E*Bform, A*C-Bform**2]
    assert all(in_relations(f) for f in exact_relations)
    assert matrix(QQ, [coefficients(f) for f in exact_relations]).rank() == 6
    print("EXACT_SPLIT_VERONESE", "RANK", transform.rank(), flush=True)

    rec_path = DATA / "cm_frame_B3_space_recognition.json"
    recognized = json.loads(rec_path.read_text())
    ds = matrix(QQ, recognized["denominator_space"]["selected_quadric_rows"])
    rows = transform*ds
    report = {"status": "pass", "milestone": "D76", "date": "2026-09-18",
              "sources": [checks.source(p) for p in (__file__, job_path, rec_path,
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py")],
              "relation_rows": [[str(x) for x in r] for r in relations],
              "surface_point": [str(x) for x in p],
              "secant_cubic": str(cubic), "polar_rank": 3,
              "tangent_vector": [str(x) for x in v],
              "second_jet": [str(x) for x in w], "conic_point": [str(x) for x in u],
              "veronese_transformation": [[str(x) for x in r] for r in transform],
              "veronese_section_rows": [[str(x) for x in r] for r in rows],
              "ordering": ["F", "D", "E", "A", "B", "C"],
              "exact_split_veronese": True, "number_field_cover_certified": False,
              "wall_seconds": time.monotonic()-started}
    (DATA / "cm_frame_B3_veronese.json").write_text(json.dumps(report, indent=2)+"\n")
    (DATA / "cm_frame_B3_veronese.m").write_text("// D76 exact rational Veronese section rows, order F,D,E,A,B,C.\n"
        +"veronese_transform := "+str([list(r) for r in transform])+";\n"
        +"veronese_section_rows := "+str([list(r) for r in rows])+";\n")
    print("PASS|152_CM_FRAME_B3_VERONESE", round(report["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

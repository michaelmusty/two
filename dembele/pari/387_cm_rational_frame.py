"""D106 finite checks for CM-marked rigidity and rational-frame jet heights.

The geometric specialization and descent arguments are in the companion report.
This program proves finite graph/group facts and tests differential identities;
it does not evaluate any section on the actual Shimura curve.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUT = DATA / "cm_rational_frame_d106.json"


def source(path):
    p = Path(path).resolve()
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def graph_group(vertices, edges):
    adj = {v: set() for v in vertices}
    for u, v in edges:
        assert u != v and v not in adj[u]
        adj[u].add(v)
        adj[v].add(u)
    # Equal OPEN neighborhoods are an intrinsic equivalence relation.
    fibers = {}
    for v in vertices:
        fibers.setdefault(tuple(sorted(adj[v])), []).append(v)
    blocks = sorted(fibers.values())
    n = len(blocks)
    qadj = [set(j for j in range(n) if blocks[j][0] in adj[b[0]]) for b in blocks]
    for i, b in enumerate(blocks):
        assert not any(v in adj[u] for u in b for v in b)
        for j, c in enumerate(blocks):
            assert all((v in adj[u]) == (j in qadj[i]) for u in b for v in c)
    colors = [len(b) for b in blocks]
    while True:
        signatures = [(colors[i], tuple(sorted(colors[j] for j in qadj[i]))) for i in range(n)]
        vocabulary = {s: k for k, s in enumerate(sorted(set(signatures)))}
        new = [vocabulary[s] for s in signatures]
        # Refinement cannot merge colors; equal cardinalities mean stabilization.
        if len(set(new)) == len(set(colors)):
            colors = new
            break
        colors = new
    answer = []
    visited = 0

    def extend(mapping, used):
        nonlocal visited
        visited += 1
        if len(mapping) == n:
            answer.append(tuple(mapping[i] for i in range(n)))
            return
        choices = []
        for i in range(n):
            if i in mapping:
                continue
            candidates = [j for j in range(n) if j not in used and colors[i] == colors[j]
                          and all((k in qadj[i]) == (v in qadj[j]) for k, v in mapping.items())]
            choices.append((len(candidates), i, candidates))
        _, i, candidates = min(choices)
        for j in candidates:
            extend(mapping | {i: j}, used | {j})

    extend({}, set())
    lifted = set()
    for p in answer:
        for images in product(*(list(permutations(blocks[p[i]])) for i in range(n))):
            mapping = {u: v for b, image in zip(blocks, images) for u, v in zip(b, image)}
            lifted.add(tuple(mapping[v] for v in vertices))
    return blocks, answer, lifted, visited


def graph_checks():
    saved = json.loads((DATA / "hyperellipticity_graph_review_d99.json").read_text())
    vertices = saved["stable_vertices"]
    edges = [(u, v) for u, v, _ in saved["stable_edges"]]
    assert len(vertices) == 30 and len(edges) == 45
    assert all(sum(v in e for e in edges) == 3 for v in vertices)
    blocks, quotient, group, visited = graph_group(vertices, edges)
    assert len(quotient) == 4 and len(group) == 64
    assert group == set(map(tuple, saved["automorphisms"]))
    weights = {tuple(sorted((u, v))): Q(w) for u, v, w in saved["stable_edges"]}
    position = {v: i for i, v in enumerate(vertices)}
    for p in group:
        for u, v in edges:
            assert weights[tuple(sorted((p[position[u]], p[position[v]])))] == weights[u, v]
        for q in group:
            assert tuple(p[position[v]] for v in q) in group
    # A cubic graph alone does not imply a 2-group: K4 has order 24.
    _, _, control, _ = graph_group(list(range(4)), [(i, j) for i in range(4) for j in range(i+1, 4)])
    assert len(control) == 24
    return {"algorithm": "collapse identical open neighborhoods, refine colors, exhaust adjacency-preserving quotient bijections, lift every fiber bijection",
            "twin_blocks": [b for b in blocks if len(b) > 1],
            "quotient_vertices": len(blocks), "quotient_automorphisms": len(quotient),
            "search_nodes": visited, "full_unweighted_automorphism_order": len(group),
            "agrees_with_independent_D99_enumeration": True,
            "all_automorphisms_preserve_lengths": True, "group_closure_checked": True,
            "cubic_K4_control_order": len(control)}


def affine_checks():
    n = 17
    group = [(a, b) for a in range(1, n) for b in range(n)]
    def mul(g, h):
        a, b = g
        c, d = h
        return (a*c % n, (a*d+b) % n)
    def inv(g):
        a, b = g
        ai = pow(a, -1, n)
        return (ai, -ai*b % n)
    stabilizers = [set(g for g in group if (g[0]*x+g[1]) % n == x) for x in range(n)]
    assert len(group) == 272 and all(len(s) == 16 for s in stabilizers)
    assert set.intersection(*stabilizers) == {(1, 0)}
    normalizer_sizes = []
    for x, s in enumerate(stabilizers):
        fixed = [y for y in range(n) if all((a*y+b) % n == y for a, b in s)]
        assert fixed == [x]
        normalizer = set(g for g in group if {mul(mul(g, h), inv(g)) for h in s} == s)
        assert normalizer == s
        normalizer_sizes.append(len(normalizer))
    conjugates = {frozenset(mul(mul(g, h), inv(g)) for h in stabilizers[0]) for g in group}
    assert conjugates == set(map(frozenset, stabilizers))
    # Nonempty fixed points need not be ALL points without Galois normalization.
    swap = [1, 0] + list(range(2, 17))
    cycle = [(x+1) % 17 for x in range(17)]
    conjugate = [cycle[swap[(x-1) % 17]] for x in range(17)]
    assert conjugate not in [list(range(17)), swap]
    return {"affine_group_order": len(group), "point_stabilizer_orders": [16]*17,
            "point_stabilizers_are_self_normalizing": True,
            "point_stabilizer_core_is_trivial": True, "conjugate_stabilizers": len(conjugates),
            "each_stabilizer_has_one_common_fixed_point": True,
            "odd_orbit_argument_requires_Galois_normalization_control": True,
            "degree_17_residue_field_Q_automorphism_order_via_group_correspondence": 1}


def formal_jet_checks():
    p = load_module("d101_polynomial_controls", ROOT / "dembele/pari/376_cm_tangent_exactness.py")
    add, mul, diff, comp = p.padd, p.pmul, p.pdiff, p.compose
    def scale(a, c):
        return [c*x for x in a]
    def power(a, n):
        out = [1]
        for _ in range(n):
            out = mul(out, a)
        return out
    def sections(f, a, b):
        G, H = p.bracket(f, a), p.bracket(f, b)
        B = p.bracket(G, H)
        N2 = mul(power(f, 2), B)
        N3 = mul(power(f, 2), add(mul(G, diff(N2)), scale(mul(N2, diff(G)), -3)))
        expanded = add(add(scale(mul(mul(mul(power(f, 3), diff(f)), B), G), 2),
                           mul(mul(power(f, 4), G), diff(B))),
                       scale(mul(mul(power(f, 4), B), diff(G)), -3))
        assert expanded == N3
        return G, H, B, N2, N3
    def quotient(a, b):
        out = []
        for k in range(4):
            ak = a[k] if k < len(a) else 0
            out.append((Q(ak)-sum(b[j]*out[k-j] for j in range(1, min(k+1, len(b)))))/b[0])
        return out
    samples = [([2, 3, 5, 7], [11, 13, 17, 19], [23, 29, 31, 37]),
               ([1, 0, 2, 3], [5, 7, 11, 13], [17, 19, 23, 29]),
               ([3, -2, 1, 5], [7, 3, -4, 2], [11, -5, 6, 1])]
    bad_rejected = 0
    for f, a, b in samples:
        G, H, B, N2, N3 = sections(f, a, b)
        ra, rb = quotient(a, f), quotient(b, f)
        assert f[0] and G[0] and ra[1]
        u1 = 1/ra[1]
        u2 = -ra[2]/ra[1]**3
        u3 = (2*ra[2]**2-ra[1]*ra[3])/ra[1]**5
        composed = [rb[1]*u1, rb[1]*u2+rb[2]*u1**2,
                    rb[1]*u3+2*rb[2]*u1*u2+rb[3]*u1**3]
        formulas = [Q(H[0], G[0]), Q(N2[0], 2*G[0]**3), Q(N3[0], 6*G[0]**5)]
        assert composed == formulas
        # All f's represent one-form coefficients under a nonlinear coordinate.
        change = [0, 2, 1, 1]
        transformed = sections(*(mul(comp(x, change), diff(change)) for x in (f, a, b)))
        for old, new, weight in zip((G, H, B, N2, N3), transformed, (3, 3, 7, 9, 15)):
            assert new == mul(comp(old, change), power(diff(change), weight))
        factor = [2, 1, 3]
        rescaled = sections(*(mul(x, factor) for x in (f, a, b)))
        for old, new, weight in zip((G, H, B, N2, N3), rescaled, (2, 2, 4, 6, 10)):
            assert new == mul(old, power(factor, weight))
        omitted = N3[0]-2*f[0]**3*diff(f)[0]*B[0]*G[0]
        bad_rejected += omitted != N3[0]
    assert bad_rejected >= 2
    return {"formal_series_reversion_cases": len(samples), "orders": [1, 2, 3],
            "coefficients_are_Taylor_coefficients_not_derivatives": True,
            "nonlinear_coordinate_covariance_weights": [3, 3, 7, 9, 15],
            "common_function_covariance_weights": [2, 2, 4, 6, 10],
            "third_derivative_omitted_term_controls_rejected": bad_rejected}


def height_checks():
    old = load_module("d105_bounds", ROOT / "dembele/pari/386_cm_frame_arithmetic_review.py")
    log2, log6 = old.log_bounds(2)[1], old.log_bounds(6)[1]
    assert log2 < Q(7, 10) and log6 < Q(9, 5)
    S = 6+35+17*15*20
    assert S == 5141
    exps = [20, 41, 63, 85]
    g = exps[0]+exps[1]+1
    gp = exps[0]+exps[2]+1
    gpp = max(exps[1]+exps[2], exps[0]+exps[3])+2
    b, bp = g+gp+1, g+gpp+1
    n2 = 2*exps[0]+b
    terms = [1+3*exps[0]+exps[1]+b+g, 4*exps[0]+g+bp, 2+4*exps[0]+b+gp]
    n3 = max(terms)+2
    assert (g, gp, gpp, b, bp, n2, n3) == (62, 84, 107, 147, 170, 187, 315)
    assert 3*10504+(n2-3*60)*log2+log2 < 31518
    assert 5*10504+(n3-5*60)*log2+log6 < 52533
    return {"adjugate_section_norm_power_two_exponent": S,
            "derivative_functional_power_two_exponents_orders_0_through_3": exps,
            "Gaussian_and_derivative_exponents_after_common_section_factor": [g, gp, gpp],
            "B_and_derivative_exponents_after_common_section_factor": [b, bp],
            "N2_N3_exponents_after_common_section_factor": [n2, n3],
            "D103_sharp_Gaussian_exponent": 60,
            "actual_ratio_Taylor_height_strict_upper_bounds_orders_1_to_3": [10504, 31518, 52533],
            "requires_a_common_valid_ratio_chart": True, "actual_jets_evaluated": False}


def build():
    paths = [Path(__file__), ROOT / "dembele/pari/376_cm_tangent_exactness.py",
             ROOT / "dembele/pari/386_cm_frame_arithmetic_review.py",
             DATA / "hyperellipticity_graph_review_d99.json",
             DATA / "cm_adjugate_height_d103.json", DATA / "cm_intrinsic_height_d104.json",
             DATA / "cm_frame_arithmetic_review_d105.json"]
    return {"status": "pass", "milestone": "D106", "graph": graph_checks(),
            "affine_group": affine_checks(), "formal_higher_jets": formal_jet_checks(),
            "height_constants": height_checks(), "sources": [source(p) for p in paths],
            "scope": "Finite checks only; actual curve specialization, CM Galois action and marked descent are mathematical inputs to the companion proof."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    if args.check:
        assert result == json.loads(OUT.read_text())
    else:
        assert not OUT.exists(), "Preserve completed artifacts."
        OUT.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "pass", "graph_group_order": result["graph"]["full_unweighted_automorphism_order"],
                      "target_jet_heights": result["height_constants"]["actual_ratio_Taylor_height_strict_upper_bounds_orders_1_to_3"]}), flush=True)
    print("PASS|D106_CM_RATIONAL_FRAME", flush=True)


if __name__ == "__main__":
    main()

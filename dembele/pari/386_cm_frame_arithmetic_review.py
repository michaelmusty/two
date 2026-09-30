"""D105 audit: marked graph reconstruction, noneffectivity witnesses and CM field.

Reconstructs the nine marked retractions from Brandt entries rather than the
probe's chosen edge list. Checks the saved potentials and burning orders without
calling the q-reduction algorithm. The companion report supplies the geometry.
"""
import argparse
import ast
from copy import deepcopy
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUT = DATA / "cm_frame_arithmetic_review_d105.json"


def source(path):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    p = p.resolve()
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def checked(items):
    paths = []
    for item in items:
        current = source(item["path"])
        assert current["sha256"] == item["sha256"], item["path"]
        paths.append(Path(current["path"]))
    return paths


def reconstruct_marks(saved):
    raw = json.loads((DATA / "hyperellipticity_fresh_brandt_d99.json").read_text())
    graph = json.loads((DATA / "hyperellipticity_graph_review_d99.json").read_text())
    matrix, stabilizers = raw["matrix"], raw["stabilizers"]
    n = len(matrix)
    assert n == 58
    adj = {i+1: {} for i in range(n)}
    off_edges, diagonal = [], []
    for i in range(n):
        assert matrix[i][i] in (0, 1)
        if matrix[i][i]:
            diagonal.append(i+1)
        for j in range(i+1, n):
            if not matrix[i][j]:
                assert not matrix[j][i]
                continue
            assert min(matrix[i][j], matrix[j][i]) == 1
            w = Q(stabilizers[j], matrix[i][j])
            assert w == Q(stabilizers[i], matrix[j][i])
            adj[i+1][j+1] = adj[j+1][i+1] = w
            off_edges.append([i+1, j+1, str(w)])
    assert diagonal == [5, 51, 52, 53, 54, 55, 56, 57, 58]
    assert off_edges == graph["quotient_edges"][:73]
    assert len(graph["quotient_edges"]) == 82
    for k, v in enumerate(diagonal):
        assert graph["quotient_edges"][73+k] == [v, 59+k, str(Q(stabilizers[v-1], 2))]

    # Remove the rational tails, moving a mark to the attachment vertex.
    locations = {v: v for v in diagonal}
    removed = []
    while True:
        leaves = sorted(v for v in adj if len(adj[v]) == 1)
        if not leaves:
            break
        v = leaves[0]
        u = next(iter(adj[v]))
        moved = [label for label in locations if locations[label] == v]
        for label in moved:
            locations[label] = u
        removed.append({"from": v, "to": u, "marks_moved": moved})
        del adj[u][v]
        del adj[v]
    assert all(len(neighbors) in (2, 3) for neighbors in adj.values())
    ends = sorted(v for v in adj if len(adj[v]) == 3)
    assert ends == graph["stable_vertices"]
    stable, positions, used = [], {}, set()
    for u in ends:
        for v in sorted(adj[u]):
            if frozenset((u, v)) in used:
                continue
            path, distances = [u], [Q(0)]
            a, b = u, v
            while True:
                used.add(frozenset((a, b)))
                path.append(b)
                distances.append(distances[-1]+adj[a][b])
                if b in ends:
                    break
                c = next(x for x in adj[b] if x != a)
                a, b = b, c
            assert u < b
            stable.append([u, b, str(distances[-1])])
            for original, distance in zip(path[1:-1], distances[1:-1]):
                positions[original] = (u, b, distance)
    assert len(used) == sum(map(len, adj.values()))//2
    stable.sort()
    assert stable == graph["stable_edges"]
    vertices, edges, at = [f"v{v}" for v in ends], [], {}
    for u, v, length in stable:
        length = Q(length)
        assert length.denominator == 1
        chain = [ends.index(u)]
        for k in range(1, int(length)):
            at[u, v, Q(k)] = len(vertices)
            vertices.append(f"e{u}_{v}_{k}")
            chain.append(len(vertices)-1)
        chain.append(ends.index(v))
        edges.extend([a, b] for a, b in zip(chain, chain[1:]))
    marks = []
    branch = [0]*len(vertices)
    for label in diagonal:
        core_vertex = locations[label]
        u, v, distance = positions[core_vertex]
        index = at[u, v, distance]
        length = Q(next(w for a, b, w in stable if (a, b) == (u, v)))
        assert 2*distance == length
        marks.append({"diagonal_class": label, "core_vertex": core_vertex,
                      "stable_edge": [u, v], "distance_from_first_end": str(distance),
                      "unit_vertex": index, "unit_vertex_name": vertices[index]})
        branch[index] += 2
    assert vertices == saved["vertices"] and edges == saved["unit_edges"]
    assert branch == saved["branch_divisor"] and sum(branch) == 18
    assert len(vertices) == 61 and len(edges) == 76
    return {"input": "fresh D99 Brandt entries and stabilizers",
            "algebraic_quotient_edges": len(off_edges), "tail_retractions": removed,
            "marks": marks, "stable_vertices": len(ends), "stable_edges": len(stable),
            "unit_vertices": len(vertices), "unit_edges": len(edges),
            "all_marks_are_midpoints": True}


def witness(saved, case):
    n, root = len(saved["vertices"]), saved["root_index"]
    adj = [[] for _ in range(n)]
    for u, v in saved["unit_edges"]:
        assert 0 <= u < n and 0 <= v < n and u != v
        adj[u].append(v)
        adj[v].append(u)
    k = case["distinguished_vertex"]
    branch = saved["branch_divisor"]
    assert branch[k] == 2
    expected = [len(adj[i])-2-branch[i]+int(i == k) for i in range(n)]
    assert sum(expected) == 13 and case["canonical_minus_CM_divisor"] == expected
    cert = case["certificate"]
    f = cert["integer_potential"]
    assert len(f) == n and all(type(x) is int for x in f)
    reduced = expected[:]
    # Edgewise flux, independently of the discovery program's Laplacian.
    for u, v in saved["unit_edges"]:
        flux = f[u]-f[v]
        reduced[u] += flux
        reduced[v] -= flux
    assert reduced == cert["q_reduced"] and sum(reduced) == 13
    assert reduced[root] == cert["root_coefficient"] < 0
    assert all(reduced[i] >= 0 for i in range(n) if i != root)
    order = cert["burn_order"]
    assert sorted(order) == list(range(n)) and order[0] == root
    earlier = {root}
    for v in order[1:]:
        assert reduced[v] < sum(u in earlier for u in adj[v])
        earlier.add(v)
    assert cert["effective_representative_exists"] is False
    return {"distinguished_vertex": k, "root_coefficient": reduced[root],
            "potential_identity": True, "all_vertices_burn": True,
            "minimum_positive_burning_margin": min(
                sum(order.index(u) < order.index(v) for u in adj[v])-reduced[v]
                for v in order[1:])}


def expect_rejected(saved, case):
    try:
        witness(saved, case)
    except AssertionError:
        return True
    raise AssertionError("Corrupted noneffectivity certificate was accepted")


def poly_mul(a, b, f):
    n = len(f)-1
    out = [0]*(2*n-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    for k in range(len(out)-1, n-1, -1):
        for i in range(n):
            out[k-n+i] -= out[k]*f[i]
    return out[:n]


def det_mod(a, p):
    a, d = [[x % p for x in row] for row in a], 1
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            d = -d
        d = d*a[j][j] % p
        inv = pow(a[j][j], -1, p)
        for i in range(j+1, len(a)):
            c = a[i][j]*inv % p
            a[i] = [(x-c*y) % p for x, y in zip(a[i], a[j])]
    return d % p


def field_check(orbit):
    info = orbit["field_root_action"]
    cm = orbit["CM_orbit"]
    assert cm["class_number_proved"] == 17 and cm["class_group_invariants"] == [17]
    assert sorted(cm["class_labels_in_point_order"]) == list(range(17))
    assert info["p_adic_galois_proof"] and info["group_order"] == 272
    log = (ROOT / info["source"]["path"]).read_text()
    assert "GROUP_ORDER| 272" in log and "PADIC_PROOF|true" in log
    assert "PASS|96_cm_root_action" in log
    line = next(x for x in log.splitlines() if x.startswith("RESOLVENT|"))
    resolvent = ast.literal_eval(line.split("|", 1)[1].strip())
    assert resolvent == info["resolvent_ascending"]
    assert int(info["resolvent_coefficient_bound"]) == 1089**16
    assert int(info["lift_modulus"]) == 31**70 > 2*1089**16
    f = list(map(int, cm["CM_polynomial_ascending"]))
    assert f[-1] == 1 and f[0] % 4 == 2 and all(x % 2 == 0 for x in f[:-1])
    gamma = list(map(int, orbit["matching"]["resolvent_generator_in_K"]))
    powers = [[1]+[0]*15]
    for _ in range(16):
        powers.append(poly_mul(powers[-1], gamma, f))
    residual = [sum(c*row[i] for c, row in zip(resolvent, powers)) for i in range(16)]
    assert residual == [0]*16
    prime, determinant = next((p, det_mod(powers[:16], p)) for p in [31, 101, 103]
                              if det_mod(powers[:16], p))
    # Replay the frozen integral-order arithmetic. Its discriminant, not the
    # generally larger power-order discriminant, proves odd-prime unramifiedness.
    spec = importlib.util.spec_from_file_location("lattice", ROOT / "dembele/pari/378_cm_residue_lattice.py")
    lattice = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lattice)
    order = lattice.field_lattice()
    assert order == json.loads((DATA / "cm_residue_lattice_d102.json").read_text())["field_lattice"]
    assert order["ring_discriminant"] == 2**79
    return {"splitting_group_order_from_proved_D59_run": 272,
            "CM_class_number_from_proved_D59_run": 17,
            "CM_Eisenstein_at_2": True, "resolvent_evaluates_to_zero_exactly": True,
            "gamma_degree_certificate_prime": prime, "gamma_power_basis_determinant_mod_prime": determinant,
            "CM_field_degree": 16, "resolvent_degree": 16,
            "root_field_integral_order_discriminant": str(order["ring_discriminant"]),
            "integral_order_arithmetic_replayed": True,
            "common_field_degree_via_companion_class_field_proof": 272,
            "numerical_orientation_used": False, "F_equivariant_point_root_matching_proved": False}


def log_bounds(x):
    x, e = Q(x), 0
    assert x > 0
    while x >= 2:
        x /= 2
        e += 1
    assert 1 <= x < 2

    def series(y):
        t = (y-1)/(y+1)
        low = sum((2*t**(2*j+1)/Q(2*j+1) for j in range(48)), Q(0))
        return low, low+2*t**97/(97*(1-t*t))

    a, b = series(x), series(Q(2))
    return a[0]+e*b[0], a[1]+e*b[1]


def atlas_budget():
    candidate = json.loads((DATA / "cm_tangent_exactness_d101.json").read_text())
    rows = [list(map(Q, row)) for row in candidate["candidate_tangent_power_basis"]]
    assert len(rows) == 16 and all(len(row) == 17 for row in rows)
    assert not any(rows[0]) and rows[1] == [1]+[0]*16
    assert all(any(row) for row in rows[1:])
    f = json.loads((DATA / "cm_arithmetic_audit.json").read_text())["residue_algebra_input"]["polynomial_coefficients_ascending"]
    assert f[-1] == 1 and sum(abs(c)*4**i for i, c in enumerate(f[:-1])) < 4**17
    q = lcm(*(c.denominator for row in rows[1:] for c in row))
    bounds = [sum(abs(q*c)*4**i for i, c in enumerate(row)) for row in rows[1:]]
    assert all(x.denominator == 1 for x in bounds)
    upper = int(max([Q(q)]+bounds))
    bits = upper.bit_length()
    assert bits == 976 and bits*log_bounds(2)[1] < 677
    # Projective height bounds every coordinate ratio in every valid chart.
    degree, target, reference = 272, 10504, 677
    difference = Q(target+reference)+Q(7, 10)
    log10 = log_bounds(10)
    one = (degree*difference/log10[0]).__floor__()+1
    every = (difference/log10[0]).__floor__()+1
    assert (one, every) == (1320873, 4857)
    assert one*log10[0] > degree*difference and every*log10[0] > difference
    return {"candidate_only_common_clearing_integer": str(q),
            "candidate_only_coordinate_absolute_bounds": list(map(str, bounds)),
            "candidate_strict_power_of_two_exponent": bits, "candidate_projective_height_upper": reference,
            "actual_projective_height_upper_via_D103_D104_and_companion_proof": target,
            "number_of_charts": 15, "all_candidate_pivots_nonzero": True,
            "specific_actual_G12_nonzero_proved": False, "common_field_degree_bound": degree,
            "difference_height_upper": str(difference),
            "sufficient_single_embedding_decimal_error_exponent": one,
            "sufficient_all_embeddings_decimal_error_exponent": every,
            "thresholds_are_sufficient_not_minimal": True,
            "requires_consistent_choice_of_bijection_and_common_nonzero_chart": True,
            "actual_errors_certified": False}


def build():
    paths = [Path(__file__)]
    saved_path = DATA / "cm_frame_specialization_d105.json"
    saved = json.loads(saved_path.read_text())
    paths += checked(saved["sources"])+[saved_path]
    previous = {}
    for label, name in (("D99", "hyperellipticity_review_d99.json"),
                        ("D104", "cm_intrinsic_height_review_d104.json")):
        p = DATA / name
        old = json.loads(p.read_text())
        paths += checked(old["sources"])+[p]
        previous[label] = len(old["sources"])
    for stem in ("cm_frame_specialization_probe_d105", "cm_frame_specialization_d105"):
        p = DATA / (stem+"_attempt01.job.json")
        job = json.loads(p.read_text())
        assert job["status"] == "pass" and job["timeout_seconds"] == 180
        assert job["wall_seconds"] < 180 and job["timeout_terminates_process_group"]
        paths += checked(job["sources"]+[job["driver"], job["log"]])+[p]
    marks = reconstruct_marks(saved)
    witnesses = [witness(saved, case) for case in saved["cases"]]
    assert [r["root_coefficient"] for r in witnesses] == [-3]+[-2]*8
    bad_potential = deepcopy(saved["cases"][0])
    bad_potential["certificate"]["integer_potential"][0] += 1
    bad_order = deepcopy(saved["cases"][0])
    bad_order["certificate"]["burn_order"][1:3] = [0, 0]
    bad_branch = deepcopy(saved["cases"][0])
    bad_branch["distinguished_vertex"] = saved["cases"][1]["distinguished_vertex"]
    controls = {"altered_potential_rejected": expect_rejected(saved, bad_potential),
                "altered_burning_order_rejected": expect_rejected(saved, bad_order),
                "altered_distinguished_branch_allocation_rejected": expect_rejected(saved, bad_branch)}
    orbit_path = DATA / "cm_orbit.json"
    orbit = json.loads(orbit_path.read_text())
    paths += checked([orbit[k] for k in ["script_source", "helper_source", "magma_script_source", "domain_source"]]
                     +[orbit["field_root_action"]["source"]])+[orbit_path]
    arithmetic = field_check(orbit)
    budget = atlas_budget()
    paths += [DATA / "hyperellipticity_fresh_brandt_d99.json",
              DATA / "cm_tangent_exactness_d101.json", DATA / "cm_residue_lattice_d102.json",
              DATA / "cm_frame_arithmetic_sources_d105.json",
              ROOT / "dembele/certificates/cm-frame-arithmetic-d105.md"]
    return {"status": "pass", "milestone": "D105", "marked_graph_reconstruction": marks,
            "independent_noneffectivity_witness_checks": witnesses, "corruption_controls": controls,
            "auxiliary_CM_field": arithmetic, "tangent_atlas_and_recognition_budget": budget,
            "previous_source_hashes_checked": previous,
            "sources": [source(p) for p in sorted(set(p.resolve() for p in paths))],
            "actual_CM_frame_full_rank_and_all_cofactors_nonzero_via_companion_proof": True,
            "finite_tangent_atlas_available_over_H": True,
            "saved_arithmetic_point_root_orientation_certified": False,
            "candidate_identification_proved": False, "independent_Shimura_tangent_obtained": False,
            "spectral_pilot_gate_passed": False,
            "scope": "Exact finite witnesses and source preservation; geometric lemmas and cited theorems are not machine-verified."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        old = json.loads(OUT.read_text())
        checked(old["sources"])
    result = build()
    if args.check:
        assert result == old
    else:
        assert not OUT.exists(), "Preserve completed reviews."
        OUT.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "pass", "source_hashes": len(result["sources"]),
                      "previous_hashes_checked": result["previous_source_hashes_checked"],
                      "noneffectivity_cases": 9, "auxiliary_field_degree": 272,
                      "projective_tangent_height_upper": 10504,
                      "sufficient_decimal_error_exponents": [1320873, 4857]}), flush=True)
    print("PASS|D105_CM_FRAME_ARITHMETIC_REVIEW", flush=True)


if __name__ == "__main__":
    main()

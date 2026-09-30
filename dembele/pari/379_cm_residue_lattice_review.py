"""D102 review: independent trace arithmetic, quartic control and source binding."""
import argparse
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUT = DATA / "cm_residue_lattice_review_d102.json"
SPEC = importlib.util.spec_from_file_location("d102_lattice", ROOT / "dembele/pari/378_cm_residue_lattice.py")
L = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(L)


def bareiss(a):
    """Independent fraction-free determinant for integer matrices."""
    a = [list(row) for row in a]
    n, sign, previous = len(a), 1, 1
    for k in range(n-1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[pivot], a[k] = a[k], a[pivot]
            sign = -sign
        p = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                value = p*a[i][j]-a[i][k]*a[k][j]
                assert value % previous == 0
                a[i][j] = value//previous
            a[i][k] = 0
        previous = p
    return sign*a[-1][-1]


def independent_traces(saved):
    f = saved["field_lattice"]["polynomial"]
    n = len(f)-1
    powers = [[1]+[0]*(n-1)]
    # Repeated multiplication by theta in the power basis, independently of Newton sums.
    for k in range(3*n):
        row = [0]+powers[-1]
        lead = row.pop()
        powers.append([x-lead*c for x, c in zip(row, f)])
    traces = [sum(powers[k+j][j] for j in range(n)) for k in range(2*n-1)]
    b = [[Q(x) for x in row] for row in json.loads(L.BASIS.read_text())["field_basis"]["integral_basis_power_coordinates"]]
    gram = L.mul(L.mul(b, [[traces[i+j] for j in range(n)] for i in range(n)]), L.transpose(b))
    assert gram == saved["field_lattice"]["trace_gram"]
    gram = [[int(x) for x in row] for row in gram]
    assert bareiss(gram) == 2**79
    t = gram[0]
    centered = [[17*gram[i][j]-t[i]*t[j] for j in range(1, n)] for i in range(1, n)]
    assert abs(bareiss(centered)) == 2**79*17**15
    corrupted = [row[:] for row in gram]
    corrupted[1][1] += 1
    assert bareiss(corrupted) != 2**79
    return {"trace_algorithm": "diagonals of multiplication by powers of theta",
            "determinant_algorithm": "fraction-free Bareiss",
            "trace_discriminant": 2**79, "scaled_centered_index": 2**79*17**15,
            "corrupted_Gram_matrix_rejected": True}


def quartic_controls():
    records = []
    for n in [1, 2, 4, 8, 16]:
        q, precision = 17**n, n+8
        modulus, r, current = 17**precision, 4, 17
        target = 1-q**4
        while current < modulus:
            digit = (-(r**4-target)//current)*pow(4*r**3, -1, 17) % 17
            r += digit*current
            current *= 17
        assert (r**4+q**4-1) % modulus == 0 and r % 17 == 4
        e = [[1, 1, 0], [1, -1, 0], [1, r, q], [1, 0, 1]]
        c = [(-1)**i*bareiss(e[:i]+e[i+1:]) for i in range(4)]
        assert c == [r+1-q, 1-r-q, -2, 2*q]
        assert L.mul([c], e) == [[0, 0, 0]]
        assert [L.valuation(x, 17) for x in c] == [0, 0, 0, n]
        residues = [[a*x for x in row] for a, row in zip(c, e)]
        assert L.valuation(bareiss(residues[:3]), 17) == n
        records.append({"n": n, "precision": precision, "root_mod_17_power": r,
                        "cofactor_valuations": [0, 0, 0, n], "residue_index_valuation": n})
    return {"curve": "x^4+y^4=z^4 over Z_17", "genus": 3,
            "fixed_smooth_nonhyperelliptic_curve": True,
            "D_degree": 4, "D_split_etale": True, "H1_O_D_zero": True,
            "CM_counterexample_claimed": False, "closed_point_counterexample_claimed": False,
            "controls": records}


def build():
    saved = json.loads(L.OUT.read_text())
    for item in saved["sources"]:
        assert L.source(item["path"]) == item
    assert L.build() == saved
    jobpath = DATA / "cm_residue_lattice_d102_attempt01.job.json"
    job = json.loads(jobpath.read_text())
    assert job["status"] == "pass" and job["timeout_seconds"] == 180
    assert job["wall_seconds"] < 180 and job["timeout_terminates_process_group"]
    for item in job["sources"]+[job["driver"], job["log"]]:
        assert L.source(item["path"]) == item
    oldpath = DATA / "cm_tangent_exactness_review_d101.json"
    old = json.loads(oldpath.read_text())
    for item in old["sources"]:
        assert L.source(item["path"]) == item
    paths = [Path(__file__), L.OUT, jobpath, oldpath,
             ROOT / "dembele/certificates/cm-residue-lattice-d102.md",
             DATA / "cm_residue_lattice_sources_d102.json"]
    paths += [Path(x["path"]) for x in saved["sources"]+job["sources"]+[job["driver"], job["log"]]]
    return {"status": "pass", "milestone": "D102",
            "independent_trace_checks": independent_traces(saved),
            "nonhyperelliptic_geometric_control": quartic_controls(),
            "D101_bound_source_hashes_checked": len(old["sources"]),
            "sources": [L.source(p) for p in sorted(set(p.resolve() for p in paths))],
            "actual_residue_index_bounded": False, "independent_Shimura_tangent_obtained": False,
            "spectral_pilot_gate_passed": False,
            "scope": "Exact field arithmetic and proof controls; no actual Shimura restriction map or effective recognition tolerance."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        old = json.loads(OUT.read_text())
        for item in old["sources"]:
            assert L.source(item["path"]) == item
    result = build()
    if args.check:
        assert result == old
    else:
        assert not OUT.exists(), "Preserve completed audits."
        OUT.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "pass", "source_hashes": len(result["sources"]),
                      "D101_hashes_unchanged": result["D101_bound_source_hashes_checked"],
                      "independent_trace_checks": "pass", "plane_quartic_controls": "pass",
                      "actual_tangent_obtained": False}), flush=True)
    print("PASS|D102_RESIDUE_LATTICE_REVIEW", flush=True)


if __name__ == "__main__":
    main()

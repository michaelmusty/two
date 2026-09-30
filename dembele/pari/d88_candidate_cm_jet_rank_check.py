"""Independent finite-field replay of D88 candidate CM jet ranks.

This checks candidate-derived data. It does not evaluate Shimura forms.
"""
import argparse
import ast
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
PRIME, DEGREE = 31, 17


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def rank(rows):
    a = [[int(z) % PRIME for z in row] for row in rows]
    pivot = 0
    for col in range(len(a[0])):
        found = next((i for i in range(pivot, len(a)) if a[i][col]), None)
        if found is None:
            continue
        a[pivot], a[found] = a[found], a[pivot]
        inv = pow(a[pivot][col], -1, PRIME)
        a[pivot] = [(z * inv) % PRIME for z in a[pivot]]
        for i in range(pivot + 1, len(a)):
            c = a[i][col]
            if c:
                a[i] = [(x - c*y) % PRIME for x, y in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    model_path = DATA / "cm_frame_curve_candidate.json"
    model = json.loads(model_path.read_text())
    h = [int(x) % PRIME for x in model["CM_field_polynomial_ascending"]]
    assert len(h) == 18 and h[-1] == 1
    zero = [0] * DEGREE
    one = [1] + [0] * (DEGREE-1)

    def add(*vs):
        return [sum(entries) % PRIME for entries in zip(*vs)]

    def mul(a, b):
        out = [0] * (2*DEGREE-1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i+j] += x*y
        for i in range(2*DEGREE-2, DEGREE-1, -1):
            c = out[i] % PRIME
            for j in range(DEGREE):
                out[i-DEGREE+j] -= c*h[j]
        return [z % PRIME for z in out[:DEGREE]]

    def modq(s):
        q = Fraction(s)
        return q.numerator * pow(q.denominator, -1, PRIME) % PRIME

    jobs = [json.loads((DATA / name).read_text()) for name in
            ["d88_candidate_cm_jet_rank_job.json", "d88_candidate_cm_jet_rank_v2_job.json"]]
    for job in jobs:
        for item in job["sources"] + [job["driver"], job["log"]]:
            assert source(item["path"]) == item
    assert jobs[0]["status"] == "failed" and jobs[1]["status"] == "pass"
    text = Path(jobs[1]["log"]["path"]).read_text()
    assert "PASS|D88_CANDIDATE_CM_JET_RANK" in text

    def block(label, next_label):
        found = re.search(r"^" + label + r"\|(.+?)^" + next_label + r"\|", text, re.M | re.S)
        assert found
        return ast.literal_eval(found.group(1).strip())

    jets = block("JETS", "JET_MATRIX")
    stored_matrix = block("JET_MATRIX", "CPU_SECONDS")
    chart = re.search(r"^CHART\|(\d+)\|(\d+)$", text, re.M)
    assert chart
    anchor, param = (int(z)-1 for z in chart.groups())
    pt, tangent, second = jets
    assert len(jets) == 3 and all(len(row) == 16 for row in jets)
    assert all(len(z) == DEGREE and all(0 <= c < PRIME for c in z) for row in jets for z in row)
    original = [[modq(s) for s in z] for z in model["CM_projective_coordinates_power_basis"]]
    assert all(mul(pt[i], original[anchor]) == original[i] for i in range(16))
    assert pt[anchor] == one and tangent[anchor] == second[anchor] == zero
    assert tangent[param] == one and second[param] == zero
    pairs = model["monomial_pairs"]

    def matrix_from(jets):
        p, v, c = jets
        products = [[mul(p[i],p[j]), add(mul(p[i],v[j]),mul(v[i],p[j])),
                     add(mul(p[i],c[j]),mul(v[i],v[j]),mul(c[i],p[j]))] for i,j in pairs]
        return [[products[m][s][d] for m in range(136)] for s in range(3) for d in range(DEGREE)]

    def annihilates(a):
        return all(sum(c*x for c,x in zip(q,row)) % PRIME == 0
                   for q in model["quadrics"] for row in a)

    matrix = matrix_from(jets)
    assert matrix == stored_matrix and annihilates(matrix)
    ranks = [rank(matrix[:DEGREE*n]) for n in (1,2,3)]
    assert ranks == [17,34,45] and rank(model["quadrics"]) == 91
    # A nonlinear reparametrization t_old=t_new+t_new^2 preserves the kernel.
    moved = [pt, tangent, [add(c,v) for c,v in zip(second,tangent)]]
    moved_matrix = matrix_from(moved)
    assert annihilates(moved_matrix) and rank(moved_matrix) == 45
    # A wrong highest coefficient keeps the first two blocks but fails equations.
    corrupted = json.loads(json.dumps(jets))
    changed = next(i for i in range(16) if i not in (anchor,param))
    corrupted[2][changed] = add(corrupted[2][changed],one)
    bad_matrix = matrix_from(corrupted)
    assert bad_matrix[:34] == matrix[:34] and not annihilates(bad_matrix)
    paths = [__file__, model_path, DATA / "cm_frame_curve_candidate.m",
             DATA / "cm_frame_curve_verification.json", DATA / "cm_frame_marks_check.json",
             DATA / "d88_candidate_cm_jet_rank_job.json", DATA / "d88_candidate_cm_jet_rank_v2_job.json"]
    report = {"status":"pass", "date":"2026-09-23", "milestone":"D88 diagnostic",
              "scope":"candidate-side CM jets only", "prime":PRIME, "residue_degree":DEGREE,
              "chart_anchor_one_based":anchor+1, "parameter_coordinate_one_based":param+1,
              "jet_ranks_one_two_three_coefficients":ranks,
              "quadrics_rank":91, "quadrics_annihilate_jet_matrix":True,
              "nonlinear_reparametrization_control":True, "highest_coefficient_error_rejected":True,
              "candidate_J3_rank_over_Q":45,
              "rank_over_Q_reason":"Nonzero minor modulo 31 in the smooth marked model; rank is at most h0(2K)=45.",
              "Shimura_side_jets_obtained":False, "Shimura_identification_certified":False,
              "sources":[source(p) for p in paths], "jobs":jobs,
              "CM_field_polynomial_ascending":model["CM_field_polynomial_ascending"],
              "candidate_projective_jets_mod31":jets, "jet_matrix_mod31":matrix}
    target = DATA / "d88_candidate_cm_jet_rank.json"
    if args.check:
        assert json.loads(target.read_text()) == report
    else:
        assert not target.exists()
        target.write_text(json.dumps(report,indent=2)+"\n")
    print("PASS: candidate jet ranks 17/34/45; source/log hashes, polynomial identities and controls verified")


if __name__ == "__main__":
    main()

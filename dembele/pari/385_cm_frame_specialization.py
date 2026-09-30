"""D105: all nine possible distinguished branch locations on the actual metric graph.

The companion proof supplies the branch specialization, independently of which
branch point is P32. The saved integer potentials and burning orders are short
non-effectivity certificates, not numerical evidence from candidate equations.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUT = DATA / "cm_frame_specialization_d105.json"
PROBE = DATA / "cm_frame_specialization_probe_d105.json"
SPEC = importlib.util.spec_from_file_location("probe", ROOT / "dembele/pari/384_cm_frame_specialization_probe.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def source(path):
    p = Path(path).resolve()
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def build():
    probe = json.loads(PROBE.read_text())
    for item in probe["sources"]:
        assert source(item["path"]) == item
    vertices, edges, root = probe["vertices"], probe["unit_edges"], probe["root_index"]
    adj = [[] for _ in vertices]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    branch = [2 if x else 0 for x in probe["hypothetical_marked_divisor"]]
    assert sum(branch) == 18
    canonical = [len(neighbors)-2 for neighbors in adj]
    cases = []
    for distinguished in (i for i, x in enumerate(branch) if x):
        marked = branch[:]
        marked[distinguished] -= 1
        difference = [k-d for k, d in zip(canonical, marked)]
        certificate = M.reduced(adj, difference, root)
        assert certificate["root_coefficient"] < 0
        assert not certificate["effective_representative_exists"]
        cases.append({"distinguished_vertex": distinguished,
                      "distinguished_vertex_name": vertices[distinguished],
                      "canonical_minus_CM_divisor": difference, "certificate": certificate})
    assert len(cases) == 9
    return {"status": "pass", "milestone": "D105", "vertices": vertices, "unit_edges": edges,
            "root_index": root, "branch_divisor": branch, "cases": cases,
            "all_nine_canonical_minus_CM_divisors_noneffective": True,
            "arithmetic_CM_frame_full_rank_via_companion_proof": True,
            "particular_P32_retraction_not_assumed": True,
            "candidate_equations_or_jets_used": False,
            "sources": [source(Path(__file__)), source(Path(M.__file__)), source(PROBE),
                        source(DATA / "hyperellipticity_graph_review_d99.json")]}


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
        assert not OUT.exists()
        OUT.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "pass", "cases": len(result["cases"]),
                      "root_coefficients": [x["certificate"]["root_coefficient"] for x in result["cases"]]}), flush=True)
    print("PASS|D105_CM_FRAME_SPECIALIZATION", flush=True)


if __name__ == "__main__":
    main()

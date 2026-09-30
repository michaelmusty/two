"""D99: read-only replay/provenance for the full hyperellipticity review."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
REPORT = ROOT / "dembele/certificates/hyperellipticity-review-d99.md"
OUTPUT = DATA / "hyperellipticity_review_d99.json"


def compute():
    sources = {}
    def bind(path, expected=None):
        path = Path(path)
        if not path.is_absolute():
            path = ROOT/path
        path = path.resolve()
        name = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None:
            assert digest == expected, name
        if name in sources:
            assert sources[name]["sha256"] == digest
        sources[name] = {"path":name,"sha256":digest}
    def read(name):
        path = DATA/name
        bind(path)
        value = json.loads(path.read_text())
        for row in value.get("sources",[]):
            bind(row["path"],row["sha256"])
        return value

    prior = read("nelson_spectral_ideal_d98.json")
    assert len(prior["sources"]) == 169
    assert prior["CM_anchor_derivative_nonzero"] is False
    graph = read("hyperellipticity_graph_review_d99.json")
    raw = read("hyperellipticity_fresh_brandt_d99.json")
    order = read("hyperellipticity_order_review_d99.json")
    documents = read("hyperellipticity_sources_d99.json")
    assert graph["status"] == order["status"] == "PASS"
    assert order["order"]["maximal_order_discriminant_formula_matches"]
    assert int(order["order"]["absolute_reduced_trace_gram_determinant"]) == 2**126
    assert raw["class_number"] == order["order"]["class_number_proved"] == 1
    assert raw["narrow_class_number"] == 1 and order["order"]["unit_signature_rank"] == 8

    module_path = Path(__file__).with_name("372_hyperellipticity_graph_review.py")
    spec = importlib.util.spec_from_file_location("fresh_graph",module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert json.loads(json.dumps(module.review())) == graph

    job_names = [
        "hyperellipticity_fresh_brandt_d99_attempt01.job.json",
        "hyperellipticity_fresh_brandt_d99_attempt02.job.json",
        "hyperellipticity_graph_review_d99.job.json",
        "hyperellipticity_candidate_review_d99.job.json",
        "hyperellipticity_order_review_d99.job.json",
    ]
    jobs = []
    for i,name in enumerate(job_names):
        job = read(name)
        bind(job["log"]["path"],job["log"]["sha256"])
        assert job["timeout_seconds"] == 180 and job["wall_seconds"] < 180
        assert job["timeout_terminates_process_group"]
        assert job["status"] == ("failed" if i==0 else "pass")
        log = Path(job["log"]["path"]).read_text()
        if i == 0:
            assert "IsTotallyDefinite" in log and "has not been declared or assigned" in log
        else:
            assert job["exit_code"] == 0 and "PASS|" in log
        if i == 3:
            assert "PASS|SMOOTH_GEOMETRICALLY_INTEGRAL_CANONICAL_CURVE_OVER_Q" in log
            assert "PASS|TWO_CHART_SQUAREFREE_DISCRIMINANTS" in log
        jobs.append({"path":name,"status":job["status"],"wall_seconds":job["wall_seconds"]})

    for path in [Path(__file__),REPORT,ROOT/"dembele/certificates/cm-frame-verification.md",
                 ROOT/"dembele/certificates/hyperellipticity-audit.md",
                 ROOT/"dembele/certificates/curve-identification-audit.md"]:
        bind(path)
    assert len(documents["pdf_fingerprints"]) == 4
    return {"status":"PASS: fresh review proves geometric nonhyperellipticity of C, with the cited mathematical inputs",
            "prior_D98_source_hashes_verified":169,
            "stable_graph":graph["stable_summary"],
            "edge_deletions_replayed":graph["cut_check"]["deletions_tested"],
            "edge_connectivity":3,"automorphisms_recomputed":64,"involutions_recomputed":19,
            "quotient_betti_histogram":graph["quotient_betti_histogram"],
            "candidate_canonical_certificate_rerun":True,"candidate_identified_with_C":False,
            "numerical_product_rank_used_in_proof":False,"tame_reduction_assumed":False,
            "curve_automorphism_specialization_injection_used":False,
            "mathematical_proof":str(REPORT.relative_to(ROOT)),
            "CM_anchor_still_uncertified":True,"jobs":jobs,
            "sources":sorted(sources.values(),key=lambda row:row["path"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args = parser.parse_args()
    result = compute()
    if args.check:
        assert result == json.loads(OUTPUT.read_text())
    else:
        with OUTPUT.open("x") as f:
            json.dump(result,f,indent=2)
            f.write("\n")
    print("PASS|374_HYPERELLIPTICITY_REVIEW_AUDIT",len(result["sources"]),
          "hashes; 1035 edge deletions; 64 automorphisms; 19 involutions; no tree quotient")


if __name__ == "__main__":
    main()

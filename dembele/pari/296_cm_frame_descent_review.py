"""D85: exact small checks supporting the coefficient-field/descent review.

These checks do not identify the candidate with a Shimura curve or compute
the Galois action on its third-division torsor.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
BASE = DATA / "cm_frame_descent_review"
MARKER = "PASS|296_DESCENT_REVIEW"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "dembele/pari" / filename)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


prior = module("review_prior", "201_cm_frame_cubic_precision.py")
jobs = module("review_jobs", "272_cm_frame_bounded_jobs.py")


def worker():
    from sage.all import NumberField, PolynomialRing, QQ, SymmetricGroup
    R = PolynomialRing(QQ, "x"); x = R.gen()
    F = NumberField(x**8-8*x**6+20*x**4-16*x**2+2, "b")
    assert not F(5).is_square()
    root, digits = 6, 1
    assert (root*root-5) % 31 == 0
    while digits < 128:
        digits = min(2*digits, 128); modulus = 31**digits
        root = (root-(root*root-5)*pow(2*root, -1, modulus)) % modulus
    assert (root*root-5) % modulus == 0
    G = SymmetricGroup(3); H = G.subgroup([G("(1,2)")])
    normalizer = [g for g in G if all(g*h*g**-1 in H for h in H)]
    conjugates = {frozenset(g*h*g**-1 for h in H) for g in G}
    assert len(normalizer) == H.order() == 2 and len(conjugates) == 3
    source = DATA / "cm_frame_structural_checkpoint.json"
    previous = json.loads(source.read_text()); prior.checks.verify_records(previous)
    assert previous["compatible_thirds_tested"] == 9
    result = {
        "status": "pass", "milestone": "D85", "date": "2026-09-22",
        "sources": [prior.checks.source(p) for p in (Path(__file__), source)],
        "prym_dimension_from_genera": 40-16,
        "geometric_antiinvariant_three_torsion_rank": 2*(40-16),
        "geometric_third_torsor_degree": 3**48,
        "degree_scope": "Theoretical count from the 24-dimensional Prym in characteristic zero; not an enumeration or a coefficient-field degree.",
        "local_rationality_counterexample": {"polynomial": [-5, 0, 1],
            "root_mod_31": 6, "precision_digits": 128, "root": root,
            "root_equation_verified": True, "has_root_in_F": False},
        "reflection_subgroup_order": 2, "reflection_normalizer_order": 2,
        "reflection_conjugates": 3,
        "geometric_automorphisms_over_fixed_base_for_S3_cubic": 1,
        "global_Galois_action_on_selected_third_computed": False,
        "field_of_moduli_of_candidate_cover_established": False,
        "arithmetic_identification_certified": False,
        "references": ["https://stacks.math.columbia.edu/tag/0BF9",
            "https://jvoight.github.io/articles/birch-descent-021420.pdf",
            "https://arxiv.org/pdf/1906.06772"]}
    BASE.with_suffix(".json").write_text(json.dumps(result, indent=2)+"\n")
    print(MARKER, "Prym dimension 24; torsor degree", 3**48,
          "; local root does not belong to F; cover automorphism group trivial", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    if args.worker:
        worker(); return
    result, receipt = BASE.with_suffix(".json"), Path(str(BASE)+"_job.json")
    if result.exists() or receipt.exists():
        assert result.exists() and receipt.exists()
        prior.checks.read_job(receipt, MARKER)
        prior.checks.verify_records(json.loads(result.read_text()))
        print(MARKER, "existing verified"); return
    cache = Path("/private/tmp/dembele_pointed_recognition_sage"); cache.mkdir(exist_ok=True)
    job = jobs.run_job([jobs.SAGE, "-python", str(Path(__file__)), "--worker"],
        BASE.with_suffix(".out"), 180, MARKER, env=dict(os.environ, DOT_SAGE=str(cache)))
    job["sources"].append(prior.checks.source(Path(__file__)))
    receipt.write_text(json.dumps(job, indent=2)+"\n")
    assert job["status"] == "pass", job["status"]
    record = json.loads(result.read_text()); record["sources"].append(prior.checks.source(receipt))
    result.write_text(json.dumps(record, indent=2)+"\n")
    print(MARKER, round(job["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

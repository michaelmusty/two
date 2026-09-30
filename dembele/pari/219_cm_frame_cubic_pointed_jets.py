"""Construct exact pointed jets and the special-fibre inputs for pointed normalization."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("pointed_jets_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
helpers, checks = prior.helpers, prior.checks


def pointed_stem(n, suffix=""):
    return DATA / f"cm_frame_cubic_pointed_{n}{suffix}"


def prepare_special_fibre():
    old_sections = DATA / "cm_frame_cubic_lift_sections.json"
    old_third = DATA / "cm_frame_cubic_lift_third.json"
    sr = json.loads(old_sections.read_text()); tr = json.loads(old_third.read_text())
    checks.verify_records(sr); checks.verify_records(tr)
    data = sr["data"].copy()
    def reduce(v): return [reduce(x) for x in v] if isinstance(v, list) else v % 31
    for key in ("odd_section_rows", "point_coordinates", "branch_plus_values", "branch_minus_values"):
        data[key] = reduce(data[key])
    data["odd_support_components"] = [[c[0], c[1], reduce(c[2]), c[3]] for c in data["odd_support_components"]]
    data["modulus"] = 31
    base = pointed_stem(1, "_sections"); mpath = base.with_suffix(".m")
    mpath.write_text(prior.binding("cubic_lift_", data))
    report = {"status": "pass", "sources": [checks.source(p) for p in (Path(__file__), old_sections)],
              "magma_artifact": checks.source(mpath), "data": data, "precision_digits": 1, "modulus": 31}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    def field_rows(rows): return [[x % 961 % 31+31*((x//961) % 31) for x in row] for row in rows]
    tdata = {"coordinates": field_rows(tr["candidate_coordinates"]), "delta_coordinates": field_rows(tr["delta_coordinates"])}
    base = pointed_stem(1, "_third"); mpath = base.with_suffix(".m")
    mpath.write_text(prior.binding("precision_third_", tdata))
    report = {"status": "pass", "sources": [checks.source(p) for p in (Path(__file__), old_third)],
              "magma_artifact": checks.source(mpath), "data": tdata, "precision_digits": 1, "modulus": 31}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")


def sections_base(n):
    if n == 1: return pointed_stem(1, "_sections")
    if n == 2: return DATA / "cm_frame_cubic_lift_sections"
    return prior.stem(n, "_sections")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(1, 2, 4, 8, 16, 32), required=True)
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args(); n = args.digits
    if n == 1: prepare_special_fibre()
    section = sections_base(n)
    checks.verify_records(json.loads(section.with_suffix(".json").read_text()))
    script = ROOT / "dembele/magma/218_cm_frame_cubic_pointed_jets.m"
    base = pointed_stem(n, "_jets")
    wrapper = f"precision_digits := {n};\n"+prior.loadline(section.with_suffix(".m"))
    job, jpath = prior.run(script, base, "PASS|218_CM_FRAME_CUBIC_POINTED_JETS",
        [Path(__file__), section.with_suffix(".json"), DATA / "cm_frame_cubic_pointed_gauge_probe_job.json"], wrapper, args.rebuild)
    output = Path(job["log"]["path"]).read_text()
    data = {key: helpers.field(output, "POINTED_"+key.upper()) for key in (
        "jet1_coefficients", "jet2_coefficients", "curve_jets", "jacobian_rows",
        "septic_monomials", "a_leading_weights", "trace_leading_weights")}
    mpath = base.with_suffix(".m"); mpath.write_text(prior.binding("pointed_", data))
    sources = [Path(__file__), jpath]
    if n > 1:
        previous = pointed_stem(n//2, "_jets").with_suffix(".json")
        old = json.loads(previous.read_text()); checks.verify_records(old); sources.append(previous)
        for key in ("jet1_coefficients", "jet2_coefficients", "curve_jets"):
            assert [[x % (31**(n//2)) for x in row] for row in data[key]] == old["data"][key]
        for key in ("a_leading_weights", "trace_leading_weights"):
            assert [x % (31**(n//2)) for x in data[key]] == old["data"][key]
        assert data["septic_monomials"] == old["data"]["septic_monomials"]
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in sources], "magma_artifact": checks.source(mpath),
              "data": data, "precision_digits": n, "modulus": 31**n,
              "local_parameter": "w", "divisor_jet_length": 80,
              "curve_jet_length": 244, "all_curve_equations_verified": True}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|219_CM_FRAME_CUBIC_POINTED_JETS", n, round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()

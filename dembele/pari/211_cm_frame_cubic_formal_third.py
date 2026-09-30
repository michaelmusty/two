"""Divide the formal-kernel residual by three with a short, checked scalar."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("formal_third_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
helpers, checks = prior.helpers, prior.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(4, 8, 16, 32), required=True)
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args(); n = args.digits
    divisor = prior.stem(n, "_formal_divisor"); sections = prior.stem(n, "_sections")
    for p in (divisor, sections): checks.verify_records(json.loads(p.with_suffix(".json").read_text()))
    formal_exponent = 31**(n-n//2); scalar = pow(3, -1, formal_exponent)
    assert scalar == (2*formal_exponent+1)//3
    chain = prior.prior.old.addflip_chain(scalar)
    chunk_size = 12 if n == 4 else 5
    saved_indices, saved_coordinates, delta = [], [], []
    chunk_jobs = []; script = ROOT / "dembele/magma/210_cm_frame_cubic_formal_third.m"
    for start in range(2, len(chain)+1, chunk_size):
        end = min(start+chunk_size-1, len(chain))
        keep = sorted({1, end} | {i for item in chain[end:] for i in item[1:] if 0 < i <= end})
        inputs = {"chain": chain, "chain_start": start, "chain_end": end,
                  "saved_indices": saved_indices, "saved_coordinates": saved_coordinates,
                  "saved_delta": delta, "keep_indices": keep}
        wrapper = f"precision_digits := {n};\n"+prior.loadline(sections.with_suffix(".m"))
        wrapper += prior.loadline(divisor.with_suffix(".m"))+prior.binding("formal_", inputs)
        base = prior.stem(n, f"_formal_third_{end:03d}")
        job, jpath = prior.run(script, base, "PASS|210_CM_FRAME_CUBIC_FORMAL_THIRD",
            prior.CORE+[Path(__file__), divisor.with_suffix(".json"), sections.with_suffix(".json")]+chunk_jobs[-1:], wrapper, args.rebuild)
        output = Path(job["log"]["path"]).read_text()
        saved_indices = helpers.field(output, "CHECKPOINT_INDICES")
        saved_coordinates = helpers.field(output, "CHECKPOINT_COORDINATES")
        delta = helpers.field(output, "CHECKPOINT_DELTA")
        assert saved_indices == keep; chunk_jobs.append(jpath)
        print("FORMAL_THIRD_CHUNK_PASS", n, start, end, round(job["wall_seconds"], 3), flush=True)
    assert "PASS|FORMAL_THIRD_RELATION_AND_SYMMETRIES" in output
    data = {"coordinates": helpers.field(output, "FORMAL_CORRECTED_COORDINATES"), "delta_coordinates": delta}
    base = prior.stem(n, "_formal_third"); mpath = base.with_suffix(".m")
    mpath.write_text(prior.binding("precision_third_", data))
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__), *chunk_jobs]],
              "magma_artifact": checks.source(mpath), "data": data, "precision_digits": n,
              "modulus": 31**n, "formal_kernel_exponent_bound": formal_exponent,
              "correction_scalar": scalar, "addflip_steps": len(chain)-1,
              "three_division_verified": True, "frobenius_fixed": True, "antiinvariant": True,
              "class_number_assumed": False}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|211_CM_FRAME_CUBIC_FORMAL_THIRD", n, scalar.bit_length(), "scalar bits")


if __name__ == "__main__":
    main()

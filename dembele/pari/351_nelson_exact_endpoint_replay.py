"""Replay the D91--D93 analytic chain with exact dyadic endpoint exports.

QQ(MPFR) chooses a simple rational, not necessarily the exact stored
float, and can move a directed endpoint inward.  Preserve the frozen
sources and outputs; replace only serialization in these new runs.
All dependencies between replayed stages use the corrected artifacts.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
from sage.all import QQ

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
STAGES = {
    "d91": ("333_nelson_interval_sum.py", "nelson_interval_sum_d91.json"),
    "norm_one": ("341_nelson_norm_one_sum.py", "nelson_norm_one_sum_d92_T25600.json"),
    "norm_one_tail": ("342_nelson_norm_one_packing_tail.py", "nelson_norm_one_packing_tail_d92.json"),
    "prime31": ("347_nelson_prime31_sum.py", "nelson_prime31_sum_d93.json"),
    "all_ideals": ("348_nelson_all_ideal_bounds.py", "nelson_all_ideal_bounds_d93.json"),
}
REPLACEMENTS = {name: name[:-5] + "_exact_d93.json" for _, name in STAGES.values()}


class DataOverlay:
    def __truediv__(self, name):
        return DATA / REPLACEMENTS.get(str(name), str(name))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=STAGES, required=True)
    args = parser.parse_args()
    script, old_name = STAGES[args.stage]
    path = Path(__file__).with_name(script)
    spec = importlib.util.spec_from_file_location("replayed_stage", path)
    stage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stage)
    modules = [stage]
    for module in modules:
        for name in ["norm_one", "kernel"]:
            child = getattr(module, name, None)
            if child is not None and child not in modules:
                modules.append(child)
    kernel = next(module for module in modules if hasattr(module, "PRECISION"))
    counts = {"exports": 0, "old_lower_moved_inward": 0, "old_upper_moved_inward": 0,
              "imports_checked": 0}

    def interval(value):
        low_float, high_float = value.lower(), value.upper()
        lo, hi = low_float.exact_rational(), high_float.exact_rational()
        assert lo <= hi
        counts["exports"] += 1
        counts["old_lower_moved_inward"] += int(QQ(low_float) > lo)
        counts["old_upper_moved_inward"] += int(QQ(high_float) < hi)
        return {"lower": str(lo), "upper": str(hi), "display": str(value)}

    def get_ball(row):
        lo, hi = QQ(row["lower"]), QQ(row["upper"])
        value = kernel.RB((lo + hi) / 2).add_error((hi - lo) / 2)
        assert value.lower().exact_rational() <= lo <= hi <= value.upper().exact_rational()
        counts["imports_checked"] += 1
        return value

    # A concrete regression control: the old QQ conversion moves both
    # endpoints of this pi ball inward on the installed Sage version.
    pi = kernel.RB.pi()
    lo, hi = pi.lower().exact_rational(), pi.upper().exact_rational()
    assert QQ(pi.lower()) > lo and QQ(pi.upper()) < hi
    control = {"exact_lower": str(lo), "exact_upper": str(hi),
               "old_lower": str(QQ(pi.lower())), "old_upper": str(QQ(pi.upper()))}
    for module in modules:
        module.DATA = DataOverlay()
        if hasattr(module, "interval"):
            module.interval = interval
        if hasattr(module, "get_ball"):
            module.get_ball = get_ball
    output = DATA / REPLACEMENTS[old_name]
    assert not output.exists()
    sys.argv = [str(path)]
    stage.main()
    result = json.loads(output.read_text())
    result["endpoint_replay"] = {
        "stage": args.stage, "method": "MPFR lower/upper().exact_rational()",
        "original_artifact": str((DATA / old_name).relative_to(ROOT)),
        "original_QQ_conversion_is_not_outward": True,
        "pi_regression_control": control, "counts": counts,
    }
    result["sources"].extend([kernel.source(Path(__file__)), kernel.source(DATA / old_name)])
    output.write_text(json.dumps(result, indent=2) + "\n")
    print("PASS|351_nelson_exact_endpoint_replay", args.stage, counts, flush=True)


if __name__ == "__main__":
    main()

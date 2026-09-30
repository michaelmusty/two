# D85 precision adapter; original SHA256 28b24c205179dc6ee8dd221dfbe923f1712c8d953d97168c1fc35d53cb650133
"""D85: construct the adjoint move directly from the certified class matrix.

Only the class representative is needed, so this construction can run
while the separate pointed function checker verifies its equation.
The final adjoint checker still binds the completed geometry certificate.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("adjoint128_move_staged", ROOT / "dembele/pari/d85_128_262_cm_frame_cubic_staged_functions.py")
staged = importlib.util.module_from_spec(spec); spec.loader.exec_module(staged)
prior, checks = staged.prior, staged.checks


def inputs_and_wrapper():
    paths = [DATA / name for name in ("cm_frame_cubic_precision_128_sections.json",
        "cm_frame_cubic_pointed_128_jets.json", "cm_frame_cubic_pointed_128_newton_third.json",
        "cm_frame_cubic_pointed_64_check.json", "cm_frame_cubic_gauge.json")]
    records = [json.loads(p.read_text()) for p in paths]
    for record in records: checks.verify_records(record)
    cls = records[2]
    assert cls["actual_divisor_verified"] and cls["three_division_verified"]
    assert cls["frobenius_fixed"] and cls["antiinvariant"]
    coordinates = cls["data"]["coordinates"]
    assert all(0 <= x < 31**128 for row in coordinates for x in row)
    wrapper = "precision_digits := 128;\n"+"".join(prior.loadline(p.with_suffix(".m")) for p in paths[:3])
    wrapper += prior.binding("pointed_cubic_", {"descended_divisor_coordinates": coordinates})
    paths += [Path(__file__), ROOT / "dembele/magma/170_cm_frame_cover_class_arithmetic.m",
              ROOT / "dembele/magma/227_cm_frame_cubic_pointed_class_chart.m"]
    return paths, wrapper


def main():
    paths, wrapper = inputs_and_wrapper()
    original, script = staged.generated("adjoint", "first")
    base = DATA / "cm_frame_cubic_adjoint_128_function_checkpoint"
    job, jpath = prior.run(script, base, "PASS|262_ADJOINT_FIRST",
        prior.CORE+[Path(staged.__file__), original]+paths, wrapper, False)
    output = Path(job["log"]["path"]).read_text()
    data = {key: prior.helpers.field(output, "CHECKPOINT_"+key.upper()) for key in staged.ADJOINT_SAVED}
    staged.save(base, data, "checkpoint_", [Path(__file__), jpath], function_checkpoint_only=True,
        input_class_independently_verified=True, independent_final_model_check_completed=False)
    print("PASS|269_CM_FRAME_CUBIC_ADJOINT128_MOVE", round(job["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

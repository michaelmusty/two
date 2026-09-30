"""Test a lower-degree output model using the unique K_X+2P representative."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("adjoint_probe_prior", ROOT / "dembele/pari/221_cm_frame_cubic_pointed_function.py")
build = importlib.util.module_from_spec(spec); spec.loader.exec_module(build)
prior, checks = build.prior, build.checks


def main():
    paths, wrapper, previous = build.inputs_and_wrapper(1)
    root = DATA / "cm_frame_cubic_pointed_1_check.json"; checks.verify_records(json.loads(root.read_text()))
    wrapper += prior.loadline(DATA / "cm_frame_cubic_pointed_1.m")
    base = DATA / "cm_frame_cubic_adjoint_probe"
    script = ROOT / "dembele/magma/249_cm_frame_cubic_adjoint_probe.m"
    job, jpath = prior.run(script, base, "PASS|249_CM_FRAME_CUBIC_ADJOINT_PROBE",
        prior.CORE+[Path(__file__), Path(build.__file__), ROOT / "dembele/magma/227_cm_frame_cubic_pointed_class_chart.m", root]+paths, wrapper, False)
    output = Path(job["log"]["path"]).read_text()
    names = ("divisor_coordinates", "move_g_coefficients", "move_r_coefficients", "fixed_space_coordinates",
             "q_coefficients", "u_coefficients", "f_coefficients", "norm_scalar", "scaling_scalar",
             "a_quadratic_coefficients", "trace_quartic_coefficients")
    data = {key: prior.helpers.field(output, "ADJOINT_"+key.upper()) for key in names}
    mpath = base.with_suffix(".m"); mpath.write_text(prior.binding("adjoint_", data))
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in (Path(__file__), jpath)],
              "magma_artifact": checks.source(mpath), "data": data, "precision_digits": 1,
              "fixed_divisor": "K_X+2P = pi*div(X16)+R_ram+2P", "fixed_divisor_degree": 80,
              "fixed_vanishing_space_dimension": 121, "unique_intersection_dimension": 1,
              "equation": "ell*T^3 - 3*A2*ell*T - R4 = 0; weight(T)=1",
              "normalized_local_leading_coefficients": {"a_w6": 3, "h_w9": "3*sqrt(-3)"},
              "same_class_verified": True, "independent_equation_verification_completed": False,
              "characteristic_zero_cubic_constructed": False}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|250_CM_FRAME_CUBIC_ADJOINT_PROBE", round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()

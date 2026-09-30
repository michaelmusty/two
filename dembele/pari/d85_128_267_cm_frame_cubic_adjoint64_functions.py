# D85 precision adapter; original SHA256 7c65b6aaeac565c377359967acbb67082ee479ad7d869fb0e0dbcd00c06bc461
"""D85: recover the adjoint u-line, then f and the coefficients in bounded jobs."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("adjoint128_staged", ROOT / "dembele/pari/d85_128_262_cm_frame_cubic_staged_functions.py")
staged = importlib.util.module_from_spec(spec); spec.loader.exec_module(staged)
prior, checks, build = staged.prior, staged.checks, staged.adjoint
spec = importlib.util.spec_from_file_location("adjoint128_move_inputs", ROOT / "dembele/pari/d85_128_269_cm_frame_cubic_adjoint64_move.py")
move = importlib.util.module_from_spec(spec); spec.loader.exec_module(move)


def main():
    paths, wrapper = move.inputs_and_wrapper()
    first = DATA / "cm_frame_cubic_adjoint_128_function_checkpoint.json"
    checks.verify_records(json.loads(first.read_text()))
    wrapper += prior.loadline(first.with_suffix(".m"))
    original, generated = staged.generated("adjoint", "last")
    text = generated.read_text()
    old = "tripleVanishing:=RQuotient(RG2,cubeSpace,RG4,81);\nuline:=RIntersection(tripleVanishing,WB4,1);"
    assert text.count(old) == 1
    text = text.replace(old, "ok,uline:=RDegreeZero(RG2,cubeSpace,WB4); assert ok;")
    first_text, remaining = text.split("normSpace:=", 1)
    fields = dict(staged.ADJOINT_SAVED, u_coefficients="BaseCoefficients(ucoeff)[1]")
    for key, expr in fields.items():
        first_text += f'printf "FUNCTION_{key.upper()}|%o\\n",{expr};\n'
    first_text += 'printf "CPU_SECONDS|%o\\n",Cputime(started);\nprint "PASS|267_ADJOINT_U_LINE";quit;\n'
    script = ROOT / "dembele/magma/d85_128_adjoint_u_line.m"
    if script.exists(): assert script.read_text() == first_text
    else: script.write_text(first_text)
    base = DATA / "cm_frame_cubic_adjoint_128_u_checkpoint"
    inputs = prior.CORE+[Path(__file__), Path(staged.__file__), Path(build.__file__),
        Path(build.build.__file__), original, generated, first]+paths
    job, jpath = prior.run(script, base, "PASS|267_ADJOINT_U_LINE", inputs, wrapper, False)
    output = Path(job["log"]["path"]).read_text()
    data = {key: prior.helpers.field(output, "FUNCTION_"+key.upper()) for key in fields}
    staged.save(base, data, "function_", [Path(__file__), jpath], function_checkpoint_only=True)
    print("ADJOINT128_U_RECOVERED", round(job["wall_seconds"], 3), flush=True)
    wrapper += prior.loadline(base.with_suffix(".m")); inputs.append(base.with_suffix(".json"))
    second_text = '''SetQuitOnError(true); SetColumns(0); SetSeed(83267); started:=Cputime();
load "dembele/magma/199_cm_frame_cubic_precision_model.m";
load "dembele/magma/227_cm_frame_cubic_pointed_class_chart.m";
root:=ZZ!11; rootdigits:=1;
while rootdigits lt precision_digits do root-:=(root^2+3)*(2*root)^-1; rootdigits*:=2; end while;
assert root^2 eq -3;
WRcoords:=RBase(Matrix(ZZ,function_divisor_coordinates)); WR:=RMultiply(WRcoords,RG2);
gc:=RBaseRow(function_move_g_coefficients); rc:=RBaseRow(function_move_r_coefficients);
UHc:=RBase(Matrix(ZZ,function_fixed_space_coordinates));
qcoeff:=RBaseRow(function_q_coefficients); q:=RMultiply(qcoeff,RG1);
ucoeff:=RBaseRow(function_u_coefficients); u:=RMultiply(ucoeff,RG4);
cubeSpace:=RProduct(RProduct(WR,WR,201),WR,321);
normSpace:=''' + remaining.replace("PASS|262_ADJOINT_LAST", "PASS|267_ADJOINT_F_AND_COEFFICIENTS")
    script = ROOT / "dembele/magma/d85_128_adjoint_f_and_coefficients.m"
    if script.exists(): assert script.read_text() == second_text
    else: script.write_text(second_text)
    job, jpath = prior.run(script, DATA / "cm_frame_cubic_adjoint_128_f_coefficients",
                          "PASS|267_ADJOINT_F_AND_COEFFICIENTS", inputs, wrapper, False)
    output = Path(job["log"]["path"]).read_text()
    data = {key: prior.helpers.field(output, "ADJOINT_"+key.upper()) for key in build.NAMES}
    previous = DATA / "cm_frame_cubic_adjoint_64.json"
    old = json.loads(previous.read_text()); checks.verify_records(old)
    for key in build.CORE:
        assert build.build.reduced(data[key], 31**64) == old["data"][key], key
    staged.save(DATA / "cm_frame_cubic_adjoint_128", data, "adjoint_", [Path(__file__), jpath, previous],
        route="checkpointed adjoint move and direct degree-zero u search",
        fixed_divisor="K_X+2P", fixed_divisor_degree=80,
        equation="ell*T^3 - 3*A2*ell*T - R4 = 0; weight(T)=1",
        coefficientwise_reduction_verified=True, characteristic_zero_cubic_constructed=False,
        target_field_constructed=False)
    print("PASS|267_CM_FRAME_CUBIC_ADJOINT128_FUNCTIONS", round(job["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

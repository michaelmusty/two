"""D83: recover u directly in its required subspace, then recover f separately.

The old search first found an 81-dimensional quotient inside RG4 and
intersected it with WB4. Search the final degree-zero line inside WB4
directly. RDegreeZero verifies the entire RG2 inclusion, and the saved
functions are subsequently checked independently by script 242.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("pointed64_staged", ROOT / "dembele/pari/262_cm_frame_cubic_staged_functions.py")
staged = importlib.util.module_from_spec(spec); spec.loader.exec_module(staged)
prior, checks, build = staged.prior, staged.checks, staged.pointed


def write_script(name, text, original):
    path = ROOT / "dembele/magma" / name
    text = "// D83 split and restricted search; original SHA256 " + hashlib.sha256(original.read_bytes()).hexdigest()+"\n"+text
    if path.exists(): assert path.read_text() == text
    else: path.write_text(text)
    return path


def output_fields(fields, marker):
    text = ""
    for key, expr in fields.items(): text += f'printf "CHECKPOINT_{key.upper()}|%o\\n",{expr};\n'
    return text + f'printf "CPU_SECONDS|%o\\n",Cputime(started);\nprint "{marker}";quit;\n'


def main():
    paths, wrapper, previous = build.inputs_and_wrapper(64)
    original = ROOT / "dembele/magma/240_cm_frame_cubic_pointed_direct_function.m"
    text = original.read_text()
    first, rest = text.split("normSpace:=", 1)
    old = "tripleVanishing:=RQuotient(RG2,cubeSpace,RG4,81);\nuline:=RIntersection(tripleVanishing,WB4,1);"
    assert first.count(old) == 1
    first = first.replace(old, "ok,uline:=RDegreeZero(RG2,cubeSpace,WB4); assert ok;")
    fields = {key: value for key, value in staged.POINTED_SAVED.items() if key not in ("f_coefficients", "norm_scalar")}
    first += output_fields(fields, "PASS|266_POINTED_U_SEARCH")
    script = write_script("d83_64_pointed_u_search.m", first, original)
    inputs = prior.CORE+[Path(__file__), Path(staged.__file__), Path(build.__file__),
                         Path(build.old.__file__), original]+paths
    base = DATA / "cm_frame_cubic_pointed_64_u_checkpoint"
    job, jpath = prior.run(script, base, "PASS|266_POINTED_U_SEARCH", inputs, wrapper, False)
    output = Path(job["log"]["path"]).read_text()
    data = {key: prior.helpers.field(output, "CHECKPOINT_"+key.upper()) for key in fields}
    staged.save(base, data, "checkpoint_", [Path(__file__), jpath], function_checkpoint_only=True)
    print("POINTED64_U_RECOVERED", round(job["wall_seconds"], 3), flush=True)
    second = '''SetQuitOnError(true); SetColumns(0); SetSeed(83266); started:=Cputime();
load "dembele/magma/199_cm_frame_cubic_precision_model.m";
WRcoords:=RBase(Matrix(ZZ,checkpoint_descended_divisor_coordinates));
WR:=RMultiply(WRcoords,RG2);
qcoeff:=RBaseRow(checkpoint_q_coefficients); q:=RMultiply(qcoeff,RG1);
ucoeff:=RBaseRow(checkpoint_u_coefficients); u:=RMultiply(ucoeff,RG4);
cubeSpace:=RProduct(RProduct(WR,WR,201),WR,321);
normSpace:=''' + rest.split("xs:=[pt[1..16]", 1)[0]
    second += output_fields(staged.POINTED_SAVED, "PASS|266_POINTED_F_AND_NORM")
    script = write_script("d83_64_pointed_f_and_norm.m", second, original)
    wrapper += prior.loadline(base.with_suffix(".m")); inputs.append(base.with_suffix(".json"))
    jobbase = DATA / "cm_frame_cubic_pointed_64_f_checkpoint"
    job, jpath = prior.run(script, jobbase, "PASS|266_POINTED_F_AND_NORM", inputs, wrapper, False)
    output = Path(job["log"]["path"]).read_text()
    data = {key: prior.helpers.field(output, "CHECKPOINT_"+key.upper()) for key in staged.POINTED_SAVED}
    final = DATA / "cm_frame_cubic_pointed_64_function_checkpoint"
    staged.save(final, data, "checkpoint_", [Path(__file__), jpath], function_checkpoint_only=True)
    print("POINTED64_F_AND_NORM_RECOVERED", round(job["wall_seconds"], 3), flush=True)
    print("PASS|266_CM_FRAME_CUBIC_POINTED64_FUNCTIONS", flush=True)


if __name__ == "__main__":
    main()

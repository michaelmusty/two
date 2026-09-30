"""D83: checkpoint function construction to retain the 180-second job bound.

The pointed constructor is split after recovering its functions and norm;
the adjoint constructor is split after its actual divisor move. Generated
Magma sources contain the corresponding unchanged portions of 240/249.
Final coefficients must reduce to the complete verified 32-digit arrays.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "dembele/pari" / filename)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


pointed = module("staged_pointed", "241_cm_frame_cubic_pointed_direct_function.py")
adjoint = module("staged_adjoint", "253_cm_frame_cubic_adjoint_lift.py")
prior, checks = pointed.prior, pointed.checks
POINTED_SAVED = {
    "descended_divisor_coordinates": "BaseCoefficients(WRcoords)",
    "q_coefficients": "BaseCoefficients(qcoeff)[1]",
    "u_coefficients": "BaseCoefficients(ucoeff)[1]",
    "f_coefficients": "BaseCoefficients(fcoeff)[1]",
    "norm_scalar": "Integers()!c[1][1,1]",
}
ADJOINT_SAVED = {
    "divisor_coordinates": "BaseCoefficients(WRcoords)",
    "move_g_coefficients": "BaseCoefficients(gc)[1]",
    "move_r_coefficients": "BaseCoefficients(rc)[1]",
    "fixed_space_coordinates": "BaseCoefficients(UHc)",
    "q_coefficients": "BaseCoefficients(qcoeff)[1]",
}


def generated(family, phase):
    name = "240_cm_frame_cubic_pointed_direct_function.m" if family == "pointed" else "249_cm_frame_cubic_adjoint_probe.m"
    source = ROOT / "dembele/magma" / name
    original = source.read_text()
    prefix = "// D83 checkpoint split of " + name + "; SHA256 " + hashlib.sha256(source.read_bytes()).hexdigest() + "\n"
    if family == "pointed":
        before, after = original.split("xs:=[pt[1..16]:pt in liftpts[1..1024]];", 1)
        if phase == "first":
            body = before
            fields = POINTED_SAVED
        else:
            body = '''SetQuitOnError(true); SetColumns(0); SetSeed(83262); started:=Cputime();
load "dembele/magma/199_cm_frame_cubic_precision_model.m";
WRcoords:=RBase(Matrix(ZZ,checkpoint_descended_divisor_coordinates));
qcoeff:=RBaseRow(checkpoint_q_coefficients); q:=RMultiply(qcoeff,RG1);
ucoeff:=RBaseRow(checkpoint_u_coefficients); u:=RMultiply(ucoeff,RG4);
fcoeff:=RBaseRow(checkpoint_f_coefficients); f:=RMultiply(fcoeff,RG2);
c:=RBaseRow([checkpoint_norm_scalar]); ut:=RTau(u,tt); qt:=RTau(q,tt);
xs:=[pt[1..16]:pt in liftpts[1..1024]];
''' + after.replace("PASS|240_CM_FRAME_CUBIC_POINTED_DIRECT_FUNCTION", "PASS|262_POINTED_LAST")
    else:
        before, after = original.split("cubeSpace:=", 1)
        if phase == "first":
            body = before
            fields = ADJOINT_SAVED
        else:
            setup = before.split("// H =", 1)[0]
            body = setup + '''load "dembele/magma/227_cm_frame_cubic_pointed_class_chart.m";
WRcoords:=RBase(Matrix(ZZ,checkpoint_divisor_coordinates));
WR:=RMultiply(WRcoords,RG2);
gc:=RBaseRow(checkpoint_move_g_coefficients);
rc:=RBaseRow(checkpoint_move_r_coefficients);
UHc:=RBase(Matrix(ZZ,checkpoint_fixed_space_coordinates));
assert qcoeff eq RBaseRow(checkpoint_q_coefficients);
cubeSpace:=''' + after.replace("PASS|249_CM_FRAME_CUBIC_ADJOINT_PROBE", "PASS|262_ADJOINT_LAST")
    if phase == "first":
        for key, expr in fields.items():
            body += f'printf "CHECKPOINT_{key.upper()}|%o\\n",{expr};\n'
        body += f'printf "CPU_SECONDS|%o\\n",Cputime(started);\nprint "PASS|262_{family.upper()}_FIRST";quit;\n'
    target = ROOT / "dembele/magma" / f"d83_64_{family}_{phase}.m"
    text = prefix + body
    if target.exists(): assert target.read_text() == text
    else: target.write_text(text)
    return source, target


def save(base, data, prefix, paths, **extra):
    artifact = base.with_suffix(".m")
    artifact.write_text(prior.binding(prefix, data))
    report = {"status": "pass", "milestone": "D83", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__)]+paths],
              "magma_artifact": checks.source(artifact), "precision_digits": 64,
              "modulus": 31**64, "data": data, **extra}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", choices=("pointed", "adjoint"), required=True)
    parser.add_argument("--stage", choices=("first", "last", "all"), default="all")
    args = parser.parse_args(); family = args.family
    build = pointed if family == "pointed" else adjoint
    values = build.inputs_and_wrapper(64)
    paths, wrapper = values[:2]
    stem = DATA / f"cm_frame_cubic_{family}_64"
    first = Path(str(stem)+"_function_checkpoint")
    paths += [Path(build.__file__)]
    if family == "pointed": paths += [Path(build.old.__file__), Path(build.jets.__file__)]
    else: paths += [Path(build.build.__file__)]
    if args.stage in ("first", "all"):
        source, script = generated(family, "first")
        job, jpath = prior.run(script, first, f"PASS|262_{family.upper()}_FIRST",
                              prior.CORE+[Path(__file__), source]+paths, wrapper, False)
        output = Path(job["log"]["path"]).read_text()
        names = POINTED_SAVED if family == "pointed" else ADJOINT_SAVED
        data = {key: prior.helpers.field(output, "CHECKPOINT_"+key.upper()) for key in names}
        save(first, data, "checkpoint_", [jpath], function_checkpoint_only=True)
        print("STAGED_FUNCTION_FIRST_PASS", family, round(job["wall_seconds"], 3), flush=True)
    if args.stage in ("last", "all"):
        checkpoint = first.with_suffix(".json")
        checks.verify_records(json.loads(checkpoint.read_text()))
        wrapper += prior.loadline(first.with_suffix(".m"))
        source, script = generated(family, "last")
        base = Path(str(stem)+"_function_finish")
        job, jpath = prior.run(script, base, f"PASS|262_{family.upper()}_LAST",
                              prior.CORE+[Path(__file__), source, checkpoint]+paths, wrapper, False)
        output = Path(job["log"]["path"]).read_text()
        names = pointed.old.CORE_NAMES if family == "pointed" else adjoint.NAMES
        data = {key: prior.helpers.field(output, family.upper()+"_"+key.upper()) for key in names}
        previous = DATA / f"cm_frame_cubic_{family}_32.json"
        old = json.loads(previous.read_text()); checks.verify_records(old)
        core = names if family == "pointed" else adjoint.CORE
        for key in core: assert pointed.old.reduced(data[key], 31**32) == old["data"][key], key
        final = Path(str(stem)+"_direct") if family == "pointed" else stem
        save(final, data, "pointed_cubic_" if family == "pointed" else "adjoint_", [jpath, previous],
             route="checkpointed function construction", coefficientwise_reduction_verified=True,
             characteristic_zero_cubic_constructed=False, target_field_constructed=False)
        print("STAGED_FUNCTION_LAST_PASS", family, round(job["wall_seconds"], 3), flush=True)
    print("PASS|262_STAGED_FUNCTION_CONSTRUCTION", family, args.stage, flush=True)


if __name__ == "__main__":
    main()

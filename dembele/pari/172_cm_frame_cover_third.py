"""D78: try a Hecke-suggested scalar, but certify its actual class relation.

The suggested Prym order is only a search aid. No class-number statement
is made from it; the resulting residual is tested by exact arithmetic.
"""
import argparse
import ast
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


helpers = module("third_helpers", ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")
jobs = module("third_jobs", ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")
checks = helpers.checks


def integer_value(expression, z):
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.Name) and node.id == "z":
            return z
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -visit(node.operand)
        if isinstance(node, ast.BinOp):
            a, b = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add): return a+b
            if isinstance(node.op, ast.Sub): return a-b
            if isinstance(node.op, ast.Mult): return a*b
            if isinstance(node.op, ast.Pow) and 0 <= b <= 40: return a**b
        raise ValueError("unexpected Hecke polynomial syntax")
    return visit(ast.parse(expression.replace("^", "**"), mode="eval").body)


def addflip_chain(n):
    chain = [[1, 0, 0], [-1, 1, 0]]
    cache = {1: 1, -1: 2}
    def rec(value):
        if value in cache:
            return cache[value]
        if value % 2 == 0:
            left = right = rec(-value//2)
        else:
            b = -1 if value % 4 == 1 else 1
            left, right = rec(-value-b), cache[b]
        assert value == -chain[left-1][0]-chain[right-1][0]
        chain.append([value, left, right])
        cache[value] = len(chain)
        return len(chain)
    rec(n)
    assert chain[-1][0] == n
    return chain


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collect-only", action="store_true")
    args = parser.parse_args()
    result_path = DATA / "cm_frame_cover_third.json"
    if args.collect_only:
        report = json.loads(result_path.read_text())
        checks.verify_records(report)
        print("PASS|172_CM_FRAME_COVER_THIRD_PROVENANCE", report["three_division_computed"])
        return
    class_job = DATA / "cm_frame_cover_class_check_job.json"
    previous = checks.read_job(class_job, "PASS|171_CM_FRAME_COVER_CLASS_CHECK")
    output = Path(previous["log"]["path"]).read_text()
    delta = helpers.field(output, "DELTA_SECTION_ROWS")
    bank = DATA / "levelraise_p2k_charpolys.m"
    p40 = bank.read_text().splitlines()[3].strip().rstrip(",")
    assert p40.startswith("z^40")
    N40 = integer_value(p40, 32)
    base_path = DATA / "cm_frame_curve_verification.json"
    base = json.loads(base_path.read_text())
    checks.verify_records(base)
    p16 = base["Hecke_trace_polynomial_coefficients_ascending"]
    N16 = sum(c*32**i for i, c in enumerate(p16))
    assert N40 % N16 == 0
    Nprym = N40//N16
    m, exponent = Nprym, 0
    while m % 3 == 0:
        m //= 3
        exponent += 1
    scalar = (-pow(3, -1, m)) % m
    chain = addflip_chain(scalar)
    ipath = DATA / "cm_frame_cover_third_input.m"
    inputs = {"delta_rows": delta, "scalar": scalar, "chain": chain,
              "heuristic_prym_order": Nprym, "cofactor": m, "three_valuation": exponent}
    ipath.write_text("// D78: proposed scalar; its class relation must be checked.\n"+
                     "\n".join(f"third_{key} := {helpers.magma(value)};"
                               for key, value in inputs.items())+"\n")
    script = ROOT / "dembele/magma/173_cm_frame_cover_third.m"
    job = jobs.run_job(jobs.magma_command(script), DATA / "cm_frame_cover_third.out", 180,
                       "PASS|173_CM_FRAME_COVER_THIRD")
    job["sources"] = [checks.source(p) for p in (__file__, script, ipath, class_job, bank, base_path,
                      ROOT / "dembele/magma/170_cm_frame_cover_class_arithmetic.m",
                      DATA / "cm_frame_cover_makdisi.m", ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
    jpath = DATA / "cm_frame_cover_third_job.json"
    jpath.write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass":
        raise RuntimeError(f"class scalar computation: {job['status']}")
    output = Path(job["log"]["path"]).read_text()
    def bool_field(label):
        return helpers.field(output.replace("|true", "|True").replace("|false", "|False"), label)
    success = bool_field("THREE_DIVISION_VERIFIED")
    report = {"status": "pass", "milestone": "D78", "date": "2026-09-21",
              "sources": [checks.source(p) for p in (__file__, jpath)],
              "heuristic_prym_order": Nprym, "heuristic_three_valuation": exponent,
              "heuristic_coprime_cofactor": m, "proposed_scalar": scalar,
              "class_number_certified": False, "addflip_chain_steps": len(chain)-1,
              "three_division_computed": success,
              "residual_killed_by_three": bool_field("RESIDUAL_KILLED_BY_THREE"),
              "residual_killed_by_nine": bool_field("RESIDUAL_KILLED_BY_NINE"),
              "candidate_rows": helpers.field(output, "CANDIDATE_SECTION_ROWS"),
              "residual_rows": helpers.field(output, "RESIDUAL_SECTION_ROWS"),
              "residual_class": "3*c*Delta+Delta=2*m*Delta",
              "cyclic_cubic_constructed": False}
    result_path.write_text(json.dumps(report, indent=2)+"\n")
    print("THREE_DIVISION_COMPUTED", success, "RESIDUAL_KILLED_BY_THREE", report["residual_killed_by_three"])
    print("PASS|172_CM_FRAME_COVER_THIRD")


if __name__ == "__main__":
    main()

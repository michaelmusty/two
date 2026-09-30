"""D74: saturated integral basis of H0(2K-T), then Q/F recognition tests.

The exact complementary divisor T is defined by D73's rational numerator.
Magma script 134 exports its dimension-17 multiplication-kernel description.
All reduced sections retain paired witnesses r*d=n*s on the curve.
"""
import importlib.util
import ast
import json
from pathlib import Path
import re
import time

from sage.all import QQ, ZZ, GF, Zmod, PolynomialRing, matrix, vector, gcd, lcm, identity_matrix

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


checks = module("check_helpers", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")
rec = module("recognition_helpers", ROOT / "dembele/pari/132_cm_frame_denominator_recognition.py")
projective = module("projection_helpers", ROOT / "dembele/pari/133_cm_frame_projective_denominator.py")
source = checks.source


def primitive(row):
    denominator = lcm([x.denominator() for x in row])
    row = [ZZ(c*denominator) for c in row]
    content = gcd(row)
    return [c//content for c in row]


def main():
    started = time.monotonic()
    job_path = DATA / "cm_frame_denominator_space_job.json"
    checks.read_job(job_path, "PASS|134_CM_FRAME_DENOMINATOR_SPACE")
    output = (DATA / "cm_frame_denominator_space.out").read_text()
    raw = re.search(r"^PAIRED_BASIS_RATIONAL_STRINGS\|(.*?)(?=^SECOND_NUMERATOR\|)",
                    output, re.M | re.S).group(1)
    # Magma %o prints Sprint strings without quotes; quote rational tokens
    # before literal parsing, never evaluate the exported text as code.
    parsed = ast.literal_eval(re.sub(r"(-?\d+/\d+)", r"'\1'", raw.strip()))
    paired = matrix(QQ, [[QQ(c) for c in row] for row in parsed])
    assert paired.nrows() == 17 and paired.ncols() == 90
    curve = json.loads((DATA / "cm_frame_curve_candidate.json").read_text())
    pair = json.loads((DATA / "cm_frame_doubling_normalized_128.json").read_text())
    chart = pair["section_chart_indices_zero_based"]
    projection = projective.section_projection(curve, chart)
    denominators = paired.matrix_from_columns(list(range(45)))
    witnesses = paired.matrix_from_columns(list(range(45, 90)))
    ambient = matrix(QQ, 17, 136)
    for i in range(17):
        for j, col in enumerate(chart):
            ambient[i, col] = denominators[i, j]
    # The exported basis already has an identity pivot block. Eliminate
    # those 17 coordinates directly instead of recomputing a large
    # rational nullspace with 1322-digit coefficients (a bounded timeout).
    assert denominators.matrix_from_columns(list(range(17))) == identity_matrix(QQ, 17)
    constraints = (projection.matrix_from_columns(list(range(17, 45)))
                   -projection.matrix_from_columns(list(range(17)))
                    *denominators.matrix_from_columns(list(range(17, 45)))).transpose()
    assert constraints.matrix_from_columns(chart[17:]) == identity_matrix(QQ, 28)
    assert constraints*ambient.transpose() == 0
    assert constraints*matrix(QQ, curve["quadrics"]).transpose() == 0
    print("EXACT_DENOMINATOR_SPACE", 17, round(time.monotonic()-started, 3), flush=True)
    integral = matrix(ZZ, [primitive(row) for row in constraints])
    lattice = integral.right_kernel_matrix(algorithm="pari", basis="LLL")
    assert lattice.nrows() == 108 and integral*lattice.transpose() == 0
    smith = lattice.elementary_divisors()
    assert smith == [1]*108
    images = lattice.change_ring(QQ)*projection
    sections = matrix(ZZ, [row for row, image in zip(lattice, images) if image])
    assert sections.nrows() == 17
    section_images = sections.change_ring(QQ)*projection
    assert section_images.change_ring(GF(31)).rank() == 17
    heights = [len(str(max(abs(c) for c in row))) for row in sections]
    print("REDUCED_SECTION_HEIGHT_DIGITS", heights, round(time.monotonic()-started, 3), flush=True)
    # Retain exact paired witnesses for an independent polynomial check.
    pivots = list(denominators.pivots())
    coordinates = section_images.matrix_from_columns(pivots)*denominators.matrix_from_columns(pivots).inverse()
    assert coordinates*denominators == section_images
    witness_images = coordinates*witnesses
    witness_rows = []
    for row in witness_images:
        full = [QQ(0)]*136
        for j, col in enumerate(chart):
            full[col] = row[j]
        witness_rows.append(full)
    data_m = DATA / "cm_frame_denominator_space_reduced.m"
    data_m.write_text("// D74 exact reduced sections and paired multiplication witnesses.\n"
                      +"space_second_numerator := "+str(checks.field(output, "SECOND_NUMERATOR"))+";\n"
                      +"space_section_rows := "+str([[int(x) for x in row] for row in sections])+";\n"
                      +"space_witness_rows := ["+",\n".join("["+",".join(str(c) for c in row)+"]"
                                                               for row in witness_rows)+"];\n")
    pivots = list(section_images.change_ring(GF(31)).pivots())
    assert len(pivots) == 17
    coefficients = {}
    for digits in (32, 64, 128):
        stage = json.loads((DATA / f"cm_frame_doubling_normalized_{digits}.json").read_text())
        Z = Zmod(31**digits)
        images_mod = section_images.change_ring(Z)
        target = vector(Z, [stage["denominator_coefficients"][j] for j in chart])
        cs = vector(Z, [target[j] for j in pivots])*images_mod.matrix_from_columns(pivots).inverse()
        assert cs*images_mod == target
        coefficients[digits] = [int(x) for x in cs]
        if digits > 32:
            assert [c % (31**(digits//2)) for c in coefficients[digits]] == coefficients[digits//2]
    T = PolynomialRing(ZZ, "t")
    f = T([2, 0, -16, 0, 20, 0, -8, 0, 1])
    roots31 = sorted(int(r) for r, e in f.change_ring(GF(31)).roots() if e == 1)
    roots = [rec.hensel_root(f, r, 128) for r in roots31]
    anchor = next(i for i, c in enumerate(coefficients[128]) if c % 31)
    results = []
    for train, valid in ((32, 64), (64, 128)):
        for mode in ("affine", "projective"):
            inv = pow(coefficients[valid][anchor], -1, 31**valid) if mode == "projective" else 1
            records = []
            for i, value in enumerate(coefficients[valid]):
                if mode == "projective" and i == anchor:
                    continue
                value = value*inv % (31**valid)
                qc = rec.rational_candidate(value, train, valid)
                fc = []
                for residue, root in zip(roots31, roots):
                    candidates = rec.field_candidates(value, root, train, valid)
                    fc.append({"root_mod31": residue,
                               "survivors": [c for c in candidates if c["validates_unused_digits"]],
                               "tested_rows": len(candidates)})
                records.append({"basis_index_zero_based": i, "rational_candidate": qc, "field_trials": fc})
            qcount = sum(bool(r["rational_candidate"] and r["rational_candidate"]["validates_unused_digits"])
                         for r in records)
            counts = {str(root): sum(bool(next(t["survivors"] for t in r["field_trials"] if t["root_mod31"] == root))
                                      for r in records) for root in roots31}
            results.append({"training_digits": train, "validation_digits": valid, "mode": mode,
                            "rational_survivors": qcount, "field_survivors_by_root": counts,
                            "coefficient_count": len(records), "records": records})
            print("REDUCED_SPACE_RECOGNITION", train, valid, mode, "Q", qcount, "F", counts, flush=True)
    report = {"status": "pass", "milestone": "D74", "date": "2026-09-18",
              "sources": [source(p) for p in (__file__, job_path, DATA / "cm_frame_denominator_space.out",
                          DATA / "cm_frame_curve_candidate.json", DATA / "cm_frame_doubling_check.json",
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py",
                          ROOT / "dembele/pari/132_cm_frame_denominator_recognition.py",
                          ROOT / "dembele/pari/133_cm_frame_projective_denominator.py")]
                         +[source(DATA / f"cm_frame_doubling_normalized_{n}.json") for n in (32, 64, 128)],
              "space_dimension": 17, "full_integer_lattice_rank": 108,
              "smith_invariants": [int(x) for x in smith],
              "full_lattice_basis": [[int(x) for x in row] for row in lattice],
              "section_rows": [[int(x) for x in row] for row in sections],
              "section_height_decimal_digits": heights,
              "witness_rows_rational": [[str(x) for x in row] for row in witness_rows],
              "second_numerator_coefficients": checks.field(output, "SECOND_NUMERATOR"),
              "section_chart_coordinates_rational": [[str(x) for x in row] for row in section_images],
              "denominator_basis_coefficients": coefficients, "projective_anchor_index_zero_based": anchor,
              "recognition_results": results, "number_field_cover_obtained": False,
              "nonmembership_or_height_exclusion_proved": False,
              "wall_seconds": time.monotonic()-started}
    (DATA / "cm_frame_denominator_space_reduced.json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|135_CM_FRAME_DENOMINATOR_SPACE_REDUCTION", round(report["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()

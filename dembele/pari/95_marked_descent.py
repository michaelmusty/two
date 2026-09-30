"""D58: exact descent inputs and a bounded rational CM-polynomial pilot.

Run with sage -python. The geometric descent argument is in
certificates/marked-descent.md; field identities alone do not prove descent.
Numerical intervals use checkpoint discrepancies, NOT certified error bounds.
"""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import time

from sage.all import CyclotomicField, NumberField, PolynomialRing, QQ


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location(
    "cm_arithmetic", Path(__file__).with_name("94_cm_arithmetic.py"))
arithmetic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arithmetic)


def decimal(value, digits=25):
    value = Fraction(value)
    with localcontext() as ctx:
        ctx.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def farey_neighbors(value, bound):
    """Immediate neighbors among all rationals with denominator <= bound."""
    value = Fraction(value)
    if bound < 1 or value.denominator > bound:
        raise ValueError("the value must have denominator at most a positive bound")
    p, q = value.numerator, value.denominator
    if q == 1:
        return value-Fraction(1, bound), value+Fraction(1, bound)
    inverse = pow(p, -1, q)
    left_q = inverse + (bound-inverse)//q*q
    right_q = (-inverse) % q
    right_q += (bound-right_q)//q*q
    return (Fraction((p*left_q-1)//q, left_q),
            Fraction((p*right_q+1)//q, right_q))


def bounded_interval(center, radius, bound):
    """Exhaustive existence/uniqueness test in a closed rational interval.

    Fraction.limit_denominator gives an absolute nearest rational at the
    denominator bound. Its Farey neighbors decide uniqueness exactly.
    This certifies a statement about the SUPPLIED interval, not its accuracy.
    """
    center, radius = Fraction(center), Fraction(radius)
    if radius < 0 or bound < 1:
        raise ValueError("nonnegative radius and positive bound required")
    candidate = center.limit_denominator(bound)
    error = abs(candidate-center)
    result = {"denominator_bound": int(bound), "nearest": str(candidate),
              "distance": str(error), "status": "none"}
    if error > radius:
        return result
    left, right = farey_neighbors(candidate, bound)
    unique = left < center-radius and center+radius < right
    result.update(status="unique" if unique else "ambiguous",
                  left_neighbor=str(left), right_neighbor=str(right))
    return result


def exact_descent_inputs():
    ring = PolynomialRing(QQ, "b")
    field = NumberField(ring(arithmetic.FIELD_COEFFICIENTS), "b")
    b = field.gen()
    sigma = field.hom([b**3-3*b], field)
    orbit, value = [], b
    for _ in range(8):
        orbit.append(value)
        value = sigma(value)
    assert len(set(orbit)) == 8 and value == b
    prime = field.ideal(2+b)
    assert prime.norm() == 2 and prime**8 == field.ideal(2)
    assert 2+sigma(b) == (2+b)*(b-1)**2
    assert field.ideal(2+sigma(b)) == prime
    lift_product = field(1)
    for value in orbit:
        lift_product *= 1-value
    assert lift_product == -1
    class_number = field.class_number(proof=True)
    narrow_number = int(field.pari_bnf(proof=True).bnfnarrow()[0])
    cm_point_field = CyclotomicField(32)
    cm_point_class_number = cm_point_field.class_number(proof=True)
    assert class_number == narrow_number == cm_point_class_number == 1
    assert field.discriminant() == 2**31
    # Riemann--Hurwitz on the coarse smooth curves, not orbifold Euler numbers.
    branch_degree = (2*40-2)-2*(2*16-2)
    assert branch_degree == 18 == 17+1
    return {
        "F_polynomial_ascending": arithmetic.FIELD_COEFFICIENTS,
        "F_discriminant": str(field.discriminant()),
        "F_automorphism": "b -> b^3-3*b", "automorphism_order": 8,
        "F_class_number_proved": int(class_number),
        "F_narrow_class_number_proved": narrow_number,
        "prime_generator": "2+b", "prime_norm": 2, "ramification_index": 8,
        "prime_invariance_identity": "2+sigma(b)=(2+b)*(b-1)^2",
        "CM_lift": "beta^2=-2-b; sigma(beta)=(1-b)*beta",
        "CM_lift_eighth_power_factor": str(lift_product),
        "ray_class_reason": "O_F/p=F_2 and narrow class number 1 imply trivial ray class group for p times any subset of real places",
        "distinguished_CM_field": "Q(zeta_32)",
        "distinguished_CM_field_class_number_proved": int(cm_point_class_number),
        "source_genus": 40, "quotient_genus": 16, "cover_degree": 2,
        "branch_degree_Riemann_Hurwitz": branch_degree,
        "status": "exact arithmetic checks supporting the cited geometric argument; no explicit curve descent maps computed",
    }


def coefficient_intervals(normalizations, multiplier=10):
    """Use exact saved decimal strings and an empirical L1 discrepancy radius."""
    names = ("current", "previous", "alternate_fit", "larger_probe")
    banks = {name: [tuple(Fraction(v) for v in pair) for pair in
                    normalizations[name]["x_cm_value_polynomial_ascending"]]
             for name in names}
    if any(len(bank) != 18 for bank in banks.values()):
        raise ValueError("expected four monic degree-17 polynomial banks")
    if multiplier <= 0:
        raise ValueError("positive empirical multiplier required")
    rows = []
    for i, (real, imag) in enumerate(banks["current"]):
        changes = {name: abs(real-bank[i][0])+abs(imag-bank[i][1])
                   for name, bank in banks.items() if name != "current"}
        imaginary = max(abs(bank[i][1]) for bank in banks.values())
        radius = multiplier*max(imaginary, *changes.values())
        rows.append({"index": i, "center": str(real), "center_decimal": decimal(real),
                     "empirical_radius": str(radius), "radius_decimal": decimal(radius),
                     "changes_L1": {name: decimal(v) for name, v in changes.items()},
                     "maximum_imaginary_part": decimal(imaginary)})
    identities = {}
    for name, bank in banks.items():
        identities[name] = {
            "c16_absolute_L1": decimal(sum(abs(v) for v in bank[16])),
            "c17_minus_one_absolute_L1": decimal(abs(bank[17][0]-1)+abs(bank[17][1])),
            "2c15_minus_3c14_absolute_L1": decimal(sum(
                abs(2*bank[15][j]-3*bank[14][j]) for j in range(2))),
        }
    return rows, identities


def rational_pilot(path, bounds):
    normalizations = json.loads(path.read_text())["canonical_cm_normalizations"]
    rows, identities = coefficient_intervals(normalizations)
    independent = list(range(14))+[15]
    scans = []
    for bound in bounds:
        entries = [dict(index=i, **bounded_interval(
            row["center"], row["empirical_radius"], bound))
                   for i, row in enumerate(rows[:16])]
        scans.append({
            "denominator_bound": bound, "coefficients": entries,
            "independent_hit_indices": [i for i in independent if entries[i]["status"] != "none"],
            "independent_unique_indices": [i for i in independent if entries[i]["status"] == "unique"],
            "independent_missing_indices": [i for i in independent if entries[i]["status"] == "none"],
            "all_independent_intervals_have_a_candidate": all(entries[i]["status"] != "none" for i in independent),
        })
    return {
        "source": arithmetic.source(path),
        "interval_rule": "center=Re(current); radius=10*max(L1 changes to previous/alternate_fit/larger_probe, all four imaginary parts)",
        "interval_status": "empirical intervals, not certified enclosures of the exact coefficients",
        "coefficient_intervals": rows, "normalization_identity_residuals": identities,
        "exact_identities_from_normalization": ["c17=1", "c16=0", "2*c15=3*c14"],
        "independent_indices": independent, "scans": scans,
        "certified_target_polynomial": None,
        "status": "bounded interval tests only; individual hits are not algebraic recognitions",
    }


def normalization_height_control():
    """A simple known generator can give a monic polynomial with huge denominators."""
    ring = PolynomialRing(QQ, "T")
    t = ring.gen()
    h = ring(arithmetic.HARBATER_COEFFICIENTS)
    polynomial = (QQ(17)/30)**17*h((30*t+2)/17)
    assert polynomial.is_monic() and polynomial[16] == 0
    assert 2*polynomial[15] == 3*polynomial[14]
    denominators = [int(v.denominator()) for v in polynomial]
    # Recover from truncated 80-place decimals with a genuine, known error bound.
    scale = 10**80
    controls = []
    for value in polynomial:
        exact = Fraction(int(value.numerator()), int(value.denominator()))
        approximation = Fraction((exact*scale).__floor__(), scale)
        result = bounded_interval(approximation, Fraction(1, scale), max(denominators))
        controls.append(result["status"] == "unique" and Fraction(result["nearest"]) == exact)
    assert all(controls)
    return {
        "generator": "X1=(17*theta-2)/30, for Elkies's theta; NOT the target X",
        "polynomial_coefficients_ascending": [str(v) for v in polynomial],
        "coefficient_denominators": denominators,
        "maximum_denominator": max(denominators),
        "all_coefficients_recovered_from_80_place_truncations": all(controls),
        "consequence": "a coefficient denominator cap is not a generator-height bound",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cm-report", type=Path, default=DATA / "cm_pointed_maps_flag_16384.json")
    parser.add_argument("--bounds", type=int, nargs="+", default=[1000, 10000, 100000, 1000000])
    parser.add_argument("--output", type=Path, default=DATA / "marked_descent.json")
    args = parser.parse_args()
    if any(bound < 1 for bound in args.bounds):
        parser.error("bounds must be positive")
    start = time.monotonic()
    report = {
        "status": "descent inputs checked; see marked-descent.md for the proof and its hypotheses; bounded rational pilot complete",
        "script_source": arithmetic.source(Path(__file__)),
        "arithmetic_helper_source": arithmetic.source(Path(arithmetic.__file__)),
        "exact_inputs": exact_descent_inputs(),
        "geometric_dependencies": {
            "specific_curve": "Dembélé 1906.06772v2, Theorem 5.1 and Lemma 5.2; compatible canonical conjugation preserves CM type and the p-labelled Atkin--Lehner cover",
            "marked_descent": "Sijsling--Voight, On explicit descent of marked curves and maps, Theorem 1.3.2 in the 2020 author version (published Theorem 1.8)",
            "function_hypotheses": "P ordinary and the D56 second/third moments nonzero; numerically supported, not certified here",
            "explicit_descent_isomorphisms": None,
        },
        "rational_pilot": rational_pilot(args.cm_report, args.bounds),
        "normalization_height_control": normalization_height_control(),
        "limitations": [
            "Arithmetic identities do not constitute an independent proof of the canonical-model conjugation theorem.",
            "No exact coefficients of the target functions or their CM polynomial are recovered.",
            "The checkpoint intervals are empirical; bounded exclusions are not height lower bounds.",
            "The CM polynomial alone would not define the curve or the desired nonsolvable field.",
        ],
        "wall_seconds": time.monotonic()-start,
    }
    output = json.dumps(report, indent=2, allow_nan=False)+"\n"
    args.output.write_text(output)
    args.output.with_suffix(".out").write_text(output)
    print(report["status"])
    for scan in report["rational_pilot"]["scans"]:
        print("Bound", scan["denominator_bound"],
              "hits", scan["independent_hit_indices"],
              "unique", scan["independent_unique_indices"],
              "missing", scan["independent_missing_indices"])
    print("Known simple generator: maximum monic denominator",
          report["normalization_height_control"]["maximum_denominator"])


if __name__ == "__main__":
    main()

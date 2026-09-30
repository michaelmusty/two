"""D59: simultaneous CM evaluation reconstruction using the labelled orbit.

This is a bounded numerical experiment, not a certificate of the target
values. It uses the four existing analytic banks and creates no new bank.
"""
import argparse
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import time

import mpmath as mp
from sage.all import NumberField, PolynomialRing, QQ, ZZ, gcd, matrix


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result
descent = module("cm_descent", "95_marked_descent.py")
arithmetic = descent.arithmetic
BANKS = ("current", "previous", "alternate_fit", "larger_probe")


def pair(value, digits=55):
    return [mp.nstr(value.real,digits), mp.nstr(value.imag,digits)]


def evaluate(element, root):
    return sum(mp.mpf(str(c))*root**j for j,c in enumerate(element.list()))


def matrix_norm_inf(value):
    return max(sum(abs(value[i,j]) for j in range(value.cols)) for i in range(value.rows))


def evaluation_basis(roots):
    ring = PolynomialRing(QQ, "t")
    field = NumberField(ring(arithmetic.HARBATER_COEFFICIENTS), "theta")
    # Default floating precision can give a very badly reduced basis for this
    # power order. Check the resulting basis and matrix, not its method name.
    integral = list(field.reduced_basis(prec=256))
    constants = [z for z in integral if z in QQ]
    assert len(constants) == 1 and abs(constants[0]) == 1
    integral = [field(1)]+[z for z in integral if z not in QQ]
    assert field.discriminant(integral) == field.discriminant() == 2**79
    basis = [field(1)]+[z-z.trace()/17 for z in integral[1:]]
    values = mp.matrix([[evaluate(z,r) for z in basis] for r in roots])
    inverse = values**-1
    residual = matrix_norm_inf(values*inverse-mp.eye(17))
    condition = matrix_norm_inf(values)*matrix_norm_inf(inverse)
    assert residual < mp.mpf("1e-50") and condition < 100
    return field, basis, values, inverse, {
        "integral_basis_power_coordinates": [[str(c) for c in z.list()] for z in integral],
        "trace_centered_basis_power_coordinates": [[str(c) for c in z.list()] for z in basis],
        "integral_basis_discriminant": str(field.discriminant(integral)),
        "basis_reduction_precision_bits": 256,
        "evaluation_matrix_condition_inf": mp.nstr(condition,25),
        "evaluation_matrix_inverse_residual_inf": mp.nstr(residual,25),
    }


def projective_search(ratios, errors, pivot, height_cap=10**9,
                      scales=(10**10,10**11,10**12,10**13)):
    """LLL search for a single primitive integer vector in projective intervals.

    This is not exhaustive enumeration up to height_cap. A height cap prevents
    generic huge-denominator approximations from being called recognitions.
    """
    n = len(ratios)
    indices = [i for i in range(n) if i != pivot]
    seen, accepted, best = set(), [], None
    examined = 0
    for scale in scales:
        rounded = [ZZ(int(mp.nint(scale*ratios[j].real))) for j in indices]
        lattice = matrix(ZZ,n,n)
        lattice[0,0] = 1
        for j,value in enumerate(rounded):
            lattice[0,j+1] = value
            lattice[j+1,j+1] = scale
        for row in lattice.LLL().rows():
            denominator = row[0]
            if not denominator:
                continue
            integers = [ZZ(0)]*n
            integers[pivot] = denominator
            for j,index in enumerate(indices):
                assert (denominator*rounded[j]-row[j+1]) % scale == 0
                integers[index] = (denominator*rounded[j]-row[j+1])//scale
            divisor = gcd(integers)
            integers = [v//divisor for v in integers]
            if integers[pivot] < 0:
                integers = [-v for v in integers]
            key = tuple(map(int,integers))
            if key in seen:
                continue
            seen.add(key)
            examined += 1
            height = max(map(abs,key))
            score = max(abs(mp.mpf(int(integers[j]))/int(integers[pivot])-ratios[j])/
                        max(errors[j],mp.mpf("1e-70")) for j in indices)
            row_summary = {"height": height, "maximum_interval_residual": mp.nstr(score,25), "lattice_scale": scale}
            if best is None or score < best[0]:
                best = (score,row_summary)
            if height <= height_cap and score <= 1:
                accepted.append(dict(row_summary,primitive_vector=list(key)))
    return {
        "height_cap": height_cap, "lattice_scales": list(scales),
        "distinct_LLL_vectors_examined": examined,
        "accepted_directions": accepted,
        "best_interval_fit_regardless_of_height": best[1] if best else None,
        "status": "bounded LLL search, not exhaustive height exclusion; intervals are empirical",
    }


def normalized_line(element):
    centered = element-element.trace()/17
    second, third = (centered**2).trace()/17, (centered**3).trace()/17
    if not second or not third:
        raise ValueError("zero normalization moment")
    return second/third*centered


def value_validation(element, roots, lookup, banks, radii):
    predicted = [evaluate(element,roots[j]) for j in lookup]
    scores = {name: max(abs(predicted[i]-values[i])/max(radii[i],mp.mpf("1e-70"))
                        for i in range(17)) for name,values in banks.items()}
    return {"bank_maximum_scaled_errors": {name: mp.nstr(v,25) for name,v in scores.items()},
            "fits_all_empirical_value_intervals": all(v <= 1 for v in scores.values())}


def reconstruct(which, normalizations, roots, lookup, field, basis, inverse, height_cap):
    banks = {name: [mp.mpc(*v) for v in normalizations[name]["normalized_"+which+"_values"]]
             for name in BANKS}
    coefficients = {}
    for name,values in banks.items():
        ordered = mp.matrix(17,1)
        for i,j in enumerate(lookup):
            ordered[j] = values[i]
        coefficients[name] = inverse*ordered
    pivot = max(range(1,17),key=lambda j:abs(coefficients["current"][j]))
    ratios = {name: [values[j]/values[pivot] for j in range(1,17)]
              for name,values in coefficients.items()}
    current = ratios["current"]
    errors = [10*max(
        max(abs(current[j].real-ratios[name][j].real)+abs(current[j].imag-ratios[name][j].imag)
            for name in BANKS[1:]),
        max(abs(ratios[name][j].imag) for name in BANKS)) for j in range(16)]
    # Structural pivot=1 is excluded from the independent interval count.
    intervals = []
    for j in range(16):
        if j == pivot-1:
            continue
        intervals.append({
            "basis_index": j+1, "ratio": pair(current[j]),
            "empirical_radius": mp.nstr(errors[j],55),
            "bounds": [descent.bounded_interval(Fraction(mp.nstr(current[j].real,65)),
                       Fraction(mp.nstr(errors[j],65)),bound)
                       for bound in (100,1000,10000,100000,1000000)],
        })
    search = projective_search(current,errors,pivot-1,height_cap)
    radii = [10*max(abs(banks["current"][i]-banks[name][i]) for name in BANKS[1:]) for i in range(17)]
    for candidate in search["accepted_directions"]:
        element = sum((ZZ(c)*z for c,z in zip(candidate["primitive_vector"],basis[1:])),field(0))
        element = normalized_line(element)
        candidate["normalized_element_power_coordinates"] = [str(c) for c in element.list()]
        candidate["value_validation"] = value_validation(element,roots,lookup,banks,radii)
        candidate["status"] = "numerical candidate only, even if all value checks pass"
    return {
        "function": which.upper(), "coefficients_by_bank": {name: [pair(v) for v in coefs] for name,coefs in coefficients.items()},
        "maximum_trace_constant_coefficient": mp.nstr(max(abs(c[0]) for c in coefficients.values()),25),
        "projective_pivot_basis_index": pivot,
        "projective_intervals": intervals,
        "interval_hit_counts": [{"bound": bound,
            "hits": sum(row["bounds"][k]["status"] != "none" for row in intervals),
            "unique": sum(row["bounds"][k]["status"] == "unique" for row in intervals)}
            for k,bound in enumerate((100,1000,10000,100000,1000000))],
        "joint_search": search,
    }


def known_field_control(field, basis, roots, lookup, inverse):
    exact = normalized_line(field.gen())
    truth = [evaluate(exact,roots[j]) for j in lookup]
    # A known bounded perturbation tests recovery independently of target data.
    perturbed = [v+mp.mpf("1e-15")*(i-8)/17 for i,v in enumerate(truth)]
    ordered = mp.matrix(17,1)
    for i,j in enumerate(lookup):
        ordered[j] = perturbed[i]
    coefficients = inverse*ordered
    pivot = max(range(1,17),key=lambda j:abs(coefficients[j]))
    ratios = [coefficients[j]/coefficients[pivot] for j in range(1,17)]
    search = projective_search(ratios,[mp.mpf("1e-12")]*16,pivot-1,height_cap=1000)
    recovered = []
    for candidate in search["accepted_directions"]:
        element = normalized_line(sum((ZZ(c)*z for c,z in zip(candidate["primitive_vector"],basis[1:])),field(0)))
        recovered.append(element == exact)
    assert any(recovered)
    validation = value_validation(exact,roots,lookup,{"control":perturbed},[mp.mpf("1e-12")]*17)
    assert validation["fits_all_empirical_value_intervals"]
    return {"generator": "(17*theta-2)/30", "known_perturbation_bound": "1e-15",
            "direction_height_cap": 1000, "exact_element_recovered": any(recovered),
            "value_check": validation}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--orbit", type=Path, default=DATA/"cm_orbit.json")
    parser.add_argument("--cm-report", type=Path, default=DATA/"cm_pointed_maps_flag_16384.json")
    parser.add_argument("--height-cap", type=int, default=10**9)
    parser.add_argument("--output", type=Path, default=DATA/"cm_field_recognition.json")
    args = parser.parse_args()
    if args.height_cap < 1:
        parser.error("positive height cap required")
    start = time.monotonic()
    with mp.workdps(85):
        orbit = json.loads(args.orbit.read_text())
        roots = [mp.mpc(*z) for z in orbit["field_root_action"]["complex_roots"]]
        lookup = orbit["matching"]["point_to_root_index_zero_based"]
        assert sorted(lookup) == list(range(17))
        field,basis,values,inverse,basis_report = evaluation_basis(roots)
        normalizations = json.loads(args.cm_report.read_text())["canonical_cm_normalizations"]
        # Check the chosen reference point and conjugation on BOTH functions.
        classes = orbit["CM_orbit"]["class_labels_in_point_order"]
        conjugates = [classes.index((-c)%17) for c in classes]
        diagnostics = {}
        for which in ("x","y"):
            data = [mp.mpc(*v) for v in normalizations["current"]["normalized_"+which+"_values"]]
            error = max(abs(data[conjugates[i]]-mp.conj(data[i])) for i in range(17))
            separation = min(abs(data[j]-mp.conj(data[i])) for i in range(17) for j in range(17) if j != conjugates[i])
            assert error < mp.mpf("1e-14") and separation > mp.mpf("1e-4")
            assert abs(data[8].imag) < mp.mpf("1e-14")
            diagnostics[which] = {"conjugation_discrepancy": mp.nstr(error,25), "next_match_separation": mp.nstr(separation,25)}
        for i,j in enumerate(conjugates):
            assert abs(roots[lookup[j]]-mp.conj(roots[lookup[i]])) < mp.mpf("1e-75")
        outputs = [reconstruct(which,normalizations,roots,lookup,field,basis,inverse,args.height_cap) for which in ("x","y")]
        report = {
            "status": "labelled simultaneous reconstruction pilot complete; candidates require independent certification",
            "script_source": arithmetic.source(Path(__file__)),
            "interval_helper_source": arithmetic.source(Path(descent.__file__)),
            "arithmetic_helper_source": arithmetic.source(Path(arithmetic.__file__)),
            "orbit_source": arithmetic.source(args.orbit), "CM_values_source": arithmetic.source(args.cm_report),
            "field_basis": basis_report, "conjugation_checks": diagnostics,
            "reconstruction_target": "projective directions of X,Y in a trace-zero basis of Q(theta); joint primitive integer vectors, not monic polynomial coefficients",
            "interval_rule": "10*max(projective coordinate L1 differences to the three other banks, all four imaginary parts)",
            "functions": outputs,
            "known_field_control": known_field_control(field,basis,roots,lookup,inverse),
            "limitations": [
                "The target intervals are empirical, not certified analytic error enclosures.",
                "The LLL search is not exhaustive up to its imposed projective height cap.",
                "Huge-denominator numerical approximations are rejected rather than called field identifications.",
                "Recognizing CM restrictions would still not give an exact curve model.",
            ],
            "wall_seconds": time.monotonic()-start,
        }
    output = json.dumps(report,indent=2,allow_nan=False)+"\n"
    args.output.write_text(output)
    args.output.with_suffix(".out").write_text(output)
    print(report["status"])
    print("Evaluation condition:",basis_report["evaluation_matrix_condition_inf"])
    for row in outputs:
        print(row["function"],row["interval_hit_counts"])
        print("Accepted joint directions:",len(row["joint_search"]["accepted_directions"]))
        print("Best fit without height cap:",row["joint_search"]["best_interval_fit_regardless_of_height"])


if __name__ == "__main__":
    main()

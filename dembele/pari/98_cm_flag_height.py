"""D60: exact height exclusions for empirical CM evaluation subspace boxes.

All chart and certificate arithmetic is rational, starting from D59's saved
decimal coordinates. The boxes are empirical; the certificates do not prove
that the unknown target lies in them. No new analytic bank is generated.
"""
import argparse
from fractions import Fraction
import importlib.util
import itertools
import json
from math import isqrt
from pathlib import Path
import time

from sage.all import QQ, ZZ, QuadraticField, matrix, prod


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("cm_field_height", Path(__file__).with_name("97_cm_field_recognition.py"))
recognition = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recognition)
arithmetic = recognition.arithmetic
GAUSSIAN = QuadraticField(-1, "imaginary_unit")
BANKS = recognition.BANKS
SCALES = (10**8, 10**10, 10**11, 10**12, 10**13, 10**14, 10**16)


def rational_decimal(value):
    return QQ(Fraction(value))


def gaussian(pair):
    return GAUSSIAN(rational_decimal(pair[0]))+rational_decimal(pair[1])*GAUSSIAN.gen()


def real_imag(value):
    return tuple(GAUSSIAN(value).vector())


def complex_l1(value):
    return sum(abs(c) for c in real_imag(value))


def serialized_matrix(value):
    return [[str(v) for v in row] for row in value.rows()]


def chart_box(banks, pivots=None):
    """Choose a nonzero maximal minor and form exact [I | A] charts.

    The imaginary parts and bank discrepancies define an empirical real
    box. Exact arithmetic on saved decimal inputs is not an analytic bound.
    """
    current = banks["current"]
    dimension, ambient = current.nrows(), current.ncols()
    if dimension not in (1, 2) or ambient <= dimension:
        raise ValueError("expected a line or plane in a larger ambient space")
    if any(m.dimensions() != current.dimensions() for m in banks.values()):
        raise ValueError("inconsistent bank dimensions")
    if pivots is None:
        options = list(itertools.combinations(range(ambient), dimension))
        pivots = max(options, key=lambda p: current.matrix_from_columns(p).det().norm())
    pivots = list(pivots)
    if len(pivots) != dimension or len(set(pivots)) != dimension:
        raise ValueError("invalid pivot columns")
    if not all(0 <= j < ambient for j in pivots):
        raise ValueError("pivot outside ambient space")
    charts = {}
    for name, values in banks.items():
        pivot = values.matrix_from_columns(pivots)
        if not pivot.det():
            raise ValueError("chosen chart is singular")
        charts[name] = pivot.inverse()*values
        assert charts[name].matrix_from_columns(pivots) == matrix.identity(GAUSSIAN, dimension)
    free = [j for j in range(ambient) if j not in pivots]
    centers, radii = matrix(QQ, dimension, len(free)), matrix(QQ, dimension, len(free))
    entries = []
    for i in range(dimension):
        for k, j in enumerate(free):
            centers[i,k] = real_imag(charts["current"][i,j])[0]
            changes = [complex_l1(charts["current"][i,j]-v[i,j])
                       for name,v in charts.items() if name != "current"]
            imaginary = [abs(real_imag(v[i,j])[1]) for v in charts.values()]
            radii[i,k] = 10*max(changes+imaginary)
            entries.append({
                "chart_row": i, "field_basis_index": j+1,
                "center": str(centers[i,k]), "empirical_radius": str(radii[i,k]),
                "individual_denominator_tests": [
                    recognition.descent.bounded_interval(Fraction(str(centers[i,k])),
                        Fraction(str(radii[i,k])), bound)
                    for bound in (1000,10000,100000,1000000,10000000)],
            })
    report = {
        "dimension": dimension, "ambient_dimension": ambient,
        "pivot_coordinate_indices_zero_based": pivots,
        "pivot_field_basis_indices": [i+1 for i in pivots],
        "free_coordinate_indices_zero_based": free,
        "centers": serialized_matrix(centers), "radii": serialized_matrix(radii),
        "interval_rule": "10*max(complex L1 change from current to every other bank, imaginary parts of all banks); exact arithmetic on saved decimals",
        "minimum_empirical_radius": str(min(radii.list())),
        "maximum_empirical_radius": str(max(radii.list())),
        "maximum_chart_imaginary_part": str(max(abs(real_imag(v)[1]) for m in charts.values() for v in m.list())),
        "entries": entries,
        "denominator_test_counts": [{"bound": bound,
            "hits": sum(e["individual_denominator_tests"][k]["status"] != "none" for e in entries),
            "unique": sum(e["individual_denominator_tests"][k]["status"] == "unique" for e in entries)}
            for k,bound in enumerate((1000,10000,100000,1000000,10000000))],
    }
    return report, charts


def approximation_lattice(centers, scale):
    rank, free = centers.dimensions()
    ambient = rank+free
    rounded = matrix(ZZ, [[(scale*c+QQ(1)/2).floor() for c in row] for row in centers.rows()])
    lattice = matrix(ZZ, ambient, ambient)
    for i in range(rank):
        lattice[i,i] = 1
        for j in range(free):
            lattice[i,rank+j] = rounded[i,j]
    for j in range(free):
        lattice[rank+j,rank+j] = scale
    return lattice, rounded


def gram_schmidt_squared(basis):
    """Exact LDL calculation; no reliance on floating LLL metadata."""
    gram = basis*basis.transpose()
    n = basis.nrows()
    mu, squared = matrix(QQ,n,n), []
    for i in range(n):
        for j in range(i):
            mu[i,j] = (gram[i,j]-sum(mu[i,k]*mu[j,k]*squared[k] for k in range(j)))/squared[j]
        value = gram[i,i]-sum(mu[i,k]**2*squared[k] for k in range(i))
        if value <= 0:
            raise ValueError("lattice basis must have independent rows")
        squared.append(value)
    assert prod(squared) == gram.det()
    return squared


def strict_integer_sqrt(value):
    """Largest nonnegative integer h with h^2 < a positive rational value."""
    value = QQ(value)
    if value <= 0:
        raise ValueError("positive threshold required")
    height = isqrt(int(value.floor()))
    if height*height == value:
        height -= 1
    return max(height,0)


def exclusion_factors(centers, radii, scale, rounded, squared):
    rank = centers.nrows()
    errors = matrix(QQ, [[abs(rounded[i,j]-scale*centers[i,j])+scale*radii[i,j]
                         for j in range(centers.ncols())] for i in range(rank)])
    # Any nonzero r-vector in the exterior lattice has at least this norm^2.
    lower = prod(sorted(squared)[:rank])
    # Hadamard bounds the wedge of the r graph rows [I | rounding errors].
    factor = prod(1+sum(c*c for c in row) for row in errors.rows())
    threshold = lower/factor
    return errors, lower, factor, threshold


def make_certificate(box, scale):
    centers, radii = matrix(QQ,box["centers"]), matrix(QQ,box["radii"])
    if scale < 1 or min(radii.list()) < 0:
        raise ValueError("invalid scale or radius")
    lattice, rounded = approximation_lattice(centers,scale)
    reduced, transform = lattice.LLL(delta=0.99, transformation=True)
    assert transform*lattice == reduced and abs(transform.det()) == 1
    squared = gram_schmidt_squared(reduced)
    errors,lower,factor,threshold = exclusion_factors(centers,radii,scale,rounded,squared)
    result = {
        "dimension": centers.nrows(), "ambient_dimension": lattice.nrows(),
        "lattice_scale": scale,
        "rounded_graph": serialized_matrix(rounded),
        "reduced_basis": serialized_matrix(reduced),
        "unimodular_transformation": serialized_matrix(transform),
        "gram_schmidt_squared_lengths": [str(v) for v in squared],
        "rounding_and_interval_bounds": serialized_matrix(errors),
        "exterior_length_squared_lower_bound": str(lower),
        "exterior_length_squared_upper_factor": str(factor),
        "height_squared_threshold": str(threshold),
        "excluded_height_inclusive": strict_integer_sqrt(threshold),
        "height_definition": "maximum absolute primitive integer Pluecker coordinate in the fixed D59 trace-centered basis",
        "claim": "No rational subspace in this declared real chart box has height at most the excluded bound; membership of the target in the box is NOT certified.",
    }
    verify_certificate(box,result)
    return result


def verify_certificate(box, certificate):
    """Check a saved exclusion using exact arithmetic only, without LLL."""
    centers, radii = matrix(QQ,box["centers"]), matrix(QQ,box["radii"])
    rank, free = centers.dimensions()
    if rank not in (1,2) or free < 1 or radii.dimensions() != centers.dimensions():
        raise ValueError("invalid line/plane box")
    if min(radii.list()) < 0:
        raise ValueError("negative interval radius")
    scale = ZZ(certificate["lattice_scale"])
    if scale < 1:
        raise ValueError("nonpositive lattice scale")
    assert certificate["dimension"] == rank and certificate["ambient_dimension"] == rank+free
    lattice, rounded = approximation_lattice(centers,scale)
    reduced = matrix(ZZ,certificate["reduced_basis"])
    transform = matrix(ZZ,certificate["unimodular_transformation"])
    assert transform*lattice == reduced and abs(transform.det()) == 1
    assert matrix(ZZ,certificate["rounded_graph"]) == rounded
    squared = gram_schmidt_squared(reduced)
    assert squared == [QQ(v) for v in certificate["gram_schmidt_squared_lengths"]]
    errors,lower,factor,threshold = exclusion_factors(centers,radii,scale,rounded,squared)
    assert matrix(QQ,certificate["rounding_and_interval_bounds"]) == errors
    assert QQ(certificate["exterior_length_squared_lower_bound"]) == lower
    assert QQ(certificate["exterior_length_squared_upper_factor"]) == factor
    assert QQ(certificate["height_squared_threshold"]) == threshold
    height = certificate["excluded_height_inclusive"]
    assert height == strict_integer_sqrt(threshold)
    assert height*height*factor < lower <= (height+1)**2*factor
    return True


def primitive_pluecker(basis):
    """Canonical primitive integer exterior coordinates of a rational space."""
    rank, ambient = basis.dimensions()
    minors = [basis.matrix_from_columns(p).det() for p in itertools.combinations(range(ambient),rank)]
    denominator = ZZ(1)
    for value in minors:
        denominator = denominator.lcm(QQ(value).denominator())
    integers = [ZZ(denominator*v) for v in minors]
    divisor = ZZ(0)
    for value in integers:
        divisor = divisor.gcd(value)
    if divisor == 0:
        raise ValueError("rank-deficient subspace")
    integers = [v//divisor for v in integers]
    if next(v for v in integers if v) < 0:
        integers = [-v for v in integers]
    return integers


def analyse(name, banks):
    box, charts = chart_box(banks)
    certificates = [make_certificate(box,scale) for scale in SCALES]
    best = max(certificates,key=lambda c:c["excluded_height_inclusive"])
    return {
        "subspace": name, "box": box,
        "scale_results": [{"scale": c["lattice_scale"], "excluded_height_inclusive": c["excluded_height_inclusive"]}
                          for c in certificates],
        "best_certificate": best,
    }


def known_plane_control(source):
    """A small exact plane mixed by a nonrational change of generators."""
    ring = recognition.arithmetic
    from sage.all import NumberField, PolynomialRing
    field = NumberField(PolynomialRing(QQ,"t")(ring.HARBATER_COEFFICIENTS),"theta")
    # Number-field construction from lists of rational coefficients is exact.
    basis = [field([QQ(c) for c in row]) for row in source["field_basis"]["trace_centered_basis_power_coordinates"]]
    power = matrix(QQ,[v.vector() for v in basis]).transpose()
    centered = [field.gen()**j-(field.gen()**j).trace()/17 for j in (1,2)]
    exact = matrix(QQ,[list(power.solve_right(v.vector()))[1:] for v in centered])
    true_height = int(max(map(abs,primitive_pluecker(exact))))
    imaginary = GAUSSIAN.gen()
    mixed = matrix(GAUSSIAN,[[1+imaginary,2-imaginary],[-3+2*imaginary,1]])*exact
    banks = {}
    for k,name in enumerate(BANKS):
        # Perturb each independent generator before row reduction.
        banks[name] = mixed+matrix(GAUSSIAN,2,16,
            [QQ((k+1)*(j-15))/10**18 for j in range(32)])
    box,_ = chart_box(banks)
    pivots = box["pivot_coordinate_indices_zero_based"]
    truth = exact.matrix_from_columns(pivots).inverse()*exact
    centers,radii = matrix(QQ,box["centers"]),matrix(QQ,box["radii"])
    free = box["free_coordinate_indices_zero_based"]
    assert all(abs(truth[i,j]-centers[i,k]) <= radii[i,k]
               for i in range(2) for k,j in enumerate(free))
    cert = make_certificate(box,10**12)
    assert cert["excluded_height_inclusive"] < true_height
    # With known height and these much narrower control intervals, each
    # coordinate is uniquely reconstructed and the exact plane is recovered.
    rebuilt = matrix(QQ,2,16)
    for i,j in enumerate(pivots):
        rebuilt[i,j] = 1
    for i in range(2):
        for k,j in enumerate(free):
            hit = recognition.descent.bounded_interval(Fraction(str(centers[i,k])),
                Fraction(str(radii[i,k])),true_height)
            assert hit["status"] == "unique"
            rebuilt[i,j] = QQ(Fraction(str(centers[i,k])).limit_denominator(true_height))
    assert rebuilt.row_space() == exact.row_space()
    return {"plane": "span(theta-Tr(theta)/17, theta^2-Tr(theta^2)/17)",
            "exact_pluecker_height": true_height,
            "excluded_height_inclusive": cert["excluded_height_inclusive"],
            "known_plane_inside_box": True, "exact_plane_recovered_with_known_height": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path,default=DATA/"cm_field_recognition.json")
    parser.add_argument("--output",type=Path,default=DATA/"cm_flag_height.json")
    parser.add_argument("--verify",type=Path,help="verify a saved report without new lattice reductions")
    args = parser.parse_args()
    if args.verify:
        report = json.loads(args.verify.read_text())
        for result in report["subspaces"]:
            verify_certificate(result["box"],result["best_certificate"])
        print("PASS: all saved lattice exclusion certificates verified exactly")
        return
    started = time.monotonic()
    source = json.loads(args.source.read_text())
    coefficients = {row["function"]: {
        name:[gaussian(v) for v in row["coefficients_by_bank"][name][1:]] for name in BANKS}
        for row in source["functions"]}
    spaces = [analyse(label,{name:matrix(GAUSSIAN,[coefficients[label][name]]) for name in BANKS})
              for label in ("X","Y")]
    spaces.append(analyse("span(X,Y)",{name:matrix(GAUSSIAN,[coefficients[v][name] for v in ("X","Y")]) for name in BANKS}))
    control = known_plane_control(source)
    report = {
        "status": "exact height exclusions within empirical coordinate boxes; no unconditional target height bound or exact function value",
        "script_source": arithmetic.source(Path(__file__)),
        "recognition_helper_source": arithmetic.source(Path(recognition.__file__)),
        "interval_helper_source": arithmetic.source(Path(recognition.descent.__file__)),
        "arithmetic_helper_source": arithmetic.source(Path(arithmetic.__file__)),
        "coordinate_source": arithmetic.source(args.source),
        "coordinate_field": "fixed D59 trace-centered basis of the known degree-17 CM residue field",
        "subspaces": spaces, "known_plane_control": control,
        "limitations": [
            "Finite decimal inputs define the boxes exactly, but no analytic theorem places the target in them.",
            "The CM/root matching and D56/D58 geometric hypotheses remain inputs.",
            "Pluecker height is independent of a basis for the subspace, but depends on the fixed ambient field basis.",
            "The certificates exclude every rational subspace up to their bounds inside the declared boxes; they do not give a target upper bound.",
            "No new analytic data, exact section evaluations, or curve model are produced.",
        ],
        "wall_seconds": time.monotonic()-started,
    }
    output = json.dumps(report,indent=2,allow_nan=False)+"\n"
    args.output.write_text(output)
    args.output.with_suffix(".out").write_text(output)
    print(report["status"])
    for row in spaces:
        cert = row["best_certificate"]
        print(row["subspace"], "excludes height <=",cert["excluded_height_inclusive"],"at scale",cert["lattice_scale"])
    print("Known plane control:",control)


if __name__ == "__main__":
    main()

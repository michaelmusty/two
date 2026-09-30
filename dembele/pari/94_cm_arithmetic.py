"""Audit exact CM residue data separately from the unknown section evaluations.

Run with sage -python. No analytic solve or algebraic recognition is performed.
The Harbater algebra below is an available arithmetic input, NOT an equation
for the curve or for the values of the functions constructed in D56.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

import mpmath as mp
from sage.all import GF, QQ, NumberField, PolynomialRing


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
GP = Path("/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/10.6/local/bin/gp")
FIELD_COEFFICIENTS = [2, 0, -16, 0, 20, 0, -8, 0, 1]
# Elkies's polynomial, Dembélé 1906.06772v2, Remark 6.2.
HARBATER_COEFFICIENTS = [68, -2, -128, 16, 80, 40, 32, -80, -32,
                       64, 0, -16, 16, 8, 0, 0, -2, 1]


def source(path):
    path = Path(path)
    return {"path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def normalize_pair(x, y, average):
    """D56 normalization in an exact algebra with an F-valued average trace."""
    xc = x - average(x)
    m2, m3 = average(xc**2), average(xc**3)
    if not m2 or not m3:
        raise ValueError("zero second or third X moment")
    xx = m2 / m3 * xc
    yc = y - average(y)
    z = yc - average(yc * xx) / average(xx**2) * xx
    n2, n3 = average(z**2), average(z**3)
    if not n2 or not n3:
        raise ValueError("zero second or third Y moment")
    return xx, n2 / n3 * z


def constraints(x, y, average):
    return [average(x), average(y), average(x*y),
            average(x*x-x**3), average(y*y-y**3)]


def cm_cyclic_field():
    """Verify the cyclic degree-16 CM field, including complex conjugation."""
    ring = PolynomialRing(QQ, "s")
    s = ring.gen()
    g = ring(FIELD_COEFFICIENTS)(-s*s-2)
    field = NumberField(g, "beta")
    beta = field.gen()
    image = beta**3+3*beta
    assert g.is_irreducible() and g(image) == 0
    sigma = field.hom([image], field)
    orbit = [beta]
    for _ in range(16):
        orbit.append(sigma(orbit[-1]))
    assert len(set(orbit[:16])) == 16 and orbit[16] == beta and orbit[8] == -beta
    return {"polynomial_coefficients_ascending": [str(c) for c in g.list()],
            "generator_relation": "beta^2=-2-b",
            "automorphism": "beta -> beta^3+3*beta",
            "automorphism_order": 16,
            "eighth_power": "beta -> -beta (complex conjugation)",
            "class_number": 17,
            "class_number_provenance": "Dembélé sections 5.2 and 5.4; not recomputed here"}


def exact_examples():
    ring = PolynomialRing(QQ, "t")
    h = ring(HARBATER_COEFFICIENTS)
    field = NumberField(h, "theta")
    theta = field.gen()
    average = lambda v: v.trace() / 17
    examples = []
    elements = []
    for label, (x, y) in zip(["theta,theta^2", "theta^2,theta^3"],
                             [(theta, theta**2), (theta**2, theta**3)]):
        xx, yy = normalize_pair(x, y, average)
        checks = constraints(xx, yy, average)
        assert all(v == 0 for v in checks)
        assert xx.minpoly().degree() == 17
        elements.append((xx, yy))
        examples.append({
            "input": label,
            "status": "counterexample in the residue algebra; NOT target curve values",
            "X_power_basis": [str(v) for v in xx.list()],
            "Y_power_basis": [str(v) for v in yy.list()],
            "five_trace_constraints": [str(v) for v in checks],
            "E_X2": str(average(xx**2)), "E_Y2": str(average(yy**2)),
            "X_minpoly_degree": int(xx.minpoly().degree()),
        })
    # Different second moments exclude even a permutation of the embeddings.
    assert average(elements[0][0]**2) != average(elements[1][0]**2)
    return h, field, elements, examples


def reduction_report(h, elements, prime):
    """Reduce the KNOWN algebra and the counterexamples, never the target maps."""
    k = GF(prime)
    if not k(17):
        raise ValueError("average trace divides by 17")
    hp = h.change_ring(k)
    if not hp.is_squarefree():
        raise ValueError("power-basis order is not etale at this prime")
    algebra = hp.parent().quotient(hp, "theta_bar")
    average = lambda v: v.matrix().trace() / k(17)
    samples = []
    for xx, yy in elements:
        x = algebra(xx.polynomial().change_ring(k))
        y = algebra(yy.polynomial().change_ring(k))
        checks = constraints(x, y, average)
        assert not any(checks)
        samples.append({"five_trace_constraints": [int(v) for v in checks],
                        "E_X2": int(average(x*x)), "E_Y2": int(average(y*y))})
    # These are split primes of F, so the displayed algebras are over F_p.
    fp = PolynomialRing(k, "b")(FIELD_COEFFICIENTS)
    assert sorted(f.degree() for f, e in fp.factor() for _ in range(e)) == [1]*8
    roots = sorted(int(r) for r, _ in fp.roots())
    return {"prime": prime,
            "F_factor_degrees": [1]*8,
            "F_roots": roots,
            "CM_quadratic_splits_at_F_roots": [bool(k(-2-r).is_square()) for r in roots],
            "residue_algebra_factor_degrees": sorted(int(f.degree()) for f, e in hp.factor() for _ in range(e)),
            "factor_coefficients_ascending": [[int(v) for v in f.list()] for f, _ in hp.factor()],
            "example_reductions": samples,
            "target_X_Y_reductions": None}


def saved_embedding_audit(gp):
    """Recover exact square witnesses from the SAME saved elliptic generators."""
    commands = r'''read("fdom.gp");
coeffstrings(z)=vector(8,j,Str(polcoef(lift(z),j-1)));
{
X=read("../../data/computed/normalizer_domain.bin");
A=afuchalg(X); F=algcenter(A); E=afuchelliptic(X);
orders=Vec(afuchsignature(X)[2]); count=0;
for(i=1,#E,if(orders[i]==2,
  tr=algtrace(A,E[i]); nr=algnorm(A,E[i]); delta=tr^2-4*nr;
  roots=nfroots(F,x^2-delta/(-2-Mod(y,F.pol)));
  if(tr!=0 || #roots!=2,error("wrong order-two CM field"));
  if(algpow(A,E[i],2)!=alg1ijktobasis(A,[-nr,0,0,0]~),error("quaternion square check"));
  print("CM|",i-1,"|",coeffstrings(tr),"|",coeffstrings(nr),"|",coeffstrings(roots[1]));
  count++;
));
if(count!=17,error("wrong CM point count"));
print("PASS|94_cm_embeddings");
}
quit;
'''
    result = subprocess.run([str(gp), "-fq", "-s", "128000000"], input=commands,
                            text=True, capture_output=True, timeout=90,
                            cwd=ROOT / "dembele/vendor/rickards-fdom")
    if result.returncode or "PASS|94_cm_embeddings" not in result.stdout:
        raise RuntimeError(result.stdout + result.stderr)
    ring = PolynomialRing(QQ, "b")
    field = NumberField(ring(FIELD_COEFFICIENTS), "b")
    b = field.gen()
    entries = []
    for line in result.stdout.splitlines():
        if not line.startswith("CM|"):
            continue
        _, index, trace, norm, witness = line.split("|")
        arrays = [json.loads(v) for v in (trace, norm, witness)]
        tr, nr, s = [field([QQ(c) for c in v]) for v in arrays]
        assert tr == 0 and tr**2 - 4*nr == (-2-b)*s**2
        entries.append({"point_index": int(index), "trace": arrays[0],
                        "norm": arrays[1], "square_witness": arrays[2]})
    assert [v["point_index"] for v in entries] == list(range(17))
    return {"domain_source": source(DATA / "normalizer_domain.bin"),
            "geometry_source": source(DATA / "expansion_geometry.json"),
            "identity": "Tr(q)^2-4*Nrd(q)=(-2-b)*s^2",
            "CM_field": "F(sqrt(-2-b))", "entries": entries,
            "status": "exact identities in F; no function values evaluated"}


def numerical_comparison(path):
    data = json.loads(path.read_text())
    with mp.workdps(60):
        rows = {}
        for name in ("current", "previous", "alternate_fit"):
            values = data["canonical_cm_normalizations"][name]
            xs = [mp.mpc(*v) for v in values["normalized_x_values"]]
            ys = [mp.mpc(*v) for v in values["normalized_y_values"]]
            e2 = sum(x*x for x in xs)/17
            ey2 = sum(y*y for y in ys)/17
            rows[name] = (e2, ey2)
        current = rows["current"]
        return {"source": source(path),
                "E_X2": [mp.nstr(v, 35) for v in (current[0].real, current[0].imag)],
                "E_Y2": [mp.nstr(v, 35) for v in (current[1].real, current[1].imag)],
                "checkpoint_change_E_X2": mp.nstr(abs(current[0]-rows["previous"][0]), 22),
                "same_checkpoint_fit_change_E_X2": mp.nstr(abs(current[0]-rows["alternate_fit"][0]), 22),
                "distance_to_counterexample_E_X2": [mp.nstr(abs(current[0]-mp.mpf(16)/225),22),
                                                    mp.nstr(abs(current[0]+mp.mpf(32)/5041),22)],
                "status": "empirical comparison, not a certified error or recognition"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gp", type=Path, default=GP)
    parser.add_argument("--cm-report", type=Path, default=DATA / "cm_pointed_maps_flag_16384.json")
    parser.add_argument("--output", type=Path, default=DATA / "cm_arithmetic_audit.json")
    args = parser.parse_args()
    start = time.monotonic()
    embedding = saved_embedding_audit(args.gp)
    h, field, elements, examples = exact_examples()
    disc = field.discriminant()
    assert h.is_irreducible() and disc == 2**79 and field.signature() == (1, 8)
    index = QQ(h.discriminant()/disc).sqrt()
    assert index in QQ and index.denominator() == 1
    reductions = [reduction_report(h, elements, p) for p in [31, 97, 127, 191]]
    assert reductions[0]["residue_algebra_factor_degrees"] == [17]
    assert all(row["residue_algebra_factor_degrees"] == [1]+[2]*8 for row in reductions[1:])
    report = {
        "status": "exact CM input audit complete; target section evaluations unavailable",
        "script_source": source(Path(__file__)),
        "saved_elliptic_embeddings": embedding,
        "CM_cyclic_field": cm_cyclic_field(),
        "residue_algebra_input": {
            "polynomial_coefficients_ascending": HARBATER_COEFFICIENTS,
            "polynomial_source": "https://arxiv.org/pdf/1906.06772, Remark 6.2 (Elkies)",
            "field_discriminant": str(disc), "signature": list(map(int, field.signature())),
            "power_order_index": str(index),
            "irreducible_over_Q": True,
            "irreducible_over_F_certificate": "irreducible modulo 31; 31 splits completely in F",
            "CM_divisor_identification": "uses CM reciprocity and the published Harbater class-field identification; no labelled embedding is constructed",
        },
        "exact_counterexamples": examples,
        "finite_residue_algebras": reductions,
        "saved_target_comparison": numerical_comparison(args.cm_report),
        "reconstruction_target": {
            "algebra": "A_D=H^0(D,O_D), represented abstractly by F[t]/H(t)",
            "missing_data": "ev_D L(17P) subset ev_D L(18P) subset A_D, of dimensions 2 and 3 containing 1",
            "dimension_condition": "D56 ordinarity and nonzero moments imply injectivity; those hypotheses remain numerically supported",
            "flag_parameter_count": 29,
            "known_exact_target_values": 0,
            "known_target_finite_reductions": 0,
            "recognition_height_bound": None,
        },
        "limitations": [
            "The example elements satisfy the trace conditions but are not asserted to extend with the required poles on C.",
            "Residue-field Frobenius permutations do not evaluate X or Y.",
            "CM conjugates at one embedding of F do not supply the other seven embeddings of their F-valued traces.",
            "No new analytic bank, curve equation, torsion point, or target field polynomial is computed.",
        ],
        "wall_seconds": time.monotonic()-start,
    }
    output = json.dumps(report, indent=2, allow_nan=False)+"\n"
    args.output.write_text(output)
    args.output.with_suffix(".out").write_text(output)
    print(report["status"])
    print("Exact saved CM embeddings:", len(embedding["entries"]))
    print("Residue algebra reductions:", [(r["prime"], r["residue_algebra_factor_degrees"]) for r in reductions])
    print("Different normalized second moments:", [r["E_X2"] for r in examples])
    print("Saved target comparison:", report["saved_target_comparison"])


if __name__ == "__main__":
    main()

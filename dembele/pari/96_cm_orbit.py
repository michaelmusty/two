"""D59: label the saved CM embeddings by ideal classes and Frobenius.

Run with sage -python after magma/96_cm_root_action.m. Quaternion and
ideal calculations are exact. The choice of complex embedding is made
explicitly from the saved disk action and checked at high precision.
No values of the target functions are recognized by this script.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import time

import mpmath as mp
from sage.all import AA, NumberField, PolynomialRing, QQ, Qp, QuaternionAlgebra, ZZ, matrix, vector


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("cm_arithmetic", Path(__file__).with_name("94_cm_arithmetic.py"))
arithmetic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arithmetic)


def export_quaternions(gp):
    commands = r'''read("fdom.gp");
vecq(q)=concat(vector(4,j,vector(8,k,Str(polcoef(lift(q[j]),k-1)))));
{
X=read("../../data/computed/normalizer_domain.bin");
A=afuchalg(X); ord=afuchorder(X); E=afuchelliptic(X);
if(matsize(ord)!=[32,32],error("wrong order size"));
if(!algisorder(A,ord),error("saved lattice is not an order"));
if(Vec(afuchsignature(X)[2])[1..17]!=vector(17,j,2),error("wrong point order"));
print("DATA|{\"order_basis\":",vector(32,j,vecq(algbasisto1ijk(A,ord[,j]))),
      ",\"elliptics\":",vector(17,j,vecq(algbasisto1ijk(A,E[j]))),"}");
print("PASS|96_export");
}
quit;
'''
    result = subprocess.run([str(gp), "-fq", "-s", "128000000"], input=commands,
                            text=True, capture_output=True, timeout=60,
                            cwd=ROOT / "dembele/vendor/rickards-fdom")
    if result.returncode or "PASS|96_export" not in result.stdout:
        raise RuntimeError(result.stdout+result.stderr)
    return json.loads(next(line[5:] for line in result.stdout.splitlines() if line.startswith("DATA|")))


def preimage_lattice(order_inverse, embedding_matrix):
    """Columns span {c in Q^d : order_inverse*embedding_matrix*c integral}."""
    w = order_inverse*embedding_matrix
    denominator = w.denominator()
    rows = matrix(ZZ, denominator*w).row_module(ZZ).basis_matrix()
    if rows.nrows() != w.ncols():
        raise ValueError("embedding must have full column rank")
    columns = denominator*rows.change_ring(QQ).inverse()
    assert all(c in ZZ for c in (w*columns).list())
    return columns


def cm_orbit(raw, base_index=8):
    ring = PolynomialRing(QQ, "s")
    s = ring.gen()
    f = ring(arithmetic.FIELD_COEFFICIENTS)
    field = NumberField(f, "b")
    b = field.gen()
    algebra = QuaternionAlgebra(field, b-b*b, -1)
    def from_vector(v):
        return algebra([field([QQ(c) for c in v[8*j:8*(j+1)]]) for j in range(4)])
    def coordinates(q):
        return vector(QQ, sum([list(c.vector()) for c in q.coefficient_tuple()], []))
    order = matrix(QQ, [coordinates(from_vector(v)) for v in raw["order_basis"]]).transpose()
    inverse = order.inverse()
    witness = -4*b**6+22*b**4-28*b*b+4*b+2
    betas = [2/witness*from_vector(v) for v in raw["elliptics"]]
    assert len(betas) == 17 and all(z*z == algebra(-2-b) for z in betas)
    real_places = field.embeddings(AA)
    split = next(emb for emb in real_places if 0 < emb(b) < 1)
    cm = NumberField(f(-s*s-2), "beta")
    classes = cm.class_group(proof=True)
    assert classes.order() == 17 and list(classes.invariants()) == [17]
    integral_basis = cm.integral_basis()
    integral_matrix = matrix(QQ, [v.vector() for v in integral_basis]).transpose()
    base = betas[base_index]
    def embed(elt, generator=base):
        return sum((algebra(c)*generator**j for j,c in enumerate(elt.list())), algebra(0))
    embedded = [embed(v) for v in integral_basis]
    entries = []
    for i, beta_i in enumerate(betas):
        orientation = 1
        if i == base_index:
            u = algebra(1)
        else:
            u = beta_i+base
            if u == 0 or split(u.reduced_norm()) < 0:
                orientation, beta_i = -1, -beta_i
                u = beta_i+base
        assert u != 0 and all(place(u.reduced_norm()) > 0 for place in real_places)
        assert beta_i*u == u*base
        # Embedding the full ring of integers proves optimality in the order.
        assert all(c in ZZ for z in integral_basis for c in inverse*coordinates(embed(z, beta_i)))
        image = matrix(QQ, [coordinates(u*z) for z in embedded]).transpose()
        columns = preimage_lattice(inverse, image)
        generators = [sum((columns[j,k]*integral_basis[j] for j in range(16)), cm(0)) for k in range(16)]
        ideal = cm.fractional_ideal(generators)
        actual = matrix(QQ, [z.vector() for z in ideal.basis()]).transpose()
        change = (integral_matrix*columns).inverse()*actual
        # Do not silently enlarge the intersection when forming its O_K-span.
        assert abs(change.det()) == 1 and all(c in ZZ for c in change.list())
        # I*O subset u^-1*O follows from the intersection and closure of O.
        # These equal covolumes then prove equality, the reciprocity certificate.
        norm_product = ideal.norm()*u.reduced_norm().norm()
        assert norm_product == 1
        power = int(classes(ideal).list()[0])
        entries.append({
            "point_index": i, "orientation_sign": orientation,
            "ideal_class": power, "ideal_norm": str(ideal.norm()),
            "intertwiner_quaternion_coordinates": [str(c) for c in coordinates(u)],
            "ideal_basis_power_coordinates": [[str(c) for c in z.list()] for z in ideal.basis()],
            "full_integer_ring_embeds": True,
            "intersection_equals_ideal_lattice": True,
            "ideal_norm_times_intertwiner_norm": str(norm_product),
        })
    assert sorted(row["ideal_class"] for row in entries) == list(range(17))
    generator_ideal = classes.gen().ideal()
    report = {
        "CM_polynomial_ascending": [str(c) for c in cm.defining_polynomial()],
        "class_number_proved": 17, "class_group_invariants": [17],
        "class_generator_ideal_basis": [[str(c) for c in z.list()] for z in generator_ideal.basis()],
        "base_point_index": base_index,
        "class_labels_in_point_order": [row["ideal_class"] for row in entries],
        "construction": "I_i={a in K : u_i*iota_0(a) in O}; I_i*O=u_i^-1*O",
        "entries": entries,
    }
    return report, cm, classes


def parse_root_action(path):
    text = path.read_text()
    if "PASS|96_cm_root_action" not in text or "PADIC_PROOF|true" not in text:
        raise ValueError("root-action log lacks its completion/proof markers")
    def array(tag):
        return json.loads(text.split(tag+"|", 1)[1].split("\n", 1)[0].strip())
    roots = [[a.strip(), b.strip()] for _,a,b in re.findall(r"ROOT\|(\d+)\|([^\n|]+)\|([^\n|]+)", text)]
    if len(roots) != 17:
        raise ValueError("expected seventeen labelled roots")
    return {
        "source": arithmetic.source(path), "group_order": 272, "p_adic_galois_proof": True,
        "complex_roots": roots,
        "complex_to_padic": array("COMPLEX_TO_PADIC"),
        "complex_frobenius_31": array("COMPLEX_FROBENIUS"),
        "padic_frobenius_31": array("PADIC_FROBENIUS"),
        "resolvent_ascending": array("RESOLVENT"),
        "resolvent_coefficient_bound": str(array("RESOLVENT_COEFFICIENT_BOUND")),
        "lift_modulus": str(array("LIFT_MODULUS")),
        "kappa_mod31_60": str(array("PADIC_KAPPA_MOD31_60")),
        "kappa_complex": [v.strip() for v in text.split("COMPLEX_KAPPA|",1)[1].split("\n",1)[0].split("|")],
        "complex_action_provenance": "Magma complex Galois calculation, compared by GaloisGroupConjugation with the proved 31-adic calculation; complex GaloisProof is not implemented",
    }


def cm_embedding_value(geometry, base_index):
    """Select the CM embedding using the eigenvalue on the saved fixed line."""
    with mp.workdps(90):
        raw = json.loads(geometry.read_text(), parse_float=str)
        a, c = [mp.mpc(*pair) for pair in raw["elliptic_actions"][base_index]]
        linear = mp.conj(a)-a
        disc = linear**2+4*mp.conj(c)*c
        points = [(-linear+sign*mp.sqrt(disc))/(2*mp.conj(c)) for sign in (1,-1)]
        point = next(z for z in points if abs(z) < 1)
        eigenvalue = mp.conj(c)*point+mp.conj(a)
        b = 2*mp.cos(7*mp.pi/16)
        square = -4*b**6+22*b**4-28*b*b+4*b+2
        sign = int(mp.sign(square*eigenvalue.imag))
        beta = sign*1j*mp.sqrt(2+b)
        return beta, {
            "source": arithmetic.source(geometry), "beta_imaginary_sign": sign,
            "normalized_eigenvalue": [mp.nstr(eigenvalue.real,60), mp.nstr(eigenvalue.imag,60)],
            "eigenvalue_distance_from_chosen_sign": mp.nstr(abs(eigenvalue-mp.sign(eigenvalue.imag)*1j),25),
            "status": "complex orientation selected from the saved numerical disk action, not a new error certificate",
        }


def match_frobenius(orbit, cm, classes, action, geometry):
    with mp.workdps(90):
        beta_c, orientation = cm_embedding_value(geometry, orbit["base_point_index"])
        kappa = mp.mpc(*action["kappa_complex"])
        ring = PolynomialRing(QQ, "t")
        resolvent = ring(action["resolvent_ascending"])
        candidates = resolvent.roots(cm, multiplicities=False)
        assert len(candidates) == 16
        evaluate = lambda z: sum(mp.mpf(str(c))*beta_c**j for j,c in enumerate(z.list()))
        candidates.sort(key=lambda z: abs(evaluate(z)-kappa))
        gamma = candidates[0]
        error = abs(evaluate(gamma)-kappa)
        separation = min(abs(evaluate(z)-kappa) for z in candidates[1:])
        assert error < mp.mpf("1e-65") and separation > mp.mpf("1e-3")
        assert gamma.minpoly().list() == resolvent.list()
        local = Qp(31,70)
        local_kappa = local(ZZ(action["kappa_mod31_60"]))
        beta_roots = cm.defining_polynomial().roots(local, multiplicities=False)
        pg = gamma.polynomial().change_ring(local)
        valuations = [(pg(v)-local_kappa).valuation() for v in beta_roots]
        assert max(valuations) >= 60 and sum(v >= 60 for v in valuations) == 1
        beta_local = beta_roots[valuations.index(max(valuations))]
        residue = ZZ(beta_local.residue())
        prime = cm.ideal(31,cm.gen()-residue)
        assert prime.norm() == 31
        exponent = int(classes(prime).list()[0])
        assert exponent % 17
        roots = [mp.mpc(*z) for z in action["complex_roots"]]
        real_index = next(i for i,z in enumerate(roots) if z.imag == 0)
        cycle, current = [], real_index
        for _ in range(17):
            cycle.append(current)
            current = action["complex_frobenius_31"][current]-1
        assert current == real_index and len(set(cycle)) == 17
        inverse = pow(exponent,-1,17)
        lookup = [cycle[(inverse*c)%17] for c in orbit["class_labels_in_point_order"]]
        return {
            "orientation": orientation,
            "resolvent_generator_in_K": [str(c) for c in gamma.list()],
            "complex_generator_match_error": mp.nstr(error,30),
            "complex_generator_next_match_distance": mp.nstr(separation,30),
            "padic_generator_match_valuation": int(max(valuations)),
            "beta_mod31": int(residue), "prime_norm": 31, "prime_ideal_class": exponent,
            "frobenius_root_cycle_zero_based": cycle,
            "point_to_root_index_zero_based": lookup,
            "reference_root": "the unique real root; reference CM point 8 is checked against the saved conjugation pattern",
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gp", type=Path, default=arithmetic.GP)
    parser.add_argument("--root-action", type=Path, default=DATA/"cm_root_action.out")
    parser.add_argument("--output", type=Path, default=DATA/"cm_orbit.json")
    args = parser.parse_args()
    start = time.monotonic()
    raw = export_quaternions(args.gp)
    orbit, cm, classes = cm_orbit(raw)
    action = parse_root_action(args.root_action)
    matching = match_frobenius(orbit, cm, classes, action, DATA/"expansion_geometry.json")
    report = {
        "status": "exact CM ideal classes and arithmetic root matching computed; no target value recognized",
        "script_source": arithmetic.source(Path(__file__)),
        "helper_source": arithmetic.source(Path(arithmetic.__file__)),
        "magma_script_source": arithmetic.source(ROOT/"dembele/magma/96_cm_root_action.m"),
        "domain_source": arithmetic.source(DATA/"normalizer_domain.bin"),
        "quaternion_export": raw, "CM_orbit": orbit,
        "field_root_action": action, "matching": matching,
        "limitations": [
            "CM reciprocity identifies the ideal action with Galois action; that theorem is an input.",
            "The archimedean orientation uses the saved disk action, and root numbering uses Magma's complex/p-adic comparison.",
            "The reference CM point is selected by the saved real/conjugate pattern; no target analytic error enclosure is supplied.",
            "No section evaluations, target function coefficients, or curve equations are certified by these ideal calculations.",
        ],
        "wall_seconds": time.monotonic()-start,
    }
    output = json.dumps(report, indent=2, allow_nan=False)+"\n"
    args.output.write_text(output)
    args.output.with_suffix(".out").write_text(output)
    print(report["status"])
    print("Class labels:",orbit["class_labels_in_point_order"])
    print("Prime (31,beta-%s) has class %s" % (matching["beta_mod31"],matching["prime_ideal_class"]))
    print("Point-to-root matching:",matching["point_to_root_index_zero_based"])


if __name__ == "__main__":
    main()

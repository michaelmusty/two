"""D91: remove all powers of the division-place uniformizer beta.

The output is a finite list of primitive central-unit classes. Their
entire beta strings can be summed geometrically because U_p2=+1.
This is not a complete list of primitive classes.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path
from sage.all import QQ, ZZ, NumberField, PolynomialRing, QuaternionAlgebra, matrix, vector

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def source(p):
    return {"path": str(p.relative_to(ROOT)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def main():
    paths = [DATA / name for name in ["cm_orbit.json", "nelson_cm_lattice_d90.json", "nelson_unfolding_data_d91.json"]]
    raw, local, pilot = [json.loads(p.read_text()) for p in paths]
    R = PolynomialRing(QQ, "s"); s = R.gen()
    F = NumberField(s**8-8*s**6+20*s**4-16*s*s+2, "b"); b = F.gen()
    B = QuaternionAlgebra(F, b-b*b, -1)
    def quat(v): return B([F([QQ(c) for c in v[8*j:8*(j+1)]]) for j in range(4)])
    def coords(q): return vector(QQ, sum([list(c.vector()) for c in q.coefficient_tuple()], []))
    basis = [quat(v) for v in raw["quaternion_export"]["order_basis"]]
    O = matrix(QQ, [coords(q) for q in basis]).transpose(); inv = O.inverse()
    beta = quat(local["arithmetic"]["CM_beta_power_coordinates"])
    def integral(q): return all(c in ZZ for c in inv*coords(q))
    assert integral(beta) and beta*beta == B(-2-b)
    # Multiplication preserves O; beta O has index Norm(pi)^2=4.
    left = matrix(QQ, [inv*coords(beta*q) for q in basis]).transpose()
    assert all(c in ZZ for c in left.list()) and abs(left.det()) == 4
    groups = {}; records = []; origins = []
    roots = [x for x in range(31) if (x**8-8*x**6+20*x**4-16*x*x+2) % 31 == 0]
    for entry in pilot["unit_classes"]:
        original = quat(entry["quaternion_power_coordinates"])
        exponent = ZZ(entry["norm_ideal_norm"]).valuation(2)
        q = beta**(-exponent)*original
        assert integral(q) and not integral(beta**(-1)*q)
        n = q.reduced_norm(); nn = ZZ(n.norm()); assert nn in [1,31]
        parallel = (q+beta*q*beta**(-1))/2
        A = nn*parallel.reduced_norm()/n
        old_A = F([QQ(c) for c in entry["multiplicative_majorant_field_element"]])
        assert old_A == 2**exponent*A
        cs = q.coefficient_tuple(); pivot = next(c for c in cs if c != 0)
        key = (tuple(tuple(c/pivot) for c in cs), int(nn))
        matching = None
        for previous in groups.get(key, []):
            unit = pivot/previous["pivot"]
            if unit.is_integral() and (1/unit).is_integral():
                assert q == unit*previous["q"] and abs(unit.norm()) == 1
                matching = previous; break
        if matching is None:
            if nn == 1: bucket = "known"
            else:
                csn = list(n.vector())
                zeros = [x for x in roots if sum(ZZ(c.numerator())*pow(int(c.denominator()),-1,31)*pow(x,i,31)
                                                    for i,c in enumerate(csn)) % 31 == 0]
                assert len(zeros) == 1; bucket = "a31_b"+str(zeros[0])
            record = {"index": len(records), "norm_ideal_norm": int(nn), "Hecke_bucket": bucket,
                      "quaternion_power_coordinates": [str(c) for c in coords(q)],
                      "norm_generator": [str(c) for c in n.vector()],
                      "multiplicative_majorant_field_element": [str(c) for c in A.vector()],
                      "mixed": q != parallel, "input_indices": []}
            records.append(record)
            matching = {"index":record["index"], "q":q, "pivot":pivot}
            groups.setdefault(key,[]).append(matching); unit = F(1)
        records[matching["index"]]["input_indices"].append(entry["index"])
        origins.append({"pilot_index":entry["index"], "primitive_index":matching["index"],
                        "beta_exponent":int(exponent), "unit_power_coordinates":[str(c) for c in unit.vector()]})
    assert len(records) == 29
    assert Counter(r["Hecke_bucket"] for r in records) == {"known":9,"a31_b10":12,"a31_b20":4,"a31_b21":4}
    # Explicitly show why the old shell cannot serve as a global tail.
    # beta times any norm-one mixed representative is a missing norm-two
    # mixed class: the old list has only a pure-K norm-two class.
    r = next(r for r in records if r["mixed"] and r["norm_ideal_norm"] == 1)
    missing = beta*quat(r["quaternion_power_coordinates"])
    assert integral(missing) and missing.reduced_norm().norm() == 2
    assert all(not t["mixed"] for t in pilot["unit_classes"] if t["norm_ideal_norm"] == 2)
    result = {"status":"pass: primitive finite class set and exact beta strings",
              "primitive_classes":records, "pilot_decomposition":origins,
              "bucket_counts":dict(Counter(r["Hecke_bucket"] for r in records)),
              "beta_left_multiplication_in_order_basis":[[str(c) for c in row] for row in left.rows()],
              "missing_old_pilot_class":{"primitive_index":r["index"],
                  "quaternion_power_coordinates":[str(c) for c in coords(missing)],
                  "norm_ideal_norm":2, "mixed":True},
              "beta_string_Mellin_multiplier":"1/(1-2^(-s-1))",
              "two_cusps_and_beta_strings":"(1+2^s)/(1-2^(-s-1))",
              "complete_primitive_class_cutoff":False, "Shimura_derivative_computed":False,
              "sources":[source(p) for p in [Path(__file__)]+paths]}
    out = DATA/"nelson_primitive_classes_d91.json"; assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("Primitive classes:",len(records),"Hecke buckets:",result["bucket_counts"])
    print("PASS|329_nelson_primitive_classes")


if __name__ == "__main__": main()

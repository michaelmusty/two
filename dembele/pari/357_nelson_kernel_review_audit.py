"""D94 rational audit: contour weights, local contraction arithmetic, provenance.

No Sage is needed. Arb nodes are hash-bound, not recomputed here. The
local analytic proof is in the bound report; global comparison is open.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import comb, factorial, ceil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUTPUT = DATA / "nelson_kernel_review_d94.json"
spec = importlib.util.spec_from_file_location("arithmetic", Path(__file__).with_name("334_nelson_unfolding_audit.py"))
arith = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arith)
mat = arith.mat


def multiply(p, q):
    out = [Q(0)] * (len(p)+len(q)-1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i+j] += x*y
    return out


def at(p, x):
    value = Q(0)
    for a in reversed(p):
        value = value*x+a
    return value


def reflected(p):
    return [sum(p[j]*comb(j,i)*(-1)**i for j in range(i,len(p))) for i in range(len(p))]


def read_interval(row):
    lo, hi = Q(row["lower"]), Q(row["upper"])
    assert lo <= hi
    assert all(v.denominator & (v.denominator-1) == 0 for v in (lo, hi))
    return lo, hi


def intervals(value):
    if isinstance(value, dict):
        if "lower" in value and "upper" in value:
            yield read_interval(value)
        else:
            for child in value.values():
                yield from intervals(child)
    elif isinstance(value, list):
        for child in value:
            yield from intervals(child)


def weights_and_tails(packet):
    assert packet["precision_bits"] == 320 and packet["mesh_denominator"] == 128
    assert packet["vertical_height"] == 16
    assert not packet["global_test_vector_identified"] and not packet["Shimura_derivative_computed"]
    assert packet["nonzero_weight_requires_new_partial_sums"]
    seen = set()
    best = {str(m): {} for m in (0,1,2,4)}
    rounded = []
    z0 = read_interval(packet["Z0"])
    for row in packet["rows"]:
        c, m, r = Q(row["contour"]), row["weight_power"], Q(row["weight_parameter"])
        assert Q(3,2) < c <= 2 and r == c*(c-1)
        assert (c,m) not in seen
        seen.add((c,m))
        W = [Q(-1), Q(2)]
        for _ in range(m):
            W = multiply(W, [Q(1), 1/r, -1/r])
        assert W == list(map(Q,row["W_coefficients"]))
        assert reflected(W) == [-v for v in W]
        H = [v/2 for v in W]
        H[0] += Q(1,2)
        assert H == list(map(Q,row["H_coefficients"]))
        assert at(H,0) == 0 and at(H,1) == 1
        assert row["can_use_D93_partial_sums"] == (m == 0)
        mass = read_interval(row["omitted_divisor_mass"])
        orbit = read_interval(row["whole_orbit_moment"])
        assert mass[0] > 0 and orbit[0] > 1
        # Raising to the denominator verifies the rational-power bound.
        assert (1-1/orbit[1])**c.denominator >= Q(2,9)**c.numerator
        bounds = {}
        for a in (1,3,5):
            bsum = Q(0)
            for j in (2,a+2):
                record = row["constants"][str(a)][str(j)]
                p = [Q(1)]
                for _ in range(31):
                    p = multiply(p,[Q(2),Q(1)])
                for shift in range(a+2):
                    p = multiply(p,[Q(2+shift),Q(1)])
                p = multiply(multiply(p,[Q(3),Q(2)]),[Q(2+j),Q(1)])
                for _ in range(m):
                    p = multiply(p,[1+2/r,3/r,1/r])
                assert p == list(map(Q,record["tail_polynomial"])) and all(x>0 for x in p)
                integral = sum(x*sum(Q(comb(k,v)*16**(k-v)*factorial(v),24**(v+1))
                                     for v in range(k+1)) for k,x in enumerate(p))
                assert integral == Q(record["tail_integral_before_exponential"])
                assert read_interval(record["vertical_tail"])[0] > 0
                lo, hi = read_interval(record["bound"])
                assert lo > 0
                bsum += hi
            value = read_interval(row["all_uncomputed_norm_ideal_bounds"][str(a)])
            upper = ceil(value[1])
            # The integer upper bound covers the full serialized boxes,
            # including any widening beyond the live Arb inputs.
            assert upper**c.denominator*z0[0]**c.numerator > (bsum*orbit[1]*mass[1])**c.denominator
            bounds[str(a)] = str(upper)
            previous = best[str(m)].get(str(a))
            if previous is None or value[1] < previous[0]:
                best[str(m)][str(a)] = (value[1],str(c))
        rounded.append({"contour":str(c),"weight_power":m,"bounds":bounds})
    expected = {(Q(3,2)+Q(1,d),m) for d in (128,64,32,16,8,4,2) for m in (0,1,2,4)}
    assert seen == expected
    choices = {m:{a:v[1] for a,v in rows.items()} for m,rows in best.items()}
    assert choices == packet["best_contours_by_weight_power"]
    assert best["0"]["1"][0] < 2680*10**10
    assert best["1"]["1"][0] < 2257*10**10
    return {"contour_weight_choices":len(seen), "exact_tail_polynomials":6*len(seen),
            "dyadic_interval_records":len(list(intervals(packet))),
            "rounded_up_bounds":rounded, "best_contours_by_weight_power":choices,
            "unchanged_kernel_S11_omitted_bound_rounded_up":"26800000000000",
            "changed_weight_partial_sums_computed":False,
            "analytic_node_replay":"hash-bound 355 Arb run; exact tail polynomials independently replayed"}


def local_arithmetic(packet, raw):
    inverse = tuple(map(Q,packet["inverse_delta_power_coordinates"]))
    delta = tuple(map(Q,packet["delta_power_coordinates"]))
    assert arith.fmul(delta,inverse) == arith.ONE
    assert inverse == (Q(1,8),Q(1,16))+(Q(0),)*6
    multiplication = arith.fmatrix(inverse)
    trace = sum(multiplication[i][i] for i in range(8))
    assert trace == Q(packet["inverse_delta_trace"]) == 1
    assert arith.fnorm(delta) == Q(packet["delta_norm"]) == 2**31
    roots = []
    for i,row in enumerate(packet["real_places"]):
        lo,hi = map(Q,row["b_interval"])
        assert -2 < lo < hi < 2 and at(arith.POLY+[1],lo)*at(arith.POLY+[1],hi) < 0
        assert [str((2+lo)/16),str((2+hi)/16)] == row["inverse_delta_interval"]
        assert row["kind"] == ("split" if i == 4 else "definite")
        assert (lo*(1-hi)>0) if i == 4 else (hi<0 or lo>1)
        roots.append((lo,hi))
    assert len(roots) == 8 and all(roots[i][1]<roots[i+1][0] for i in range(7))
    O = mat.transpose(mat.matrix(raw["quaternion_export"]["order_basis"]))
    C = mat.matrix(packet["order_conjugation_matrix"])
    JO = [row if i<8 else [-v for v in row] for i,row in enumerate(O)]
    assert arith.integral(sum(C,[])) and mat.multiply(O,C) == JO
    assert mat.multiply(C,C) == mat.identity(32) and abs(mat.determinant(C)) == 1
    identity = list(map(Q,packet["identity_in_order_coordinates"]))
    assert arith.integral(identity) and arith.mv(O,identity) == [Q(1)]+[Q(0)]*31
    assert packet["matching_total_K_weight"] == 2-2 == 0
    assert packet["wrong_dual_total_K_weight"] == 2+2 != 0
    assert packet["wrong_dual_angular_average"] == "0"
    assert packet["archimedean_product"] == "exp(-2*pi)"
    assert packet["local_norm_one_contractions_nonzero"]
    for key in ("global_test_vector_identified","D91_Petersson_prefactor_verified",
                "CM_anchor_derivative_nonzero","Shimura_derivative_computed"):
        assert packet[key] is False
    # A wrong trace or a changed conjugation entry cannot pass these identities.
    assert trace != 0
    bad = [row[:] for row in C]
    bad[0][0] += 1
    assert mat.multiply(O,bad) != JO
    return {"isolated_positive_inverse_delta_places":8,"inverse_delta_trace":"1",
            "integral_order_conjugation_replayed":True,"conjugation_corruption_rejected":True,
            "dual_K_type_control_replayed":True,
            "local_integral_proof":"bound D94 report; no claim of global Petersson normalization"}


def compute():
    sources = {}
    def bind(path, expected=None):
        path = Path(path)
        if not path.is_absolute():
            path = ROOT/path
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None:
            assert digest == expected, path
        name = str(path.relative_to(ROOT))
        sources[name] = {"path":name,"sha256":digest}
    def read(name):
        path = DATA/name
        bind(path)
        result = json.loads(path.read_text())
        for row in result.get("sources",[]):
            bind(row["path"],row["sha256"])
        return result
    prior = read("nelson_prime31_exact_d93.json")
    contour = read("nelson_contour_weight_bounds_d94.json")
    local = read("nelson_norm_one_test_vector_d94.json")
    raw = read("cm_orbit.json")
    jobs = []
    for name in ("nelson_contour_weight_d94_attempt01.job.json","nelson_test_vector_d94_attempt01.job.json"):
        job = read(name)
        bind(job["log"]["path"],job["log"]["sha256"])
        assert job["status"] == "pass" and job["exit_code"] == 0
        assert job["timeout_seconds"] == 180 and job["timeout_terminates_process_group"]
        assert job["wall_seconds"] < 180
        jobs.append({"path":str((DATA/name).relative_to(ROOT)),"status":job["status"],"wall_seconds":job["wall_seconds"]})
    bind(Path(__file__))
    bind(Path(arith.__file__))
    bind(Path(mat.__file__))
    bind(ROOT/local["proof_report"])
    return {"status":"pass: contour review and local norm-one contraction; global comparison open",
            "contours":weights_and_tails(contour),"local":local_arithmetic(local,raw),
            "previous_root_hashes_verified":len(prior["sources"]),
            "previous_exhaustive_enumeration_repeated":False,"jobs":jobs,
            "global_test_vector_identified":False,"Shimura_derivative_computed":False,
            "sources":sorted(sources.values(),key=lambda row:row["path"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args = parser.parse_args()
    result = compute()
    if args.check:
        assert result == json.loads(OUTPUT.read_text())
    else:
        assert not OUTPUT.exists()
        OUTPUT.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS|357_nelson_kernel_review_audit",len(result["sources"]),"hashes;",
          result["contours"]["dyadic_interval_records"],"dyadic intervals")


if __name__ == "__main__":
    main()

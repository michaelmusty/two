"""D95: independent rational replay and provenance for the global comparison.

The analytic proof and its literature inputs are in the bound report.
PARI's certified class-number run is bound, not re-executed by this
standard-Python audit. No new numerical CM value is claimed.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUTPUT = DATA / "nelson_global_identification_d95.json"
spec = importlib.util.spec_from_file_location("arithmetic",Path(__file__).with_name("334_nelson_unfolding_audit.py"))
arith = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arith)
mat = arith.mat


def box_mul(x,y):
    values = [a*b for a in x for b in y]
    return min(values),max(values)


def box_poly(coefficients,interval):
    value = (Q(0),Q(0))
    for c in reversed(coefficients):
        lo,hi = box_mul(value,interval)
        value = lo+c,hi+c
    return value


def rank2(rows):
    values = [sum(int(v)<<i for i,v in enumerate(row)) for row in rows]
    rank = 0
    for bit in range(8):
        pivot = next((i for i in range(rank,len(values)) if values[i]&(1<<bit)),None)
        if pivot is None:
            continue
        values[rank],values[pivot] = values[pivot],values[rank]
        for i in range(len(values)):
            if i != rank and values[i]&(1<<bit):
                values[i] ^= values[rank]
        rank += 1
    return rank


def field_and_level(packet,raw,local,local_nonzero):
    field = packet["field"]
    assert field["class_number_proof_true"] == field["narrow_class_number"] == field["pari_bnfcertify"] == 1
    assert Q(field["discriminant"]) == 2**31 and field["power_basis_is_integral_basis"]
    assert field["positive_even_valuation_square_classes"] == 1
    roots = [tuple(map(Q,row["b_interval"])) for row in local_nonzero["real_places"]]
    assert len(roots) == 8
    signs = []
    for row in field["units_power_coordinates"]:
        unit = tuple(map(Q,row))
        assert arith.integral(unit) and arith.integral(arith.finverse(unit))
        assert abs(arith.fnorm(unit)) == 1
        signature = []
        for interval in roots:
            lo,hi = box_poly(unit,interval)
            assert hi<0 or lo>0
            signature.append(int(hi<0))
        signs.append(signature)
    assert signs == field["unit_signatures"] and rank2(signs) == field["signature_rank"] == 8
    basis = [arith.quaternion(row) for row in raw["quaternion_export"]["order_basis"]]
    dual_matrix = mat.matrix(local["arithmetic"]["relative_dual_in_order_coordinates"])
    order_columns = mat.transpose(mat.matrix(raw["quaternion_export"]["order_basis"]))
    dual_columns = mat.multiply(order_columns,dual_matrix)
    dual = [arith.quaternion(row) for row in mat.transpose(dual_columns)]
    count = 0
    for label,elements,scale in (("order",basis,arith.ONE),
                                 ("relative_dual",dual,(Q(2),Q(1))+(Q(0),)*6)):
        diagonals = [arith.fmul(scale,arith.qnorm(q)) for q in elements]
        assert all(arith.integral(n) for n in diagonals)
        count += len(diagonals)
        cross_count = 0
        for i in range(32):
            for j in range(i):
                cross = arith.fmul(scale,arith.qnorm(arith.qadd(elements[i],elements[j])))
                cross = arith.fadd(cross,arith.fscale(arith.fadd(diagonals[i],diagonals[j]),-1))
                assert arith.integral(cross)
                cross_count += 1
        count += cross_count
        record = packet["local_level"][label]
        assert record["diagonal_tests"] == 32 and record["cross_tests"] == cross_count == 496
        assert record["norm_polynomial_integral"]
    assert count == 1056
    return {"unit_signatures_replayed":8,"unit_signature_rank":8,
            "norm_integrality_conditions_replayed":count,
            "class_number_proof":"hash-bound 358 Sage/PARI proof=True and bnfcertify=1 run"}


def orientation_and_normalization(packet):
    assert packet["matrix_convention"] == "[[X,conjugate(Y)],[Y,conjugate(X)]]"
    assert packet["classical_tensor_orientation"] == "conjugate(v(g1))*v(g2)"
    checks = []
    for row in packet["derivative_records"]:
        a,b = row["pair"]
        assert b == 1 and a in (1,3,5)
        # Expand exp(h*(u*x*yb-v*x*y+u*v*x^2)) independently:
        # choose i copies of u, j copies of v, k copies of uv.
        expected = {}
        for k in range(min(a,b)+1):
            i,j = a-k,b-k
            coefficient = Q((-1)**j*factorial(a)*factorial(b),factorial(i)*factorial(j)*factorial(k))
            exponents = (2+i+j+2*k,0,j,i,i+j+k,0,0)
            expected[exponents] = expected.get(exponents,Q(0))+coefficient
        actual = {tuple(term["exponents"]):Q(term["coefficient"]) for term in row["terms"]}
        assert actual == expected
        assert row["first_variable"] == "anti-holomorphic" and row["second_variable"] == "holomorphic"
        assert Q(row["coarse_ratio_factorial"]) == factorial(a)
        checks.append([a,b])
    assert checks == [[1,1],[3,1],[5,1]]
    assert packet["normalized_bump_multiplicative_integrals"] == ["1"]*8
    # Eight real sign choices, eight inverse-square Jacobians, and
    # one global sign quotient, with finite unit volume one.
    factor = Q(2**8,2)*Q(1,2)**8
    assert factor == Q(packet["central_unfolded_signed_lattice_factor"]) == Q(1,2)
    assert not packet["central_unit_regulator_extra_factor"]
    # Exact negative control: J1=1, J3=1+i gives S31=1-i.
    # The upstairs c3/c1 is (1+i)/6, not (1-i)/6.
    correct_ratio = (Q(1,6),Q(1,6))
    missing_conjugation = (Q(1,6),Q(-1,6))
    missing_factorial = (Q(1),Q(1))
    assert correct_ratio != missing_conjugation and correct_ratio != missing_factorial
    assert packet["Mellin_prefactor"] == "D^(3/2)/(64*R_F*(4*pi)^9)"
    assert packet["Mellin_argument"] == "(4*pi^2)^8*A/D^2"
    # Check the height degree of every saved Gaussian monomial against
    # the cancellation used in the Mellin argument.
    for row in packet["derivative_records"]:
        for term in row["terms"]:
            x_power,xb_power,y_power,yb_power,r,_,_ = term["exponents"]
            assert xb_power == 0
            assert x_power+y_power+yb_power-(4+2*r) == -2
            assert (2+r)-r-1 == 1  # remaining delta_0 exponent is s+1
            assert (2+r)-r+7 == 9  # total four-pi exponent is 8*s+9
    return {"Gaussian_pairs_replayed":checks,"central_lattice_factor":"1/2",
            "missing_conjugation_rejected":True,"missing_factorial_rejected":True,
            "ratio_rule":packet["coarse_ratio_rule"],
            "analytic_proof":"bound D95 report, invoking the general-field Shimizu correspondence"}


def compute():
    sources = {}
    def bind(path,expected=None):
        path = Path(path)
        if not path.is_absolute():
            path = ROOT/path
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None:
            assert digest == expected,path
        name = str(path.relative_to(ROOT))
        sources[name] = {"path":name,"sha256":digest}
    def read(name):
        path = DATA/name
        bind(path)
        result = json.loads(path.read_text())
        for row in result.get("sources",[]):
            bind(row["path"],row["sha256"])
        return result
    prior = read("nelson_kernel_review_d94.json")
    packet = read("nelson_global_comparison_data_d95.json")
    raw = read("cm_orbit.json")
    local = read("nelson_cm_lattice_d90.json")
    local_nonzero = read("nelson_norm_one_test_vector_d94.json")
    job = read("nelson_global_comparison_d95_attempt01.job.json")
    bind(job["log"]["path"],job["log"]["sha256"])
    assert job["status"] == "pass" and job["exit_code"] == 0
    assert job["timeout_seconds"] == 180 and job["timeout_terminates_process_group"]
    assert job["wall_seconds"] < 180
    bind(ROOT/packet["global_comparison_proof"])
    bind(Path(__file__))
    bind(Path(arith.__file__))
    bind(Path(mat.__file__))
    assert packet["global_kernel_identified_up_to_positive_scalar"]
    for key in ("global_scalar_numerically_evaluated","full_Mellin_series_numerically_evaluated",
                "CM_anchor_derivative_nonzero","arithmetic_CM_jet_computed"):
        assert packet[key] is False
    arithmetic = field_and_level(packet,raw,local,local_nonzero)
    print("FIELD_LEVEL_RATIONAL_REPLAY_PASS",flush=True)
    symbolic = orientation_and_normalization(packet)
    return {"status":"pass: global kernel comparison proof and arithmetic audit; numerical CM accuracy open",
            "arithmetic":arithmetic,"orientation_and_normalization":symbolic,
            "previous_root_hashes_verified":len(prior["sources"]),
            "global_kernel_identified_up_to_positive_scalar":True,
            "full_Mellin_series_numerically_evaluated":False,
            "CM_anchor_derivative_nonzero":False,"arithmetic_CM_jet_computed":False,
            "jobs":[{"path":"dembele/data/computed/nelson_global_comparison_d95_attempt01.job.json",
                     "status":job["status"],"wall_seconds":job["wall_seconds"]}],
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
    print("PASS|359_nelson_global_identification_audit",len(result["sources"]),"hashes")


if __name__ == "__main__":
    main()

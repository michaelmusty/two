"""D96: sum the positive radial/ideal majorant before bounding its Mellin integral.

Certify 0<K3<K4 and decreasing K4/A on a finite A range. Disjoint
acosh(8) disks give C_N(A)<=32*A/(7*N) within every right orbit.
Stieltjes integration then bounds it by (32/(7*N))*F(N), where
F(N)=K4(Z0*N)+integral_N^infinity K4(Z0*A)dA/A, up to an explicit
finite-range splice. The divisor Euler series sums all ideals exactly.
"""
import importlib.util
import json
from math import comb, factorial
from pathlib import Path
import time
from sage.all import QQ

spec = importlib.util.spec_from_file_location("blocks", Path(__file__).with_name("360_nelson_completed_scalar_blocks.py"))
blocks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blocks)
kernel = blocks.kernel
RB, CB, PI, DATA = kernel.RB, kernel.CB, kernel.PI, kernel.DATA
interval, ball = blocks.interval, blocks.ball
SIGN_RADIUS = QQ(3)/8


def bernstein_matrix(n):
    # x=r*(2*t-1), 0<=t<=1; convert powers of x to degree-n Bernstein coefficients.
    return [[SIGN_RADIUS**m*sum(QQ(comb(m, l)*(-1)**(m-l)*2**l*comb(k, l))/comb(n, l)
                                for l in range(min(m, k)+1))
             for m in range(n+1)] for k in range(n+1)]


def polynomial_lower(coefficients, matrix):
    values = [sum((c*w for c, w in zip(coefficients, row)), RB(0)) for row in matrix]
    index = min(range(len(values)), key=lambda j: values[j].lower())
    return values[index], index


def zeta(c):
    value = kernel.dedekind_zeta(CB(c))
    assert value.imag().contains_zero() and value.real().lower()>1
    return value.real()


def divisor_mass(c):
    x = RB(2)**(-c)
    local = (1-2*x*x)/((1-x)**2*(1-2*x)**2)
    return zeta(c)**2*zeta(c-1)**2/zeta(2*c-1)/local


def sign_certificates(packet, Z0):
    h = ball(packet["log_half_width"])
    assert h.upper()<SIGN_RADIUS
    matrices = {n: bernstein_matrix(n) for n in (30, 31)}
    records = []
    failed = None
    for row in packet["blocks"][:72]:
        j = row["index"]
        hs = [ball(v) for v in row["kernels"]["H"]["finite_Taylor_coefficients"]]
        qs = [ball(v) for v in row["kernels"]["Q"]["finite_Taylor_coefficients"]]
        # Q=e^-x*K4. Recover the K3 coefficients by H+e^x*Q.
        k3 = [hs[m]+sum((qs[l]/factorial(m-l) for l in range(m+1)), RB(0)) for m in range(32)]
        minus_h = [-v for v in hs]
        minus_qprime = [-(m+1)*qs[m+1] for m in range(31)]
        rh = ball(row["kernels"]["H"]["exponential_remainder_bound"])
        rq = ball(row["kernels"]["Q"]["exponential_remainder_bound"])
        e3, e4, e5 = [kernel.quadrature_error(Z0*2**j, k, 32)[0] for k in (3, 4, 5)]
        errors = {"K3": rh/4+e3,
                  "K4_minus_K3": rh+e3+e4,
                  "minus_Qprime": rq*32/h+RB(2).sqrt()*(3*e4+e5)}
        certificates = {}
        for name, coefficients in (("K3", k3), ("K4_minus_K3", minus_h), ("minus_Qprime", minus_qprime)):
            minimum, index = polynomial_lower(coefficients, matrices[len(coefficients)-1])
            margin = minimum-errors[name]
            certificates[name] = {"Bernstein_minimum": interval(minimum), "minimum_index": index,
                                  "error_bound": interval(errors[name]), "positive_margin": interval(margin)}
        record = {"block_index": j, "certificates": certificates}
        if not all(ball(v["positive_margin"]).lower()>0 for v in certificates.values()):
            failed = record
            break
        records.append(record)
    assert len(records)>=48, "Finite positivity range too small for this pilot"
    return {"polynomial_domain_radius": str(SIGN_RADIUS), "certified_block_count": len(records),
            "A_range": ["1", str(2**len(records))], "records": records, "first_uncertified_block": failed}


def real_factor_bounds(c):
    x = RB(2)**(-c-QQ(1)/2)
    reciprocal_local = (1+x)**2*(1+2*x)**2/(1-2*x*x)
    return {"all": zeta(c+QQ(1)/2)**2*zeta(c-QQ(1)/2)**2*reciprocal_local,
            "unit": zeta(2*c), "prime31": 64*RB(31)**(-c-QQ(1)/2)*zeta(2*c)}


def cusp(c):
    return (1+RB(2)**c)/(1-RB(2)**(-c-1))


def quadrature_errors(Z0, denominator):
    boundary = {}
    for c in (2, 3):
        common = Z0**(-c)*cusp(c)*(1+QQ(1)/c)*kernel.gamma_integral_bound(c, 4)
        boundary[c] = {name: common*value for name, value in real_factor_bounds(QQ(c)).items()}
    c = QQ(5)/2
    # Binet: |Gamma(5/2+it)|^16 <= 8^8 exp(8/15) (3+t)^32 exp(-24t).
    polynomial = [QQ(1)]
    for _ in range(39):
        polynomial = kernel.polynomial_times(polynomial, 3, 1)
    polynomial = kernel.polynomial_times(polynomial, 4, 2)
    for j in range(4):
        polynomial = kernel.polynomial_times(polynomial, 3+j, 1)
    assert len(polynomial)-1 == 44 and 44<24*16
    integral = sum(coefficient*sum(QQ(comb(j, r)*16**(j-r)*factorial(r))/24**(r+1)
                                  for r in range(j+1)) for j, coefficient in enumerate(polynomial))
    common_tail = Z0**(-c)*cusp(c)*(1+1/c)*8**8*(RB(QQ(4)/(3*c))-24*16).exp()*RB(integral)/3
    real_factors = real_factor_bounds(c)
    errors = {}
    for name in real_factors:
        strip = (boundary[2][name]+boundary[3][name])/(6*((RB(3*denominator)).exp()-1))
        tail = common_tail*real_factors[name]
        errors[name] = {"strip": interval(strip), "tail": interval(tail), "total": interval(strip+tail)}
    return errors, list(map(str, polynomial)), str(integral)


def completed_ideal_sum(Z0):
    c, denominator, height = QQ(5)/2, 64, 16
    totals = {name: RB(0) for name in ("all", "unit", "prime31")}
    coarse = {name: RB(0) for name in totals}
    log2, log31, logZ = RB(2).log(), RB(31).log(), Z0.log()
    for j in range(height*denominator+1):
        s = CB(c, QQ(j)/denominator)
        two_s = (s*log2).exp()
        base = (2*s-1)*s.gamma()**16*s**7*s*(s+1)*(s+2)*(s+3)
        base *= (1+two_s)/(1-1/(2*two_s))*(1+1/s)*(-s*logZ).exp()
        x = (-(s+QQ(1)/2)*log2).exp()
        reciprocal_local = (1-x)**2*(1-2*x)**2/(1-2*x*x)
        zet = kernel.dedekind_zeta(2*s)
        factors = {"all": kernel.dedekind_zeta(s+QQ(1)/2)**2*kernel.dedekind_zeta(s-QQ(1)/2)**2*reciprocal_local,
                   "unit": zet, "prime31": zet*64*(-(s+QQ(1)/2)*log31).exp()}
        weight = 1 if j == 0 else 2
        for name, factor in factors.items():
            term = weight*(base*factor).real()
            totals[name] += term
            if j % 2 == 0:
                coarse[name] += term
    errors, polynomial, integral = quadrature_errors(Z0, denominator)
    coarse_errors, _, _ = quadrature_errors(Z0, denominator//2)
    values = {}
    for name in totals:
        fine = (totals[name]/(2*PI*denominator)).add_error(ball(errors[name]["total"]).upper())
        rough = (coarse[name]/(PI*denominator)).add_error(ball(coarse_errors[name]["total"]).upper())
        assert fine.overlaps(rough)
        values[name] = {"value": interval(fine), "analytic_error": errors[name],
                        "coarse_value": interval(rough), "coarse_analytic_error": coarse_errors[name],
                        "coarse_grid_overlaps": True}
    omitted = ball(values["all"]["value"])-ball(values["unit"]["value"])-ball(values["prime31"]["value"])
    return {"contour": str(c), "step_denominator": denominator, "height": height, "strip_half_width": "1/2",
            "values": values, "omitted_ideal_sum": interval(omitted),
            "tail_polynomial": polynomial, "tail_integral_before_exponential": integral}


def main():
    output = DATA / "nelson_completed_ideal_majorant_d96.json"
    assert not output.exists()
    started = time.monotonic()
    paths = [DATA/"nelson_completed_scalar_blocks_d96.json", DATA/"nelson_all_ideal_bounds_d93_exact_d93.json",
             DATA/"nelson_contour_weight_bounds_d94.json", DATA/"nelson_prime31_sum_d93_exact_d93.json"]
    packet, old, d94, prime = [json.loads(p.read_text()) for p in paths]
    Z0 = (4*PI*PI)**8/2**62
    signs = sign_certificates(packet, Z0)
    T = QQ(signs["A_range"][1])
    print("SCALAR_SIGNS", signs["certified_block_count"], "blocks, A<=", T, flush=True)
    completed = completed_ideal_sum(Z0)
    print("COMPLETED_IDEAL_SUM", completed["omitted_ideal_sum"]["display"], flush=True)
    c, u, kappa = QQ(4), QQ(25)/16, QQ(32)/7
    constants = next(row for row in old["constants"] if row["contour"] == c)["constants"]["1"]
    bh, bk = [ball(constants[key]["bound"]) for key in ("2", "3")]
    mass = divisor_mass(u+QQ(1)/2)
    moment = 1/(1-RB(QQ(2)/9)**u)
    scale = Z0**(-c)*RB(T)**(u-c)*mass
    omitted_A_tail = scale*(bh+bk)*moment
    norm_sum_splice = kappa*scale*bk*(1+2/c)
    new_bound = kappa*ball(completed["omitted_ideal_sum"])+omitted_A_tail+norm_sum_splice
    assert new_bound.lower()>0
    prior = min((row for row in d94["rows"] if row["weight_power"] == 0),
                key=lambda row: QQ(row["all_uncomputed_norm_ideal_bounds"]["1"]["upper"]))
    old_bound = ball(prior["all_uncomputed_norm_ideal_bounds"]["1"])
    selected = prime["weighted_first_quartic_orbit"][prime["selected_root_index"]]["unit_plus_prime_families"]["1"]
    two_family_error = ball(selected["absolute_error_bound"])
    total_error = new_bound+two_family_error
    enclosure = ball(selected["partial_sum"]["real"]).add_error(total_error.upper())
    assert enclosure.contains_zero()
    result = {"status": "pass: completed scalar/ideal majorant; CM anchor still uncertified",
              "sign_certificates": signs, "completed_norm_sum": completed,
              "packing_count_coefficient": str(kappa), "packing_count_bound": "C_N(A)<=32*A/(7*N)",
              "finite_radial_majorant": "|K3-(1-N/A)*K4|/A <= K4/A, for N<=A<=T",
              "ideal_completed_kernel": "F(N)=K4(Z0*N)+integral_N^infinity K4(Z0*A)*dA/A",
              "norm_Euler_factor_cancellation": "zeta_F(2*s)*D_odd(s+1/2)=zeta_F(s+1/2)^2*zeta_F(s-1/2)^2/F2(2^(-s-1/2))",
              "splice": {"T": str(T), "c": str(c), "u": str(u), "divisor_mass": interval(mass),
                         "orbit_moment": interval(moment), "common_scale": interval(scale),
                         "all_A_above_T_error": interval(omitted_A_tail), "norm_sum_splice_error": interval(norm_sum_splice)},
              "uncomputed_ideal_S11_bound": interval(new_bound), "D94_bound": interval(old_bound),
              "improvement_factor": interval(old_bound/new_bound),
              "selected_partial_sum": selected["partial_sum"]["real"],
              "two_family_tail": selected["absolute_error_bound"], "full_S11_error_bound": interval(total_error),
              "full_S11_enclosure": interval(enclosure),
              "new_quaternion_enumeration": False, "new_Hecke_data": False,
              "global_kernel_identified_up_to_positive_scalar": True,
              "CM_anchor_derivative_nonzero": False, "arithmetic_CM_jet_computed": False,
              "sources": [kernel.source(p) for p in [Path(__file__), Path(blocks.__file__), Path(kernel.__file__)]+paths]}
    output.write_text(json.dumps(result, indent=2)+"\n")
    print("COMPLETED_IDEAL_BOUND", new_bound, "IMPROVEMENT", old_bound/new_bound, flush=True)
    print("PASS|361_nelson_completed_ideal_majorant", round(time.monotonic()-started, 2), flush=True)


if __name__ == "__main__":
    main()

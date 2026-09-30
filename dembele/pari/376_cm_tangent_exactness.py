"""D101 bounded candidate tangent and independent exactness-interface checks.

--run creates a new bounded Magma job; --collect uses its saved receipt;
--check replays saved data without Magma. No output is an independently
computed arithmetic Shimura tangent.
"""
import argparse
import ast
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
MODEL = DATA / "cm_frame_curve_candidate.json"
BASIS = DATA / "cm_field_recognition.json"
OLD_JETS = DATA / "d88_candidate_cm_jet_rank.json"
DRIVER = ROOT / "dembele/magma/375_cm_tangent_candidate_height.m"
INPUT = DATA / "cm_tangent_candidate_height_d101_input.m"
OUTPUT = DATA / "cm_tangent_exactness_d101.json"
MARKER = "PASS|D101_EXACT_CANDIDATE_TANGENT"
N = 17


def source(path):
    p = Path(path).resolve()
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def load(path):
    return json.loads(Path(path).read_text())


def magma_literal(value):
    if isinstance(value, list):
        return "[" + ",".join(magma_literal(x) for x in value) + "]"
    return str(Q(value))


def field_mul(a, b, h, modulus=None):
    c = [0] * (2*N-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    for i in range(2*N-2,N-1,-1):
        v = c[i] if modulus is None else c[i] % modulus
        for j in range(N):
            c[i-N+j] -= v*h[j]
    return c[:N] if modulus is None else [x % modulus for x in c[:N]]


def field_power(a, exponent, h, modulus):
    out = [1] + [0]*(N-1)
    while exponent:
        if exponent & 1:
            out = field_mul(out,a,h,modulus)
        a = field_mul(a,a,h,modulus)
        exponent >>= 1
    return out


def finite_field_rank(rows, h, prime=31):
    a = [[list(z) for z in row] for row in rows]
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r,len(a)) if any(a[i][col])),None)
        if pivot is None:
            continue
        a[r],a[pivot] = a[pivot],a[r]
        inv = field_power(a[r][col], prime**N-2,h,prime)
        a[r] = [field_mul(z,inv,h,prime) for z in a[r]]
        for i in range(r+1,len(a)):
            c = a[i][col]
            if any(c):
                a[i] = [[(x-y) % prime for x,y in zip(z,field_mul(c,w,h,prime))]
                        for z,w in zip(a[i],a[r])]
        r += 1
        if r == len(a):
            break
    return r


def trim(p):
    p = list(p)
    while len(p)>1 and p[-1]==0:
        p.pop()
    return p


def padd(a,b):
    return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
                 for i in range(max(len(a),len(b)))])


def pmul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]+=x*y
    return trim(out)


def pdiff(a):
    return trim([i*a[i] for i in range(1,len(a))] or [0])


def compose(a,b):
    out=[0]
    for x in reversed(a):
        out=padd(pmul(out,b),[x])
    return out


def bracket(a,b):
    return padd(pmul(a,pdiff(b)),[-x for x in pmul(b,pdiff(a))])


def formal_controls():
    a,b,g,h=[2,3,5],[7,11,13],[1,3,1],[0,2,1]
    # Multiplying both local coefficients by g multiplies their bracket by g^2.
    assert bracket(pmul(g,a),pmul(g,b)) == pmul(pmul(g,g),bracket(a,b))
    # Differential coefficients transform with h'; the bracket transforms with h'^3.
    ap=pmul(compose(a,h),pdiff(h)); bp=pmul(compose(b,h),pdiff(h))
    hp3=pmul(pmul(pdiff(h),pdiff(h)),pdiff(h))
    assert bracket(ap,bp) == pmul(compose(bracket(a,b),h),hp3)
    # u=z^2: the tricanonical coefficient has a factor 8*z^3.
    h=[0,0,1]
    ap=pmul(compose(a,h),pdiff(h)); bp=pmul(compose(b,h),pdiff(h))
    assert bracket(ap,bp) == pmul([0,0,0,8],compose(bracket(a,b),h))
    assert bracket(ap,bp)[3] == 8*(a[0]*b[1]-b[0]*a[1])
    # Strictness and integrality are essential in the norm separation test.
    m=19
    assert m**17*Q(1,m)**17 == 1
    assert m**136*Q(1,2*m)**136 < 1
    assert (m*Q(1,2*m)).denominator != 1
    return {"common_factor_covariance":True,"coordinate_change_weight_three":True,
            "order_two_pullback_factor":"8*z^3","norm_threshold_strict":True,
            "missing_integrality_control_rejected":True}


def audit(job):
    for item in job["sources"]+[job["driver"],job["input"],job["log"]]:
        assert source(item["path"]) == item, item["path"]
    assert job["status"] == "pass"
    log=Path(job["log"]["path"]).read_text()
    assert MARKER in log
    def block(label):
        m=re.search(r"^"+label+r"\|(.+?)(?=^[A-Z_]+\||\Z)",log,re.M|re.S)
        assert m,label
        return ast.literal_eval(m.group(1).strip())
    num,den=block("TANGENT_NUMERATORS"),block("TANGENT_DENOMINATORS")
    inu,ide=block("INTEGRAL_NUMERATORS"),block("INTEGRAL_DENOMINATORS")
    assert all(len(x)==16 and all(len(row)==N for row in x) for x in [num,den,inu,ide])
    v=[[Q(x,y) for x,y in zip(a,b)] for a,b in zip(num,den)]
    iv=[[Q(x,y) for x,y in zip(a,b)] for a,b in zip(inu,ide)]
    model,basis,old=load(MODEL),load(BASIS)["field_basis"],load(OLD_JETS)
    h=[int(z) for z in model["CM_field_polynomial_ascending"]]
    raw=[[Q(z) for z in row] for row in model["CM_projective_coordinates_power_basis"]]
    ib=[[Q(z) for z in row] for row in basis["integral_basis_power_coordinates"]]
    for i in range(16):
        assert [sum(iv[i][j]*ib[j][k] for j in range(N)) for k in range(N)] == v[i]
    dp=math.lcm(*(x.denominator for row in v for x in row))
    di=math.lcm(*(x.denominator for row in iv for x in row))
    assert f"CLEARING_INTEGERS|{dp}|{di}" in log
    assert block("BASIS_DISCRIMINANT") == int(basis["integral_basis_discriminant"])
    assert dp%31 and di%31
    assert v[0]==[Q(0)]*N and v[1]==[Q(1)]+[Q(0)]*(N-1)
    dpoint=math.lcm(*(x.denominator for row in raw for x in row))
    pp=[[int(dpoint*x) for x in row] for row in raw]
    vv=[[int(dp*x) for x in row] for row in v]
    pairs=model["monomial_pairs"]
    linear=[]
    constant=[]
    for i,j in pairs:
        a=field_mul(pp[i],vv[j],h); b=field_mul(pp[j],vv[i],h)
        linear.append([x+y for x,y in zip(a,b)])
        constant.append(field_mul(pp[i],pp[j],h))
    for q in model["quadrics"]:
        for values in [constant,linear]:
            assert all(sum(c*z[k] for c,z in zip(q,values))==0 for k in range(N))
    def reduce(row):
        return [(x.numerator*pow(x.denominator,-1,31))%31 for x in row]
    vmod=[reduce(row) for row in v]
    assert vmod == old["candidate_projective_jets_mod31"][1]
    pmod=[reduce(row) for row in raw]
    zero=[0]*N; one=[1]+[0]*(N-1)
    jac=[]
    for q in model["quadrics"]:
        row=[[0]*N for _ in range(16)]
        for c,(i,j) in zip(q,pairs):
            row[i]=[(x+c*y)%31 for x,y in zip(row[i],pmod[j])]
            row[j]=[(x+c*y)%31 for x,y in zip(row[j],pmod[i])]
        jac.append(row)
    assert finite_field_rank(jac,h)==14
    extended=jac+[[one if j==i else zero for j in range(16)] for i in [0,1]]
    assert finite_field_rank(extended,h)==16
    assert any(any(row[2]) for row in jac)  # adding 1 to v_3 fails at least one equation
    # This root bound gives certified conjugate bounds for the candidate only.
    radius=4
    assert sum(abs(h[i])*radius**i for i in range(N)) < radius**N
    bounds=[sum(abs(c)*radius**j for j,c in enumerate(row)) for row in v]
    paths=[Path(__file__),DRIVER,INPUT,MODEL,BASIS,OLD_JETS,
           ROOT/"dembele/data/computed/cm_frame_curve_candidate.m",
           ROOT/"dembele/certificates/d88-cm-expansion-identification-review.md",
           ROOT/"dembele/certificates/cm-tangent-local-arithmetic-d89.md",
           ROOT/"dembele/certificates/nelson-spectral-ideal-d98.md",
           DATA/"cm_tangent_exactness_d101_parser_failed.py",
           DATA/"cm_tangent_exactness_d101_parser_failure.json"]
    return {"status":"pass","milestone":"D101","scope":"candidate reference and conditional exactness interface only",
            "arithmetic_Shimura_tangent_computed":False,"candidate_identification_proved":False,
            "unknown_arithmetic_denominator_bound_proved":False,
            "candidate_field_degree":N,"possible_F_residue_field_absolute_degree":136,
            "candidate_tangent_power_basis":[[str(c) for c in row] for row in v],
            "candidate_tangent_integral_basis":[[str(c) for c in row] for row in iv],
            "power_basis_clearing_integer":str(dp),"integral_lattice_clearing_integer":str(di),
            "power_basis_integer_decimal_digits":len(str(dp)),"integral_lattice_integer_decimal_digits":len(str(di)),
            "candidate_conjugate_absolute_upper_bounds":[str(x) for x in bounds],
            "exact_quadric_linearizations_checked":91,"jacobian_rank_mod31":14,
            "normalized_tangent_uniqueness_rank_mod31":16,"matches_D88_mod31":True,
            "candidate_corruption_rejected":True,"formal_controls":formal_controls(),
            "conditional_norm_test":{"hypothesis":"M*(actual-candidate) integral; certified bounds E_sigma at EVERY embedding",
                                     "acceptance":"M^d * product(E_sigma) < 1",
                                     "equal_error_sufficient":"E_sigma < 1/M for every sigma",
                                     "arithmetic_hypotheses_currently_verified":False},
            "sources":[source(p) for p in paths],"job":job}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run",action="store_true")
    group.add_argument("--collect",action="store_true")
    group.add_argument("--check",action="store_true")
    args=parser.parse_args()
    if args.run:
        assert not OUTPUT.exists(), "Preserve the existing completed artifact."
        model,basis=load(MODEL),load(BASIS)["field_basis"]
        data="\n".join([
            "// D101 generated candidate input; not independently computed Shimura data.",
            "Hcoeffs := "+magma_literal(model["CM_field_polynomial_ascending"])+";",
            "point_coeffs := "+magma_literal(model["CM_projective_coordinates_power_basis"])+";",
            "integral_basis_coeffs := "+magma_literal(basis["integral_basis_power_coordinates"])+";",
            "expected_basis_discriminant := "+str(int(basis["integral_basis_discriminant"]))+";",""])
        if INPUT.exists():
            assert INPUT.read_text()==data
        else:
            INPUT.write_text(data)
        spec=importlib.util.spec_from_file_location("d101_bounded",ROOT/"dembele/pari/272_cm_frame_bounded_jobs.py")
        runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
        n=1
        while (DATA/f"cm_tangent_candidate_height_d101_attempt{n:02}.job.json").exists():
            n+=1
        prefix=f"cm_tangent_candidate_height_d101_attempt{n:02}"
        log=DATA/(prefix+".log")
        job=runner.run_job([runner.MAGMA,"-bn","-l","2000000000",str(DRIVER)],log,180,MARKER)
        job.update({"driver":source(DRIVER),"input":source(INPUT)})
        (DATA/(prefix+".job.json")).write_text(json.dumps(job,indent=2)+"\n")
        print(json.dumps({"job_status":job["status"],"wall_seconds":job["wall_seconds"],"log":str(log)}),flush=True)
        assert job["status"]=="pass"
        report=audit(job)
        OUTPUT.write_text(json.dumps(report,indent=2)+"\n")
    elif args.collect:
        assert not OUTPUT.exists(), "Preserve the existing completed artifact."
        job=load(DATA/"cm_tangent_candidate_height_d101_attempt01.job.json")
        report=audit(job)
        OUTPUT.write_text(json.dumps(report,indent=2)+"\n")
    else:
        old=load(OUTPUT)
        for item in old["sources"]:
            assert source(item["path"])==item,item["path"]
        report=audit(old["job"])
        assert report==old
    print(json.dumps({"status":"pass","scope":report["scope"],
                      "integral_lattice_clearing_integer":report["integral_lattice_clearing_integer"],
                      "power_basis_integer_decimal_digits":report["power_basis_integer_decimal_digits"],
                      "arithmetic_tangent":False}),flush=True)


if __name__=="__main__":
    main()

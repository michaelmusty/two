"""D91: rigorous Mellin integrals for finitely many primitive classes.

Arb balls enclose every quadrature node. Explicit strip and vertical-tail
bounds enclose the infinite trapezoidal quadrature. The Dedekind zeta
factor includes every auxiliary ideal, and a geometric factor includes
every beta power. Missing primitive quaternion classes remain unbounded.
"""
import hashlib
import json
import time
from math import comb, factorial
from pathlib import Path
from sage.all import (AA, QQ, ZZ, ComplexBallField, NumberField, PolynomialRing,
                      QuaternionAlgebra, RealBallField, prime_range)

ROOT = Path(__file__).resolve().parents[2]; DATA = ROOT/"dembele/data/computed"
PRECISION = 320; STEP_DENOMINATOR = 32; HEIGHT = 16
RB = RealBallField(PRECISION); CB = ComplexBallField(PRECISION); PI = RB.pi()


def source(p):
    return {"path":str(p.relative_to(ROOT)), "sha256":hashlib.sha256(p.read_bytes()).hexdigest()}


def interval(x):
    return {"lower":str(QQ(x.lower())), "upper":str(QQ(x.upper())), "display":str(x)}


def complex_interval(x): return {"real":interval(x.real()), "imag":interval(x.imag())}


ROOT8 = (CB(0,1)*PI/4).exp()
CHARACTERS = [[ROOT8**(k*j) for j in range(8)] for k in range(1,8)]


def dedekind_zeta(s):
    """zeta_F(s) = zeta(s) times the seven nontrivial even L's mod 32.

    The imprimitive modulus introduces no extra Euler factors for these
    seven characters, whose primitive conductors are also powers of two.
    """
    values=[]
    for j in range(8):
        a=pow(5,j,32)
        values.append(s.zeta(QQ(a)/32)+s.zeta(QQ(32-a)/32))
    scale=CB(32)**(-s); answer=s.zeta()
    for row in CHARACTERS:
        answer *= scale*sum((c*v for c,v in zip(row,values)),CB(0))
    return answer


def euler_checks():
    checks=[]; limit=1000
    for imaginary in [0,3,16]:
        s=CB(4,imaginary); exact=dedekind_zeta(s)
        partial=1/(1-CB(2)**(-s))
        for p in prime_range(3,limit+1):
            f=next(k for k in [1,2,4,8] if pow(int(p),k,32) in [1,31])
            partial *= (1-CB(p)**(-f*s))**(-8//f)
        # Bound the logarithm of every omitted Euler factor by allowing
        # eight degree-one prime factors at every integer above the cutoff.
        logarithmic=RB(QQ(8)/(3*limit**3)/(1-QQ(1)/(limit+1)**4))
        error=(RB(4)/3)**8*(logarithmic.exp()-1)
        assert abs(exact-partial).upper() < error.lower()
        checks.append({"argument":[4,imaginary], "zeta":complex_interval(exact),
                       "Euler_product_limit":limit, "Euler_remainder_bound":interval(error)})
    return checks


def polynomial_times(p,a,b):
    q=[0]*(len(p)+1)
    for i,c in enumerate(p):q[i]+=a*c;q[i+1]+=b*c
    return q


def gamma_majorant(c,k):
    """P(t) with |(2s-1) Gamma(s)^8 Gamma(s+1)^7 Gamma(s+k)|
    <= P(|t|) exp(-24 |t|) on Re(s)=c, c=1,2,3.
    Uses pi*t/sinh(pi*t) <= (1+2*pi*t)exp(-pi*t), 3<pi<4.
    """
    p=[1]
    for _ in range(8):p=polynomial_times(p,1,8)
    for end,power in [(c-1,8),(c,7),(c+k-1,1)]:
        for j in range(1,end+1):
            for _ in range(power):p=polynomial_times(p,j,1)
    p=polynomial_times(p,2*c-1,2)
    assert len(p)-1 == 16*c+k
    return p


def gamma_integral_bound(c,k,cutoff=0):
    p=gamma_majorant(c,k)
    answer=QQ(0)
    for j,coefficient in enumerate(p):
        answer += coefficient*sum(QQ(comb(j,r)*cutoff**(j-r)*factorial(r))/24**(r+1) for r in range(j+1))
    return 2*RB(answer)*RB(-24*cutoff).exp()


def boundary_bound(z,c,k,cutoff=0):
    zeta_bound=(QQ(2*c)/(2*c-1))**8
    cusp_beta_bound=QQ(1+2**c)/(1-QQ(1)/2**(c+1))
    return z**(-c)*zeta_bound*cusp_beta_bound*gamma_integral_bound(c,k,cutoff)


def quadrature_error(z,k,denominator):
    # Standard infinite trapezoidal strip bound, with half-width 1.
    # Replacing 2*pi by 6 enlarges both the normalizing factor and error.
    strip=(boundary_bound(z,1,k)+boundary_bound(z,3,k))/(6*(RB(6*denominator).exp()-1))
    # For t>=16, P(t)exp(-24t) decreases since deg(P)<=40<24*16.
    # Thus the omitted grid sum is bounded by the corresponding integral.
    assert 16*2+k < 24*HEIGHT
    tail=boundary_bound(z,2,k,HEIGHT)/6
    return strip+tail, strip, tail


def main():
    started=time.monotonic()
    paths=[DATA/"nelson_primitive_classes_d91.json",DATA/"nelson_cm_lattice_d90.json"]
    primitive,local=[json.loads(p.read_text()) for p in paths]
    R=PolynomialRing(QQ,"s"); s=R.gen()
    F=NumberField(s**8-8*s**6+20*s**4-16*s*s+2,"b"); b=F.gen()
    B=QuaternionAlgebra(F,b-b*b,-1)
    def quat(v):return B([F([QQ(c) for c in v[8*j:8*(j+1)]]) for j in range(4)])
    place=sorted(F.embeddings(AA),key=lambda v:v(b))[4]
    def real(x):return RB(place(x))
    root=real(b);sqrt_a=(root-root*root).sqrt(); beta=quat(local["arithmetic"]["CM_beta_power_coordinates"])
    def embed(q):
        a0,a1,a2,a3=[real(c) for c in q.coefficient_tuple()]
        return a0+a1*sqrt_a,a2+a3*sqrt_a,-a2+a3*sqrt_a,a0-a1*sqrt_a
    ba,bb,bc,bd=embed(beta); x0=(ba-bd)/(2*bc); y0=real(2+b).sqrt()/abs(bc)
    def xy(q):
        a,bb,c,d=embed(q); off=(bb+(a-d)*x0-c*x0*x0)/y0
        return (CB(a+d)+CB(0,1)*(off-c*y0))/2, (CB(a-d-2*c*x0)+CB(0,1)*(off+c*y0))/2
    args={}; records=[]
    for entry in primitive["primitive_classes"]:
        q=quat(entry["quaternion_power_coordinates"]); X,Y=xy(q)
        key=tuple(entry["multiplicative_majorant_field_element"])
        A=real(F([QQ(c) for c in key])); norm=entry["norm_ideal_norm"]
        assert A.lower()>0
        rho=1-RB(norm)/A
        if not entry["mixed"]: Y=CB(0);rho=RB(0)
        else:assert rho.lower()>0 and rho.upper()<1
        absX=abs(X); phases={a:(X/absX)**(a+3)*(Y.conjugate()/absX)**(a-1) for a in [1,3,5]}
        assert (abs(Y)**2/absX**2-rho).contains_zero()
        if key not in args:
            args[key]={"A":A,"Z":(4*PI*PI)**8*A/2**62,
                       "sum":{k:RB(0) for k in range(3,9)},"coarse":{k:RB(0) for k in range(3,9)}}
        records.append({"entry":entry,"key":key,"A":A,"rho":rho,"phases":phases})
    calibration=euler_checks();print("Euler calibration passed; arguments:",len(args),flush=True)
    log2=RB(2).log();logs={key:v["Z"].log() for key,v in args.items()}
    count=HEIGHT*STEP_DENOMINATOR
    for j in range(count+1):
        s=CB(2,QQ(j)/STEP_DENOMINATOR)
        gamma=s.gamma();two_s=(s*log2).exp()
        base=(2*s-1)*gamma**16*s**7*dedekind_zeta(2*s)*(1+two_s)/(1-1/(2*two_s))
        rising=CB(1);factors={}
        for k in range(1,9):
            rising*=s+k-1
            if k>=3:factors[k]=base*rising
        weight=1 if j==0 else 2
        for key,arg in args.items():
            power=(-s*logs[key]).exp()
            for k in range(3,9):
                term=weight*(factors[k]*power).real()
                arg["sum"][k]+=term
                if j%2==0:arg["coarse"][k]+=term
        if j%128==0:print("Quadrature node",j,"/",count,"elapsed",round(time.monotonic()-started,2),flush=True)
    kernels=[];largest_error=RB(0)
    for key,arg in args.items():
        values=[]; arg["kernel"]={}
        for k in range(3,9):
            error,strip,tail=quadrature_error(arg["Z"],k,STEP_DENOMINATOR)
            value=arg["sum"][k]/(2*PI*STEP_DENOMINATOR)
            rigorous=value.add_error(error.upper())
            coarse_error,_,_=quadrature_error(arg["Z"],k,STEP_DENOMINATOR//2)
            coarse=(arg["coarse"][k]/(PI*STEP_DENOMINATOR)).add_error(coarse_error.upper())
            assert rigorous.overlaps(coarse)
            assert QQ(rigorous.rad()) < QQ(1)/10**30
            arg["kernel"][k]=rigorous
            largest_error=max(largest_error,RB(error.upper()))
            values.append({"k":k,"value":interval(rigorous),"strip_error_bound":interval(strip),
                           "vertical_tail_bound":interval(tail),"coarse_grid_overlaps":True})
        kernels.append({"majorant_field_element":list(key),"A":interval(arg["A"]),"Z":interval(arg["Z"]),"values":values})
    buckets={bucket:{a:CB(0) for a in [1,3,5]} for bucket in primitive["bucket_counts"]}
    terms=[]
    for record in records:
        entry=record["entry"];ks=args[record["key"]]["kernel"]
        values={a:record["phases"][a]*(a*ks[a+2]-record["rho"]*ks[a+3])/record["A"] for a in [1,3,5]}
        for a,value in values.items():buckets[entry["Hecke_bucket"]][a]+=value
        terms.append({"primitive_index":entry["index"],"bucket":entry["Hecke_bucket"],
                      "values":{str(a):complex_interval(v) for a,v in values.items()}})
    print("Bucket sums, without common Petersson scalar:",flush=True)
    for bucket,values in buckets.items():
        for a,v in values.items():print(bucket,(a,1),v,flush=True)
    result={"status":"pass: interval-enclosed primitive-subset sums, all auxiliary ideals and beta powers",
            "precision_bits":PRECISION,"contour_real_part":2,"trapezoidal_step":"1/32","height":HEIGHT,
            "strip_half_width":1,"Dedekind_zeta":"zeta(s) times seven nontrivial even Dirichlet L-functions mod 32",
            "kernel":"integral_(2) (2s-1) Gamma(s)^8 Gamma(s+1)^7 Gamma(s+k) zeta_F(2s) Z^-s (1+2^s)/(1-2^(-s-1)) ds/(2*pi*i)",
            "argument":"Z=(4*pi^2)^8*A/2^62","primitive_classes":len(records),
            "Euler_checks":calibration,"kernels":kernels,"class_terms":terms,
            "Hecke_affine_buckets":{bucket:{str(a):complex_interval(v) for a,v in values.items()} for bucket,values in buckets.items()},
            "largest_kernel_quadrature_error_bound":interval(largest_error),
            "all_auxiliary_ideals_summed":True,"all_beta_powers_summed":True,
            "omitted_primitive_classes_bounded":False,"global_Shimizu_test_vector_identification_proved":False,
            "Shimura_derivative_computed":False,
            "sources":[source(p) for p in [Path(__file__)]+paths]}
    output=DATA/"nelson_interval_sum_d91.json";assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS|333_nelson_interval_sum")


if __name__=="__main__": main()

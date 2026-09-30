"""D92: complete cutoff sums and an infinite norm-one-family error bound.

This is the norm-one control for the D91 expression, including its beta
powers and auxiliary ideals. It is not the complete Hecke-weighted lift.
"""
import argparse
import importlib.util
import json
from math import comb, factorial
from pathlib import Path
import time
from sage.all import AA, QQ, NumberField, PolynomialRing, QuaternionAlgebra

spec=importlib.util.spec_from_file_location("kernel",Path(__file__).with_name("333_nelson_interval_sum.py"))
kernel=importlib.util.module_from_spec(spec);spec.loader.exec_module(kernel)
RB,CB,PI=kernel.RB,kernel.CB,kernel.PI
DATA,ROOT=kernel.DATA,kernel.ROOT


def vertical_tail(c,k,shift):
    # Binet: |Gamma(c+it)| <= sqrt(2*pi)*exp(1/(12*c))
    # *(c*c+t*t)^((c-1/2)/2)*exp(-pi*t/2), 1/2<=c<=1.
    # Bound Gamma(s)^16*s^7*(s)_k*(2*s-1)*(s+shift)
    # by 8^8*exp(4/(3*c))*P(t)*exp(-24*t).
    assert QQ(1)/2<c<=1
    p=[1]
    for _ in range(15):p=kernel.polynomial_times(p,1,1)
    for j in range(1,k+1):p=kernel.polynomial_times(p,j,1)
    p=kernel.polynomial_times(p,1,2)
    p=kernel.polynomial_times(p,1+shift,1)
    h=16
    integral=sum(coefficient*sum(QQ(comb(j,r)*h**(j-r)*factorial(r))/24**(r+1)
                               for r in range(j+1)) for j,coefficient in enumerate(p))
    return 8**8*(RB(QQ(4)/(3*c))-24*h).exp()*RB(integral)


def tail_constants():
    answers=[];denominator=128;height=16
    for c in [QQ(3)/4,QQ(7)/8,QQ(1)]:
        totals={(a,shift):RB(0) for a in [1,3,5] for shift in [2,a+2]}
        for j in range(height*denominator):
            t=RB(QQ(2*j+1)/(2*denominator)).add_error(QQ(1)/(2*denominator))
            s=CB(RB(c),t);base=abs((2*s-1)*s.gamma()**16*s**7)
            rising=CB(1)
            for k in range(1,8):
                rising*=s+k-1
                if k in [3,5,7]:
                    a=k-2
                    for shift in [2,a+2]:
                        upper=(base*abs(rising*(s+shift))).upper()
                        totals[a,shift]+=RB(upper)/denominator
        zeta=kernel.dedekind_zeta(CB(2*c));assert zeta.imag().contains_zero() and zeta.real().lower()>1
        two=RB(2)**c;cusp=(1+two)/(1-1/(2*two));values={}
        for a in [1,3,5]:
            values[str(a)]={}
            for shift in [2,a+2]:
                tail=vertical_tail(c,a+2,shift)
                bound=zeta.real()*cusp*(totals[a,shift]+tail)/PI
                assert bound.lower()>0 and QQ(tail.upper())<QQ(1)/10**100
                values[str(a)][str(shift)]={"bound":kernel.interval(bound),"vertical_tail":kernel.interval(tail)}
        answers.append({"contour":str(c),"zeta_F_2c":kernel.interval(zeta.real()),
                        "cusp_beta_bound":kernel.interval(cusp),"constants":values})
        print("TAIL_CONSTANTS",c,{a:values[str(a)]["2"]["bound"]["display"] for a in [1,3,5]},flush=True)
    return {"precision_bits":kernel.PRECISION,"interval_mesh":"1/128","height":height,
            "orbit_count_bound":"N(T) <= (32/7)*T for T>=1",
            "proof_input":"complete A<=400 list; only identity has A=1; all other A>64",
            "contours":answers}


def get_ball(interval):
    lo,hi=QQ(interval["lower"]),QQ(interval["upper"])
    return RB((lo+hi)/2).add_error((hi-lo)/2)


def main():
    started=time.monotonic();p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--bound",type=int,default=25600);args=p.parse_args()
    paths=[DATA/f"nelson_norm_one_d92_T{args.bound}.json",DATA/"nelson_cm_lattice_d90.json",
           DATA/"nelson_norm_one_d92_T400.json",DATA/f"nelson_norm_one_coverage_d92_T{args.bound}.json",
           DATA/"nelson_norm_one_coverage_d92_T400.json"]
    packet,local,small,coverage,small_coverage=[json.loads(path.read_text()) for path in paths]
    out=DATA/f"nelson_norm_one_sum_d92_T{args.bound}.json";assert not out.exists()
    assert coverage["signed_pair_count"]*2==packet["enumeration"]["vectors_including_both_signs"]
    identity=[r for r in small["classes"] if r["A_field_coefficients"]==["1"]+["0"]*7]
    assert len(identity)==1
    assert all(QQ(r["A_interval"][0])>64 for r in small["classes"] if r not in identity)
    R=PolynomialRing(QQ,"s");s=R.gen();F=NumberField(s**8-8*s**6+20*s**4-16*s*s+2,"b");b=F.gen()
    B=QuaternionAlgebra(F,b-b*b,-1)
    def quat(v):return B([F([QQ(c) for c in v[8*j:8*(j+1)]]) for j in range(4)])
    place=sorted(F.embeddings(AA),key=lambda v:v(b))[4]
    def real(x):return RB(place(x))
    root=real(b);sqrt_a=(root-root*root).sqrt();beta=quat(local["arithmetic"]["CM_beta_power_coordinates"])
    def embed(q):
        a0,a1,a2,a3=[real(c) for c in q.coefficient_tuple()]
        return a0+a1*sqrt_a,a2+a3*sqrt_a,-a2+a3*sqrt_a,a0-a1*sqrt_a
    ba,bb,bc,bd=embed(beta);x0=(ba-bd)/(2*bc);y0=real(2+b).sqrt()/abs(bc)
    def xy(q):
        a,bb,c,d=embed(q);off=(bb+(a-d)*x0-c*x0*x0)/y0
        return (CB(a+d)+CB(0,1)*(off-c*y0))/2,(CB(a-d-2*c*x0)+CB(0,1)*(off+c*y0))/2
    arguments={};records=[];Z0=(4*PI*PI)**8/2**62
    for entry in packet["classes"]:
        q=quat(entry["quaternion_power_coordinates"]);assert q.reduced_norm()==F(1)
        X,Y=xy(q);key=tuple(entry["A_field_coefficients"]);Af=F([QQ(c) for c in key]);A=real(Af)
        rho=1-1/A
        if Af==F(1):Y=CB(0);rho=RB(0)
        else:assert rho.lower()>0 and rho.upper()<1
        absX=abs(X);phases={a:(X/absX)**(a+3)*(Y.conjugate()/absX)**(a-1) for a in [1,3,5]}
        assert (abs(X)**2-A).contains_zero() and (abs(Y)**2/absX**2-rho).contains_zero()
        if key not in arguments:
            arguments[key]={"A":A,"Z":Z0*A,"sum":{k:RB(0) for k in range(3,9)}}
        records.append({"entry":entry,"key":key,"A":A,"rho":rho,"phases":phases})
    print("SUM_ARGUMENTS",len(arguments),"classes",len(records),flush=True)
    logs={key:v["Z"].log() for key,v in arguments.items()};log2=RB(2).log()
    for j in range(kernel.HEIGHT*kernel.STEP_DENOMINATOR+1):
        s=CB(2,QQ(j)/kernel.STEP_DENOMINATOR);two=(s*log2).exp()
        base=(2*s-1)*s.gamma()**16*s**7*kernel.dedekind_zeta(2*s)*(1+two)/(1-1/(2*two))
        rising=CB(1);factors={}
        for k in range(1,9):
            rising*=s+k-1
            if k>=3:factors[k]=base*rising
        weight=1 if j==0 else 2
        for key,arg in arguments.items():
            power=(-s*logs[key]).exp()
            for k in range(3,9):arg["sum"][k]+=weight*(factors[k]*power).real()
    kernels=[]
    for key,arg in arguments.items():
        arg["kernel"]={};values=[]
        for k in range(3,9):
            error,strip,tail=kernel.quadrature_error(arg["Z"],k,kernel.STEP_DENOMINATOR)
            value=(arg["sum"][k]/(2*PI*kernel.STEP_DENOMINATOR)).add_error(error.upper())
            assert QQ(value.rad())<QQ(1)/10**30;arg["kernel"][k]=value
            values.append({"k":k,"value":kernel.interval(value),"strip_error_bound":kernel.interval(strip),
                           "vertical_tail_bound":kernel.interval(tail)})
        kernels.append({"A_field_coefficients":list(key),"A":kernel.interval(arg["A"]),"values":values})
    cutoffs=[t for t in [400,1600,6400,25600] if t<=args.bound]
    assert cutoffs[-1]==args.bound
    sums={t:{a:CB(0) for a in [1,3,5]} for t in cutoffs};counts={t:0 for t in cutoffs};terms=[]
    for record in records:
        ks=arguments[record["key"]]["kernel"]
        values={a:record["phases"][a]*(a*ks[a+2]-record["rho"]*ks[a+3])/record["A"] for a in [1,3,5]}
        for t in cutoffs:
            assert not (record["A"].lower()<=t<=record["A"].upper())
            if record["A"].upper()<t:
                counts[t]+=1
                for a,v in values.items():sums[t][a]+=v
        terms.append({"class_index":record["entry"]["index"],"values":{str(a):kernel.complex_interval(v) for a,v in values.items()}})
    constants=tail_constants();results=[]
    for t in cutoffs:
        tails={};full={}
        for a in [1,3,5]:
            options=[]
            for row in constants["contours"]:
                c=QQ(row["contour"]);v=row["constants"][str(a)]
                b1=get_ball(v["2"]["bound"]);b2=get_ball(v[str(a+2)]["bound"])
                error=RB(QQ(32)/7)*(Z0*t)**(-c)*((c+1)/c*b1+(c+2)/(c+1)*b2/t)
                options.append({"contour":str(c),"bound":kernel.interval(error)})
            best=min(options,key=lambda v:QQ(v["bound"]["upper"]))
            tails[str(a)]={"chosen_contour":best["contour"],"absolute_error_bound":best["bound"],"alternatives":options}
            e=QQ(best["bound"]["upper"]);v=sums[t][a]
            full[str(a)]={"real":kernel.interval(v.real().add_error(e)),"imag":kernel.interval(v.imag().add_error(e))}
            if a==1:
                assert v.imag().contains_zero()
                full[str(a)]["imag"]=kernel.interval(RB(0))
        results.append({"cutoff":t,"class_count":counts[t],
                        "partial_sums":{str(a):kernel.complex_interval(v) for a,v in sums[t].items()},
                        "infinite_norm_one_tail":tails,"full_norm_one_family_enclosures":full})
        print("CUTOFF",t,"classes",counts[t],"S11",sums[t][1],"tail",tails["1"]["absolute_error_bound"]["display"],flush=True)
    result={"status":"pass: complete norm-one cutoff sums and bounded infinite norm-one tail",
            "invariant_A_cutoff":args.bound,"kernel_convention":"D91; no common Petersson scalar",
            "precision_bits":kernel.PRECISION,"kernels":kernels,"class_terms":terms,
            "cutoffs":results,"tail_constants":constants,
            "all_auxiliary_ideals_summed":True,"all_beta_powers_summed":True,
            "complete_norm_one_family_bounded":True,"other_norm_ideal_families_bounded":False,
            "global_Shimizu_test_vector_identification_proved":False,"Shimura_derivative_computed":False,
            "sources":[kernel.source(path) for path in [Path(__file__),Path(kernel.__file__)]+paths]}
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS|341_nelson_norm_one_sum",round(time.monotonic()-started,3))


if __name__=="__main__":main()

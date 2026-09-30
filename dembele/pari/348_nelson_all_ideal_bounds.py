"""D93: an explicit all-ideal majorant and a cost gate for the D91 series.

Ramanujan gives |a_f(a)| <= d(a)*sqrt(Na). Local rank-two lattice
counting bounds right norm-one orbits by sigma_1(a), for a coprime to
p2. This proves absolute convergence and bounds all uncomputed ideal
families, but the resulting enclosure need not be numerically useful.
"""
import importlib.util
import json
from math import comb,factorial
from pathlib import Path
from sage.all import QQ,PolynomialRing

spec=importlib.util.spec_from_file_location("norm_one",Path(__file__).with_name("341_nelson_norm_one_sum.py"))
norm_one=importlib.util.module_from_spec(spec);spec.loader.exec_module(norm_one)
kernel=norm_one.kernel;RB,CB,PI=kernel.RB,kernel.CB,kernel.PI;DATA=kernel.DATA


def zeta(s):
    value=kernel.dedekind_zeta(CB(s));assert value.imag().contains_zero() and value.real().lower()>1
    return value.real()


def divisor_mass(s):
    assert s>2
    x=RB(2)**(-s);factor2=(1-2*x*x)/((1-x)**2*(1-2*x)**2)
    value=zeta(s)**2*zeta(s-1)**2/zeta(2*s-1)/factor2
    assert value.lower()>1
    return {"argument":str(s),"mass":kernel.interval(value),"removed_norm_two_Euler_factor":kernel.interval(factor2)}


def orbit_moment(p):return 1/(1-RB(QQ(2)/9)**p)


def vertical_tail(c,k,shift):
    poly=kernel.polynomial_times(kernel.gamma_majorant(c,k),c+shift,1);h=16
    integral=sum(coefficient*sum(QQ(comb(j,r)*h**(j-r)*factorial(r))/24**(r+1)
                               for r in range(j+1)) for j,coefficient in enumerate(poly))
    return RB(integral)*RB(-24*h).exp()


def constants():
    answer=[];denominator=128;height=16
    for c in [2,3,4]:
        totals={(a,shift):RB(0) for a in [1,3,5] for shift in [2,a+2]}
        for j in range(height*denominator):
            t=RB(QQ(2*j+1)/(2*denominator)).add_error(QQ(1)/(2*denominator));s=CB(c,t)
            base=abs((2*s-1)*s.gamma()**16*s**7);rising=CB(1)
            for k in range(1,8):
                rising*=s+k-1
                if k in [3,5,7]:
                    a=k-2
                    for shift in [2,a+2]:totals[a,shift]+=RB((base*abs(rising*(s+shift))).upper())/denominator
        zet=zeta(2*c);cusp=QQ(1+2**c)/(1-QQ(1)/2**(c+1));values={}
        for a in [1,3,5]:
            values[str(a)]={}
            for shift in [2,a+2]:
                tail=vertical_tail(c,a+2,shift);value=zet*cusp*(totals[a,shift]+tail)/PI
                values[str(a)][str(shift)]={"bound":kernel.interval(value),"vertical_tail":kernel.interval(tail)}
        answer.append({"contour":c,"zeta_F_2c":kernel.interval(zet),"cusp_beta_bound":str(cusp),"constants":values})
        print("GLOBAL_CONSTANTS",c,{a:values[str(a)]["2"]["bound"]["display"] for a in [1,3,5]},flush=True)
    return answer


def main():
    path=DATA/"nelson_prime31_sum_d93.json";prime=json.loads(path.read_text())
    out=DATA/"nelson_all_ideal_bounds_d93.json";assert not out.exists()
    # Exact local Euler identity: (X/((1-X)(1-qX)))'.
    R=PolynomialRing(QQ,["q","X"]);q,X=R.gens()
    generating=X/((1-X)*(1-q*X))
    assert generating.derivative(X)==(1-q*X*X)/((1-X)**2*(1-q*X)**2)
    coefficients=[]
    for e in range(9):coefficients.append(str((e+1)*sum(q**j for j in range(e+1))))
    rows=constants();Z0=(4*PI*PI)**8/2**62
    masses={}
    def mass(s):
        key=str(s)
        if key not in masses:masses[key]=divisor_mass(s)
        return norm_one.get_ball(masses[key]["mass"])
    omitted={};complete_cutoff_bounds=[]
    for a in [1,3,5]:
        options=[]
        for row in rows:
            c=row["contour"];bs=row["constants"][str(a)]
            bsum=norm_one.get_ball(bs["2"]["bound"])+norm_one.get_ball(bs[str(a+2)]["bound"])
            omitted_mass=mass(QQ(c)+QQ(1)/2)-1-64*RB(31)**(-c-QQ(1)/2)
            assert omitted_mass.lower()>0
            error=Z0**(-c)*bsum*orbit_moment(c)*omitted_mass
            options.append({"contour":c,"omitted_divisor_mass":kernel.interval(omitted_mass),"bound":kernel.interval(error)})
        best=min(options,key=lambda v:QQ(v["bound"]["upper"]))
        omitted[str(a)]={"chosen_contour":best["contour"],"absolute_error_bound":best["bound"],"alternatives":options}
    for T in [25600,10**6,10**8,10**10,10**12,10**14]:
        values={}
        for a in [1,3,5]:
            options=[]
            for row in rows:
                c=row["contour"];bs=row["constants"][str(a)]
                bsum=norm_one.get_ball(bs["2"]["bound"])+norm_one.get_ball(bs[str(a+2)]["bound"])
                for u in [QQ(7)/4,QQ(2),QQ(5)/2,QQ(3)]:
                    if u>=c:continue
                    error=Z0**(-c)*bsum*RB(T)**(u-c)*orbit_moment(u)*mass(u+QQ(1)/2)
                    options.append({"contour":c,"moment_exponent":str(u),"bound":kernel.interval(error)})
            best=min(options,key=lambda v:QQ(v["bound"]["upper"]))
            values[str(a)]={"chosen_contour":best["contour"],"chosen_moment_exponent":best["moment_exponent"],
                            "absolute_error_bound":best["bound"],"alternatives":options}
        complete_cutoff_bounds.append({"hypothetical_complete_A_cutoff":T,"bounds":values,"cutoff_enumerated":False})
        print("ALL_IDEAL_A_TAIL",T,values["1"]["absolute_error_bound"]["display"],flush=True)
    selected=prime["weighted_first_quartic_orbit"][prime["selected_root_index"]];full={}
    for a in ["1","3","5"]:
        row=selected["unit_plus_prime_families"][a]
        error=norm_one.get_ball(row["absolute_error_bound"])+norm_one.get_ball(omitted[a]["absolute_error_bound"])
        full[a]={"absolute_error_bound":kernel.interval(error),
                 "enclosure":{part:kernel.interval(norm_one.get_ball(row["partial_sum"][part]).add_error(error.upper())) for part in ["real","imag"]}}
        if a=="1":full[a]["enclosure"]["imag"]=kernel.interval(RB(0))
    print("UNCOMPUTED_NORM_IDEALS_S11",omitted["1"]["absolute_error_bound"]["display"],flush=True)
    result={"status":"pass: absolute convergence and explicit all-ideal bounds; not useful CM accuracy",
            "coefficient_theorem":{"source":"https://arxiv.org/pdf/math/0511007","location":"Theorem 1 and section 2.2",
                                   "arithmetic_normalization_bound":"|a_f(a)| <= d(a)*sqrt(N(a)) for a coprime to p2"},
            "right_orbit_bound":"at most sigma_1(a); local Hermite forms give 1+q+...+q^e",
            "local_divisor_Euler_identity":"sum_(e>=0) (e+1)*(1+q+...+q^e)*X^e = (1-qX^2)/((1-X)^2*(1-qX)^2)",
            "first_local_coefficients":coefficients,
            "odd_ideal_mass":"D_odd(s)=zeta_F(s)^2*zeta_F(s-1)^2/zeta_F(2s-1), divided by the norm-two Euler factor",
            "whole_orbit_moment_bound":"sum A_gamma^(-u-1) <= 1/(1-(2/9)^u)",
            "precision_bits":kernel.PRECISION,"interval_mesh":"1/128","height":16,
            "constants":rows,"divisor_masses":masses,"uncomputed_norm_ideal_bounds":omitted,
            "hypothetical_complete_cutoff_bounds":complete_cutoff_bounds,
            "selected_formal_series_enclosures":full,
            "all_ideal_absolute_convergence_proved":True,"all_uncomputed_norm_ideal_families_bounded":True,
            "complete_A_cutoff_evaluated":False,"useful_CM_accuracy_reached":False,
            "global_Shimizu_test_vector_identification_proved":False,"Shimura_derivative_computed":False,
            "sources":[kernel.source(p) for p in [Path(__file__),Path(norm_one.__file__),Path(kernel.__file__),path,
                         DATA/"nelson_norm_one_d92.json",DATA/"nelson_norm_one_d92_T400.json",DATA/"nelson_norm_one_coverage_d92_T400.json"]]}
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS|348_nelson_all_ideal_bounds")


if __name__=="__main__":main()

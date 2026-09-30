"""D92: improve the infinite tail using positive disk averages.

The complete A<=400 enumeration proves that hyperbolic balls of radius
acosh(8) about norm-one orbit points are disjoint. Positive coefficients
in the angular binomial average give a substantially sharper bound than
the crude orbit count. See the D92 report for the elementary proof.
"""
import importlib.util
import json
from pathlib import Path
from sage.all import QQ

spec=importlib.util.spec_from_file_location("norm_one",Path(__file__).with_name("341_nelson_norm_one_sum.py"))
norm_one=importlib.util.module_from_spec(spec);spec.loader.exec_module(norm_one)
RB,PI=norm_one.RB,norm_one.PI;kernel=norm_one.kernel;DATA=kernel.DATA


def moment_bound(T,p):
    assert T>=400 and QQ(1)/2<p<=2
    # cosh(R)=2*T-1, cosh(r)=8. The disks beyond R lie beyond R-r.
    outside_A=(8*(2*RB(T)-1)-2*RB(63).sqrt()*RB(T*(T-1)).sqrt()+1)/2
    assert outside_A.lower()>1
    u=QQ(7)/9;w2=1-QQ(1)/T
    # H/(4*pi) >= L * sum_{n=0}^128 ((p+1)_n/n!)^2
    #                    * w2^n * u^(n+1)/(n+1).
    series=QQ(0);coefficient=QQ(1)
    for n in range(129):
        if n:coefficient*=((p+n)/n)**2
        series+=coefficient*w2**n*u**(n+1)/(n+1)
    lower_weight=RB(1) if p<=1 else RB(1-u)**(p-1)
    answer=outside_A**(-p)/(p*lower_weight*RB(series))
    return {"exponent_p":str(p),"outside_A":kernel.interval(outside_A),
            "angular_series_terms":129,"angular_series_lower_sum":str(series),
            "radial_weight_lower_bound":kernel.interval(lower_weight),
            "sum_A_to_minus_p_minus_one_upper_bound":kernel.interval(answer)}


def main():
    path=DATA/"nelson_norm_one_sum_d92_T25600.json";packet=json.loads(path.read_text())
    small_path=DATA/"nelson_norm_one_d92_T400.json";small=json.loads(small_path.read_text())
    coverage_path=DATA/"nelson_norm_one_coverage_d92_T400.json"
    assert json.loads(coverage_path.read_text())["signed_pair_count"]==21
    identity=[v for v in small["classes"] if v["A_field_coefficients"]==["1"]+["0"]*7]
    assert len(identity)==1
    assert all(QQ(v["A_interval"][0])>64 for v in small["classes"] if v not in identity)
    constants=packet["tail_constants"]["contours"];Z0=(4*PI*PI)**8/2**62
    cutoffs=[]
    for row in packet["cutoffs"]:
        T=row["cutoff"];moments={};tails={};full={}
        for c in [QQ(v["contour"]) for v in constants]:
            for p in [c,c+1]:
                if str(p) not in moments:moments[str(p)]=moment_bound(T,p)
        for a in [1,3,5]:
            options=[]
            for v in constants:
                c=QQ(v["contour"]);bs=v["constants"][str(a)]
                b1=norm_one.get_ball(bs["2"]["bound"]);b2=norm_one.get_ball(bs[str(a+2)]["bound"])
                m1=norm_one.get_ball(moments[str(c)]["sum_A_to_minus_p_minus_one_upper_bound"])
                m2=norm_one.get_ball(moments[str(c+1)]["sum_A_to_minus_p_minus_one_upper_bound"])
                error=Z0**(-c)*(b1*m1+b2*m2)
                options.append({"contour":str(c),"bound":kernel.interval(error)})
            best=min(options,key=lambda v:QQ(v["bound"]["upper"]))
            assert QQ(best["bound"]["upper"])<QQ(row["infinite_norm_one_tail"][str(a)]["absolute_error_bound"]["lower"])
            tails[str(a)]={"chosen_contour":best["contour"],"absolute_error_bound":best["bound"],"alternatives":options}
            error=QQ(best["bound"]["upper"]);partial=row["partial_sums"][str(a)]
            full[str(a)]={part:kernel.interval(norm_one.get_ball(partial[part]).add_error(error)) for part in ["real","imag"]}
            if a==1:
                assert norm_one.get_ball(partial["imag"]).contains_zero()
                full[str(a)]["imag"]=kernel.interval(RB(0))
        cutoffs.append({"cutoff":T,"class_count":row["class_count"],"partial_sums":row["partial_sums"],
                        "moment_bounds":moments,"infinite_norm_one_tail":tails,
                        "full_norm_one_family_enclosures":full})
        print("PACKING_TAIL",T,{a:tails[str(a)]["absolute_error_bound"]["display"] for a in [1,3,5]},flush=True)
        print("FULL_NORM_ONE_S11",full["1"]["real"]["display"],flush=True)
    result={"status":"pass: full norm-one-family bounds from disjoint disk averages",
            "disk_radius":"acosh(8)","disk_coordinate_radius_squared":"7/9",
            "coverage_proves_minimum_nontrivial_A_greater_than":64,
            "cutoffs":cutoffs,"complete_norm_one_family_bounded":True,
            "other_norm_ideal_families_bounded":False,"Shimura_derivative_computed":False,
            "sources":[kernel.source(p) for p in [Path(__file__),Path(norm_one.__file__),Path(kernel.__file__),path,small_path,coverage_path]]}
    out=DATA/"nelson_norm_one_packing_tail_d92.json";assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS|342_nelson_norm_one_packing_tail")


if __name__=="__main__":main()

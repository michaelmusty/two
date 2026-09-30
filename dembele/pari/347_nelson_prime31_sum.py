"""D93: bounded prime-31 family, weighted by the saved first quartic orbit.

The 32 certified right norm-one orbits transfer D92's disk separation.
This completes this one prime family, not the full Hecke-weighted sum.
"""
import importlib.util
import json
from pathlib import Path
import re
from sage.all import AA,QQ,NumberField,PolynomialRing,QuaternionAlgebra

spec=importlib.util.spec_from_file_location("norm_one_sum",Path(__file__).with_name("341_nelson_norm_one_sum.py"))
norm_one=importlib.util.module_from_spec(spec);spec.loader.exec_module(norm_one)
kernel=norm_one.kernel;RB,CB,PI=kernel.RB,kernel.CB,kernel.PI;DATA,ROOT=kernel.DATA,kernel.ROOT


def moment_bound(T,p):
    # Same positive disk-average argument as D92, with a rational cutoff
    # T/N. The actual necessary restriction is R(T)>r, or T>9/2.
    T=QQ(T);p=QQ(p);assert T>QQ(9)/2 and QQ(1)/2<p<=2
    outside_A=(8*(2*RB(T)-1)-2*RB(63*T*(T-1)).sqrt()+1)/2
    assert outside_A.lower()>1
    u=QQ(7)/9;w2=1-1/T;series=QQ(0);coefficient=QQ(1)
    for j in range(129):
        if j:coefficient*=((p+j)/j)**2
        series+=coefficient*w2**j*u**(j+1)/(j+1)
    weight=RB(1) if p<=1 else RB(1-u)**(p-1)
    bound=outside_A**(-p)/(p*weight*RB(series))
    return {"displacement_cutoff":str(T),"exponent_p":str(p),"outside_A":kernel.interval(outside_A),
            "angular_series_terms":129,"angular_series_lower_sum":str(series),
            "radial_weight_lower_bound":kernel.interval(weight),"orbit_moment_bound":kernel.interval(bound)}


def main():
    names=["nelson_prime31_b27_d93_T25600.json","nelson_prime31_coverage_d93_T25600.json",
           "nelson_prime31_cosets_d93_T25600.json","nelson_cm_lattice_d90.json",
           "nelson_norm_one_sum_d92_T25600.json","nelson_norm_one_packing_tail_d92.json",
           "f16_steinberg.out"]
    paths=[DATA/n for n in names];packet,coverage,cosets,local,old,old_tail=[json.loads(p.read_text()) for p in paths[:-1]]
    out=DATA/"nelson_prime31_sum_d93.json";assert not out.exists()
    assert coverage["signed_pair_count"]*2==packet["enumeration"]["vectors_including_both_signs"]
    assert cosets["all_32_orbits_exhibited"] and cosets["realized_orbits"]==32 and len(cosets["class_witnesses"])==len(packet["classes"])
    R=PolynomialRing(QQ,"s");s=R.gen();F=NumberField(s**8-8*s**6+20*s**4-16*s*s+2,"b");b=F.gen();B=QuaternionAlgebra(F,b-b*b,-1)
    def quat(v):return B([F([QQ(c) for c in v[8*j:8*(j+1)]]) for j in range(4)])
    place=sorted(F.embeddings(AA),key=lambda p:p(b))[4]
    def real(x):return RB(place(x))
    n=F([QQ(c) for c in packet["norm_generator"]["totally_positive_generator_coefficients"]]);n0=real(n)
    root=real(b);sqrt_a=(root-root*root).sqrt();beta=quat(local["arithmetic"]["CM_beta_power_coordinates"])
    def embed(q):
        a0,a1,a2,a3=[real(c) for c in q.coefficient_tuple()]
        return a0+a1*sqrt_a,a2+a3*sqrt_a,-a2+a3*sqrt_a,a0-a1*sqrt_a
    ba,bb,bc,bd=embed(beta);x0=(ba-bd)/(2*bc);y0=real(2+b).sqrt()/abs(bc)
    def xy(q):
        a,bb,c,d=embed(q);off=(bb+(a-d)*x0-c*x0*x0)/y0
        return (CB(a+d)+CB(0,1)*(off-c*y0))/2,(CB(a-d-2*c*x0)+CB(0,1)*(off+c*y0))/2
    text=paths[-1].read_text();poly=R([-899,433,-36,-8,1])
    assert "z^4 - 8*z^3 - 36*z^2 + 433*z - 899" in text and poly.is_irreducible()
    assert re.search(r"R60\|orbit 1 \(dim 4\): U_p2 charpoly \[\s*<z - 1, 4>\s*\]",text)
    roots=sorted(poly.roots(AA,multiplicities=False));assert len(roots)==4
    eigenvalues=[RB(r) for r in roots];assert all(abs(v).upper()<2*RB(31).sqrt().lower() for v in eigenvalues)
    print("HECKE_EIGENVALUES",list(map(str,eigenvalues)),flush=True)
    arguments={};records=[];Z0=(4*PI*PI)**8/2**62
    for entry in packet["classes"]:
        q=quat(entry["quaternion_power_coordinates"]);assert q.reduced_norm()==n
        X,Y=xy(q);key=tuple(entry["A_field_coefficients"]);Af=F([QQ(c) for c in key]);A=real(Af);rho=1-31/A
        if Af==F(31):Y=CB(0);rho=RB(0)
        else:assert rho.lower()>0 and rho.upper()<1
        absX=abs(X);phases={a:(X/absX)**(a+3)*(Y.conjugate()/absX)**(a-1) for a in [1,3,5]}
        assert (31*abs(X)**2/n0-A).contains_zero() and (abs(Y)**2/absX**2-rho).contains_zero()
        if key not in arguments:arguments[key]={"A":A,"Z":Z0*A,"sum":{k:RB(0) for k in range(3,9)}}
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
            values.append({"k":k,"value":kernel.interval(value),"strip_error_bound":kernel.interval(strip),"vertical_tail_bound":kernel.interval(tail)})
        kernels.append({"A_field_coefficients":list(key),"A":kernel.interval(arg["A"]),"values":values})
    cutoffs=[400,1600,6400,25600];sums={T:{a:CB(0) for a in [1,3,5]} for T in cutoffs};counts={T:0 for T in cutoffs};terms=[]
    for row in records:
        ks=arguments[row["key"]]["kernel"]
        values={a:row["phases"][a]*(a*ks[a+2]-row["rho"]*ks[a+3])/row["A"] for a in [1,3,5]}
        for T in cutoffs:
            assert not (row["A"].lower()<=T<=row["A"].upper())
            if row["A"].upper()<T:
                counts[T]+=1
                for a,v in values.items():sums[T][a]+=v
        terms.append({"class_index":row["entry"]["index"],"values":{str(a):kernel.complex_interval(v) for a,v in values.items()}})
    constants=old["tail_constants"]["contours"];results=[]
    for T in cutoffs:
        moments={};tails={};full={}
        for v in constants:
            c=QQ(v["contour"])
            for p in [c,c+1]:
                if str(p) not in moments:moments[str(p)]=moment_bound(QQ(T)/31,p)
        for a in [1,3,5]:
            options=[]
            for v in constants:
                c=QQ(v["contour"]);bs=v["constants"][str(a)]
                b1=norm_one.get_ball(bs["2"]["bound"]);b2=norm_one.get_ball(bs[str(a+2)]["bound"])
                m1=norm_one.get_ball(moments[str(c)]["orbit_moment_bound"]);m2=norm_one.get_ball(moments[str(c+1)]["orbit_moment_bound"])
                error=32*RB(31)**(-c-1)*Z0**(-c)*(b1*m1+b2*m2)
                options.append({"contour":str(c),"bound":kernel.interval(error)})
            best=min(options,key=lambda v:QQ(v["bound"]["upper"]))
            tails[str(a)]={"chosen_contour":best["contour"],"absolute_error_bound":best["bound"],"alternatives":options}
            e=QQ(best["bound"]["upper"]);v=sums[T][a]
            full[str(a)]={"real":kernel.interval(v.real().add_error(e)),"imag":kernel.interval(v.imag().add_error(e))}
            if a==1:
                assert v.imag().contains_zero();full[str(a)]["imag"]=kernel.interval(RB(0))
        results.append({"cutoff":T,"class_count":counts[T],"partial_sums":{str(a):kernel.complex_interval(v) for a,v in sums[T].items()},
                        "moment_bounds":moments,"infinite_prime_family_tail":tails,"full_unweighted_prime_family_enclosures":full})
        print("PRIME_CUTOFF",T,"classes",counts[T],"S11",sums[T][1],"tail",tails["1"]["absolute_error_bound"]["display"],flush=True)
    final=results[-1];unit=old_tail["cutoffs"][-1];weighted=[]
    for i,eigenvalue in enumerate(eigenvalues):
        values={};combined={}
        for a in [1,3,5]:
            partial=eigenvalue*sums[25600][a]
            error=abs(eigenvalue)*norm_one.get_ball(final["infinite_prime_family_tail"][str(a)]["absolute_error_bound"])
            values[str(a)]={"partial_sum":kernel.complex_interval(partial),"absolute_error_bound":kernel.interval(error),
                            "full_family":{"real":kernel.interval(partial.real().add_error(error.upper())),
                                           "imag":kernel.interval(partial.imag().add_error(error.upper()))}}
            u=unit["partial_sums"][str(a)];up=CB(norm_one.get_ball(u["real"]),norm_one.get_ball(u["imag"]))
            ue=norm_one.get_ball(unit["infinite_norm_one_tail"][str(a)]["absolute_error_bound"]);v=up+partial;e=error+ue
            combined[str(a)]={"partial_sum":kernel.complex_interval(v),"absolute_error_bound":kernel.interval(e),
                              "two_families":{"real":kernel.interval(v.real().add_error(e.upper())),"imag":kernel.interval(v.imag().add_error(e.upper()))}}
            if a==1:
                values[str(a)]["full_family"]["imag"]=kernel.interval(RB(0));combined[str(a)]["two_families"]["imag"]=kernel.interval(RB(0))
        weighted.append({"root_index_in_increasing_order":i,"Hecke_eigenvalue":kernel.interval(eigenvalue),
                         "weighted_prime_family":values,"unit_plus_prime_families":combined})
    result={"status":"pass: certified weighted prime-31 family with all 32 norm-one orbits",
            "prime_norm":31,"prime_b_residue":27,"precision_bits":kernel.PRECISION,
            "Hecke_polynomial_coefficients":[-899,433,-36,-8,1],"U_p2":1,"selected_root_index":0,
            "kernels":kernels,"class_terms":terms,"cutoffs":results,"weighted_first_quartic_orbit":weighted,
            "complete_prime_family_bounded":True,"all_auxiliary_ideals_summed":True,"all_beta_powers_summed":True,
            "other_norm_ideal_families_bounded":False,"global_Shimizu_test_vector_identification_proved":False,"Shimura_derivative_computed":False,
            "sources":[kernel.source(p) for p in [Path(__file__),Path(norm_one.__file__),Path(kernel.__file__)]+paths]}
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS|347_nelson_prime31_sum")


if __name__=="__main__":main()

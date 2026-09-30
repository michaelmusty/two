"""D112 rational replay of CM embeddings, principal classes and local root labels.

No Sage/Magma runtime dependency. The accompanying report states the geometric
CM reciprocity and uniformization inputs, the chosen local CM character, and
the unique-anchor argument; numerical equality alone does not supply them.
"""
import argparse
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/"dembele/data/computed"
OUT=DATA/"dyadic_cm_matching_review_d112.json"
REPORT=ROOT/"dembele/certificates/dyadic-cm-matching-d112.md"
spec=importlib.util.spec_from_file_location("d111",ROOT/"dembele/pari/405_dyadic_edge_reducer.py")
rt=importlib.util.module_from_spec(spec);spec.loader.exec_module(rt)
r,a=rt.r,rt.a;mat=r.mat;Z,O=r.ZERO,r.ONE
source,checked=r.source,r.checked
MP=[2,0,64,0,336,0,672,0,660,0,352,0,104,0,16,0,1]
LP=[68,-2,-128,16,80,40,32,-80,-32,64,0,-16,16,8,0,0,-2,1]
MZ=(Q(0),)*16;MO=(Q(1),)+(Q(0),)*15;BETA=(Q(0),Q(1))+(Q(0),)*14

def mf(row):return tuple(map(Q,row))+(Q(0),)*(16-len(row))
def ma(x,y):return tuple(u+v for u,v in zip(x,y))
def ms(x,c):return tuple(v*c for v in x)
def mm(x,y):
    out=[Q(0)]*31
    for i,u in enumerate(x):
        if u:
            for j,v in enumerate(y):
                if v:out[i+j]+=u*v
    for k in range(30,15,-1):
        if out[k]:
            for i,c in enumerate(MP[:-1]):
                if c:out[k-16+i]-=out[k]*c
    return tuple(out[:16])
def meval(cs,x):
    v=MZ
    for c in reversed(cs):v=ma(mm(v,x),ms(MO,Q(c)))
    return v
def mval(x):return min((16*r.v2(c)+i for i,c in enumerate(x) if c),default=10**9)
def mtruncate(x,precision):
    out=[]
    for i,c in enumerate(x):
        denpow=max(0,-r.v2(Q(c.denominator))) if c else 0
        # The denominator is a positive integer: its 2-valuation is nonnegative.
        denpow=r.v2(Q(c.denominator))
        odd=c.denominator>>denpow;bits=max(0,(precision-i+15)//16+denpow)
        out.append(Q((c.numerator*pow(odd,-1,1<<bits))%(1<<bits),1<<denpow) if bits else Q(0))
    out=tuple(out);assert mval(ma(x,ms(out,-1)))>=precision
    return out
def truncated_eval(cs,x,precision):
    v=MZ
    for c in reversed(cs):v=mtruncate(ma(mm(v,x),ms(MO,Q(c))),precision)
    return v
def mserialize(x):return list(map(str,x))
def mcoordinates(basis):return mat.transpose([list(x) for x in basis])
def matrix_integral(m):return a.integral(sum(m,[]))
def same_lattice(left,right):
    t=mat.multiply(mat.inverse(mcoordinates(left)),mcoordinates(right))
    assert matrix_integral(t) and abs(mat.determinant(t))==1
def mideal(basis,ibinv):
    lattice=mcoordinates(basis);li=mat.inverse(lattice)
    assert all(a.integral(r.ar.mv(li,mm(BETA,z))) for z in basis)
    return abs(mat.determinant(mat.multiply(ibinv,lattice)))

def arithmetic_checks(cm,witness,raw,split):
    lam=r.add(r.scale(O,2),r.PI);OB=[r.fm(v) for v in raw["order_Z_basis"]]
    OZi=mat.inverse(a.matrix_of_basis(OB));W=r.fm(cm["entries"][0]["embedded_beta"])
    oldgroup=json.loads((DATA/"dyadic_group_transport_d110.json").read_text())
    assert W==r.fm(oldgroup["transports"]["W"]["quaternion"])
    k=(Z,Z,Z,O);assert r.qnorm(k)==O and r.qmul(k,W)==a.central(r.qmul(W,k),r.neg(O))
    assert a.integral(r.ar.mv(OZi,r.flatten(k))) and a.integral(r.ar.mv(OZi,r.flatten(a.qinv(k))))
    assert a.qs(k)==cm["anchor_exchange"]["quaternion"]
    ib=[mf(z) for z in cm["CM_integral_basis"]];ibm=mcoordinates(ib);ibi=mat.inverse(ibm)
    assert matrix_integral(ibm) and abs(mat.determinant(ibm))==1  # O_M=Z[beta], using inherited maximal basis.
    powers=[[mf(z) for z in rows] for rows in witness["generator_power_bases"]]
    assert len(powers)==17;same_lattice(powers[0],ib)
    for c,bs in enumerate(powers):
        assert mideal(bs,ibi)==31**c
        assert matrix_integral(mat.multiply(ibi,mcoordinates(bs)))
        if c:
            inv=mat.inverse(mcoordinates(bs))
            for z in powers[c-1]:
                assert a.integral(r.ar.mv(inv,ms(z,31)))
                assert a.integral(r.ar.mv(inv,mm(ma(BETA,ms(MO,16)),z)))
    old=json.loads((DATA/"cm_orbit.json").read_text())
    same_lattice(powers[1],[mf(z) for z in old["CM_orbit"]["class_generator_ideal_basis"]])
    sigma=mf(witness["sigma_beta"]);assert sigma==ma(mm(mm(BETA,BETA),BETA),ms(BETA,3))
    assert meval(MP,sigma)==MZ
    orbit=[];v=BETA
    for _ in range(16):orbit.append(v);v=meval(v,sigma)
    assert v==BETA and len(set(orbit))==16 and orbit[8]==ms(BETA,-1)
    alpha=witness["sigma_class_multiplier"];assert len({pow(alpha,j,17) for j in range(16)})==16
    gen=mf(witness["sigma_generator_ideal_principal_witness"])
    same_lattice([meval(z,sigma) for z in powers[1]],[mm(gen,z) for z in powers[alpha]])

    # Arithmetic in F[t]/(t^2+y^2+1), retaining the exact D109 local root.
    y=r.f(split["Hensel"]["y"]);h=r.neg(r.add(r.mul(y,y),O));x0=r.f(split["Hensel"]["x0"])
    EZ=(Z,Z);EO=(O,Z)
    def ea(x,y):return r.add(x[0],y[0]),r.add(x[1],y[1])
    def en(x):return r.neg(x[0]),r.neg(x[1])
    def em(x,y):return (r.add(r.mul(x[0],y[0]),r.mul(h,r.mul(x[1],y[1]))),r.add(r.mul(x[0],y[1]),r.mul(x[1],y[0])))
    def escale(x,c):return r.mul(x[0],c),r.mul(x[1],c)
    def ema(x,y):return tuple(ea(u,v) for u,v in zip(x,y))
    def emm(x,y):return tuple(ea(em(x[2*i],y[j]),em(x[2*i+1],y[2+j])) for i in range(2) for j in range(2))
    def esc(x,c):return tuple(escale(v,c) for v in x)
    def parse(m):return tuple((r.f(v[0]),r.f(v[1])) for v in m)
    EI=tuple((c,Z) for c in r.fm(split["I_exact"]))
    EJ=tuple((c,d) for c,d in zip(r.fm(split["J_constant"]),r.fm(split["J_slope"])))
    EK=emm(EI,EJ);EE=(EO,EZ,EZ,EO);standard=(EZ,(r.neg(lam),Z),EO,EZ)
    assert emm(EI,EI)==emm(EJ,EJ)==esc(EE,r.neg(O)) and emm(EI,EJ)==tuple(en(v) for v in emm(EJ,EI))
    basepowers=[(O,Z,Z,Z)]
    for _ in range(15):basepowers.append(r.qmul(basepowers[-1],W))
    def embed(z,qs=basepowers):
        out=(Z,Z,Z,Z)
        for c,v in zip(z,qs):out=tuple(r.add(u,r.scale(w,c)) for u,w in zip(out,v))
        return out
    def localized(v):return a.dyadic(r.ar.mv(OZi,r.flatten(v)))
    assert embed(ma(ms(mm(BETA,BETA),-1),ms(MO,-2)))==(r.PI,Z,Z,Z)
    results=[]
    for idx,row in enumerate(cm["entries"]):
        v,u=r.fm(row["embedded_beta"]),r.fm(row["intertwiner"])
        assert r.qmul(v,v)==(r.neg(lam),Z,Z,Z) and r.qmul(v,u)==r.qmul(u,W)
        if idx:
            e=row["reversed_edge"];t=r.fm(raw["edges"][e]["quaternion"]);sc=r.f(row["normalizing_scalar"])
            assert r.mul(sc,sc)==r.mul(r.qnorm(t),r.inv(lam))
            assert v==a.central(t,r.scale(r.inv(sc),row["sign"]))
            assert raw["edges"][e]["source_class"]==raw["edges"][e]["target_class"]
            assert raw["stabilizers"][raw["edges"][e]["source_class"]]==1
        vp=[(O,Z,Z,Z)]
        for _ in range(15):vp.append(r.qmul(vp[-1],v))
        assert all(localized(embed(z,vp)) for z in ib)
        ideal=[mf(z) for z in row["ideal_basis_power_coordinates"]];norm=mideal(ideal,ibi)
        assert norm==Q(row["ideal_norm"])
        assert all(localized(r.qmul(u,embed(z))) for z in ideal)
        np=norm*r.ar.fnorm(r.qnorm(u));assert np==Q(row["norm_product"])
        assert np>0 and a.dyadic([np,1/np])
        c=row["relative_ideal_class"];saved=witness["principal_class_witnesses"][idx]
        assert saved["index"]==idx and saved["class"]==c
        gen=mf(saved["principal_generator"]);same_lattice(ideal,[mm(gen,z) for z in powers[c]])
        A=ema(ema(esc(EE,v[0]),esc(EI,v[1])),ema(esc(EJ,v[2]),esc(EK,v[3])))
        assert A==parse(row["splitting_matrix"])
        S=(EO,A[0],EZ,A[2]);assert S==parse(row["CM_coordinate_matrix"])
        assert emm(A,S)==emm(S,standard)
        Sc=tuple(r.add(c,r.mul(d,x0)) for c,d in S);Ss=tuple(d for c,d in S)
        assert Sc==r.fm(row["CM_coordinate_center"]) and Ss==r.fm(row["CM_coordinate_slope"])
        error=180+r.mval(r.mmul(r.minv(Sc),Ss))
        assert error==row["CM_coordinate_lattice_error_lower_bound"] and error>=1
        assert 180+r.val(S[3][1])>r.val(r.mdet(Sc))==row["CM_coordinate_determinant_valuation"]
        if idx==0:
            refl=parse(cm["anchor_exchange"]["CM_chart_action"])
            assert emm(EK,S)==emm(S,refl) and emm(refl,standard)==tuple(en(v) for v in emm(standard,refl))
        results.append({"index":idx,"class":c,"coordinate_error":error,"norm_product":str(np)})
    assert sorted(row["class"] for row in results)==list(range(17))
    assert [row["class"] for row in results]==cm["relative_class_labels"]
    assert cm["CM_roots_of_unity"]==2 and cm["dyadic_CM_prime_norm"]==2
    print("CM_REVIEW|17 exact coordinates and principal class witnesses; sigma class multiplier 10",flush=True)
    return results,sigma,alpha

def root_checks(cm,witness,proposal,sigma,alpha):
    assert proposal["CM_polynomial"]==MP and proposal["root_polynomial"]==witness["root_polynomial"]==LP
    roots=[mf(row) for row in proposal["root_centers"]];assert len(roots)==17
    derivative=[i*LP[i] for i in range(1,len(LP))];certificates=[]
    for z in roots:
        n,s=mval(meval(LP,z)),mval(meval(derivative,z));assert n>2*s
        certificates.append({"residual_valuation_beta":n,"derivative_valuation_beta":s,"root_error_valuation_beta":n-s})
    sep=max(mval(ma(x,ms(y,-1))) for i,x in enumerate(roots) for y in roots[:i])
    N=min(c["root_error_valuation_beta"] for c in certificates);assert N>sep
    anchor=next(i for i,z in enumerate(roots) if mval(z)==16)
    assert sorted(mval(z) for z in roots)==[1]*16+[16]
    rational=witness["rational_dyadic_root"];u=int(rational["unit_center"]);g=rational["scaled_polynomial"]
    assert [4*c for c in g]==[c*2**i for i,c in enumerate(LP)]
    assert [v%2 for v in g]==[1,1]+[0]*16
    def evalZ(cs,x):
        v=0
        for c in reversed(cs):v=v*x+c
        return v
    assert evalZ(g,u)%(1<<128)==0 and evalZ([i*g[i] for i in range(1,len(g))],u)%2==1
    theta=int(rational["theta_center"]);assert theta==2*u and r.v2(Q(theta))==1
    assert mval(ma(roots[anchor],ms(MO,-theta)))>sep
    permutation=[];matchbounds=[]
    for z in roots:
        value=meval(z,sigma);ds=[mval(ma(value,ms(w,-1))) for w in roots]
        hits=[i for i,d in enumerate(ds) if d>sep];assert len(hits)==1
        permutation.append(hits[0]);matchbounds.append(ds[hits[0]])
    assert permutation[anchor]==anchor and sorted(permutation)==list(range(17))
    cyc=[];v=next(i for i in range(17) if i!=anchor)
    for _ in range(16):cyc.append(v);v=permutation[v]
    assert v==cyc[0] and len(set(cyc))==16
    old=json.loads((DATA/"cm_orbit.json").read_text());gamma=mf(old["matching"]["resolvent_generator_in_K"])
    assert meval(old["field_root_action"]["resolvent_ascending"],gamma)==MZ
    gamma_roots=[];v=gamma
    for _ in range(16):gamma_roots.append(v);v=meval(v,sigma)
    gamma_sep=max(mval(ma(x,ms(y,-1))) for i,x in enumerate(gamma_roots) for y in gamma_roots[:i])
    assert N>gamma_sep
    candidates=[]
    for mult in range(1,17):
        labels=[0]*17
        for j,i in enumerate(cyc):labels[i]=mult*pow(alpha,j,17)%17
        order=[labels.index(c) for c in range(17)]
        frob=[order[(c+3)%17] for c in labels]
        kappa=MZ
        for j,z in enumerate(roots):kappa=ma(kappa,mm(mm(z,z),roots[frob[j]]))
        distance=mval(ma(kappa,ms(gamma,-1)))
        candidates.append({"multiplier":mult,"distance_to_gamma_beta":distance,"labels":labels,"frob31":frob,"kappa":kappa})
    selected=[c for c in candidates if c["distance_to_gamma_beta"]>gamma_sep];assert len(selected)==1
    selected=selected[0];assert selected["distance_to_gamma_beta"]>=N
    assert all(c is selected or c["distance_to_gamma_beta"]<=gamma_sep for c in candidates)
    labels=selected["labels"];byclass=[labels.index(c) for c in range(17)]
    oldlabels=old["CM_orbit"]["class_labels_in_point_order"]
    oldlookup=old["matching"]["point_to_root_index_zero_based"]
    matching=[]
    for row in cm["entries"]:
        c=row["relative_ideal_class"];point=oldlabels.index(c)
        matching.append({"CM_index":row["index"],"name":row["name"],"ideal_class":c,
                         "saved_complex_point_index":point,"saved_complex_root_index":oldlookup[point],
                         "dyadic_root_index":byclass[c]})
    # Actual algebraic values of the pre-existing rational residue basis, with bounds.
    framepath=DATA/"cm_field_recognition.json";eta=json.loads(framepath.read_text())["field_basis"]["trace_centered_basis_power_coordinates"][1:]
    assert len(eta)==16;P=384
    coeff_bound=min(16*r.v2(Q(c)) for row in eta for c in row if Q(c))
    assert N+coeff_bound>=P
    values=[]
    for item in matching:
        x=roots[item["dyadic_root_index"]]
        values.append([mserialize(truncated_eval(row,x,P)) for row in eta])
    # Sum over all embeddings annihilates each trace-centered basis element.
    assert all(mval(tuple(sum(Q(values[i][j][k]) for i in range(17)) for k in range(16)))>=P for j in range(16))
    assert all(mval(mf(row[0]))==16 for row in values[:1])  # eta_1 at the rational anchor has v_beta=16.
    bad=ma(roots[anchor],MO)
    assert mval(meval(LP,bad))<=2*mval(meval(derivative,bad))
    inverse=[selected["frob31"].index(j) for j in range(17)];wrong=MZ
    for j,z in enumerate(roots):wrong=ma(wrong,mm(mm(z,z),roots[inverse[j]]))
    assert mval(ma(wrong,ms(gamma,-1)))<=gamma_sep
    print(f"ROOT_REVIEW|17 Hensel roots; error >= {N} beta digits; separation <= {sep}; unique resolvent match; frame precision {P}",flush=True)
    return {"root_certificates":certificates,"minimum_root_error_beta":N,"maximum_root_separation_valuation_beta":sep,
      "unique_rational_root_index":anchor,"sigma_root_permutation":permutation,"sigma_match_lower_bound_beta":min(matchbounds),
      "sigma_class_multiplier":alpha,"gamma_conjugate_separation_valuation_beta":gamma_sep,
      "resolvent_candidates":[{k:v for k,v in c.items() if k in ["multiplier","distance_to_gamma_beta"]} for c in candidates],
      "chosen_class_multiplier":selected["multiplier"],"root_class_labels":labels,
      "arithmetic_frobenius31_permutation":selected["frob31"],"CM_point_root_matching":matching,
      "rational_residue_frame_values":values,"rational_residue_frame_error_beta":P,
      "frame_error_pi":P//2,"rational_anchor_theta_center":str(theta),"rational_anchor_theta_error_v2":129,
      "altered_root_rejected":True,"inverse_Artin_cycle_rejected":True}

def computations():
    cm=json.loads((DATA/"dyadic_cm_embeddings_d112.json").read_text())
    witness=json.loads((DATA/"dyadic_cm_class_witnesses_d112.json").read_text())
    raw=json.loads((DATA/"dyadic_quotient_export_d111.json").read_text())
    split=json.loads((DATA/"definite_dyadic_certificate_d109.json").read_text())
    proposal=json.loads((DATA/"dyadic_cm_root_proposals_d112.json").read_text())
    arithmetic,sigma,alpha=arithmetic_checks(cm,witness,raw,split)
    roots=root_checks(cm,witness,proposal,sigma,alpha)
    return {"arithmetic":arithmetic,"roots_and_frame":roots,
            "CM_character_convention":"The chosen local embedding of M is the eigenvalue character at the W anchor; beta maps to the eigenvalue on S*(beta:1).",
            "CM_Artin_convention":"Arithmetic Artin(a): if iota(a)R=xi R then P -> xi^(-1)P; here xi=u^(-1).",
            "geometric_label_proof":"Inertia fixes the W orbit via k; it is the unique K-rational point of D. Use the H-place taking the saved real reference root to the unique Q2 root, and the normalized CM character. See companion report."}

def build():
    result=computations();previous=DATA/"dyadic_harmonic_review_d111.json";prior=json.loads(previous.read_text())
    assert prior["status"]=="pass" and len(prior["sources"])==661
    paths=checked(prior["sources"])+[previous,Path(__file__),REPORT,DATA/"dyadic_cm_matching_sources_d112.json",DATA/"cm_field_recognition.json"]
    for name in ["dyadic_cm_embeddings_d112.json","dyadic_cm_class_witnesses_d112.json","dyadic_cm_root_proposals_d112.json"]:
        p=DATA/name;record=json.loads(p.read_text());paths += [p]+checked(record.get("sources",[]))
    attempts=[]
    for pattern in ["dyadic_cm_embeddings_d112_attempt*.job.json","dyadic_cm_class_witnesses_d112_attempt*.job.json",
                    "dyadic_cm_root_proposals_d112_attempt*.job.json","dyadic_cm_matching_review_d112_probe_attempt*.job.json"]:
        attempts+=list(DATA.glob(pattern))
    for p in sorted(attempts):
        job=json.loads(p.read_text());assert job["timeout_seconds"]==180 and job["timeout_terminates_process_group"]
        paths += checked(job["sources"]+[job["log"]])+[p]
        if job["status"]=="pass":
            assert job["wall_seconds"]<180;paths+=checked([job["driver"]])
        else:
            assert job["status"] in ["failed","timeout"]
            snapshot=p.with_name(p.name.replace(".job.json","_failed"+Path(job["driver"]["path"]).suffix))
            assert source(snapshot)["sha256"]==job["driver"]["sha256"];paths.append(snapshot)
    return {"status":"pass","milestone":"D112","certificates":result,"D111_source_hashes_checked_unchanged":661,
      "dyadic_CM_fixed_points_and_coordinates_certified":True,"dyadic_CM_labels_and_residue_frame_matched":True,
      "actual_moments_computed":False,"actual_harmonic_to_residue_frame_change_computed":False,
      "actual_Shimura_tangent_or_jet_evaluated":False,"candidate_identification_proved":False,
      "target_field_polynomial_constructed":False,
      "sources":[source(p) for p in sorted(set(p.resolve() for p in paths))]}

def main():
    parser=argparse.ArgumentParser(description=__doc__);group=parser.add_mutually_exclusive_group()
    group.add_argument("--probe",action="store_true");group.add_argument("--check",action="store_true");args=parser.parse_args()
    if args.probe:
        result=computations();data=result["roots_and_frame"]
        print(json.dumps({"CM_points":len(result["arithmetic"]),"root_error_beta":data["minimum_root_error_beta"],
              "frame_error_beta":data["rational_residue_frame_error_beta"],"matching":data["CM_point_root_matching"]},indent=2),flush=True)
        print("PASS|D112_CM_MATCHING_PROBE",flush=True);return
    if args.check:old=json.loads(OUT.read_text());checked(old["sources"])
    result=build()
    if args.check:assert result==old
    else:
        assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"pass","source_hashes":len(result["sources"]),"D111_hashes_unchanged":661,
                      "CM_points":17,"frame_error_beta":384}),flush=True)
    print("PASS|D112_CM_MATCHING_REVIEW",flush=True)

if __name__=="__main__":main()

"""D110 independent rational replay of ideal and moving-vertex witnesses.

The group identification uses D99's certified class and unit facts and
the geometric uniformization explained in the accompanying report.
"""
import argparse
from collections import deque
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/"dembele/data/computed"
OUT=DATA/"dyadic_group_transport_review_d110.json"
REPORT=ROOT/"dembele/certificates/dyadic-group-transport-d110.md"
spec=importlib.util.spec_from_file_location("d109",ROOT/"dembele/pari/399_definite_dyadic_review.py")
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
source,checked=r.source,r.checked
Z,O=r.ZERO,r.ONE;mat=r.mat


def central(q,c):return tuple(r.mul(x,c) for x in q)
def qinv(q):return central((q[0],)+tuple(r.neg(x) for x in q[1:]),r.inv(r.qnorm(q)))
def fpow(a,n):
    if n<0:return fpow(r.inv(a),-n)
    out=O
    for _ in range(n):out=r.mul(out,a)
    return out
def fs(x):return list(map(str,x))
def qs(q):return [fs(c) for c in q]
def integral(a):return all(c.denominator==1 for c in a)
def dyadic(a):return all(c.denominator&(c.denominator-1)==0 for c in a)
def matrix_of_basis(basis):return mat.transpose([r.flatten(q) for q in basis])


def computations():
    raw=json.loads((DATA/"dyadic_brandt_transport_export_d110.json").read_text())
    packet=json.loads((DATA/"dyadic_group_transport_d110.json").read_text())
    old=json.loads((DATA/"hyperellipticity_fresh_brandt_d99.json").read_text())
    order=json.loads((DATA/"definite_dyadic_export_d109.json").read_text())
    split=json.loads((DATA/"definite_dyadic_certificate_d109.json").read_text())
    facts=json.loads((DATA/"hyperellipticity_order_review_d99.json").read_text())["order"]
    assert raw["matrix"]==old["matrix"] and raw["stabilizers"]==old["stabilizers"]
    assert raw["order_Z_basis"]==order["order_Z_basis"]
    assert old["class_number"]==old["narrow_class_number"]==facts["class_number_proved"]==1
    signs=[sum(v<<j for j,v in enumerate(row)) for row in facts["unit_signature_rows"]]
    pivots={}
    for a in signs:
        while a:
            j=a.bit_length()-1
            if j not in pivots:pivots[j]=a;break
            a^=pivots[j]
    assert len(pivots)==facts["unit_signature_rank"]==8
    OB=[r.fm(q) for q in raw["order_Z_basis"]];OZ=matrix_of_basis(OB);OZi=mat.inverse(OZ)
    ideals={};ideal_checks=[]
    for row in raw["selected_ideals"]:
        j=row["class_index"];basis=[r.fm(q) for q in row["Z_basis"]]
        M=matrix_of_basis(basis);Mi=mat.inverse(M);inclusion=mat.multiply(OZi,M)
        assert integral(sum(inclusion,[])) and abs(mat.determinant(inclusion))==row["absolute_norm"]**2
        assert all(integral(r.ar.mv(Mi,r.flatten(central(q,r.PI)))) for q in basis)
        assert all(integral(r.ar.mv(Mi,r.flatten(r.qmul(q,v)))) for q in basis for v in OB)
        ideals[j]=(basis,M,Mi)
        ideal_checks.append({"class_index":j,"absolute_norm":row["absolute_norm"],
                             "Z_index_in_order":str(abs(mat.determinant(inclusion))),"right_order_closure_checked":True})
    assert ideal_checks==packet["selected_ideal_checks"] and ideals[0][1]==OZ
    w=(O,Z,Z,Z)
    for k,edge in enumerate(raw["edges"]):
        a,b=edge["source_class"],edge["target_class"]
        assert [a,b]==raw["walk"][k:k+2] and old["matrix"][b][a]==edge["brandt_multiplicity"]
        t=r.fm(edge["quaternion"]);data=packet["edge_inclusion_checks"][k]
        assert data["source_class"]==a and data["target_class"]==b
        image=matrix_of_basis([r.qmul(t,q) for q in ideals[a][0]])
        upper=mat.multiply(ideals[b][2],image)
        lower=mat.multiply(mat.inverse(image),matrix_of_basis([central(q,r.PI) for q in ideals[b][0]]))
        assert upper==mat.matrix(data["upper_inclusion_coordinates"])
        assert lower==mat.matrix(data["lower_inclusion_coordinates"])
        assert integral(sum(upper,[])) and integral(sum(lower,[]))
        assert abs(mat.determinant(upper))==abs(mat.determinant(lower))==4
        w=r.qmul(t,w)
    assert w==r.fm(raw["odd_element"])
    norm=r.qnorm(w)
    assert norm==r.f(raw["odd_element_norm"])==r.f(packet["odd_norm"])
    assert r.val(norm)==7 and r.ar.fnorm(norm)==128 and integral(norm)
    assert w[0]==Z and r.qmul(w,w)==(r.neg(norm),Z,Z,Z)
    lam=r.add(r.scale(O,2),r.PI)
    assert lam==r.f(packet["positive_uniformizer"]) and r.ar.fnorm(lam)==2 and r.val(lam)==1
    a=r.f(packet["normalizing_scalar"])
    assert r.mul(a,a)==r.mul(norm,r.inv(lam)) and r.val(a)==packet["normalizing_scalar_valuation"]==3
    W=central(w,r.inv(a));u=r.fm(split["transport"]["quaternion"])
    g=r.qmul(r.qmul(W,u),qinv(W))
    assert r.qnorm(W)==lam and r.qmul(W,W)==(r.neg(lam),Z,Z,Z)
    assert g==r.fm(raw["norm_one_moving_element"]) and r.qnorm(g)==O
    membership={}
    for name,q in [("w",w),("w_inverse",qinv(w)),("W",W),("W_inverse",qinv(W)),("g",g),("g_inverse",qinv(g))]:
        coords=r.ar.mv(OZi,r.flatten(q));assert dyadic(coords)
        membership[name]={"order_coordinates":list(map(str,coords)),
                          "maximum_denominator_2_exponent":max(c.denominator.bit_length()-1 for c in coords)}
    assert membership==packet["localized_order_membership"]
    # Exact conjugation matrices on the localized order exhibit normalizer membership.
    conjugation={}
    for name,q in [("W",W),("g",g)]:
        cols=[r.ar.mv(OZi,r.flatten(r.qmul(r.qmul(q,v),qinv(q)))) for v in OB]
        action=mat.transpose(cols);reverse=mat.inverse(action)
        assert dyadic(sum(action,[])) and dyadic(sum(reverse,[]))
        assert mat.determinant(action)==1
        conjugation[name]={"matrix":[list(map(str,row)) for row in action],
                           "inverse_matrix":[list(map(str,row)) for row in reverse]}
        if name=="W":assert mat.multiply(action,action)==mat.identity(32)

    I,Jc,Jt=[r.fm(split[k]) for k in ["I_exact","J_constant","J_slope"]]
    x0=r.f(split["Hensel"]["x0"]);d=split["Hensel"]["root_error_valuation"]
    def image(q):
        const=r.madd(r.madd(r.mscale(r.E,q[0]),r.mscale(I,q[1])),
                     r.madd(r.mscale(Jc,q[2]),r.mscale(r.mmul(I,Jc),q[3])))
        slope=r.madd(r.mscale(Jt,q[2]),r.mscale(r.mmul(I,Jt),q[3]))
        return r.madd(const,r.mscale(slope,x0)),slope
    distances={};errors={}
    for name,q in [("w",w),("W",W),("g",g)]:
        saved=packet["transports"][name];assert r.fm(saved["quaternion"])==q
        center,slope=image(q);norm=r.qnorm(q);minimum=r.mval(center);nv=r.val(norm)
        error=d+r.mval(slope);distance=nv-2*minimum
        assert error>minimum and distance>0
        assert center==r.fm(saved["matrix_center"]) and slope==r.fm(saved["matrix_slope"])
        assert norm==r.f(saved["reduced_norm"]) and nv==saved["norm_valuation"]
        assert minimum==saved["minimum_entry_valuation"] and error==saved["matrix_error_lower_bound"]
        assert distance==saved["base_vertex_displacement"] and -minimum==saved["homothety_power"]
        rr=Z
        for j,bit in enumerate(saved["target_digits"]):
            assert bit in [0,1]
            rr=r.add(rr,r.scale(fpow(r.PI,j),bit))
        assert len(saved["target_digits"])==distance
        L=(rr,fpow(r.PI,distance),O,Z) if saved["target_rows_swapped"] else (O,Z,rr,fpow(r.PI,distance))
        assert L==r.fm(saved["target_lattice"])
        H=r.mscale(center,fpow(r.PI,-minimum));Hs=r.mscale(slope,fpow(r.PI,-minimum))
        U=r.mmul(r.minv(L),H);V=r.mmul(r.minv(L),Hs)
        determinant=r.mul(r.mul(norm,fpow(r.PI,-2*minimum)),r.inv(r.mdet(L)))
        assert r.mval(U)>=0 and d+r.mval(V)>=1 and r.val(determinant)==0
        assert U==r.fm(saved["transition_center"]) and V==r.fm(saved["transition_slope"])
        assert determinant==r.f(saved["exact_transition_determinant"])
        assert d+r.mval(V)==saved["transition_error_lower_bound"]
        assert r.val(r.mdet(center))==nv
        distances[name]=distance;errors[name]=d+r.mval(V)
    assert distances=={"w":7,"W":7,"g":14}
    # g is finite projective order three; do not label it a hyperbolic generator.
    g2=r.qmul(g,g);g3=r.qmul(g2,g)
    assert g3==(r.neg(O),Z,Z,Z)
    # A derived product also gives a hyperbolic norm-one element, without any search.
    h=r.qmul(u,g);hc,hs=image(h);htrace=r.scale(h[0],2)
    assert r.qnorm(h)==O and dyadic(r.ar.mv(OZi,r.flatten(h)))
    assert r.val(htrace)==-7 and r.mval(hc)==-7 and d+r.mval(hs)>-7
    # X^2-tr(h)X+1 has Newton slopes -7,7, proving translation length 14.
    hyperbolic={"quaternion":qs(h),"reduced_trace":fs(htrace),"trace_valuation":-7,
                "reduced_norm":"1","translation_length":14,"base_vertex_displacement":14}

    queue=deque([(0,0)]);dist={(0,0):0}
    while (0,1) not in dist:
        v,s=queue.popleft()
        for z in range(58):
            state=z,1-s
            if old["matrix"][z][v] and state not in dist:
                dist[state]=dist[v,s]+1;queue.append(state)
    assert dist[0,1]==7==packet["shortest_odd_closed_walk_length"]
    # Controls: odd norm is incompatible with Gamma; pretending g fixes v0 fails.
    assert r.val(r.qnorm(W))%2==1
    gc,gs=image(g)
    assert r.mval(gc)<0 and d+r.mval(gs)>r.mval(gc)
    assert r.val(r.qnorm(g))==0  # Thus no scalar rescaling can make it GL2(O_K).
    return {"D99_matrix_and_stabilizers_replayed_identically":True,"D109_order_basis_identical":True,
            "unit_signature_rank":8,"selected_right_ideals":4,"right_order_products_checked":4096,
            "exact_ideal_sandwiches_checked":7,"each_inclusion_Z_index":4,
            "shortest_odd_closed_walk_length":7,"normalized_odd_element_square":"-(2+b)",
            "normalized_odd_projective_order":2,"norm_parity_quotient_order":2,
            "localized_order_conjugation":conjugation,"base_vertex_displacements":distances,
            "transition_error_lower_bounds":errors,"moving_norm_one_projective_order":3,
            "derived_hyperbolic_element":hyperbolic,
            "odd_element_rejected_from_norm_one_projective_group":True,
            "false_base_vertex_stabilization_rejected":True,
            "full_fundamental_domain_or_harmonic_cocycle_computed":False}


def build():
    result=computations()
    previous=DATA/"definite_dyadic_review_d109.json";prior=json.loads(previous.read_text())
    assert prior["status"]=="pass" and len(prior["sources"])==629
    paths=checked(prior["sources"])+[previous,Path(__file__),REPORT,DATA/"dyadic_group_transport_sources_d110.json"]
    for name in ["dyadic_brandt_transport_export_d110.json","dyadic_group_transport_d110.json"]:
        p=DATA/name;record=json.loads(p.read_text());paths+=[p]+checked(record.get("sources",[]))
    attempts=list(DATA.glob("dyadic_brandt_transport_export_d110_attempt*.job.json"))
    attempts+=list(DATA.glob("dyadic_group_transport_d110_attempt*.job.json"))
    for p in sorted(attempts):
        job=json.loads(p.read_text());assert job["timeout_seconds"]==180 and job["timeout_terminates_process_group"]
        paths+=checked(job["sources"]+[job["log"]])+[p]
        if job["status"]=="pass":
            assert job["wall_seconds"]<180;paths+=checked([job["driver"]])
        else:
            assert job["status"] in ["failed","timeout"]
            snapshot=p.with_name(p.name.replace(".job.json","_failed"+Path(job["driver"]["path"]).suffix))
            assert source(snapshot)["sha256"]==job["driver"]["sha256"];paths.append(snapshot)
    for p in sorted(DATA.glob("dyadic_group_transport_review_d110_probe_attempt*.job.json")):
        job=json.loads(p.read_text());paths+=checked(job["sources"]+[job["log"]])+[p]
        if job["status"]=="pass":paths+=checked([job["driver"]])
        else:
            snapshot=p.with_name(p.name.replace(".job.json","_failed.py"))
            assert source(snapshot)["sha256"]==job["driver"]["sha256"];paths.append(snapshot)
    return {"status":"pass","milestone":"D110","certificates":result,
            "D109_source_hashes_checked_unchanged":629,
            "group_and_Atkin_Lehner_coset_instantiated":True,"moving_vertex_transport_certified":True,
            "full_fundamental_domain_constructed":False,"actual_harmonic_cocycle_or_moments_computed":False,
            "actual_dyadic_CM_matching_proved":False,"actual_Shimura_tangent_or_jet_evaluated":False,
            "candidate_identification_proved":False,"target_field_polynomial_constructed":False,
            "sources":[source(p) for p in sorted(set(p.resolve() for p in paths))]}


def main():
    parser=argparse.ArgumentParser(description=__doc__);group=parser.add_mutually_exclusive_group()
    group.add_argument("--check",action="store_true");group.add_argument("--probe",action="store_true")
    args=parser.parse_args()
    if args.probe:
        result=computations()
        print(json.dumps({k:v for k,v in result.items() if k!="localized_order_conjugation"},indent=2),flush=True)
        print("PASS|D110_GROUP_PROBE",flush=True);return
    if args.check:old=json.loads(OUT.read_text());checked(old["sources"])
    result=build()
    if args.check:assert result==old
    else:
        assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"pass","source_hashes":len(result["sources"]),
                      "D109_hashes_unchanged":629,"vertex_displacement":14}),flush=True)
    print("PASS|D110_GROUP_REVIEW",flush=True)


if __name__=="__main__":main()

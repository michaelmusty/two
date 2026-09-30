"""D111 independent rational verification, without Sage or Magma.

Checks the complete finite certificate and replays the arithmetic reducer.
The 58-class and full unit counts retain the certified Magma provenance of
D99/D110. Local-to-global arguments are stated in the accompanying report.
"""
import argparse
from functools import lru_cache
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/"dembele/data/computed"
OUT=DATA/"dyadic_harmonic_review_d111.json"
REPORT=ROOT/"dembele/certificates/dyadic-harmonic-d111.md"
spec=importlib.util.spec_from_file_location("reducer",ROOT/"dembele/pari/405_dyadic_edge_reducer.py")
runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)
a,r=runtime.a,runtime.r;Z,O=r.ZERO,r.ONE;mat=r.mat
source,checked=r.source,r.checked

def rank_mod(rows,p):
    piv={}
    for row in rows:
        row=[v%p for v in row]
        for j in range(len(row)):
            if not row[j]:continue
            if j in piv:
                c=row[j];row=[(x-c*y)%p for x,y in zip(row,piv[j])]
            else:
                inv=pow(row[j],-1,p);piv[j]=[(c*inv)%p for c in row];break
    return len(piv)

@lru_cache(None)
def canonical(q):return a.central(q,r.inv(next(c for c in q if c!=Z)))

def computations():
    raw=json.loads((DATA/"dyadic_quotient_export_d111.json").read_text())
    packet=json.loads((DATA/"dyadic_harmonic_certificate_d111.json").read_text())
    old=json.loads((DATA/"hyperellipticity_fresh_brandt_d99.json").read_text())
    order=json.loads((DATA/"definite_dyadic_export_d109.json").read_text())
    assert raw["matrix"]==old["matrix"] and raw["stabilizers"]==old["stabilizers"]
    assert raw["order_Z_basis"]==order["order_Z_basis"]
    assert not raw["new_level_or_prime"] and not raw["expanded_class_census"]
    split=runtime.Splitting();assert split.error==180
    OB=[r.fm(v) for v in raw["order_Z_basis"]];OZ=a.matrix_of_basis(OB);OZi=mat.inverse(OZ)
    def localized(q):return a.dyadic(r.ar.mv(OZi,r.flatten(q)))
    frames=[];inverses=[];keys=[];permutations=[];frame_errors=[];unit_errors=[]
    for j,row in enumerate(raw["ideals"]):
        assert row["class_index"]==j
        saved=packet["ideal_checks"][j];assert saved["class_index"]==j
        basis=[r.fm(v) for v in row["Z_basis"]];M=a.matrix_of_basis(basis);Mi=mat.inverse(M)
        inc=mat.multiply(OZi,M);n=row["norm_exponent"]
        assert a.integral(sum(inc,[])) and abs(mat.determinant(inc))==2**(2*n)
        assert saved["Z_index_in_order"]==str(2**(2*n)) and saved["norm_exponent"]==n
        assert all(a.integral(r.ar.mv(Mi,r.flatten(a.central(v,r.PI)))) for v in basis)
        L=r.fm(saved["local_frame"]);Li=r.minv(L);assert r.val(r.mdet(L))==n
        if j==0:assert M==OZ and L==r.E
        residues=[];errors=[]
        for v in basis:
            C,S=split.image(v);C=r.mmul(Li,C);S=r.mmul(Li,S)
            assert r.mval(C)>=0 and split.error+r.mval(S)>=1
            residues.append(runtime.residue(C));errors.append(split.error+r.mval(S))
        assert rank_mod(residues,2)==saved["local_order_module_residue_rank"]==4
        assert min(errors)==saved["frame_error_lower_bound"];frame_errors+=errors
        U=[r.fm(v) for v in row["stabilizer_units"]];K=[canonical(v) for v in U]
        assert len(U)==old["stabilizers"][j] and len(set(K))==len(U)
        assert (O,Z,Z,Z) in K
        perms=[];errors=[]
        for v in U:
            assert r.qnorm(v)==O and localized(v) and localized(a.qinv(v))
            C,S=split.image(v);C=r.mmul(r.mmul(Li,C),L);S=r.mmul(r.mmul(Li,S),L)
            assert r.mval(C)>=0 and split.error+r.mval(S)>=1
            bits=runtime.residue(C);assert (bits[0]*bits[3]-bits[1]*bits[2])%2==1
            perms.append([runtime.LINES.index(tuple(sum(bits[2*i+k]*l[k] for k in range(2))%2 for i in range(2))) for l in runtime.LINES])
            errors.append(split.error+r.mval(S))
        assert all(canonical(r.qmul(v,w)) in K for v in U for w in U)
        assert perms==saved["stabilizer_permutations"] and min(errors)==saved["stabilizer_error_lower_bound"]
        frames.append(L);inverses.append(Li);keys.append(K);permutations.append(perms);unit_errors+=errors
    assert len(frames)==58 and sum(map(len,keys))==164
    print("REVIEW|58 p-supported global ideals and exact local frames; all 164 stabilizer elements",flush=True)
    stars=[[-1]*3 for _ in frames];edges=[];counts=[[0]*58 for _ in frames];edge_errors=[]
    for k,row in enumerate(raw["edges"]):
        j,i=row["source_class"],row["target_class"];t=r.fm(row["quaternion"]);ti=a.qinv(t)
        assert localized(t) and localized(ti)
        nt=r.qnorm(t);assert r.val(nt)==1+raw["ideals"][i]["norm_exponent"]-raw["ideals"][j]["norm_exponent"]
        C,S=split.image(ti)
        C=r.mscale(r.mmul(r.mmul(inverses[j],C),frames[i]),r.PI)
        S=r.mscale(r.mmul(r.mmul(inverses[j],S),frames[i]),r.PI)
        fe=split.error+r.mval(S);assert r.mval(C)>=0 and fe>=1
        exactdet=r.mul(r.mul(runtime.power(r.PI,2),r.inv(nt)),r.mul(r.mdet(frames[i]),r.inv(r.mdet(frames[j]))))
        assert r.val(exactdet)==1;forward=runtime.line(C)
        C,S=split.image(t);C=r.mmul(r.mmul(inverses[i],C),frames[j]);S=r.mmul(r.mmul(inverses[i],S),frames[j])
        re=split.error+r.mval(S);assert r.mval(C)>=0 and re>=1
        exactdet=r.mul(nt,r.mul(r.mdet(frames[j]),r.inv(r.mdet(frames[i]))))
        assert r.val(exactdet)==1;reverse=runtime.line(C)
        assert stars[j][forward]==-1;stars[j][forward]=k;counts[i][j]+=1;edge_errors += [fe,re]
        edges.append({"source_class":j,"target_class":i,"line":forward,"reverse_line":reverse,
                      "forward_error_lower_bound":fe,"reverse_error_lower_bound":re,"each_global_inclusion_Z_index":4})
    assert len(edges)==174 and all(-1 not in star for star in stars)
    assert stars==packet["stars"] and counts==old["matrix"]
    relations=[]
    def relation(terms):
        row=[0]*174
        for k,v in terms:row[k]+=v
        if any(row):relations.append(row)
    for j,star in enumerate(stars):
        relation([(e,1) for e in star])
        for perm in permutations[j]:
            for l in range(3):
                assert edges[star[l]]["target_class"]==edges[star[perm[l]]]["target_class"]
                relation([(star[l],1),(star[perm[l]],-1)])
    for k,row in enumerate(edges):
        j,i=row["source_class"],row["target_class"];rev=stars[i][row["reverse_line"]]
        assert edges[rev]["target_class"]==j;row["reverse_edge"]=rev
        v=a.central(r.qmul(r.fm(raw["edges"][rev]["quaternion"]),r.fm(raw["edges"][k]["quaternion"])),r.inv(r.PI))
        row["reverse_stabilizer_index"]=keys[j].index(canonical(v))
        relation([(k,1),(rev,1)])
    assert edges==packet["edges"] and relations==packet["harmonic_relations"]
    basis=packet["harmonic_basis"]
    assert len(basis)==16 and all(len(b)==174 and all(type(c) is int for c in b) for b in basis)
    assert all(sum(x*y for x,y in zip(row,b))==0 for row in relations for b in basis)
    hrank,brank=rank_mod(relations,101),rank_mod(basis,101)
    assert hrank==packet["relation_rank"]==158 and brank==packet["harmonic_dimension"]==16
    # Independent orbit calculation by repeatedly saturating each three-element star.
    unseen=set(range(174));orbits=[]
    while unseen:
        e=min(unseen);j=edges[e]["source_class"];orbit={e};changed=True
        while changed:
            nxt=orbit|{stars[j][perm[edges[v]["line"]]] for v in orbit for perm in permutations[j]}
            changed=nxt!=orbit;orbit=nxt
        assert orbit<=unseen;unseen-=orbit;orbits.append(sorted(orbit))
    assert {tuple(es) for es in orbits}=={tuple(es) for es in packet["oriented_edge_orbits"]}
    which={e:j for j,es in enumerate(orbits) for e in es};rev={}
    for j,es in enumerate(orbits):
        rs={which[edges[e]["reverse_edge"]] for e in es};assert len(rs)==1;rev[j]=rs.pop()
    assert all(rev[rev[j]]==j for j in rev)
    inverted=[es for j,es in enumerate(orbits) if rev[j]==j]
    assert len(orbits)==155 and len(inverted)==9 and (len(orbits)-len(inverted))//2==73
    assert {tuple(es) for es in inverted}=={tuple(es) for es in packet["inverted_edge_orbits"]}
    assert all(b[e]==0 for b in basis for es in inverted for e in es)
    assert max(abs(c) for b in basis for c in b)==packet["basis_maximum_absolute_integer"]==4
    assert packet["measure_denominator_bound"]==0
    bad=list(basis[0]);bad[0]+=1
    assert any(sum(x*y for x,y in zip(row,bad))!=0 for row in relations)
    print("REVIEW|376 exact relations; rank 158 and 16 independent integral cocycles verified",flush=True)
    validations=runtime.validations()
    assert validations==json.loads((DATA/"dyadic_edge_reducer_d111.json").read_text())
    return {"classes":58,"stabilizer_elements":164,"outgoing_edge_slots":174,"oriented_edge_orbits":155,
      "inverted_edge_orbits":9,"noninverted_unoriented_edge_orbits":73,"relations":len(relations),
      "relation_rank_mod_101":hrank,"basis_rank_mod_101":brank,"harmonic_dimension":16,
      "measure_denominator_bound":0,"basis_maximum_absolute_integer":4,
      "minimum_frame_error":min(frame_errors),"minimum_stabilizer_error":min(unit_errors),
      "minimum_neighbor_error":min(edge_errors),"all_local_stars_and_reversals_verified":True,
      "p_supported_indices_and_local_frames_prove_global_right_ideal_and_sandwich_assertions":True,
      "reducer_sample_stars":len(validations["samples"]),"nonzero_sample_edges":validations["nonzero_sample_edges"],
      "sample_depth_maximum":32,"adaptive_root_errors":validations["adaptive_precision"]["root_error_sequence"],
      "arithmetic_invariance_checked_for":[row["element"] for row in validations["arithmetic_invariance_samples"]],
      "altered_cocycle_rejected":True,"nonadjacent_input_rejected":validations["nonadjacent_input_rejected"]}

def build():
    result=computations();previous=DATA/"dyadic_group_transport_review_d110.json"
    prior=json.loads(previous.read_text());assert prior["status"]=="pass" and len(prior["sources"])==643
    paths=checked(prior["sources"])+[previous,Path(__file__),REPORT,DATA/"dyadic_harmonic_sources_d111.json"]
    for name in ["dyadic_quotient_export_d111.json","dyadic_harmonic_certificate_d111.json","dyadic_edge_reducer_d111.json"]:
        p=DATA/name;record=json.loads(p.read_text());paths += [p]+checked(record.get("sources",[]))
    attempts=[]
    for pattern in ["dyadic_quotient_export_d111_attempt*.job.json","dyadic_harmonic_certificate_d111_attempt*.job.json",
                    "dyadic_edge_reducer_d111_attempt*.job.json","dyadic_harmonic_review_d111_probe_attempt*.job.json"]:
        attempts+=list(DATA.glob(pattern))
    for p in sorted(attempts):
        job=json.loads(p.read_text());assert job["timeout_seconds"]==180 and job["timeout_terminates_process_group"]
        paths+=checked(job["sources"]+[job["log"]])+[p]
        if job["status"]=="pass":
            assert job["wall_seconds"]<180;paths+=checked([job["driver"]])
        else:
            assert job["status"] in ["failed","timeout"]
            snapshot=p.with_name(p.name.replace(".job.json","_failed"+Path(job["driver"]["path"]).suffix))
            assert source(snapshot)["sha256"]==job["driver"]["sha256"];paths.append(snapshot)
    return {"status":"pass","milestone":"D111","certificates":result,"D110_source_hashes_checked_unchanged":643,
      "finite_arithmetic_edge_reducer_constructed":True,"actual_invariant_harmonic_cocycles_constructed":True,
      "full_generating_set_or_connected_fundamental_domain_constructed":False,
      "actual_moments_computed":False,"actual_dyadic_CM_matching_proved":False,
      "actual_Shimura_tangent_or_jet_evaluated":False,"candidate_identification_proved":False,
      "target_field_polynomial_constructed":False,"sources":[source(p) for p in sorted(set(p.resolve() for p in paths))]}

def main():
    parser=argparse.ArgumentParser(description=__doc__);group=parser.add_mutually_exclusive_group()
    group.add_argument("--probe",action="store_true");group.add_argument("--check",action="store_true");args=parser.parse_args()
    if args.probe:
        print(json.dumps(computations(),indent=2),flush=True);print("PASS|D111_HARMONIC_PROBE",flush=True);return
    if args.check:old=json.loads(OUT.read_text());checked(old["sources"])
    result=build()
    if args.check:assert result==old
    else:
        assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"pass","source_hashes":len(result["sources"]),"D110_hashes_unchanged":643,
                      "harmonic_dimension":16,"measure_denominator_bound":0}),flush=True)
    print("PASS|D111_HARMONIC_REVIEW",flush=True)

if __name__=="__main__":main()

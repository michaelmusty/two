"""D111: exact local frames, all stars/stabilizers, and scalar harmonic basis.

Global lattice assertions follow from the exact p-supported index and local
equalities; this avoids repeating all 58*1024 order products. No moments or CM
labels are inferred. Run with Sage through bounded runner 272.
"""
import hashlib
import json
from pathlib import Path
from sage.all import QQ, ZZ, NumberField, PolynomialRing, matrix, vector, identity_matrix, gcd, lcm

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/"dembele/data/computed"

def source(path):
    path=Path(path).resolve()
    return {"path":str(path),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
    out=DATA/"dyadic_harmonic_certificate_d111.json";assert not out.exists()
    rawpath=DATA/"dyadic_quotient_export_d111.json";raw=json.loads(rawpath.read_text())
    oldpath=DATA/"hyperellipticity_fresh_brandt_d99.json";old=json.loads(oldpath.read_text())
    orderpath=DATA/"definite_dyadic_export_d109.json";order=json.loads(orderpath.read_text())
    splitpath=DATA/"definite_dyadic_certificate_d109.json";split=json.loads(splitpath.read_text())
    assert raw["matrix"]==old["matrix"] and raw["stabilizers"]==old["stabilizers"]
    assert raw["order_Z_basis"]==order["order_Z_basis"]
    P=PolynomialRing(QQ,"x");x=P.gen();F=NumberField(x**8-8*x**6+20*x**4-16*x*x+2,"b");b=F.gen()
    def f(row):return F([QQ(c) for c in row])
    def q(row):return vector(F,[f(c) for c in row])
    def m(row):return matrix(F,2,2,[f(c) for c in row])
    def fs(c):return list(map(str,F(c).list()))
    def ms(M):return [fs(c) for c in M.list()]
    def val(c):return min((8*a.valuation(2)+i for i,a in enumerate(F(c).list()) if a),default=10**9)
    def mv(M):return min(map(val,M.list()))
    def qm(q,r):
        a,c,d,e=q;A,C,D,E=r
        return vector(F,[a*A-c*C-d*D-e*E,a*C+c*A+d*E-e*D,a*D+d*A+e*C-c*E,a*E+e*A+c*D-d*C])
    def norm(q):return sum(c*c for c in q)
    def qi(q):return vector(F,[q[0],-q[1],-q[2],-q[3]])/norm(q)
    def flat(q):return vector(QQ,sum([list(F(c)) for c in q],[]))
    def zm(basis):return matrix(QQ,[flat(q) for q in basis]).transpose()
    def integral(M):return all(c.denominator()==1 for c in M.list())
    def canonical(q):return tuple(q/next(c for c in q if c))
    E=identity_matrix(F,2);I=m(split["I_exact"]);Jc=m(split["J_constant"]);Jt=m(split["J_slope"])
    IJc=I*Jc;IJt=I*Jt;x0=f(split["Hensel"]["x0"]);d=split["Hensel"]["root_error_valuation"]
    def image(q):
        slope=q[2]*Jt+q[3]*IJt
        return q[0]*E+q[1]*I+q[2]*Jc+q[3]*IJc+x0*slope,slope
    def residue(M):
        assert mv(M)>=0
        return [int(val(c)==0) for c in M.list()]
    lines=[(1,0),(0,1),(1,1)]
    def line(M):
        a,c,e,g=residue(M);cols=[(a,e),(c,g)];nz=[v for v in cols if v!=(0,0)]
        assert nz and all(v==nz[0] for v in nz)
        return lines.index(nz[0])
    def rank2(rows):
        piv={}
        for row in rows:
            a=sum(v<<i for i,v in enumerate(row))
            while a:
                k=a.bit_length()-1
                if k not in piv:piv[k]=a;break
                a^=piv[k]
        return len(piv)
    OB=[q(v) for v in raw["order_Z_basis"]];OZ=zm(OB);OZi=OZ.inverse()
    def localized(q):return all(c.denominator().is_power_of(2) for c in OZi*flat(q))
    frames=[];Li=[];units=[];unitkeys=[];ideal_checks=[]
    for j,row in enumerate(raw["ideals"]):
        assert row["class_index"]==j
        basis=[q(v) for v in row["Z_basis"]];Z=zm(basis);Zi=Z.inverse();n=row["norm_exponent"]
        inclusion=OZi*Z
        assert integral(inclusion) and abs(inclusion.det())==2**(2*n)
        assert all(integral(Zi*flat(b*v)) for v in basis)
        images=[image(v) for v in basis];cols=[C.column(k) for C,S in images for k in range(2)]
        a=min(val(c) for v in cols for c in v)
        v=next(v for v in cols if min(map(val,v))==a)
        candidates=[matrix(F,2,2,[v[0],w[0],v[1],w[1]]) for w in cols]
        H=min(candidates,key=lambda C:val(C.det()));assert val(H.det())==n
        H/=b**a;delta=n-2*a
        pivot=0 if any(val(H[0,k])==0 for k in range(2)) else 1
        k=next(k for k in range(2) if val(H[pivot,k])==0)
        ratio=H[1-pivot,k]/H[pivot,k];rr=F(0);digits=[]
        for k in range(delta):
            rem=(ratio-rr)/b**k;assert val(rem)>=0
            bit=int(val(rem)==0);digits.append(bit);rr+=bit*b**k
        assert val(ratio-rr)>=delta
        L=b**a*(matrix(F,[[1,0],[rr,b**delta]]) if pivot==0 else matrix(F,[[rr,b**delta],[1,0]]))
        if j==0:L=E;assert Z==OZ and n==0
        L_inv=L.inverse();assert val(L.det())==n
        residues=[];errors=[]
        for C,S in images:
            assert mv(L_inv*C)>=0 and d+mv(L_inv*S)>=1
            residues.append(residue(L_inv*C));errors.append(d+mv(L_inv*S))
        assert rank2(residues)==4
        U=[q(v) for v in row["stabilizer_units"]];keys=[canonical(v) for v in U]
        assert len(U)==raw["stabilizers"][j] and len(set(keys))==len(U)
        assert canonical(vector(F,[1,0,0,0])) in keys
        permutations=[];ue=[]
        for v in U:
            assert norm(v)==1 and localized(v) and localized(qi(v))
            C,S=image(v);C=L_inv*C*L;S=L_inv*S*L
            assert mv(C)>=0 and d+mv(S)>=1
            bits=residue(C);A=matrix(ZZ,2,2,bits)
            assert A.det()%2==1
            permutations.append([lines.index(tuple(int(c%2) for c in A*vector(ZZ,l))) for l in lines])
            ue.append(d+mv(S))
        assert all(canonical(qm(v,w)) in keys for v in U for w in U)
        frames.append(L);Li.append(L_inv);units.append(U);unitkeys.append(keys)
        ideal_checks.append({"class_index":j,"norm_exponent":n,"Z_index_in_order":str(2**(2*n)),
          "local_frame":ms(L),"local_order_module_residue_rank":4,"frame_error_lower_bound":int(min(errors)),
          "stabilizer_permutations":permutations,"stabilizer_error_lower_bound":int(min(ue))})
    print("FRAMES|58 exact local right-ideal frames; 164 projective stabilizer elements checked",flush=True)
    stars=[[-1]*3 for _ in frames];edges=[]
    counts=[[0]*58 for _ in frames]
    for k,row in enumerate(raw["edges"]):
        j,i=row["source_class"],row["target_class"];t=q(row["quaternion"])
        assert localized(t) and localized(qi(t));assert val(norm(t))==1+raw["ideals"][i]["norm_exponent"]-raw["ideals"][j]["norm_exponent"]
        C,S=image(qi(t));C=b*Li[j]*C*frames[i];S=b*Li[j]*S*frames[i]
        assert mv(C)>=0 and d+mv(S)>=1 and val(C.det())==1
        forward=line(C);fe=d+mv(S)
        C,S=image(t);C=Li[i]*C*frames[j];S=Li[i]*S*frames[j]
        assert mv(C)>=0 and d+mv(S)>=1 and val(C.det())==1
        reverse=line(C);re=d+mv(S)
        assert stars[j][forward]==-1;stars[j][forward]=k;counts[i][j]+=1
        edges.append({"source_class":j,"target_class":i,"line":forward,"reverse_line":reverse,
          "forward_error_lower_bound":int(fe),"reverse_error_lower_bound":int(re),"each_global_inclusion_Z_index":4})
    assert counts==raw["matrix"] and all(-1 not in s for s in stars)
    relations=[]
    def relation(terms):
        row=[0]*174
        for k,v in terms:row[k]+=v
        if any(row):relations.append(row)
    for j,star in enumerate(stars):
        relation([(e,1) for e in star])
        for perm in ideal_checks[j]["stabilizer_permutations"]:
            for l in range(3):
                assert edges[star[l]]["target_class"]==edges[star[perm[l]]]["target_class"]
                relation([(star[l],1),(star[perm[l]],-1)])
    for k,row in enumerate(edges):
        rev=stars[row["target_class"]][row["reverse_line"]];row["reverse_edge"]=rev
        assert edges[rev]["target_class"]==row["source_class"]
        v=qm(q(raw["edges"][rev]["quaternion"]),q(raw["edges"][k]["quaternion"]))/b
        row["reverse_stabilizer_index"]=unitkeys[row["source_class"]].index(canonical(v))
        relation([(k,1),(rev,1)])
    H=matrix(QQ,relations);ker=H.right_kernel();assert ker.dimension()==16 and H.rank()==158
    basis=[]
    for v in ker.basis():
        vv=vector(ZZ,v*lcm(c.denominator() for c in v));vv/=gcd(list(vv))
        basis.append([int(c) for c in vv])
    assert H*matrix(QQ,basis).transpose()==0
    # Quotient of oriented slots by the full vertex stabilizers.
    parent=list(range(174))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(i,j):parent[find(i)]=find(j)
    for j,star in enumerate(stars):
        for perm in ideal_checks[j]["stabilizer_permutations"]:
            for l in range(3):union(star[l],star[perm[l]])
    orbits={}
    for e in range(174):orbits.setdefault(find(e),[]).append(e)
    revmap={a:find(edges[es[0]]["reverse_edge"]) for a,es in orbits.items()}
    assert all(find(edges[e]["reverse_edge"])==revmap[a] for a,es in orbits.items() for e in es)
    assert all(revmap[revmap[a]]==a for a in revmap)
    inverted=[es for a,es in orbits.items() if revmap[a]==a]
    assert len(orbits)==155 and len(inverted)==9
    assert all(b[e]==0 for b in basis for es in inverted for e in es)
    result={"status":"pass","milestone":"D111","ideal_checks":ideal_checks,"stars":stars,"edges":edges,
      "harmonic_relations":relations,"harmonic_basis":basis,"harmonic_dimension":16,"relation_rank":158,
      "oriented_edge_orbits":list(orbits.values()),"inverted_edge_orbits":inverted,
      "noninverted_unoriented_edge_orbits":73,"measure_denominator_bound":0,
      "basis_maximum_absolute_integer":max(abs(c) for row in basis for c in row),
      "actual_invariant_harmonic_cocycles_constructed":True,"actual_moments_or_Shimura_jet_computed":False,
      "sources":[source(p) for p in [Path(__file__),rawpath,oldpath,orderpath,splitpath]]}
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("HARMONIC|174 slots; 155 oriented orbits; 9 inverted orbits; rank 158; dimension 16; bound d=0",flush=True)
    print("PASS|404_dyadic_harmonic_certificate",flush=True)

if __name__=="__main__":main()

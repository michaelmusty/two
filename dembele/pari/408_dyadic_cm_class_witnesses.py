"""D112: replayable principal-ideal witnesses and the unique rational dyadic root."""
import hashlib
import json
from pathlib import Path
from sage.all import QQ, ZZ, NumberField, PolynomialRing

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/"dembele/data/computed"

def source(p):
    p=Path(p).resolve();return {"path":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}

def main():
    out=DATA/"dyadic_cm_class_witnesses_d112.json";assert not out.exists()
    old=json.loads((DATA/"cm_orbit.json").read_text());cm=json.loads((DATA/"dyadic_cm_embeddings_d112.json").read_text())
    P=PolynomialRing(QQ,"x");x=P.gen();M=NumberField(P(old["CM_orbit"]["CM_polynomial_ascending"]),"beta");beta=M.gen()
    def elt(row):return M([QQ(c) for c in row])
    def basis(a):return [list(map(str,z.list())) for z in a.basis()]
    G=M.fractional_ideal([elt(row) for row in old["CM_orbit"]["class_generator_ideal_basis"]])
    assert G==M.ideal(31,beta+16) and G.norm()==31
    powers=[G**k for k in range(17)]
    witnesses=[]
    for row in cm["entries"]:
        a=M.fractional_ideal([elt(v) for v in row["ideal_basis_power_coordinates"]]);c=row["relative_ideal_class"]
        quotient=a/powers[c];generators=quotient.gens_reduced();assert len(generators)==1
        z=generators[0];assert a==z*powers[c]
        witnesses.append({"index":row["index"],"class":c,"principal_generator":list(map(str,z.list()))})
    sigma=M.hom([beta**3+3*beta],M)
    current=beta;orbit=[]
    for i in range(16):orbit.append(current);current=sigma(current)
    assert current==beta and len(set(orbit))==16 and orbit[8]==-beta
    classes=M.class_group(proof=True);base=int(classes(G).list()[0]);assert classes.order()==17 and base%17
    Gs=M.fractional_ideal([sigma(z) for z in G.basis()]);alpha=int(classes(Gs).list()[0])*pow(base,-1,17)%17
    assert len({pow(alpha,i,17) for i in range(16)})==16
    gen=(Gs/powers[alpha]).gens_reduced();assert len(gen)==1 and Gs==gen[0]*powers[alpha]
    # g(X)=f_L(2X)/4 is integral and is 1-X modulo 2.
    L=[68,-2,-128,16,80,40,32,-80,-32,64,0,-16,16,8,0,0,-2,1]
    g=[ZZ(c*2**i)//4 for i,c in enumerate(L)];assert [v%2 for v in g]==[1,1]+[0]*16
    dg=[i*g[i] for i in range(1,len(g))]
    def evaluate(cs,a,mod):
        v=0
        for c in reversed(cs):v=(v*a+c)%mod
        return int(v)
    u=1;bits=1
    while bits<128:
        bits=min(2*bits,128);mod=1<<bits
        u=(u-evaluate(g,u,mod)*pow(evaluate(dg,u,mod),-1,mod))%mod
    assert evaluate(g,u,1<<128)==0
    result={"status":"pass","milestone":"D112","class_generator_two_generators":["31","beta+16"],
      "generator_power_bases":[basis(a) for a in powers],"principal_class_witnesses":witnesses,
      "sigma_beta":["0","3","0","1"]+["0"]*12,"sigma_order":16,
      "sigma_class_multiplier":alpha,"sigma_generator_ideal_principal_witness":list(map(str,gen[0].list())),
      "root_polynomial":L,"rational_dyadic_root":{"theta_center":str(2*u),"theta_congruence_2_exponent":129,
        "scaled_polynomial":[int(v) for v in g],"unit_center":str(u),"unit_congruence_2_exponent":128,
        "Newton_slopes":[[-1,1],[-1,16]],"root_valuations_v2":[[1,1]]+[[1,16]]*16,
        "unique_root_in_K":True},
      "sources":[source(p) for p in [Path(__file__),DATA/"cm_orbit.json",DATA/"dyadic_cm_embeddings_d112.json"]]}
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(f"CLASSES|17 principal witnesses; sigma(beta)=beta^3+3*beta; class multiplier {alpha}; unique Q2 root modulo 2^129",flush=True)
    print("PASS|408_dyadic_cm_class_witnesses",flush=True)

if __name__=="__main__":main()

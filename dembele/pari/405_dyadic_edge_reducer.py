"""D111 arithmetic edge reduction and evaluation of 16 invariant cocycles.

Public API: Reducer().reduce(U,V), with row-major 2x2 matrices over F,
each field entry a tuple of eight rational coefficients. Returns the
arithmetic transport, decreasing-distance trace and all 16 values.
Precision is refined from the same exact D109 Hensel root when needed.
Run the executable validation through bounded runner 272.
"""
from functools import lru_cache
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/"dembele/data/computed"
spec=importlib.util.spec_from_file_location("d110",ROOT/"dembele/pari/402_dyadic_group_transport_review.py")
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
r=a.r;Z,O=r.ZERO,r.ONE;PI=r.PI;E=r.E
source,checked=r.source,r.checked
power=lru_cache(None)(a.fpow)
LINES=[(1,0),(0,1),(1,1)]
NEIGHBORS=[(O,Z,Z,PI),(PI,Z,Z,O),(O,Z,O,PI)]

def residue(M):
    assert r.mval(M)>=0
    return [int(r.val(c)==0) for c in M]

def line(M):
    aa,b,c,d=residue(M);nz=[v for v in [(aa,c),(b,d)] if v!=(0,0)]
    assert nz and all(v==nz[0] for v in nz),"Expected a rank-one primitive matrix"
    return LINES.index(nz[0])

def truncate(x,precision):
    """Integral F element modulo pi^precision, using its power basis."""
    assert r.val(x)>=0
    out=[]
    for i,c in enumerate(x):
        bits=max(0,(precision-i+7)//8);mod=1<<bits
        assert c.denominator%2==1
        out.append(r.Q((c.numerator*pow(c.denominator,-1,mod))%mod) if bits else r.Q(0))
    y=tuple(out);assert r.val(r.sub(x,y))>=precision
    return y

class Splitting:
    def __init__(self,initial_precision=None):
        p=json.loads((DATA/"definite_dyadic_certificate_d109.json").read_text())
        self.I,self.Jc,self.Jt=[r.fm(p[k]) for k in ["I_exact","J_constant","J_slope"]]
        self.IJc=r.mmul(self.I,self.Jc);self.IJt=r.mmul(self.I,self.Jt)
        self.original=r.f(p["Hensel"]["x0"]);self.y=r.f(p["Hensel"]["y"])
        self.y2plus1=r.add(r.mul(self.y,self.y),O)
        self.x=self.original if initial_precision is None else truncate(self.original,initial_precision)
        self.refinements=0;self.root_errors=[];self.validate_root()

    def validate_root(self):
        n=r.val(r.add(r.mul(self.x,self.x),self.y2plus1));s=r.val(r.scale(self.x,2))
        assert s==8 and n>2*s and r.val(r.sub(self.x,self.original))>8
        self.error=n-s;self.root_errors.append(self.error)

    def refine(self):
        old_error=self.error
        residual=r.add(r.mul(self.x,self.x),self.y2plus1)
        new=r.sub(self.x,r.mul(residual,r.inv(r.scale(self.x,2))))
        self.x=truncate(new,2*old_error-8);self.refinements+=1;self.validate_root()
        assert self.error>old_error

    def image(self,q):
        const=r.madd(r.madd(r.mscale(E,q[0]),r.mscale(self.I,q[1])),
                     r.madd(r.mscale(self.Jc,q[2]),r.mscale(self.IJc,q[3])))
        slope=r.madd(r.mscale(self.Jt,q[2]),r.mscale(self.IJt,q[3]))
        return r.madd(const,r.mscale(slope,self.x)),slope

class Reducer:
    def __init__(self,initial_precision=None):
        self.raw=json.loads((DATA/"dyadic_quotient_export_d111.json").read_text())
        self.packet=json.loads((DATA/"dyadic_harmonic_certificate_d111.json").read_text())
        self.frames=[r.fm(row["local_frame"]) for row in self.packet["ideal_checks"]]
        self.inverse_frames=[r.minv(L) for L in self.frames]
        self.quaternions=[r.fm(row["quaternion"]) for row in self.raw["edges"]]
        self.split=Splitting(initial_precision);assert self.frames[0]==E

    def relative(self,j,q,U):
        """Exact distance and first direction from v_j to iota(q)[U]."""
        determinant=r.mul(r.mul(r.qnorm(q),r.mdet(U)),r.inv(r.mdet(self.frames[j])))
        assert determinant!=Z
        while True:
            C,S=self.split.image(q);C=r.mmul(r.mmul(self.inverse_frames[j],C),U)
            S=r.mmul(r.mmul(self.inverse_frames[j],S),U)
            minimum=r.mval(C);error=self.split.error+r.mval(S)
            if error>minimum:break
            self.split.refine()
        distance=r.val(determinant)-2*minimum;assert distance>=0
        direction=None if distance==0 else line(r.mscale(C,power(PI,-minimum)))
        return distance,direction,error-minimum

    def reduce(self,U,V,max_steps=10000):
        assert r.mdet(U)!=Z and r.mdet(V)!=Z
        A=r.mmul(r.minv(U),V)
        assert r.val(r.mdet(A))-2*r.mval(A)==1,"Input vertices must be adjacent"
        j=0;q=(O,Z,Z,Z);trace=[];word=[];bounds=[]
        initial=self.relative(j,q,U)[0]
        if initial>max_steps:raise ValueError("Initial tree distance exceeds caller's step cap")
        while True:
            distance,direction,bound=self.relative(j,q,U)
            assert distance==initial-len(word),"Distance must decrease by one at each transport"
            trace.append(distance);bounds.append(bound)
            if distance==0:break
            e=self.packet["stars"][j][direction];word.append(e)
            q=r.qmul(self.quaternions[e],q);j=self.raw["edges"][e]["target_class"]
        distance,direction,bound=self.relative(j,q,V);assert distance==1;bounds.append(bound)
        e=self.packet["stars"][j][direction]
        return {"source_class":j,"edge_index":e,"values":[b[e] for b in self.packet["harmonic_basis"]],
                "transport_quaternion":a.qs(q),"transport_word":word,"distance_trace":trace,
                "minimum_residue_error_margin":min(bounds)}

def transformed_lattice(split,q,U):
    """Return an F-matrix spanning precisely iota(q)U, with certified error."""
    while True:
        C,S=split.image(q);V=r.mmul(C,U)
        if r.mdet(V)!=Z:
            error=split.error+r.mval(r.mmul(r.minv(V),r.mmul(S,U)))
            if error>=1:return V,error
        split.refine()

def validations():
    reducer=Reducer();samples=[];nonzero=0
    # Representative finite/infinite boundary sectors and increasingly deep balls.
    vertices=[]
    for n in [0,7,14,28,32]:
        rr=Z
        for k in range(n):
            if (k*k+3*k+1)%5<2:rr=r.add(rr,power(PI,k))
        vertices.append((n,(O,Z,rr,power(PI,n))))
    vertices.append((14,(Z,power(PI,14),O,power(PI,3))))
    for n,U in vertices:
        values=[];evaluations=[]
        for N in NEIGHBORS:
            V=r.mmul(U,N);ev=reducer.reduce(U,V);rev=reducer.reduce(V,U)
            assert ev["values"]==[-v for v in rev["values"]]
            values.append(ev["values"]);evaluations.append(ev)
            nonzero+=int(any(ev["values"]))
        assert all(sum(v[k] for v in values)==0 for k in range(16))
        samples.append({"nominal_depth":n,"source_lattice":[a.fs(c) for c in U],"evaluations":evaluations,
                        "harmonicity_and_reversal_verified":True})
    assert nonzero>0
    low=Reducer(initial_precision=24);U=vertices[4][1];V=r.mmul(U,NEIGHBORS[2])
    adaptive=low.reduce(U,V);full=reducer.reduce(U,V)
    assert adaptive["values"]==full["values"] and adaptive["edge_index"]==full["edge_index"]
    assert low.split.refinements>0
    d110=json.loads((DATA/"dyadic_group_transport_d110.json").read_text())
    oldreview=json.loads((DATA/"dyadic_group_transport_review_d110.json").read_text())
    u=r.fm(json.loads((DATA/"definite_dyadic_certificate_d109.json").read_text())["transport"]["quaternion"])
    W=r.fm(d110["transports"]["W"]["quaternion"])
    h=r.fm(oldreview["certificates"]["derived_hyperbolic_element"]["quaternion"])
    invariance=[];U=vertices[1][1];V=r.mmul(U,NEIGHBORS[2]);base=reducer.reduce(U,V)
    for name,q in [("u",u),("W",W),("h",h)]:
        Uq,eu=transformed_lattice(reducer.split,q,U);Vq,ev=transformed_lattice(reducer.split,q,V)
        answer=reducer.reduce(Uq,Vq);assert answer["values"]==base["values"]
        invariance.append({"element":name,"lattice_error_bounds":[eu,ev],"values":answer["values"],
                           "reduction_steps":len(answer["transport_word"])})
    # Negative control: a non-edge is refused before reduction.
    try:reducer.reduce(E,(O,Z,Z,power(PI,2)))
    except AssertionError:bad_edge_rejected=True
    else:raise AssertionError("Nonadjacent input was accepted")
    return {"status":"pass","milestone":"D111","samples":samples,"nonzero_sample_edges":nonzero,
      "adaptive_precision":{"initial_precision":24,"root_error_sequence":low.split.root_errors,
        "refinements":low.split.refinements,"matches_full_precision":True,"evaluation":adaptive},
      "arithmetic_invariance_samples":invariance,"nonadjacent_input_rejected":bad_edge_rejected,
      "measure_denominator_bound":0,"actual_moments_or_Shimura_jet_computed":False,
      "sources":[source(p) for p in [Path(__file__),Path(a.__file__),DATA/"dyadic_quotient_export_d111.json",
        DATA/"dyadic_harmonic_certificate_d111.json",DATA/"definite_dyadic_certificate_d109.json",
        DATA/"dyadic_group_transport_d110.json",DATA/"dyadic_group_transport_review_d110.json"]]}

def main():
    out=DATA/"dyadic_edge_reducer_d111.json";assert not out.exists()
    result=validations();out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"sample_stars":len(result["samples"]),"nonzero_edges":result["nonzero_sample_edges"],
       "root_errors":result["adaptive_precision"]["root_error_sequence"],"group_invariance":[v["element"] for v in result["arithmetic_invariance_samples"]]}),flush=True)
    print("PASS|405_dyadic_edge_reducer",flush=True)

if __name__=="__main__":main()

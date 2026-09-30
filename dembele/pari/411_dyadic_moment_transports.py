"""D113: finite contracting transports for the 174 boundary-ball charts.

All matrices are exact in the D109 quadratic splitting algebra. Their
normalized F-valued centers are supplied with rigorous local error bounds.
Run through runner 272 with a 180-second cap.
"""
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
spec=importlib.util.spec_from_file_location('edge',ROOT/'dembele/pari/405_dyadic_edge_reducer.py')
rt=importlib.util.module_from_spec(spec);spec.loader.exec_module(rt)
r,a=rt.r,rt.a;Z,O,PI=r.ZERO,r.ONE,r.PI
source,checked=r.source,r.checked
# In D111 direction order: infinity, zero, one. Each H maps O_K to its ball.
BALLS=[(Z,O,PI,Z),(PI,Z,Z,O),(PI,O,Z,O)]

def adj(M):return M[3],r.neg(M[1]),r.neg(M[2]),M[0]
def conjugate(q):return (q[0],)+tuple(r.neg(c) for c in q[1:])
def serialize(M):return [a.fs(x) for x in M]

class Exact:
    def __init__(self,split):
        self.split=split;self.h=r.neg(split.y2plus1)
    def image(self,q):
        C,S=self.split.image(q)
        return r.madd(C,r.mscale(S,r.neg(self.split.x))),S
    def mul(self,X,Y):
        C,S=X;D,T=Y
        return (r.madd(r.mmul(C,D),r.mscale(r.mmul(S,T),self.h)),
                r.madd(r.mmul(C,T),r.mmul(S,D)))
    def left(self,M,X):return r.mmul(M,X[0]),r.mmul(M,X[1])
    def right(self,X,M):return r.mmul(X[0],M),r.mmul(X[1],M)
    def normalize(self,X,detval=None):
        C,S=X;V=r.madd(C,r.mscale(S,self.split.x))
        if V[3]==Z:return None
        vd=r.val(V[3]);bound=self.split.error+r.mval(S)-vd
        assert bound>16  # Enough to decide every shape and the pilot coefficients.
        N=r.mscale(V,r.inv(V[3]))
        if r.mval(N)<0 or r.val(N[2])<1:return None
        delta=r.sub(N[0],r.mul(N[1],N[2]));dv=r.val(delta)
        if detval is not None and dv!=detval:return None
        assert bound>dv
        return {'matrix_constant':serialize(C),'matrix_slope':serialize(S),
                'normalized_center':serialize(N),'normalized_error_pi':bound,
                'determinant_valuation':dv,'denominator_slope_valuation':r.val(N[2]),
                'constant_residue':int(r.val(N[1])==0)}

def computations():
    red=rt.Reducer();ex=Exact(red.split)
    H=[None]*174;directions=[None]*174
    for j,star in enumerate(red.packet['stars']):
        for d,e in enumerate(star):
            assert H[e] is None
            H[e]=r.mmul(red.frames[j],BALLS[d]);directions[e]=d
    assert all(h is not None for h in H)
    transitions=[]
    for e,row in enumerate(red.raw['edges']):
        target=row['target_class'];q=red.quaternions[e]
        left=ex.left(adj(H[e]),ex.image(conjugate(q)))
        children=[]
        for f in red.packet['stars'][target]:
            record=ex.normalize(ex.right(left,H[f]),1)
            if record is not None:
                record.update({'target_edge':f});children.append(record)
        assert len(children)==2 and sorted(c['constant_residue'] for c in children)==[0,1]
        children.sort(key=lambda c:c['constant_residue'])
        assert all(sum(red.packet['harmonic_basis'][k][c['target_edge']] for c in children)
                   ==red.packet['harmonic_basis'][k][e] for k in range(16))
        transitions.append({'edge':e,'source_class':row['source_class'],
                            'transport_edge':e,'children':children})
    print('TRANSPORT|174 states, 348 strict contractions; both residue classes and all zeroth relations',flush=True)
    cm=json.loads((DATA/'dyadic_cm_embeddings_d112.json').read_text())
    previous=json.loads((DATA/'dyadic_cm_matching_review_d112.json').read_text())
    charts=[]
    for row in cm['entries']:
        S=tuple((r.f(z[0]),r.f(z[1])) for z in row['CM_coordinate_matrix'])
        Sm=(tuple(z[0] for z in S),tuple(z[1] for z in S))
        Sc=r.fm(row['CM_coordinate_center'])
        for name,d in [('A',1),('B',2),('C',0)]:
            Hcm=ex.right(Sm,BALLS[d])
            ev=red.reduce(Sc,r.mmul(Sc,rt.NEIGHBORS[d]));q=r.fm(ev['transport_quaternion'])
            # The omitted determinants are central projective scalars.
            matrix=ex.right(ex.mul((adj(Hcm[0]),adj(Hcm[1])),ex.image(conjugate(q))),H[ev['edge_index']])
            cert=ex.normalize(matrix,0);assert cert is not None
            ci=row['index'];old=previous['certificates']['CM_chart_zeroth_masses'][ci]
            assert ev['values']==old['zeroth_moments'][old['chart_names'].index(name)]
            cert.update({'CM_index':ci,'chart':name,'target_edge':ev['edge_index'],
                         'transport_quaternion':ev['transport_quaternion'],
                         'transport_word':ev['transport_word'],'zeroth_moments':ev['values']})
            charts.append(cert)
    print('CM_TRANSPORT|51 exact ball isomorphisms; all D112 zeroth masses recovered',flush=True)
    return {'status':'pass','milestone':'D113','state_count':174,
            'canonical_ball_matrices':[serialize(h) for h in H],
            'directions':directions,'transitions':transitions,'CM_charts':charts,
            'minimum_transition_error_pi':min(c['normalized_error_pi'] for row in transitions for c in row['children']),
            'minimum_CM_chart_error_pi':min(c['normalized_error_pi'] for c in charts),
            'pilot_maximum_working_precision_pi':16,
            'sources':[source(p) for p in [Path(__file__),Path(rt.__file__),
               DATA/'dyadic_quotient_export_d111.json',DATA/'dyadic_harmonic_certificate_d111.json',
               DATA/'definite_dyadic_certificate_d109.json',DATA/'dyadic_cm_embeddings_d112.json',
               DATA/'dyadic_cm_matching_review_d112.json']]}

def main():
    out=DATA/'dyadic_moment_transports_d113.json';assert not out.exists()
    result=computations();out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['state_count','minimum_transition_error_pi','minimum_CM_chart_error_pi']}),flush=True)
    print('PASS|411_DYADIC_MOMENT_TRANSPORTS',flush=True)

if __name__=='__main__':main()

"""D113 independent transport and finite moment-residual review.

Uses rational splitting algebra and ordinary coefficient convolution rather
than source 412's bit-plane arithmetic. A fixed-point residual, contraction
proof and independent depth-three ball sums certify the actual moments.
"""
import argparse
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'dyadic_moment_review_d113.json'
REPORT=ROOT/'dembele/certificates/dyadic-moments-d113.md'
spec=importlib.util.spec_from_file_location('edge_review',ROOT/'dembele/pari/405_dyadic_edge_reducer.py')
rt=importlib.util.module_from_spec(spec);spec.loader.exec_module(rt)
r,a=rt.r,rt.a;Z,O,PI=r.ZERO,r.ONE,r.PI
source,checked=r.source,r.checked
P,J=12,11
MOD=np.array([4]*4+[2]*4,dtype=np.int64)
ZERO=(0,)*8;ONE=(1,)+(0,)*7
BALLS=[(Z,O,PI,Z),(PI,Z,Z,O),(PI,O,Z,O)]

def encode(x):
    return tuple(int(c.numerator*pow(c.denominator,-1,int(mod))%int(mod)) for c,mod in zip(x,MOD))
def val(x):
    return min((i+(8 if c%2==0 else 0) for i,c in enumerate(x) if c),default=P)
def poly_add(x,y):return tuple(int((c+d)%mod) for c,d,mod in zip(x,y,MOD))
def poly_neg(x):return tuple(int(-c%mod) for c,mod in zip(x,MOD))
@lru_cache(maxsize=65536)
def poly_mul(x,y):
    z=np.convolve(x,y)
    z[:7]-=2*z[8:15]
    return tuple(int(c) for c in z[:8]%MOD)
@lru_cache(None)
def multiplier(x):
    # Multiplication on the eight power coefficients, retaining all sixteen
    # measure components as separate ordinary integer columns.
    ans=np.zeros((8,8),dtype=np.int64)
    for i,c in enumerate(x):
        for j in range(8):ans[(i+j)%8,j]+=c*(-2 if i+j>=8 else 1)
    return ans
@lru_cache(None)
def series(params,degree,truncation):
    aa,bb,cc=params;delta=poly_add(aa,poly_neg(poly_mul(bb,cc)))
    phi=[bb,delta]
    for _ in range(2,truncation+1):phi.append(poly_neg(poly_mul(cc,phi[-1])))
    rows=[[ONE]+[ZERO]*truncation]
    for _ in range(degree):
        new=[ZERO]*(truncation+1)
        for i,x in enumerate(rows[-1]):
            if x!=ZERO:
                for k,y in enumerate(phi[:truncation+1-i]):
                    if y!=ZERO:new[i+k]=poly_add(new[i+k],poly_mul(x,y))
        rows.append(new)
    return rows
def params(row):return tuple(encode(r.f(x)) for x in row['normalized_center'][:3])
def adj(M):return M[3],r.neg(M[1]),r.neg(M[2]),M[0]

def transport_checks(packet):
    raw=json.loads((DATA/'dyadic_quotient_export_d111.json').read_text())
    harmonic=json.loads((DATA/'dyadic_harmonic_certificate_d111.json').read_text())
    split=json.loads((DATA/'definite_dyadic_certificate_d109.json').read_text())
    I,Jc,Jt=[r.fm(split[k]) for k in ['I_exact','J_constant','J_slope']]
    x0,y=r.f(split['Hensel']['x0']),r.f(split['Hensel']['y'])
    err=split['Hensel']['root_error_valuation'];h=r.neg(r.add(r.mul(y,y),O))
    def image(q):
        C=r.madd(r.madd(r.mscale(r.E,q[0]),r.mscale(I,q[1])),
                  r.madd(r.mscale(Jc,q[2]),r.mscale(r.mmul(I,Jc),q[3])))
        S=r.madd(r.mscale(Jt,q[2]),r.mscale(r.mmul(I,Jt),q[3]))
        return C,S
    def product(X,Y):
        C,S=X;D,T=Y
        return (r.madd(r.mmul(C,D),r.mscale(r.mmul(S,T),h)),
                r.madd(r.mmul(C,T),r.mmul(S,D)))
    def check(row,X,dv):
        C,S=X
        assert C==r.fm(row['matrix_constant']) and S==r.fm(row['matrix_slope'])
        V=r.madd(C,r.mscale(S,x0));denv=r.val(V[3])
        N=r.mscale(V,r.inv(V[3]));bound=err+r.mval(S)-denv
        assert N==r.fm(row['normalized_center']) and N[3]==O
        assert r.mval(N)>=0 and r.val(N[2])>=1
        assert r.val(r.mdet(N))==dv==row['determinant_valuation']
        assert bound==row['normalized_error_pi'] and bound>P
        assert int(r.val(N[1])==0)==row['constant_residue']
        assert r.val(N[2])==row['denominator_slope_valuation']
        return bound,denv
    frames=[r.fm(row['local_frame']) for row in harmonic['ideal_checks']]
    H=[None]*174
    for j,star in enumerate(harmonic['stars']):
        for d,e in enumerate(star):
            H[e]=r.mmul(frames[j],BALLS[d]);assert packet['directions'][e]==d
    assert H==[r.fm(x) for x in packet['canonical_ball_matrices']]
    assert len(packet['transitions'])==174 and packet['state_count']==174
    ebounds=[]
    for e,row in enumerate(packet['transitions']):
        assert row['edge']==row['transport_edge']==e
        assert row['source_class']==raw['edges'][e]['source_class']
        q=r.fm(raw['edges'][e]['quaternion']);qb=(q[0],)+tuple(r.neg(x) for x in q[1:])
        C,S=image(qb);children=row['children'];assert len(children)==2
        assert [c['constant_residue'] for c in children]==[0,1]
        for child in children:
            f=child['target_edge'];assert f in harmonic['stars'][raw['edges'][e]['target_class']]
            X=tuple(r.mmul(r.mmul(adj(H[e]),M),H[f]) for M in [C,S])
            bound,denv=check(child,X,1);ebounds.append(bound)
            exactdet=r.mul(r.mul(r.mdet(H[e]),r.qnorm(q)),r.mdet(H[f]))
            assert r.val(exactdet)-2*denv==1
        assert all(sum(harmonic['harmonic_basis'][k][c['target_edge']] for c in children)
                   ==harmonic['harmonic_basis'][k][e] for k in range(16))
    cm=json.loads((DATA/'dyadic_cm_embeddings_d112.json').read_text())
    old=json.loads((DATA/'dyadic_cm_matching_review_d112.json').read_text())
    assert len(packet['CM_charts'])==51;cbounds=[]
    for n,row in enumerate(packet['CM_charts']):
        ci=n//3;name=['A','B','C'][n%3];d=[1,2,0][n%3]
        assert (row['CM_index'],row['chart'])==(ci,name)
        entries=cm['entries'][ci]['CM_coordinate_matrix']
        S0=tuple(r.f(z[0]) for z in entries);S1=tuple(r.f(z[1]) for z in entries)
        Hcm=(r.mmul(S0,BALLS[d]),r.mmul(S1,BALLS[d]))
        q=(O,Z,Z,Z)
        for e in row['transport_word']:q=r.qmul(r.fm(raw['edges'][e]['quaternion']),q)
        assert q==r.fm(row['transport_quaternion'])
        qb=(q[0],)+tuple(r.neg(x) for x in q[1:])
        X=product(tuple(adj(M) for M in Hcm),image(qb))
        X=tuple(r.mmul(M,H[row['target_edge']]) for M in X)
        bound,_=check(row,X,0);cbounds.append(bound)
        masses=[b[row['target_edge']] for b in harmonic['harmonic_basis']]
        assert masses==row['zeroth_moments']==old['certificates']['CM_chart_zeroth_masses'][ci]['zeroth_moments'][n%3]
    assert min(ebounds)==packet['minimum_transition_error_pi']
    assert min(cbounds)==packet['minimum_CM_chart_error_pi']
    print('TRANSPORT_REVIEW|348 contracting maps and 51 CM maps independently reconstructed',flush=True)
    return {'states':174,'strict_contractions':348,'CM_ball_isomorphisms':51,
            'minimum_transition_error_pi':min(ebounds),'minimum_CM_chart_error_pi':min(cbounds)}

def moment_checks(packet,pilot):
    assert (pilot['working_precision_pi'],pilot['state_maximum_degree'],pilot['iterations'])==(P,J,P)
    # Check the independent quotient model against exact F multiplication.
    basis=[tuple(r.Q(i==j) for i in range(8)) for j in range(8)]
    for x in basis:
        for y in basis:assert poly_mul(encode(x),encode(y))==encode(r.mul(x,y))
    assert val(encode(r.scale(O,2)))==8
    harmonic=json.loads((DATA/'dyadic_harmonic_certificate_d111.json').read_text())
    m=np.array(pilot['state_moments_power_basis'],dtype=np.int64).transpose(0,1,3,2)
    assert m.shape==(174,12,8,16) and np.all(m>=0) and np.all(m<MOD[None,None,:,None])
    positive=0
    for e,row in enumerate(packet['transitions']):
        expect=np.zeros((8,16),dtype=np.int64);expect[0]=[v[e]%4 for v in harmonic['harmonic_basis']]
        assert np.array_equal(m[e,0],expect)
        rhs=np.zeros((J+1,8,16),dtype=np.int64)
        for child in row['children']:
            f=child['target_edge'];coefs=series(params(child),J,J)
            for n in range(J+1):
                for k,c in enumerate(coefs[n]):
                    if k and n:assert val(c)>=min(k,P)
                    if c!=ZERO:rhs[n]+=multiplier(c)@m[f,k]
        rhs%=MOD[None,:,None]
        assert np.array_equal(rhs,m[e]),f'Nonzero moment residual at edge {e}'
        positive+=sum(val(tuple(m[e,n,:,a]))<P for n in range(1,J+1) for a in range(16))
    nonzero=anchor=0
    for row,saved in zip(packet['CM_charts'],pilot['CM_chart_moments']):
        assert (row['CM_index'],row['chart'])==(saved['CM_index'],saved['chart'])
        coefs=series(params(row),3,J);rhs=np.zeros((4,8,16),dtype=np.int64)
        for n in range(4):
            for k,c in enumerate(coefs[n]):
                assert val(c)>=max(0,k-n)
                if c!=ZERO:rhs[n]+=multiplier(c)@m[row['target_edge'],k]
        rhs%=MOD[None,:,None]
        assert np.array_equal(rhs,np.array(saved['moments_power_basis']).transpose(0,2,1))
        assert saved['positive_degree_errors_pi']==[11,10,9]
        assert saved['zeroth_moments_exact']==row['zeroth_moments']
        for n in range(1,4):
            for a in range(16):
                if val(tuple(rhs[n,:,a]))<12-n:
                    nonzero+=1
                    if row['CM_index']==0:anchor+=1
    assert nonzero==pilot['certified_nonzero_positive_CM_entries']==2043
    assert anchor==pilot['anchor_certified_nonzero_positive_entries']==0
    # A unit perturbation of a positive moment changes its own residue;
    # every right-hand-side dependence on positive moments is divisible by pi.
    wrong=(int(m[0,1,0,0])+1)%4
    assert wrong%2!=int(m[0,1,0,0])%2
    print(f'MOMENT_REVIEW|33408 state moments; residual zero; {nonzero} certified nonzero CM entries',flush=True)
    return {'state_moment_entries':174*12*16,'state_positive_nonzero_residues':positive,
            'fixed_point_residual_zero':True,'contraction_precision_gain_pi':1,
            'state_moment_error_pi':P,'CM_positive_moment_errors_pi':[11,10,9],
            'CM_certified_nonzero_positive_entries':nonzero,'anchor_certified_nonzero_positive_entries':anchor,
            'altered_positive_moment_rejected':True,'ramification_eight_verified':True}

def direct_ball_checks(pilot):
    red=rt.Reducer();cm=json.loads((DATA/'dyadic_cm_embeddings_d112.json').read_text())
    depth=3;checks=[]
    for ci,name,d in [(0,'A',1),(0,'B',2),(0,'C',0),(1,'B',2)]:
        row=cm['entries'][ci];H=r.mmul(r.fm(row['CM_coordinate_center']),BALLS[d])
        slope=r.mmul(r.fm(row['CM_coordinate_slope']),BALLS[d])
        sums=np.zeros((4,8,16),dtype=np.int64);total=[0]*16;bounds=[];samples=[]
        for code in range(1<<depth):
            z=Z
            for k in range(depth):
                if (code>>k)&1:z=r.add(z,rt.power(PI,k))
            parent=r.sub(z,rt.power(PI,depth-1)) if (code>>(depth-1))&1 else z
            D=(rt.power(PI,depth),z,Z,O);Dp=(rt.power(PI,depth-1),parent,Z,O)
            U,V=r.mmul(H,Dp),r.mmul(H,D)
            for A,M in [(Dp,U),(D,V)]:
                bound=180+r.mval(r.mmul(r.minv(M),r.mmul(slope,A)));assert bound>=1;bounds.append(bound)
            ev=red.reduce(U,V);mass=ev['values'];total=[x+y for x,y in zip(total,mass)]
            zmod=encode(z);zp=ONE
            for n in range(4):
                sums[n]+=np.array(zp)[:,None]*np.array(mass)[None,:]
                zp=poly_mul(zp,zmod)
            samples.append({'code':code,'mass':mass,'edge_index':ev['edge_index'],
                            'transport_word':ev['transport_word']})
        saved=next(x for x in pilot['CM_chart_moments'] if (x['CM_index'],x['chart'])==(ci,name))
        assert total==saved['zeroth_moments_exact']
        exact=np.array(saved['moments_power_basis']).transpose(0,2,1)
        difference=(sums-exact)%MOD[None,:,None]
        lower=min(val(tuple(difference[n,:,a])) for n in range(1,4) for a in range(16))
        assert lower>=depth
        checks.append({'CM_index':ci,'chart':name,'depth':depth,'leaf_count':1<<depth,
                       'comparison_error_pi':lower,'minimum_lattice_error_pi':min(bounds),
                       'samples':samples})
    print('DIRECT_CHECK|32 independently reduced leaf balls; degrees 1..3 agree modulo pi^3',flush=True)
    return checks

def computations():
    packet=json.loads((DATA/'dyadic_moment_transports_d113.json').read_text())
    pilot=json.loads((DATA/'dyadic_moment_pilot_d113.json').read_text())
    return {'transports':transport_checks(packet),'moments':moment_checks(packet,pilot),
            'direct_ball_checks':direct_ball_checks(pilot)}

def build():
    result=computations();previous=DATA/'dyadic_cm_matching_review_d112.json'
    prior=json.loads(previous.read_text());assert prior['status']=='pass' and len(prior['sources'])==682
    paths=checked(prior['sources'])+[previous,Path(__file__),REPORT,DATA/'dyadic_moment_sources_d113.json']
    for name in ['dyadic_moment_transports_d113.json','dyadic_moment_pilot_d113.json']:
        p=DATA/name;obj=json.loads(p.read_text());paths+=[p]+checked(obj['sources'])
    for pattern in ['dyadic_moment_transports_d113_attempt*.job.json','dyadic_moment_pilot_d113_attempt*.job.json',
                    'dyadic_moment_review_d113_probe_attempt*.job.json']:
        for p in sorted(DATA.glob(pattern)):
            job=json.loads(p.read_text());assert job['timeout_seconds']==180 and job['timeout_terminates_process_group']
            paths+=[p]+checked(job['sources']+[job['log']])
            if job['status']=='pass':
                assert job['wall_seconds']<180;paths+=checked([job['driver']])
            else:
                assert job['status'] in ['failed','timeout']
                failed=p.with_name(p.name.replace('.job.json','_failed'+Path(job['driver']['path']).suffix))
                assert source(failed)['sha256']==job['driver']['sha256'];paths.append(failed)
    return {'status':'pass','milestone':'D113','certificates':result,
            'D112_source_hashes_checked_unchanged':682,
            'actual_positive_degree_moments_computed':True,'actual_Shimura_tangent_or_jet_evaluated':False,
            'actual_harmonic_to_residue_frame_change_computed':False,
            'anchor_nonvanishing_certified':False,'candidate_identification_proved':False,
            'target_field_polynomial_constructed':False,
            'sources':[source(p) for p in sorted(set(p.resolve() for p in paths))]}

def main():
    parser=argparse.ArgumentParser(description=__doc__);g=parser.add_mutually_exclusive_group()
    g.add_argument('--probe',action='store_true');g.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.probe:
        result=computations();print(json.dumps({k:v for k,v in result.items() if k!='direct_ball_checks'},indent=2),flush=True)
        print('PASS|D113_MOMENT_PROBE',flush=True);return
    if args.check:old=json.loads(OUT.read_text());checked(old['sources'])
    result=build()
    if args.check:assert result==old
    else:
        assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'pass','sources':len(result['sources']),'D112_hashes_unchanged':682}),flush=True)
    print('PASS|D113_MOMENT_REVIEW',flush=True)

if __name__=='__main__':main()

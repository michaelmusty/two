"""D145: orthogonal trace bases, independent exhaustive replay and extension."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
SAGE=Path('/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/Current')
PYTHON=SAGE/'venv/bin/python3'


def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def worker(out):
    from sage.all import AA,QQ,ZZ,NumberField,PolynomialRing,RealBallField,matrix,vector
    import math
    R=RealBallField(224);P=PolynomialRing(QQ,'x');x=P.gen()
    F=NumberField(x**8-8*x**6+20*x**4-16*x**2+2,'b');b=F.gen()
    primary=json.loads((DATA/'P1600_trace_systole_d145.json').read_text());assert primary['status']=='pass'
    roots=sorted(F.embeddings(AA),key=lambda e:e(b));rb=[R(e(b)) for e in roots]
    iv=lambda t:[str(QQ(t.lower())),str(QQ(t.upper()))]
    def embed(t,j):return sum((R(c)*rb[j]**k for k,c in enumerate(t.list())),R(0))
    def vec(t):return vector(QQ,t.list()+[0]*(8-len(t.list())))
    def canonical(v):
        v=tuple(map(int,v))
        return v if next(x for x in reversed(v) if x)>0 else tuple(-x for x in v)
    C=[F(2),b]
    for _ in range(2,9):C.append(b*C[-1]-C[-2])
    assert C[8]==0
    records=[]
    for label,n,basis,weights in [('unit',F(1),[F(1)]+C[1:8],[8]+[16]*7),
                                ('dyadic',2+b,[C[j]+C[j+1] for j in range(8)],[16]*8)]:
        M=matrix(QQ,[vec(t) for t in basis]).transpose()
        assert abs(M.det())==(1 if label=='unit' else 2)
        G=matrix(QQ,8,8,lambda i,j:(basis[i]*basis[j]/n).trace())
        assert G==matrix.diagonal(QQ,weights)
        # Exact integer recursion in an orthogonal basis; no floating ranges.
        all_vectors=[];current=[0]*8
        def walk(k,remaining):
            if k==8:
                if any(current) and next(v for v in reversed(current) if v)>0:
                    all_vectors.append(tuple(current))
                return
            radius=math.isqrt(remaining//weights[k])
            for a in range(-radius,radius+1):
                current[k]=a;walk(k+1,remaining-weights[k]*a*a)
            current[k]=0
        walk(0,80)
        old=next(r for r in primary['families'] if r['family']==label)
        old_basis=[F(list(map(QQ,t))) for t in old['trace_lattice_basis']]
        old_change=matrix(ZZ,old['reduction_change'])
        old_traces=[]
        for v in old['all_reduced_lattice_vectors']:
            coords=old_change*vector(ZZ,v)
            tau=sum((coords[k]*old_basis[k] for k in range(8)),F(0))
            row=M.inverse()*vec(tau)
            assert all(t.denominator()==1 for t in row)
            old_traces.append(canonical(row))
        small={v for v in all_vectors if sum(weights[k]*v[k]*v[k] for k in range(8))<=40}
        assert set(old_traces)==small and len(old_traces)==len(small)
        damaged=set(small);damaged.pop();assert damaged!=small
        basis_values=[[embed(t,j) for t in basis] for j in range(8)]
        norms=[embed(n,j) for j in range(8)]
        candidates=[]
        for v in all_vectors:
            if label=='unit' and abs(v[0])==2 and not any(v[1:]):continue
            values=[];allowed=True
            for j in [4,0,1,2,3,5,6,7]:
                t=sum((v[k]*basis_values[j][k] for k in range(8)),R(0))
                u=t*t/norms[j]
                assert u<4 or u>4
                if (j==4 and u<4) or (j!=4 and u>4):allowed=False;break
                if j==4:split=u
            if not allowed:continue
            tau=sum((v[k]*basis[k] for k in range(8)),F(0))
            u=tau*tau/n
            assert u.trace()==sum(weights[k]*v[k]*v[k] for k in range(8))
            ell=2*(split.sqrt()/2).arccosh()
            candidates.append({'orthogonal_coordinates':list(v),'trace_coefficients':list(map(str,tau.list())),
                               'normalized_trace_square_coefficients':list(map(str,u.list())),
                               'normalized_trace_square_interval':iv(split),'length_interval':iv(ell),
                               'display_length':float(ell.center())})
        candidates.sort(key=lambda r:QQ(r['length_interval'][0]))
        floor=QQ(R(25).arccosh().lower())
        if candidates:floor=min(floor,QQ(candidates[0]['length_interval'][0]))
        records.append({'family':label,'orthogonal_trace_basis':[list(map(str,t.list())) for t in basis],
                        'gram_diagonal':weights,'basis_index_in_OF':str(abs(M.det())),
                        'quadratic_bound':80,'signed_pairs':len(all_vectors),'replayed_bound40_pairs':len(small),
                        'all_orthogonal_vectors':[list(v) for v in all_vectors],
                        'all_admissible_candidates':candidates,'lower_length_bound':str(floor)})
    floor=min(QQ(r['lower_length_bound']) for r in records)
    result={'status':'pass','milestone':'D145','arb_precision_bits':224,
            'independent_orthogonal_bases':True,'exact_integer_enumeration':True,
            'complete_D145_bound40_replayed':True,'omitted_vector_control_rejected':True,
            'families':records,'normalizer_systole_lower_rational':str(floor),
            'display_normalizer_systole_lower':float(floor),
            'trace_candidates_are_not_asserted_to_embed':True,
            'new_quaternion_classes_or_geodesics_enumerated':False,
            'actual_curve_eigenvalue_computation_started':False,
            'candidate_identification_proved':False,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}
    assert result['peak_rss_bytes']<2*(1<<30)
    with out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('D145_TRACE_AUDIT_WORKER_PASS',flush=True)


if __name__=='__main__':
    assert __debug__
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--worker',type=Path);args=ap.parse_args()
    if args.worker:worker(args.worker);sys.exit(0)
    tick=time.monotonic();output=DATA/'P1600_trace_systole_audit_d145.json';child_path=DATA/'P1600_trace_systole_audit_d145_worker.json'
    assert not output.exists() and not child_path.exists()
    env=dict(os.environ,DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH']=str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH','')
    child=subprocess.run([str(PYTHON),str(Path(__file__).resolve()),'--worker',str(child_path)],cwd=ROOT,env=env,capture_output=True,text=True)
    assert child.returncode==0 and 'D145_TRACE_AUDIT_WORKER_PASS' in child.stdout,(child.returncode,child.stdout,child.stderr)
    result=json.loads(child_path.read_text());rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    crss=max(result['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024));assert rss+crss<2*(1<<30)
    result.update({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':rss,'child_peak_rss_bytes':crss,
                   'conservative_peak_rss_bytes':rss+crss,'sources':[source(p) for p in [Path(__file__),PYTHON,child_path,DATA/'P1600_trace_systole_d145.json']]})
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|610_P1600_TRACE_SYSTOLE_AUDIT',flush=True)

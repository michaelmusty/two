"""D145: finite trace-lattice bound for the normalizer systole.

Enumerates necessary scalar trace candidates, not quaternion classes or
closed geodesics. Use the frozen capped wrapper.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'dembele/data/computed'
SAGE=Path('/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/Current')
PYTHON=SAGE/'venv/bin/python3'
HELPER=ROOT/'dembele/pari/340_nelson_norm_one_coverage.py'


def source(path):
    p=Path(path).resolve()
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def worker(out):
    from sage.all import AA,QQ,ZZ,NumberField,PolynomialRing,RealBallField,matrix,vector,lcm
    spec=importlib.util.spec_from_file_location('d92_exact_enumeration',HELPER)
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    P=PolynomialRing(QQ,'x');x=P.gen()
    F=NumberField(x**8-8*x**6+20*x**4-16*x**2+2,'b');b=F.gen()
    assert F.discriminant()==2**31 and F.polynomial().discriminant()==2**31
    R=RealBallField(192)
    roots=sorted(F.embeddings(AA),key=lambda e:e(b))
    rb=[R(e(b)) for e in roots]
    assert rb[4]>0 and rb[4]<1
    def embed(t,j):
        return sum((R(c)*rb[j]**k for k,c in enumerate(t.list())),R(0))
    iv=lambda t:[str(QQ(t.lower())),str(QQ(t.upper()))]
    C=[F(2),b]
    for k in range(2,8):C.append(b*C[-1]-C[-2])
    basis=[F(1)]+C[1:]
    assert abs(matrix(QQ,[t.list()+[0]*(8-len(t.list())) for t in basis]).det())==1
    families=[]
    for label,n,lattice in [('unit',F(1),basis),('dyadic',2+b,[b*c for c in basis])]:
        assert n.norm()==(1 if label=='unit' else 2)
        G=matrix(QQ,8,8,lambda i,j:(lattice[i]*lattice[j]/n).trace())
        if label=='unit':assert G==matrix.diagonal(QQ,[8]+[16]*7)
        den=lcm(c.denominator() for c in G.list())
        change=matrix(ZZ,(den*G).__pari__().qflllgram(1))
        assert abs(change.det())==1
        reduced=change.transpose()*G*change
        vectors,coverage=helper.enumerate_exact(reduced,QQ(40))
        candidates=[];positive=0
        for coords in sorted(vectors):
            original=change*vector(ZZ,coords)
            tau=sum((original[k]*lattice[k] for k in range(8)),F(0))
            u=tau*tau/n
            assert QQ(u.trace())==vector(QQ,coords)*reduced*vector(QQ,coords)<=40
            if u==4:continue
            values=[embed(u,j) for j in range(8)]
            assert all(v>4 or v<4 for v in values)
            if values[4]<4:continue
            positive+=1
            if any(values[j]>4 for j in range(8) if j!=4):continue
            assert all(values[j]>=0 for j in range(8))
            length=2*(values[4].sqrt()/2).arccosh()
            candidates.append({'reduced_lattice_vector':list(map(int,coords)),
                               'trace_coefficients':list(map(str,tau.list())),
                               'normalized_trace_square_coefficients':list(map(str,u.list())),
                               'normalized_trace_square_interval':iv(values[4]),
                               'length_interval':iv(length),'display_length':float(length.center())})
        candidates.sort(key=lambda r:QQ(r['length_interval'][0]))
        floor=R(5).arccosh()
        if candidates:
            floor=R(QQ(candidates[0]['length_interval'][0]))
        assert floor>0
        families.append({'family':label,'norm_coefficients':list(map(str,n.list())),
                         'trace_lattice_basis':[list(map(str,t.list())) for t in lattice],
                         'gram':[list(map(str,row)) for row in G.rows()],
                         'reduction_change':[list(map(int,row)) for row in change.rows()],
                         'trace_quadratic_cutoff':'40',
                         'enumerated_sign_pairs':len(vectors),'split_hyperbolic_sign_pairs':positive,
                         'coverage':coverage,'all_reduced_lattice_vectors':[list(map(int,v)) for v in sorted(vectors)],
                         'admissible_trace_candidates':candidates,'systole_lower_interval':iv(floor)})
    lower=min(QQ(r['systole_lower_interval'][0]) for r in families)
    result={'status':'pass','milestone':'D145','arb_precision_bits':192,
            'field_polynomial':str(F.polynomial()),'field_discriminant':str(F.discriminant()),
            'split_root_index_zero_based':4,'real_root_intervals':[iv(t) for t in rb],
            'families':families,'normalizer_systole_lower_rational':str(lower),
            'display_normalizer_systole_lower':float(lower),
            'coverage_is_exhaustive_for_necessary_trace_conditions':True,
            'trace_candidates_are_not_asserted_to_embed':True,
            'quaternion_class_enumeration_started':False,'geodesic_census_started':False,
            'actual_curve_eigenvalue_computation_started':False,
            'group_and_normalizer_claims_require_companion_proof':True,
            'spectral_target_proved':False,'candidate_identification_proved':False,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}
    assert result['peak_rss_bytes']<2*(1<<30)
    with out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('D145_TRACE_WORKER_PASS',flush=True)


if __name__=='__main__':
    assert __debug__
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--worker',type=Path)
    args=ap.parse_args()
    if args.worker:worker(args.worker);sys.exit(0)
    tick=time.monotonic();output=DATA/'P1600_trace_systole_d145.json';child_path=DATA/'P1600_trace_systole_d145_worker.json'
    assert not output.exists() and not child_path.exists()
    env=dict(os.environ,DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH']=str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH','')
    child=subprocess.run([str(PYTHON),str(Path(__file__).resolve()),'--worker',str(child_path)],cwd=ROOT,env=env,capture_output=True,text=True)
    assert child.returncode==0 and 'D145_TRACE_WORKER_PASS' in child.stdout,(child.returncode,child.stdout,child.stderr)
    result=json.loads(child_path.read_text());rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    crss=max(result['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024))
    assert rss+crss<2*(1<<30)
    result.update({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':rss,'child_peak_rss_bytes':crss,
                   'conservative_peak_rss_bytes':rss+crss,
                   'sources':[source(p) for p in [Path(__file__),PYTHON,HELPER,child_path,
                       ROOT/'dembele/certificates/nelson-norm-one-control-d92.md',
                       ROOT/'dembele/certificates/marked-descent.md',
                       ROOT/'dembele/certificates/P1600-joint-adjunction-RR-d144.md']]})
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|609_P1600_TRACE_SYSTOLE',flush=True)

"""D131 weighted-only P=3200 replay with generation-bound row authentication.

All inputs are frozen D129 data. The GMP original action checks Q T(w)=w
and every retained uniform coordinate; CM outputs use w directly. Nothing
is refined and no duplicate uniform or CM binary is written.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
spec = importlib.util.spec_from_file_location('previous', ROOT/'dembele/pari/528_dyadic_streamed_precision3200.py')
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)
b, l, p = w.b, w.l, w.p
P, N, BITS = 3200, 174, 400
PATHS = {Path(__file__), Path(w.__file__), Path(b.__file__), Path(l.__file__), Path(p.__file__), Path(p.g.__file__), Path(p.f.__file__)}
CACHE = {}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    if path not in CACHE:
        sha = hashlib.sha256()
        with path.open('rb') as f:
            while raw := f.read(1 << 20):
                sha.update(raw)
        CACHE[path] = {'path': str(path), 'sha256': sha.hexdigest()}
    return CACHE[path]


def read(stem):
    path = DATA/(stem+'.json')
    PATHS.add(path)
    packet = json.loads(path.read_text())
    assert packet['status'] == 'pass'
    return packet


def layout(count, bits, weighted=False):
    return [tuple(max(0, (count-k-i+7)//8) if weighted and k>32 else bits for i in range(8)) for k in range(count)]


def encode(values, bitcounts):
    assert len(values) == len(bitcounts)
    return b''.join((v % (1 << bits)).to_bytes((bits+7)//8,'little') for row,bs in zip(values,bitcounts) for v,bits in zip(row,bs))


class Reader:
    def __init__(self, record):
        self.record = record
        self.path = Path(record['payload']['path'])
        self.bits = layout(record['count'],record['bits'],record['weighted'])
        self.width = sum((n+7)//8 for bs in self.bits for n in bs)
        assert self.width == record['row_bytes']
        assert len(record['row_sha256']) == record['rows']
        assert self.path.stat().st_size == self.width*record['rows']
        self.file = self.path.open('rb')
        self.reads = 0

    def raw(self, e):
        assert 0<=e<self.record['rows']
        self.file.seek(e*self.width)
        raw = self.file.read(self.width)
        assert len(raw)==self.width and hashlib.sha256(raw).hexdigest()==self.record['row_sha256'][e]
        self.reads += 1
        return raw

    def row(self,e):
        raw=self.raw(e);out=[];at=0
        for bs in self.bits:
            row=[]
            for bit in bs:
                size=(bit+7)//8;value=int.from_bytes(raw[at:at+size],'little');at+=size
                assert value < (1<<bit)
                row.append(value)
            out.append(tuple(row))
        assert at==len(raw)
        return out

    def close(self):
        self.file.close()


def manifest():
    prior=read('dyadic_target_feasibility_review_d130')
    expected={r['path']:r['sha256'] for r in prior['sources']}
    state=read('dyadic_streamed_P3200_col00_verified_d129')
    assert state['certificate']['original_full_residual_zero']
    weighted=read(Path(state['weighted_state_metadata']['path']).stem)
    cm=read('dyadic_CM_P3200_col00_d129')
    inputs={}; largest=0
    records=[('weighted',weighted['state_file'],P,N,True),('uniform',state['state_file'],P,N,False)]
    records += [(f"cm{ch['first_chart']:02d}",ch['file'],2*P,ch['last_chart']-ch['first_chart']+1,False) for ch in cm['moment_chunks']]
    for label,record,count,rows,reduced in records:
        path=Path(record['path']);assert expected[str(path)]==record['sha256']
        size=sum((n+7)//8 for bs in layout(count,BITS,reduced) for n in bs)
        assert path.stat().st_size==size*rows
        full=hashlib.sha256();digests=[]
        with path.open('rb') as f:
            for _ in range(rows):
                sha=hashlib.sha256();left=size
                while left:
                    raw=f.read(min(1<<20,left));assert len(raw)==min(1<<20,left)
                    sha.update(raw);full.update(raw);left-=len(raw);largest=max(largest,len(raw))
                digests.append(sha.hexdigest())
            assert not f.read(1)
        assert full.hexdigest()==record['sha256'];CACHE[path]=record;PATHS.add(path)
        inputs[label]={'payload':record,'count':count,'bits':BITS,'weighted':reduced,'rows':rows,'row_bytes':size,'row_sha256':digests}
    for name in ('dyadic_streamed_P3200_col00_verified_d129',Path(state['weighted_state_metadata']['path']).stem,'dyadic_CM_P3200_col00_d129'):
        rec=source(DATA/(name+'.json'));assert expected[rec['path']]==rec['sha256']
    return {'inputs':inputs,'CM_chunks':cm['moment_chunks'],'maximum_hash_read_bytes':largest,
            'all_payloads_bound_to_prior_fixed_review':True,'generation_metadata':source(Path(state['weighted_state_metadata']['path'])),
            'prior_fixed_review':source(DATA/'dyadic_target_feasibility_review_d130.json')}


def inputs():
    packet=read('dyadic_weighted_manifest_d131')
    assert packet['phase']=='manifest' and packet['certificates']['all_payloads_bound_to_prior_fixed_review']
    return packet['certificates']


def parameters(ring):
    packet=read('dyadic_target_transports_d121')
    return packet,lambda child:tuple(tuple(int(v)&ring.mask for v in x) for x in child['normalized_center'][:3])


def composed(chart,child,ring,pars):
    A,B,C=pars(chart);a,bv,cv=pars(child);one=b.ONE;two=(2,)+(0,)*7
    den=ring.add(one,ring.mul(C,bv));inv=one
    for _ in range(P.bit_length()):inv=ring.mul(inv,ring.add(two,ring.neg(ring.mul(den,inv))))
    assert ring.mul(den,inv)==one
    return (ring.mul(ring.add(ring.mul(A,a),ring.mul(B,cv)),inv),
            ring.mul(ring.add(ring.mul(A,bv),B),inv),ring.mul(ring.add(cv,ring.mul(C,a)),inv))


def states(first,last):
    assert 0<=first<=last<N and last-first<6
    m=inputs();weighted=Reader(m['inputs']['weighted']);uniform=Reader(m['inputs']['uniform'])
    ring=p.Ring(BITS);transport,pars=parameters(ring)
    masses=read('dyadic_harmonic_certificate_d111')['harmonic_basis'][0]
    rows=[]
    for e in range(first,last+1):
        start=time.monotonic();total=[b.ZERO]*P
        for child in transport['transitions'][e]['children']:
            plan=l.Plan(ring,*pars(child),P,P)
            total=ring.padd(total,plan.apply(weighted.row(child['target_edge'])))
            del plan
        raw=encode(total,uniform.bits);assert raw==uniform.raw(e)
        assert encode(total,weighted.bits)==weighted.raw(e)
        assert total[0]==(masses[e]&ring.mask,)+(0,)*7
        rows.append({'state':e,'uniform_sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.monotonic()-start})
    weighted.close();uniform.close()
    return {'first_state':first,'last_state':last,'GMP_original_child_actions':2*len(rows),
            'uniform_scalar_comparisons':len(rows)*P*8,'weighted_scalar_comparisons':len(rows)*P*8,
            'all_QT_w_equals_w':True,'exact_masses_checked':len(rows),'rows':rows,
            'per_request_full_payload_hashes':0,'new_binary_payload_bytes':0}


def cm(first,last):
    assert 0<=first<=last<17 and last-first<3
    m=inputs();weighted=Reader(m['inputs']['weighted']);ring=p.Ring(BITS)
    transport,pars=parameters(ring);charts=[c for c in transport['CM_charts'] if c['chart']=='A']
    out=[]
    for ci in range(first,last+1):
        chart=charts[ci];total=[b.ZERO]*(2*P)
        for child in transport['transitions'][chart['target_edge']]['children']:
            plan=l.Plan(ring,*composed(chart,child,ring,pars),P,2*P)
            total=ring.padd(total,plan.apply(weighted.row(child['target_edge'])))
            del plan
        ch=[x for x in m['CM_chunks'] if x['first_chart']<=ci<=x['last_chart']][0]
        ref=Reader(m['inputs'][f"cm{ch['first_chart']:02d}"])
        raw=encode(total,ref.bits);assert raw==ref.raw(ci-ch['first_chart']);ref.close()
        assert total[0]==(chart['zeroth_moments'][0]&ring.mask,)+(0,)*7
        out.append({'chart':ci,'sha256':hashlib.sha256(raw).hexdigest()})
    weighted.close()
    return {'first_chart':first,'last_chart':last,'GMP_composed_child_actions':2*len(out),
            'complete_CM_scalar_comparisons':len(out)*2*P*8,'charts':out,
            'D129_reference_already_used_weighted_inputs':True,'per_request_full_payload_hashes':0,'new_binary_payload_bytes':0}


def negative():
    m=inputs();reader=Reader(m['inputs']['weighted']);ring=p.Ring(BITS)
    transport,pars=parameters(ring);child=transport['transitions'][0]['children'][0]
    values=reader.row(child['target_edge']);reader.close();a,bv,c=pars(child)
    plan=l.Plan(ring,a,bv,c,P,P);expected=plan.apply(values)
    noisy=list(values)
    for k,i in ((33,0),(1599,3),(3199,7)):
        row=list(noisy[k]);row[i]=(row[i]+(1<<max(0,(P-k-i+7)//8)))&ring.mask;noisy[k]=tuple(row)
    assert noisy!=values and encode(noisy,reader.bits)==encode(values,reader.bits)
    assert plan.apply(noisy)==expected
    wrong=list(values);row=list(wrong[1]);row[0]=(row[0]+1)&ring.mask;wrong[1]=tuple(row)
    altered=plan.apply(wrong);delta=ring.add(a,ring.neg(ring.mul(bv,c)))
    assert delta!=b.ZERO and ring.add(altered[1],ring.neg(expected[1]))==delta
    assert altered!=expected
    return {'full_annihilator_scalar_comparisons':P*8,'nontrivial_error_lattice_perturbations':3,
            'low_moment_error_detected':True,'wrong_low_output_difference_equals_delta':True,
            'only_private_memory_modified':True}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--phase',choices=('manifest','states','cm','negative'),required=True)
    ap.add_argument('--first',type=int);ap.add_argument('--last',type=int);ap.add_argument('--output',required=True)
    args=ap.parse_args();out=DATA/(args.output+'.json');assert not out.exists()
    tick=time.monotonic()
    cert=manifest() if args.phase=='manifest' else states(args.first,args.last) if args.phase=='states' else cm(args.first,args.last) if args.phase=='cm' else negative()
    packet={'status':'pass','milestone':'D131','phase':args.phase,'certificates':cert,
            'actual_harmonic_precision_increased':False,'working_precision_pi':P,
            'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
            'sources':[source(p) for p in sorted(PATHS)]}
    out.write_text(json.dumps(packet,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(out)),flush=True)
    print(json.dumps({'phase':args.phase,'wall_seconds':packet['wall_seconds'],'peak_rss_bytes':packet['peak_rss_bytes']}),flush=True)
    print('PASS|541_DYADIC_WEIGHTED_CERTIFICATE',flush=True)

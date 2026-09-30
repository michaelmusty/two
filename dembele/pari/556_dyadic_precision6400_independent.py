"""D133 bounded independent checks on the sealed actual weighted P=6400 column.

Pure quotient arithmetic is inherited from reviewer 486. Production
arithmetic is never imported. Complete old overlaps and sampled original
recurrences have separate, explicit scopes.
"""
import argparse
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path
import resource
import sys
import time
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
STORE=DATA/'dyadic_rowjournal_P6400_col00_d132';BASE='dyadic_staged_P6400_col00_d133'
s=importlib.util.spec_from_file_location('independent',ROOT/'dembele/pari/486_dyadic_precision400_independent.py')
r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
P,S,N=6400,3200,174;PATHS={Path(__file__),Path(r.__file__)};CACHE={}
def source(path):
    path=Path(path).resolve();PATHS.add(path)
    if path not in CACHE:CACHE[path]=r.source(path)
    return CACHE[path]
def canonical(d):return json.dumps(d,sort_keys=True,separators=(',',':')).encode()
def read(stem):
    path=DATA/(stem+'.json');PATHS.add(path);d=json.loads(path.read_text());assert d['status']=='pass';return d
def env(name):
    path=STORE/name;PATHS.add(path);p=json.loads(path.read_text());assert set(p)=={'value','sha256'}
    assert hashlib.sha256(canonical(p['value'])).hexdigest()==p['sha256'];return p['value']
def current():
    seal=env('SEALED.json');cur=env('CURRENT.json')
    assert seal['all_remaining_files_frozen'] and seal['current_sha256']==hashlib.sha256(canonical(cur)).hexdigest()
    assert cur['tag']=='ready096' and cur['phase']=='ready' and cur['authority']=={'u':6368,'count':33,'bits':4}
    return cur
def decode(raw,count,bits,weighted=False):
    values=[];at=0
    for k in range(count):
        row=[]
        for i in range(8):
            bit=bits if not weighted or k<=32 else max(0,(count-k-i+7)//8)
            size=(bit+7)//8;v=int.from_bytes(raw[at:at+size],'little');at+=size
            assert v<1<<bit;row.append(v)
        values.append(tuple(row))
    assert at==len(raw);return values
def stored(info,e,count,bits,weighted=False):
    path=STORE/info['name'];PATHS.add(path);assert path.stat().st_size==info['bytes']
    with path.open('rb') as f:f.seek(e*info['row_bytes']);raw=f.read(info['row_bytes'])
    assert len(raw)==info['row_bytes'] and hashlib.sha256(raw).hexdigest()==info['row_sha256'][e]
    return decode(raw,count,bits,weighted)
def reference(record,e,count,bits):
    path=Path(record['path']);assert source(path)==record;width=count*8*((bits+7)//8)
    with path.open('rb') as f:f.seek(e*width);raw=f.read(width)
    assert len(raw)==width;return decode(raw,count,bits)
def recurrence(ring,pars,values,degrees):
    a,b,c=pars;power=[ring.one]+[ring.zero]*(len(values)-1);out={}
    for n in range(1,max(degrees)+1):
        new=[ring.mul(b,power[0])]
        for k in range(1,len(values)):new.append(ring.sub(ring.add(ring.mul(b,power[k]),ring.mul(a,power[k-1])),ring.mul(c,new[-1])))
        power=new
        if n in degrees:
            val=ring.zero
            for x,y in zip(power,values):val=ring.add(val,ring.mul(x,y))
            out[n]=val
    return out
def states(first,last):
    assert 0<=first<=last<N and last-first<29
    cur=current();inputs=env('INPUTS.json');masses=read('dyadic_harmonic_certificate_d111')['harmonic_basis'][0]
    old=inputs['seed']['payload'];assert inputs['seed']['count']==S and not inputs['seed']['weighted']
    count=0;digests=[]
    for e in range(first,last+1):
        row=stored(cur['state'],e,P,800,True);prior=reference(old,e,S,400)
        assert row[0]==(masses[e]%(1<<800),)+(0,)*7
        for k in range(S):
            for i in range(8):
                bit=400 if k<=32 else max(0,(S-k-i+7)//8)
                assert row[k][i]%(1<<bit)==prior[k][i]%(1<<bit);count+=1
        assert stored(cur['aux'],e,33,4)==[(0,)*8]*33
        digests.append(cur['state']['row_sha256'][e])
    return {'first_state':first,'last_state':last,'complete_old_weighted_overlap_scalars':count,
            'exact_masses':last-first+1,'final_residual_zero_rows':last-first+1,'row_sha256':digests}
def ordinary_state(e):
    assert e in (0,83,173);cur=current();ring=r.Quotient(r.FP,P);transport=read('dyadic_target_transports_d121')
    degrees=(1,2,3);total={n:ring.zero for n in degrees}
    for child in transport['transitions'][e]['children']:
        assert child['normalized_error_pi']>=P
        row=stored(cur['state'],child['target_edge'],P,800,True)
        part=recurrence(ring,tuple(map(ring.norm,child['normalized_center'][:3])),row,degrees)
        for n in total:total[n]=ring.add(total[n],part[n])
    own=stored(cur['state'],e,P,800,True)
    for n,value in total.items():assert value==own[n]
    return {'state':e,'degrees':list(degrees),'ordinary_original_scalar_checks':24,'complete_operator_independently_recomputed':False}
def cm_rows(first,last):
    assert 0<=first<=last<17 and last-first<3
    current();cm=env('pool_CM.json');prior=read('dyadic_CM_P3200_col00_d129');scalars=0
    transport=read('dyadic_target_transports_d121');charts=[x for x in transport['CM_charts'] if x['chart']=='A']
    ring=r.Quotient(r.MP,12864);coarse_count=0
    for ci in range(first,last+1):
        values=stored(cm,ci,2*P,800)
        assert values[0]==(charts[ci]['zeroth_moments'][0]%(1<<800),)+(0,)*7
        chunk=next(x for x in prior['moment_chunks'] if x['first_chart']<=ci<=x['last_chart'])
        old=reference(chunk['file'],ci-chunk['first_chart'],2*S,400)
        assert [tuple(x% (1<<400) for x in row) for row in values[:2*S]]==old;scalars+=2*S*8
        for order,gain in enumerate((32,48,32,64)):
            d=read(f'{BASE}_coarse_c{ci:02d}_o{order}')['certificates']
            assert d['chart']==ci and d['order']==order and d['error_beta']==2*P+gain
            oldvalue=prior['CM_values'][ci]['coarse_coefficients_beta'][order]
            assert ring.value(ring.sub(ring.norm(d['coarse_value_beta']),ring.norm(oldvalue)))>=prior['coarse_error_beta'][order];coarse_count+=1
    return {'first_chart':first,'last_chart':last,'old_CM_overlap_scalars':scalars,'coarse_old_overlaps':coarse_count,'new_coarse_errors_beta':[12832,12848,12832,12864]}
def ordinary_cm(ci):
    assert ci in (0,8,16);cur=current();cm=env('pool_CM.json');ring=r.Quotient(r.FP,P)
    transport=read('dyadic_target_transports_d121');chart=[x for x in transport['CM_charts'] if x['chart']=='A'][ci]
    A,B,C=map(ring.norm,chart['normalized_center'][:3]);totals={n:ring.zero for n in (1,2,3)}
    for child in transport['transitions'][chart['target_edge']]['children']:
        a,b,c=map(ring.norm,child['normalized_center'][:3]);den=ring.add(ring.one,ring.mul(C,b));inv=ring.one
        for _ in range(P.bit_length()):inv=ring.mul(inv,ring.sub(ring.scale(ring.one,2),ring.mul(den,inv)))
        assert ring.mul(den,inv)==ring.one
        pars=(ring.mul(ring.add(ring.mul(A,a),ring.mul(B,c)),inv),ring.mul(ring.add(ring.mul(A,b),B),inv),ring.mul(ring.add(c,ring.mul(C,a)),inv))
        assert ring.value(pars[2])>=1 and ring.value(ring.sub(pars[0],ring.mul(pars[1],pars[2])))>=1
        part=recurrence(ring,pars,stored(cur['state'],child['target_edge'],P,800,True),(1,2,3))
        for n in totals:totals[n]=ring.add(totals[n],part[n])
    expected=stored(cm,ci,2*P,800)
    for n,value in totals.items():assert value==expected[n]
    return {'chart':ci,'degrees':[1,2,3],'ordinary_CM_scalar_checks':24,'complete_CM_operator_independently_recomputed':False}
def coarse_horner(ci,order):
    assert ci in (0,8,16) and order in (0,3);current();cm=env('pool_CM.json');moments=stored(cm,ci,2*P,800)
    ring=r.Quotient(r.MP,12864);pi=ring.sub(ring.scale(ring.one,-2),ring.mul(ring.beta,ring.beta));q=ring.sub(tuple(r.MP[1:]),ring.beta)
    assert ring.mul(q,ring.beta)==pi;powers=[ring.one]
    for _ in range(7):powers.append(ring.mul(powers[-1],pi))
    n=2*order+2;value=ring.zero
    for k in range(2*P-1,-1,-1):
        embedded=ring.zero
        for x,power in zip(moments[k],powers):embedded=ring.add(embedded,ring.scale(power,x))
        coefficient=0 if k==0 else -sum(comb(n,i)*comb(n+k-i-1,k-i) for i in range(min(n,k)+1))
        value=ring.add(ring.mul(value,q),ring.scale(embedded,coefficient))
    expected=read(f'{BASE}_coarse_c{ci:02d}_o{order}')['certificates']
    assert value==tuple(expected['coarse_value_beta'])
    return {'chart':ci,'order':order,'independent_integer_quotient_Horner_matches_direct_sum':True,'complete_beta_scalar_checks':16,'error_beta':expected['error_beta']}
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--phase',choices=('states','ordinary-state','cm','ordinary-cm','coarse-horner'),required=True)
    for name in ('first','last','state','chart','order'):ap.add_argument('--'+name,type=int)
    ap.add_argument('--output',required=True);a=ap.parse_args();out=DATA/(a.output+'.json');assert not out.exists();tick=time.monotonic()
    cert=states(a.first,a.last) if a.phase=='states' else ordinary_state(a.state) if a.phase=='ordinary-state' else cm_rows(a.first,a.last) if a.phase=='cm' else ordinary_cm(a.chart) if a.phase=='ordinary-cm' else coarse_horner(a.chart,a.order)
    packet={'status':'pass','milestone':'D133','phase':a.phase,'certificates':cert,'production_arithmetic_not_imported':True,
            'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
            'sources':[source(x) for x in sorted(PATHS)]}
    assert packet['peak_rss_bytes']<=2*(1<<30)
    out.write_text(json.dumps(packet,indent=2)+'\n');print('PHASE_METADATA|'+json.dumps(source(out)),flush=True)
    print('PASS|556_DYADIC_PRECISION6400_INDEPENDENT',flush=True)

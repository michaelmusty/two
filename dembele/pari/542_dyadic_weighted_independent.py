"""D131 separate ordinary-arithmetic samples and complete replay coverage audit."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('independent',ROOT/'dembele/pari/486_dyadic_precision400_independent.py')
r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
PATHS={Path(__file__),Path(r.__file__)}


def source(path):
    path=Path(path).resolve();PATHS.add(path);return r.source(path)


def read(stem):
    path=DATA/(stem+'.json');PATHS.add(path);p=json.loads(path.read_text());assert p['status']=='pass';return p


def row(record,e):
    assert 0<=e<record['rows'];size=record['row_bytes']
    with Path(record['payload']['path']).open('rb') as f:
        f.seek(e*size);raw=f.read(size)
    assert len(raw)==size and hashlib.sha256(raw).hexdigest()==record['row_sha256'][e]
    at=0;out=[]
    for k in range(record['count']):
        vals=[]
        for i in range(8):
            bits=max(0,-((i-(record['count']-k))//8)) if record['weighted'] and k>32 else record['bits']
            n=(bits+7)//8;v=int.from_bytes(raw[at:at+n],'little');at+=n;assert v<1<<bits;vals.append(v)
        out.append(tuple(vals))
    assert at==size;return out


def samples(kind):
    m=read('dyadic_weighted_manifest_d131')['certificates']
    t=read('dyadic_target_transports_d121');ring=r.Quotient(r.FP,3200)
    charts=[c for c in t['CM_charts'] if c['chart']=='A']
    selected=(0,83,173) if kind=='states' else (0,8,16)
    for e in selected:
        chart=charts[e] if kind=='cm' else None
        edge=chart['target_edge'] if chart else e
        totals=[ring.zero]*3
        for child in t['transitions'][edge]['children']:
            a,b,c=map(ring.norm,child['normalized_center'][:3])
            if chart:
                A,B,C=map(ring.norm,chart['normalized_center'][:3]);den=ring.add(ring.one,ring.mul(C,b));inv=ring.one
                for _ in range(12):inv=ring.mul(inv,ring.sub(ring.scale(ring.one,2),ring.mul(den,inv)))
                assert ring.mul(den,inv)==ring.one
                a,b,c=(ring.mul(ring.add(ring.mul(A,a),ring.mul(B,c)),inv),
                       ring.mul(ring.add(ring.mul(A,b),B),inv),ring.mul(ring.add(c,ring.mul(C,a)),inv))
            values=row(m['inputs']['weighted'],child['target_edge'])
            power=[ring.one]+[ring.zero]*3199
            for n in range(3):
                new=[ring.mul(b,power[0])]
                for k in range(1,3200):
                    new.append(ring.sub(ring.add(ring.mul(b,power[k]),ring.mul(a,power[k-1])),ring.mul(c,new[-1])))
                power=new;v=ring.zero
                for x,y in zip(power,values):v=ring.add(v,ring.mul(x,y))
                totals[n]=ring.add(totals[n],v)
        if kind=='states':expected=row(m['inputs']['uniform'],e)
        else:
            ch=[c for c in m['CM_chunks'] if c['first_chart']<=e<=c['last_chart']][0]
            expected=row(m['inputs'][f"cm{ch['first_chart']:02d}"],e-ch['first_chart'])
        assert totals==expected[1:4]
    return {'kind':kind,'sampled_states_or_charts':list(selected),'ordinary_power_degrees':[1,2,3],
            'full_input_moment_count':3200,'scalar_equations_checked':72,
            'complete_original_operator_independently_recomputed':False}


def aggregate():
    m=read('dyadic_weighted_manifest_d131')['certificates']
    rows=[];charts=[]
    for first in range(0,174,6):
        p=read(f'dyadic_weighted_replay_e{first:03d}_{first+5:03d}_d131');c=p['certificates']
        assert c['all_QT_w_equals_w'] and c['uniform_scalar_comparisons']==c['weighted_scalar_comparisons']==6*3200*8
        assert c['exact_masses_checked']==6 and c['new_binary_payload_bytes']==0
        assert c['per_request_full_payload_hashes']==0 and not p['actual_harmonic_precision_increased']
        for x in c['rows']:
            assert x['state']==len(rows);assert x['uniform_sha256']==m['inputs']['uniform']['row_sha256'][len(rows)];rows.append(x)
    for first in range(0,17,3):
        c=read(f'dyadic_weighted_CM_c{first:02d}_{min(16,first+2):02d}_d131')['certificates']
        assert c['new_binary_payload_bytes']==c['per_request_full_payload_hashes']==0
        for x in c['charts']:
            ci=len(charts);assert x['chart']==ci
            ch=[z for z in m['CM_chunks'] if z['first_chart']<=ci<=z['last_chart']][0]
            assert x['sha256']==m['inputs'][f"cm{ch['first_chart']:02d}"]['row_sha256'][ci-ch['first_chart']]
            charts.append(x)
    assert len(rows)==174 and len(charts)==17
    neg=read('dyadic_weighted_annihilator_d131')['certificates']
    assert neg['full_annihilator_scalar_comparisons']==25600 and neg['low_moment_error_detected']
    bounds=read('dyadic_target_feasibility_review_d130')['finite_certificates']['weighted_representation_coefficient_bounds']
    assert bounds['original_children_checked']==348 and bounds['CM_compositions_checked']==34
    assert bounds['all_denominators_units_and_c_delta_divisible_by_pi']
    return {'complete_original_state_coverage':174,'original_child_actions':348,
            'uniform_coordinate_comparisons':4454400,'weighted_coordinate_comparisons':4454400,
            'exact_masses':174,'complete_CM_chart_coverage':17,'composed_CM_child_actions':34,
            'CM_coordinate_comparisons':870400,'no_new_uniform_or_CM_payload_written':True,
            'weighted_fixed_point_certificate_replayed':True,'new_harmonic_precision_claimed':False}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--phase',choices=('states','cm','aggregate'),required=True);ap.add_argument('--output',required=True)
    a=ap.parse_args();out=DATA/(a.output+'.json');assert not out.exists();tick=time.monotonic()
    cert=aggregate() if a.phase=='aggregate' else samples(a.phase)
    p={'status':'pass','milestone':'D131','phase':a.phase,'certificates':cert,
       'production_arithmetic_not_imported':True,'actual_harmonic_precision_increased':False,
       'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
       'sources':[source(x) for x in sorted(PATHS)]}
    out.write_text(json.dumps(p,indent=2)+'\n');print('PHASE_METADATA|'+json.dumps(source(out)),flush=True)
    print('PASS|542_DYADIC_WEIGHTED_INDEPENDENT',flush=True)

"""D115: inspect support reachable from the W boundary chart."""
from collections import deque
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'

def main():
    p=json.loads((DATA/'dyadic_moment_transports_d113.json').read_text())
    h=json.loads((DATA/'dyadic_harmonic_certificate_d111.json').read_text())
    byedge=p['transitions'];start=p['CM_charts'][0]['target_edge']
    queue=deque([start]);distance={start:0};paths={start:[]};levels={}
    while queue:
        e=queue.popleft();mass=[row[e] for row in h['harmonic_basis']]
        if any(mass):levels.setdefault(distance[e],[]).append(e)
        for j,child in enumerate(byedge[e]['children']):
            f=child['target_edge']
            if f not in distance:distance[f]=distance[e]+1;paths[f]=paths[e]+[(e,j,f)];queue.append(f)
    print(json.dumps({'anchor_A_edge':start,'reachable_states':len(distance),'nearest_support_distance':min(levels) if levels else None,
          'support_by_distance':levels,'first_support_path':paths[levels[min(levels)][0]] if levels else None},indent=2),flush=True)
    for P in [16,24,40,56]:
        path=DATA/('dyadic_moment_extension_d114.json' if P==16 else f'dyadic_precision{P}_d115.json')
        if not path.exists():continue
        data=json.loads(path.read_text());rows=data.get('CM_A_chart_moments',data.get('CM_chart_moments'))[0]['moments_power_basis']
        def val(cs):return min((8*((c&-c).bit_length()-1)+i for i,c in enumerate(cs) if c),default=P)
        print(json.dumps({'P':P,'minimum_anchor_moment_valuation':min(val(x) for row in rows for x in row),
            'first_nonzero_moment':next((n for n,row in enumerate(rows) if any(val(x)<P for x in row)),None)}),flush=True)
    print('PASS|419_DYADIC_SUPPORT',flush=True)

if __name__=='__main__':main()

"""D136: one complete target CM chart on a synthetic compatible lift.

Both composed children run in the same process, as in production. High
digits are deliberately synthetic: this measures the integrated memory
shape and verifies old certified overlaps, never new harmonic precision.
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
STORE = DATA / 'dyadic_rowjournal_P6400_col00_d132'
P, S, K, OLD_BITS = 10552, 6400, 1319, 800
CAP = 2 * (1 << 30)
PATHS = {Path(__file__)}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    h = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            h.update(raw)
    return {'path': str(path), 'sha256': h.hexdigest()}


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--chart',type=int,required=True)
    ap.add_argument('--output',required=True)
    args = ap.parse_args()
    assert 0 <= args.chart < 17
    output = DATA / (args.output + '.json')
    binary = DATA / (args.output + '.bin')
    assert not output.exists() and not binary.exists()
    tick = time.monotonic()
    prior_path = DATA / 'dyadic_bank_recost_review_d135.json'
    prior = json.loads(prior_path.read_text())
    assert prior['status'] == 'pass' and prior['independent_finite_review_complete']
    known = {r['path']:r['sha256'] for r in prior['sources']}
    assert len(known) == 93928
    prior_source = source(prior_path)

    def read_bound(path, envelope=False):
        path = Path(path)
        raw = path.read_bytes()
        assert known[str(path)] == hashlib.sha256(raw).hexdigest()
        PATHS.add(path)
        value = json.loads(raw)
        if envelope:
            assert hashlib.sha256(canonical(value['value'])).hexdigest() == value['sha256']
            return value['value']
        assert value['status'] == 'pass'
        return value

    driver = ROOT / 'dembele/pari/554_dyadic_resumable_staged_production.py'
    assert source(driver)['sha256'] == known[str(driver)]
    spec = importlib.util.spec_from_file_location('d136_original',driver)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for path in m.immutable_dependencies():
        assert source(path)['sha256'] == known[str(path)], str(path)
    current = read_bound(STORE/'CURRENT.json',True)
    sealed = read_bound(STORE/'SEALED.json',True)
    read_bound(STORE/'VERIFIED.json',True)
    assert current['tag'] == 'ready096'
    cm = read_bound(STORE/'pool_CM.json',True)
    assert cm['complete'] and cm['rows'] == 17
    transport = read_bound(DATA/'dyadic_target_transports_d121.json')
    harmonic = read_bound(DATA/'dyadic_harmonic_certificate_d111.json')
    charts = [r for r in transport['CM_charts'] if r['chart'] == 'A']
    chart = charts[args.chart]
    assert chart['CM_index'] == args.chart
    ring = m.p.Ring(K)
    def pars(record):
        assert record['normalized_error_pi'] >= P
        return tuple(tuple(int(v)&ring.mask for v in row) for row in record['normalized_center'][:3])
    old_layout = m.v.layout(S,OLD_BITS,True)
    new_layout = m.v.layout(P,K,True)
    state_record = current['state']
    state_path = STORE/state_record['name']
    assert state_record['sha256'] == known[str(state_path)]
    assert state_path.stat().st_size == state_record['bytes']
    # The full payload is bound by the reviewed current generation; each row
    # actually used below is freshly authenticated, without rehashing449MB.
    old_inputs = []
    def lift(edge):
        with state_path.open('rb') as f:
            f.seek(edge*state_record['row_bytes'])
            raw = f.read(state_record['row_bytes'])
        assert hashlib.sha256(raw).hexdigest() == state_record['row_sha256'][edge]
        old_inputs.append({'state':edge,'row_sha256':state_record['row_sha256'][edge]})
        old = m.decode(raw,S,OLD_BITS,True)
        out = []
        for degree, widths in enumerate(new_layout):
            row = []
            for basis,bits in enumerate(widths):
                label = f'D136-compatible-state{edge}-degree{degree}-basis{basis}'.encode()
                noise = int.from_bytes(hashlib.shake_256(label).digest((bits+7)//8),'little')
                if degree < S:
                    value = old[degree][basis] + (noise << old_layout[degree][basis])
                    assert value % (1<<old_layout[degree][basis]) == old[degree][basis]
                else:
                    value = noise
                row.append(value & ((1<<bits)-1))
            out.append(tuple(row))
        out[0] = (harmonic['harmonic_basis'][0][edge]&ring.mask,) + (0,)*7
        return out

    A,B,C = pars(chart)
    total = [m.b.ZERO] * (2*P)
    child_times = []
    arithmetic_tick = time.monotonic()
    for branch,child in enumerate(transport['transitions'][chart['target_edge']]['children']):
        begin = time.monotonic()
        a,b,c = pars(child)
        den = ring.add(m.b.ONE,ring.mul(C,b))
        inv = m.b.ONE
        two = (2,)+(0,)*7
        for _ in range(P.bit_length()):
            inv = ring.mul(inv,ring.add(two,ring.neg(ring.mul(den,inv))))
        assert ring.mul(den,inv) == m.b.ONE
        par = (ring.mul(ring.add(ring.mul(A,a),ring.mul(B,c)),inv),
               ring.mul(ring.add(ring.mul(A,b),B),inv),
               ring.mul(ring.add(c,ring.mul(C,a)),inv))
        values = lift(child['target_edge'])
        # Match the live-object lifecycle in source554 exactly: retain the
        # first child's total, and release each plan/input after addition.
        plan = m.l.Plan(ring,*par,P,2*P)
        total = ring.padd(total,plan.apply(values))
        del plan,values
        seconds = time.monotonic()-begin
        child_times.append(seconds)
        print('TARGET_CHART_CHILD|'+json.dumps({'chart':args.chart,'branch':branch,'seconds':seconds}),flush=True)
    assert total[0] == (chart['zeroth_moments'][0]&ring.mask,)+(0,)*7
    cm_path = STORE/cm['name']
    assert cm['sha256'] == known[str(cm_path)]
    with cm_path.open('rb') as f:
        f.seek(args.chart*cm['row_bytes'])
        old_raw = f.read(cm['row_bytes'])
    assert hashlib.sha256(old_raw).hexdigest() == cm['row_sha256'][args.chart]
    old_cm = m.decode(old_raw,2*S,OLD_BITS)
    mask = (1<<OLD_BITS)-1
    assert [[x&mask for x in row] for row in total[:2*S]] == [list(row) for row in old_cm]
    raw = m.b.pack([total],K)
    assert len(raw) == 2*P*8*165
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    print('TARGET_CHART_RESOURCE|'+json.dumps({'chart':args.chart,'peak_rss_bytes':peak,'cap_bytes':CAP}),flush=True)
    assert peak <= CAP, 'Integrated chart exceeds measured per-job RSS admission; split or redesign before proceeding'
    with binary.open('xb') as f:
        f.write(raw)
    record = {'status':'pass','milestone':'D136','kind':'complete_target_chart_memory_control',
              'chart':args.chart,'working_precision_pi':P,'seed_precision_pi':S,'column':0,
              'input_kind':'synthetic_high_digits_preserving_reviewed_P6400_weighted_rows',
              'prior_fixed_review':prior_source,'production_driver':source(driver),
              'two_composed_children_same_process':True,'child_seconds':child_times,
              'old_weighted_inputs':old_inputs,'old_CM_row_sha256':cm['row_sha256'][args.chart],
              'all_old_CM_overlap_scalars':2*S*8,'zeroth_mass_checked':True,
              'target_scalar_count':2*P*8,'target_binary_bytes':len(raw),'target_binary':source(binary),
              'arithmetic_and_comparison_seconds':time.monotonic()-arithmetic_tick,
              'peak_rss_bytes':peak,'measured_per_job_RSS_cap_bytes':CAP,
              'wall_seconds':time.monotonic()-tick,
              'actual_harmonic_precision_increased':False,'actual_CM_precision_increased':False,
              'candidate_identification_proved':False,'full_bank_launch_admitted':False,
              'sources':[source(p) for p in sorted(PATHS) if p != binary]}
    with output.open('x') as f:
        f.write(json.dumps(record,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|562_DYADIC_TARGET_CHART_CONTROL',flush=True)


if __name__ == '__main__':
    main()

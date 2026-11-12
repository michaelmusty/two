"""D144: joint adjunction constants and a reconstructed compact RR constant.

Run only through run_dyadic_capped.py. Geometric/analytic proofs are in the
companion report; finite checks do not mechanically verify those proofs.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
SAGE = Path('/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/Current')
PYTHON = SAGE/'venv/bin/python3'
INPUTS = ['cm_intrinsic_height_review_d104', 'cm_finite_height_review_d118',
          'cm_cartier_frame_review_d119', 'P1600_elliptic_heights_d143',
          'P1600_dyadic_model_diagnostic_d143', 'P1600_dyadic_model_audit_d143']


def source(path):
    p = Path(path).resolve()
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def worker(out):
    from sage.all import QQ, RealBallField, PolynomialRing
    R = RealBallField(192)
    iv = lambda x: [str(QQ(x.lower())), str(QQ(x.upper()))]
    def ball(pair):
        a, b = map(QQ, pair)
        return R((a+b)/2, (b-a)/2)
    packets = {n: json.loads((DATA/(n+'.json')).read_text()) for n in INPUTS}
    assert all(p['status'] == 'pass' for p in packets.values())
    model = packets['P1600_dyadic_model_diagnostic_d143']
    audit = packets['P1600_dyadic_model_audit_d143']
    h = {2: R(QQ(packets['cm_intrinsic_height_review_d104']['independent_analytic']['Hodge_height_interval'][1]))}
    h.update({r['elliptic_order']: ball(r['absolute_Hodge_height_interval'])
              for r in packets['P1600_elliptic_heights_d143']['CM_heights']})
    signature = {2: 17, 3: 9, 32: 1}
    alpha = {m: 1-QQ(1)/m for m in signature}
    beta = {m: 1-QQ(1)/m**2 for m in signature}
    gamma = {m: m-QQ(1)/m for m in signature}
    # Eliminate H_i symbolically, retaining unordered pair intersections.
    orders = [2, 3, 32]
    P = PolynomialRing(QQ, names=['l0','l1','l2','k0','k1','k2','q0','q1','q2','j01','j02','j12'])
    ell, lm, q = P.gens()[:3], P.gens()[3:6], P.gens()[6:9]
    j = {(0,1): P.gen(9), (0,2): P.gen(10), (1,2): P.gen(11)}
    cross = lambda i: sum(alpha[orders[k]]*j[tuple(sorted((i,k)))] for k in range(3) if k != i)
    H = [orders[i]*(ell[i]+lm[i]-q[i]-cross(i)) for i in range(3)]
    S = sum(beta[m]*H[i] for i,m in enumerate(orders))+sum(2*alpha[orders[i]]*alpha[orders[k]]*x for (i,k),x in j.items())
    rhs = sum(gamma[m]*(ell[i]+lm[i]-q[i]) for i,m in enumerate(orders))-sum(alpha[orders[i]]*alpha[orders[k]]*(orders[i]+orders[k])*x for (i,k),x in j.items())
    assert S == rhs
    weighted_v = sum(gamma[m]*c['different_coefficient']*c['order'+str(m)+'_points']
                     for c in model['components'] for m in signature)
    assert weighted_v/8 == QQ(27799)/256
    tails = model['tail_contractions']
    tail_length = sum(QQ(t['length']) for t in tails)
    tail_W = sum(QQ(t['length'])*(1-QQ(t['mark_weight_carried']))**2 for t in tails)
    tail_S = sum(QQ(t['length'])*(QQ(t['mark_weight_carried'])**2-2*QQ(t['mark_weight_carried'])) for t in tails)
    assert tail_length == 48 and tail_W == QQ(16955)/768
    assert tail_S == tail_W-tail_length == -QQ(19909)/768
    # Recover the anchor collision from the already revalued D118 jet.
    contents = packets['cm_finite_height_review_d118']['certificates']['composite_fibre']['combined_dyadic_contents_beta']
    assert contents == [280]+[17]*16
    anchor_path_length = sum(QQ(t['length']) for t in tails if t['contracted'] in [5,4,2,3])
    assert anchor_path_length == 36
    anchor_J = (QQ(contents[0])/2-2*25+8-anchor_path_length)/(2*alpha[32])
    ordinary_J = QQ(packets['cm_cartier_frame_review_d119']['certificate']['model']['intersection_length_each_ordinary_pair_beta'])/2
    assert anchor_J == 32 and ordinary_J == QQ(33)/2
    assert 2*alpha[2]*ordinary_J-8 == QQ(contents[1])/2
    anchor_cost = alpha[2]*alpha[32]*(2+32)*anchor_J/8
    ordinary_cost = 8*alpha[2]**2*(2+2)*ordinary_J/8
    assert anchor_cost == QQ(527)/8 and ordinary_cost == QQ(33)/2
    # At p=3 integrality forces a weighted row sum >= (2/3) v(3).
    prime3_rows = []
    for i,m in enumerate(orders):
        for n in orders[i:]:
            cost = alpha[m]*alpha[n]*(m+n)
            row_weight = (alpha[n] if m == 3 else 0)+(alpha[m] if n == 3 else 0)
            assert cost >= 2*row_weight
            prime3_rows.append({'orders':[m,n], 'cost':str(cost), 'twice_row_weight':str(2*row_weight)})
    prime3_cost = 2*signature[3]*QQ(2)/3
    assert prime3_cost == 12
    l2, lp, l3 = R(2).log(), R.pi().log(), R(3).log()
    cm = sum(signature[m]*gamma[m]*(h[m]+R(m).log()) for m in signature)
    stage0 = cm-weighted_v/8*l2+tail_S/8*l2
    stage1 = stage0-ordinary_cost*l2
    stage2 = stage1-anchor_cost*l2
    joint = stage2-prime3_cost*l3
    log2_cost = weighted_v/8+ordinary_cost+anchor_cost-tail_S/8
    assert log2_cost == QQ(1193197)/6144
    # Reassemble from scalar spectrum, cap, boundary anomaly and adjunction.
    z, eg = R(-1).zetaderiv(1), R.euler_constant()
    base = 15*(l2+lp-QQ(1)/3)+6*l2
    C_direct, C_closed, C_printed = base, base, base
    cone_records = []
    for m in [1,2,3,32]:
        m = QQ(m); a = 1-1/m; b = 1-1/m**2; logm = R(m).log()
        gammas = [R(QQ(k)/m).log_gamma() for k in range(1,int(m))]
        A = sum((2*QQ(k)-1-m)/m*gammas[k-1] for k in range(1,int(m)))
        G = sum(k*gammas[k-1] for k in range(1,int(m)))
        cnew = -m*(l2/3+lp/2)-(2*z-2*G+QQ(5)/12-l2/6)/m+logm/2+m*logm/6+logm/(3*m)
        cold = m*(2*z-QQ(1)/6+l2/6)-(QQ(5)/12-l2/6+eg/6)/m+logm/2+m*logm/6+logm/(6*m)+QQ(1)/4
        spectral = a*(2*z-QQ(1)/4+(l2+lp)/2)+A+(m-1/m)*logm/6
        disk = -2*z-(l2+lp)/2+l2/3-QQ(5)/12
        # Cut at epsilon/2; correct outward-normal Polyakov limit.
        anomaly = a/2-b*l2/6
        negative_cone = (m+1/m)*a*l2/6-cnew
        topological = a*l2/6-a*logm/3
        assembled = spectral+anomaly+disk+logm/3+negative_cone+topological
        closed = a*(l2-1)/6+logm/(3*m)
        assert (assembled-closed).contains_zero()
        printed = A+(QQ(1)/6-QQ(2)/(3*m))*logm-(2*z-QQ(1)/6)*m-(2*z+(l2+lp)/2+QQ(2)/3*l2-eg/6-QQ(1)/6)/m-l2/(6*m*m)+l2/2-QQ(5)/12
        # Difference from final author version (1.2), including all repairs.
        repair = -(cnew-cold)+(QQ(1)/(3*m)-(a+b)/6)*l2-QQ(2)/3*a*logm
        assert (printed+repair-closed).contains_zero()
        if m == 1:
            assert closed == 0 and assembled.contains_zero()
        else:
            C_direct += signature[int(m)]*assembled
            C_closed += signature[int(m)]*closed
            C_printed += signature[int(m)]*printed
        cone_records.append({'m':int(m), 'assembled_elliptic_log_constant_interval':iv(assembled),
                             'closed_elliptic_log_constant_interval':iv(closed),
                             'local_cone_change_interval':iv(cnew-cold),
                             'total_repair_to_author_printed_constant_interval':iv(repair)})
    simple = 15*lp+QQ(5081)/192*l2+l3-QQ(485)/64
    assert (C_closed-simple).contains_zero() and (C_direct-simple).contains_zero()
    main = ball(audit['RR_main_term_after_model_interval'])
    threshold29 = (main-joint-348)/6-simple
    baseline = (main-joint-6*simple)/12
    result = {'status':'pass','milestone':'D144','arb_precision_bits':192,
              'signature':{str(m):n for m,n in signature.items()},
              'joint_adjunction_symbolic_identity':True,'weighted_vertical_coefficient_log2':str(weighted_v/8),
              'tail_total_length_b':str(tail_length),'tail_joint_correction_coefficient_log2':str(tail_S/8),
              'tail_RR_invariance_checked':True,'anchor_intersection_on_Q_b':str(anchor_J),
              'anchor_intersection_on_minimal_regular_b':str(anchor_J+anchor_path_length),
              'ordinary_intersection_on_Q_b':str(ordinary_J),
              'known_dyadic_pair_cost_coefficient_log2':str(anchor_cost+ordinary_cost),
              'prime3_pair_cost_coefficient_log3':str(prime3_cost),'prime3_pair_inequalities':prime3_rows,
              'joint_upper_formula':'(51/2)(hL2+log2)+24(hL3+log3)+(1023/32)(hL32+log32)-(1193197/6144)log2-12log3',
              'joint_upper_stages_intervals':list(map(iv,[stage0,stage1,stage2,joint])),
              'joint_Psi_plus_I_upper_interval':iv(joint),'display_joint_upper':float(joint.center()),
              'compact_log_C_formula':'(g-1)(log(2*pi)-1/3)+(g+2)log2/3+sum((1-1/m)(log2-1)/6+log(m)/(3*m))',
              'signature_log_C_formula':'15log(pi)+(5081/192)log2+log3-485/64',
              'signature_log_C_interval':iv(simple),'display_log_C':float(simple.center()),
              'signature_author_printed_log_C_interval':iv(C_printed),'cone_and_gluing_controls':cone_records,
              'Faltings_lower_affine_baseline_interval':iv(baseline),
              'Faltings_lower_affine_formula':'hFal >= baseline_lower - average(log Zprime(1))/2',
              'sufficient_average_log_Zprime_for_Faltings29_interval':iv(threshold29),
              'display_sufficient_average_log_Zprime':float(threshold29.center()),
              'mathematical_claims_require_companion_derivations':True,
              'corrections_are_our_derivation_not_author_confirmed':True,
              'actual_curve_spectral_calculation_started':False,'Faltings_lower_29_proved':False,
              'candidate_identification_proved':False,
              'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}
    assert result['peak_rss_bytes'] < 2*(1 << 30)
    with out.open('x') as f:
        f.write(json.dumps(result,indent=2)+'\n')
    print('D144_JOINT_WORKER_PASS',flush=True)


if __name__ == '__main__':
    assert __debug__
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker',type=Path)
    args = ap.parse_args()
    if args.worker:
        worker(args.worker)
        sys.exit(0)
    tick = time.monotonic()
    output = DATA/'P1600_joint_adjunction_d144.json'
    child_path = DATA/'P1600_joint_adjunction_d144_worker.json'
    assert not output.exists() and not child_path.exists()
    env = dict(os.environ,DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH'] = str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH','')
    child = subprocess.run([str(PYTHON),str(Path(__file__).resolve()),'--worker',str(child_path)],cwd=ROOT,env=env,capture_output=True,text=True)
    assert child.returncode == 0 and 'D144_JOINT_WORKER_PASS' in child.stdout,(child.returncode,child.stdout,child.stderr)
    result = json.loads(child_path.read_text())
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    crss = max(result['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024))
    assert rss+crss < 2*(1 << 30)
    result.update({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':rss,'child_peak_rss_bytes':crss,
                   'conservative_peak_rss_bytes':rss+crss,
                   'sources':[source(p) for p in [Path(__file__),PYTHON,child_path]+[DATA/(n+'.json') for n in INPUTS]]})
    with output.open('x') as f:
        f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|606_P1600_JOINT_ADJUNCTION',flush=True)

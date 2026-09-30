"""D121 refine the certified splitting branch and every transport to P=10552.

This refines transport parameters, not harmonic moments.  Exact matrix
constants/slopes and all state/CM labels are inherited without alteration.
"""
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
s = importlib.util.spec_from_file_location('ring', ROOT/'dembele/pari/466_dyadic_prepared_transport.py')
f = importlib.util.module_from_spec(s); s.loader.exec_module(f)
FP = [2, 0, -16, 0, 20, 0, -8, 0, 1]


def valuation(a, precision):
    return min([precision]+[8*((abs(x)&-abs(x)).bit_length()-1)+i for i,x in enumerate(a) if x])


def unit_inverse(a, ring):
    assert a[0] & 1
    z = f.f.ONE
    two = ring.add(f.f.ONE, f.f.ONE)
    for _ in range((8*ring.bits-1).bit_length()):
        z = ring.mul(z, ring.add(two, ring.neg(ring.mul(a, z))))
    assert ring.mul(a, z) == f.f.ONE
    return z


def rational(a, ring, shift=0):
    result = []
    for value in a:
        q = Q(value)*(1 << shift)
        assert q.denominator & 1
        result.append(q.numerator*pow(q.denominator, -1, ring.mod) & ring.mask)
    assert len(result) == 8
    return tuple(result)


def divide_pi(a, count, ring):
    # f(b)=0 gives 2/b=-b^7+8b^5-20b^3+16b. Each step loses at
    # most one pi-digit; the caller explicitly budgets all such losses.
    for _ in range(count):
        assert not (a[0] & 1)
        half = a[0]//2
        a = tuple(((a[i+1] if i < 7 else 0)-half*FP[i+1]) & ring.mask for i in range(8))
    return a


def build():
    start = time.monotonic(); target = 10552
    old_path = DATA/'dyadic_moment_transports_refined_d115.json'
    old = json.loads(old_path.read_text())
    base_path = DATA/'definite_dyadic_certificate_d109.json'
    base = json.loads(base_path.read_text())
    rows = [c for row in old['transitions'] for c in row['children']]+old['CM_charts']
    def shift_for(row):
        dens = [Q(x).denominator for key in ('matrix_constant','matrix_slope') for a in row[key] for x in a]
        return max((d&-d).bit_length()-1 for d in dens)
    shifts = [shift_for(row) for row in rows]
    work_precision = target+8*max(shifts)+256
    assert work_precision % 8 == 0
    ring = f.Ring(work_precision//8); exported = f.Ring(target//8)
    x = rational(old['root_refinement']['new_center'], ring)
    old_x = x
    y = rational(base['Hensel']['y'], ring)
    y2plus1 = ring.add(ring.mul(y,y), f.f.ONE)
    def residual(x): return ring.add(ring.mul(x,x), y2plus1)
    derivative_valuation = 8
    root_error = valuation(residual(x), work_precision)-derivative_valuation
    assert valuation(x, work_precision) == 0
    assert root_error >= old['root_refinement']['new_error_pi'] == 352
    refinements = [root_error]
    while root_error < work_precision-8:
        res = residual(x)
        assert all(c % 2 == 0 for c in res)
        correction = ring.mul(tuple(c//2 for c in res), unit_inverse(x,ring))
        x = ring.add(x, ring.neg(correction))
        next_error = valuation(residual(x),work_precision)-8
        assert next_error >= min(work_precision-8,2*root_error-8)
        assert next_error > root_error
        root_error = next_error; refinements.append(root_error)
    assert valuation(ring.add(x,ring.neg(old_x)),work_precision) >= 352
    print('TARGET_ROOT|'+json.dumps({'work_precision_pi':work_precision,'errors_pi':refinements}),flush=True)
    certificates = []
    for index, (row, shift) in enumerate(zip(rows, shifts)):
        C = [rational(a,ring,shift) for a in row['matrix_constant']]
        S = [rational(a,ring,shift) for a in row['matrix_slope']]
        values = [ring.add(c,ring.mul(a,x)) for c,a in zip(C,S)]
        vd = valuation(values[3],work_precision)
        slope_value = min(valuation(a,work_precision) for a in S)
        computed_error = min(work_precision,root_error+slope_value)-vd
        assert computed_error >= target
        assert all(valuation(a,work_precision) >= vd for a in values)
        primitive = [divide_pi(a,vd,ring) for a in values]
        inv = unit_inverse(primitive[3],ring)
        normalized = [tuple(c & exported.mask for c in ring.mul(a,inv)) for a in primitive]
        assert normalized[3] == f.f.ONE
        delta = exported.add(normalized[0],exported.neg(exported.mul(normalized[1],normalized[2])))
        assert valuation(delta,target) == row['determinant_valuation']
        assert valuation(normalized[2],target) == min(target,row['denominator_slope_valuation'])
        assert int(valuation(normalized[1],target)==0) == row['constant_residue']
        overlap = min(valuation(exported.add(a,exported.neg(rational(b,exported))),target)
                      for a,b in zip(normalized,row['normalized_center']))
        # The exact-rational implementation uses 10^9 as v(0).  A row
        # independent of x can therefore advertise an effectively infinite
        # old error. Compare only the digits present in this quotient ring.
        assert overlap >= min(target,row['normalized_error_pi']), {'row':index, 'overlap':overlap,
            'old_error':row['normalized_error_pi'], 'denominator_valuation':vd,
            'slope_valuation':slope_value, 'new_error':computed_error}
        certificates.append({'row':index,'dyadic_common_denominator_bits':shift,
            'scaled_denominator_valuation_pi':vd,'scaled_slope_valuation_pi':slope_value,
            'computed_normalization_error_pi':computed_error,'old_center_overlap_pi':overlap})
        row['normalized_center'] = [list(map(str,a)) for a in normalized]
        row['normalized_error_pi'] = target
        if index % 75 == 0:
            print(f'TARGET_TRANSPORTS|{index+1}/399; seconds={time.monotonic()-start:.3f}',flush=True)
    assert len(certificates)==399
    old.update({'status':'pass','milestone':'D121',
        'minimum_transition_error_pi':target,'minimum_CM_chart_error_pi':target,
        'parameter_precision_pi':target,'actual_moment_precision_increased':False,
        'prior_pilot_maximum_working_precision_pi':old.pop('pilot_maximum_working_precision_pi'),
        'normalization_certificates':certificates,
        'root_refinement':{'old_error_pi':352,'new_error_pi':root_error,
            'work_ring_precision_pi':work_precision,'new_center':list(map(str,x)),
            'successive_root_error_lower_bounds_pi':refinements,
            'new_residual_lower_pi':valuation(residual(x),work_precision),
            'same_Hensel_branch_certified':True,
            'derivative_valuation_pi':derivative_valuation},
        'wall_seconds':time.monotonic()-start,
        'sources':[f.f.source(p) for p in [Path(__file__),Path(f.__file__),old_path,base_path,
            DATA/'dyadic_precision_design_d120.json']]})
    print('TARGET_TRANSPORTS_RESULT|'+json.dumps({'root_error_pi':root_error,
        'transition_count':348,'CM_chart_count':51,'parameter_precision_pi':target,
        'maximum_common_denominator_bits':max(shifts),'wall_seconds':time.monotonic()-start}),flush=True)
    return old


if __name__=='__main__':
    out=DATA/'dyadic_target_transports_d121.json';assert not out.exists()
    out.write_text(json.dumps(build(),indent=2)+'\n')
    print('PASS|471_DYADIC_TARGET_TRANSPORTS',flush=True)

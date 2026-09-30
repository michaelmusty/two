"""D120: infer norm-97 cofactor separation from the already banked Hecke data.

No Hecke operator is recomputed.  The companion proof explains why the
old/new multiplicities and the all-Hecke injection apply to canonical Y64.
"""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'


def source(p):
    p = Path(p).resolve()
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def degree(a):
    return a.bit_length()-1


def remainder(a, b):
    assert b
    while degree(a) >= degree(b):
        a ^= b << (degree(a)-degree(b))
    return a


def mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
    return result


def power(a, n, p):
    result = 1
    while n:
        if n & 1:
            result = remainder(mul(result, a), p)
        a = remainder(mul(a, a), p)
        n >>= 1
    return result


def gcd(a, b):
    while b:
        a, b = b, remainder(a, b)
    return a


def irreducible8(p):
    return degree(p) == 8 and power(2, 256, p) == 2 and gcd(power(2, 16, p)^2, p) == 1


def derivative(p):
    return sum(((p >> i) & 1) << (i-1) for i in range(1, degree(p)+1, 2))


def frobenius(h):
    d = degree(h)
    result, q = 0, 1
    for i in range(d+1):
        if (h >> i) & 1:
            result ^= q << (d-i)
        q = mul(q, 5)  # x^2+1
    return result


def coefficients(p):
    return [(p >> i) & 1 for i in range(degree(p)+1)]


def build():
    log58 = (DATA/'levelraise_p2k.out').read_text()
    log60 = (DATA/'f16_steinberg.out').read_text()
    assert 'PASS|58_levelraise_p2k' in log58 and 'PASS|60_f16_steinberg' in log60
    assert 'zz^8 + zz^4 + zz^3 + zz^2 + 1,' in log58
    assert 'zz^8 + zz^6 + zz^5 + zz + 1' in log58
    pattern = r'residual\(97\) multiplicities in cp\(T97\) at level p2\^2: \[ (\d+), (\d+) \] \(level 1: \[ (\d+), (\d+) \]\)'
    matches = re.findall(pattern, log58)
    assert matches == [('4', '4', '1', '1')]
    assert 'gen. f1(31)-space dim 8 ; joint with gen. spaces of residual(97) factors: [ 0, 8 ]' in log58
    assert 'gen. f2(31)-space dim 8 ; joint with gen. spaces of residual(97) factors: [ 8, 0 ]' in log58
    assert 'R60|new charpoly(T_p97) mod 2: [\n<zz, 40>\n]' in log60
    # D51 supplies occurrence in the p^2-new space, so m_new2 >= 1.
    # The old/new decomposition gives 4 = 3*1 + 2*m_new1 + m_new2.
    solutions = [(m1, m2) for m1 in range(3) for m2 in range(1, 5) if 4 == 3+2*m1+m2]
    assert solutions == [(0, 1)]
    traces = [sum(1 << i for i in exponents) for exponents in ([8, 4, 3, 2, 0], [8, 6, 5, 1, 0])]
    rows = []
    for target_index, h in enumerate(traces):
        assert irreducible8(h)
        psi = frobenius(h)
        assert degree(psi) == 16 and gcd(psi, derivative(psi)) == 1
        factors = [p for p in range(257, 512, 2) if remainder(psi, p) == 0 and irreducible8(p)]
        if target_index == 0:
            assert len(factors) == 2 and mul(*factors) == psi
            for p in factors:
                assert power(2, 51, p) == 1
                assert power(2, 17, p) != 1 and power(2, 3, p) != 1
            order = 51
        else:
            assert not factors
            # Rabin irreducibility for degree 16; the only prime divisor
            # of 16 is 2.  The order 257 is prime.
            assert power(2, 65536, psi) == 2
            assert gcd(power(2, 256, psi)^2, psi) == 1
            assert power(2, 257, psi) == 1 and remainder(2, psi) != 1
            factors, order = [psi], 257
        assert power(2, order, psi) == 1
        rows.append({'trace_polynomial_coefficients': coefficients(h),
                     'torsion_polynomial_coefficients': coefficients(psi),
                     'irreducible_factor_coefficients': list(map(coefficients, factors)),
                     'factor_degrees': list(map(degree, factors)),
                     'factor_root_orders': [order]*len(factors),
                     'differential_target_multiplicity_in_Y64': 1,
                     'torsion_factor_coprime_to_full_Y64_cofactor': True,
                     'kernel_dimension_over_F2_on_JY2': 16,
                     'all_nonzero_target_vectors_have_Frobenius_orbit_length': order,
                     'nonzero_vector_orbits': 65535//order})
    assert gcd(frobenius(traces[0]), frobenius(traces[1])) == 1
    result = {'status': 'pass', 'milestone': 'D120', 'prime_norm': 97,
        'input_full_level_p2_squared_trace_multiplicities': [4, 4],
        'input_level_one_trace_multiplicities': [1, 1],
        'derived_level_p_new_trace_multiplicities': [0, 0],
        'derived_level_p2_squared_new_trace_multiplicities': [1, 1],
        'independent_banked_level_p_new_polynomial_mod2': 't^40',
        'old_Y16_target_trace_multiplicities': [0, 0],
        'T31_to_T97_target_factor_indices_one_based': [2, 1],
        'targets': rows,
        'target_torsion_rational_over_residue_extension_degrees': [51, 257],
        'preferred_T97_factor_index_one_based': 1,
        'preferred_original_T31_factor_index_one_based': 2,
        'nonzero_vectors_per_target': 65535,
        'Frobenius_orbits_for_preferred_target': 1285,
        'projective_lines_over_F256_per_target': 257,
        'new_Hecke_computation_performed': False,
        'full_norm97_Euler_polynomial_computed': False,
        'Frobenius_kernel_isolation_is_local_not_a_global_Hecke_scalar_action': True,
        'canonical_Y64_identification_still_required_for_any_candidate': True,
        'genus64_extension51_torsion_backend_validated': False,
        'target_field_polynomial_constructed': False,
        'input_scope': 'Uses frozen exact Hecke logs and D51; does not independently regenerate their matrices.',
        'sources': [source(p) for p in [Path(__file__), DATA/'levelraise_p2k.out',
            DATA/'f16_steinberg.out', DATA/'curve_first_frobenius.out', ROOT/'dembele/magma/58_levelraise_p2k.m',
            ROOT/'dembele/magma/60_f16_steinberg.m', ROOT/'dembele/magma/64_curve_first_frobenius.m',
            ROOT/'dembele/certificates/target-realization.md']]}
    print('NORM97_ISOLATION|both targets simple in Y64; first split 8+8 with order 51, second irreducible with order 257', flush=True)
    return result


if __name__ == '__main__':
    out = DATA/'norm97_target_isolation_d120.json'
    assert not out.exists()
    out.write_text(json.dumps(build(), indent=2)+'\n')
    print('PASS|460_NORM97_TARGET_ISOLATION', flush=True)

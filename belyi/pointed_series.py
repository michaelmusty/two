"""Exact reference for normalizing differentials at a marked point.

Run with Sage's Python. The integral coordinate removes arbitrary formal
coordinate changes; the final weighted rescaling follows the method in
Musty--Schiavone--Sijsling--Voight, section 4.4. No Belyi map is required
by this local operation. See dembele/certificates/pointed-normalization.md.
"""
import argparse
import json
from pathlib import Path
import runpy


def echelon(forms, orders):
    from sage.all import matrix
    field = forms[0].base_ring()
    change = matrix(field, [[f[j] for f in forms] for j in orders]).inverse()
    return [sum(f*change[i, j] for i, f in enumerate(forms))
            for j in range(len(forms))]


def intrinsic_forms(forms, orders, length):
    """Use the highest-vanishing line, then re-echelonize after substitution.

    orders must be the true vanishing sequence. The numerical adapter must
    assess this separately. At least length + max(orders) input jets are
    needed, including the jets determining the coordinate change.
    """
    from sage.all import QQ
    if len(forms) != len(orders) or list(orders) != sorted(set(orders)):
        raise ValueError('one increasing vanishing order per differential is required')
    m = orders[-1]
    if min(f.prec() for f in forms) < length+m:
        raise ValueError('insufficient jets for the integral coordinate')
    h = echelon(forms, orders)
    if any(f.valuation() != a for f, a in zip(h, orders)):
        raise ValueError('the supplied orders are not the vanishing sequence')
    u = h[0].parent().gen()
    # tau^(m+1) = (m+1) integral(h_last du); choose tau = u + ... .
    unit = ((m+1)*h[-1].integral()/u**(m+1)).add_bigoh(length)
    tau = u*unit**(QQ(1)/(m+1))
    inverse = tau.reverse()
    pulled = [(f(inverse)*inverse.derivative()).add_bigoh(length) for f in h]
    return echelon(pulled, orders)


def weight_one_gauge(forms, orders):
    """Return rescaled forms and a Bezout witness, or refuse a root choice.

    A gcd greater than one does not prove failure over the base field;
    it means that this finite set of coefficients does not remove the
    remaining root ambiguity over that field.
    """
    from sage.all import xgcd
    entries = sorted((n-a, n, i) for i, a in enumerate(orders)
                     for n in range(a+1, int(forms[i].prec())) if forms[i][n])
    gcd, witness = 0, []
    for weight, n, i in entries:
        new_gcd, s, t = xgcd(gcd, weight)
        witness = [(row, col, exponent*s) for row, col, exponent in witness]
        witness.append((n, i, t))
        gcd = new_gcd
        if gcd == 1:
            break
    if gcd != 1:
        raise ValueError(f'nonzero coefficient weights have gcd {gcd}; no weight-one gauge')
    witness = [(int(n), int(i), int(e)) for n, i, e in witness if e]
    scale = forms[0].base_ring().one()
    for n, i, e in witness:
        scale *= forms[i][n]**e
    u = forms[0].parent().gen()
    return [scale**a*f(u/scale) for f, a in zip(forms, orders)], scale, witness


def q8_ordinary_forms(length):
    """The thesis Q8 curve at (x,y)=(1,sqrt(15)), with t=x-1.

    Multiplying both regular forms by sqrt(15) leaves their complex span
    unchanged and gives the rational series used here.
    """
    from sage.all import QQ, PowerSeriesRing
    ring = PowerSeriesRing(QQ, 'u', default_prec=length)
    u = ring.gen()
    h = ((16*(1+u)**5-(1+u))/15)**(QQ(-1)/2)
    return [h, u*h]


def control(length=18):
    from sage.all import QQ, PowerSeriesRing, QuadraticField, gcd, matrix
    root = Path(__file__).resolve().parents[1]
    # Reuse the workspace's exact check of the actual thesis curve.
    known = runpy.run_path(str(root/'belyi/validate_q8.sage'))
    assert known['f'] == 16*known['m']**5-known['m']
    forms = q8_ordinary_forms(length+6)
    original = intrinsic_forms(forms, [0, 1], length)
    expected, scale, witness = weight_one_gauge(original, [0, 1])
    field = QuadraticField(-1, 'I')
    I = field.gen()
    ring = PowerSeriesRing(field, 'v', default_prec=length+6)
    v = ring.gen()
    coordinate = (1+I)*v+QQ(2)/7*v**2+I/11*v**3
    change = matrix(field, [[2, I], [1, 1+I]])
    pulled = [ring(f)(coordinate)*coordinate.derivative() for f in forms]
    changed = [sum(pulled[i]*change[i, j] for i in range(2)) for j in range(2)]
    normalized, _, _ = weight_one_gauge(intrinsic_forms(changed, [0, 1], length), [0, 1])
    assert all(normalized[i] == ring(expected[i]) for i in range(2))
    # A missing differential Jacobian is a substantive, detectable error.
    wrong = [ring(f)(coordinate) for f in forms]
    wrong, _, _ = weight_one_gauge(intrinsic_forms(wrong, [0, 1], length), [0, 1])
    assert any(wrong[i] != ring(expected[i]) for i in range(2))
    # At infinity the Q8 curve has an order-eight local symmetry. Do not
    # turn an eighth-root normalization into an unsupported claim over Q.
    r = PowerSeriesRing(QQ, 't', default_prec=32)
    t = r.gen()
    h = (1-t**8/16)**(QQ(-1)/2)
    branch = intrinsic_forms([h, t**2*h], [0, 2], 26)
    weights = [n-a for f, a in zip(branch, [0, 2]) for n in range(a+1, 26) if f[n]]
    assert gcd(weights) == 8
    try:
        weight_one_gauge(branch, [0, 2])
    except ValueError as error:
        assert 'gcd 8' in str(error)
    else:
        raise AssertionError('a root ambiguity was silently accepted')
    return {'status': 'PASS: exact thesis-curve normalization controls',
            'curve': 'y^2 = 16*x^5-x', 'point': '(1,sqrt(15))',
            'point_field': 'Q(sqrt(15)); these particular normalized jets lie in Q',
            'input_reference': 'belyi/validate_q8.sage',
            'coordinate_and_basis_invariance': 'exact, including nonlinear coordinate change',
            'missing_derivative_negative_control': 'rejected',
            'intrinsic_coefficients_2_3': [str(original[0][2]), str(original[0][3])],
            'scale': str(scale), 'weight_one_witness': witness,
            'normalized_coefficients': [[str(f[n]) for n in range(length)] for f in expected],
            'infinity_vanishing_sequence': [0, 2], 'infinity_weight_gcd': 8,
            'infinity_root_ambiguity': 'refused', 'exact_output_jets': length}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = control()
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(report['status'])

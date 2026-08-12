#!/usr/bin/env sage
"""Direct Hilbert-Eisenstein evaluation on the genus-4 17T7 control point.

This is an exploratory numerical gate, not a rigorous truncation certificate.
It evaluates the normalized parallel-weight-4 Hilbert Eisenstein series

    E_4(z) = 1 + (2^n / zeta_K(-3))
                   sum_{0 << nu in d_K^-1} sigma_3((nu)d_K) q^nu

on the 17 two-isogeny neighbors.  The purpose is to test whether this much
cheaper invariant separates the neighbors and is numerically stable.
"""

from itertools import product
from math import ceil

from sage.all import (
    CC,
    ComplexField,
    NumberField,
    PolynomialRing,
    Polyhedron,
    QQ,
    RealField,
    prod,
)


BITS = 220
DECIMAL_SCALE = 10**24
KX = PolynomialRing(QQ, "x")
x = KX.gen()
K = NumberField(x**4 - 10 * x**3 + 20 * x**2 + 25 * x - 25, "a")
a = K.gen()
OK = K.ring_of_integers()
DIFFERENT = K.different()
CODIFFERENT = DIFFERENT.inverse()
CODIFFERENT_BASIS = CODIFFERENT.basis()
EMBEDDINGS = K.real_embeddings(prec=BITS)
RR = RealField(BITS)
CF = ComplexField(BITS)

# The Schottky-selected Jacobian neighbor recovered by
# dembele/magma/40_genus4_reference_point.m.  Ordering agrees with
# InfinitePlaces(H) in the pinned EichlerShimuraHMF run.
BASE_Z = [
    CF(
        "-0.1343913910670493537747196637672716808113029586903012984807190099631768117338910343636",
        "2.522414218719873141733609227356794804399970593756344000056323447122958354301940416858",
    ),
    CF(
        "0.2042093858776124360081332714418397702936411319667832870004087154537617424598988551466",
        "1.391453383469640933143498549396517451342423896738080373770970194488520007646542889952",
    ),
    CF(
        "4.250705642247650443480399642644064935405585918518809557660969727783087100492845020585",
        "0.3770790857838415972679252964500259691370382245258616118793888042187911344062768542749",
    ),
    CF(
        "10.17947636294178647428618674968136697511207590820470845381934056672632796878114715863",
        "0.7138706449424023981306712630191730398368451437161044090959919377717977597759104880565",
    ),
]
BASE_Y = [z.imag() for z in BASE_Z]

ZETA_MINUS_THREE = QQ(541) / 15
NORMALIZATION = QQ(2**K.degree()) / ZETA_MINUS_THREE


def rational_approximation(value):
    """Fixed-denominator rational approximation for Normaliz inequalities."""
    return QQ(round(RR(value) * DECIMAL_SCALE)) / DECIMAL_SCALE


EMBEDDED_BASIS = [
    [rational_approximation(place(b)) for b in CODIFFERENT_BASIS]
    for place in EMBEDDINGS
]


SIGMA_THREE_CACHE = {}


def sigma_three(ideal):
    """Return sum of cubes of norms of integral ideal divisors."""
    if ideal in SIGMA_THREE_CACHE:
        return SIGMA_THREE_CACHE[ideal]
    answer = 1
    for prime, exponent in ideal.factor():
        norm = prime.norm()
        answer *= sum(norm ** (3 * j) for j in range(exponent + 1))
    SIGMA_THREE_CACHE[ideal] = answer
    return answer


def fourier_terms(y, exponential_tolerance):
    """Enumerate terms whose bare exponential is above the tolerance."""
    cutoff = -RR(exponential_tolerance).log() / (2 * RR.pi())
    yq = [rational_approximation(v) for v in y]
    cutoff_q = rational_approximation(cutoff)

    inequalities = [[QQ(0)] + row for row in EMBEDDED_BASIS]
    upper = [cutoff_q] + [
        -sum(yq[j] * EMBEDDED_BASIS[j][i] for j in range(K.degree()))
        for i in range(K.degree())
    ]
    polytope = Polyhedron(
        ieqs=inequalities + [upper],
        base_ring=QQ,
        backend="normaliz",
    )

    terms = []
    for coordinates in polytope.integral_points():
        if not any(coordinates):
            continue
        nu = sum(
            (coordinates[i] * CODIFFERENT_BASIS[i] for i in range(K.degree())),
            K(0),
        )
        embedded = [RR(place(nu)) for place in EMBEDDINGS]
        if min(embedded) <= 0:
            continue
        decay = sum(embedded[i] * y[i] for i in range(K.degree()))
        if decay > cutoff:
            continue

        ideal = K.fractional_ideal(nu) * DIFFERENT
        if not ideal.is_integral():
            raise AssertionError("(nu) times the different is not integral")
        terms.append((embedded, sigma_three(ideal)))
    return terms


def eisenstein_value(z, terms):
    """Evaluate the truncated normalized E_4 expansion."""
    value = CF(1)
    for embedded, coefficient in terms:
        exponent = 2 * CF.pi() * CF.gen() * sum(
            CF(embedded[i]) * z[i] for i in range(K.degree())
        )
        value += CF(NORMALIZATION * coefficient) * exponent.exp()
    return value


def residue_representatives_mod_two():
    """Represent O_K/(2) using the integral basis."""
    basis = OK.basis()
    return [
        sum((bits[i] * basis[i] for i in range(K.degree())), K(0))
        for bits in product((0, 1), repeat=K.degree())
    ]


def isogeny_roots(exponential_tolerance):
    """Evaluate the direct Eisenstein invariant on all 17 neighbors."""
    base_terms = fourier_terms(BASE_Y, exponential_tolerance)
    half_y = [y / 2 for y in BASE_Y]
    half_terms = fourier_terms(half_y, exponential_tolerance)
    double_y = [2 * y for y in BASE_Y]
    double_terms = fourier_terms(double_y, exponential_tolerance)

    base_value = eisenstein_value(BASE_Z, base_terms)
    roots = []
    for residue in residue_representatives_mod_two():
        residue_embeddings = [CF(place(residue)) for place in EMBEDDINGS]
        neighbor = [
            (BASE_Z[i] + residue_embeddings[i]) / 2
            for i in range(K.degree())
        ]
        roots.append(eisenstein_value(neighbor, half_terms) / base_value)

    # For diag(2,1), the inverse automorphy factor is Norm(2)^4 = 2^16.
    roots.append(
        CF(2**16)
        * eisenstein_value([2 * z for z in BASE_Z], double_terms)
        / base_value
    )
    return roots, (len(base_terms), len(half_terms), len(double_terms))


def nearest_root_error(left, right):
    """Hausdorff-style matching error for two unordered root sets."""
    return max(min(abs(a - b) for b in right) for a in left)


def polynomial_from_roots(roots):
    ring = PolynomialRing(CF, "T")
    T = ring.gen()
    return prod(T - root for root in roots)


def main():
    coarse_roots, coarse_counts = isogeny_roots(RR("1e-18"))
    fine_roots, fine_counts = isogeny_roots(RR("1e-22"))

    separation = min(
        abs(fine_roots[i] - fine_roots[j])
        for i in range(len(fine_roots))
        for j in range(i)
    )
    stability = nearest_root_error(coarse_roots, fine_roots)
    coarse_polynomial = polynomial_from_roots(coarse_roots)
    fine_polynomial = polynomial_from_roots(fine_roots)
    coefficient_stability = max(
        abs(a - b)
        for a, b in zip(coarse_polynomial, fine_polynomial)
    )
    max_coefficient_imaginary_part = max(
        abs(coefficient.imag()) for coefficient in fine_polynomial
    )

    print(f"RESULT|zeta_K_minus_3|{ZETA_MINUS_THREE}")
    print(f"RESULT|normalization|{NORMALIZATION}")
    print("RESULT|coarse_term_counts|" + "|".join(map(str, coarse_counts)))
    print("RESULT|fine_term_counts|" + "|".join(map(str, fine_counts)))
    print(f"RESULT|min_root_separation|{separation}")
    print(f"RESULT|coarse_fine_root_error|{stability}")
    print(f"RESULT|max_root_absolute_value|{max(map(abs, fine_roots))}")
    print(f"RESULT|max_coefficient_absolute_value|{max(map(abs, fine_polynomial))}")
    print(f"RESULT|max_coefficient_imaginary_part|{max_coefficient_imaginary_part}")
    print(f"RESULT|coarse_fine_coefficient_error|{coefficient_stability}")

    if len(fine_roots) != 17:
        raise AssertionError("expected 17 isogeny roots")
    if separation <= 100 * stability:
        raise AssertionError("the direct Eisenstein invariant is not stably separating")
    print("PASS|hilbert_eisenstein_genus4")


if __name__ == "__main__":
    main()

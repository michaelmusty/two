# Milestone 2: cyclic / superelliptic 2-group Belyi maps (the "trivial square root"
# base case of the tower).  A C_N cover of P^1 branched at {0,1,oo} (N = 2^n) is a
# Kummer extension  y^N = c * x^a * (x-1)^b,  ramified only over {0,1,oo}.  As a tower
# it is iterated square roots of a single radicand: y = f^{1/N}, i.e.
#   z_1^2 = f,  z_2^2 = z_1, ..., z_n^2 = z_{n-1},  f = c*x^a*(x-1)^b.
# Local ramification orders:
#   over 0 : N / gcd(N, a)     over 1 : N / gcd(N, b)     over oo : N / gcd(N, a+b).
from sage.all import FunctionField, PolynomialRing, gcd, Infinity

def cyclic_absolute(k, n, a, b, c=1, var='y'):
    """Absolute model of the C_{2^n} Belyi map y^{2^n} = c*x^a*(x-1)^b over k."""
    N = 2**n
    K = FunctionField(k, 'x'); x = K.gen()
    R = PolynomialRing(K, 'Y'); Y = R.gen()
    f = k(c) * x**a * (x - 1)**b
    L = K.extension(Y**N - f, var)
    return L, x, f

def cyclic_passport(n, a, b):
    N = 2**n
    return (N // gcd(N, a), N // gcd(N, b), N // gcd(N, a + b))

def cyclic_radicand_tower(n, a, b, c=1):
    """The radicand sequence (bottom-up) realizing y^{2^n}=c*x^a*(x-1)^b as
    n successive square roots.  Returned symbolically for provenance/tests."""
    # f_0 = c*x^a*(x-1)^b, then each further level is sqrt of the previous generator.
    return ["%s * x^%d * (x-1)^%d" % (c, a, b)] + ["sqrt(prev level generator)"] * (n - 1)

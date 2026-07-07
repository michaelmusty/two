# Milestone 3 (part 1): compose a square-root step into an ABSOLUTE model.
#
# Current curve X_i has function field K = F_p(x)[y]/(P(x,y)), degree m.  Adjoining
# z = sqrt(f) for f = f(x,y) in K gives X_{i+1} with absolute minimal polynomial over
# F_p(x)  Q(x,z) = Res_y( P(x,y),  z^2 - f(x,y) ) = prod_{P(y_j)=0} (z^2 - f(x,y_j)),
# a degree-2m polynomial in z (the norm form).  We return its squarefree primitive
# part and, on request, the Sage function field F_p(x)[z]/(Q).
from sage.all import PolynomialRing, FunctionField, FractionField

def compose_sqrt(base, P_y, f_y):
    """base = F_p(x) (a rational function field or fraction field of F_p[x]);
    P_y, f_y are univariate polynomials in 'y' over base.  Return Q in base[z],
    the (squarefree) minimal polynomial of z = sqrt(f) over base."""
    Ryz = PolynomialRing(base, ['yy', 'zz'])
    yy, zz = Ryz.gens()
    Pyz = P_y.subs({P_y.parent().gen(): yy})
    fyz = f_y.subs({f_y.parent().gen(): yy})
    res = (zz**2 - fyz).resultant(Pyz, yy)          # eliminate y -> polynomial in zz
    Rz = PolynomialRing(base, 'z'); z = Rz.gen()
    Q = res.univariate_polynomial()(z) if hasattr(res, 'univariate_polynomial') \
        else Rz(res)
    # squarefree radical (drop repeated factors from the norm form): Q / gcd(Q, Q').
    Q = Q / Q.leading_coefficient()
    g = Q.gcd(Q.derivative())
    Qsf = Q // g
    return Qsf / Qsf.leading_coefficient()

def tower_field(p, radicands):
    """Build a tower F_p(x) ⊂ K_1 ⊂ ... by successive sqrt steps.
    radicands[0] is a polynomial in y0 over F_p(x) with y0 a dummy (level-0 field is
    F_p(x) itself, so radicands[0] should be an element of F_p(x) as a constant poly).
    Each later radicand is given as a poly in the previous generator.
    Returns (L_abs, x) the final absolute function field and base gen.  (Helper for
    cyclic sanity checks; the group-driven radicands come in build.sage.)"""
    raise NotImplementedError  # exercised via explicit calls in tests for now

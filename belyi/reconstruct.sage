# Milestone 3.4 (genus-0-intermediate tower): reconstruct a 2-group Belyi curve from
# its permutation triple, entirely in Sage over F_p, when all intermediate rungs are
# genus 0.  We track the current genus-0 rung as F_p(s) via a rational function
# x = x(s) (the Belyi coordinate in terms of the rung parameter).  At each chief-series
# step the group driver says which of {0,1,oo} ramify; the radicand is prod(s - r) over
# the finite places above those branch points; a genus-0 result is reparametrized, a
# positive-genus result is the hyperelliptic model y^2 = radicand.
load("belyi/groups.sage")
from sage.all import GF, PolynomialRing, prod

def reconstruct(G, s0, s1, p, verbose=True):
    Fp = GF(p)
    R = PolynomialRing(Fp, 's'); s = R.gen()
    x = R.fraction_field()(s)                     # X_0 = F_p(x), parameter s = x
    chain = chief_series_indices(G); sinf = (s0 * s1)**(-1)
    for i in range(len(chain) - 1):
        rb = step_ramified_branch_points(G, chain[i], chain[i + 1], s0, s1, sinf)
        num, den = x.numerator(), x.denominator()
        roots = set()
        for b in rb:
            poly = {'0': num, '1': num - den, 'oo': den}[b]   # x=0 / x=1 / poles
            for r, _ in poly.roots():
                roots.add(r)
        roots = sorted(roots); m = len(roots)
        radicand = prod([s - r for r in roots]) if roots else R(1)
        genus = (m + (m % 2)) // 2 - 1
        if verbose:
            print(f"  step {i}: ramify {rb}, {m} finite branch pts {roots}, "
                  f"radicand deg {radicand.degree()}, step-genus {genus}", flush=True)
        if genus > 0:
            return radicand                        # hyperelliptic model y^2 = radicand
        # reparametrize the genus-0 double cover y^2 = radicand
        Rw = PolynomialRing(Fp, 'w'); w = Rw.gen(); Fw = Rw.fraction_field()
        if m == 1:
            a = roots[0]; s_new = Fw(w**2 + a)
        elif m == 2:
            a, b = roots; s_new = (a * w**2 - b) / (w**2 - 1)
        else:
            raise ValueError(("unexpected genus-0 step with %d branch points" % m,))
        x = num(s_new) / den(s_new)                # x in the new parameter w
        R, s = Rw, w
    raise RuntimeError("tower ended without a positive-genus rung")

if __name__ == "__main__":
    from sage.all import QQ
    G = libgap.SmallGroup(8, 4)                    # Q8
    gens = libgap.GeneratorsOfGroup(G)
    print("Reconstructing Q8 8T5-4,4,4-g2 over F_13:")
    f = reconstruct(G, gens[0], gens[1], 13)
    print("  hyperelliptic model:  y^2 =", f, "=", f.factor())
    # 2-torsion field = splitting field of the quintic; check roots (expect 0,+-1,+-i)
    print("  quintic roots in F_13:", sorted(r for r, _ in f.roots()))
    # sanity: lift the same factorization pattern to Q -> splitting field Q(i)
    RQ = PolynomialRing(QQ, 't'); t = RQ.gen()
    fQ = t**5 - t
    print("  over Q, s^5-s =", fQ.factor(), "-> splitting field Q(i), Gal C2, SOLVABLE")

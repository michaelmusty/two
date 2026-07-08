# EXPERIMENT: can we avoid the class group by finding the radicand in the F_2-span of
# the known tower functions {x, x-1, y_1, ..., y_i} (parities at the S-places)?
# Tests the smallest nonabelian positive-genus-intermediate case C8:C2 = [16,6],
# genera [0,0,0,1,3].  We track the tower via parametrization through the genus-0
# rungs (carrying x, x-1, and the generators y_j as rational functions of the current
# parameter), then at the first positive-genus rung (X_3, genus 1) we BUILD X_3 and
# check if the target ramification parity R lies in the span of the known functions.
load("belyi/groups.sage")
from sage.all import GF, PolynomialRing, FunctionField, prod, matrix, vector, Infinity

def run(order, gid, p, quo=0, verbose=True):
    Fp = GF(p)
    G = libgap.SmallGroup(order, gid); gens = libgap.GeneratorsOfGroup(libgap.FreeGroup(2))
    F2free = libgap.FreeGroup(2); fg = libgap.GeneratorsOfGroup(F2free)
    h = libgap.GQuotients(F2free, G)[quo]
    s0 = libgap.Image(h, fg[0]); s1 = libgap.Image(h, fg[1]); sinf = (s0*s1)**(-1)
    chain = chief_series_indices(G)

    R = PolynomialRing(Fp, 's'); s = R.gen()
    x = R.fraction_field()(s)
    funcs = {'x': x, 'x-1': x - 1}          # known functions of current parameter
    ngen = 0
    for i in range(len(chain) - 1):
        rb = step_ramified_branch_points(G, chain[i], chain[i+1], s0, s1, sinf)
        num, den = x.numerator(), x.denominator()
        roots = set()
        for b in rb:
            poly = {'0': num, '1': num - den, 'oo': den}[b]
            for r, _ in poly.roots():
                roots.add(r)
        roots = sorted(roots); m = len(roots)
        radicand = prod([s - r for r in roots]) if roots else R(1)
        genus = (m + (m % 2)) // 2 - 1
        if verbose:
            print(f"step {i}->{i+1}: ramify {rb}, radicand deg {radicand.degree()}, "
                  f"X_{i+1} step-genus {genus}", flush=True)
        if genus > 0:
            # X_{i+1} is positive genus: BUILD it and test the radicand for the NEXT
            # step (i+1 -> i+2), which is the one that actually lives on a positive-genus
            # curve.  X_{i+1} = F_p(s)[v]/(v^2 - radicand(s)); funcs (x, x-1, y_j) live in
            # F_p(s) = base, and v = y_{i+1} is the new generator.
            return span_test_pg(Fp, G, chain, i, s0, s1, sinf, x, funcs, radicand, s)
        # reparametrize genus-0 double cover; carry all known funcs + add new generator
        Rw = PolynomialRing(Fp, 'w'); w = Rw.gen(); Fw = Rw.fraction_field()
        if m == 1:
            a = roots[0]; s_new = Fw(w**2 + a); v_new = Fw(w)
        else:
            a, b = roots; s_new = (a*w**2 - b)/(w**2 - 1); v_new = (a - b)*w/(w**2 - 1)
        x = num(s_new) / den(s_new)
        newfuncs = {k: (g.numerator()(s_new) / g.denominator()(s_new)) for k, g in funcs.items()}
        ngen += 1; newfuncs[f'y{ngen}'] = v_new     # generator y_{i+1} = sqrt(radicand)
        funcs = newfuncs
        R, s = Rw, w
    print("tower finished without a positive-genus rung")

def span_test_pg(Fp, G, chain, i, s0, s1, sinf, x_expr, funcs, radicand, s):
    # Build the positive-genus curve X = X_{i+1} = F_p(s)[v]/(v^2 - radicand(s)).
    Ks = FunctionField(Fp, 's'); sv = Ks.gen()
    def toKs(rat):
        return Ks(rat.numerator()(sv)) / Ks(rat.denominator()(sv))
    Rv = PolynomialRing(Ks, 'V'); V = Rv.gen()
    rho = Ks(radicand(sv))
    X = Ks.extension(V**2 - rho, 'v'); v = X.gen()
    print(f"\n  built X_{i+1} = F_p(s)[v]/(v^2 - radicand),  genus = {X.genus()}")
    # known functions on X: x, x-1, the y_j (all from F_p(s)) and v = y_{i+1}
    known = {k: X(toKs(g)) for k, g in funcs.items()}
    known[f'y{i+1}'] = v
    x_on_X = X(toKs(x_expr))
    # the NEXT step's ramified branch points (i+1 -> i+2)
    rb_next = step_ramified_branch_points(G, chain[i+1], chain[i+2], s0, s1, sinf)
    print(f"  next step {i+1}->{i+2} ramifies over {rb_next}")
    # S-places of X over x = 0, 1, oo  (x here = x_on_X, a function on X)
    def places_over(b):
        if b == 'oo':
            return list(x_on_X.poles())
        val = Fp(0 if b == '0' else 1)
        return list((x_on_X - val).zeros())
    Splaces = []
    for b in ['0', '1', 'oo']:
        Splaces += list(places_over(b))
    # target divisor R = all places over the ramifying branch points (all-or-nothing)
    target_places = set()
    for b in rb_next:
        for P in places_over(b):
            target_places.add(P)
    def parity(g):
        return vector(GF(2), [ (g.valuation(P)) % 2 for P in Splaces ])
    target = vector(GF(2), [ (1 if P in target_places else 0) for P in Splaces ])
    print(f"  #S-places = {len(Splaces)};  target R parity = {list(target)}")
    keys = list(known.keys())
    rows = []
    for k in keys:
        pv = parity(known[k]); rows.append(pv)
        print(f"  parity[{k:4s}] = {list(pv)}")
    M = matrix(GF(2), rows)
    try:
        sol = M.solve_left(target)
        combo = [keys[j] for j in range(len(keys)) if sol[j] == 1]
        print(f"\n  RESULT: R IS in span => radicand ~ product of {combo}, NO class group needed")
        return True
    except ValueError:
        print(f"\n  RESULT: R NOT in span of known tower functions => CLASS GROUP element NEEDED")
        return False

def span_test(Fp, x, funcs, radicand, rb, level):
    # The needed radicand lives on the CURRENT curve X_i = F_p(s) (genus 0 here, but the
    # NEXT curve X_{i+1} is positive genus).  We test whether `radicand`'s parity vector
    # (at the S-places over x=0,1,oo) is in the F_2-span of the known functions' parities.
    s = radicand.parent().gen()
    def mult(poly, P):
        c = 0; q = poly
        while q != 0 and q(P) == 0:
            q = q // (s - P); c += 1
        return c
    xnum, xden = x.numerator(), x.denominator()
    Splaces = set()
    for poly in [xnum, xnum - xden, xden]:
        for r, _ in poly.roots():
            Splaces.add(r)
    Splaces = sorted(Splaces) + ['oo']
    Rpoly = s.parent()
    def par(gexpr):
        n = Rpoly(gexpr.numerator()); d = Rpoly(gexpr.denominator())
        row = []
        for P in Splaces:
            v = (d.degree() - n.degree()) if P == 'oo' else (mult(n, P) - mult(d, P))
            row.append(v % 2)
        return vector(GF(2), row)
    target = par(radicand)
    keys = list(funcs.keys())
    M = matrix(GF(2), [list(par(funcs[k])) for k in keys])
    print(f"\n  S-places (s-values over 0,1,oo): {Splaces}")
    print(f"  target R parity      : {list(target)}")
    for k in keys:
        print(f"  parity[{k:4s}]         : {list(par(funcs[k]))}")
    # is target in the row span of M?
    try:
        sol = M.solve_left(target)
        combo = [keys[j] for j in range(len(keys)) if sol[j] == 1]
        print(f"\n  RESULT: R IS in span. radicand ~ product of {combo}  =>  NO class group needed here")
        return True
    except ValueError:
        print(f"\n  RESULT: R NOT in span of known tower functions  =>  class group element NEEDED")
        return False

def gfp(d, pp):
    S = sum((d - d//e) for e in pp); return 1 + (S - 2*d)//2

def find_cases(order):
    """All nonabelian triples of this order with a positive-genus intermediate rung
    whose first genus jump leaves at least one more step to test."""
    Fr = libgap.FreeGroup(2); fg = libgap.GeneratorsOfGroup(Fr)
    out = []
    n = int(libgap.NrSmallGroups(order))
    for i in range(1, n+1):
        G = libgap.SmallGroup(order, i)
        if bool(libgap.IsAbelian(G)): continue
        for qi, h in enumerate(libgap.GQuotients(Fr, G)):
            s0 = libgap.Image(h, fg[0]); s1 = libgap.Image(h, fg[1])
            chain = chief_series_indices(G)
            genera = [gfp(int(libgap.Index(G, chain[j])),
                          level_passport(G, s0, s1, chain[j])) for j in range(len(chain))]
            # first intermediate rung with positive genus, and a further step exists
            for j in range(1, len(chain)-2):
                if genera[j] > 0:
                    out.append((order, i, qi, str(libgap.StructureDescription(G)), genera)); break
    return out

if __name__ == "__main__":
    npass = nfail = 0
    for order in [16, 32]:
        cases = find_cases(order)
        seen = set()
        for (o, gid, qi, struct, genera) in cases:
            key = (o, gid)
            if key in seen: continue        # one triple per group for the survey
            seen.add(key)
            print(f"\n######## order {o} G=[{o},{gid}] {struct} genera {genera} ########")
            try:
                r = run(o, gid, 13, quo=qi, verbose=False)
                if r is True: npass += 1
                elif r is False: nfail += 1
            except Exception as e:
                print("  (skipped:", str(e)[:60], ")")
    print(f"\n==== span trick: {npass} pass (no class group), {nfail} FAIL (class group needed) ====")

# The recognition step reduces to: given a q0-adic approximation of an algebraic
# number of degree d and height H, how much precision M does LLL need to recover
# its minimal polynomial?  That relation does not depend on how the
# approximation was produced, so it can be measured without the period pipeline.
q0 = 2003
print("q0 = %d ; entries below are the minimal M (q0-adic digits) for recovery" % q0)
print("deg  log10(H)   M_needed   M/(d*log_q0(H))")
set_random_seed(1)
R.<x> = QQ[]
for d in [2, 4, 8, 16]:
    for hexp in [5, 10, 20]:
        H = 10^hexp
        # a monic irreducible of degree d with coefficients of size ~H
        while True:
            f = x^d + sum(ZZ.random_element(-H, H)*x^i for i in range(d))
            if f.is_irreducible():
                break
        K = Qp(q0, 400)
        rts = f.roots(K)
        if not rts:
            print("  deg %d h1e%d: no q0-adic root, skipped" % (d, hexp))
            continue
        alpha = rts[0][0]
        found = None
        for M in range(4, 400, 4):
            a = Qp(q0, M)(alpha)
            g = algdep(a, d)
            if g is not None and g.degree() == d and (g/g.leading_coefficient() == f or g == f or g == -f):
                found = M
                break
        pred = d*hexp/log(q0,10)
        print("  %-4d %-10d %-10s %.2f" % (d, hexp, found, (found/pred) if found else float('nan')))

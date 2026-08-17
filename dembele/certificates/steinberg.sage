# Does the U_q eigenvalue stay RATIONAL for a Steinberg newform whose Hecke
# field is bigger than Q?  This is what decides whether the lift's central
# normalisation (scale = ZZ(Tq_eigenvalue(p))^-1) survives for a component with
# eigenvalues in a degree-16 field.
print("level  dim  Hecke field        a_q (q || N, Steinberg)   other a_ell")
for N in [43, 61, 67, 73, 97, 109]:
    if not is_prime(N):
        continue
    for f in Newforms(N, 2, names='a'):
        K = f.hecke_eigenvalue_field()
        aq = f[N]                      # U_q eigenvalue, q = N || N
        others = [f[l] for l in [2,3,5] if N % l != 0][:2]
        rational = aq in QQ
        print("%5d  %3d  %-18s %-24s %s   %s" % (
            N, K.degree(), K.defining_polynomial() if K.degree()>1 else "Q",
            "%s  (rational: %s)" % (aq, rational), others,
            "<== a_q rational, field is not" if rational and K.degree()>1 else ""))

# Root discriminant of L = the degree-257 field cut out by the projective
# representation, and what it forces.
#
# Inertia at 2: wild inertia sits in the 2-Sylow of SL_2(F_256), the unipotent
# subgroup U = {[[1,b],[0,1]]} of order 256.  On P^1(F_256) = 257 points, U
# fixes infinity and acts on the affine line by translation x -> x + b, i.e.
# SIMPLY TRANSITIVELY.  So the orbits are {oo} and one orbit of size 256:
# one unramified prime, and one prime with e = 256, f = 1.
n_L_F  = 257
n_F    = 8
n_L    = n_L_F * n_F
e      = 256
# different exponent for a wildly ramified prime: d <= e-1 + v_p(e)*e
d_max  = (e - 1) + valuation(e, 2) * e
v2_disc_LF = d_max                      # one prime, f = 1
v2_disc_F  = 31                         # disc(F) = 2^31
v2_disc_L  = v2_disc_LF + v2_disc_F * n_L_F     # tower formula
rd = RR(2)^(RR(v2_disc_L)/n_L)
print("[L:Q] = %d" % n_L)
print("worst-case different exponent at the wild prime: d <= %d" % d_max)
print("v_2(disc L/Q) <= %d + %d*%d = %d" % (v2_disc_LF, v2_disc_F, n_L_F, v2_disc_L))
print("root discriminant rd(L) <= %.2f" % rd)
print()
print("Odlyzko asymptotic lower bounds:  totally real >= ~60.8 ; totally imaginary >= ~22.3")
print("  => L totally real is IMPOSSIBLE (%.1f < 60.8): E has complex places," % rd)
print("     i.e. complex conjugation acts nontrivially (as a unipotent involution).")
print("  => consistent with totally imaginary (%.1f > 22.3)." % rd)

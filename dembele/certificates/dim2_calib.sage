# Dimension-2 end-to-end calibration, step 1: get the 2-dimensional cocycle and
# lift it overconvergently.  Times each stage and reports the precision.
import time
from darmonpoints.sarithgroup import BigArithGroup
from darmonpoints.cohomology_arithmetic import ArithCoh, get_twodim_cocycle, get_overconvergent_class_quaternionic

prec = 20
p, level = 5, 33
t0 = time.time()
G = BigArithGroup(p, (1,1), level, base=QQ, grouptype='PSL2', magma=magma)
print("STAGE group: %.1f s" % (time.time()-t0))

t0 = time.time()
Coh = ArithCoh(G)
print("STAGE cohomology: %.1f s   dimension = %s" % (time.time()-t0, Coh.dimension()))

t0 = time.time()
(f0, f1), hecke_data = get_twodim_cocycle(Coh, 1)
print("STAGE twodim cocycle: %.1f s" % (time.time()-t0))
print("  hecke_data ells: %s" % [ell for ell, _ in hecke_data])
for ell, T0 in hecke_data:
    print("  T_%s charpoly = %s  irreducible=%s" % (ell, T0.charpoly().factor(), T0.charpoly().is_irreducible()))

t0 = time.time()
Phi0 = get_overconvergent_class_quaternionic(p, f0, G, prec, 1, 1)
el = time.time()-t0
print("STAGE overconvergent lift f0: %.1f s  (prec=%d)" % (el, prec))
t0 = time.time()
Phi1 = get_overconvergent_class_quaternionic(p, f1, G, prec, 1, 1)
print("STAGE overconvergent lift f1: %.1f s" % (time.time()-t0))
print("LIFT_OK")

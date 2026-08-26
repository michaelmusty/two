from sage.all import *
import sys
sys.path.insert(0,'dembele/tests')
load('dembele/tests/hilbert_eisenstein_genus4.sage')
D = 725; n = 4
Ny = prod(BASE_Y)
tol = RR("1e-22"); C = -tol.log()/(2*RR.pi())
print("C =", C, " N(y) =", Ny, " sqrtD/N(y) =", sqrt(D)/Ny)
for name, y, obs in [("base", BASE_Y, 5007), ("half", [v/2 for v in BASE_Y], 80286), ("double", [2*v for v in BASE_Y], 315)]:
    pred = sqrt(RR(D))*C**n/(factorial(n)*prod(y))
    terms = fourier_terms(y, tol)
    tmin = min(sum(e[i]*y[i] for i in range(n)) for e,_ in terms)
    amgm = n*(prod(y)/sqrt(RR(D)))**(1/n)
    print(f"{name}: predicted {pred:.0f} observed {obs} enumerated {len(terms)}  min trace {tmin:.4f}  AM-GM floor {amgm:.4f}  ratio rho {tmin/amgm:.3f}  C/tmin {C/tmin:.2f}")
# dimension constants
for m in [4,8,16]:
    print(f"n={m}: n^n/n! = {RR(m)**m/factorial(m):.3e}")
# zeta_H(-3) estimate via functional equation: zeta(1-k) = D^(k-1/2) (2 (k-1)!/(2 pi)^k)^n zeta(k), k=4
def zeta_est(Dv, m):
    return RR(Dv)**RR(3.5) * (2*6/(2*RR.pi())**4)**m
print("zeta est H8:", zeta_est(11015140625, 8), " exact 1.7326e18")
print("zeta est K725:", zeta_est(725, 4), " exact", 541/15.)
DH = 51536621539079846122207574462890625
print("zeta est H:", zeta_est(DH, 16), " log10:", log(zeta_est(DH,16),10))
print("sqrt DH:", sqrt(RR(DH)))
print("normalization 2^16/zeta_H(-3) ~", 2**16/zeta_est(DH,16))
c16 = RR(16)**16/factorial(16)
for t in [1.25,1.5,2,3,4.7]:
    print(f"t={t}: count >= {c16*RR(t)**16:.2e}")

from sage.all import *
x = polygen(QQ)
H8 = NumberField(x^8+218*x^7+18263*x^6+714011*x^5+11517840*x^4-12312339*x^3-1919681667*x^2-6177513277*x+26601321401, 'c')
print("disc", H8.discriminant().factor(), float(sqrt(abs(H8.discriminant()))))
print("signature", H8.signature())
print("primes above 2:", [(P.residue_class_degree(), P.ramification_index()) for P in H8.primes_above(2)])
print("class group", H8.class_group().invariants(), "narrow", H8.narrow_class_group().invariants())
print("different norm", H8.different().norm())
# a nicer defining polynomial
print("polredabs", pari(H8.polynomial()).polredabs())
# zeta_{H8}(-3) via PARI lfun
L = pari(H8).lfuncreate()
val = L.lfun(-3, precision=200)
print("zeta(-3) approx", val)
print("bestappr", pari(val).bestappr(10**30))
# genus-4 control field: minimal trace ratio check
K = NumberField(x^4-10*x^3+20*x^2+25*x-25,'a')
print("K disc", K.discriminant(), "zeta_K(-3)", pari(K).lfuncreate().lfun(-3, precision=100).bestappr(10**10))

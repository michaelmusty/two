# Heights read off Bosman Table 1 (arXiv:0710.1237): (weight k, prime ell),
# degree ell+1, largest |coefficient|.
data = [ (12,11,12,341), (12,13,14,2561), (12,17,18,211803), (12,19,20,47443),
         (16,17,18,1315239), (16,19,20,6555150), (16,23,24,397878081),
         (18,17,18,184016925), (18,19,20,2205335301), (18,23,24,237109280887),
         (20,19,20,588303992), (20,23,24,1139040818642),
         (22,23,24,2786655204876088) ]
print("  k  ell  deg   log10(maxcoeff)")
pts = []
for k, l, n, c in data:
    print("  %-3d %-4d %-5d %.1f" % (k, l, n, log(c,10)))
    pts.append((n, log(c,10).n()))
# fit log10 H = a*n + b  (least squares)
import numpy as np
ns = np.array([p[0] for p in pts]); hs = np.array([float(p[1]) for p in pts])
a, b = np.polyfit(ns, hs, 1)
print("\nlinear fit: log10 H = %.3f * n + %.2f" % (a, b))
print("  extrapolated to n = 257:  log10 H = %.0f" % (a*257+b))
# structural model: log10 H ~ n*log10(2) + (n/2)*log10|alpha|
import math
alphas = [(h - n*math.log10(2))/(n/2) for n, h in zip(ns, hs)]
amean = sum(alphas)/len(alphas)
print("\nstructural model log10 H = n*log10(2) + (n/2)*log10|alpha|")
print("  implied log10|alpha| per row, mean = %.3f  (|alpha| ~ %.2f)" % (amean, 10**amean))
print("  extrapolated to n = 257:  log10 H = %.0f" % (257*math.log10(2) + 128.5*amean))
for H in [130, 195]:
    M = 0.7*H
    print("  log10 H = %3d -> M ~ %3d -> kernel cost x%.0f vs M=20" % (H, M, (M/20)**3))

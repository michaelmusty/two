# Narrow the kernel constant.  The inner loop is v_new[j] = sum_k A_k v_old[T[j][k]].
# For FIXED k this is one (M x M) by (M x positions) multiply -- flint territory.
# Measure that, then extrapolate to the real shape.
import time
q0, positions_real, cosets_real = 2003, 58*2112, 2112
print("M    chunk    one (MxM)x(Mxchunk) multiply    -> per-iteration      -> 16 classes, M iters")
for M in [20, 40, 100]:
    N = q0^M
    bits = N.nbits()
    chunk = 4000
    A = random_matrix(ZZ, M, M, x=0, y=N)
    V = random_matrix(ZZ, M, chunk, x=0, y=N)
    t0 = time.time(); C = A*V; el = time.time()-t0
    # per-iteration: cosets multiplies, each over positions/chunk chunks
    per_iter = el * cosets_real * (positions_real/chunk)
    total16 = per_iter * M * 16 / 3600
    print("%-4d %-8d %-30s %-20s %.0f core-hours (entry %d bits)" % (
        M, chunk, "%.3f s" % el, "%.0f s" % per_iter, total16, bits))

# The gate-4 cost is (positions) x (cosets) x (cost of one moment-vector
# operation).  Measure that last factor honestly at the q0 we would actually
# use, then extrapolate.
import time
for p, M in [(2003, 20), (2003, 40), (11, 20)]:
    R = Zp(p, M)
    a = vector(R, [R.random_element() for _ in range(M)])
    b = vector(R, [R.random_element() for _ in range(M)])
    c = R(3)
    N = 20000
    t0 = time.time()
    for _ in range(N):
        a = a + c * b            # the inner operation: scale-and-accumulate
    el = (time.time() - t0) / N
    print("p=%-6d M=%-3d  per moment-vector op: %.2f us" % (p, M, el*1e6))
    positions = 58 * (p + 1) if p > 100 else 58 * (p + 1)
    cosets = p + 1
    iters = 20
    total = positions * cosets * iters * el
    print("        one class, %d positions x %d cosets x %d iters -> %.1f core-hours"
          % (positions, cosets, iters, total/3600))
    print("        sixteen classes -> %.1f core-hours" % (16*total/3600))

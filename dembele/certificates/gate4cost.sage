# Two couplings that decide where effort is worth spending:
#  (a) gate-4 cost vs Nq0 -- positions ~ 58(Nq0+1) AND cosets ~ Nq0+1, so ~Nq0^2
#  (b) gate-4 cost vs precision M -- moments ~M and Up iterations ~M, so ~M^2
# Calibrated on the measured 5.3 us per moment-vector op at M=20.
base_us = 5.3e-6
def cost_hours(Nq0, M):
    positions = 58*(Nq0+1); cosets = Nq0+1; iters = M
    per_op = base_us * (M/20.0)
    return positions*cosets*iters*per_op/3600.0
print("gate-4 inner loop, ONE class (x16 classes, but they run in parallel)")
print("  Nq0     M=20      M=60       M=100      recognizable height")
for Nq0 in [257, 1103, 2111, 5003, 20011]:
    row = "  %-7d" % Nq0
    for M in [20, 60, 100]:
        row += "%-10.1f" % cost_hours(Nq0, M)
    # q0-adic precision Nq0^M; recognizing h in Q(sqrt2) needs ~H^2 -> H ~ Nq0^(M/2)
    H = RR(Nq0)**(100/2)
    row += " 10^%d at M=100" % RR(log(H,10))
    print(row)

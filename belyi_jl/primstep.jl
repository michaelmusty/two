using Pkg; Pkg.activate(@__DIR__); using Hecke
k = GF(13); kt, x = rational_function_field(k, "x")

# ---- F1 = k(x)[t]/(t^2 - x),  primitive element theta1 = y1 = sqrt(x) ----
R1, T1 = polynomial_ring(kt, "t1")
F1, th1 = function_field(T1^2 - x, "th1")
println("F1 built, genus ", genus(F1), "  [F1:k(x)] = ", degree(F1))

# radicand for the next step lives in F1.  Take rad = x-1  (an element of F1)
rad = F1(x - 1)

# express rad in the power basis {1, th1} of F1 over k(x): coordinates
co = coordinates(rad)                 # vector of length degree(F1) over kt
println("coordinates(rad) = ", co, "   (so R(t) = ", co[1], " + ", co[2], "*t )")

# minpoly of theta2 = th1 + y2, y2^2 = rad, by eliminating t from
#   m1(t) = t^2 - x   and   (TH - t)^2 - R(t)
# Work in kt[TH][t]; R(t) = co[1] + co[2]*t
Rth, TH = polynomial_ring(kt, "TH")
Rt,  t  = polynomial_ring(Rth, "t")
m1  = t^2 - Rth(x)
Rpoly = Rth(co[1]) + Rth(co[2]) * t     # R(t) with TH-free coeffs
p2  = (TH - t)^2 - Rpoly
m2  = resultant(m1, p2)                 # in Rth = kt[TH]
println("minpoly(theta2) deg = ", degree(m2), "  = ", m2)

# ---- F2 = k(x)[TH]/(m2) : absolute model, degree 4 ----
R2, TT = polynomial_ring(kt, "TT")
m2u = R2(collect(coefficients(m2)))     # coerce m2 into univariate ring R2
F2, th2 = function_field(m2u, "th2")
println("F2 built, genus ", genus(F2), "  [F2:k(x)] = ", degree(F2))

# ---- recover th1 as an element of F2 via gcd over F2[t] ----
RF, tf = polynomial_ring(F2, "tf")
g = gcd(tf^2 - F2(x), (th2 - tf)^2 - (F2(x) - F2(1)))   # rad=x-1 here
println("gcd over F2[t] (should be linear) = ", g)
th1_in_F2 = -constant_coefficient(g) // leading_coefficient(g)
y1 = th1_in_F2
y2 = th2 - th1_in_F2
println("y1^2 == x ?      ", y1^2 == F2(x))
println("y2^2 == x-1 ?    ", y2^2 == F2(x - 1))

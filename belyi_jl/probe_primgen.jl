using Pkg; Pkg.activate(@__DIR__); using Hecke
k = GF(13); kt, x = rational_function_field(k, "x")
# Absolute model of the biquadratic field F_p(x)(sqrt x, sqrt(x-1)) via a primitive element.
# theta = y1 + y2 with y1^2=x, y2^2=x-1.  minpoly(theta) = (t^2-(2x-1))^2 - 4x(x-1) ... build by resultant.
ky, y = polynomial_ring(kt, "y")
# step1: L1 = k(x)[y1]/(y1^2 - x)
# step2 absolute: resultant_{y1}( y1^2 - x , (t - y1)^2 - (x-1) ) gives minpoly of theta=y1+y2 over k(x)
kt2, t = polynomial_ring(kt, "t")
R2, (Y1,) = polynomial_ring(kt, ["Y1"])
# do the resultant in a poly ring where t is a param:  work in kt[t][Y1]
Ktt, tt = rational_function_field(k, "T")   # treat theta as transcendental to get minpoly
# simpler: use Nemo resultant over kt[Y1] with coefficients involving t as a second var
Ruv, (u, w) = polynomial_ring(kt, ["u", "w"])   # u=y1, w=theta
p1 = u^2 - kt_to(x, kt, Ruv)   # placeholder

# Decisive probe: does Hecke give the FULL Pic^0 (divisor class group of the smooth
# projective curve) for a function field over F_p?  Test curve z^4 = x(x-1) over F_7,
# genus 1, where |Pic^0(F_7)| = 8 (Sage's class_group gave only the affine order 1).
using Pkg; Pkg.activate(@__DIR__)
using Hecke

k = GF(7)
kt, x = rational_function_field(k, "x")
ky, y = polynomial_ring(kt, "y")
F, a = function_field(y^4 - x*(x-1), "a")
println("genus = ", genus(F))

# class group of the (finite) maximal order + the infinite places -> full Pic^0?
try
    OF = maximal_order(F)
    Cl, mCl = class_group(OF)
    println("finite class_group(maximal_order) = ", Cl)
catch e
    println("class_group(maximal_order) error: ", e)
end

# Hecke divisor / Picard machinery for function fields?
println("\nHecke names containing 'divisor'/'class'/'picard':")
for n in names(Hecke; all=false)
    s = String(n)
    if occursin(r"(?i)divisor|class_group|picard|riemann", s)
        println("  ", s)
    end
end

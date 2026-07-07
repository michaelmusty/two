using Pkg; Pkg.activate(@__DIR__)
using Hecke
k = GF(7)
kt, x = rational_function_field(k, "x")
ky, y = polynomial_ring(kt, "y")
F, a = function_field(y^4 - x*(x-1), "a")
Ofin = finite_maximal_order(F); Oinf = infinite_maximal_order(F)

# try picard_group and divisor-class-group style calls
for expr in ["picard_group(Ofin)", "picard_group(F)",
             "class_group(Ofin)", "class_group(Ofin, Oinf)"]
    try
        r = eval(Meta.parse(expr)); println(expr, " => ", r)
    catch e
        println(expr, " ERR ", first(sprint(showerror, e), 70))
    end
end

# build a divisor of a function and inspect the Divisor API
D = divisor(a)                    # principal divisor of the generator a
println("\ndivisor(a) type: ", typeof(D))
println("Divisor operations:")
for n in names(Hecke; all=true)
    s = String(n)
    if occursin(r"(?i)^(is_principal|principal|class_of|class_group|divisor_class)", s)
        println("  ", s)
    end
end
# what methods act on a Divisor?
println("\nfunctions accepting Divisor:")
for fn in [:is_principal, :is_effective, :dimension, :degree, :riemann_roch_space, :support]
    try
        applicable(getfield(Hecke, fn), D) && println("  ", fn, " applicable")
    catch; end
end

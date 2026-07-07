using Pkg; Pkg.activate(@__DIR__)
using Hecke
k = GF(7)
kt, x = rational_function_field(k, "x")
ky, y = polynomial_ring(kt, "y")
F, a = function_field(y^4 - x*(x-1), "a")
println("genus = ", genus(F))

for fn in [:finite_maximal_order, :infinite_maximal_order, :maximal_order]
    try
        O = getfield(Hecke, fn)(F)
        println(fn, " => ", typeof(O))
    catch e
        println(fn, " ERR ", typeof(e))
    end
end

# divisor class group of the function field?
for expr in ["class_group(F)", "divisor_class_group(F)"]
    try
        r = eval(Meta.parse(expr))
        println(expr, " => ", r)
    catch e
        println(expr, " ERR ", sprint(showerror, e)[1:min(end,80)])
    end
end

# methods of class_group applicable to function fields
println("\nmethods(class_group):")
for m in methods(class_group); println("  ", m); end

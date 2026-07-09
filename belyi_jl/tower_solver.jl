using Pkg; Pkg.activate(@__DIR__); using Hecke
import JSON
include("radicand.jl")

# ---------- primitive-element extension:  Fnew = F(sqrt(rad)) as an absolute model ----------
# returns (Fnew, theta_old_in_Fnew, y_new_in_Fnew); gen(Fnew) is the new primitive element.
function extend(F, rad, kt)
    co = coordinates(rad)                     # rad in power basis of theta=gen(F), coeffs in kt
    m  = defining_polynomial(F)               # minpoly of theta over kt
    Rth, TH = polynomial_ring(kt, "TH")
    Rt,  t  = polynomial_ring(Rth, "t")
    mt = sum(Rth(coeff(m, j)) * t^j for j in 0:degree(m))
    Rt_rad = sum(Rth(co[j]) * t^(j-1) for j in 1:length(co))
    mnew = resultant(mt, (TH - t)^2 - Rt_rad)     # minpoly(theta + sqrt rad) over kt
    R2, TT = polynomial_ring(kt, "TT")
    mnew_u = sum(coeff(mnew, j) * TT^j for j in 0:degree(mnew))
    Fnew, thnew = function_field(mnew_u, "th")
    # recover theta as element of Fnew via gcd over Fnew[t]
    RF, tf = polynomial_ring(Fnew, "tf")
    mF   = sum(Fnew(coeff(m, j)) * tf^j for j in 0:degree(m))
    radF = sum(Fnew(co[j]) * tf^(j-1) for j in 1:length(co))
    g = gcd(mF, (thnew - tf)^2 - radF)            # linear:  tf - theta_old
    @assert degree(g) == 1 "recovery gcd not linear (deg $(degree(g)))"
    theta_old = -constant_coefficient(g) // leading_coefficient(g)
    return Fnew, theta_old, thnew - theta_old
end

# remap an element given by its power-basis coords (in kt) into Fnew via theta_old
remap(coordsvec, theta_old, Fnew) =
    sum(Fnew(coordsvec[j]) * theta_old^(j-1) for j in 1:length(coordsvec))

# places over a branch point b in {"0","1","oo"} on F, with x = xF
function places_over(F, xF, b)
    D = b == "oo" ? pole_divisor(xF) : zero_divisor(xF - (b == "0" ? 0 : 1))
    return [P for (P, _) in support(D)]
end

parity(g, Splaces) = [ Int(valuation(Hecke.divisor(g), P)) % 2 for P in Splaces ]

function solve_tower(data)
    p = 13; k = GF(p); kt, x = rational_function_field(k, "x")
    steps = data["steps"]
    # ----- step 0: rad0 = x^[0]*(x-1)^[1]; build F1 -----
    r0 = steps[1]["ramify"]
    R1, T1 = polynomial_ring(kt, "t")
    rad0 = (("0" in r0) ? x : one(kt)) * (("1" in r0) ? (x-1) : one(kt))
    F, th = function_field(T1^2 - rad0, "y1")
    xF = F(x)
    gens = Dict{String,Any}("x"=>F(x), "x-1"=>F(x-1), "y1"=>th)
    order = ["x","x-1","y1"]
    CHECK = haskey(ENV,"CHECK_GENUS"); DEBUG = haskey(ENV,"DEBUG")
    println("step 0: ramify $r0  rad0=$rad0  -> genus (want ", steps[1]["genus_after"], ")",
            CHECK ? " [built $(genus(F))]" : "")
    CHECK && @assert genus(F) == steps[1]["genus_after"]
    # ----- steps 1.. -----
    for i in 2:length(steps)
        ram = steps[i]["ramify"]; want = steps[i]["genus_after"]
        pl = Dict(b => places_over(F, xF, b) for b in ["0","1","oo"])
        Splaces = collect(Iterators.flatten(values(pl)))
        target = [ any(P in pl[b] for b in ram) ? 1 : 0 for P in Splaces ]
        if DEBUG
            tags = [ (P in pl["0"] ? "0" : P in pl["1"] ? "1" : "oo") for P in Splaces ]
            println("   S-place branches: ", tags, "  degrees ", [Int(degree(P)) for P in Splaces])
            println("   target          : ", target)
            for nm in order; println("   parity[$nm] = ", parity(gens[nm], Splaces)); end
        end
        rows = [ parity(gens[nm], Splaces) for nm in order ]
        M = matrix(GF(2), reduce(vcat, [permutedims(r) for r in rows]))
        tvec = matrix(GF(2), permutedims(target))
        local sol
        insp = try; sol = solve(M, tvec; side=:left); true; catch; false; end
        if haskey(ENV,"STOP_PG") && steps[i]["genus_before"] > 0
            combo = insp ? [order[j] for j in 1:length(order) if !iszero(sol[j])] : String[]
            println("PGRUNG step $(i-1)  base-genus $(steps[i]["genus_before"])  ramify $ram  : ",
                    insp ? "SPAN-PASS ~ $combo" : "SPAN-FAIL (positive-genus base!)")
            return insp ? :span_pg : :spanfail_pg
        end
        target_places = [P for P in Splaces if any(P in pl[b] for b in ram)]
        if insp
            combo = [order[j] for j in 1:length(order) if !iszero(sol[j])]
            radi = prod(gens[nm] for nm in combo)
            println("step $(i-1): ramify $ram  radicand ~ ", combo, "  (SPAN: no solver needed)")
        else
            g0 = genus(F)
            radi, D = find_radicand_rr(F, target_places, Splaces)
            radi === nothing && (println("step $(i-1): RR solver found no half-divisor on S-places (genuine Pic[2] obstruction?)"); return :obstruction)
            lbl = g0 == 0 ? "Riemann-Roch on genus-0 base (rational param; no torsion)" : "Riemann-Roch + Pic^0 halving (base genus $g0)"
            println("step $(i-1): ramify $ram  span INSUFFICIENT -> $lbl")
        end
        if haskey(ENV,"MAXSTEP") && (i-1) >= parse(Int, ENV["MAXSTEP"])
            println("MAXSTEP reached at step $(i-1); stopping (verdict captured)"); return :maxstep
        end
        # coords of everything BEFORE extending
        cds = Dict(nm => coordinates(gens[nm]) for nm in order)
        Fnew, theta_old, ynew = extend(F, radi, kt)
        F = Fnew; xF = remap(cds["x"], theta_old, F)
        for nm in order; gens[nm] = remap(cds[nm], theta_old, F); end
        newname = "y$(i)"; gens[newname] = ynew; push!(order, newname)
        if CHECK
            g = genus(F)
            println("            built X_$(i): genus $g (want $want)  ", g == want ? "OK" : "*** MISMATCH ***")
            @assert g == want
        else
            println("            built X_$(i): (predicted genus $want)")
        end
    end
    println("TOWER COMPLETE through predicted genus ", steps[end]["genus_after"])
    return :complete
end

data = JSON.parsefile(ARGS[1])
println("### ", data["struct"], "  genera ", data["genera"], " ###")
solve_tower(data)

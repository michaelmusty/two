"""Checked D65 adaptation; keep the pinned and D63 entry points callable."""
from lifttors_lift import adapt_lift, replace_once


def adapt_rows(text):
    signature = "GEN PicLiftTors(GEN J, GEN W, long eini, GEN l)"
    # The D63 generator already preserves the original function and workers.
    retained = replace_once(adapt_lift(text), signature,
                            signature.replace("PicLiftTors", "PicLiftTors_D63"))
    _, body = text.split(signature)
    native = signature + body
    eager = "for(i=1;i<=d0;i++) gel(V0,i) = DivMul(FqM_FqC_mul(V,gel(U0,i),T,pefin2),V,T,pefin2);"
    native = replace_once(native, "GEN sW,Vs,U0,V0;", "GEN sW,Vs,U0;")
    native = replace_once(native, "\tV0 = cgetg(d0+1,t_VEC);\n\t" + eager,
                          "\t/* Row generation needs no vector of product matrices. */")
    start = "  \tK = cgetg(nGW*d0+2,t_MAT);"
    stop = "KM = matkerpadic(K,T,pe21,p,e21);"
    if native.count(start) != 1 or native.count(stop) != 1:
        raise ValueError("Lifting-system boundaries changed")
    before, rest = native.split(start)
    _, after = rest.split(stop)
    native = before + """  \t/* Generate rows, solve selected equations, replay all equations. */
        KM = LiftRowsMatker(V,U0,uv,AinvB,CAinv,rho,T,pe21,p,e21);""" + after
    # K belonged only to the removed queue; chart workers still use the queue.
    native = replace_once(native, "GEN K,U,U2;", "GEN U,U2;")
    native = replace_once(native, "GEN randseed,vFixedParams,args,worker,done;",
                          "GEN randseed,vFixedParams,worker,done;")
    declaration = "GEN LiftRowsMatker(GEN,GEN,GEN,GEN,GEN,GEN,GEN,GEN,GEN,long);\n"
    return retained + "\n" + declaration + native

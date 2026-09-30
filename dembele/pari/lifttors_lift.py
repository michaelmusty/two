"""Apply checked, local memory adaptations to the pinned LiftTors lift.c.

The upstream lift stays callable as PicLiftTors_original. The new worker
forms one product matrix on demand and discards it before returning its
derivative column. No lifting equations or precision steps are removed.
"""


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f"LiftTors source changed; review adaptation: {old!r}")
    return text.replace(old, new)


def adapt_lift(text, batched_kernel=True):
    signature = "GEN PicLiftTors(GEN J, GEN W, long eini, GEN l)"
    if text.count(signature) != 1:
        raise ValueError("LiftTors entry point changed")
    prefix, body = text.split(signature)
    original = signature.replace("PicLiftTors", "PicLiftTors_original") + body
    # Optional diagnostics leave the original algorithm intact.
    eager = "for(i=1;i<=d0;i++) gel(V0,i) = DivMul(FqM_FqC_mul(V,gel(U0,i),T,pefin2),V,T,pefin2);"
    original = replace_once(original, eager, """for(i=1;i<=d0;i++) {
        gel(V0,i) = DivMul(FqM_FqC_mul(V,gel(U0,i),T,pefin2),V,T,pefin2);
        if (getenv("LIFTTORS_TRACE") && (i==1 || i%16==0 || i==d0)) {
            pari_printf("TRACE|eager_v0|count=%lu|stack_bytes=%lu\\n",i,(ulong)(av-avma));
            pari_flush();
        }
    }""")
    adapted = signature + body
    adapted = replace_once(adapted, "GEN sW,Vs,U0,V0;", "GEN sW,Vs,U0;")
    adapted = replace_once(adapted, "\tV0 = cgetg(d0+1,t_VEC);\n\t" + eager,
                           "\t/* Product matrices are formed inside the worker, one at a time. */")
    adapted = replace_once(adapted, "vFixedParams = cgetg(6,t_VEC);", "vFixedParams = cgetg(7,t_VEC);")
    adapted = replace_once(adapted, "gel(vFixedParams,5) = pe21;", "gel(vFixedParams,5) = pe21;\n\t\tgel(vFixedParams,6) = V;")
    adapted = replace_once(adapted, 'is_entry("PicLift_worker")', 'is_entry("PicLift_worker_streamed")')
    adapted = replace_once(adapted, "gel(args,1) = gel(V0,j);", "gel(args,1) = gel(U0,j);")
    adapted = replace_once(adapted, "if(done) gel(K,workid) = done;", """if(done) {
                gel(K,workid) = done;
                if (getenv("LIFTTORS_TRACE") && (workid==1 || workid%16==0)) {
                    pari_printf("TRACE|lift_column|index=%ld|stack_bytes=%lu\\n",workid,(ulong)(av-avma));
                    pari_flush();
                }
            }""")
    adapted = replace_once(adapted, "KM = matkerpadic(K,T,pe21,p,e21);", """if (getenv("LIFTTORS_TRACE")) {
            pari_printf("TRACE|lift_system|rows=%ld|columns=%ld|stack_bytes=%lu\\n",
                        lg(gel(K,1))-1,lg(K)-1,(ulong)(av-avma));
            pari_flush();
        }
        KM = matkerpadic(K,T,pe21,p,e21);""")
    if batched_kernel:
        adapted = replace_once(adapted, "KM = matkerpadic(K,T,pe21,p,e21);",
                               "KM = LiftMatker_batched(K,T,pe21,p,e21);")
        prefix += "GEN LiftMatker_batched(GEN, GEN, GEN, GEN, long);\n"
    return prefix + original + "\n" + adapted

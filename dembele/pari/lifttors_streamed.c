/* Memory-only adaptation of the pinned LiftTors lifting worker.
 * The derivative is the original PicLift_worker applied to the same
 * product matrix modulo the required p^e. Its temporary product is
 * reclaimed before the derivative column is returned to the queue.
 */
#include "linalg.h"
#include "pic.h"

GEN PicLift_worker(GEN V0j, ulong shift, GEN uv, GEN AinvB,
                   GEN CAinv, GEN T, GEN pe21);

GEN PicLift_worker_streamed(GEN U0j, ulong shift, GEN uv, GEN AinvB,
                            GEN CAinv, GEN T, GEN pe21, GEN V)
{
    pari_sp av = avma;
    GEN product = DivMul(FqM_FqC_mul(V,U0j,T,pe21),V,T,pe21);
    GEN column = PicLift_worker(product,shift,uv,AinvB,CAinv,T,pe21);
    return gerepilecopy(av,column);
}

/* A shallow row slice; the input matrix stays alive throughout the call. */
static GEN lift_rows(GEN matrix, long first, long last)
{
    long i, j, columns = lg(matrix), rows = last-first+1;
    GEN block = cgetg(columns,t_MAT);
    for (j=1;j<columns;j++) {
        gel(block,j)=cgetg(rows+1,t_COL);
        for (i=0;i<rows;i++) gcoeff(block,i+1,j)=gcoeff(matrix,first+i,j);
    }
    return block;
}

/* Same kernel as matkerpadic on its stated domain (good reduction).
 * Select a complete row basis mod p, retaining original coefficients.
 * Check every row, and at higher precision verify K*L=0 in batches.
 * Peak temporary storage depends on the column count, not all rows.
 */
GEN LiftMatker_batched(GEN K, GEN T, GEN pe, GEN p, long e)
{
    pari_sp av=avma, scratch;
    const long batch=256;
    long rows, first, last;
    GEN R, L, block, residual;
    if (lg(K)==1) return cgetg(1,t_MAT);
    rows=lg(gel(K,1))-1;
    if (!rows) return matid(lg(K)-1);
    last=rows<batch ? rows : batch;
    R=FqM_image(gtrans(lift_rows(K,1,last)),T,p);
    if (lg(R)==1) {
        R=zeromat(0,lg(K)-1);
        L=matid(lg(K)-1);
    } else {
        R=gtrans(R);
        L=matkerpadic(R,T,pe,p,e);
    }
    gerepileall(av,2,&R,&L);
    for (first=last+1;first<=rows && lg(L)>1;first+=batch) {
        scratch=avma;
        last=first+batch-1; if (last>rows) last=rows;
        block=lift_rows(K,first,last);
        residual=FqM_mul(block,L,T,p);
        if (!gequal0(residual)) {
            R=gtrans(FqM_image(gtrans(vconcat(R,block)),T,p));
            L=matkerpadic(R,T,pe,p,e);
            gerepileall(av,2,&R,&L);
        } else avma=scratch;
    }
    if (getenv("LIFTTORS_TRACE")) {
        pari_printf("TRACE|lift_kernel_basis|rank=%ld|nullity=%ld|rows=%ld\n",
                    lg(K)-lg(L),lg(L)-1,rows);
        pari_flush();
    }
    /* At e=1 the row-basis pass already proves this over the field.
     * At e>1 this explicitly checks matkerpadic's good-reduction premise. */
    if (e>1 && lg(L)>1) {
        for (first=1;first<=rows;first+=batch) {
            scratch=avma;
            last=first+batch-1; if (last>rows) last=rows;
            residual=FqM_mul(lift_rows(K,first,last),L,T,pe);
            if (!gequal0(residual))
                pari_err(e_MISC,"Lifting linear system does not have good reduction");
            avma=scratch;
        }
    }
    return gerepilecopy(av,L);
}

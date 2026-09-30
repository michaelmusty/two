/* Exact batched replacement for LiftTors's DivSub_dimval.
 *
 * Select a full row basis modulo p, retaining its ORIGINAL coefficients
 * modulo p^e. Lift its kernel, then test EVERY original equation modulo
 * p^e, one block at a time. No random equation is omitted. This computes
 * the same rank/valuation criterion without stacking O(g) large blocks.
 * The upstream implementation remains available as DivSub_dimval_original.
 */
#include "linalg.h"

static GEN constraint_block(GEN WA, long n, GEN KB, GEN T, GEN pe)
{
    long j, k, columns = lg(KB), rows = lg(gel(KB,1));
    GEN block = cgetg(columns,t_MAT);
    for (j=1;j<columns;j++) {
        gel(block,j)=cgetg(rows,t_COL);
        for (k=1;k<rows;k++)
            gcoeff(block,k,j)=Fq_mul(gcoeff(WA,j,n),gcoeff(KB,k,j),T,pe);
    }
    return block;
}

ulong DivSub_dimval(GEN WA, GEN WB, long dim, GEN KV,
                   GEN T, GEN p, long e, GEN pe)
{
    pari_sp av=avma, keep, scratch;
    GEN KB, R, L, block, residual;
    long n, val;
    ulong answer=(ulong)e;
    KB=mateqnpadic(WB,T,pe,p,e);
    keep=avma;
    R=gcopy(KV);
    L=matkerpadic(R,T,pe,p,e);
    for (n=1;n<lg(WA);n++) {
        if (lg(L)==1) break;
        scratch=avma;
        block=constraint_block(WA,n,KB,T,pe);
        residual=FqM_mul(block,L,T,p);
        if (!gequal0(residual)) {
            /* FqM_image selects independent original columns, as also
             * used by upstream DivAdd. It does not reduce them mod p. */
            R=gtrans(FqM_image(gtrans(vconcat(R,block)),T,p));
            L=matkerpadic(R,T,pe,p,e);
            gerepileall(keep,2,&R,&L);
        } else avma=scratch;
    }
    if (lg(L)-1!=dim) { avma=av; return 0; }
    residual=FqM_mul(KV,L,T,pe);
    if (!gequal0(residual)) answer=(ulong)gvaluation(residual,p);
    for (n=1;n<lg(WA);n++) {
        scratch=avma;
        block=constraint_block(WA,n,KB,T,pe);
        residual=FqM_mul(block,L,T,pe);
        if (!gequal0(residual)) {
            val=gvaluation(residual,p);
            if ((ulong)val<answer) answer=(ulong)val;
        }
        avma=scratch;
    }
    avma=av;
    return answer;
}

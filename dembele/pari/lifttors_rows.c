/* D65: generate Schur-complement equations in row blocks, never a full K.
 * This is a storage adaptation of Mascot's pinned PicLift_worker.
 * See lifttors-extension.md for the identity and its GP comparison.
 */
#include "linalg.h"
#include "pic.h"

static GEN row_pol(GEN value, GEN T)
{
    return typ(value)==t_POL ? value : scalarpol(value,varn(T));
}

/* Cache S=V*U0 and H_i=V*N_i; N scatters [-A^-1 B;Id] to original rows. */
GEN LiftRowsPrepare(GEN V, GEN U0, GEN uv, GEN AinvB, GEN T, GEN pe)
{
    pari_sp av=avma, scratch;
    GEN P=gmael(uv,2,1), Pc=gmael(uv,2,2), S, H, N;
    long nV=lg(V)-1, b=lg(Pc)-1, r=lg(P)-1, groups, i,j,k,offset;
    if (nV<=0 || (r+b)%nV)
        pari_err(e_MISC,"Invalid lifting column partition");
    groups=(r+b)/nV;
    S=FqM_mul(V,U0,T,pe);
    H=cgetg(groups+1,t_VEC);
    for (i=1;i<=groups;i++) {
        scratch=avma;
        offset=(i-1)*nV;
        N=cgetg(b+1,t_MAT);
        for (k=1;k<=b;k++) {
            gel(N,k)=cgetg(nV+1,t_COL);
            for (j=1;j<=nV;j++) gcoeff(N,j,k)=pol_0(varn(T));
            for (j=1;j<=r;j++)
                if (P[j]>offset && P[j]<=offset+nV)
                    gcoeff(N,P[j]-offset,k)=row_pol(Fq_neg(gcoeff(AinvB,j,k),T,pe),T);
            if (Pc[k]>offset && Pc[k]<=offset+nV)
                gcoeff(N,Pc[k]-offset,k)=pol_1(varn(T));
        }
        gel(H,i)=gerepilecopy(scratch,FqM_mul(V,N,T,pe));
    }
    return gerepilecopy(av,mkvec2(S,H));
}

static GEN row_scaled_subset(GEN S, GEN h, GEN indices, GEN T, GEN pe)
{
    long i,j,m=lg(indices)-1,n=lg(S)-1;
    GEN B=cgetg(n+1,t_MAT);
    for (j=1;j<=n;j++) {
        gel(B,j)=cgetg(m+1,t_COL);
        for (i=1;i<=m;i++)
            gcoeff(B,i,j)=row_pol(Fq_mul(gel(h,indices[i]),gcoeff(S,indices[i],j),T,pe),T);
    }
    return B;
}

/* Original K row (j-1)*b+k appears as row j in this block.
 * Each entry is a polynomial, including constants, for matkerpadic.
 */
GEN LiftRowsBlock(GEN cache, GEN uv, GEN CAinv, GEN rho, long k, GEN T, GEN pe)
{
    pari_sp av=avma, scratch;
    GEN S=gel(cache,1),H=gel(cache,2),I=gmael(uv,1,1),Ic=gmael(uv,1,2);
    GEN block,left,right,h;
    long groups=lg(H)-1,d0=lg(S)-1,m=lg(Ic)-1,i,j,s;
    if (k<1 || k>=lg(rho)) pari_err(e_MISC,"Invalid lifting row-block index");
    block=cgetg(groups*d0+2,t_MAT);
    for (i=1;i<=groups;i++) {
        scratch=avma;
        h=gmael(H,i,k);
        left=row_scaled_subset(S,h,Ic,T,pe);
        right=FqM_mul(CAinv,row_scaled_subset(S,h,I,T,pe),T,pe);
        for (j=1;j<=d0;j++) for (s=1;s<=m;s++)
            gcoeff(left,s,j)=row_pol(Fq_sub(gcoeff(left,s,j),gcoeff(right,s,j),T,pe),T);
        left=gerepilecopy(scratch,left);
        for (j=1;j<=d0;j++) gel(block,(i-1)*d0+j)=gel(left,j);
    }
    gel(block,groups*d0+1)=cgetg(m+1,t_COL);
    for (s=1;s<=m;s++)
        gcoeff(block,s,groups*d0+1)=row_pol(Fq_red(gcoeff(rho,s,k),T,pe),T);
    return gerepilecopy(av,block);
}

typedef GEN (*row_generator)(void *, long);

/* Selected rows are original equations, not reduced or transformed rows.
 * A unit pivot minor gives a free kernel; replaying every equation at pe
 * proves equality with the full kernel. Rank drop raises the D63 error.
 */
static GEN kernel_generated(void *context, row_generator generate,
                            long blocks, long rows, long columns,
                            GEN T, GEN pe, GEN p, long e)
{
    pari_sp av=avma,scratch;
    GEN R=zeromat(0,columns),L=matid(columns),B,residual,selected;
    long k,max_block_bytes=0,bytes,scanned=0,replayed=0;
    ulong checkpoint=0,used;
    int trace=getenv("LIFTTORS_TRACE")!=NULL;
    pari_timer timer;
    walltimer_start(&timer);
    for (k=1;k<=blocks && lg(L)>1;k++) {
        scratch=avma;
        B=generate(context,k);
        if (trace) {
            bytes=gsizebyte(B); if(bytes>max_block_bytes) max_block_bytes=bytes;
        }
        residual=FqM_mul(B,L,T,p);
        scanned++;
        if (!gequal0(residual)) {
            selected=FqM_image(gtrans(vconcat(R,B)),T,p);
            R=gtrans(selected);
            L=matkerpadic(R,T,pe,p,e);
            used=(ulong)(av-avma); if(used>checkpoint) checkpoint=used;
            gerepileall(av,2,&R,&L);
        } else {
            used=(ulong)(av-avma); if(used>checkpoint) checkpoint=used;
            avma=scratch;
        }
    }
    /* Also replay at e=1: the saved trace then records an explicit check.
     * A zero kernel needs no replay; its unit full-rank minor is decisive. */
    if (lg(L)>1) for (k=1;k<=blocks;k++) {
        scratch=avma;
        B=generate(context,k);
        if (trace) {
            bytes=gsizebyte(B); if(bytes>max_block_bytes) max_block_bytes=bytes;
        }
        residual=FqM_mul(B,L,T,pe);
        if (!gequal0(residual))
            pari_err(e_MISC,"Lifting linear system does not have good reduction");
        replayed++;
        used=(ulong)(av-avma); if(used>checkpoint) checkpoint=used;
        avma=scratch;
    }
    if (trace) {
        pari_printf("TRACE|row_kernel|rows=%ld|columns=%ld|blocks=%ld|rank=%ld|nullity=%ld|scanned=%ld|replayed=%ld|maximum_block_bytes=%ld|selected_row_bytes=%ld|kernel_bytes=%ld|stack_checkpoint_bytes=%lu|ms=%ld\n",
                    rows,columns,blocks,columns-lg(L)+1,lg(L)-1,scanned,replayed,
                    max_block_bytes,gsizebyte(R),gsizebyte(L),checkpoint,walltimer_delay(&timer));
        pari_flush();
    }
    return gerepilecopy(av,L);
}

struct row_context { GEN cache,uv,CAinv,rho,T,pe; };

static GEN generated_block(void *context, long k)
{
    struct row_context *c=(struct row_context *)context;
    return LiftRowsBlock(c->cache,c->uv,c->CAinv,c->rho,k,c->T,c->pe);
}

GEN LiftRowsKernel(GEN cache, GEN uv, GEN CAinv, GEN rho,
                   GEN T, GEN pe, GEN p, long e)
{
    struct row_context context={cache,uv,CAinv,rho,T,pe};
    long blocks=lg(rho)-1,rows=(lg(gmael(uv,1,2))-1)*blocks;
    long columns=(lg(gel(cache,1))-1)*(lg(gel(cache,2))-1)+1;
    return kernel_generated(&context,generated_block,blocks,rows,columns,T,pe,p,e);
}

GEN LiftRowsMatker(GEN V, GEN U0, GEN uv, GEN AinvB, GEN CAinv,
                   GEN rho, GEN T, GEN pe, GEN p, long e)
{
    pari_sp av=avma;
    GEN cache=LiftRowsPrepare(V,U0,uv,AinvB,T,pe),L;
    if (getenv("LIFTTORS_TRACE")) {
        pari_printf("TRACE|row_setup|cache_bytes=%ld|stack_bytes=%lu\n",
                    gsizebyte(cache),(ulong)(av-avma));
        pari_flush();
    }
    L=LiftRowsKernel(cache,uv,CAinv,rho,T,pe,p,e);
    return gerepilecopy(av,L);
}

/* Test entry point: the same streaming solver with caller-supplied blocks.
 * Production uses generated_block and never constructs this vector. */
static GEN stored_block(void *context, long k) { return gel((GEN)context,k); }

GEN LiftMatker_blocks(GEN blocks, GEN T, GEN pe, GEN p, long e)
{
    long i,n,rows=0;
    if (typ(blocks)!=t_VEC || lg(blocks)<2)
        pari_err(e_MISC,"Expected at least one equation block");
    n=lg(gel(blocks,1))-1;
    if (n<1) pari_err(e_MISC,"Expected at least one equation column");
    for(i=1;i<lg(blocks);i++) {
        if(typ(gel(blocks,i))!=t_MAT || lg(gel(blocks,i))!=n+1)
            pari_err(e_MISC,"Inconsistent equation block columns");
        rows+=lg(gmael(blocks,i,1))-1;
    }
    return kernel_generated((void *)blocks,stored_block,lg(blocks)-1,rows,n,T,pe,p,e);
}

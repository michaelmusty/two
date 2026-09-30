/* D122 exact truncated polynomial products over (Z/2^bits)[b]/f(b).
 * Degree-seven coefficient polynomials are evaluated at 0,...,14.
 * FLINT performs the fifteen scalar polynomial products. Integer Newton
 * interpolation uses eleven guard bits, as independently proved in D121.
 */
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <gmp.h>
#include <flint/flint.h>
#include <flint/fmpz.h>
#include <flint/fmpz_mod.h>
#include <flint/fmpz_mod_poly.h>

static const long FP[8]={2,0,-16,0,20,0,-8,0};

int dembele_poly_mul(unsigned char *out,const unsigned char *aa,
                    const unsigned char *bb,long na,long nb,long length,
                    unsigned long bits)
{
    if(na<1 || nb<1 || length<1 || length>na+nb-1 || bits<1 || bits>16384)return 1;
    flint_set_num_threads(1);
    const size_t width=(bits+7)/8;
    fmpz_t modulus,workmod,x,q,odd,oddinv,rem;
    fmpz_init(modulus);fmpz_init(workmod);fmpz_init(x);fmpz_init(q);
    fmpz_init(odd);fmpz_init(oddinv);fmpz_init(rem);
    fmpz_one(modulus);fmpz_mul_2exp(modulus,modulus,bits);
    fmpz_one(workmod);fmpz_mul_2exp(workmod,workmod,bits+11);
    fmpz_mod_ctx_t ctx;fmpz_mod_ctx_init(ctx,workmod);
    fmpz_mod_poly_t A[8],B[8],C[8],values[15],left,right,quotient,scaled;
    mpz_t convert;mpz_init(convert);
    for(long u=0;u<8;u++){
        fmpz_mod_poly_init(A[u],ctx);fmpz_mod_poly_init(B[u],ctx);fmpz_mod_poly_init(C[u],ctx);
        for(long i=0;i<na;i++){
            mpz_import(convert,width,-1,1,0,0,aa+((size_t)i*8+u)*width);
            fmpz_set_mpz(x,convert);fmpz_mod_poly_set_coeff_fmpz(A[u],i,x,ctx);
        }
        for(long i=0;i<nb;i++){
            mpz_import(convert,width,-1,1,0,0,bb+((size_t)i*8+u)*width);
            fmpz_set_mpz(x,convert);fmpz_mod_poly_set_coeff_fmpz(B[u],i,x,ctx);
        }
    }
    fmpz_mod_poly_init(left,ctx);fmpz_mod_poly_init(right,ctx);
    fmpz_mod_poly_init(quotient,ctx);fmpz_mod_poly_init(scaled,ctx);
    for(long t=0;t<15;t++){
        fmpz_mod_poly_init(values[t],ctx);
        fmpz_mod_poly_zero(left,ctx);fmpz_mod_poly_zero(right,ctx);
        for(long u=7;u>=0;u--){
            fmpz_mod_poly_scalar_mul_ui(left,left,t,ctx);fmpz_mod_poly_add(left,left,A[u],ctx);
            fmpz_mod_poly_scalar_mul_ui(right,right,t,ctx);fmpz_mod_poly_add(right,right,B[u],ctx);
        }
        fmpz_mod_poly_mullow(values[t],left,right,length,ctx);
    }
    fmpz_t basis[15][8],next[9];
    for(long j=0;j<15;j++)for(long u=0;u<8;u++)fmpz_init(basis[j][u]);
    for(long u=0;u<9;u++)fmpz_init(next[u]);
    fmpz_one(basis[0][0]);
    for(long j=0;j<14;j++){
        for(long u=0;u<9;u++)fmpz_zero(next[u]);
        for(long u=0;u<8;u++){
            fmpz_addmul_si(next[u],basis[j][u],-j);
            fmpz_add(next[u+1],next[u+1],basis[j][u]);
        }
        for(long u=0;u<8;u++){
            fmpz_addmul_si(next[u],next[8],-FP[u]);fmpz_set(basis[j+1][u],next[u]);
        }
    }
    unsigned long factorial=1;
    for(long degree=0;degree<15;degree++){
        if(degree>0)factorial*=(unsigned long)degree;
        unsigned long oddpart=factorial,shift=0;
        while((oddpart&1UL)==0){oddpart>>=1;shift++;}
        assert(shift<=11);fmpz_set_ui(odd,oddpart);assert(fmpz_invmod(oddinv,odd,modulus));
        fmpz_mod_poly_zero(quotient,ctx);
        for(long i=0;i<length;i++){
            fmpz_mod_poly_get_coeff_fmpz(x,values[0],i,ctx);
            fmpz_fdiv_r_2exp(rem,x,shift);assert(fmpz_is_zero(rem));
            fmpz_fdiv_q_2exp(q,x,shift);fmpz_mul(q,q,oddinv);fmpz_fdiv_r_2exp(q,q,bits);
            fmpz_mod_poly_set_coeff_fmpz(quotient,i,q,ctx);
        }
        for(long u=0;u<8;u++){
            fmpz_mod_poly_scalar_mul_fmpz(scaled,quotient,basis[degree][u],ctx);
            fmpz_mod_poly_add(C[u],C[u],scaled,ctx);
        }
        for(long t=0;t<14-degree;t++)fmpz_mod_poly_sub(values[t],values[t+1],values[t],ctx);
    }
    memset(out,0,(size_t)length*8*width);
    for(long i=0;i<length;i++)for(long u=0;u<8;u++){
        fmpz_mod_poly_get_coeff_fmpz(x,C[u],i,ctx);fmpz_fdiv_r_2exp(x,x,bits);fmpz_get_mpz(convert,x);
        assert((mpz_sizeinbase(convert,2)+7)/8<=width);
        size_t written=0;mpz_export(out+((size_t)i*8+u)*width,&written,-1,1,0,0,convert);assert(written<=width);
    }
    for(long u=0;u<8;u++){
        fmpz_mod_poly_clear(A[u],ctx);fmpz_mod_poly_clear(B[u],ctx);fmpz_mod_poly_clear(C[u],ctx);
    }
    for(long t=0;t<15;t++)fmpz_mod_poly_clear(values[t],ctx);
    fmpz_mod_poly_clear(left,ctx);fmpz_mod_poly_clear(right,ctx);
    fmpz_mod_poly_clear(quotient,ctx);fmpz_mod_poly_clear(scaled,ctx);
    for(long j=0;j<15;j++)for(long u=0;u<8;u++)fmpz_clear(basis[j][u]);
    for(long u=0;u<9;u++)fmpz_clear(next[u]);
    mpz_clear(convert);fmpz_mod_ctx_clear(ctx);
    fmpz_clear(modulus);fmpz_clear(workmod);fmpz_clear(x);fmpz_clear(q);
    fmpz_clear(odd);fmpz_clear(oddinv);fmpz_clear(rem);
    return 0;
}

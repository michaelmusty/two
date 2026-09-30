/* D121 exact matrix products over (Z/2^bits Z)[b]/f(b), deg(f)=8.
 * Evaluate degree-seven entries at 0,...,14, multiply 15 ordinary
 * modular matrices, and interpolate via integral finite differences.
 * Eleven guard bits cover v_2(14!); no even element is inverted.
 */
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <gmp.h>
#include <flint/flint.h>
#include <flint/fmpz.h>
#include <flint/fmpz_mod.h>
#include <flint/fmpz_mod_mat.h>

static const long FP[8] = {2,0,-16,0,20,0,-8,0};

const char *dembele_flint_version(void) { return FLINT_VERSION; }

int dembele_block_mul(unsigned char *out, const unsigned char *aa,
                      const unsigned char *bb, long nr, long nk,
                      long nc, unsigned long bits)
{
    if (nr < 1 || nk < 1 || nc < 1 || bits < 1 || bits > 16384) return 1;
    flint_set_num_threads(1);
    const size_t width = (bits+7)/8;
    const unsigned long workbits = bits+11;
    fmpz_t modulus, workmod, temp, quotient, odd, oddinv, rem;
    fmpz_init(modulus); fmpz_init(workmod); fmpz_init(temp);
    fmpz_init(quotient); fmpz_init(odd); fmpz_init(oddinv); fmpz_init(rem);
    fmpz_one(modulus); fmpz_mul_2exp(modulus, modulus, bits);
    fmpz_one(workmod); fmpz_mul_2exp(workmod, workmod, workbits);
    fmpz_mod_ctx_t context; fmpz_mod_ctx_init(context, workmod);
    fmpz_mod_mat_t A[8], B[8], C[8], values[15], left, right;
    mpz_t convert; mpz_init(convert);
    for (long u=0; u<8; u++) {
        fmpz_mod_mat_init(A[u], nr, nk, context);
        fmpz_mod_mat_init(B[u], nk, nc, context);
        fmpz_mod_mat_init(C[u], nr, nc, context);
        for (long i=0; i<nr; i++) for (long k=0; k<nk; k++) {
            mpz_import(convert, width, -1, 1, 0, 0, aa+(((size_t)i*nk+k)*8+u)*width);
            fmpz_set_mpz(fmpz_mod_mat_entry(A[u],i,k), convert);
        }
        for (long k=0; k<nk; k++) for (long j=0; j<nc; j++) {
            mpz_import(convert, width, -1, 1, 0, 0, bb+(((size_t)k*nc+j)*8+u)*width);
            fmpz_set_mpz(fmpz_mod_mat_entry(B[u],k,j), convert);
        }
    }
    fmpz_mod_mat_init(left, nr, nk, context);
    fmpz_mod_mat_init(right, nk, nc, context);
    for (long t=0; t<15; t++) {
        fmpz_mod_mat_init(values[t], nr, nc, context);
        for (long i=0; i<nr; i++) for (long k=0; k<nk; k++) {
            fmpz *x = fmpz_mod_mat_entry(left,i,k); fmpz_zero(x);
            for (long u=7; u>=0; u--) {
                fmpz_mul_ui(x,x,t); fmpz_add(x,x,fmpz_mod_mat_entry(A[u],i,k));
            }
            fmpz_fdiv_r_2exp(x,x,workbits);
        }
        for (long k=0; k<nk; k++) for (long j=0; j<nc; j++) {
            fmpz *x = fmpz_mod_mat_entry(right,k,j); fmpz_zero(x);
            for (long u=7; u>=0; u--) {
                fmpz_mul_ui(x,x,t); fmpz_add(x,x,fmpz_mod_mat_entry(B[u],k,j));
            }
            fmpz_fdiv_r_2exp(x,x,workbits);
        }
        fmpz_mod_mat_mul(values[t], left, right, context);
    }
    /* Falling factorial polynomials reduced in Z[b]/f(b). */
    fmpz_t basis[15][8], next[9];
    for (long j=0; j<15; j++) for (long u=0; u<8; u++) fmpz_init(basis[j][u]);
    for (long u=0; u<9; u++) fmpz_init(next[u]);
    fmpz_one(basis[0][0]);
    for (long j=0; j<14; j++) {
        for (long u=0; u<9; u++) fmpz_zero(next[u]);
        for (long u=0; u<8; u++) {
            fmpz_addmul_si(next[u],basis[j][u],-j);
            fmpz_add(next[u+1],next[u+1],basis[j][u]);
        }
        for (long u=0; u<8; u++) {
            fmpz_addmul_si(next[u],next[8],-FP[u]);
            fmpz_set(basis[j+1][u],next[u]);
        }
    }
    unsigned long factorial = 1;
    for (long degree=0; degree<15; degree++) {
        if (degree > 0) factorial *= (unsigned long)degree; /* 14! < 2^37 */
        unsigned long oddpart=factorial, shift=0;
        while ((oddpart & 1UL)==0) { oddpart >>= 1; shift++; }
        assert(shift <= 11);
        fmpz_set_ui(odd,oddpart); assert(fmpz_invmod(oddinv,odd,modulus));
        for (long i=0; i<nr; i++) for (long j=0; j<nc; j++) {
            fmpz *value = fmpz_mod_mat_entry(values[0],i,j);
            fmpz_fdiv_r_2exp(rem,value,shift); assert(fmpz_is_zero(rem));
            fmpz_fdiv_q_2exp(quotient,value,shift);
            fmpz_mul(quotient,quotient,oddinv);
            fmpz_fdiv_r_2exp(quotient,quotient,bits);
            for (long u=0; u<8; u++)
                fmpz_addmul(fmpz_mod_mat_entry(C[u],i,j),quotient,basis[degree][u]);
        }
        for (long t=0; t<14-degree; t++)
            for (long i=0; i<nr; i++) for (long j=0; j<nc; j++) {
                fmpz *value = fmpz_mod_mat_entry(values[t],i,j);
                fmpz_sub(value,fmpz_mod_mat_entry(values[t+1],i,j),value);
                fmpz_fdiv_r_2exp(value,value,workbits);
            }
    }
    memset(out,0,(size_t)nr*nc*8*width);
    for (long i=0; i<nr; i++) for (long j=0; j<nc; j++) for (long u=0; u<8; u++) {
        fmpz *value = fmpz_mod_mat_entry(C[u],i,j);
        fmpz_fdiv_r_2exp(value,value,bits); fmpz_get_mpz(convert,value);
        assert((mpz_sizeinbase(convert,2)+7)/8 <= width);
        size_t written=0;
        mpz_export(out+(((size_t)i*nc+j)*8+u)*width,&written,-1,1,0,0,convert);
        assert(written <= width);
    }
    for (long u=0; u<8; u++) {
        fmpz_mod_mat_clear(A[u],context); fmpz_mod_mat_clear(B[u],context);
        fmpz_mod_mat_clear(C[u],context);
    }
    for (long t=0; t<15; t++) fmpz_mod_mat_clear(values[t],context);
    fmpz_mod_mat_clear(left,context); fmpz_mod_mat_clear(right,context);
    for (long j=0; j<15; j++) for (long u=0; u<8; u++) fmpz_clear(basis[j][u]);
    for (long u=0; u<9; u++) fmpz_clear(next[u]);
    mpz_clear(convert); fmpz_mod_ctx_clear(context);
    fmpz_clear(modulus); fmpz_clear(workmod); fmpz_clear(temp);
    fmpz_clear(quotient); fmpz_clear(odd); fmpz_clear(oddinv); fmpz_clear(rem);
    return 0;
}

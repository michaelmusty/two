/* D124 move the proved carry-free small polynomial products into C.
 * Large products retain the frozen D122 implementation. The caller uses
 * fixed-width, little-endian unsigned field coefficients throughout.
 */
#include "476_dyadic_polynomial_kernel.c"

int dembele_adaptive_poly_mul(unsigned char *out,const unsigned char *aa,
                             const unsigned char *bb,long na,long nb,
                             long length,unsigned long bits)
{
    if(na<1 || nb<1 || length<1 || length>na+nb-1 || bits<1 || bits>16384)return 1;
    if(length>=24)return dembele_poly_mul(out,aa,bb,na,nb,length,bits);
    if(na>length)na=length;
    if(nb>length)nb=length;
    const size_t width=(bits+7)/8;
    unsigned long terms=8UL*(unsigned long)(na<nb?na:nb),guard=0;
    for(unsigned long t=terms;t;t>>=1)guard++;
    const size_t packed_width=(2*bits+guard+7)/8;
    const long full=na+nb-1;
    const size_t left_bytes=(size_t)na*15*packed_width;
    const size_t right_bytes=(size_t)nb*15*packed_width;
    const size_t product_bytes=(size_t)full*15*packed_width;
    unsigned char *left=calloc(left_bytes,1),*right=calloc(right_bytes,1),*product=calloc(product_bytes,1);
    if(!left || !right || !product){free(left);free(right);free(product);return 2;}
    assert(width<=packed_width);
    for(long i=0;i<na;i++)for(long j=0;j<8;j++)
        memcpy(left+((size_t)i*15+j)*packed_width,aa+((size_t)i*8+j)*width,width);
    for(long i=0;i<nb;i++)for(long j=0;j<8;j++)
        memcpy(right+((size_t)i*15+j)*packed_width,bb+((size_t)i*8+j)*width,width);
    mpz_t x,y,z,coeff[15];mpz_init(x);mpz_init(y);mpz_init(z);
    for(long j=0;j<15;j++)mpz_init(coeff[j]);
    mpz_import(x,left_bytes,-1,1,0,0,left);mpz_import(y,right_bytes,-1,1,0,0,right);mpz_mul(z,x,y);
    assert((mpz_sizeinbase(z,2)+7)/8<=product_bytes);
    size_t written=0;mpz_export(product,&written,-1,1,0,0,z);assert(written<=product_bytes);
    memset(out,0,(size_t)length*8*width);
    for(long i=0;i<length;i++){
        for(long j=0;j<15;j++)mpz_import(coeff[j],packed_width,-1,1,0,0,product+((size_t)i*15+j)*packed_width);
        for(long k=14;k>=8;k--)for(long j=0;j<8;j++){
            if(FP[j]>0)mpz_submul_ui(coeff[k-8+j],coeff[k],(unsigned long)FP[j]);
            if(FP[j]<0)mpz_addmul_ui(coeff[k-8+j],coeff[k],(unsigned long)(-FP[j]));
        }
        for(long j=0;j<8;j++){
            mpz_fdiv_r_2exp(coeff[j],coeff[j],bits);
            written=0;mpz_export(out+((size_t)i*8+j)*width,&written,-1,1,0,0,coeff[j]);assert(written<=width);
        }
    }
    for(long j=0;j<15;j++)mpz_clear(coeff[j]);
    mpz_clear(x);mpz_clear(y);mpz_clear(z);free(left);free(right);free(product);
    return 0;
}

/* D87: skip polynomial tails only after checking an absolute ball bound.
 * The Python caller checks |coefficient| <= 10^8 for both polynomials.
 * For L < n, both omitted value and derivative are bounded by
 * 10^8*n*r^(L-1)/(1-r).  Add that error to all four output balls.
 * This bounds only a FINITE POLYNOMIAL tail, not the differential tail.
 */
#include <flint/acb.h>
#include <flint/acb_poly.h>
#include <math.h>
typedef struct { slong length; acb_ptr data; } cm_vector;

int cover_evaluate2(cm_vector *out, const cm_vector *polynomials,
                    const cm_vector *nodes, slong n, slong prec)
{
    slong count = nodes->length;
    if (polynomials->length != 2*n || out->length != 4*count) return 0;
    arb_t radius, upper, bound, denominator, tolerance;
    arf_t endpoint;
    mag_t error;
    arb_init(radius); arb_init(upper); arb_init(bound);
    arb_init(denominator); arb_init(tolerance); arf_init(endpoint); mag_init(error);
    arb_set_str(tolerance, "1e-65", prec);
    for (slong i = 0; i < count; i++) {
        acb_abs(radius, nodes->data+i, prec);
        arb_get_ubound_arf(endpoint, radius, prec);
        double r = arf_get_d(endpoint, ARF_RND_CEIL);
        slong length = n;
        mag_zero(error);
        if (r > 0 && r < 1) {
            double estimate = ceil(log(1e-70*(1-r)/(1e8*n))/log(r))+1;
            if (estimate >= 2 && estimate < n) {
                length = (slong)estimate;
                arb_set_d(upper, r);
                arb_pow_ui(bound, upper, length-1, prec);
                arb_mul_ui(bound, bound, 100000000, prec);
                arb_mul_ui(bound, bound, n, prec);
                arb_one(denominator);
                arb_sub(denominator, denominator, upper, prec);
                arb_div(bound, bound, denominator, prec);
                if (arb_lt(bound, tolerance)) arb_get_mag(error, bound);
                else length = n;
            }
        }
        for (slong q = 0; q < 2; q++) {
            _acb_poly_evaluate2_rectangular(out->data+q*count+i,
                 out->data+(q+2)*count+i, polynomials->data+q*n, length,
                 nodes->data+i, prec);
            acb_add_error_mag(out->data+q*count+i, error);
            acb_add_error_mag(out->data+(q+2)*count+i, error);
        }
    }
    arb_clear(radius); arb_clear(upper); arb_clear(bound);
    arb_clear(denominator); arb_clear(tolerance); arf_clear(endpoint); mag_clear(error);
    return _acb_vec_is_finite(out->data, out->length);
}

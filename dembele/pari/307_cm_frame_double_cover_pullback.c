/* D87: form the TWO full quadratic polynomials in a saved differential bank.
 * No series terms are discarded.  The cm_vector ABI is that of cm_acb.c.
 * Arithmetic balls do not bound errors in the input geometry or series tail.
 */
#include <flint/acb.h>
#include <flint/acb_poly.h>

typedef struct { slong length; acb_ptr data; } cm_vector;

int cover_quadrics(cm_vector *out, const cm_vector *bank,
                   const cm_vector *change, const slong *numerator,
                   const slong *denominator, slong n, slong prec)
{
    const slong g = 16, m = 2*n-1;
    if (n < 2 || bank->length != n*g || change->length != g*g ||
        out->length != 2*m) return 0;
    acb_ptr points = _acb_vec_init(n*g);
    acb_ptr linear = _acb_vec_init(n);
    acb_ptr product = _acb_vec_init(m);
    for (slong j = 0; j < g; j++)
        for (slong k = 0; k < n; k++)
            acb_dot(points+j*n+k, NULL, 0, bank->data+k, n,
                    change->data+j*g, 1, g, prec);
    for (slong q = 0; q < 2; q++) {
        const slong *coefficients = q ? denominator : numerator;
        _acb_vec_zero(out->data+q*m, m);
        slong term = 0;
        for (slong i = 0; i < g; i++) {
            _acb_vec_zero(linear, n);
            for (slong j = i; j < g; j++, term++)
                for (slong k = 0; k < n; k++)
                    acb_addmul_si(linear+k, points+j*n+k, coefficients[term], prec);
            _acb_poly_mul(product, points+i*n, n, linear, n, prec);
            _acb_vec_add(out->data+q*m, out->data+q*m, product, m, prec);
        }
        if (term != 136) flint_abort();
    }
    _acb_vec_clear(points, n*g);
    _acb_vec_clear(linear, n);
    _acb_vec_clear(product, m);
    return _acb_vec_is_finite(out->data, out->length);
}

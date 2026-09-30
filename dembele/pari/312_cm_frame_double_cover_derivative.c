/* D87: values and first derivatives of the two cached full polynomials. */
#include <flint/acb.h>
#include <flint/acb_poly.h>
typedef struct { slong length; acb_ptr data; } cm_vector;

int cover_evaluate2(cm_vector *out, const cm_vector *polynomials,
                    const cm_vector *nodes, slong n, slong prec)
{
    slong count = nodes->length;
    if (polynomials->length != 2*n || out->length != 4*count) return 0;
    for (slong q = 0; q < 2; q++)
        for (slong i = 0; i < count; i++)
            _acb_poly_evaluate2_rectangular(out->data+q*count+i,
                 out->data+(q+2)*count+i, polynomials->data+q*n, n,
                 nodes->data+i, prec);
    return _acb_vec_is_finite(out->data, out->length);
}

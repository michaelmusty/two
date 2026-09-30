/* Arbitrary-precision Cauchy actions for the CM differential computation.
 *
 * FLINT balls enclose arithmetic on the supplied decimal geometry. They do
 * not enclose the exact geometric inputs or an infinite-series tail.
 * Matrices below are stored column by column. The Python wrapper owns sizes.
 */
#include <flint/acb.h>
#include <flint/acb_dft.h>
#include <flint/acb_poly.h>
#include <math.h>
#include <stdio.h>

typedef struct {
    slong length;
    acb_ptr data;
} cm_vector;

typedef struct {
    slong n, count, prec;
    acb_ptr nodes, weights, phases, values, transformed;
    acb_dft_pre_t plan;
} cm_operator;

const char *cm_version(void) { return FLINT_VERSION; }
void cm_free(void *p) { flint_free(p); }

cm_vector *cm_vec_new(slong length)
{
    if (length <= 0) return NULL;
    cm_vector *v = flint_malloc(sizeof(*v));
    v->length = length;
    v->data = _acb_vec_init(length);
    return v;
}

void cm_vec_free(cm_vector *v)
{
    if (!v) return;
    _acb_vec_clear(v->data, v->length);
    flint_free(v);
}

int cm_vec_set_str(cm_vector *v, slong i, const char *re, const char *im, slong prec)
{
    if (i < 0 || i >= v->length) return 0;
    return arb_set_str(acb_realref(v->data+i), re, prec) == 0 &&
           arb_set_str(acb_imagref(v->data+i), im, prec) == 0 &&
           acb_is_finite(v->data+i);
}

int cm_vec_set_double(cm_vector *v, const double *data)
{
    for (slong i = 0; i < v->length; i++) {
        if (!isfinite(data[2*i]) || !isfinite(data[2*i+1])) return 0;
        acb_set_d_d(v->data+i, data[2*i], data[2*i+1]);
    }
    return 1;
}

char *cm_vec_component(const cm_vector *v, slong i, int component, slong digits)
{
    if (i < 0 || i >= v->length || component < 0 || component > 3) return NULL;
    arb_srcptr value = component % 2 ? acb_imagref(v->data+i) : acb_realref(v->data+i);
    if (component < 2) return arf_get_str(arb_midref(value), digits);
    arf_t radius;
    arf_init(radius);
    arf_set_mag(radius, arb_radref(value));
    char *result = arf_get_str(radius, digits);
    arf_clear(radius);
    return result;
}

/* Infinity norm bounds: mode 0 bounds midpoints, mode 1 bounds radii,
 * mode 2 bounds the whole complex balls. Bounds are for one column. */
char *cm_vec_bound(const cm_vector *v, slong start, slong length,
                   int mode, slong prec, slong digits)
{
    if (start < 0 || length <= 0 || start+length > v->length) return NULL;
    arf_t best, value;
    acb_t mid;
    arf_init(best); arf_init(value); acb_init(mid);
    for (slong i = start; i < start+length; i++) {
        if (mode == 1) acb_get_rad_ubound_arf(value, v->data+i, prec);
        else {
            acb_get_mid(mid, v->data+i);
            acb_get_abs_ubound_arf(value, mode == 0 ? mid : v->data+i, prec);
        }
        if (arf_cmp(value, best) > 0) arf_set(best, value);
    }
    char *result = arf_get_str(best, digits);
    arf_clear(best); arf_clear(value); acb_clear(mid);
    return result;
}

/* Residuals smaller than the double exponent range must still survive the
 * conversion to the correction solver. Each column gets an exact 2^e scale. */
int cm_vec_scaled_doubles(const cm_vector *v, slong rows, slong columns,
                          double *out, slong *exponents)
{
    if (rows*columns != v->length) return 0;
    arf_t largest, temp;
    arf_init(largest); arf_init(temp);
    for (slong c = 0; c < columns; c++) {
        arf_zero(largest);
        for (slong j = 0; j < rows; j++) {
            acb_srcptr z = v->data+c*rows+j;
            if (!acb_is_finite(z)) { arf_clear(largest); arf_clear(temp); return 0; }
            if (arf_cmpabs(arb_midref(acb_realref(z)), largest) > 0)
                arf_abs(largest, arb_midref(acb_realref(z)));
            if (arf_cmpabs(arb_midref(acb_imagref(z)), largest) > 0)
                arf_abs(largest, arb_midref(acb_imagref(z)));
        }
        slong e = arf_is_zero(largest) ? 0 : arf_abs_bound_lt_2exp_si(largest);
        exponents[c] = e;
        for (slong j = 0; j < rows; j++) {
            slong i = c*rows+j;
            arf_mul_2exp_si(temp, arb_midref(acb_realref(v->data+i)), -e);
            out[2*i] = arf_get_d(temp, ARF_RND_NEAR);
            arf_mul_2exp_si(temp, arb_midref(acb_imagref(v->data+i)), -e);
            out[2*i+1] = arf_get_d(temp, ARF_RND_NEAR);
        }
    }
    arf_clear(largest); arf_clear(temp);
    return 1;
}

int cm_vec_add_correction(cm_vector *v, slong rows, slong columns,
                          const double *correction, const slong *exponents, slong prec)
{
    if (rows*columns != v->length) return 0;
    for (slong i = 0; i < 2*v->length; i++)
        if (!isfinite(correction[i])) return 0;
    acb_t delta;
    acb_init(delta);
    for (slong c = 0; c < columns; c++) {
        for (slong j = 0; j < rows; j++) {
            slong i = c*rows+j;
            acb_set_d_d(delta, correction[2*i], correction[2*i+1]);
            acb_mul_2exp_si(delta, delta, exponents[c]);
            acb_add(v->data+i, v->data+i, delta, prec);
            /* Iterates are dyadic points. The next residual encloses the
             * action at this point, avoiding accumulated interval dependency. */
            acb_get_mid(v->data+i, v->data+i);
        }
    }
    acb_clear(delta);
    return 1;
}

int cm_vec_write(const cm_vector *v, const char *path)
{
    FILE *file = fopen(path, "wx");
    if (!file) return 0;
    fprintf(file, "CM_ACB_V1 %ld\n", v->length);
    for (slong i = 0; i < v->length; i++) {
        arb_dump_file(file, acb_realref(v->data+i)); fputc('\n', file);
        arb_dump_file(file, acb_imagref(v->data+i)); fputc('\n', file);
    }
    int ok = !ferror(file);
    if (fclose(file)) ok = 0;
    return ok;
}

cm_vector *cm_vec_read(const char *path, slong length)
{
    FILE *file = fopen(path, "r");
    if (!file) return NULL;
    slong stored;
    if (fscanf(file, "CM_ACB_V1 %ld\n", &stored) != 1 || stored != length) {
        fclose(file); return NULL;
    }
    cm_vector *v = cm_vec_new(length);
    for (slong i = 0; i < length; i++) {
        if (arb_load_file(acb_realref(v->data+i), file) ||
            arb_load_file(acb_imagref(v->data+i), file) || !acb_is_finite(v->data+i)) {
            fclose(file); cm_vec_free(v); return NULL;
        }
    }
    fclose(file);
    return v;
}

cm_operator *cm_op_new(slong n, const cm_vector *nodes, const cm_vector *weights,
                        const char *offset, slong prec)
{
    if (n <= 0 || nodes->length < n || nodes->length != weights->length) return NULL;
    acb_t phase, shift;
    acb_init(phase); acb_init(shift);
    if (arb_set_str(acb_realref(shift), offset, prec) || !acb_is_finite(shift)) {
        acb_clear(phase); acb_clear(shift); return NULL;
    }
    cm_operator *op = flint_malloc(sizeof(*op));
    op->n = n; op->count = nodes->length; op->prec = prec;
    op->nodes = _acb_vec_init(op->count);
    op->weights = _acb_vec_init(op->count);
    op->phases = _acb_vec_init(n);
    op->values = _acb_vec_init(op->count);
    op->transformed = _acb_vec_init(op->count);
    _acb_vec_set(op->nodes, nodes->data, op->count);
    _acb_vec_set(op->weights, weights->data, op->count);
    for (slong k = 0; k < n; k++) {
        acb_mul_si(phase, shift, -2*k, prec);
        acb_div_ui(phase, phase, op->count, prec);
        acb_exp_pi_i(phase, phase, prec);
        acb_div_ui(op->phases+k, phase, op->count, prec);
    }
    acb_dft_precomp_init(op->plan, op->count, prec);
    acb_clear(phase); acb_clear(shift);
    return op;
}

void cm_op_free(cm_operator *op)
{
    if (!op) return;
    _acb_vec_clear(op->nodes, op->count);
    _acb_vec_clear(op->weights, op->count);
    _acb_vec_clear(op->phases, op->n);
    _acb_vec_clear(op->values, op->count);
    _acb_vec_clear(op->transformed, op->count);
    acb_dft_precomp_clear(op->plan);
    flint_free(op);
}

static void evaluate(acb_t out, acb_srcptr coefficients, slong n,
                      const acb_t node, slong prec, int method)
{
    if (method == 0) _acb_poly_evaluate_horner(out, coefficients, n, node, prec);
    else _acb_poly_evaluate_rectangular(out, coefficients, n, node, prec);
}

int cm_evaluate(cm_vector *out, const cm_vector *coefficients, slong n,
                 slong columns, const cm_vector *nodes, slong prec, int method)
{
    if (coefficients->length != n*columns || out->length != nodes->length*columns) return 0;
    for (slong c = 0; c < columns; c++)
        for (slong t = 0; t < nodes->length; t++)
            evaluate(out->data+c*nodes->length+t, coefficients->data+c*n,
                     n, nodes->data+t, prec, method);
    return _acb_vec_is_finite(out->data, out->length);
}

int cm_op_apply(cm_operator *op, cm_vector *out, const cm_vector *coefficients,
                 slong columns, slong first, slong stop, int method)
{
    if (coefficients->length != op->n*columns || out->length != coefficients->length ||
        first < 0 || stop < first || stop > columns) return 0;
    for (slong c = first; c < stop; c++) {
        for (slong t = 0; t < op->count; t++) {
            evaluate(op->values+t, coefficients->data+c*op->n, op->n,
                     op->nodes+t, op->prec, method);
            acb_mul(op->values+t, op->values+t, op->weights+t, op->prec);
        }
        acb_dft_precomp(op->transformed, op->values, op->plan, op->prec);
        for (slong k = 0; k < op->n; k++)
            acb_mul(out->data+c*op->n+k, op->transformed+k, op->phases+k, op->prec);
    }
    return _acb_vec_is_finite(out->data+first*op->n, (stop-first)*op->n);
}

/* out = B[:, :columns] - (I-A)X - B(B* X), given AX in out. */
int cm_stabilized_residual(cm_vector *out, const cm_vector *x,
                            const cm_vector *basis, slong n, slong columns,
                            slong rank, slong prec)
{
    if (out->length != n*columns || x->length != out->length ||
        basis->length != n*rank || columns > rank) return 0;
    acb_ptr conjugate = _acb_vec_init(n*rank);
    acb_ptr inner = _acb_vec_init(rank);
    acb_t projection;
    acb_init(projection);
    for (slong i = 0; i < n*rank; i++) acb_conj(conjugate+i, basis->data+i);
    for (slong c = 0; c < columns; c++) {
        for (slong j = 0; j < rank; j++)
            acb_dot(inner+j, NULL, 0, conjugate+j*n, 1, x->data+c*n, 1, n, prec);
        for (slong k = 0; k < n; k++) {
            acb_dot(projection, NULL, 0, basis->data+k, n, inner, 1, rank, prec);
            slong i = c*n+k;
            acb_sub(out->data+i, out->data+i, x->data+i, prec);
            acb_sub(out->data+i, out->data+i, projection, prec);
            acb_add(out->data+i, out->data+i, basis->data+i, prec);
        }
    }
    acb_clear(projection);
    _acb_vec_clear(conjugate, n*rank); _acb_vec_clear(inner, rank);
    return _acb_vec_is_finite(out->data, out->length);
}

int cm_vec_sub(cm_vector *out, const cm_vector *a, const cm_vector *b, slong prec)
{
    if (out->length != a->length || a->length != b->length) return 0;
    _acb_vec_sub(out->data, a->data, b->data, out->length, prec);
    return _acb_vec_is_finite(out->data, out->length);
}

int cm_weighted_sub(cm_vector *out, const cm_vector *left, const cm_vector *right,
                     const cm_vector *weights, slong columns, slong prec)
{
    if (left->length != weights->length*columns || right->length != left->length ||
        out->length != left->length) return 0;
    for (slong c = 0; c < columns; c++)
        for (slong j = 0; j < weights->length; j++) {
            slong i = c*weights->length+j;
            acb_mul(out->data+i, weights->data+j, right->data+i, prec);
            acb_sub(out->data+i, left->data+i, out->data+i, prec);
        }
    return _acb_vec_is_finite(out->data, out->length);
}

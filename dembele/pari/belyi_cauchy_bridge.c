/* Adapter only: compile the user's existing Belyi operator and Arnoldi
   implementation in this translation unit, without modifying its source.
   BELYI_ROOT/Cext is supplied as an include directory by the Python driver. */
#define POWSER_NO_MAIN
#include "powser_arnoldi.c"

typedef struct {
    matvec_ws_t *ws;
    slong n;
    acb_ptr full_in, full_out;
} cover_ctx_t;

/* Three sheet functions in the elliptic-transposition eigenbasis:
   f0 = -2 w^31 a(w^32), f1 = w^31 a(w^32)+w^15 b(w^32),
   f2 = w^31 a(w^32)-w^15 b(w^32). Radius scaling is in the input nodes. */
static void cover_embed(acb_ptr full, acb_srcptr v, slong n, slong prec)
{
    for (slong i = 0; i < n; i++) {
        acb_mul_si(full+i, v+i, -2, prec);
        acb_set(full+n+2*i+1, v+i);
        acb_set(full+n+2*i, v+n+i);
    }
}

static void cover_project(acb_ptr v, acb_srcptr full, slong n, slong prec)
{
    for (slong i = 0; i < n; i++) {
        acb_sub(v+i, full+n+2*i+1, full+i, prec);
        acb_div_si(v+i, v+i, 3, prec);
        acb_set(v+n+i, full+n+2*i);
    }
}

static void cover_matvec(acb_ptr out, acb_srcptr in, void *opaque)
{
    cover_ctx_t *ctx = opaque;
    slong prec = ctx->ws->pb->prec;
    cover_embed(ctx->full_in, in, ctx->n, prec);
    matvec_structured(ctx->full_out, ctx->full_in, ctx->ws);
    cover_project(out, ctx->full_out, ctx->n, prec);
}

int main(int argc, char **argv)
{
    if (argc != 5) {
        fprintf(stderr, "usage: belyi_bridge apply|new|solve input output threads\n");
        return 1;
    }
    int standard = strcmp(argv[1], "apply") != 0;
    int solve = strcmp(argv[1], "solve") == 0;
    if (strcmp(argv[1], "apply") && strcmp(argv[1], "new") && !solve)
        return 1;
    problem_t pb;
    memset(&pb, 0, sizeof(pb));
    problem_read(&pb, argv[2], atol(argv[4]));
    if (pb.nv != 2 || pb.NN[1] != 2*pb.NN[0]) {
        fprintf(stderr, "expected orbit blocks of lengths n and 2n\n");
        return 1;
    }
    matvec_ws_t ws;
    matvec_ws_init(&ws, &pb);
    slong n = pb.NN[0], size = standard ? 2*n : 3*n;
    cover_ctx_t ctx = {&ws, n, _acb_vec_init(3*n), _acb_vec_init(3*n)};
    acb_ptr start = _acb_vec_init(size), out = _acb_vec_init(size);
    arb_t minsing;
    arb_init(minsing);
    FILE *file = fopen(argv[3], "w");
    if (!file) { perror("output"); return 1; }
    fprintf(file, "%ld %ld\n", (long)size, (long)pb.dim);
    int allok = 1;
    for (slong d = 0; d < pb.dim; d++) {
        if (standard)
            cover_project(start, pb.start+d*pb.V, n, pb.prec);
        else
            _acb_vec_set(start, pb.start+d*pb.V, size);
        if (solve) {
            int ok = arnoldi_run(out, start, size, cover_matvec, &ctx, &pb, minsing, 1);
            allok &= ok;
            flint_printf("BRIDGE|vector=%wd; converged=%d; minsing=", d, ok);
            arb_printn(minsing, 8, ARB_STR_NO_RADIUS);
            flint_printf("\n");
        } else if (standard) {
            cover_matvec(out, start, &ctx);
        } else {
            matvec_structured(out, start, &ws);
        }
        double max_mid = 0, max_radius = 0;
        for (slong j = 0; j < size; j++) {
            max_mid = fmax(max_mid, hypot(arf_get_d(arb_midref(acb_realref(out+j)), ARF_RND_NEAR),
                                         arf_get_d(arb_midref(acb_imagref(out+j)), ARF_RND_NEAR)));
            max_radius = fmax(max_radius, hypot(mag_get_d(arb_radref(acb_realref(out+j))),
                                               mag_get_d(arb_radref(acb_imagref(out+j)))));
            /* Return the numerical iterate, while reporting the arithmetic
               ball radii separately. arb_get_str alone may print zero for
               a ball that contains a nonzero midpoint and zero. */
            acb_get_mid(out+j, out+j);
            write_arb(file, acb_realref(out+j), pb.digs);
            fputc(' ', file);
            write_arb(file, acb_imagref(out+j), pb.digs);
            fputc('\n', file);
        }
        printf("BRIDGE|vector=%ld; max_midpoint=%.8e; max_arithmetic_radius=%.8e\n",
               (long)d, max_mid, max_radius);
    }
    fclose(file);
    arb_clear(minsing);
    _acb_vec_clear(start, size); _acb_vec_clear(out, size);
    _acb_vec_clear(ctx.full_in, 3*n); _acb_vec_clear(ctx.full_out, 3*n);
    matvec_ws_clear(&ws);
    return allok ? 0 : 2;
}

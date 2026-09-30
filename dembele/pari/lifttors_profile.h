/* D67 diagnostic hooks. They allocate no PARI objects and change no RNG state.
 * Stack figures are checkpoints, not high-water marks or process RSS. */
#ifndef LIFTTORS_PROFILE_H
#define LIFTTORS_PROFILE_H
#include <pari/pari.h>
typedef struct LiftProfileFrame {
    struct LiftProfileFrame *parent;
    const char *name;
    ulong id;
    pari_sp entry;
    pari_timer timer;
    long precision;
    int active;
} LiftProfileFrame;
void LiftProfileEnable(long enabled);
void LiftProfileStart(LiftProfileFrame *frame, const char *name, long precision);
void LiftProfilePoint(LiftProfileFrame *frame, const char *stage, GEN object, long precision);
GEN LiftProfileEnd(LiftProfileFrame *frame, GEN result);
ulong LiftProfileEndU(LiftProfileFrame *frame, ulong result);
#endif

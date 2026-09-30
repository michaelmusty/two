#include "lifttors_profile.h"
#include <stdio.h>

/* The diagnostic scale jobs use one thread. Worker-local nesting also makes
 * the hooks safe for the retained chart path; those worker trees are not
 * combined into the single-thread scale reports. */
static _Thread_local LiftProfileFrame *current_frame = NULL;
static _Thread_local ulong next_id = 0;
static int enabled = 0;

void LiftProfileEnable(long value)
{
    enabled = value != 0;
    current_frame = NULL;
    next_id = 0;
}

void LiftProfilePoint(LiftProfileFrame *frame, const char *stage, GEN object, long precision)
{
    ulong used, local, capacity;
    long elapsed, bytes;
    if (!frame->active) return;
    used = (ulong)(pari_mainstack->top-avma);
    local = (ulong)(frame->entry-avma);
    capacity = (ulong)pari_mainstack->size;
    elapsed = walltimer_get(&frame->timer);
    bytes = object ? gsizebyte(object) : 0;
    fprintf(stdout,"TRACE|allocation|id=%lu|parent=%lu|function=%s|stage=%s|e=%ld|stack_bytes=%lu|local_stack_bytes=%lu|object_bytes=%ld|elapsed_ms=%ld|stack_capacity=%lu\n",
            frame->id,frame->parent ? frame->parent->id : 0,frame->name,stage,
            precision,used,local,bytes,elapsed,capacity);
    fflush(stdout);
}

void LiftProfileStart(LiftProfileFrame *frame, const char *name, long precision)
{
    frame->active = enabled;
    if (!enabled) return;
    frame->parent = current_frame;
    frame->name = name;
    frame->id = ++next_id;
    frame->entry = avma;
    frame->precision = precision;
    walltimer_start(&frame->timer);
    current_frame = frame;
    LiftProfilePoint(frame,"enter",NULL,precision);
}

GEN LiftProfileEnd(LiftProfileFrame *frame, GEN result)
{
    if (frame->active) {
        LiftProfilePoint(frame,"exit",NULL,frame->precision);
        current_frame = frame->parent;
    }
    return result;
}

ulong LiftProfileEndU(LiftProfileFrame *frame, ulong result)
{
    if (frame->active) {
        LiftProfilePoint(frame,"exit",NULL,frame->precision);
        current_frame = frame->parent;
    }
    return result;
}

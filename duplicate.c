#include "postgres.h"
#include <string.h>
#include "fmgr.h"
#include "utils/geo_decls.h"
#include "utils/array.h"
#include "utils/builtins.h"


PG_MODULE_MAGIC;

/* by value */

PG_FUNCTION_INFO_V1(add_one);

Datum
add_one(PG_FUNCTION_ARGS)
{
    int32   arg = PG_GETARG_INT32(0);

    PG_RETURN_INT32(arg + 1);
}

/* by reference, fixed length */

PG_FUNCTION_INFO_V1(add_one_float8);

Datum
add_one_float8(PG_FUNCTION_ARGS)
{
    /* The macros for FLOAT8 hide its pass-by-reference nature. */
    float8   arg = PG_GETARG_FLOAT8(0);

    PG_RETURN_FLOAT8(arg + 1.0);
}

PG_FUNCTION_INFO_V1(makepoint);

Datum
makepoint(PG_FUNCTION_ARGS)
{
    /* Here, the pass-by-reference nature of Point is not hidden. */
    Point     *pointx = PG_GETARG_POINT_P(0);
    Point     *pointy = PG_GETARG_POINT_P(1);
    Point     *new_point = (Point *) palloc(sizeof(Point));

    new_point->x = pointx->x;
    new_point->y = pointy->y;

    PG_RETURN_POINT_P(new_point);
}

/* by reference, variable length */

PG_FUNCTION_INFO_V1(copytext);

Datum
copytext(PG_FUNCTION_ARGS)
{
    text     *t = PG_GETARG_TEXT_PP(0);

    /*
     * VARSIZE_ANY_EXHDR is the size of the struct in bytes, minus the
     * VARHDRSZ or VARHDRSZ_SHORT of its header.  Construct the copy with a
     * full-length header.
     */
    text     *new_t = (text *) palloc(VARSIZE_ANY_EXHDR(t) + VARHDRSZ);
    SET_VARSIZE(new_t, VARSIZE_ANY_EXHDR(t) + VARHDRSZ);

    /*
     * VARDATA is a pointer to the data region of the new struct.  The source
     * could be a short datum, so retrieve its data through VARDATA_ANY.
     */
    memcpy((void *) VARDATA(new_t), /* destination */
           (void *) VARDATA_ANY(t), /* source */
           VARSIZE_ANY_EXHDR(t));   /* how many bytes */
    PG_RETURN_TEXT_P(new_t);
}

PG_FUNCTION_INFO_V1(concat_text);

Datum
concat_text(PG_FUNCTION_ARGS)
{
    text  *arg1 = PG_GETARG_TEXT_PP(0);
    text  *arg2 = PG_GETARG_TEXT_PP(1);
    int32 arg1_size = VARSIZE_ANY_EXHDR(arg1);
    int32 arg2_size = VARSIZE_ANY_EXHDR(arg2);
    int32 new_text_size = arg1_size + arg2_size + VARHDRSZ;
    text *new_text = (text *) palloc(new_text_size);

    SET_VARSIZE(new_text, new_text_size);
    memcpy(VARDATA(new_text), VARDATA_ANY(arg1), arg1_size);
    memcpy(VARDATA(new_text) + arg1_size, VARDATA_ANY(arg2), arg2_size);
    PG_RETURN_TEXT_P(new_text);
}

PG_FUNCTION_INFO_V1(duplicate_sfunc);
Datum
duplicate_sfunc(PG_FUNCTION_ARGS)
{
        Oid                     arg1_typeid = get_fn_expr_argtype(fcinfo->flinfo, 1);
        MemoryContext aggcontext;
        ArrayBuildState *state;
        Datum           elem;

        if (arg1_typeid == InvalidOid)
                ereport(ERROR,
                                (errcode(ERRCODE_INVALID_PARAMETER_VALUE),
                                 errmsg("could not determine input data type")));

        /*
         * Note: we do not need a run-time check about whether arg1_typeid is a
         * valid array element type, because the parser would have verified that
         * while resolving the input/result types of this polymorphic aggregate.
         */

        if (!AggCheckCallContext(fcinfo, &aggcontext))
        {
                /* cannot be called directly because of internal-type argument */
                elog(ERROR, "array_agg_transfn called in non-aggregate context");
        }

        if (PG_ARGISNULL(0))
                state = initArrayResult(arg1_typeid, aggcontext, false);
        else
                state = (ArrayBuildState *) PG_GETARG_POINTER(0);

        elem = PG_ARGISNULL(1) ? (Datum) 0 : PG_GETARG_DATUM(1);

        state = accumArrayResult(state,
                                                         elem,
                                                         PG_ARGISNULL(1),
                                                         arg1_typeid,
                                                         aggcontext);
        state = accumArrayResult(state,
                                                         elem,
                                                         PG_ARGISNULL(1),
                                                         arg1_typeid,
                                                         aggcontext);

        /*
         * The transition type for array_agg() is declared to be "internal", which
         * is a pass-by-value type the same size as a pointer.  So we can safely
         * pass the ArrayBuildState pointer through nodeAgg.c's machinations.
         */
        PG_RETURN_POINTER(state);
}

PG_FUNCTION_INFO_V1(duplicate_finalfunc);
Datum
duplicate_finalfunc(PG_FUNCTION_ARGS)
{
        Datum           result;
        ArrayBuildState *state;
        int                     dims[1];
        int                     lbs[1];

        /* cannot be called directly because of internal-type argument */
        Assert(AggCheckCallContext(fcinfo, NULL));

        state = PG_ARGISNULL(0) ? NULL : (ArrayBuildState *) PG_GETARG_POINTER(0);

        if (state == NULL)
                PG_RETURN_NULL();               /* returns null iff no input values */

        dims[0] = state->nelems;
        lbs[0] = 1;

        /*
         * Make the result.  We cannot release the ArrayBuildState because
         * sometimes aggregate final functions are re-executed.  Rather, it is
         * nodeAgg.c's responsibility to reset the aggcontext when it's safe to do
         * so.
         */
        result = makeMdArrayResult(state, 1, dims, lbs,
                                                           CurrentMemoryContext,
                                                           false);

        PG_RETURN_DATUM(result);
}


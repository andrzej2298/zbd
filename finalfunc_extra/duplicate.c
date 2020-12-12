#include "postgres.h"
#include <string.h>
#include "fmgr.h"
#include "utils/geo_decls.h"
#include "utils/array.h"
#include "utils/builtins.h"


PG_MODULE_MAGIC;

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


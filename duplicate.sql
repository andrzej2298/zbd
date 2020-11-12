CREATE OR REPLACE FUNCTION
  add_one(int4)
RETURNS
  int4
AS
  '/home/zbd/duplicate.so', 'add_one'
LANGUAGE
  C
STRICT
IMMUTABLE;

CREATE OR REPLACE FUNCTION
  duplicate_sfunc(internal, anynonarray)
RETURNS
  internal
AS
  '/home/zbd/duplicate.so', 'duplicate_sfunc'
LANGUAGE
  C;

CREATE OR REPLACE FUNCTION
  duplicate_finalfunc(internal, anynonarray)
RETURNS
  anyarray
AS
  '/home/zbd/duplicate.so', 'duplicate_finalfunc'
LANGUAGE
  C;

CREATE OR REPLACE AGGREGATE array_agg_duplicate (anynonarray)
(
    sfunc = duplicate_sfunc,
    stype = internal,
    finalfunc = duplicate_finalfunc,
    finalfunc_extra
);

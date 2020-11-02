create table if not exists targets_source ( field text );
truncate table targets_source;
create table if not exists targets ( target jsonb );
truncate table targets;
\copy targets_source from 'targets.json';
insert into targets select jsonb_array_elements(to_jsonb(field::jsonb)) from targets_source;

create table if not exists audience_source ( field text );
truncate table audience_source;
create table if not exists audience ( audience jsonb );
truncate table audience;
\copy audience_source from 'audience-2019-01-01.json';
\copy audience_source from 'audience-2019-01-02.json';
\copy audience_source from 'audience-2019-01-03.json';
\copy audience_source from 'audience-2019-01-04.json';
\copy audience_source from 'audience-2019-01-05.json';
\copy audience_source from 'audience-2019-01-06.json';
\copy audience_source from 'audience-2019-01-07.json';
\copy audience_source from 'audience-2019-01-08.json';
\copy audience_source from 'audience-2019-01-09.json';
\copy audience_source from 'audience-2019-01-10.json';
\copy audience_source from 'audience-2019-01-11.json';
\copy audience_source from 'audience-2019-01-12.json';
\copy audience_source from 'audience-2019-01-13.json';
\copy audience_source from 'audience-2019-01-14.json';
\copy audience_source from 'audience-2019-01-15.json';
\copy audience_source from 'audience-2019-01-16.json';
\copy audience_source from 'audience-2019-01-17.json';
\copy audience_source from 'audience-2019-01-18.json';
\copy audience_source from 'audience-2019-01-19.json';
\copy audience_source from 'audience-2019-01-20.json';
\copy audience_source from 'audience-2019-01-21.json';
\copy audience_source from 'audience-2019-01-22.json';
\copy audience_source from 'audience-2019-01-23.json';
\copy audience_source from 'audience-2019-01-24.json';
\copy audience_source from 'audience-2019-01-25.json';
\copy audience_source from 'audience-2019-01-26.json';
\copy audience_source from 'audience-2019-01-27.json';
\copy audience_source from 'audience-2019-01-28.json';
\copy audience_source from 'audience-2019-01-29.json';
\copy audience_source from 'audience-2019-01-30.json';
insert into audience select jsonb_array_elements(to_jsonb(field::jsonb)) from audience_source;

with statistics as (
    select distinct
        audience -> 'person_id' as person_id,
        target ->> 'definition' as definition,
        unnest(string_to_array(audience ->> 'contacts', NULL)) as ad
    from targets
    join audience
    on audience ->> 'demography' like replace(target ->> 'definition', ' ', '_')
)
select
    definition,
    ad,
    count(person_id)
from statistics
group by definition, ad
order by definition, ad;

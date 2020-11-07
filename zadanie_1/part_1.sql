with audience_unnested as (
    select file_date, jsonb_array_elements(content) as audience
    from audience_json
),
targets_unnested as (
    select jsonb_array_elements(content) as target
    from targets_json
),
statistics as (
    select
        target ->> 'definition' as definition,
        file_date,
        audience -> 'person_id' as person_id,
        unnest(string_to_array(audience ->> 'contacts', NULL)) as ad
    from targets_unnested
    join audience_unnested
    on audience ->> 'demography' like replace(target ->> 'definition', ' ', '_')
)
select
    file_date as dzien,
    definition as grupa,
    ad as reklama,
    count(distinct person_id) as osob
from statistics
group by dzien, grupa, reklama
order by dzien, grupa, reklama;

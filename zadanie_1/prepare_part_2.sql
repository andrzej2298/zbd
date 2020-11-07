drop table if exists contacts;
drop table if exists demography;
drop table if exists targets;
drop table if exists ads;
drop table if exists users;

create table users (
    id serial primary key
);
create table ads (
    id serial primary key,
    name varchar unique
);
create table targets (
    id serial primary key,
    definition varchar
);
create table demography (
    day date,
    user_id serial,
    demography varchar,
    primary key (day, user_id),
    foreign key (user_id) references users (id)
);
create table contacts (
    day date,
    user_id serial,
    ad_id  serial,
    foreign key (user_id) references users (id),
    foreign key (ad_id) references ads (id)
);

with user_ids as (
    select distinct
    (jsonb_array_elements(content) -> 'person_id')::integer as user_id
    from audience_json
)
insert into users
select
    user_id
from user_ids
order by user_id;

insert into ads (name)
select distinct
    unnest(string_to_array(jsonb_array_elements(content) ->> 'contacts', null)) as ad
from audience_json
order by ad;

insert into targets (definition)
select
    jsonb_array_elements(content) ->> 'definition'
from targets_json;

with audience_unnested as (
    select file_date, jsonb_array_elements(content) as audience
    from audience_json
)
insert into demography
select
    file_date,
    (audience -> 'person_id')::int,
    audience ->> 'demography'
from audience_unnested;

with audience_unnested as (
    select file_date, jsonb_array_elements(content) as audience
    from audience_json
),
ad_views as (
    select
        file_date,
        (audience -> 'person_id')::int as person_id,
        unnest(string_to_array(audience ->> 'contacts', NULL)) as ad_name
    from audience_unnested
)
insert into contacts
select file_date, person_id, ads.id
from ad_views
join ads on ads.name = ad_name;

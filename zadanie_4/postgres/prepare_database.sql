drop table user_ad_requests;
create table user_ad_requests (
    id serial,
    cookie varchar,
    ip inet,
    dt timestamp
);

drop table user_info;
create table user_info (
    request_id serial,
    country varchar,
    city varchar
);

drop table emissions;
create table emissions (
    emission_id serial,
    request_id serial
);

drop table emissions_on_time;
create table emissions_on_time (
    emission_id serial
);

drop table emissions_delayed;
create table emissions_delayed (
    emission_id serial
);

drop table user_ad_requests;
create table user_ad_requests (
    id serial,
    cookie varchar,
    ip inet
);

drop table user_info;
create table user_info (
    request_id serial,
    country varchar,
    city varchar
);

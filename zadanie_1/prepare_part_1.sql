drop table if exists targets_json;
create table targets_json (content jsonb not null);
\set content `cat targets.json`
insert into targets_json values (:'content');
create index on targets_json using gin(content);

drop table if exists audience_json;
create table audience_json (
    file_date date not null primary key,
    content jsonb not null
);
\set content `cat audience-2019-01-01.json`
insert into audience_json values ('2019-01-01', :'content');
\set content `cat audience-2019-01-02.json`
insert into audience_json values ('2019-01-02', :'content');
\set content `cat audience-2019-01-03.json`
insert into audience_json values ('2019-01-03', :'content');
\set content `cat audience-2019-01-04.json`
insert into audience_json values ('2019-01-04', :'content');
\set content `cat audience-2019-01-05.json`
insert into audience_json values ('2019-01-05', :'content');
\set content `cat audience-2019-01-06.json`
insert into audience_json values ('2019-01-06', :'content');
\set content `cat audience-2019-01-07.json`
insert into audience_json values ('2019-01-07', :'content');
\set content `cat audience-2019-01-08.json`
insert into audience_json values ('2019-01-08', :'content');
\set content `cat audience-2019-01-09.json`
insert into audience_json values ('2019-01-09', :'content');
\set content `cat audience-2019-01-10.json`
insert into audience_json values ('2019-01-10', :'content');
\set content `cat audience-2019-01-11.json`
insert into audience_json values ('2019-01-11', :'content');
\set content `cat audience-2019-01-12.json`
insert into audience_json values ('2019-01-12', :'content');
\set content `cat audience-2019-01-13.json`
insert into audience_json values ('2019-01-13', :'content');
\set content `cat audience-2019-01-14.json`
insert into audience_json values ('2019-01-14', :'content');
\set content `cat audience-2019-01-15.json`
insert into audience_json values ('2019-01-15', :'content');
\set content `cat audience-2019-01-16.json`
insert into audience_json values ('2019-01-16', :'content');
\set content `cat audience-2019-01-17.json`
insert into audience_json values ('2019-01-17', :'content');
\set content `cat audience-2019-01-18.json`
insert into audience_json values ('2019-01-18', :'content');
\set content `cat audience-2019-01-19.json`
insert into audience_json values ('2019-01-19', :'content');
\set content `cat audience-2019-01-20.json`
insert into audience_json values ('2019-01-20', :'content');
\set content `cat audience-2019-01-21.json`
insert into audience_json values ('2019-01-21', :'content');
\set content `cat audience-2019-01-22.json`
insert into audience_json values ('2019-01-22', :'content');
\set content `cat audience-2019-01-23.json`
insert into audience_json values ('2019-01-23', :'content');
\set content `cat audience-2019-01-24.json`
insert into audience_json values ('2019-01-24', :'content');
\set content `cat audience-2019-01-25.json`
insert into audience_json values ('2019-01-25', :'content');
\set content `cat audience-2019-01-26.json`
insert into audience_json values ('2019-01-26', :'content');
\set content `cat audience-2019-01-27.json`
insert into audience_json values ('2019-01-27', :'content');
\set content `cat audience-2019-01-28.json`
insert into audience_json values ('2019-01-28', :'content');
\set content `cat audience-2019-01-29.json`
insert into audience_json values ('2019-01-29', :'content');
\set content `cat audience-2019-01-30.json`
insert into audience_json values ('2019-01-30', :'content');
\set content `cat audience-2019-01-31.json`
insert into audience_json values ('2019-01-31', :'content');
\set content `cat audience-2019-02-01.json`
insert into audience_json values ('2019-02-01', :'content');
\set content `cat audience-2019-02-02.json`
insert into audience_json values ('2019-02-02', :'content');
\set content `cat audience-2019-02-03.json`
insert into audience_json values ('2019-02-03', :'content');
\set content `cat audience-2019-02-04.json`
insert into audience_json values ('2019-02-04', :'content');
\set content `cat audience-2019-02-05.json`
insert into audience_json values ('2019-02-05', :'content');
\set content `cat audience-2019-02-06.json`
insert into audience_json values ('2019-02-06', :'content');
\set content `cat audience-2019-02-07.json`
insert into audience_json values ('2019-02-07', :'content');
\set content `cat audience-2019-02-08.json`
insert into audience_json values ('2019-02-08', :'content');
\set content `cat audience-2019-02-09.json`
insert into audience_json values ('2019-02-09', :'content');
\set content `cat audience-2019-02-10.json`
insert into audience_json values ('2019-02-10', :'content');
\set content `cat audience-2019-02-11.json`
insert into audience_json values ('2019-02-11', :'content');
\set content `cat audience-2019-02-12.json`
insert into audience_json values ('2019-02-12', :'content');
\set content `cat audience-2019-02-13.json`
insert into audience_json values ('2019-02-13', :'content');
\set content `cat audience-2019-02-14.json`
insert into audience_json values ('2019-02-14', :'content');
\set content `cat audience-2019-02-15.json`
insert into audience_json values ('2019-02-15', :'content');
\set content `cat audience-2019-02-16.json`
insert into audience_json values ('2019-02-16', :'content');
\set content `cat audience-2019-02-17.json`
insert into audience_json values ('2019-02-17', :'content');
\set content `cat audience-2019-02-18.json`
insert into audience_json values ('2019-02-18', :'content');
\set content `cat audience-2019-02-19.json`
insert into audience_json values ('2019-02-19', :'content');
\set content `cat audience-2019-02-20.json`
insert into audience_json values ('2019-02-20', :'content');
\set content `cat audience-2019-02-21.json`
insert into audience_json values ('2019-02-21', :'content');
\set content `cat audience-2019-02-22.json`
insert into audience_json values ('2019-02-22', :'content');
\set content `cat audience-2019-02-23.json`
insert into audience_json values ('2019-02-23', :'content');
\set content `cat audience-2019-02-24.json`
insert into audience_json values ('2019-02-24', :'content');
\set content `cat audience-2019-02-25.json`
insert into audience_json values ('2019-02-25', :'content');
\set content `cat audience-2019-02-26.json`
insert into audience_json values ('2019-02-26', :'content');
\set content `cat audience-2019-02-27.json`
insert into audience_json values ('2019-02-27', :'content');
\set content `cat audience-2019-02-28.json`
insert into audience_json values ('2019-02-28', :'content');
\set content `cat audience-2019-03-01.json`
insert into audience_json values ('2019-03-01', :'content');
\set content `cat audience-2019-03-02.json`
insert into audience_json values ('2019-03-02', :'content');
\set content `cat audience-2019-03-03.json`
insert into audience_json values ('2019-03-03', :'content');
\set content `cat audience-2019-03-04.json`
insert into audience_json values ('2019-03-04', :'content');
\set content `cat audience-2019-03-05.json`
insert into audience_json values ('2019-03-05', :'content');
\set content `cat audience-2019-03-06.json`
insert into audience_json values ('2019-03-06', :'content');
\set content `cat audience-2019-03-07.json`
insert into audience_json values ('2019-03-07', :'content');
\set content `cat audience-2019-03-08.json`
insert into audience_json values ('2019-03-08', :'content');
\set content `cat audience-2019-03-09.json`
insert into audience_json values ('2019-03-09', :'content');
\set content `cat audience-2019-03-10.json`
insert into audience_json values ('2019-03-10', :'content');
\set content `cat audience-2019-03-11.json`
insert into audience_json values ('2019-03-11', :'content');
\set content `cat audience-2019-03-12.json`
insert into audience_json values ('2019-03-12', :'content');
\set content `cat audience-2019-03-13.json`
insert into audience_json values ('2019-03-13', :'content');
\set content `cat audience-2019-03-14.json`
insert into audience_json values ('2019-03-14', :'content');
\set content `cat audience-2019-03-15.json`
insert into audience_json values ('2019-03-15', :'content');
\set content `cat audience-2019-03-16.json`
insert into audience_json values ('2019-03-16', :'content');
\set content `cat audience-2019-03-17.json`
insert into audience_json values ('2019-03-17', :'content');
\set content `cat audience-2019-03-18.json`
insert into audience_json values ('2019-03-18', :'content');
\set content `cat audience-2019-03-19.json`
insert into audience_json values ('2019-03-19', :'content');
\set content `cat audience-2019-03-20.json`
insert into audience_json values ('2019-03-20', :'content');
\set content `cat audience-2019-03-21.json`
insert into audience_json values ('2019-03-21', :'content');
\set content `cat audience-2019-03-22.json`
insert into audience_json values ('2019-03-22', :'content');
\set content `cat audience-2019-03-23.json`
insert into audience_json values ('2019-03-23', :'content');
\set content `cat audience-2019-03-24.json`
insert into audience_json values ('2019-03-24', :'content');
\set content `cat audience-2019-03-25.json`
insert into audience_json values ('2019-03-25', :'content');
\set content `cat audience-2019-03-26.json`
insert into audience_json values ('2019-03-26', :'content');
\set content `cat audience-2019-03-27.json`
insert into audience_json values ('2019-03-27', :'content');
\set content `cat audience-2019-03-28.json`
insert into audience_json values ('2019-03-28', :'content');
\set content `cat audience-2019-03-29.json`
insert into audience_json values ('2019-03-29', :'content');
\set content `cat audience-2019-03-30.json`
insert into audience_json values ('2019-03-30', :'content');
\set content `cat audience-2019-03-31.json`
insert into audience_json values ('2019-03-31', :'content');
\set content `cat audience-2019-04-01.json`
insert into audience_json values ('2019-04-01', :'content');
\set content `cat audience-2019-04-02.json`
insert into audience_json values ('2019-04-02', :'content');
\set content `cat audience-2019-04-03.json`
insert into audience_json values ('2019-04-03', :'content');
\set content `cat audience-2019-04-04.json`
insert into audience_json values ('2019-04-04', :'content');
\set content `cat audience-2019-04-05.json`
insert into audience_json values ('2019-04-05', :'content');
\set content `cat audience-2019-04-06.json`
insert into audience_json values ('2019-04-06', :'content');
\set content `cat audience-2019-04-07.json`
insert into audience_json values ('2019-04-07', :'content');
\set content `cat audience-2019-04-08.json`
insert into audience_json values ('2019-04-08', :'content');
\set content `cat audience-2019-04-09.json`
insert into audience_json values ('2019-04-09', :'content');
\set content `cat audience-2019-04-10.json`
insert into audience_json values ('2019-04-10', :'content');
\set content `cat audience-2019-04-11.json`
insert into audience_json values ('2019-04-11', :'content');
\set content `cat audience-2019-04-12.json`
insert into audience_json values ('2019-04-12', :'content');
\set content `cat audience-2019-04-13.json`
insert into audience_json values ('2019-04-13', :'content');
\set content `cat audience-2019-04-14.json`
insert into audience_json values ('2019-04-14', :'content');
\set content `cat audience-2019-04-15.json`
insert into audience_json values ('2019-04-15', :'content');
\set content `cat audience-2019-04-16.json`
insert into audience_json values ('2019-04-16', :'content');
\set content `cat audience-2019-04-17.json`
insert into audience_json values ('2019-04-17', :'content');
\set content `cat audience-2019-04-18.json`
insert into audience_json values ('2019-04-18', :'content');
\set content `cat audience-2019-04-19.json`
insert into audience_json values ('2019-04-19', :'content');
\set content `cat audience-2019-04-20.json`
insert into audience_json values ('2019-04-20', :'content');
\set content `cat audience-2019-04-21.json`
insert into audience_json values ('2019-04-21', :'content');
\set content `cat audience-2019-04-22.json`
insert into audience_json values ('2019-04-22', :'content');
\set content `cat audience-2019-04-23.json`
insert into audience_json values ('2019-04-23', :'content');
\set content `cat audience-2019-04-24.json`
insert into audience_json values ('2019-04-24', :'content');
\set content `cat audience-2019-04-25.json`
insert into audience_json values ('2019-04-25', :'content');
\set content `cat audience-2019-04-26.json`
insert into audience_json values ('2019-04-26', :'content');
\set content `cat audience-2019-04-27.json`
insert into audience_json values ('2019-04-27', :'content');
\set content `cat audience-2019-04-28.json`
insert into audience_json values ('2019-04-28', :'content');
\set content `cat audience-2019-04-29.json`
insert into audience_json values ('2019-04-29', :'content');
\set content `cat audience-2019-04-30.json`
insert into audience_json values ('2019-04-30', :'content');

create index on audience_json using gin(content);

drop table if exists podobny_slodycz;
drop table if exists slodycz_w_paczce;
drop table if exists paczka;
drop table if exists slodycz_w_magazynie;

create table slodycz_w_magazynie (
    nazwa varchar,
    ilosc_pozostalych int check ( ilosc_pozostalych >= 0 ),
    primary key (nazwa)
);

create table paczka (
    identyfikator serial,
    kraj varchar,
    opis_obdarowanego varchar,
    primary key (identyfikator)
);

create table slodycz_w_paczce (
    identyfikator_paczki serial,
    slodycz varchar,
    ilosc int,
    foreign key (identyfikator_paczki) references paczka (identyfikator),
    foreign key (slodycz) references slodycz_w_magazynie (nazwa)
);

create table podobny_slodycz (
    ktory_slodycz_jest_podobny varchar,
    do_czego_slodycz_jest_podobny varchar,
    podobienstwo float check ( podobienstwo >= 0 and podobienstwo <= 1 ),
    foreign key (ktory_slodycz_jest_podobny) references slodycz_w_magazynie (nazwa),
    foreign key (do_czego_slodycz_jest_podobny) references slodycz_w_magazynie (nazwa)
);

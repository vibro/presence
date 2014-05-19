drop table if exists session;
create table session(
       SESSID varchar(30) primary key,
       UID integer,
       TID integer,
       status enum("p","m","c"),
       foreign key (UID) references user (UID),
       foreign key (TID) references team (TID)
);
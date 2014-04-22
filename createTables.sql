drop table if exists user;
create table user(
	UID 	integer auto_increment primary key,
	email 	varchar(30),
	name 	varchar(30),
	dob 	date,
	phnum	char(11),
	nickname varchar(30)
);

drop table if exists userpass;
create table userpass(
       id       int primary key,
       password char(15),   
       foreign key (id) references user(UID)
);

drop table if exists team;
create table team(
	TID integer auto_increment primary key,
	name varchar(50),
	manager integer,
	location varchar(50)
);

drop table if exists player;
create table player(
	PID 	integer,
	team 	integer,
	position varchar(30),
	
	foreign key (PID) references user(UID),
	foreign key (team) references team(TID)
);

drop table if exists coach;
create table coach(
	CID 	integer,
	team 	integer,

	foreign key (CID) references user(UID),
	foreign key (team) references team(TID)
);


-- edited by Lulu on 21 April
drop table if exists event;
create table event(
	EID  	integer auto_increment primary key,
	host_id	integer,
	location varchar(50),
	event_date date,
	foreign key (host_id) references team(TID)
);




drop table if exists attend;
create table attend(
	EID	integer,
	UID	integer,
	
	foreign key (EID) references event(EID),
	foreign key (UID) references user(UID)
);

create table user(
	UID 	integer auto_increment primary key,
	email 	varchar(30),
	name 	varchar(30),
	dob 	date,
	phnum char(11),
	nickname varchar(30)
);

create table userpass(
       id       int primary key,
       password char(15),   
       primary key (id),
       foreign key (id) references user(UID)
);

create table team(
	TID integer auto_increment primary key,
	name varchar(50),
	manager integer,
	location varchar(50),
);

create table player(
	PID 	integer,
	team 	integer,
	position varchar(30),
	
	foreign key (PID) references user(UID),
	foreign key (team) references team(TID)
);

create table coach(
	CID 	integer,
	team 	integer,

	foreign key (CID) references user(UID),
	foreign key (team) references team(TID)
);

create table event(
	EID  	integer auto_increment primary key,
	host 	integer,

	foreign key (host) references team(TID)
);

create table attend(
	EID	integer,
	UID	integer,
	
	foreign key (EID) references event(EID),
	foreign key (UID) references user(UID)
);


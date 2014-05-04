-- Test data for our Rugsbee file.
-- Inserts a few users into the user database, then creates a team
-- Then create an event associated with the team.

-- delete if in the table() prevents multiple 

DELETE from user;
DELETE from team;
DELETE from player;


-- create some users
INSERT INTO user(email, name, dob, nickname) VALUES ("harry@hogwarts.com", "Harry Potter", 31-07-1980, "The Chosen One");
INSERT INTO user(email, name, dob, nickname) VALUES ("ronald@hogwarts.com", "Ron Weasley", 01-03-1980, "Won Won");
INSERT INTO user(email, name, dob, nickname) VALUES ("hermione@hogwarts.com", "Hermione Granger", 15-09-1979, "Hermy");

-- create a team
-- INSERT INTO team(name, location) VALUES("Rugsbee", "Wellesley");
INSERT INTO team(name, manager, location) VALUES("DA", 3, "Hogwarts"); -- hopefully hermione is managing


-- add players onto team 
INSERT INTO player(PID, team, position) VALUES(1, 1, "Seeker"); -- Harry
INSERT INTO player(PID, team, position) VALUES(2, 1, "Keeper"); -- Ron
INSERT INTO player(PID, team, position) VALUES(3, 1, "Chaser"); -- Hermione


-- create event
INSERT INTO event(host_id, location) VALUES(1, "Astronomy Tower"); -- hopefully hosted by Hogwarts
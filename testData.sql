-- Test data for our Rugsbee file.
-- Inserts a few users into the user database, then creates a team
-- Then create an event associated with the team.

-- delete if in the table() prevents multiple 

DELETE from user;
DELETE from team;
DELETE from player;


-- create some users
INSERT INTO user(email, name, dob, nickname) VALUES ("harry@hogwarts.com", "Harry Potter", 1980-07-31, "The Chosen One");
INSERT INTO user(email, name, dob, nickname) VALUES ("ronald@hogwarts.com", "Ron Weasley", 1980-03-01, "Won Won");
INSERT INTO user(email, name, dob, nickname) VALUES ("hermione@hogwarts.com", "Hermione Granger", 1979-09-17, "Hermy");

-- create a team
-- INSERT INTO team(name, location) VALUES("Rugsbee", "Wellesley");
INSERT INTO team(name, manager, location) VALUES("DA", 3, "Hogwarts"); -- hopefully hermione is managing


-- add players onto team 
INSERT INTO player(PID, team, position) VALUES(1, 1, "Seeker"); -- Harry
INSERT INTO player(PID, team, position) VALUES(2, 1, "Keeper"); -- Ron
INSERT INTO player(PID, team, position) VALUES(3, 1, "Chaser"); -- Hermione


-- create event
INSERT INTO event(host_id, location,event_name) VALUES(1, "Astronomy Tower","Practice"); -- hopefully hosted by Hogwarts

-- attend events
INSERT INTO attend(EID,UID,status) VALUES(1, 1,"y"); -- Harry goes to practice at astronomy tower
INSERT INTO attend(EID,UID,status) VALUES(1, 2,"m"); -- Ron goes to practice at astronomy tower
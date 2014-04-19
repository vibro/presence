-- Test data for our Rugsbee file.
-- Inserts a few users into the user database, then creates a team
-- Then create an event associated with the team.

-- delete if in the table() prevents multiple 

DELETE from user;
DELETE from team;
DELETE from player;


-- create some users
INSERT INTO user(name,phnum) VALUES("Tori", 12345678910);
INSERT INTO user(name,phnum) VALUES("Lulu", 10987654321);

-- create a team
INSERT INTO team(name, location) VALUES("Rugsbee", "Wellesley");


-- add players onto team
-- INSERT INTO player() VALUES();

-- create event
-- INSERT INTO event() VALUES();
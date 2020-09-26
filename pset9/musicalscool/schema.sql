DROP TABLE IF EXISTS users;

CREATE TABLE 'users' (
    'id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
    'username' text NOT NULL, 
    'hash' text NOT NULL
);

DROP TABLE IF EXISTS students;

CREATE TABLE 'students' (
    'ID' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
    'Firstname' text NOT NULL, 
    'Lastname' text NOT NULL, 
    'Birthdate' date NOT NULL, 
    'Class' text NOT NULL, 
    'Phone' text NOT NULL, 
    'Phone2' text, 
    'Email' text NOT NULL, 
    'Email2' text,
    'Showtime' text, 
    'Role' text, 
    'Notes' text
);
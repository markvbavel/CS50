DROP TABLE IF EXISTS users;

CREATE TABLE 'users' (
    'id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
    'username' text NOT NULL, 
    'hash' text NOT NULL
);

DROP TABLE IF EXISTS students;
CREATE TABLE 'students' (
    'id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
    'first' text NOT NULL, 
    'middle' text, 
    'last' text NOT NULL, 
    'birth' date NOT NULL, 
    'city' text NOT NULL, 
    'class' text NOT NULL, 
    'tel_1' integer NOT NULL, 
    'tel_2' integer, 
    'email_1' text NOT NULL, 
    'email_2' text, 
    'cast' text, 
    'role' text, 
    'notes' text
);


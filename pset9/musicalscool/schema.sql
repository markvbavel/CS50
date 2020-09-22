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
    'last' text NOT NULL, 
    'birth' date NOT NULL, 
    'class' text NOT NULL, 
    'tel_1' text NOT NULL, 
    'tel_2' text, 
    'email_1' text NOT NULL, 
    'email_2' text, 
    'cast' text, 
    'role' text, 
    'notes' text
);

DROP VIRTUAL TABLE IF EXISTS students_v;

CREATE VIRTUAL TABLE 'students_v' (
    'first' text NOT NULL, 
    'last' text NOT NULL, 
    'birth' date NOT NULL, 
    'class' text NOT NULL, 
    'tel_1' text NOT NULL, 
    'tel_2' text, 
    'email_1' text NOT NULL, 
    'email_2' text, 
    'cast' text, 
    'role' text, 
    'notes' text
);

CREATE TRIGGER after_hotels_reviews_insert AFTER INSERT ON hotels_reviews BEGIN
  INSERT INTO students_v (
    rowid,
    review
  )
  VALUES(
    new.id,
    new.review
  );
END;
import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
            ("test", "test"))

cur.execute("INSERT INTO students (first, middle, last, tel_1, birth, email_1, city, class) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("test", "test", "test", "1234567890", "01-01-2001", "test@test.com", "Test", "Test"))            

connection.commit()
connection.close()
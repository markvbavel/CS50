import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


conn = sqlite3.connect('database.db')

with open('schema.sql') as f:
    conn.executescript(f.read())

"""cursor = conn.cursor()
hash = generate_password_hash("test")

cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
            ("test", hash))

cursor.execute("INSERT INTO students (first, middle, last, tel_1, birth, email_1, city, class) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("test", "test", "test", "1234567890", "01-01-2001", "test@test.com", "Test", "Test"))            
"""
conn.commit()
conn.close()
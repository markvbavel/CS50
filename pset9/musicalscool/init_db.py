import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


conn = sqlite3.connect('database.db')

with open('schema.sql') as f:
    conn.executescript(f.read())

conn.commit()
conn.close()
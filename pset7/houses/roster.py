# Program that outputs a list of all students in a given house. Data collected from a SQLite3 database

from cs50 import SQL
from sys import argv

# Ensure correct number of command-line arguments
if len(argv) != 2:
    print("Error 1. \nUsage: python import.py database.csv")
    exit(1)

key = argv[1]
print(key)

# Connects database
db = SQL("sqlite:///students.db")

# Selects relevant data from database, sorted by last name, then by first name
table = db.execute('SELECT * FROM students ORDER BY last, first')
for row in table:

    # Check if 'house' field matches the key
    if row['house'] != key:
        continue

    # Print 'first' and 'last' when there's no middle name
    if row['middle'] == None:
        print('{} {}, born {}'.format(row['first'], row['last'], row['birth']))

    # Print all name fields when there is a middle name present
    else:
        print('{} {} {}, born {}'.format(row['first'], row['middle'], row['last'], row['birth']))

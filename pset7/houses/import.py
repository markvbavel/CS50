# Program that imports data from a CSV spreadsheet into a sqlite database

from cs50 import SQL
from sys import argv
import csv

# Ensure correct number of command-line arguments
if len(argv) != 2:
    print("Error 1. \nUsage: python import.py database.csv")
    exit(1)

# Ensure correct file extension
if (argv[1].lower().endswith('.csv') == False):
    print("Error 2. \nPlease enter a .csv file")
    exit(2)

# Connects database
db = SQL("sqlite:///students.db")

# Open CSV file
with open(argv[1], 'r') as f:

    # Create DictReader. Gets 'name', 'house', 'birth'
    dreader = csv.DictReader(f)

    # Iterate over rows
    for row in dreader:

        # Print contents of each field
        print("{} | {} | {}".format(row['name'], row['house'], row['birth']))

        # New list to split name fields
        names = []

        # Iterate over the name field, using ' ' to check how many items are there
        for fields in row['name'].split(' '):
            names.append(fields)

        # I.e. if the student has no middle name
        if len(names) == 2:
            db.execute('INSERT INTO students (first, last, house, birth) VALUES (?, ?, ?, ?)',
                       names[0], names[1], row['house'], row['birth'])

        # If the student has a middle name
        elif len(names) == 3:
            db.execute('INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)',
                       names[0], names[1], names[2], row['house'], row['birth'])

# https://www.reddit.com/r/cs50/comments/gbdhwd/2020_pset_7_houses_help/
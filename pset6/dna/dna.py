from sys import argv, exit
import csv
import re


# Empty dict
DNA = {}


#STEP 1: Ensure correct usage

# Ensure correct number of arguments at command-line
if len(argv) != 3:
    print("Usage: python dna.py database sequence")
    exit(1)
# Ensure correct file extension at argv[1]
if (argv[1].lower().endswith('.csv') == False):
    print("Please enter a .csv file")
    exit(2)
# Ensure correct file extension at argv[2]
if (argv[2].lower().endswith('.txt') == False):
    print("Please enter a .txt file")
    exit(3)


#STEP 2: Open, read and store CSV file contents

# Open CSV file
with open(argv[1], 'r') as file1:
    csvread = csv.reader(file1)
    # rows[i] -> name and repeat counts
    rows = list(csvread)
    # prints ['AGATC', 'AATG']...
    headers = rows[0][1:]


#STEP 3: Open, read and store TXT file contents

# Open TXT file
with open(argv[2], 'r') as file2:
    txtread = file2.read()


#STEP 4: Search for patterns in TXT file

    # Iterate over headers
    for i in range(len(headers)):
        # Create a temp max variable
        max_temp = 0
        # Creates a search pattern for the i'th header
        pattern = re.compile(fr'({headers[i]})+')
        # Search TXT for the pattern
        for match in re.finditer(pattern, txtread):
            # Calculates length of match
            match_length = match.end() - match.start()
            # Calculates longest number of matches
            match_run = match_length / len(headers[i])

            if match_run > max_temp:
                max_temp = match_run

            # Creates new key: value pair in dict
            DNA[headers[i]] = int(max_temp)


#STEP 5: Compare database with samples

# Open csv again
with open(argv[1], 'r') as file1:
    csvread = csv.DictReader(file1)
    # Iterate trough rows
    for person in csvread:
        # Integer to keep track of how many of the STR's match
        match_count = 0
        # Iterate trough all col (STR's)
        for col in DNA:
            if (DNA[col] == int(person[col])):
                match_count += 1
        # A person matches every STR
        if match_count == len(headers):
            print(person['name'])
            exit(0)
    # When no-one is a match
    print("No match")
    exit(1)
from cs50 import get_string


def main():

    # Get input
    text = get_string("Text: ")

    # Check for letters in the text
    count_letters = 0
    for i in text:
        if (i.isalpha()) == True:
            count_letters += 1

    # Check the number of words in text
    count_words = 1
    for i in text:
        if (i.isspace()) == True:
            count_words += 1

    # Check the number of sentences in text
    count_sentences = 0
    for i in text:
        if "!" in i:
            count_sentences += 1
        if "?" in i:
            count_sentences += 1
        if "." in i:
            count_sentences += 1

    # Print
    print(f"{count_letters} letter(s)")
    print(f"{count_words} word(s)")
    print(f"{count_sentences} sentence(s)")

    # Calculate L and S for formula
    L = (count_letters / count_words) * 100
    S = (count_sentences / count_words) * 100

    # Use the formula and round the output
    index = 0.0588 * L - 0.296 * S - 15.8
    index = round(index)

    # Print the appropriate grade assignment
    if (index <= 16 and index >= 1):
        print(f"Grade {index}")
    elif (index > 16):
        print("Grade 16+")
    elif (index < 1):
        print("Before Grade 1")


main()
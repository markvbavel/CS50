# Program that prints a left-alligned pyramid of hashes according to the user's input
from cs50 import get_int


def main():
    h = get_height()

    for i in range(h):
        for j in range(h):
            if i + j < h - 1:
                print(" ", end="")
            else:
                print("#", end="")
        print()


def get_height():
    while True:
        n = get_int("number 1-8: ")
        if n >= 1 and n <= 8:
            break
    return n


main()
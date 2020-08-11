# Program that calculates how many coins are needed to return the requested amount of change
from cs50 import get_float


def main():
    # Get input from the user
    while True:
        n = get_float("Change owned: ")
        if n >= 0:
            break
    # Round the float input to an integer
    cents = round(n * 100)

    # Initialize quarters, dimes, nickels, pennies and coins
    q = 0
    d = 0
    n = 0
    p = 0
    coins = 0

    # Check for quarters
    while (cents >= 25):
        q += 1
        coins += 1
        cents = cents - 25
    print(f"Quarters: {q}")
    print(f"Cents after quarters: {cents}")

    # Check for dimes
    while (cents >= 10):
        d += 1
        coins += 1
        cents = cents - 10
    print(f"Dimes: {d}")
    print(f"Cents after dimes: {cents}")

    # Check for nickels
    while (cents >= 5):
        n += 1
        coins += 1
        cents = cents - 5
    print(f"Nickels: {n}")
    print(f"Cents after nickels: {cents}")

    # Check for pennies
    while (cents >= 1):
        p += 1
        coins += 1
        cents = cents - 1
    print(f"Pennies: {p}")
    print(f"Cents after pennies: {cents}")

    print(f"Total coins: {coins}")


main()
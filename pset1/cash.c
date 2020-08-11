// Greedy algorithm. Use as little coins as possible to hand the customer their cash.
// Quarters: 0.25, Dimes: 0.10, Nickels: 0.05, Pennies: 0.01
// Prints every coin used. Not for submission

// Conditions and declarations
#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)

{
    // Prompt user for input
    float dollars;
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars <= 0);

    // Convert float to int, making input in cents
    int cents = round(dollars * 100);
    printf("Cents: %i\n", cents);

    int coins = 0;

    for (int q = 1; (cents / 25 >= 1); q++)
    {
        printf("quarters: %i\n", q);
        cents = cents - 25;
        coins++;
    }
    for (int d = 1; cents / 10 >= 1; d++)
    {
        printf("dimes: %i\n", d);
        cents = cents - 10;
        coins++;
    }
    for (int n = 1; cents / 5 >= 1; n++)
    {
        printf("nickels: %i\n", n);
        cents = cents - 5;
        coins++;
    }
    for (int p = 1; cents / 1 >= 1; p++)
    {
        printf("pennies: %i\n", p);
        cents = cents - 1;
        coins++;
    }
    printf("Total coins used: %i\n", coins);
    printf("Remaining change: %i\n", cents);
}
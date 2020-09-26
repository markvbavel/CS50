// Program that runs a basic greedy algorith. 
// User inputs the change owed in Dollars, program outputs the ammount of coins used.
// Quarters: 0.25, Dimes: 0.10, Nickels: 0.05, Pennies: 0.01

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
    int coins = 0;

    // Loop for quarters
    for (int q = 1; (cents / 25 >= 1); q++)
    {
        cents = cents - 25;
        coins++;
    }

    // Loop for dimes
    for (int d = 1; cents / 10 >= 1; d++)
    {
        cents = cents - 10;
        coins++;
    }

    // Loop for nickels
    for (int n = 1; cents / 5 >= 1; n++)
    {
        cents = cents - 5;
        coins++;
    }

    // Loop for pennies
    for (int p = 1; cents / 1 >= 1; p++)
    {
        cents = cents - 1;
        coins++;
    }

    // Prints number of coins used
    printf("Total coins used: %i\n", coins);
}
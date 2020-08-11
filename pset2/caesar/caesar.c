//Program that encryps a message with a key provided by the user. Outputs the encrypted message.

//Libraries
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>


// Main
int main(int argc, string argv[])
{
    
    // Ensures correct number of arguments
    if (argc == 2)
    {
        string s = (argv[1]);

        // Iterates over the provided key, checks if it's an integer
        for (int i = 0, n = strlen(s); i < n; i++)
        {
            bool x = isdigit(s[i]);
            if (x == false)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }

        // Converts string to integer
        int k = atoi(s);
        printf("Key: %i\n", k);

        // Promt user for plain text input
        string p = get_string("Plain text: ");

        printf("ciphertext: ");

        // Iterates over the plain text
        for (int i = 0, n = strlen(p); i < n; i++)
        {
            // Checks if the character is alphanumerical
            bool x = isalpha(p[i]);
            if (x == true)
            {
                // Adjust ASCII values for upper- or lowercase
                bool y = isupper(p[i]);
                if (y == true)
                {
                    int u = (((- 65) + (p[i] + k)) % 26);
                    // Prints converted ASCII character
                    printf("%c", (char) u + 65);
                }
                else
                {
                    int l = (((-97) + (p[i] + k)) % 26);
                    // Prints converted ASCII character
                    printf("%c", (char) l + 97);
                }
            }
            
            // No need to convert if it's not alphanumerical
            else
            {
                printf("%c", p[i]);
            }
        }
        printf("\n");
        return 0;
    }

    // Error when argc != 2
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}
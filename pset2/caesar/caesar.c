//Program that encryps a message with a key provided by the user. Outputs the encrypted message as letters.

//Libraries
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

//Declarations and scope

//Main

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        string s = (argv[1]);

        for (int i = 0, n = strlen(s); i < n; i++)
        {
            bool x = isdigit(s[i]);
            if (x == false)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }

        int k = atoi(s);
        printf("Key: %i\n", k);

        string p = get_string("Plain text: ");

        printf("ciphertext: ");
        for (int i = 0, n = strlen(p); i < n; i++)
        {
            bool x = isalpha(p[i]);
            if (x == true)
            {
                bool y = isupper(p[i]);
                if (y == true)
                {
                    int u = (((- 65) + (p[i] + k)) % 26);
                    printf("%c", (char) u + 65);
                }
                else
                {
                    int l = (((-97) + (p[i] + k)) % 26);
                    printf("%c", (char) l + 97);
                }
            }
            else
            {
                printf("%c", p[i]);
            }
        }
        printf("\n");
        return 0;
    }

    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}

//Functions
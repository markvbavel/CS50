/*Recover: a program to recover lost JPEG files.

PSEUDOCODE
Open memory card
Repeat untill end of card:
Read 512 bytes into a buffer
If start of new JPEG
If first JPEG
Write 000.jpg .....
Else
Close the previous file
Open new file
Else
If already found JPEG
Keep writing to the jpeg file. It's the second block.
Close any remaining files */

// Includes
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// Function declarations
typedef uint8_t BYTE;

// Main
int main(int argc, char *argv[])
{
    // Check for correct usage
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open memory card
    FILE *file = fopen(argv[1], "r");
    // Check for errors while opening the file
    if (file == NULL)
    {
        printf("Error opening file.\n");
        return 2;
    }

    BYTE buffer[512]; // Buffer of 512 bytes
    FILE *img = NULL; // outfile, set to be blank
    int jpg_count = 0; // keep track of number of JPEG's
    char filename[8]; // Name: ###.jpg\0

    // Read trough the source file, one buffer size at a time, untill there are no more buffer size blocks to read
    while (fread(buffer, sizeof(buffer), 1, file) == 1)
    {
        // first four bytes. Specified in the short
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer [3] & 0xf0) == 0xe0))
        {
            // First JPEG
            if (jpg_count == 0)
            {
                sprintf(filename, "%03i.jpg", jpg_count); // Name for the new file
                img = fopen(filename, "w"); // open the new file, ready to be written into
                fwrite(buffer, sizeof(buffer), 1, img); // write the contents of the buffer into the new file
                jpg_count++; // add one to the jpg_count
            }

            // All other JPEG's
            else
            {
                fclose(img); // close the current open file
                sprintf(filename, "%03i.jpg", jpg_count); // Name the file
                img = fopen(filename, "w"); // Open the new file
                fwrite(buffer, sizeof(buffer), 1, img); // Write contents of buffer
                jpg_count++; // Add to counter
            }
        }
        else if (jpg_count != 0)
        {
            fwrite(buffer, sizeof(buffer), 1, img);
        }
    }
    return 0;
}

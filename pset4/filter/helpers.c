// Includes
#include <math.h>
#include "helpers.h"
#include <stdio.h>

// Function prototypes
void swap(RGBTRIPLE *a, RGBTRIPLE *b);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate trough all rows (height)
    for (int i = 0; i < height; i++)
    {
        // Iterate trough all collums (width)
        for (int j = 0; j < width; j++)
        {
            // Check rgbtRed && rgbtGreen && rgbtBlue value and store it. (Hexadecimal??)
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            // Calculate average of the three values
            float faverage = ((float) red + (float) green + (float) blue) / 3;
            // Round average to nearest integer
            int iaverage = round(faverage);

            // Change rgbtRed && rgbtGreen && rgbtBlue to the stored value
            image[i][j].rgbtRed = iaverage;
            image[i][j].rgbtGreen = iaverage;
            image[i][j].rgbtBlue = iaverage;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate trough all rows
    for (int i = 0; i < height; i++)
    {
        // Iterate trough all collums
        for (int j = 0; j < width; j++)
        {
            // Check RGBT values and store them in an integer
            int orgRed = image[i][j].rgbtRed;
            int orgGreen = image[i][j].rgbtGreen;
            int orgBlue = image[i][j].rgbtBlue;

            // Apply sepia formula to RGBT values and round the output to the nearest integer
            int sepiaRed = round((orgRed * 0.393) + (orgGreen * 0.769) + (orgBlue * 0.189));

            // Ensure that sepiaRed 0 >< 255
            if (sepiaRed < 0)
            {
                sepiaRed = 0;
            }
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            // Change origional rgbt values to their new sepia values
            image[i][j].rgbtRed = sepiaRed;

            // Do the same for Green
            int sepiaGreen = round((orgRed * 0.349) + (orgGreen * 0.686) + (orgBlue * 0.168));

            if (sepiaGreen < 0)
            {
                sepiaGreen = 0;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            image[i][j].rgbtGreen = sepiaGreen;

            // Do the same for Blue;
            int sepiaBlue = round((orgRed * 0.272) + (orgGreen * 0.534) + (orgBlue * 0.131));

            if (sepiaBlue < 0)
            {
                sepiaBlue = 0;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate trough rows
    for (int i = 0; i < height; i++)
    {
        int n = 1;
        for (int j = 0; j < (width / 2); j++)
        {
            swap(&image[i][j], &image[i][width - n]);
            n++;
        }
    }
    return;
}

void swap(RGBTRIPLE *a, RGBTRIPLE *b)
{
    RGBTRIPLE temp;
    RGBTRIPLE temp2;
    temp = *a;
    temp2 = *b;
    *a = temp2;
    *b = temp;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // 1 | 2 | 3
    // 4 | 5 | 6
    // 7 | 8 | 9

    // Make a copy of the original picture
    RGBTRIPLE copy[height][width];
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            copy[h][w] = image[h][w];
        }
    }

    // For every pixel
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            // Declare sum variables and a counter, initialize to current pixel (5)
            int count = 0;
            int sumRed = 0;
            int sumGreen = 0;
            int sumBlue = 0;

            // Loop over horizontal adjecent pixels (range: -1 - 1) (1-3)
            for (int k = -1; k < 2; k++)
            {
                // Loop over vertical adjecent pixels (range: -1 - 1) (2-8)
                for (int l = -1; l < 2; l++)
                {
                    int x = h + k;
                    int y = w + l;

                    if (x >= 0 && x < height && y >= 0 && y < width)
                    {
                        // image = [[1, 2, 3, 4],
                        //          [5, 6, 7, 8],
                        // .        [9, 10, 11, 12],
                        // .        [13, 14, 15, [r g b]]]
                        sumRed += image[x][y].rgbtRed;
                        sumGreen += image[x][y].rgbtGreen;
                        sumBlue += image[x][y].rgbtBlue;
                        count ++;
                    }
                }
            }

            copy[h][w].rgbtRed = round((float)sumRed / count);
            copy[h][w].rgbtGreen = round((float)sumGreen / count);
            copy[h][w].rgbtBlue = round((float)sumBlue / count);
        }
    }

    // Copy the altered pixel to the original picture
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;
}

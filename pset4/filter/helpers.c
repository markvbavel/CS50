// Helper functions for filter.c

// Includes
#include <math.h>
#include "helpers.h"
#include <stdio.h>

// Function prototypes
void swap(RGBTRIPLE *a, RGBTRIPLE *b);

// Converts image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate trough rows (height)

    // i = h
    // j = w
    for (int h = 0; h < height; h++)
    {
        // Iterate trough collums (width)
        for (int w = 0; w < width; w++)
        {
            // Check rgbtRed, rgbtGreen, rgbtBlue value and store it
            int red = image[h][w].rgbtRed;
            int green = image[h][w].rgbtGreen;
            int blue = image[h][w].rgbtBlue;

            // Calculate average of the three values
            float faverage = ((float) red + (float) green + (float) blue) / 3;
            // Round average to nearest integer
            int iaverage = round(faverage);

            // Change rgbtRed && rgbtGreen && rgbtBlue to the stored value
            image[h][w].rgbtRed = iaverage;
            image[h][w].rgbtGreen = iaverage;
            image[h][w].rgbtBlue = iaverage;
        }
    }
    return;
}

// Converts image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate trough rows
    for (int h = 0; h < height; h++)
    {
        // Iterate trough collums
        for (int w = 0; w < width; w++)
        {
            // Check RGBT values and store them in an integer
            int orgRed = image[h][w].rgbtRed;
            int orgGreen = image[h][w].rgbtGreen;
            int orgBlue = image[h][w].rgbtBlue;

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
            image[h][w].rgbtRed = sepiaRed;

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

            image[h][w].rgbtGreen = sepiaGreen;

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
            image[h][w].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflects image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate trough rows (height)
    for (int h = 0; h < height; h++)
    {
        int n = 1;
        
        // Iterate trough HALF the width
        for (int w = 0; w < (width / 2); w++)
        {
            // Swaps pixels
            swap(&image[h][w], &image[h][width - n]);
            n++;
        }
    }
    return;
}

// Help function to swap two RGBTRIPLE values
void swap(RGBTRIPLE *a, RGBTRIPLE *b)
{
    RGBTRIPLE temp1;
    RGBTRIPLE temp2;
    temp1 = *a;
    temp2 = *b;
    *a = temp2;
    *b = temp1;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // image = [[1, 2, 3],
    //          [4, 5, 6],
    //          [7, 8, [r, g, b]]]

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

            // Iterate over horRange adjecent pixels ( px 1-3)
            for (int horRange = -1; horRange <= 1; horRange++) // k
            {
                // Iterate over vertical adjecent pixels ( px 2-8)
                for (int verRange = -1; verRange <= 1; verRange++) // l
                {
                    int horAvg = h + horRange; //x
                    int verAvg = w + verRange; //y

                    if (horAvg >= 0 && horAvg < height && verAvg >= 0 && verAvg < width)
                    {
                        sumRed += image[horAvg][verAvg].rgbtRed;
                        sumGreen += image[horAvg][verAvg].rgbtGreen;
                        sumBlue += image[horAvg][verAvg].rgbtBlue;
                        count ++;
                    }

                    else
                    {
                        continue;
                    }    
                }
            }

            copy[h][w].rgbtRed = round((float)sumRed / count);
            copy[h][w].rgbtGreen = round((float)sumGreen / count);
            copy[h][w].rgbtBlue = round((float)sumBlue / count);
        }
    }

    // Copy the altered pixel to the original picture
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            image[h][w] = copy[h][w];
        }
    }
    return;
}

// Program that analyzes text and tracks the sentence, word and letter count.
// The program outputs a grade of the complexity of the text.
// Formula: 'index = 0.0588 * L - 0.296 * S - 15.8'. 
// 'L' = average number of letters per 100 words
// 'S' = average number of sentences per 100 words

// Libraries
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


// Main
int main(void)
{
    // Prompt user for string input
    string text = get_string("Text: ");

    int n = strlen(text);

    // Check for upper- or lowercase letters
    int count_letters = 0;
    for (int i = 0; i < n; i++)
    {
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            count_letters++;
        }
        if (text[i] >= 'A' && text[i] <= 'Z')
        {
            count_letters++;
        }
    }

    // Check for words and keeping count
    // When a space is found, a word is added
    int count_words = 0;
    for (int j = 0; j < n; j++)
    {
        if (text[j] == ' ')
        {
            count_words++;
        }
    }
    count_words++;

    // Check for sentences and keeping count
    // A sentence is added when '.', '?' or '!' is found
    int count_sentences = 0;
    for (int k = 0; k < n; k++)
    {
        if ((text [k] == '.') || (text[k] == '?') || (text[k] == '!'))
        {
            count_sentences++;
        }
    }

    // Calculating the values of L and S
    float L = ((float) count_letters) / ((float) count_words) * 100;
    float S = ((float) count_sentences) / ((float) count_words) * 100;

    // Adding the numbers together
    float index = (0.0588 * L) - (0.296 * S) - 15.8;

    // Printing grade output
    if (index <= 16 && index >= 1)
    {
        printf("Grade %i\n", (int) round(index));
    }
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
}
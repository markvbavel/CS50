// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include "dictionary.h"
#include <string.h>
#include <stdlib.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *hashtable[N];

// Word counter for size function
int word_count = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Hash the word
    int hashval = hash(word);

    // Acces the linked list at the hashval index
    node *cursor = hashtable[hashval];

    // Traverse linked list untill we hit NULL or have found the word
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Iterate over all possible hash values
    for (int i = 0; i <= N; i++)
    {
        // When the first letter in the word matches the hash location, put it there
        if ((word[0] == i + 65) || (word[0] == i + 97))
        {
            return i;
        }
    }
    return 0;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Clear hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary file
    FILE *inptr = fopen(dictionary, "r");
    if (inptr == NULL)
    {
        unload();
        return false;
    }

    // Buffer word the word to be stored in
    char buffer[LENGTH + 1];

    // Iterate over the file, one word(buffer) at a time
    while (fscanf(inptr, "%s", buffer) != EOF)
    {
        // Allocate space for a new node in memory
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }

        // Copy the contents of the buffer into the word field of the new node
        strcpy(new_node->word, buffer);

        // Get the hash value for the new word
        int hashval = hash(buffer);

        // Insert node into linked list
        // If there is nothing in this location of the hash table, change it to the current node
        if (hashtable[hashval] == NULL)
        {
            hashtable[hashval] = new_node;
            new_node->next = NULL;
            word_count++;
        }
        
        // If there is a word in the hash table: point the new node to the existing node. Then point the array to the new node.
        else
        {
            new_node->next = hashtable[hashval];
            hashtable[hashval] = new_node;
            word_count++;
        }

    }
    // Close the dictionary file
    fclose(inptr);

    return true;
}

// Returns number of words in dictionary
unsigned int size(void)
{
    // When the file failed to load, size is 0
    if (!&load)
    {
        return 0;
    }

    // Returns the word count form load
    else
    {
        return word_count;
    }
}

// Unloads dictionary from memory. Returns true if successful
bool unload(void)
{
    // Iterate over hashtable array. Thus finding the headers
    for (int i = 0; i < N; i++)
    {
        // Create a cursor pointer to scroll trough the linked list
        node *cursor = hashtable[i];

        // Step trough everything in the linked list
        while (cursor != NULL)
        {
            node *tmp = cursor; // Temp pointer points to the same as cursor does
            cursor = cursor->next; // Cursor follows the arrow
            free(tmp); // Temp gets freed
        }

        // When end is reached, cursor gets freed
        free(cursor);
    }

    return true;
}
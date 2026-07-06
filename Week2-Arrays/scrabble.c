#include <cs50.h>   // CS50 library for get_string
#include <ctype.h>  // character classification helpers
#include <stdio.h>  // standard input/output
#include <string.h> // string handling functions

// Points assigned to each letter of the alphabet in Scrabble scoring order
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

// Function prototype for score calculation
int compute_score(string word);

int main(void)
{
    // Prompt the user for each player's word
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Calculate each player's score using the Scrabble scoring rules
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Compare scores and announce the result
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    // Total score for the provided word
    int score = 0;

    // Iterate through each character in the word
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        // If the character is uppercase, map it to POINTS by subtracting 'A'
        if (isupper(word[i]))
        {
            score += POINTS[word[i] - 'A'];
        }
        // If the character is lowercase, map it to POINTS by subtracting 'a'
        else if (islower(word[i]))
        {
            score += POINTS[word[i] - 'a'];
        }
    }

    return score;
}
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // check for exactly one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caser key\n");
        return 1;
    }
    // check that every character in the key is a digit
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caeser key\n");
            return 1;
        }
    }
    // convert key from string to integer
    int key = atoi(argv[1]);

    // get plaintext from the user
    string plaintext = get_string("Plaintext: ");
    printf("Ciphertext: ");

    // encript each character
    for (int i = 0; i < strlen(plaintext); i++)
    {
        char c = plaintext[i];
        // encript uppercase letters
        if (isupper(c))
        {
            c = ((c - 'A' + key) % 26) + 'A';
        }
        // encript lowercase letters
        if (islower(c))
        {
            c = ((c - 'a' + key) % 26) + 'a';
        }
        // print the encripted character
        printf("%c", c);
    }
    printf("\n");
    return 0;
}
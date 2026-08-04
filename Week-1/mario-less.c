#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    // ask for height
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // print pyramid
    for (int i = 1; i <= height; i++)
    {
        // print spaces
        for (int j = 1; j <= height - i; j++)
        {
            printf(" ");
        }
        // print #
        for (int k = 1; k <= i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}
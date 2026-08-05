#include <stdio.h>

int main(void)
{
    int height = 4;

    for (int i = 1; i <= height; i++)
    {
        // Leading spaces
        for (int j = 0; j < height - i; j++)
        {
            printf(" ");
        }

        // Left pyramid
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }

        // Gap
        printf("  ");

        // Right pyramid
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }

        printf("\n");
    }

    return 0;
}
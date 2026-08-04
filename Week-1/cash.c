#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int change;
    // get input
    do
    {
        change = get_int("Change owed: ");
    }
    while (change < 1);

    int coins = 0;
    // use quarters
    coins = coins + change / 25;
    change = change % 25;

    // use dimes
    coins = coins + change / 10;
    change = change % 10;

    // use nickles
    coins = coins + change / 5;
    change = change % 5;

    // use pennies
    coins = coins + change / 1;

    printf("%d\n", coins);
}
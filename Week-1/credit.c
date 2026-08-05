#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long card = get_long("Number: ");

    long temp = card;
    int sum = 0;
    int position = 0;
    int length = 0;

    long first_two = 0;
    int first_digit = 0;

    while (temp > 0)
    {
        int digit = temp % 10;
        if (position % 2 == 0)
        {
            sum = sum + digit;
        }
        else
        {
            int product = digit * 2;
            if (product > 9)
            {
                sum = sum + (product / 10) + (product % 10);
            }
            else
            {
                sum = sum + product;
            }
        }

        temp = temp / 10;
        position++;
        length++;
    }

    temp = card;

    while (temp >= 100)
    {
        temp = temp / 10;
    }
    first_two = temp;
    first_digit = temp / 10;

    if (sum % 10 != 0)
    {
        printf("INVALID\n");
    }
    else if ((length == 15) && (first_two == 34 || first_two == 37))
    {
        printf("AMEX\n");
    }
    else if ((length == 16) && (first_two >= 51 && first_two <= 55))
    {
        printf("MASTERCARD\n");
    }
    else if ((length == 13 || length == 16) && first_digit == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}

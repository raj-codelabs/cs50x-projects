from cs50 import get_float

while True:
    change = get_float("Change owned: ")
    if change > 0:
        break

change = round(change * 100)
coins = 0

# use quaters
coins += change // 25
change = change % 25

# use dimes
coins += change // 10
change = change % 10

# use nickels
coins += change // 5
change = change % 5

# use pennies
coins += change // 1

print(coins)

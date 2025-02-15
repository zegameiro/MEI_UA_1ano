import random

def higher_lower_game(value):

    attempts = 0
    guess = 0
    higher_value = 100
    lower_value = 1

    while guess != value: 

        guess = get_number(lower_value, higher_value)
        attempts += 1

        print(f"Attempt {attempts} for value {value} with guess {guess}")

        if guess > value:
            higher_value = guess

        elif guess < value:
            lower_value = guess

    return attempts

def get_number(a, b):
    return random.randint(a, b)

def get_statistics(attempts, stats):

    if attempts not in stats.keys():
        stats[attempts] = 1

    else:
        stats[attempts] += 1

    return stats

def main():

    stats = {}
    # key -> Number of attempts
    # value -> Number of times the value was guessed with n attempts

    for i in range(1, 100001):
        value = random.randint(1, 100)
        attempts = higher_lower_game(value=value)
        print(f"Found value {value} with {attempts} attempts")

        stats = get_statistics(attempts=attempts, stats=stats)

    stats = dict(sorted(stats.items()))
    sum = 0
    for attempt, elems in stats.items():
        print(f"{attempt} attempts: {elems} - {elems / 10000}%")
        sum += elems

    print("Sum: ", sum)
 
if __name__ == "__main__":
    main()
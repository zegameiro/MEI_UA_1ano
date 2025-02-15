import random
import pprint

def roll_dice(max_bound):
    attempts = 0
    found = False
    results = []

    while not found:
        roll = random.randint(1, max_bound)
        attempts += 1

        if roll in results:
            found = True

        else:
            results.append(roll)
    
    return attempts

def all_dice(max_bound):
    attempts = 0
    found = False
    results = []
    final_result = [i for i in range(1, max_bound)]
    print(final_result)

    while not found:
        roll = random.randint(1, max_bound)
        attempts += 1

        print(results)

        if results == final_result:
            found = True

        else:
            results.append(roll)

    return attempts

        

def main(num_rolls = 100000):
    # att = {}
    max_bound = 2 # 6 for the dice problem and 365 for the birthday problem

    # for _ in range(num_rolls):
    #     attempts = roll_dice(max_bound=max_bound)
    #     if attempts not in att:
    #         att[attempts] = 0
    #     else:
    #         att[attempts] += 1
    
    # for key, value in att.items():
    #     percent = (value / num_rolls) * 100
    #     att[key] = percent

    att_1 = {}

    for _ in range(num_rolls):
        attempts = all_dice(max_bound=max_bound)
        if attempts not in att_1:
            att_1[attempts] = 0
        else:
            att_1[attempts] += 1

    for key, value in att_1.items():
        percent = (value / num_rolls) * 100
        att_1[key] = percent

    pprint.pprint(att_1)


if __name__ == '__main__':
    main(100)
    
        


def brute_force_approach_iterative(a, b):

    res = a
    count = 1

    if b == 0:
        return count

    for element in range(1, b):
        print(f"iteration with b equals {count}: {res} * {a}")
        res = res * a
        count += 1

    return res


def brute_force_approach_recursive(a, b):

    print(f"iteration with b equals {b}: {a}")

    if b == 0:
        return 1

    if b == 1:
        return a

    return a * brute_force_approach_recursive(a, b - 1)


def divide_and_conquer_approach(a, b):

    if b == 0:
        return 1

    if b == 1:
        return a
    
    print(f"iteration with b equals {b}: {a}")
    
    new_b = b // 2

    return divide_and_conquer_approach(a, new_b) * divide_and_conquer_approach(a, b - new_b)


def divide_and_conquer_smart_approach(a, b):

    print(f"iteration with b equals {b}: {a}")

    if b == 0:
        return 1

    if b == 2:
        return a * a
    
    if b % 2 == 0:
        return divide_and_conquer_smart_approach(a, b // 2) ** 2
    
    return a * divide_and_conquer_smart_approach(a, b - 1)
    

if __name__ == '__main__':
    a = 2
    b = 7
    print("Result from iterative: ", brute_force_approach_iterative(a, b), "\n")
    print("Result from recursive", brute_force_approach_recursive(a, b), "\n")
    print("Result from divide and conquer approach: ", divide_and_conquer_approach(a, b), "\n")

    for i in range(0, 11):
        print("for b equals: ", i)
        print("Result from divide and conquer smart approach: ", divide_and_conquer_smart_approach(a, i), "\n")

    print("Result from divide and conquer smart approach: ", divide_and_conquer_smart_approach(a, 15), "\n")

def f1(n):

    r = 0
    
    for i in range(0, n + 1):
        r += i

    return r

def f2(n):

    r = 0

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            r += 1
    
    return r

def f3(n):

    r = 0

    for i in range(1, n + 1):
        for j in range(i, n + 1):
            r += 1
    
    return r

def f4(n):

    r = 0

    for i in range(1, n + 1):
        for j in range(1, i + 1):
            r += j

    return r

def main(fun):
    for inp in range(1, 11):
        print(inp," - ",fun(inp))


if __name__ == '__main__':
    print("f1")
    main(f1)
    print("\nf2")
    main(f2)
    print("\nf3")
    main(f3)
    print("\nf4")
    main(f4)
    

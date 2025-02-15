def fibonacci_recursive_dp(n, memo={}):

    # Base cases
    if n <= 1:
        return n
    
    # Check if the value is already computed and stored in the memo dictionary
    if n in memo:
        return memo[n]
    
    # Compute the Fibonacci number and store it in the memo dictionary
    memo[n] = fibonacci_recursive_dp(n - 1, memo) + fibonacci_recursive_dp(n - 2, memo)
    
    return memo[n]

def main():
    n = 10
    result = fibonacci_recursive_dp(n)
    print(f"Fibonacci number at position {n} is {result}")


if __name__ == "__main__":
    main()

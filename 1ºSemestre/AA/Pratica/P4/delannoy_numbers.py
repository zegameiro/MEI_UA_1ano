import timeit

# Recursive Case
def delannoy_recursive(m, n):
    if m == 0 or n == 0:
        return 1
    
    return delannoy_recursive(m - 1, n) + delannoy_recursive(m, n - 1) + delannoy_recursive(m - 1, n - 1)

def delannoy_2d_array(m, n):

    # Create the 2D array with dimension (m+1) x (n+1)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # If m or n is 0, there's only one way to reach (m, n)
    for i in range(m + 1):
        dp[i][0] = 1

    for j in range(n + 1):
        dp[0][j] = 1

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1] + dp[i - 1][j - 1]

    return dp[m][n]

def delannoy_2_1d_array(m, n):

    # Create the 2 1D arrays
    previous = [1] * (n + 1)
    current = [1] * (n + 1)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            current[j] = previous[j] + current[j - 1] + previous[j - 1]

        # Updated the previous with the current array
        previous = current[:]

    return current[n]

if __name__ == "__main__":
    m = 5
    n = 5
    print(timeit.timeit("delannoy_recursive(m, n)", setup="from __main__ import delannoy_recursive, m, n", number=1))
    print(timeit.timeit("delannoy_2d_array(m, n)", setup="from __main__ import delannoy_2d_array, m, n", number=1))
    print(timeit.timeit("delannoy_2_1d_array(m, n)", setup="from __main__ import delannoy_2_1d_array, m, n", number=1))
    

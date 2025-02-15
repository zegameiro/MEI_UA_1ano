def coin_row_problem(n, coins):

    if n == 0:
        return 0
    
    if n == 1:
        return coins[0]
    
    return max(coin_row_problem(n - 1, coins), coin_row_problem(n - 2, coins) + coins[n - 1])

coins_row = [3, 1, 5, 2, 5, 4, 2, 3, 4, 2, 5, 6, 7, 4, 6, 1]

if __name__ == '__main__': 
    print("Maximum amount of money that can be obtained:", coin_row_problem(len(coins_row), coins_row))
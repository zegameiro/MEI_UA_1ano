import numpy as np
from scipy.stats import binom

# Part 1: Simulate experiments to estimate the probability
def simulate_coin_tosses(trials=100000, tosses=15, target_heads=6):
    successes = 0
    for _ in range(trials):
        # Simulate 15 coin tosses with equal probability of heads and tails (0.5)
        tosses_result = np.random.binomial(1, 0.5, tosses)  # 1 for heads, 0 for tails
        heads_count = np.sum(tosses_result)
        if heads_count == target_heads:
            successes += 1
    estimated_probability = successes / trials
    return estimated_probability

# Part 2: Calculate the exact probability using binomial distribution
def calculate_binomial_probability(tosses=15, target_heads=6, p_heads=0.5):
    probability = binom.pmf(target_heads, tosses, p_heads)
    return probability

# Run the simulation
estimated_prob = simulate_coin_tosses()
print(f"Estimated Probability of getting exactly 6 heads in 15 tosses: {estimated_prob}")

# Calculate exact probability with binomial distribution
exact_prob = calculate_binomial_probability()
print(f"Exact Probability of getting exactly 6 heads in 15 tosses: {exact_prob}")

# Part 3: Adjust probability for P(heads) = 2 * P(tails)
# Let P(heads) = 2/3 and P(tails) = 1/3, so total probability is still 1
adjusted_p_heads = 2 / 3
adjusted_estimated_prob = simulate_coin_tosses(trials=100000, tosses=15, target_heads=6)
adjusted_exact_prob = calculate_binomial_probability(p_heads=adjusted_p_heads)

print(f"Estimated Probability (P[heads] = 2 * P[tails]): {adjusted_estimated_prob}")
print(f"Exact Probability (P[heads] = 2 * P[tails]): {adjusted_exact_prob}")

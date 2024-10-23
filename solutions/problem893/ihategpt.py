import itertools
from functools import reduce
from collections import Counter
from itertools import product as itertools_product
from math import prod

# Optimized prime factorization using trial division
def primeFactorization(num):
    num = int(num)
    factors = []
    i = 2
    while i * i <= num:
        if num % i:
            i += 1
        else:
            num //= i
            factors.append(i)
    if num > 1:
        factors.append(num)
    return factors

digitToMatches = {1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6, 0: 6, "+": 2, "*": 2}

def repToMatches(expr):
    """Takes a string representing a number or an expression and counts the number of matchsticks."""
    return sum(digitToMatches.get(char, 0) for char in str(expr))

# A helper to generate sum representations
def allSum(n):
    return [f"{i}+{n-i}" for i in range(1, n // 2 + 1)]

# Main function M to find the minimal matchsticks for a number n
def M(n):
    factors = primeFactorization(n)
    all_factors = findAllPossibilities(factors, n)
    sums = allSum(n)
    all_expressions = all_factors + sums
    match_counts = [repToMatches(expr) for expr in all_expressions]
    return min(match_counts), min(all_expressions, key=lambda x: repToMatches(x))

def T(n):
    return sum(M(i)[0] for i in range(1, n + 1))

def main():
    usrInput = int(input("What number do you want? "))
    print(T(usrInput))

if __name__ == "__main__":
    main()


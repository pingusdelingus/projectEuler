
import itertools
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
    numMatches = 0
    for char in expr:
        if char.isdigit():
            numMatches += digitToMatches[int(char)]
        else:
            numMatches += digitToMatches[char]
    return numMatches

def evaluate(expr):
    """Helper function to safely evaluate basic expressions."""
    try:
        return eval(expr)
    except:
        return None

# Generates all possible representations from prime factorization (using multiplications)
def findAllPossibilities(prime_factors, theNumber):
    factor_counts = Counter(prime_factors)
    
    combinations = []
    for factor, count in factor_counts.items():
        combinations.append([factor**i for i in range(count + 1)])
    
    all_combinations = itertools_product(*combinations)
    
    result = []
    full_factorization = '*'.join(map(str, prime_factors))
    
    for combo in all_combinations:
        combo_product = prod(combo)
        factors = [str(factor) for factor in combo if factor != 1]
        
        if len(factors) >= 2:
            factor_str = '*'.join(factors)
            if factor_str not in result:
                result.append(factor_str)
        
        if combo_product == theNumber and str(combo_product) not in result:
            result.append(str(combo_product))
    
    result = [full_factorization] + sorted(result, key=lambda x: evaluate(x))
    return [expr for expr in result if evaluate(expr) == theNumber]

# A helper to generate sum representations
def allSum(n):
    return [f"{i}+{n-i}" for i in range(1, n // 2 + 1)]

# Main function M to find the minimal matchsticks for a number n
def M(n):
    factors = primeFactorization(n)
    all_factors = findAllPossibilities(factors, n)
    sums = allSum(n)
    all_expressions = all_factors + sums
    
    print(f"Prime factors of {n}: {factors}")
    print(f"All possible expressions for {n}: {all_expressions}")
    
    match_counts = [repToMatches(expr) for expr in all_expressions]
    
    min_match_count = min(match_counts)
    best_expr = all_expressions[match_counts.index(min_match_count)]
    
    print(f"Best expression for {n}: {best_expr}, matchsticks: {min_match_count}")
    
    return min_match_count, best_expr

def T(n):
    total_matches = 0
    for i in range(1, n + 1):
        matches, _ = M(i)
        total_matches += matches
    return total_matches

def main():
    usrInput = int(input("What number do you want? "))
    print(f"Total matchsticks for T({usrInput}): {T(usrInput)}")

if __name__ == "__main__":
    main()
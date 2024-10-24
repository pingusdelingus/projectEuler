
import tensorflow as tf
import numpy as np
import itertools
from collections import Counter
from itertools import product as itertools_product
from math import prod
from colorama import Fore, init

init()

# Reading prime numbers from a file
with open("1milPrimes", "r") as file:
    primeList = np.array([int(prime.rstrip()) for prime in file.readlines()])  # Store primes in a NumPy array

# Dictionary to hold the number of matchsticks needed for each digit
digitToMatches = {1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6, 0: 6, "+": 2, "*": 2}

# Cache for previously calculated results
seenReps = {}

# Function to return a list with all prime factors of num
def primeFactorization(num):
    factors = []
    keepLoop = True
    index = 0
    while keepLoop and index < len(primeList):  # Prevent index out of range
        if primeList[index] > num:
            keepLoop = False
        elif num % primeList[index] == 0:
            factors.append(primeList[index])
            num //= primeList[index]  # Use integer division
        else:
            index += 1
    return factors

# Function to evaluate a string representation to return the number of matches needed
def evaluate(str1):
    if str1 == "":
        return None
    res = eval(str1)
    return res

# Function to convert a representation to the number of matchsticks needed
def repToMatches(str1):
    if str1 in seenReps:
        return seenReps[str1]
    
    numMatches = tf.reduce_sum(tf.convert_to_tensor(
        [digitToMatches[int(char)] if char.isdigit() else 2 for char in str1], dtype=tf.int32
    ))  # Use TensorFlow to sum matchsticks
    seenReps[str1] = numMatches.numpy()  # Convert back to numpy for caching
    return numMatches

# Function to find all possible representations of prime factors
def findAllPossibilities(prime_factors, theNumber):
    factor_counts = Counter(prime_factors)
    combinations = []
    for factor, count in factor_counts.items():
        combinations.append([factor**i for i in range(count + 1)])
    
    all_combinations = itertools_product(*combinations)
    result = []
    total_product = prod(prime_factors)
    full_factorization = '*'.join(map(str, prime_factors))
    
    for combo in all_combinations:
        combo_product = prod(combo)
        factors = [str(factor) for factor in combo if factor != 1]
        if len(factors) >= 2:
            factor_str = '*'.join(factors)
            if factor_str not in result and factor_str != full_factorization:
                result.append(factor_str)
        if combo_product == total_product and str(combo_product) not in result:
            result.append(str(combo_product))
    
    result = [full_factorization] + sorted(result, key=lambda x: eval(x))
    ans = [item for item in result if evaluate(item) == theNumber]  # List comprehension for filtering
    return ans

# Function to count the match numbers for all possible representations
def countMatchNums(allPoss):
    return [repToMatches(poss) for poss in allPoss]  # List comprehension for collecting matches

# Function to find possible sum representations
def allSum(n, minMatchesOfAllP):
    ans = []
    redudCount = 0
    for index in range(1, (n // 2) + 1):
        if redudCount >= 1000:
            break
        string = f"{index}+{n - index}"
        res = repToMatches(string)
        if res >= minMatchesOfAllP:
            redudCount += 1
        else:
            ans.append(res)
    
    return [minMatchesOfAllP] if len(ans) == 0 else ans

# Function to compute M(n)
def M(n):
    rawFacts = primeFactorization(n)
    allP = findAllPossibilities(rawFacts, n)
    matchesOfAllP = countMatchNums(allP)
    minMatchesOfAllP = min(matchesOfAllP)
    sums = allSum(n, minMatchesOfAllP)
    minSum = min(sums) if sums else minMatchesOfAllP
    return min(minSum, minMatchesOfAllP)

# Function to compute T(n)
def T(n):
    sum = tf.constant(0, dtype=tf.int32)  # Initialize sum as TensorFlow constant
    for index in range(1, n + 1):
        res = M(index)
        sum += res
        print(f"{Fore.RED} the value of M({index}) is : {res} {Fore.RESET}")
    return sum.numpy()  # Convert back to numpy for printing

# Main function
def main():
    usrInput = int(input("What number do you want? "))
    print(T(usrInput))

main()

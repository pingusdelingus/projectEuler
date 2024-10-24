import numpy as np
import itertools
import math
from functools import reduce
from collections import Counter
from itertools import product as itertools_product
from math import prod
from colorama import Fore, init

init()

'''
We are given a number, and we want to find the min number of matchsticks needed to represent it.
We can also use addition and multiplication to represent a number.
We can first make a dict matching each individual digit to its number of match sticks needed.
We can use the fundamental theorem of arithmetic to get the unique prime factorization of N 
and then check how many matchsticks it takes compared to the raw representation.
'''

# Reading prime numbers from a file
with open("1milPrimes", "r") as file:
    primeList = [int(prime.rstrip()) for prime in file.readlines()]

# Dictionary to hold the number of matchsticks needed for each digit
digitToMatches = {1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6, 0: 6, "+": 2, "*": 2}

# Cache for previously calculated results
seenReps = {}

# Function to return a list with all prime factors of num
def primeFactorization(num):
    num = np.int32(num)  # Using CuPy int32 for GPU compatibility
    factors = []
    keepLoop = True
    index = 0
    while keepLoop:
        if primeList[index] > num:
            keepLoop = False
        elif num % primeList[index] == 0:
            num = num / primeList[index]
            factors.append(primeList[index])
        elif num % primeList[index] != 0:
            index += 1
    del(num, keepLoop, index)  # Freeing memory
    return factors

# Function to evaluate a string representation to return the number of matches needed
def evaluate(str1):
    if str1 == "":
        return
    str1 = str(str1)
    res = eval(str1)
    return res

# Function to convert a representation to the number of matchsticks needed
def repToMatches(str1):
    if str1 in seenReps:
        return seenReps[str1]
    else:
        numMatches = 0
        for char in str1:
            if char == "*" or char == "+":
                numMatches += 2
            else:
                char = int(char)
                numMatches += digitToMatches[char]
        seenReps[str1] = numMatches
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
    ans = []
    for item in result:
        if evaluate(item) == theNumber:
            ans.append(item)
    return ans

# Function to count the match numbers for all possible representations
def countMatchNums(allPoss):
    matches = []
    for poss in allPoss:
        matchNum = repToMatches(poss)
        matches.append(matchNum)
    return matches

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
            continue
        else:
            ans.append(res)
    if len(ans) == 0:
        return [minMatchesOfAllP]
    else:
        return ans

# Function to compute M(n)
def M(n):
    rawFacts = primeFactorization(n)
    allP = findAllPossibilities(rawFacts, n)
    matchesOfAllP = countMatchNums(allP)
    minMatchesOfAllP = min(matchesOfAllP)
    sums = allSum(n, minMatchesOfAllP)
    if sums is None:
        return minMatchesOfAllP
    minSum = min(sums)
    minNum = min(minSum, minMatchesOfAllP)
    return minNum

# Function to compute T(n)
def T(n):
    sum = np.int32(0)  # Using CuPy int32 for GPU compatibility
    for index in range(1, n + 1):
        res = M(index)
        sum += res
        print(f"{Fore.RED} the value of M({index}) is : {res} {Fore.RESET}")
        del(res)  # Freeing memory after each iteration
    del(index)  # Freeing index variable memory
    return sum

# Main function
def main():
    usrInput = int(input("What number do you want? "))
    print(T(usrInput))
    del(usrInput)  # Freeing memory after user input is used

main()

import itertools
from functools import reduce
from collections import Counter
from itertools import product as itertools_product
from math import prod

'''
we are given a number, and we want to find the min number of matchsticks needed to represent it.
we can also use addition and multiplication to represent a number.

we can first make a dict matching each indiviual digit to its number of match sticks needed
we can use the fundamental theorem of arithmetic to get the unique prime factorization of N and then check how many matchsticks it takes compared to the 
raw representation
'''

with open("1milPrimes", "r") as file:
    primeList = [int(prime.rstrip()) for prime in file.readlines()]





#! returns a list with all prime factors of num
#! i.e for 28 would return [2,2,7]
#! factors are unique
def primeFactorization(num):
    num = int(num)
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

    return factors
digitToMatches = {1 : 2, 2 : 5, 3 : 5, 4 : 4, 5 : 5, 6 : 6, 7 : 3, 8 : 7, 9 : 6, 0 : 6, "+" : 2, "*" : 2}





#! takes in a string and returns the number of matches needed to display that representation
#! i.e. for "28" returns 12 since you need 5 matches for 2 and 7 matches for 8
def eval(str1):
    res = 1
    str1 = str1.split("*")
    for num in str1:
        res *= int(num)
    return res

def repToMatches(str1):
    ourSum = 0
    for char in str1:
        if char == "*" or char == "+":
            ourSum += digitToMatches[char]
        else:
            char = int(char)
            ourSum += digitToMatches[char]
    return ourSum
#given a list of prime factors, return a list of all possible representations as strings
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
        if eval(item) == theNumber:
            ans.append(item)

    return ans

raw = "20"
rawSum = repToMatches(raw)

rawFactors = primeFactorization(raw)
print(rawFactors)


allPoss = findAllPossibilities(rawFactors, int(raw))
def countMatchNums(allPoss):

    matches = []
    for poss in allPoss:
        matches.append(repToMatches(poss))
    return matches
# now that we have the raw sum, we must check all other representations of the num

def M(n):
    rawFacts = primeFactorization(n)
    allP = findAllPossibilities(rawFacts, n)
    allMatchNums = countMatchNums(allP)
    return min(allMatchNums)

def T(n):
    sum = 0
    for index in range(1,n+1):
        sum += M(n)
    return sum

def main():
    usrInput = int(input("what num you want"))
    ans = T(usrInput)
    print(ans)

main()




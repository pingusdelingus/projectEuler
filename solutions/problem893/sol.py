import itertools
import math
from functools import reduce
from collections import Counter
from itertools import product as itertools_product
from math import prod
from colorama import Fore, init
init()
'''
we are given a number, and we want to find the min number of matchsticks needed to represent it.
we can also use addition and multiplication to represent a number.

we can first make a dict matching each indiviual digit to its number of match sticks needed
we can use the fundamental theorem of arithmetic to get the unique prime factorization of N and then check how many matchsticks it takes compared to the 
raw representation
'''

with open("1milPrimes", "r") as file:
    primeList = [int(prime.rstrip()) for prime in file.readlines()]



#! NEW IDEA! MAKE A DICT THAT HOLDS EACH CALCULATION OF repToMatches so for large values we can lookup and return them instead of calculating them.

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
def evaluate(str1):
    if str1 == "":
        return
    str1= str(str1)
    res = eval(str1)
    return res

def repToMatches(str1):
    seenReps = {}
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
        if evaluate(item) == theNumber:
            ans.append(item)

    return ans

def findSumAndMults(factors,):
    pass

def countMatchNums(allPoss):

    matches = []
    for poss in allPoss:
        matchNum = repToMatches(poss)
        matches.append(matchNum)
    return matches

# now that we have the raw sum, we must check all other representations of the num
def allSum(n, minMatchesOfAllP):
    ans = []
    redudCount = 0
    for index in range(1, (n//2)+1):
        if redudCount >= 1000:
            break
        string = f"{index}+{n-index}"
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
def M(n):
    rawFacts = primeFactorization(n)
   # print(f"this is all rawFacts {rawFacts}")
    allP = findAllPossibilities(rawFacts, n)
    matchesOfAllP = countMatchNums(allP)
    minMatchesOfAllP = min(matchesOfAllP)

   # print(f"this is allP : {allP}")
    sums = allSum(n, minMatchesOfAllP)
   # print(f"this is sums: {sums}")
    if sums == None:
       return minMatchesOfAllP
    minSum = min(sums)
    minNum = min(minSum, minMatchesOfAllP)
    return minNum 
def T(n):
    sum = 0
    x = ""
    with open("sol.txt", "a") as file:
        
        for index in range(1,n+1):
            res = M(index)
            sum += res
            print(f"THE CURRENT SUM IS : {sum}")
            x = f"{Fore.RED} the value of M({index}) is : {res} {Fore.RESET}"
            print(x)
            file.write(x + "\n")
            del(res)
        return sum

def main():
    usrInput = int(input("what num you want"))
    print(T(usrInput)) 
main()




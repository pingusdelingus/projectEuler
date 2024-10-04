from test import primesfrom3to

x = int(input("what prime do you want to check"))
primeList = list(primesfrom3to(x))

primeList.insert(0,2)
# given a target prime and a primelist, check if the 
# primes below it sum up to it and return how many consecutive primes sum to it
# 41 would return 6 since 2+3+5+7+11+13 = 41.
def getCount(primeList, targetPrime):
    start, current_sum, count = 0, 0, 0
    
    for end in range(len(primeList)):
        current_sum += primeList[end]
        
        # Slide the window if sum exceeds targetPrime
        while current_sum > targetPrime and start < end:
            current_sum -= primeList[start]
            start += 1
        
        # Check if we've found a sum equal to targetPrime
        if current_sum == targetPrime:
            return end - start + 1  # The number of primes in the window
    
    return -1  # Return -1 if no such sum is found
    

primeToCount = {prime : 0 for prime in primeList}



for key, value in primeToCount.items():
    primeToCount[key] = getCount(primeList, key)

def getMaxOfConsecSums(primeToCount):
    max = 0
    prime = 0
    for key,value in primeToCount.items():
        if value > max:
            max = value
            prime = key
    return str(max) + " " + str(prime)
print(f" the max sum and its prime are {getMaxOfConsecSums(primeToCount)}")


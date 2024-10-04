primeList = []

with open("1milPrimes", "r") as file:
    primeList = [int(prime.rstrip()) for prime in file.readlines()]


print(primeList[5], type(primeList[5]))
x = int(input("what prime do you want to check"))

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
        if current_sum > targetPrime:
            break
    return -1  # Return -1 if no such sum is found
    
primeToCount = {prime : getCount(primeList, prime) for prime in primeList if prime < x}



maximum = max(primeToCount.items(), key=lambda item: item[1])
print(f" the max sum and its prime are{maximum} ")



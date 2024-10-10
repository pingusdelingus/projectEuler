divisors = []

for index in range(0,1000):
    if index % 3 == 0 or index % 5 == 0:
        divisors.append(index)
       

divisors = set(divisors)
theSum = sum(divisors)

print(theSum)


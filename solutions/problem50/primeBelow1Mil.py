from test import primesfrom3to
theList = primesfrom3to(1000000)
with open("1milPrimes", 'w') as file:
    file.write(str(2) + "\n")
    for prime in theList:
        file.write(str(prime) + "\n")


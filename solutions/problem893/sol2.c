
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

// Prime list with some example prime numbers
// This should be loaded from a file or dynamically generated
int primeList[1000000];

// Function to read primes from a file
void loadPrimes() {
    FILE *file = fopen("1milPrimes", "r");
    if (!file) {
        printf("Error opening file\n");
        exit(1);
    }
    int i = 0;
    while (fscanf(file, "%d", &primeList[i]) != EOF) {
        i++;
    }
    fclose(file);
}

// Returns a list of prime factors of a number
void primeFactorization(int num, int *factors, int *factorCount) {
    *factorCount = 0;
    int index = 0;
    while (num > 1 && index < 1000000) {
        if (primeList[index] > num) {
            break;
        } else if (num % primeList[index] == 0) {
            factors[(*factorCount)++] = primeList[index];
            num /= primeList[index];
        } else {
            index++;
        }
    }
}

// Given a string, calculates the number of matchsticks needed
int digitToMatches(char digit) {
    switch (digit) {
        case '1': return 2;
        case '2': return 5;
        case '3': return 5;
        case '4': return 4;
        case '5': return 5;
        case '6': return 6;
        case '7': return 3;
        case '8': return 7;
        case '9': return 6;
        case '0': return 6;
        case '+': return 2;
        case '*': return 2;
        default: return 0;
    }
}

// Converts a string representation of a number into matchstick count
int repToMatches(const char *str) {
    int numMatches = 0;
    for (int i = 0; i < strlen(str); i++) {
        numMatches += digitToMatches(str[i]);
    }
    return numMatches;
}

// Calculate product of an array
int product(int *array, int size) {
    int prod = 1;
    for (int i = 0; i < size; i++) {
        prod *= array[i];
    }
    return prod;
}

// Find all possibilities of combinations for prime factors
void findAllPossibilities(int *prime_factors, int factorCount, int theNumber, char result[100][100], int *resultCount) {
    *resultCount = 0;
    int total_product = product(prime_factors, factorCount);

    // Full factorization string
    char full_factorization[100];
    full_factorization[0] = '\0';
    for (int i = 0; i < factorCount; i++) {
        char temp[10];
        sprintf(temp, "%d", prime_factors[i]);
        strcat(full_factorization, temp);
        if (i != factorCount - 1) {
            strcat(full_factorization, "*");
        }
    }

    strcpy(result[(*resultCount)++], full_factorization);

    // TODO: Generate combinations and check results (this part needs more complex logic)
}

// Counts the match numbers for all possibilities
int countMatchNums(char allPoss[100][100], int allPossCount) {
    int minMatches = 1000000;
    for (int i = 0; i < allPossCount; i++) {
        int matchNum = repToMatches(allPoss[i]);
        if (matchNum < minMatches) {
            minMatches = matchNum;
        }
    }
    return minMatches;
}

// Generates all possible sums for a number
void allSum(int n, char sums[100][100], int *sumCount) {
    *sumCount = 0;
    for (int i = 1; i <= n / 2; i++) {
        sprintf(sums[(*sumCount)++], "%d+%d", i, n - i);
    }
}

// M function: Calculate the minimum number of matchsticks
int M(int n) {
    int prime_factors[100];
    int factorCount;
    primeFactorization(n, prime_factors, &factorCount);

    char allPoss[100][100];
    int allPossCount;
    findAllPossibilities(prime_factors, factorCount, n, allPoss, &allPossCount);

    char sums[100][100];
    int sumCount;
    allSum(n, sums, &sumCount);

    // Combine possibilities and sums
    for (int i = 0; i < sumCount; i++) {
        strcpy(allPoss[allPossCount++], sums[i]);
    }

    return countMatchNums(allPoss, allPossCount);
}

// T function: Sum of M for all numbers from 1 to n
int T(int n) {
    int total = 0;
    for (int i = 1; i <= n; i++) {
        total += M(i);
    }
    return total;
}

// Main function
int main() {
    loadPrimes();
    int usrInput;
    printf("What number do you want: ");
    scanf("%d", &usrInput);
    printf("Result: %d\n", T(usrInput));
    return 0;
}

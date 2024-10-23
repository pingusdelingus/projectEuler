
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PRIMES 1000000

int primeList[MAX_PRIMES];
int digitToMatches[] = {6, 2, 5, 5, 4, 5, 6, 3, 7, 6}; // 0 to 9
int operatorMatches = 2;

void loadPrimes(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error opening file\n");
        exit(1);
    }

    int index = 0;
    while (fscanf(file, "%d", &primeList[index]) != EOF) {
        index++;
    }
    fclose(file);
}

// Prime Factorization - fills the factors array with the prime factors of num
void primeFactorization(int num, int* factors, int* factorCount) {
    int index = 0;
    *factorCount = 0;
    while (num > 1 && index < MAX_PRIMES) {
        if (primeList[index] > num) {
            break;
        }
        if (num % primeList[index] == 0) {
            num = num / primeList[index];
            factors[(*factorCount)++] = primeList[index];
        } else {
            index++;
        }
    }
}

// Helper function to calculate the matchsticks for a given number string
int repToMatches(const char* str1) {
    int numMatches = 0;
    for (int i = 0; i < strlen(str1); i++) {
        char char1 = str1[i];
        if (char1 == '*' || char1 == '+') {
            numMatches += operatorMatches;
        } else {
            numMatches += digitToMatches[char1 - '0'];
        }
    }
    return numMatches;
}

// Recursively generate all factorizations of the number using the prime factors
void findFactorizations(int* factors, int factorCount, int currentIndex, int currentProduct, int target, char* currentRep, int* minMatches) {
    if (currentIndex == factorCount) {
        if (currentProduct == target) {
            int matchCount = repToMatches(currentRep);
            if (matchCount < *minMatches) {
                *minMatches = matchCount;
            }
        }
        return;
    }

    // Try including the current factor
    char tempRep[50];
    strcpy(tempRep, currentRep);

    if (strlen(currentRep) > 0) {
        strcat(tempRep, "*");
    }

    char factorStr[10];
    sprintf(factorStr, "%d", factors[currentIndex]);
    strcat(tempRep, factorStr);

    findFactorizations(factors, factorCount, currentIndex + 1, currentProduct * factors[currentIndex], target, tempRep, minMatches);

    // Try excluding the current factor (skip multiplication by 1)
    findFactorizations(factors, factorCount, currentIndex + 1, currentProduct, target, currentRep, minMatches);
}

// Function to evaluate the number of matchsticks required for all factorizations
int findMinMatchsticksForFactorization(int* factors, int factorCount, int target) {
    int minMatches = 10000; // Start with a large number
    char initialRep[50] = "";
    findFactorizations(factors, factorCount, 0, 1, target, initialRep, &minMatches);
    return minMatches;
}

// Sum representations (e.g., 28 = 14 + 14) and evaluate their matchsticks
int allSum(int n, int minMatchesOfAllP) {
    int minSum = minMatchesOfAllP;
    for (int i = 1; i <= n / 2; i++) {
        char str[20];
        sprintf(str, "%d+%d", i, n - i);
        int res = repToMatches(str);
        if (res < minSum) {
            minSum = res;
        }
    }
    return minSum;
}

// Function M: Find the minimum matchsticks to represent the number n
int M(int n) {
    int factors[100];
    int factorCount;

    // Get the prime factors of n
    primeFactorization(n, factors, &factorCount);

    // Get the minimum matchsticks needed for factorizations
    int minMatchesOfAllP = findMinMatchsticksForFactorization(factors, factorCount, n);

    // Get the minimum matchsticks needed for sum representations
    int minSum = allSum(n, minMatchesOfAllP);

    return minSum < minMatchesOfAllP ? minSum : minMatchesOfAllP;
}

// Function T: Sum of M for all numbers from 1 to n
int T(int n) {
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        int res = M(i);
        printf("The value of M(%d) is : %d\n", i, res);
        sum += res;
    }
    return sum;
}

int main() {
    int usrInput;
    printf("Enter a number: ");
    scanf("%d", &usrInput);
    loadPrimes("1milPrimes");
    printf("Result: %d\n", T(usrInput));
    return 0;
}

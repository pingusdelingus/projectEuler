
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_PRIMES 1000000
#define MAX_FACTORS 100

int primeList[MAX_PRIMES];
int primeCount = 0;

void loadPrimes() {
    FILE *file = fopen("1milPrimes", "r");
    if (file == NULL) {
        perror("Failed to open file");
        exit(EXIT_FAILURE);
    }
    while (fscanf(file, "%d", &primeList[primeCount]) != EOF) {
        primeCount++;
    }
    fclose(file);
}

int* primeFactorization(int num, int *size) {
    int *factors = malloc(MAX_FACTORS * sizeof(int));
    *size = 0;
    for (int index = 0; index < primeCount && primeList[index] <= num; index++) {
        while (num % primeList[index] == 0) {
            factors[(*size)++] = primeList[index];
            num /= primeList[index];
        }
    }
    return factors;
}

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

int evaluate(const char *str) {
    return atoi(str); // Simplified evaluation for this context
}

int repToMatches(const char *str) {
    int numMatches = 0;
    for (int i = 0; str[i] != '\0'; i++) {
        numMatches += digitToMatches(str[i]);
    }
    return numMatches;
}

void findAllPossibilities(int *prime_factors, int size, int theNumber, char result[][MAX_FACTORS], int *resultSize) {
    int factor_counts[MAX_FACTORS] = {0};
    for (int i = 0; i < size; i++) {
        factor_counts[prime_factors[i]]++;
    }

    *resultSize = 0;
    for (int i = 0; i < (1 << size); i++) {
        char combo[MAX_FACTORS] = "";
        int combo_product = 1;
        for (int j = 0; j < size; j++) {
            if (i & (1 << j)) {
                combo_product *= prime_factors[j];
                char buffer[10];
                sprintf(buffer, "%d*", prime_factors[j]);
                strcat(combo, buffer);
            }
        }
        if (combo_product == theNumber) {
            combo[strlen(combo) - 1] = '\0'; // Remove last '*'
            strcpy(result[(*resultSize)++], combo);
        }
    }
}

int countMatchNums(char allPoss[][MAX_FACTORS], int count) {
    int matches[MAX_FACTORS];
    for (int i = 0; i < count; i++) {
        matches[i] = repToMatches(allPoss[i]);
    }
    int minMatches = matches[0];
    for (int i = 1; i < count; i++) {
        if (matches[i] < minMatches) {
            minMatches = matches[i];
        }
    }
    return minMatches;
}

void allSum(int n, char result[][MAX_FACTORS], int *resultSize) {
    *resultSize = 0;
    for (int index = 1; index <= n / 2; index++) {
        sprintf(result[(*resultSize)++], "%d+%d", index, n - index);
    }
}

int M(int n) {
    int size;
    int *rawFacts = primeFactorization(n, &size);
    char allP[MAX_FACTORS][MAX_FACTORS];
    int allPSize = 0;

    findAllPossibilities(rawFacts, size, n, allP, &allPSize);
    char sums[MAX_FACTORS][MAX_FACTORS];
    int sumsSize;
    allSum(n, sums, &sumsSize);

    for (int i = 0; i < sumsSize; i++) {
        strcpy(allP[allPSize++], sums[i]);
    }

    int minMatches = countMatchNums(allP, allPSize);
    free(rawFacts);
    return minMatches;
}

int T(int n) {
    int sum = 0;
    for (int index = 1; index <= n; index++) {
        sum += M(index);
    }
    return sum;
}

int main() {
    loadPrimes();
    int usrInput;
    printf("What num you want: ");
    scanf("%d", &usrInput);
    printf("%d\n", T(usrInput));
    return 0;
}


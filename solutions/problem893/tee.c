
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

int evaluate(const char* str1) {
    return atoi(str1); // simplistic evaluation
}

void findAllPossibilities(int* prime_factors, int factorCount, int theNumber, char possibilities[100][20], int* possibilitiesCount) {
    // This part is simplified for C. You would need to handle combinations and recursion manually.
    // C doesn't have built-in "itertools.product", so consider simplifying or using a recursive approach.

    sprintf(possibilities[0], "%d", theNumber); // The simplest case is the number itself.
    *possibilitiesCount = 1;
}

int countMatchNums(char possibilities[100][20], int possibilitiesCount) {
    int minMatches = 10000; // large number
    for (int i = 0; i < possibilitiesCount; i++) {
        int matchNum = repToMatches(possibilities[i]);
        if (matchNum < minMatches) {
            minMatches = matchNum;
        }
    }
    return minMatches;
}

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

int M(int n) {
    int factors[100];
    int factorCount;

    primeFactorization(n, factors, &factorCount);
    
    char possibilities[100][20];
    int possibilitiesCount;
    
    findAllPossibilities(factors, factorCount, n, possibilities, &possibilitiesCount);
    
    int minMatchesOfAllP = countMatchNums(possibilities, possibilitiesCount);

    int minSum = allSum(n, minMatchesOfAllP);
    
    return minSum < minMatchesOfAllP ? minSum : minMatchesOfAllP;
}

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

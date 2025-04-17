import java.util.ArrayList;
import java.util.HashSet;
import java.util.Arrays;

public class main
{

  public static boolean finBinSearch(int n, Integer[] primes)
{
  int left = 0;
  int right = primes.length - 1;
  int mid = 0;

  while ( left <= mid && mid <= right)
  {
      mid = (right - left) / 2;

      if (primes[mid] == n){
        return true;
      }
      else if (primes[mid] < n){
        left = mid + 1;
      }else{
      right = mid - 1;
      }
    }// end of while

return false;
  }// end of findBinSearch



public static void main(String[] args)
  {
    Integer[] primes = generatePrimes(1000000);
    System.out.println("finished generating primes");

//    HashSet<Integer> primeHashTable = new HashSet<Integer>(Arrays.asList(primes));
    System.out.println("finished generating hashtable");

    int  maxConsec = 0;
    int abProduct = 0;

  int maxAbproduct = 0;
    for (int a = -1000; a < 1000; a++){

      for(int b = -1000; b < 1000; b++){

    maxConsec = testABcomboAndGetConsecNumber(a,b, primes); 
    abProduct = a * b;
    

        if (maxConsec > 1){
          System.out.println("Found a consecutive prime generating with : n^2 + " + a + "n" + " "+ b);
          System.out.println("consecutive " + maxConsec +  "number of times");
        continue;
        }

        if (abProduct > maxAbproduct){
          maxAbproduct = abProduct;
        }


      }// end of inner for

    }     // end of outer for

    System.out.println("max AB product foudn is : " + maxAbproduct);

  }// end of main method

public static boolean isPrime(int n)
{
    if (n <= 1) return false;
    if (n ==2) return true;
    if (n % 2 == 0) return false;

    int sqrt = (int)Math.sqrt(n);
    for(int index = 3; index < sqrt; index++){
      if (n % index == 0) return false;
    }// end of for loop
return true;
  }// end of isPrime

public static Integer[] generatePrimes(int maxPrime)
{
  ArrayList<Integer> prms = new ArrayList<Integer>();
for(int index = 1; index < maxPrime; index++){
    if (isPrime(index)){
        prms.add(index);
      }
    }// end of for 
Integer[] answer = prms.toArray(new Integer[0]);
return answer;      
  }// end of generate primes


public static boolean isPrimeIn(HashSet<Integer> primeHT, int num)
{
    boolean result = primeHT.contains(num);
    return result;
  }// end of is prime in


// return the number of consecutive primes from the quadratic 
public static int testABcomboAndGetConsecNumber(int a, int b, Integer[] primeArr)
{
int n = 0;
int quadraticValue = (n * n) + a * n + b;
boolean result = finBinSearch(quadraticValue,primeArr);
//    System.out.println("quadraticValue is : " + quadraticValue + " for n = " + n);

    while(result == true)
    {
      n++;
    quadraticValue= (n * n) + (a * n) + b;
    result = finBinSearch(quadraticValue,primeArr);

    }// end of while loop
return n;
  }// end of testAB combo


}// end of class main

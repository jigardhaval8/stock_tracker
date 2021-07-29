'''
Author: Soni, Jigar
Email: jigardhaval8@gmail.com
'''
import os
try:
    from yahoo_fin import stock_info
except:
    os.system('pip3 install yahoo_fin')
    from yahoo_fin import stock_info
from tkinter import *
import time 
from datetime import datetime
import winsound
import sys
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
BOLD                       = '\u001b[1m'
B_GREEN_T_WHITE            = '\x1b[6;30;42m'
B_BLACK_T_DARKGREEN        = '\x1b[4;32;40m'
B_GREEN_T_BLACK_LINE       = '\x1b[4;30;42m'
B_RED_T_WHITE              = '\x1b[2;37;41m'
B_YELLOW_T_BLACK           = '\x1b[6;30;43m'
B_BLUE_T_WHITE             = '\x1b[7;34;43m'
B_GREY_T_WHITE             = '\x1b[0;30;47m'
B_BLACK_T_GREY             = '\x1b[0;36;40m'
B_LIGHTGREY_T_WHITE        = '\x1b[6;37;40m'
B_WHITE_T_BLACK            = '\x1b[6;30;47m'
B_LIGHTYELLOW_T_BLACK      = '\x1b[5;30;43m'
B_BLACK_T_YELLOW_UNDERLINE = '\x1b[4;33;40m'
B_BLACK_T_GREY_UNDERLINE   = '\x1b[4;37;40m'
B_GREY_T_RED               = '\x1b[0;31;47m'
B_BLACK_T_DRED             = '\x1b[2;31;40m'
B_BLACK_T_RED              = '\x1b[1;31;40m'
B_GREY_T_GREEN             = '\x1b[0;32;47m'
B_BLACK_T_GREEN            = '\x1b[1;32;40m'
B_BLACK_T_LIGHTBLUE        = '\x1b[2;34;40m'
B_BLACK_T_YELLOW           = '\x1b[1;33;40m'
B_BLACK_T_LRED             = '\x1b[2;37;41m'
T_UNDERLINE                = '\x1b[4;37;40m' 
ECLR                       =  '\x1b[0m' 
CBLINK                     = '\033[5m'
print("| You will asked to enter stock code which you want to track, if you dont know find at  https://finance.yahoo.com")
stock_name = str(input("| Enter Stock Code for (e.x. INTC for Intel): "))
low_buy_limit = float(input("| Enter Low limit Value: "))
high_sell_limit = float(input("| Enter High limit Value: "))
low_value_counter=0
high_value_counter=0
try:
    os.system('cls')
except:
    try:
        os.system('clear')
    except:
        pass
print(BOLD + '|   Live Stock Tracker | Triggers Alarm when stock price reach threshold & beyond |' + ECLR)
print('{:10s} {:10s} {:12s} {:12s} '.format(B_BLACK_T_YELLOW + '{:10s}'.format(str('Time')) + ECLR, BOLD + '{:10s}'.format(stock_name) + ECLR,  B_BLACK_T_GREEN + '{:12s}'.format('BUY:'+str(low_buy_limit)) + ECLR, B_BLACK_T_GREEN + '{:12s}'.format('SELL:'+str(high_sell_limit)) + ECLR))
print('------------------------------------------------------------------')
hitflag=0
while(1):
    time.sleep(0.1)
    now = datetime.now()
    time_string = now.strftime("%H:%M:%S")
    try:
        price = stock_info.get_live_price(stock_name)
    except:
        print(B_BLACK_T_RED + 'Stock Doesnt Exists or code entered is incorrect! check for stock code at https://finance.yahoo.com' + ECLR)
        print('Also this script require Internet connection')
        exit(1)
    price_string = str(round(price,4))
    # Current_stock.set(price)
    # print( "| " + str(time_string) + "| " + str(stock_name) + " : " + str(round(price,4)))
    hitflag=0
    if(price<=low_buy_limit):
        winsound.Beep(frequency, duration)
        # print("Low Value (Time to Buy?) Alarm Triggered!")
        low_value_counter=low_value_counter+1
        low_value_counter_s = B_BLACK_T_GREEN + '{:12s}'.format(str(low_value_counter)) + ECLR
        high_value_counter_s = BOLD + '{:12s}'.format(str(high_value_counter)) + ECLR
        price_string = B_YELLOW_T_BLACK  + '{:12s}'.format(price_string) + ECLR
        hitflag=1

    if(price>=high_sell_limit):
        winsound.Beep(3000, duration)
        # print("High Value Alarm (Time to Sell?) Triggered!")
        high_value_counter=high_value_counter+1
        high_value_counter_s = B_BLACK_T_GREEN + '{:12s}'.format(str(high_value_counter)) + ECLR
        low_value_counter_s = BOLD + '{:12s}'.format(str(low_value_counter)) + ECLR
        price_string = B_YELLOW_T_BLACK  + '{:12s}'.format(price_string) + ECLR
        hitflag=1
    
    if(hitflag==0):
        low_value_counter_s = BOLD + '{:12s}'.format(str(low_value_counter)) + ECLR
        high_value_counter_s = BOLD + '{:12s}'.format(str(high_value_counter)) + ECLR
        price_string = BOLD  + '{:12s}'.format(price_string) + ECLR

    print('{:10s} {:10s} {:12s} {:^12s} \r'.format(B_BLACK_T_YELLOW + '{:10s}'.format(str(time_string)) + ECLR, price_string,  str(low_value_counter_s), str(high_value_counter_s)), end="")
    sys.stdout.flush()

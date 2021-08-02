'''
Portfolio Tracker Live

Author: Soni, Jigar
Email: jigardhaval8@gmail.com
Documentation: jigardhaval8.wordpress.com

ver0.3
'''
import os
try:
    from numpy import set_string_function
except:
    os.system('pip3 install numpy')
    from numpy import set_string_function
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
try:
    import configparser
except:
    os.system('pip3 install configparser')
    import configparser

try:
    import json
except:
    os.system('pip3 install json')
    import json
# import matplotlib.pyplot as plt

config = configparser.ConfigParser()
config.read('portfolio.cfg')
try:
    stock_ids = config.get("StockCodes", "InvestedStocks")
    stock_id_list = json.loads(stock_ids)
except:
    print(" Exception! - Invalid or Incorrect Config file, Cannot proceed")
    exit(1)

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
def time_to_sell_notify(sell,bflag,sflag):
    if(sell==1):
        if(bflag):
            winsound.Beep(2000, 700)
        if(sflag):
            winsound.Beep(frequency, duration)
    else:
        pass
stock_id_index=[]
stock_id_noofshare=[]
stock_id_avgbuy=[]
stock_id_liveprice=[]
stock_id_invested=[]
expected_return=[]
expected_buy=[]
buy_hit=[]
sell_hit=[]
total_invested=0
desired_return=0
expected_buy_feature=0
for i in range(0,len(stock_id_list)):
    try:
        sell_hit.append(0)
        buy_hit.append(0)
        stock_id_index.append(stock_id_list[i][0])
        stock_id_noofshare.append(stock_id_list[i][1])
        stock_id_avgbuy.append(stock_id_list[i][2])
        expected_return.append(stock_id_list[i][3])
        investmentamount = float(stock_id_list[i][1])*float(stock_id_list[i][2])
        stock_id_invested.append(round(investmentamount,2))
        total_invested = total_invested + investmentamount
        try:
            expected_buy.append(stock_id_list[i][4])
            expected_buy_feature=1
        except:
            expected_buy_feature=0
    except:
        print(B_BLACK_T_RED + "Oops, Something is not right!, Probably Input file is not right, check again - one or more input is missing " + ECLR)
        exit(1)
    # print("Stock : " + str(stock_id_list[i][0]) + " Total Share Invested: "+ str(stock_id_list[i][1]) + " Average: "+ str(stock_id_list[i][2]))
def clearscreen():
    try:
        os.system('cls')
    except:
        try:
            os.system('clear')
        except:
            pass
expected_return_amount=0
clearscreen()
while(1):
    total_actuals=0
    desired_return=0
    desired_hit_flag=0
    buy_flag=0
    sell_flag=0
    this_is_watchlist=0
    print_buffer=[]
    time1=0
    time2=0
    for i in range(0,len(stock_id_list)):
        now = datetime.now()
        if(i==0):
            time1=now
        elif(i==(len(stock_id_list)-1)):
            time2=now
        time_string = now.strftime("%H:%M:%S")
        stock_name_is = stock_id_index[i]
        live_stock_price = stock_info.get_live_price(stock_id_index[i])
        actual_amount_live = live_stock_price*float(stock_id_noofshare[i])
        total_actuals = total_actuals + actual_amount_live
        return_amount=round((actual_amount_live-stock_id_invested[i]),0)
        expected_return_amount=round((float(stock_id_invested[i])*float(expected_return[i]))/100,0)
        if(actual_amount_live==0):
            this_is_watchlist=1
        else:
            this_is_watchlist=0

        stock_name_color = BOLD 
        if(this_is_watchlist):
            return_per = 0
            expected_share_sell_price='NA'
            stock_name_color = B_BLACK_T_GREY 
            target_sell_price_print= BOLD + '{:>12s}'.format(str(expected_share_sell_price)) + ECLR
        else:
            return_per = round(((actual_amount_live-stock_id_invested[i])/stock_id_invested[i])*100,2)
            expected_share_sell_price = round(((float(stock_id_invested[i])+expected_return_amount)/float(stock_id_noofshare[i])),2)
            if(live_stock_price>=expected_share_sell_price):
                sell_hit[i]=sell_hit[i]+1
                stock_name_color = B_GREEN_T_BLACK_LINE
                target_sell_price_print= B_GREEN_T_BLACK_LINE + '{:>12s}'.format(str(expected_share_sell_price)+" ["+str(sell_hit[i])+"]") + ECLR
                desired_hit_flag=1
                sell_flag=1
            else:
                # stock_name_color = BOLD 
                target_sell_price_print= BOLD + '{:>12s}'.format(str(expected_share_sell_price)+" ["+str(sell_hit[i])+"]") + ECLR


        desired_return=desired_return+expected_return_amount

        if(expected_buy_feature==1):
            expected_new_buy_price = (round((float(stock_id_avgbuy[i])*float((100+int(expected_buy[i]))/100)),2))
            if(live_stock_price<=expected_new_buy_price):
                buy_hit[i]=buy_hit[i]+1
                expected_new_buy_price = B_YELLOW_T_BLACK+ '{:>12s}'.format(str(expected_new_buy_price)+" ["+str(buy_hit[i])+"]") + ECLR
                stock_name_color = B_YELLOW_T_BLACK
                buy_flag=1
            else:
                expected_new_buy_price = BOLD + '{:>12s}'.format(str(expected_new_buy_price)+" ["+str(buy_hit[i])+"]") + ECLR
                # stock_name_color = BOLD
                desired_hit_flag=1
            # expected_new_buy_price = round((float(stock_id_avgbuy[i])),2)

        if(return_per>0):
            return_print_data = B_BLACK_T_GREEN + '{:>18s}'.format(str(int(return_amount)) + "(" +str(return_per) + "%)")+ECLR
            actual_amount_print_data = B_BLACK_T_GREEN + '{:>12s}'.format(str(round(actual_amount_live,2))) + ECLR
        else:
            return_print_data = B_BLACK_T_RED + '{:>18s}'.format(str(int(return_amount)) + "(" +str(return_per) + "%)")+ECLR
            actual_amount_print_data = B_BLACK_T_RED + '{:>12s}'.format(str(round(actual_amount_live,2))) + ECLR
        


        target_return_amount=B_BLACK_T_GREEN + '{:>18s}'.format(str(int(expected_return_amount))) + ECLR
        target_return_amount_with_per= B_BLACK_T_GREEN + '{:>18s}'.format( str(expected_return_amount)+'('+str(expected_return[i])+'%)') + ECLR
        print_buffer.append('{:10s} {:15s} {:4s} {:>12s} {:>12s} {:>18s} {:>18s} {:18s} {:18s} {:15s}'.format(B_BLACK_T_YELLOW + '{:10s}'.format(str(time_string)) + ECLR, stock_name_color + '{:15s}'.format(str(stock_name_is)) + ECLR, BOLD + '{:4s}'.format(str(stock_id_noofshare[i])) + ECLR, BOLD + '{:>12s}'.format(str(stock_id_invested[i])) + ECLR, actual_amount_print_data, return_print_data,  target_return_amount_with_per, target_sell_price_print, expected_new_buy_price,  B_BLACK_T_YELLOW + '{:>9s}'.format(str(round(live_stock_price,2))) + ECLR))
    clearscreen()
    print('+-----------------------------------------------------------------------------------------------------------------------------------')
    print('| ' + B_BLACK_T_GREY + 'Portfolio Tracker ' + ECLR)
    print('+-----------------------------------------------------------------------------------------------------------------------------------')
    print('{:10s} {:15s} {:4s} {:>12s} {:>12s} {:>18s} {:>18s} {:18s} {:18s} {:15s}'.format(B_BLACK_T_YELLOW + '{:10s}'.format(str('Time')) + ECLR, BOLD + '{:15s}'.format(str('Stock')) + ECLR, BOLD + '{:4s}'.format(str('#')) + ECLR, BOLD + '{:>12s}'.format(str('Invested')) + ECLR,  BOLD + '{:>12s}'.format(str('Actuals')) + ECLR, BOLD + '{:>18s}'.format(str('% Return')) + ECLR,  B_BLACK_T_GREEN + '{:>18s}'.format(str('Desire Gain')) + ECLR, BOLD + '{:>12s}'.format(str('TargetSell')) + ECLR, BOLD + '{:>12s}'.format(str('TargetBuy')) + ECLR,  B_BLACK_T_YELLOW + '{:>9s}'.format(str('Live')) + ECLR))
    print('+-----------------------------------------------------------------------------------------------------------------------------------')
    for i in range(0,len(print_buffer)):
        print(print_buffer[i])
    print('+-----------------------------------------------------------------------------------------------------------------------------------')
    print('| ' + B_BLACK_T_GREY + 'Portfolio Summary ' + ECLR)
    print('+-----------------------------------------------------------------------------------------------------------------------------------')
    cummulative_return=total_actuals-total_invested
    cummulative_return_per=(cummulative_return/total_invested)*100
    if(cummulative_return_per>=0):
        coloris=B_BLACK_T_GREEN
    else:
        coloris=B_BLACK_T_RED
    desire_return_per=round((desired_return/total_invested)*100,2)
    time_to_sell_notify(desired_hit_flag,buy_flag,sell_flag)
    print('{:10s} {:15s} {:4s} {:>12s} {:>12s} {:>18s} {:>18s} {:18s} {:18s} {:15s}'.format(B_BLACK_T_YELLOW + '{:10s}'.format(str(' ')) + ECLR, BOLD + '{:15s}'.format(str(len(stock_id_list))) + ECLR, BOLD + '{:4s}'.format(str(' ')) + ECLR, BOLD + '{:>12s}'.format(str(round(total_invested,2))) + ECLR,  coloris + '{:>12s}'.format(str(round(total_actuals,2))) + ECLR, coloris + '{:>18s}'.format(str(round(cummulative_return,2)) + "(" + str(round(cummulative_return_per,2))+ "%)") + ECLR,  B_BLACK_T_GREEN + '{:>18s}'.format(str(desired_return) + "(" + str(desire_return_per)+ "%)") + ECLR, BOLD + '{:>12s}'.format(str(' ')) + ECLR, BOLD + '{:>12s}'.format(str(' ')) + ECLR,  '{:>9s}'.format(str(' '))))
    print("Refresh Time: " + str((time2-time1).total_seconds()) + " seconds" )


#Plot
# labels = stock_id_index
# sizes = stock_id_invested
# # colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
# # patches, texts = plt.pie(sizes, shadow=True,autopct='%1.1f%%', startangle=90)
# plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
# # plt.legend(patches, labels, loc="best")
# plt.axis('equal')
# # plt.tight_layout()
# plt.show()

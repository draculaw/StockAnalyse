
import csv_parser

import matplotlib.pyplot as plt
import numpy as np
import pandas



def calc_the_bollinger(code, period=20, k=2):
    if not isinstance(code, str):
        raise "the code should be str"
    stock_data = csv_parser.get_stock_from_csv(code)
    #stock_data.reverse()

    stock_data = sorted(stock_data, cmp=lambda x, y: cmp(x.date,y.date))
    print stock_data[0].date

    #data = [d for d in raw_data if d[0] == code and d[6].replace(' ', '') != '0']
    stock_data[0].ma = 0
    stock_data[0].dn = 0
    stock_data[0].up = 0

    for i in range(1, period):
   		stock_data[i].ma = 0
   		stock_data[i].dn = 0
   		stock_data[i].up = 0
    
    for i in range(period, len(stock_data)):
   	    close_list = [d.close for d in stock_data[i-period:i]]
   	    stock_data[i].ma = sum(close_list)/20.0
   	    stock_data[i].dn = stock_data[i].ma - k * np.std(close_list)
   	    stock_data[i].up = stock_data[i].ma + k * np.std(close_list)

    ttt = sorted(stock_data, cmp=lambda x, y: cmp(x.date,y.date))
    return ttt
		

if __name__ == "__main__":

    data = calc_the_bollinger("002093.SZ")

    income = 0
    hold = 0
    buy = 0    
    result = []

    for i in range(20, len(data)):
        if hold == 0:
            if data[i].close > data[i-1].close and data[i].close > data[i].ma and 0.2 > data[i-1].close - data[i-1].ma > 0:
                buy = data[i].close
                hold = 1
                print "date %s buy at %s" %(str(data[i].date), str(data[i].close))

        if hold == 1:
            if data[i-1].close > data[i-1].up and data[i].close < data[i].up:
                income = income + data[i].close - buy
                hold = 0
                result.append(data[i].close - buy > 0)
                print "date %s sell at %s" %(str(data[i].date), str(data[i].close))


    win = [i for i in result if i]

    #print result
    #print win
    print len(result)
    print len(win)
    print 1.0*len(win)/len(result)
    print income


    #for i in range(20:len(data)):
    #	pass
    
    
    
    
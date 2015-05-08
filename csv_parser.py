import pandas
import matplotlib.pyplot
import numpy
import csv
import sqlite3
import get
from datetime import datetime

def init_data_from_db():

    db = get.db
    c = db.cursor()
    cmd = "select * from stock"
    c.execute(cmd)
    l1 = c.fetchall()
    c.close()  

    l2 = [list(d) for d in l1]
    
    with open ("stock1.csv", "w") as csvfile:
        fieldnames = ['code', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close' ]
        writer = csv.DictWriter(csvfile, fieldnames, delimiter=";")
        writer.writeheader()

        for data in l2:
            #data[6].replace(',', '')
            d = {
                    "code":data[0], 
                    "date":data[1],
                    "open":data[2],
                    "high":data[3],
                    "low":data[4],
                    "close":data[5],
                    "volume":data[6],
                    "adj_close":data[7]
                }
            writer.writerow(d)

def get_data_from_csv():
    with open ("stock1.csv", "r") as csvfile:
        data = csvfile.readlines()
    # data = data[1:]
    
    data = [d.split(';') for d in data ]
  
    dataframe = pandas.DataFrame(data)
    series = pandas.Series(data)

    return dataframe, series[1:]

class stock_data():
    def __init__(self, data=[]):
        if len(data) < 8:
            raise "Not a stock data"

        self.code = data[0]
        self.open = float(data[2])
        self.high = float(data[3])
        self.low = float(data[4])
        self.close = float(data[5])
        self.volume = int(data[6].replace(',', ''))
        self.date = datetime.strptime(data[1], " %Y%m%d")

    def __str__(self):
        return '; '.join([str(self.date), self.code, str(self.open), str(self.high),str(self.low), str(self.close), str(self.volume)])

def get_stock_from_csv(code, all_data=None):
    if not isinstance(code, str):
        raise "Code should be str"

    if all_data == None:
        dataframe, series = get_data_from_csv()
        all_data = series
        
    data = [ stock_data(d) for d in all_data if d[6] != '0' and d[0] == code ]
    
    return data
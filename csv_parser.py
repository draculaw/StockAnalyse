

import csv
import get

import pandas
from datetime import datetime
import os


def init_data_from_db():

    db = get.db
    c = db.cursor()
    cmd = "select * from stock"
    c.execute(cmd)
    l1 = c.fetchall()
    c.close()  

    l2 = [list(d) for d in l1]
    
    for data in l2:
        filename = "csv/" + data[0] + ".csv"

        if not os.path.exists(filename):           

            with open ("stock.csv", "w") as csvfile:
                fieldnames = ['code', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close' ]
                writer = csv.DictWriter(csvfile, fieldnames, delimiter=";")
                writer.writeheader()            
        
        with open (filename, "a") as csvfile:
            fieldnames = ['code', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close' ]
            writer = csv.DictWriter(csvfile, fieldnames, delimiter=";")
            writer.writeheader()

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

all_data=None

def get_data_from_csv():

    global all_data

    if all_data is None:
        with open ("stock1.csv", "r") as csvfile:
            data = csvfile.readlines()
    # data = data[1:]
    
        data = [d.split(';') for d in data ]
  
    #dataframe = pandas.DataFrame(data)

        all_data = pandas.Series(data)[1:]


    return all_data

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
        self.ma = 0.0
        self.up = 0.0
        self.dn = 0.0

    def __str__(self):
        return '; '.join([str(self.date), self.code, str(self.open), str(self.high),str(self.low), str(self.close), str(self.volume)])


def get_stock_from_csv(code):
    if not isinstance(code, str):
        raise "Code should be str"
    


    series = get_data_from_csv()
    all_data = series
        
    data = [ stock_data(d) for d in all_data if d[6] != '0' and d[0] == code ]
    
    return data

if __name__  == "__main__":
    init_data_from_db()
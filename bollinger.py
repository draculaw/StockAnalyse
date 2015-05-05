
import pandas
import csv
import sqlite3
import get

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
    data = data[1:]
    
    data = [d.split(';') for d in data ]
    print data[0]

    s = pandas.Series(data)

    print s[0][6]
    print type(s[0][6])


if __name__ == "__main__":
    # init_data_from_db()
    get_data_from_csv()
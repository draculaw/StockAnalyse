# coding=utf-8

# read from start
# start  http://finance.yahoo.com/q/hp?s=600568.SS

# if the next exist read the next
# next <a rel="next" href="/q/hp?s=600568.SS&amp;d=3&amp;e=14&amp;f=2015&amp;g=d&amp;a=4&amp;b=18&amp;c=2001&amp;z=66&amp;y=66" data-rapid_p="21">Next</a>

# <body><div><div><table id="yfncsumtab"><tbody><tr><td><table i"yfnc_datamodoutline1"><tbody><tr><td><table><tbody><tr>

# <tr id="yui_3_9_1_9_1428976539885_38"><td class="yfnc_tabledata1" nowrap="" align="right">Apr 13, 2015</td><td class="yfnc_tabledata1" align="right">20.22</td><td class="yfnc_tabledata1" align="right">21.25</td><td class="yfnc_tabledata1" align="right">20.22</td><td class="yfnc_tabledata1" align="right">20.49</td><td class="yfnc_tabledata1" align="right">14,455,400</td><td class="yfnc_tabledata1" align="right">20.49</td></tr>

# sina real time price http://hq.sinajs.cn/list=sh601006

import urllib2
import lxml
import lxml.html
import StringIO
import datetime
import sqlite3
import requests

import csv

import get_code
import os

#stock_info = {}

def connect_db():
    db = sqlite3.connect("stock.db")
    return db

def close_db():
    db.close()

db = connect_db()

db_create_script = (
    'CREATE TABLE `stock` ('
'	`Code`	TEXT NOT NULL,'
'	`date`	TEXT,'
'	`open`	REAL,'
'	`high`	REAL,'
'	`low`	REAL,'
'	`close`	REAL,'
'	`volume`	INTEGER,'
'	`adj_close`	REAL,'
'   `PK`  TEXT,'
'   PRIMARY KEY(PK)'
');')

def init_db():
    pass

data_list = []
def insert_one_data(code, data):

    data[0].text = datetime.datetime.strptime(data[0].text, "%b %d, %Y").strftime("%Y%m%d")
    data[5].text.replace(',', '').replace('"', '')

    c = db.cursor()
    tmp_cmd =    "\", \" ".join(
            [
             code, 
             data[0].text,
             data[1].text,
             data[2].text,
             data[3].text,
             data[4].text,
             data[5].text,
             data[6].text,
             ":".join([code, data[0].text])
             ])

    cmd = "\"".join(
            [
                'insert into stock VALUES (',
                tmp_cmd,
                ')'
                ])
    c.execute(cmd)
    db.commit()
    c.close()

    filename = "csv/" + code + ".csv"

    if not os.path.exists(filename):           

        with open ("stock.csv", "w+") as csvfile:
            fieldnames = ['code', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close' ]
            writer = csv.DictWriter(csvfile, fieldnames, delimiter=";")
            writer.writeheader()     
                   
    with open ("csv/" + code + ".csv", "a") as csvfile:
        fieldnames = ['code', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close' ]
        writer = csv.DictWriter(csvfile, fieldnames, delimiter=";")
        data = { "code":code, 
                 "date":data[0].text,
                 "open":data[1].text,
                "high":data[2].text,
                 "low":data[3].text,
                 "close":data[4].text,
                 "volume":data[5].text,
                 "adj_close":data[6].text}
        writer.writerow(data)

def get_stock_info(url, code, arg = ""):
    print "download: " + url + arg 
    print "Start Time ", datetime.datetime.now()
    #res = urllib2.urlopen(url + arg)
    res = requests.get(url + arg)
    print "Over Time ", datetime.datetime.now()
    #context = res.read()
    res.encoding  = res.apparent_encoding 
    context = res.content
    #lines = context.split("\n")

    doc = lxml.html.parse(StringIO.StringIO(context))
    next_url = doc.xpath("//a[@rel='next']")

    data = doc.xpath("//td[@class='yfnc_tabledata1']/..")

    for d in data:
        if len(d) != 7:
            continue
        #single_info = {}
        
        #single_info['date'] = datetime.datetime.strptime(
        #        d[0].text,
        #        "%b %d, %Y")
        # single_info['date'] = d[0].text
        # single_info['open'] = d[1].text
        # single_info['high'] = d[2].text
        # single_info['low'] = d[3].text
        # single_info['close'] = d[4].text
        # single_info['vol'] = d[5].text
        # single_info['adj_close'] = d[6].text
        insert_one_data(code, d)

        # TODO: calc the bollinger bands
#        stock_info[code].append(single_info)

    if len(next_url) > 0:
        get_stock_info(url=url, arg=next_url[0].get('href'), code=code)

def get_stock_list_info(code_list):
    url = "http://finance.yahoo.com"     #  600563.SS"
    for code in code_list:
        #stock_info[code] = []
        # try:
        print "get the Stock: ", code 
        print "Begin Time ", datetime.datetime.now()
        get_stock_info(url=url, code=code, arg='/q/hp?s='+ code)
        
        print "End Time ", datetime.datetime.now()
        
        # except Exception as e :
        #     print "error %s on get: %s ", (e,code) 
        #     raise e
        # finally:
        #     print "get the Stock: %s Finished", code , " Time ", datetime.datetime.now()

def init_get():
    code_list = set(get_code.get_code_list())
    get_stock_list_info(code_list)
    db.close()

def update_list(ll):
    get_stock_list_info(list(ll))
    db.close()

def update_get():
    code_list = set(get_code.get_code_list())
    get_stock_list_info(list(code_list))
    db.close()


def init_db():
    cmd = "delete from stock where 1=1"

    c = db.cursor()
    c.execute(cmd)
    db.commit()
    c.close()

    os.system("mkdir csv")

    # with open ("stock.csv", "w") as csvfile:
    #     fieldnames = ['code', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close' ]
    #     writer = csv.DictWriter(csvfile, fieldnames, delimiter=";")
    #     writer.writeheader()



if __name__ == "__main__":
    print "please use the single cmd line"
    print "init_get.py for get all code from the file hehe_sz, hehe_ss and code_list_hard in get_code.py"
    print "update.py  for fetch new data from the database"
    print "fetch_one.py is for fetch an new code has not insert into db"
    
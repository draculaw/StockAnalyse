
import csv_parser

import matplotlib.pyplot
import numpy
import pandas

if __name__ == "__main__":
    
    data = csv_parser.get_stock_from_csv("000063.SZ")
    data = csv_parser.get_stock_from_csv("601398.SS")
    
    print data[0]
    
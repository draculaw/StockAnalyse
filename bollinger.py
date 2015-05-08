
import csv_parser

if __name__ == "__main__":
    
    data = csv_parser.get_stock_from_csv("000063.SZ")
    
    print data[0]
    
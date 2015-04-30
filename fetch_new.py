import sys
import get
import datetime

if __name__ == "__main__":
    print "not implement"

    if len(sys.argv) < 2:
        print "useage fetch_new.py <code1> ... <coden>"
    
    start = datetime.datetime.now()
    print "Start:", start
    print "Start %s End: %s" %(start.strftime("%Y-%m-%d %H:%M:%S:%Z"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%Z"))
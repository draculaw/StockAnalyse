import sys
import get
import datetime
import sqlite3

if __name__ == "__main__":
    print "not implement"

    if len(sys.argv) < 2:
        print "useage fetch_new.py <code1> ... <coden>"
    raw_arg = sys.argv[1:]

    db = get.db
    c = db.cursor()
    tmp_cmd = "delete from stock where code in "
    raw_code_list = '","'.join(raw_arg)
    cmd = "".join([tmp_cmd, '("', raw_code_list, '")'])
    c.execute(cmd)

    c.close()


    
    start = datetime.datetime.now()
    print "Start:", start
    get.update_list(raw_arg)
    print "Start %s End: %s" %(start.strftime("%Y-%m-%d %H:%M:%S:%Z"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%Z"))
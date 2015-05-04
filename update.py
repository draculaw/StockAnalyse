import get
import datetime
import sqlite3

if __name__ == "__main__":
    
    #get.connect_db()
    db = get.db
    c = db.cursor()
    cmd = "select distinct code from stock"
    c.execute(cmd)
    list = c.fetchall()
    c.close()

    start = datetime.datetime.now()
    print "Start:", start
    get.update_list(list)
    print "Start %s End: %s" %(start.strftime("%Y-%m-%d %H:%M:%S:%Z"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%Z"))
    
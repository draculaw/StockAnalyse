import get
import datetime
import sqlite3

if __name__ == "__main__":
    
    #get.connect_db()
    db = get.db
    c = db.cursor()
    cmd = "select distinct code from stock"
    c.execute(cmd)
    ll = c.fetchall()
    c.close()
    if  isinstance(ll[0], tuple):
        
        ll = [d[0] for d in ll]
    elif isinstance(ll[0], str):
        
        pass
    else:
        raise "The database has some issue"

    start = datetime.datetime.now()
    print "Start:", start
    get.update_list(ll)
    print "Start %s End: %s" %(start.strftime("%Y-%m-%d %H:%M:%S:%Z"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%Z"))
    
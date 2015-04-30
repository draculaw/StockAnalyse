import get
import datetime

if __name__ == "__main__":
    
    get.connect_db()
    start = datetime.datetime.now()
    print "Start:", start
    get.update_get()
    print "Start %s End: %s" %(start.strftime("%Y-%m-%d %H:%M:%S:%Z"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%Z"))
    
from get import init_get, init_db
import datetime

if __name__ == "__main__":
    init_db()
    start = datetime.datetime.now()
    print "Start:", start
    init_get()
    print "Start %s End: %s" %(start.strftime("%Y-%m-%d %H:%M:%S:%Z"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%Z"))
          
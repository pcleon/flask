#!/usr/local/bin/python
#coding: utf-8 
#import time
import sqlite3

def flowOut():
    cn = sqlite3.connect('my.db')
    cx = cn.cursor()
    sql = "select * from flow order by time desc limit 1"
    f = cx.execute(sql)
    flows = f.fetchone() 
    cn.close()
    return flows
###########################
if __name__ == "__main__":
    try :
        #getdata(sys.argv[1])
        flowOut()
    except IndexError:
        #print "Usage: %s date(YY-MM-DD)" %(sys.argv[0])
        pass

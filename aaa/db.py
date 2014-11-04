#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import time
import sys
import sqlite3

TOTAL=1650000
ALLWO=50000
DB_NAME='my.db'

def getdata(oneday):
    cn = sqlite3.connect(DB_NAME)
    cx = cn.cursor()
    f = cx.execute("select max(wo),max(alluser) from aaa where day>=date('%s','-6 days') and day<= date('%s')"  %(oneday,oneday))
    now_maxwo , now_maxall = f.fetchone()
    f = cx.execute("select max(wo),max(alluser) from aaa where day>=date('%s','-13 days') and day<= date('%s','-7 days')"  %(oneday,oneday))
    last_maxwo , last_maxall = f.fetchone()
    cn.close()
##########################
    #print now_maxwo,now_maxall,last_maxwo,last_maxall
    totalPercent = round( float(now_maxall) / TOTAL * 100 , 2)
    totalRatio = round( (float(now_maxall)-last_maxall)/last_maxall*100 , 2)
    woPercent = round( float(now_maxwo) / ALLWO * 100 , 2)
    woRatio = round( (float(now_maxwo) - last_maxwo ) / last_maxwo * 100 , 2)
    totalStatus=(totalRatio>0 and "上升" or "下降")
    woStatus=(woRatio>0 and "上升" or "下降")
    #print totalPercent , totalStatus, abs(totalRatio)
    #print woPercent , woStatus, abs(woRatio)
    return [now_maxall, totalPercent , totalStatus, abs(totalRatio), now_maxwo, woPercent , woStatus, abs(woRatio)]


def putdata(str_data=''):
    cn=sqlite3.connect(DB_NAME)
    cx=cn.cursor()
    data = str_data.split('\n')
    for line in data:
        line = line.strip().split()
        line[0] = time.strftime("%Y-") + line[0].replace('月','-').replace('日','')
        try:
            cx.execute("replace into aaa values (?,?,?)" ,(line[0],line[1],line[-1]))
        except  sqlite3.IntegrityError:
            pass
    cn.commit()
    cn.close()
###########################
if __name__ == "__main__":
    try :
        getdata(sys.argv[1])
    except IndexError:
        print "Usage: %s date(YY-MM-DD)" %(sys.argv[0])

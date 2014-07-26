#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import time
import sqlite3
import sys

DB_NAME='my.db'

def fomatday(day):
    newday = time.strftime("%Y-") + day.replace('月','-').replace('日','')
    return newday

def inputdata(filename):
    cn=sqlite3.connect(DB_NAME)
    cx=cn.cursor()
    for line in open(filename):
        listline = line.split()
        newday = time.strftime("%Y-") + listline[0].replace('月','-').replace('日','')
        listline[0]=newday
        print listline
        try:
            cx.execute("insert into aaa values (?,?,?)" ,(listline[0],listline[1],listline[-1]))
        except  sqlite3.IntegrityError:
            pass
    cn.commit()
    cn.close()

def in2(str_data=''):
    cn=sqlite3.connect(DB_NAME)
    cx=cn.cursor()
    data = str_data.strip().split('\n')
    for line in data:
        line = line.strip().split()
        line[0] = time.strftime("%Y-") + line[0].replace('月','-').replace('日','')
        print line
        try:
            cx.execute("insert into aaa values (?,?,?)" ,(line[0],line[1],line[-1]))
        except  sqlite3.IntegrityError:
            pass
    cn.commit()
    cn.close()

#select * from aaa where day>=date('now','-7 days') limit 3;
#cx.execute("select * from aaa where day >= date('%s','-7 days') limit 7" %a)
if __name__ == "__main__":
    try:
        inputdata(sys.argv[1])
    except IndexError:
        print "Usage: %s 文件名" %sys.argv[0]

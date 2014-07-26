# -*- coding: utf-8 -*-

from __future__ import division
import sqlite3
import sys
import time
import re

DB_NAME='my.db'

class fuck():
    def __init__(self):
        cn = sqlite3.connect(DB_NAME)
        cx = cn.cursor()
        out = cx.execute("select * from flow order by time desc limit 1").fetchone()
        cx.close()
        self.lastdata={
                'cc_out' : out[1],
                'flow_out' : out[2],
                'flow_in' : out[3]
                }

#        self.nowdata={}


    def dofile(self,filename):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        import xlrd
        import os
        outList=[]

        xlsData = xlrd.open_workbook(filename)
        table = xlsData.sheet_by_index(0)
        for rnum in range(0,table.nrows):
            if "Pos" in table.cell(rnum,4).value:
                city = table.row_values(rnum)[2].replace('至','-').replace('A1 ','')
                   #地市, 带宽, 平均入,平均出,峰值入,峰值出
                outList += [[ city, (table.row_values(rnum)[8]<10000 and 10000 or table.row_values(rnum)[8]), table.row_values(rnum)[9], table.row_values(rnum)[10], table.row_values(rnum)[13], table.row_values(rnum)[14]]]

        checkout = [u"南宁-南宁",u"柳州-南宁",u"桂林-南宁",u"梧州-南宁",u"玉林-南宁",u"百色-南宁",u"钦州-南宁",u"河池-南宁",u"北海-南宁",u"防城港-南宁",u"贵港-南宁",u"贺州-南宁",u"来宾-南宁",u"崇左-南宁",u"南宁-柳州",u"柳州-柳州",u"桂林-柳州",u"梧州-柳州",u"玉林-柳州",u"百色-柳州",u"钦州-柳州",u"河池-柳州",u"北海-柳州",u"防城港-柳州",u"贵港-柳州",u"贺州-柳州",u"来宾-柳州",u"崇左-柳州"]
        final_list=[]
        for x in checkout:
            for y in outList:
                if re.match(x,y[0]):
                    final_list += [y]

        print final_list[0][0]
        return final_list

    def dataToDb( self, data , day=time.strftime('%Y-%m-%d',time.localtime())):
        cn=sqlite3.connect(DB_NAME)
        cx=cn.cursor()
        for x in data:
            cx.execute(" insert into tb values (?,?,?,?,?,?,?)" , (day, x[0], x[1], x[2], x[3], x[4], x[5]) )
        cn.commit()
        cn.close()

#    def calData(self):
        cn=sqlite3.connect(DB_NAME)
        cx=cn.cursor()
        #总带宽
        sql = "select sum(bw) from tb where inputday='%s'" %day
        total_bw = cx.execute(sql).fetchone()[0] ;
        #城域网出口中继峰值流量
        sql = "select sum(max(topin,topout)) from tb where inputday='%s'" %day
        cc_out = cx.execute(sql).fetchone()[0]
        #出口中继峰值利用率
        sql = "select sum(max(topin,topout))/sum(bw)*100 from tb where inputday='%s'" %day
        per_cc_out = cx.execute(sql).fetchone()[0]
        #中继最大入流量
        sql = "select sum(topin) from tb where inputday='%s'" %day
        flow_in = cx.execute(sql).fetchone()[0]
        #中继最大出流量
        sql = "select sum(topout) from tb where inputday='%s'" %day
        flow_out = cx.execute(sql).fetchone()[0]
        #两地利用率
        sql = "select sum(max(topin,topout))/sum(bw)*100 from tb where inputday='%s' and city like '%%-南宁%%'" %day
        per_nn = cx.execute(sql).fetchone()[0]
        sql = "select sum(max(topin,topout))/sum(bw)*100 from tb where inputday='%s' and city like '%%-柳州%%'" %day
        per_lz = cx.execute(sql).fetchone()[0]
        nowdata = {
                'day' : day,
                'total_bw' : round(total_bw/1000,0),
                'cc_out' : round(cc_out/1000,2),
                'flow_in' : round(flow_in/1000,2),
                'flow_out' : round(flow_out/1000,2),
                'per_cc_out' : round(per_cc_out,2),
                'per_nn' : round(per_nn,2),
                'per_lz' : round(per_lz,2)
                }

        return nowdata


#        return ['2014-07-22', total_bw, cc_out, per_cc_out, flow_in, flow_out, per_nn, per_lz]


#print "%s %s %s %s" %( ut[0], cc_out, flow_out, flow_in)
#f=fuck()
#s=f.sortdata('RPT02050_20140709_20140715_20140709_20140715.xls')
#f.dataToDb('2014-07-22',s)
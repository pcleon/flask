#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import time,os
from flask import Blueprint, request, render_template, abort, request, redirect
from flask import url_for, redirect

flow = Blueprint('flow', __name__, template_folder='templates')

import sqlite3

import cls


UPLOAD_FOLDER = 'upload'
DB_NAME='my.db'


@flow.route('/',methods=['GET','POST'])
@flow.route('/index',methods=['GET','POST'])
def index():
    if request.method == "POST":
        day = request.form.get('day')
        f = request.files['filename']
        print f, f.filename
        DAY = f.filename[-12:-4]
        f.save(os.path.join(UPLOAD_FOLDER, DAY + f.filename[-4:]))
        fname = os.path.join(UPLOAD_FOLDER, DAY + f.filename[-4:])
        #可以打印出post的数据
        #return "%s %s" %( day,fname)
        #可以跳转
        #return redirect(url_for('.up'))
        #依然在原页面,但是可以得到数据
        #return redirect(url_for('up',day=day,fname=fname))
        #可以跳转,也可以以get方式传数据,但是在新url里面无法获取数据
        return redirect(url_for('.up',day=day,fname=fname))
    else :
        return render_template("index.html")

#@flow.route('/up', methods=['POST'])
@flow.route('/up')
def up():
    #return "%s" %(''.join(dict(request.args)['day']))
    #request.args可以获取get的参数并以ImmutableMultiDict类型(相当于字典)保存
    req = request.args
    DAY = time.strftime("%Y-%m-%d",time.strptime(req['fname'][-12:-4], "%Y%m%d"))
    action = cls.fuck()
    lastdata = action.lastdata(DAY)
    every_flow = action.dofile(req['fname'])
    #day, total_bw, cc_out, per_cc_out, flow_in, flow_out, per_cc_out, per_nn, per_lz
    middle = action.dataToDb(every_flow, DAY)
    nowdata = action.nowdata(DAY)
    sixty = action.lt60(DAY)
    num60 = len(sixty)
    str60 = ', '.join(map(lambda x: x[0] +' '+ str(round(x[1],2)) + '%', sixty))
    f_in = round( (nowdata[5]-lastdata[5])/lastdata[5]*100, 2)
    f_out = round( (nowdata[4]-lastdata[4])/lastdata[4]*100, 2)
    stat_in = ('上升' if f_in>=0 else '下降')
    stat_out = ('上升' if f_out>=0 else '下降')
    f_in = abs(f_in)
    f_out = abs(f_out)
    
    #print lastdata
    #print middle
    #print nowdata
    return render_template("up.html", DAY=DAY, flow = every_flow, lastdata=lastdata, nowdata=nowdata, num60=num60, str60=str60, f_in=f_in, stat_in=stat_in, f_out=f_out, stat_out=stat_out)

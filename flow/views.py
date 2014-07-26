#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import time,os
from flask import Blueprint, request, render_template, abort, request, redirect
from flask import url_for, redirect

flow = Blueprint('flow', __name__, template_folder='templates')

import sqlite3
from db import flowOut

import cls


UPLOAD_FOLDER = 'upload'
DAY='20140725'
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
        flows = flowOut()
        return render_template("index.html", ff = flows)

#@flow.route('/up', methods=['POST'])
@flow.route('/up')
def up():
    #return "%s" %(''.join(dict(request.args)['day']))
    #request.args可以获取get的参数并以ImmutableMultiDict类型(相当于字典)保存
    req = request.args
    DAY = time.strftime("%Y-%m-%d",time.strptime(req['fname'][-12:-4], "%Y%m%d"))
    action = cls.fuck()
    every_flow = action.dofile(req['fname'])
    result = action.dataToDb(every_flow, DAY)

    return "%s %s %s %s" %(req['day'], req['fname'], DAY, str(result))
    #day=1
    #fname=2
    #return "hello %s, %s" %(day,fname)

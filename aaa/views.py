#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, abort, request
#from flask import redirect, url_for


aaa = Blueprint('aaa', __name__, template_folder='templates')

@aaa.route('/',methods=['GET','POST'])
@aaa.route('/index',methods=['GET','POST'])
def index():
    from db import getdata,putdata
    if request.method == "POST":
        postday = request.form.get('postday')
        text = request.form.get('text').strip()
        try:
            putdata(text.encode('UTF-8'))
        except IndexError:
            #return "数据输入格式错误"
            pass
        f = getdata(postday)
        aaa = { 'total':str(f[0]).decode('UTF-8'), 
            'totalPer':str(f[1]).decode('UTF-8'), 
            'totalStats':str(f[2]).decode('UTF-8'), 
            'totalRatio':str(f[3]).decode('UTF-8'), 
            'wo':str(f[4]).decode('UTF-8'), 
            'woPer':str(f[5]).decode('UTF-8'),
            'woStats':str(f[6]).decode('UTF-8'),
            'woRatio':str(f[7]).decode('UTF-8')
        }
#        title = request.form.get('title')
        return render_template(
                "aaa.html", 
                day = postday, 
                aaa = aaa, 
                text = text.split('\n') ,
#                title = title
                )

    else :
        return render_template('aaa_in.html')

@aaa.route('/<day>')
def ooo(day):
    from db import getdata
    f=getdata(day)
    aaa = { 'total':str(f[0]).decode('UTF-8'), 
            'totalPer':str(f[1]).decode('UTF-8'), 
            'totalStats':str(f[2]).decode('UTF-8'), 
            'totalRatio':str(f[3]).decode('UTF-8'), 
            'wo':str(f[4]).decode('UTF-8'), 
            'woPer':str(f[5]).decode('UTF-8'),
            'woStats':str(f[6]).decode('UTF-8'),
            'woRatio':str(f[7]).decode('UTF-8')
          }
    return render_template("aaa.html", day = day, aaa = aaa)

if __name__ == '__main__':
    aaa.run(debug=True)

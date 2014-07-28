from flask import Flask, render_template
from flask import redirect, url_for, abort
from jinja2 import TemplateNotFound

from aaa.views import aaa
from flow.views import flow

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
def index():
    return render_template("base.html")

@app.route('/<url>')
def show():
    #try:
        return redirect(url_for('url'))
    #except :
    #    abort(410)

app.register_blueprint(aaa)
app.register_blueprint(flow)


# Blueprint can be registered many times
app.register_blueprint(aaa, url_prefix='/aaa')
app.register_blueprint(flow, url_prefix='/flow')

if __name__ == "__main__":
        app.run(host='0.0.0.0',debug = True)
       # app.run()

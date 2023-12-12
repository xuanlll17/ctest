from flask import Flask, redirect, render_template,url_for
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dash_file.dash_app import dash  #package裡的module import
from dash_file.dash_app1 import dash1
from dash_file.dash_app2 import dash2
from dash_file.dash_app3 import dash3
from dash_file.dash_app4 import dash4

#只有.py可以及時更新
app = Flask(__name__)
application = DispatcherMiddleware(
    app,
    {"/dash/app": dash.server,
     "/dash/app1": dash1.server,
     "/dash/app2": dash2.server,
     "/dash/app3": dash3.server,
     "/dash/app4": dash4.server},  #一定要有.server
)

@app.route("/")
def index():
    return redirect('/dash/app')

if __name__ == "__main__":
    run_simple("localhost", 8080, application,use_debugger=True,use_reloader=True)
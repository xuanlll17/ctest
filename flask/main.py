from flask import Flask, redirect, render_template,url_for
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dash_file.dash_app import dash  #package裡的module import

#只有.py可以及時更新
app = Flask(__name__)
application = DispatcherMiddleware(
    app,
    {"/dash/app": dash.server},  #一定要有.server
)

@app.route("/")
def index():
    return redirect("/dash/app")

if __name__ == "__main__":
    run_simple("localhost", 8080, application,use_debugger=True,use_reloader=True)
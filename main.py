from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_moment import Moment
from datetime import datetime
import sqlalchemy as db
from sqlalchemy import func
import math
from view.purchase import branch_app


app = Flask(__name__)
moment = Moment(app)
app.register_blueprint(branch_app)


@app.route('/')
def index():
    return render_template('index.html',
                           page_header="index",
                           current_time=datetime.utcnow())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

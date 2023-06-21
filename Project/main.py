from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_moment import Moment
from datetime import datetime
from view.order_app import order_menu
from view.purchase import branch_app
from view.member import member_app
from view.menu import menu_app
from view.ingredient import ingredient_app
from view.showorder import showorder_app
from view.revenue import revenue_app

app = Flask(__name__)
app.secret_key="coffee.db"
moment = Moment(app)
app.register_blueprint(order_menu)
app.register_blueprint(branch_app)
app.register_blueprint(member_app)
app.register_blueprint(menu_app)
app.register_blueprint(ingredient_app)
app.register_blueprint(showorder_app)
app.register_blueprint(revenue_app)


@app.route('/admin')
def index():
    return render_template('index.html',
                           page_header="index",
                           current_time=datetime.utcnow())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5003)

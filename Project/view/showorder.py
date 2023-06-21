from flask import Blueprint, render_template, request, session
import sqlite3

# 创建 showorder_app 蓝图
showorder_app = Blueprint('showorder', __name__)


@showorder_app.route('/showorder')
def orders():
    conn = sqlite3.connect('./db/coffee.db')
    c = conn.cursor()
    username = session['username']
    c.execute('SELECT Branch FROM Employee WHERE Employee.E_ID = ?', (username,))
    branch = c.fetchone()
    branch = branch[0]
    c.execute('SELECT * FROM Purchase, Member WHERE Member.Email = Purchase.Buyer and Purchase.Branch = ?  order by Purchase_time desc', (branch,))
    rows = c.fetchall()
    conn.close()
    return render_template('showorder.html', rows=rows)


@showorder_app.route('/get_detail', methods=['POST'])
def get_value():
    value = request.form['value']
    conn = sqlite3.connect('./db/coffee.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Purchase WHERE O_ID = ?', (value,))
    order_data = cursor.fetchone()

    cursor.execute(
        'SELECT Order_description.Item_ID, Name, Quantity, Quantity*Price FROM Order_description, Menu WHERE O_ID = ? AND Order_description.Item_ID = Menu.Item_ID Order by Order_description.Item_ID',
        (value,))
    purchase_data = cursor.fetchall()
    total_price = 0
    for i in purchase_data:
        total_price += i[3]

    member_mail = order_data[2]
    sql = "SELECT * FROM Member WHERE Email = ?"
    cursor.execute(sql, (member_mail,))
    member_data = cursor.fetchone()
    conn.close()
    return render_template('showorder_detail.html', order_data=order_data, purchase_data=purchase_data,
                           total_price=total_price, member_data=member_data)

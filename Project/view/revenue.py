from flask import Blueprint, render_template, request, session
import sqlite3

# 创建 showorder_bp 蓝图
revenue_app = Blueprint('revenue', __name__)


@revenue_app.route('/revenue')
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
    return render_template('revenue.html', rows=rows)


@revenue_app.route('/revenue_month', methods=['POST'])
def get_value():
    value = request.form['month']
    conn = sqlite3.connect('./db/coffee.db')
    cursor = conn.cursor()
    username = session['username']
    cursor.execute('SELECT Branch FROM Employee WHERE Employee.E_ID = ?', (username,))
    branch = cursor.fetchone()
    branch = branch[0]

    cursor.execute('SELECT Purchase.O_ID, Purchase.Purchase_time, Purchase.Branch FROM Purchase, Member WHERE Member.Email = Purchase.Buyer AND Purchase.Purchase_time LIKE ? AND Purchase.Branch = ? ORDER BY Purchase.Purchase_time DESC', (f'%-0{value}-%', branch))
    purchase_data = cursor.fetchall()

    data_list = []
    for purchase in purchase_data:
        total_price = calculate_total_price(cursor, purchase[0])
        data_list.append((purchase[0], purchase[1], purchase[2], total_price))

    conn.close()

    month_revenue = 0
    for i in data_list:
        month_revenue += i[3]

    return render_template('revenue_month.html', rows=data_list, month_revenue=month_revenue)

def calculate_total_price(cursor, o_id):
    cursor.execute(
        'SELECT Order_description.Item_ID, Quantity, Price FROM Order_description, Menu WHERE O_ID = ? AND Order_description.Item_ID = Menu.Item_ID ORDER BY Order_description.Item_ID',
        (o_id,))
    purchase_data = cursor.fetchall()
    total_price = 0
    for item in purchase_data:
        total_price += item[1] * item[2]
    return total_price


@revenue_app.route('/get_month_detail', methods=['POST'])
def get_month_value():
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
    return render_template('month_order_detail.html', order_data=order_data, purchase_data=purchase_data,
                           total_price=total_price, member_data=member_data)

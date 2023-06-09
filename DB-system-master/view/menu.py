from flask import render_template, request, redirect, url_for, Blueprint, jsonify
import sqlite3


menu_app = Blueprint('menu_app', __name__, url_prefix="/menu")

@menu_app.route('/')
def show():
    conn = sqlite3.connect('./db/coffee.db')
    c = conn.cursor()
    c.execute("SELECT Name, Price, Item_ID FROM Menu") #沒把 Item_ID 傳入會發生刪除時完全無法真正刪除DB資料問題， item_id = request.form.get('id')抓不到item_id
    menu = c.fetchall()
    conn.close()
    return render_template('showmenu.html', menu=menu)
    
@menu_app.route('/add_new_item', methods=['GET', 'POST'])
def add_new_item():
    if request.method == 'POST':
        item_name = request.form.get('name')
        item_price = request.form.get('price')
        item_id = request.form.get('id')
        conn = sqlite3.connect('./db/coffee.db')
        c = conn.cursor()
        c.execute("INSERT INTO Menu (Name, Price,Item_ID) VALUES (?, ?, ?)", (item_name, item_price, item_id))
        conn.commit()
        conn.close()

        return redirect('/menu')

    conn = sqlite3.connect('./db/coffee.db')
    c = conn.cursor()
    c.execute("SELECT Name, Price, Item_ID FROM Menu") 
    menu = c.fetchall()
    conn.close()

    return render_template('add_item.html', menu=menu)

@menu_app.route('/update_item', methods=['GET', 'POST'])
def update_item():
    if request.method == 'POST':
        item_name = request.form.get('name')
        item_price = request.form.get('price')
        item_id = request.form.get('id')
        conn = sqlite3.connect('./db/coffee.db')
        c = conn.cursor()

        c.execute("UPDATE Menu SET Name=?, Price=? WHERE Item_ID=?", (item_name, item_price, item_id))
        conn.commit()
        conn.close()

        return redirect('/menu')

    item_id = request.args.get('id')
    conn = sqlite3.connect('./db/coffee.db')
    c = conn.cursor()
    c.execute("SELECT Name, Price, Item_ID FROM Menu WHERE Item_ID=?", (item_id,))
    item = c.fetchone()
    conn.close()

    return render_template('update_item.html', item=item)


@menu_app.route('/delete_item', methods=['POST'])
def delete_item():
    item_id = request.form.get('id')
    print("Delete Item ID:", item_id) 
    conn = sqlite3.connect('./db/coffee.db')
    c = conn.cursor()
    c.execute("DELETE FROM Menu WHERE Item_ID=?", (item_id,))
    conn.commit()
    conn.close()
    print("Database connection closed.")

    conn = sqlite3.connect('./db/coffee.db')
    c = conn.cursor()
    c.execute("SELECT Name, Price, Item_ID FROM Menu") 
    conn.close()

    return redirect('/menu')
from flask import Blueprint, request, render_template, session, redirect, url_for, flash
import sqlite3
from  collections import defaultdict
import json

order_menu = Blueprint('order_menu', __name__)

def get_order_menu():

    c = sqlite3.connect('db/coffee.db').cursor()
    c.execute("""
                SELECT Menu.Item_ID, Menu.Name as Item_name, Menu.Price, Material.Name as Ma_name, Material.Remain_num
                FROM Menu
                LEFT JOIN Recipe ON Menu.Item_ID = Recipe.Item_ID
                LEFT JOIN Material ON Recipe.Ma_ID = Material.Ma_ID
                order by Menu.Item_ID
            """)

    rows = c.fetchall()

    c.execute("""
                SELECT Name
                FROM Branch
            """)
    branch = c.fetchall()
    c.close()

    order_menu_list = {
        'coffee': [],
        'drinks': [],
        'cakes': []
    }

    combine = -1
    for i in rows:
        id, name, price, *ingredients, num = i

        if combine >= 0 and i[0] < 300:
            if rows[combine][0] == i[0]:
                if i[0] < 200:
                    order_menu_list["coffee"][-1]["ingredients"][ingredients[0]] = num
                else:
                    order_menu_list["drinks"][-1]["ingredients"][ingredients[0]] = num
                
                combine += 1
                continue

        product = {
            "id": id,
            "name": name,
            "price": price
        }

        if ingredients[0]:  # 如果有成份資料
            product["ingredients"] = {ingredients[0] : num}

        if i[0] < 200:  # 咖啡類
            order_menu_list["coffee"].append(product)
        elif i[0] < 300:  # 飲料類
            order_menu_list["drinks"].append(product)
        else:  # 食物類
            order_menu_list["cakes"].append(product)

        combine += 1
    
    return branch, order_menu_list


res = {}
@order_menu.route('/home')
def home():
    session['branch'] = '選擇取餐地點'
    res.clear()
    return redirect(url_for('order_menu.od_mu'))


@order_menu.route('/')
def od_mu():
    username = session.get('username')

    if session.get('branch') == None:
        session['branch'] = '選擇取餐地點'

    if request.method == 'GET':
        branch, order_menu_list = get_order_menu()

    tmp = request.args.getlist('detil')
    detil = []
    if tmp:
        num = int(tmp[0][1:])-1
        if tmp[0][0] == '1':
            detil.append(order_menu_list['coffee'][num]['name'])
            detil.append(int(tmp[1]))
            detil.append(int(tmp[1])*order_menu_list['coffee'][num]['price'])
        elif tmp[0][0] == '2':
            detil.append(order_menu_list['drinks'][num]['name'])
            detil.append(int(tmp[1]))
            detil.append(int(tmp[1])*order_menu_list['drinks'][num]['price'])
        else:
            detil.append(order_menu_list['cakes'][num]['name'])
            detil.append(int(tmp[1]))
            detil.append(int(tmp[1])*order_menu_list['cakes'][num]['price'])
        res[tmp[0]] = detil
    print(res)
    return render_template("ordermenu.html", branch=branch, order_menu_list=order_menu_list, username=username, res=res)


@order_menu.route('/order_check', methods=['POST'])
def order_check():
    detil = request.form.get('detil').split(',')
    session['branch'] = detil[0]
    detil = detil[1:]
    # print('detil= ', detil)
    return redirect(url_for('order_menu.od_mu', detil=detil)) # todo: return check result


@order_menu.route('/submit_order', methods=['POST'])
def submit_order():
    print(request.form)

    if 'disorder' in request.form:
        print('disorder')
        del res[request.form.get('disorder')]

    elif 'ordersubmit' in request.form:
        if request.form.get('ordersubmit') == '選擇取餐地點':
            flash('請選擇取餐地點')
            return redirect(url_for('order_menu.od_mu'))
        
        session['branch'] = request.form.get('ordersubmit')
        return "yes, order"
    
    else:
        for i in request.form.keys():
            item_id = i
            print('item_id= ', item_id)
            if (num := request.form.get(item_id)) == '':
                flash('請輸入數量')
                return redirect(url_for('order_menu.od_mu'))
            print('1.num= ', num)
            num = int(num)
        print('2.num= ', num)
        if num != 0:
            print(res[item_id][1], res[item_id][2])
            res[item_id][2] = (res[item_id][2]/res[item_id][1]) * num
            res[item_id][1] = num
        else:
            del res[item_id]

    return redirect(url_for('order_menu.od_mu'))

@order_menu.route('/logout')
def logout():
    del session['username']
    return redirect(url_for('order_menu.home'))
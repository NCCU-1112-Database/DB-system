from flask import Blueprint, request, render_template, session, redirect, url_for, flash
import sqlite3
from  collections import defaultdict
import json
from datetime import datetime

order_menu = Blueprint('order_menu', __name__)

res = {}

@order_menu.route('/')
def home():
    session['branch'] = '選擇取餐地點'
    res.clear()

    return redirect(url_for('order_menu.od_mu'))


@order_menu.route('/homepage')
def od_mu():
    username = session.get('username')

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
    # print(res)

    total = 0
    for i in res:
        total += res[i][2]

    return render_template("ordermenu.html", 
                           branch=branch, order_menu_list=order_menu_list, 
                           username=username, res=res, total=total)


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
        del res[request.form.get('disorder')]

    elif 'ordersubmit' in request.form:
        state = request.form.get('ordersubmit').split(',')
        session['branch'] = state[0]

        if state[1] == 'None':
            flash('請先登入會員')
            return redirect(url_for('order_menu.od_mu'))
        elif state[0] == '選擇取餐地點':
            flash('請選擇取餐地點')
            return redirect(url_for('order_menu.od_mu'))
        
        conn = sqlite3.connect('db/coffee.db')
        c = conn.cursor()
        c.execute('SELECT Max(O_ID) FROM Purchase')
        new_O_ID = str(int(c.fetchone()[0]) + 1)
        print('O_ID= ', new_O_ID)
        purchase_time = datetime.now().strftime("%Y-%m-%d")
        print('purchase_time= ', purchase_time)
        
        c.execute("""
                  INSERT INTO Purchase (O_ID, Purchase_time, Buyer, Branch)
                  VALUES (?, ?, ?, ?)
                  """, (new_O_ID, purchase_time, state[1], state[0]))

        for id in res:
            print('id= ', id)
            print('res[id]= ', res[id])
            c.execute("""
                      INSERT INTO Order_description (O_ID, Item_ID, Quantity)
                      VALUES (?, ?, ?)
                      """, (new_O_ID, id, res[id][1]))
        conn.commit()
        c.close()

        total = 0
        for i in res:
            total += res[i][2]
    
        return render_template('thankorder.html', new_O_ID="new_O_ID", 
                               res=res, branch=state[0], username=state[1], total=total)
    
    else:
        for i in request.form.keys():
            item_id = i
            # print('item_id= ', item_id)
            if (num := request.form.get(item_id)) == '':
                flash('請輸入數量')
                return redirect(url_for('order_menu.od_mu'))
            # print('1.num= ', num)
            num = int(num)
        # print('2.num= ', num)
        if num != 0:
            # print(res[item_id][1], res[item_id][2])
            res[item_id][2] = (res[item_id][2]/res[item_id][1]) * num
            res[item_id][1] = num
        else:
            del res[item_id]

    return redirect(url_for('order_menu.od_mu'))

@order_menu.route('/logout')
def logout():
    del session['username']
    res.clear()
    return redirect(url_for('order_menu.home'))

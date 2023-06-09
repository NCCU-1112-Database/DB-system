

@app.route('/admin_main_page')
def orders():
    conn = sqlite3.connect('../coffee.db')
    c = conn.cursor()
    username = session['username']
    print(username)
    c.execute('SELECT Branch FROM Employee WHERE Employee.E_ID = ?', (username,))
    branch = c.fetchone()
    print(branch)
    print(type(branch))
    branch = branch[0]
    c.execute('SELECT * FROM Purchase, Member WHERE Member.Email = Purchase.Buyer and Purchase.Branch = ?  order by Purchase_time desc', (branch,))
    rows = c.fetchall()
    conn.close()
    return render_template('showorder.html', rows=rows)
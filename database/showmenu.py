from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__, template_folder='templates')


@app.route('/')
def menu():
    conn = sqlite3.connect('coffee.db')
    c = conn.cursor()
    c.execute("SELECT Name,Price FROM Menu")
    menu = c.fetchall()
    conn.close()
    return render_template('showmenu.html', menu=menu)



if __name__ == '__main__':
    app.run(debug=True)

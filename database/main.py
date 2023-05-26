from flask import Flask, session, render_template, request, flash, redirect
from models import check_user, add_user
import sqlite3

#build a web
app=Flask(__name__)
app.secret_key="coffee.db"

#main page
@app.route("/")
def index():
    username=session.get('username')
    if username!=None:
        print(username,' has logined.')
    return render_template("index.html")

#login page
@app.route("/login")
def login():
    return render_template("login.html")

#login_submit function
@app.route("/login_submit", methods=['GET', 'POST'])
def login_submit():
    session.pop('username', None)
    if request.method=='POST':
        acc=request.form.get('username')
        passwd=request.form.get('password')
    state=check_user.check_user(acc,passwd)
    print('username : ',acc,' logins with password : ',passwd,' and with state : ',state,'.')
    #four state
    if state==check_user.login_state.NOT_EXIST.value:
        flash("This account does not exist.")
    elif state==check_user.login_state.EXIST_BUT_WRONG.value:
        flash("Wrong password")
    elif state==check_user.login_state.EXIST_AND_IS_MEMBER.value:
        session['username']=acc
        session['type']=state
        #please redirect to the menu page.
        return redirect("/")
    else:
        #please redirect to the admin page
        session['username']=acc
        session['type']=state
        return redirect("/")
    return redirect("/login")

#register page
@app.route("/register")
def register():
    return render_template("register.html")

#register function
@app.route("/register_submit", methods=['GET', 'POST'])
def register_submit():
    if request.method=='POST':
        acc=request.form.get('username')
        name=request.form.get('name')
        Tel=request.form.get('Tel')
        passwd=request.form.get('password')
        conf=request.form.get('confirm')
    state=check_user.check_user(acc,passwd)
    #four state
    if state!=check_user.login_state.NOT_EXIST.value:
        flash("This account already exist.")
        return render_template("register.html")
    else:
        if passwd!=conf:
            flash("Password and confirm password do not match.")
            return render_template("register.html")
        else:
            print('username : ',acc,' has registered with password : ',passwd,'.')
            add_user.add_user(acc,name,Tel,passwd)
            flash("Account successfully created!")
            return render_template("login.html")

#logout function
@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect('/')
if __name__=="__main__":
    app.run(debug=True)

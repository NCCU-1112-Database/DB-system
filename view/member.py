from flask import Flask, session, render_template, request, flash, redirect
from models import check_user, add_user
from flask import render_template, request, redirect, url_for, Blueprint, jsonify
import sqlite3



member_app = Blueprint('member_app', __name__)

#main page
# @member_app.route("/")
# def index():
#     username=session.get('username')
#     if username!=None:
#         print(username,' has logined.')
#     return render_template("member_login_index.html")

#login page
@member_app.route("/login")
def login():
    return render_template("member_login.html")

#login_submit function
@member_app.route("/login_submit", methods=['GET', 'POST'])
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
        return redirect(url_for('branch_app.index'))
    return redirect("/login")

#register page
@member_app.route("/register")
def register():
    return render_template("member_register.html")

#register function
@member_app.route("/register_submit", methods=['GET', 'POST'])
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
        return render_template("member_register.html")
    else:
        if passwd!=conf:
            flash("Password and confirm password do not match.")
            return render_template("member_register.html")
        else:
            print('username : ',acc,' has registered with password : ',passwd,'.')
            add_user.add_user(acc,name,Tel,passwd)
            flash("Account successfully created!")
            return render_template("member_login.html")

#logout function
# @member_app.route('/logout')
# def logout():
#     del session['username']
#     del session['branch']
#     res = {}
#     return redirect(url_for('order_menu.od_mu'), res=res)


# if __name__=="__main__":
#     app.run(debug=True)

from flask import Flask, session, render_template, request, flash, redirect
from models import check_user, add_user
from flask import render_template, request, redirect, url_for, Blueprint, jsonify
import sqlite3



ingredient_app = Blueprint('ingredient_app', __name__, url_prefix="/ingredient")

@ingredient_app.route('/')
def menu():
    conn = sqlite3.connect('./db/coffee.db')
    c = conn.cursor()
    c.execute("SELECT Material.Name,Cost,Cost_per_unit,Remain_num,Producer.Name FROM Material, Producer WHERE P_ID=Producer")
    MaRemain = c.fetchall()
    conn.close()
    return render_template('showma.html', MaRemain=MaRemain)
from flask import render_template, request, redirect, url_for, Blueprint, jsonify
import sqlalchemy as db
from sqlalchemy import func, cast, Integer
from datetime import datetime
import math
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy import event
import traceback
import sys
from sqlalchemy.orm import sessionmaker

branch_app = Blueprint('branch_app', __name__, url_prefix="/purchase")

path_to_db = "./db/coffee.db"
engine = db.create_engine(f'sqlite:///{path_to_db}')
metadata = db.MetaData()
table_purchase = db.Table('Purchase', metadata, autoload_with=engine)
table_order = db.Table('Order_description', metadata, autoload_with=engine)
table_menu = db.Table('Menu', metadata, autoload_with=engine)


@branch_app.route('/')
def index():
    return render_template('branch_index.html', page_header="purchase functions", current_Purchase_Time=datetime.utcnow())


@branch_app.route('/<string:Branch>')
def branch_order_show(Branch):
    Session = sessionmaker(bind=engine)
    session = Session()
    connection = engine.connect()
    try:
        # 执行查询
        query = session.query(
            table_purchase.c.O_ID,
            table_purchase.c.Purchase_time,
            table_purchase.c.Buyer,
            table_purchase.c.Branch,
            cast(func.sum(table_menu.c.Price), Integer).label('TotalAmount')
        ).select_from(
            table_purchase.join(table_order).join(table_menu)
        ).filter(
            table_purchase.c.Branch == Branch
        ).group_by(
            table_purchase.c.O_ID,
            table_purchase.c.Purchase_time,
            table_purchase.c.Buyer,
            table_purchase.c.Branch
        )

        # 获取查询结果
        results = query.all()

        # 处理查询结果
        response_data = []
        for row in results:
            order_info = {
                'O_ID': row.O_ID,
                'Purchase_Time': row.Purchase_time,
                'Buyer': row.Buyer,
                'Branch': row.Branch,
                'TotalAmount': row.TotalAmount
            }
            response_data.append(order_info)

        total_amount = sum(item.TotalAmount for item in results)

        return render_template('branch_purchase.html',
                               page_header="Branch purchase info",
                               outputs=response_data,
                               total_amount=total_amount
                               )
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({'error': str(e)})
    finally:
        session.close()
        connection.close()

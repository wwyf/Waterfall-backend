from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,Flask, request, jsonify
)
from werkzeug.exceptions import abort

from src.db.model import db, Orders

bp = Blueprint('order', __name__, url_prefix='/apis')


@bp.route('/order/mainOrder', methods=('GET', 'POST'))
def solve_mainOrder():
    if request.method == 'POST':
        order_name = request.form['order_name']
        order_ddl = request.form['order_ddl']
        address = request.form['address']
        quantity = int(request.form['quantity'])
        price = int(request.form['price'])
        # order_summary = request.form['order_summary']
        phone = request.form['phone']
        comments = request.form['comments']
        this_order = Orders(order_name, '2010-01-01', order_ddl, address, quantity, price, 1, comments, phone)
        db.session.add(this_order)
        db.session.commit()
        data_res = {
            'msg' : '提交成功',
            'id' : 0
        }
        res = {
            'code' : 0,
            'data' : data_res
        }
        return jsonify(res)
    elif request.method == 'GET':
        res_query_results = Orders.query.all()
        res_orders = []
        for i in res_query_results:
            res_orders.append(i.to_json())
        data_res = {
            "orders" : res_orders
        }
        res = {
            'code' : 0,
            'data' : data_res
        }
        return jsonify(res)

#order_name=order_name&order_ddl=order_ddl&address=address&quantity=1&price=2&comments=comments&phone=phone
# curl http://localhost:5000/apis/order/mainOrder -X post -d "order_name=order_name&order_ddl=2010-02-01&address=address&quantity=1&price=2&comments=comments&phone=phone"
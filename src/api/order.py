from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,Flask, request, jsonify
)
from flask_cors import CORS
from werkzeug.exceptions import abort
import json
import sys


from src.db.model import db, Orders

bp = Blueprint('order', __name__, url_prefix='/apis')
CORS(bp)

@bp.route('/order/mainOrder', methods=('GET', 'POST'))
def solve_mainOrder():
    if request.method == 'POST':
        body_data = json.loads(request.data)
        order_name = body_data['order_name']
        order_ddl = body_data['order_ddl']
        address = body_data['address']
        quantity = int(body_data['quantity'])
        price = int(body_data['price'])
        phone = body_data['phone']
        comments = body_data['comments']
        this_order = Orders(order_name, '2010-01-01', order_ddl, address, quantity, price, 1, comments, phone)
        db.session.add(this_order)
        db.session.commit()
        data_res = {
            'msg' : '提交成功',
            'id' : this_order.ID
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
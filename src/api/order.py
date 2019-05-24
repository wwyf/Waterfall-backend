from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,Flask, request, jsonify
)
from flask_cors import CORS
from werkzeug.exceptions import abort
import json
import sys


from src.db.model import db, Orders
from src.solver import order_solver

bp = Blueprint('order', __name__, url_prefix='/apis')
CORS(bp)

@bp.route('/order/mainOrder', methods=('GET', 'POST'))
def solve_mainOrder():
    if request.method == 'GET':
        skip = request.args.get('skip')
        limit = request.args.get('limit')
        res = order_solver.get_main_orders(skip, limit)
        return jsonify(res)
    elif request.method == 'POST':
        json_body = json.loads(request.data)
        res = order_solver.add_new_main_order(json_body)
        return jsonify(res)

@bp.route('/order/mainOrder/<int:mainOrderId>', methods=('GET', 'POST'))
def solve_mainOrder_with_id(mainOrderId):
    if request.method == 'GET':
        res = order_solver.get_main_order_with_id(mainOrderId)
        return jsonify(res)
    
    elif request.method == 'POST':
        json_body = json.loads(request.data)
        res = order_solver.post_main_order_with_id(mainOrderId, json_body)
        return jsonify(res)

@bp.route('/order/mainOrder/<int:mainOrderId>/finish', methods=('GET', 'POST'))
def solve_finish_mainOrder_with_id(mainOrderId):
    if request.method == 'POST':
        res = order_solver.post_finish_mainOrder_with_id(mainOrderId)
        return jsonify(res)

@bp.route('/order/mainOrder/<int:mainOrderId>/cancel', methods=('GET', 'POST'))
def solve_cancel_mainOrder_with_id(mainOrderId):
    if request.method == 'POST':
        res = order_solver.post_cancel_mainOrder_with_id(mainOrderId)
        return jsonify(res)

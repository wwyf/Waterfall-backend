from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,Flask, request, jsonify
)
from flask_cors import CORS
from werkzeug.exceptions import abort
import json
import sys

from src.db.model import db, Orders
from src.api import (
    mainorder_api,
    suborder_api
)

order_bp = Blueprint('order', __name__, url_prefix='/apis/order')
CORS(order_bp)

@order_bp.route('/mainOrder', methods=('GET', 'POST'))
def solve_mainOrder():
    if request.method == 'GET':
        skip = request.args.get('skip')
        limit = request.args.get('limit')
        res = mainorder_api.get_main_orders(skip, limit)
        return jsonify(res)
    elif request.method == 'POST':
        json_body = json.loads(request.data)
        res = mainorder_api.add_new_main_order(json_body)
        return jsonify(res)

@order_bp.route('/mainOrder/<int:mainOrderId>', methods=('GET', 'POST'))
def solve_mainOrder_with_id(mainOrderId):
    if request.method == 'GET':
        res = mainorder_api.get_main_order_with_id(mainOrderId)
        return jsonify(res)
    
    elif request.method == 'POST':
        json_body = json.loads(request.data)
        res = mainorder_api.post_main_order_with_id(mainOrderId, json_body)
        return jsonify(res)

@order_bp.route('/mainOrder/<int:mainOrderId>/finish', methods=('GET', 'POST'))
def solve_finish_mainOrder_with_id(mainOrderId):
    if request.method == 'POST':
        res = mainorder_api.post_finish_mainOrder_with_id(mainOrderId)
        return jsonify(res)

@order_bp.route('/mainOrder/<int:mainOrderId>/cancel', methods=('GET', 'POST'))
def solve_cancel_mainOrder_with_id(mainOrderId):
    if request.method == 'POST':
        res = mainorder_api.post_cancel_mainOrder_with_id(mainOrderId)
        return jsonify(res)

@order_bp.route('/subOrder', methods=('GET', 'POST'))
def solve_subOrder():
    if request.method == 'GET':
        skip = request.args.get('skip')
        limit = request.args.get('limit')
        res = suborder_api.get_sub_orders(skip, limit)
        return jsonify(res)
    elif request.method == 'POST':
        json_body = json.loads(request.data)
        res = suborder_api.add_new_sub_order(json_body)
        return jsonify(res)

@order_bp.route('/subOrder/<int:subOrderId>', methods=('GET', 'POST'))
def solve_subOrder_with_id(subOrderId):
    if request.method == 'GET':
        res = suborder_api.get_sub_order_with_id(subOrderId)
        return jsonify(res)
    
    elif request.method == 'POST':
        json_body = json.loads(request.data)
        res = suborder_api.post_sub_order_with_id(subOrderId, json_body)
        return jsonify(res)

@order_bp.route('/subOrder/<int:subOrderId>/finish', methods=('GET', 'POST'))
def solve_finish_subOrder_with_id(subOrderId):
    if request.method == 'POST':
        res = suborder_api.post_finish_subOrder_with_id(subOrderId)
        return jsonify(res)

@order_bp.route('/subOrder/<int:subOrderId>/cancel', methods=('GET', 'POST'))
def solve_cancel_subOrder_with_id(subOrderId):
    if request.method == 'POST':
        res = suborder_api.post_cancel_subOrder_with_id(subOrderId)
        return jsonify(res)
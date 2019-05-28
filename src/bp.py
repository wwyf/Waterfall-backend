from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,Flask, request, jsonify, session
)
from flask_cors import CORS
from werkzeug.exceptions import abort
import json
import sys

from src.db.model import db, Orders
from src.api import (
    mainorder_api,
    suborder_api,
    user_api,
    wallet_api
)

user_bp = Blueprint('user', __name__, url_prefix='/apis/user')
CORS(user_bp)

order_bp = Blueprint('order', __name__, url_prefix='/apis/order')
CORS(order_bp)

wallet_bp = Blueprint('wallet', __name__, url_prefix='/apis/wallet')
CORS(wallet_bp)

@order_bp.route('/mainOrder', methods=('GET', 'POST'))
@user_api.permission_check(roles=['manager', 'customer', 'provider'])
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

@order_bp.route('/mainOrder/<int:mainOrderId>/subOrders', methods=['GET'])
def solve_subOrder_with_mainOrder(mainOrderId):
    if request.method == 'GET':
        res = suborder_api.get_sub_order_by_main_order(mainOrderId)
        return jsonify(res)

@user_bp.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        res = user_api.login_status()
        return jsonify(res)
    elif request.method == 'POST':
        json_body = json.loads(request.data.decode('utf-8'))
        res = user_api.login_check(json_body)
        return jsonify(res)

@user_bp.route('/register', methods=['POST'])
def user_register():
    if request.method == 'POST':
        json_body = json.loads(request.data.decode('utf-8'))
        res = user_api.do_register(json_body)
        return jsonify(res)

@user_bp.route('/logout', methods=['GET'])
def user_logout():
    if request.method == 'GET':
        res = user_api.do_logout()
        return jsonify(res)

@user_bp.route('/<int:userId>', methods=['GET', 'POST'])
@user_api.permission_check(roles=['provider', 'purchaser', 'manager'])
def user_info(userId):
    if request.method == 'GET':
        res = user_api.get_user_info(userId)
        return jsonify(res)
    if request.method == 'POST':
        json_body = json.loads(request.data.decode('utf-8'))
        res = user_api.edit_user_info(userId ,json_body)
        return jsonify(res)


@user_bp.route('/checkuser/<string:username>', methods=['GET'])
def user_check_username(username):
    if request.method == 'GET':
        res = user_api.check_username(username)
        return jsonify(res)

@wallet_bp.route('/<int:userId>', methods=['GET'])
def wallet_balance_interface(userId):
    if request.method == 'GET':
        res = wallet_api.get_wallet_balance(userId)
        return jsonify(res)

@wallet_bp.route('/<int:userId>/deposit', methods=['POST'])
@user_api.permission_check(roles=['manager'])
def wallet_deposit_interface(userId):
    if request.method == "POST":
        json_body = json.loads(request.data.decode('utf-8'))
        res = wallet_api.deposit_wallet_balance(userId, json_body['amount'])
        return jsonify(res)

@wallet_bp.route('/<int:userId>/withdraw', methods=['POST'])
def wallet_withdraw_interface(userId):
    if request.method == "POST":
        json_body = json.loads(request.data.decode('utf-8'))
        res = wallet_api.withdraw_wallet_balance(userId, json_body['amount'])
        return jsonify(res)

from flask import Flask, render_template, session, request, redirect, jsonify
from src.db.model import db, Users
from functools import wraps
import json

def get_wallet_balance(userId):
    target_user = Users.query.filter_by(ID=userId).first()
    if target_user is None:
        return {
            "code" : 1,
            "data" : {
                "msg" : "用户不存在"
            }
        }

    return {
        "code" : 0,
        "data" : {
            "balance" : target_user.balance
        }
    }

def deposit_wallet_balance(userId, amount):
    target_user =  Users.query.filter_by(ID=userId).first()
    if target_user is None:
        return {
            "code" : 1,
            "data" : {
                "msg" : "用户不存在"
            }
        }
    
    target_user.balance = target_user.balance + amount

    return {
        "code" : 0,
        "data" : {
            "msg" : "已提交/操作成功"
        }
    }

def withdraw_wallet_balance(userId, amount):
    target_user = Users.query.filter_by(ID=userId).first()
    if target_user is None:
        return {
            "code" : 1,
            "data" : {
                "msg" : "用户不存在"
            }
        }
    
    if target_user.balance < amount:
        return {
            "code" : 1,
            "data" : {
                "msg" : "余额不足"
            }
        }

    target_user.balance = target_user.balance - amount

    return {
        "code" : 0,
        "data" : {
            "msg" : "已提交/操作成功"
        }
    }
from flask import Flask, render_template, session, request, redirect, jsonify
from src.db.model import db, Users
from functools import wraps
import json

def permission_check(roles):
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            if session.get('username'):
                if roles == 'None':
                    return func(*args, **kwargs)
                if session['role'] in roles:
                    return func(*args, **kwargs)
                else:
                    return jsonify({
                        "code" : 1,
                        "data" : {
                            "msg" : "您没有权限使用该接口"
                        }
                    })
            else:
                return jsonify({
                    "code" : 1,
                    "data" : {
                        "msg" : "请先登录"
                    }
                })
        return inner_wrapper
    return wrapper

def login_status():
    if session.get('username'):
        target_user = Users.query.filter_by(username=session['username']).first()
        return { 
            'code' : 0,
            'data' : {
                "msg" : "已经登录",
                "userid" : target_user.ID
            }
        }
    else:
        return { 
            'code' : 1,
            'data' : {
                "msg" : "未登录"
            }
        }

def login_check(json_body):
    username = json_body['username']
    password = json_body['password']
    target_user = Users.query.filter_by(username=username).first()
    if target_user is None:
        return {
            "code" : 1,
            "data" : {
                "msg" : "用户名或密码错误"
            }
        }
    if target_user.password == password:
        session['username'] = username
        session['role'] = target_user.usertype
        return {
            "code" : 0,
            "data" : {
                "msg" : "登录成功",
                "userid" : target_user.ID
            }
        }
    else:
        return {
            "code" : 1,
            "data" : {
                "msg" : "用户名或密码错误"
            }
        }

def add_user(username, password, email, phone, usertype, userstatus):
    if usertype == 'manager':
        if not (session.get('role') and session['role'] == 'manager'):
            return False
    new_user = Users(
        username=username,
        password=password,
        email=email,
        phone=phone,
        usertype=usertype,
        userstatus=userstatus
    )
    
    db.session.add(new_user)
    db.session.commit()
    return True

def do_register(json_body):
    required_field = ['username', 'password', 'email', 'phone', 'role']
    for field in required_field:
        if field not in json_body.keys():
            return {
                "code" : 1,
                "data" : {
                    "msg" : "信息不完整"
                }
            }
        if json_body[field] == "":
            return {
                "code" : 1,
                "data" : {
                    "msg" : "信息不完整"
                }
            }
    find_user = Users.query.filter_by(username=json_body['username']).first()
    if not find_user is None:
        return {
            "code" : 1,
            "data" : {
                "msg" : "用户已存在"
            }
        }
    finished = add_user(
        json_body['username'], 
        json_body['password'], 
        json_body['email'], 
        json_body['phone'], 
        json_body['role'],
        1
    )
    if not finished:
        return {
            "code" : 1,
            "data" : {
                "msg" : "没有权限"
            }
        }
    else:
        find_user = Users.query.filter_by(username=json_body['username']).first()
        session['username'] = find_user.username
        session['role'] = find_user.usertype
        return {
            "code" : 0,
            "data" : {
                "msg" : "注册成功",
                "userid" : find_user.ID
            }
        }

def do_logout():
    session.clear()
    return {
        "code" : 0,
        "data" : {
            "msg" : "登出成功"
        }
    }

def get_user_info(userid):
    target_user = Users.query.filter_by(ID=userid).first()
    if target_user is None:
        return {
            "code" : 1,
            "data" : {
                "msg" : "用户不存在"
            }
        }
    res = target_user.to_json()
    res.pop("password")
    return {
        "code" : 0,
        "data" : res
    }

def edit_user_info(userid, json_body):
    target_user = Users.query.filter_by(ID=userid).first()
    if session['role'] != 'manager' and target_user.username != session["username"]:
        return {
            "code" : 1,
            "data" : {
                "msg" : "没有权限"
            }
        }
    if "password" in json_body:
        target_user.password = json_body["password"]
    if "email" in json_body:
        target_user.email = json_body["email"]
    if "phone" in json_body:
        target_user.phone = json_body["phone"]
    if "role" in json_body and session['role'] == 'manager':
        target_user.usertype = json_body["role"]
    if "status" in json_body and session['role'] == 'manager':
        target_user.userstatus = json_body["status"]
    return {
        "code" : 0,
        "data" : {
            "msg" : "修改成功"
        }
    }


def check_username(username):
    """
    若用户名不存在则返回0，
    如果用户名已存在，返回1
    Paramerers:
        username : string
            用户名
    """
    target_user = Users.query.filter_by(username=username).first()
    if target_user is None:
        return {
            "code" : 0,
            "data" : {
                "msg" : "用户名不存在"
            }
        }
    else:
        return {
            "code" : 1,
            "data" : {
                "msg" : "用户名已存在"
            }
        }
from flask import Flask, render_template, session, request, redirect
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
                    return json.dumps({
                        "ret" : 1,
                        "data" : "您没有权限使用该接口"
                    })
            else:
                return redirect('/login')
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
    if json_body['usertype'] == 'manager':
        if not (session.get('role') and session['role'] == 'manager'):
            return {
                "code" : 1,
                "data" : {
                    "msg" : "没有权限"
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
    add_user(
        json_body['username'], 
        json_body['password'], 
        json_body['email'], 
        json_body['phone'], 
        json_body['usertype'],
        1
    )
    return {
        "code" : 0,
        "data" : {
            "msg" : "注册成功"
        }
    }

import os
import sys
import pytest
import inspect
from faker import Faker

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# add current directory into import path
sys.path.append(current_dir + "/../")
sys.path.append(current_dir + "/../../")

import src
import datetime
from utils import Mocker
from src.db.model import *
from src.api.user_api import *


"""
    @brief Test for permission_check(roles)
"""
param_permission_check = [
    ({}, ['supplier', 'purchaser', 'manager'], {"code": 1, "msg": "请先登录"}),
    ({}, "None", {"code": 1, "msg": "请先登录"}),
    ({"username": "test"}, "None", {}),
    ({"username": "test", "role": "test"}, "None", {}),
    ({"username": "test", "role": "test"}, ['supplier', 'purchaser', 'manager'], {"code": 1, "msg": "您没有权限使用该接口"}),
    ({"username": "test", "role": "supplier"}, ['supplier', 'purchaser', 'manager'], {})
]


@pytest.mark.parametrize('session, roles, res', param_permission_check)
def test_permission_check(session, roles, res, monkeypatch):
    def mock_flask_func(*args, **kwargs):
        return None

    def mock_jsonify(dict):
        return dict

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.user_api.session", session)
        monkeypatch.setattr("src.api.user_api.jsonify", mock_jsonify)
        result = permission_check(roles)(mock_flask_func)()
        assert (isinstance(result, dict)
                and result["code"] == res["code"]
                and result["data"]["msg"] == res["msg"]) \
                or result is None


"""
    @brief Test for login_status()
"""
param_login_status = [
    ({}, None, {"code": 1, "msg": "未登录"}),
    ({"username": "test"}, {"ID": 1}, {"code": 0, "msg": "已经登录"})
]

@pytest.mark.parametrize('session, targets_user, res', param_login_status)
def test_login_status(session, targets_user, res, monkeypatch):
    def mock_users_query_filter_by(username):
        def mock_first():
            if targets_user is not None:
                user = Users(username=username,
                             password="123456",
                             email="spam@spam.com",
                             phone="None",
                             usertype=0,
                             userstatus=0)
                user.ID = targets_user["ID"]
                return user
            else:
                return None
        return Mocker(first=mock_first)

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.user_api.session", session)
        monkeypatch.setattr("src.api.user_api.Users.query", Mocker(filter_by=mock_users_query_filter_by))
        result = login_status()
        assert (isinstance(result, dict)
                and result["code"] == res["code"]
                and result["data"]["msg"] == res["msg"]
                and result["data"]["userid"] == targets_user["ID"] if targets_user is not None else True)


"""
    @brief Test for login_check()
"""
param_login_check = [
    ({"username": "test", "password": "test"}, None, {"code": 1, "msg": "用户名或密码错误"}),
    ({"username": "test", "password": "test"}, {"ID": 1, "password": "test1"}, {"code": 1, "msg": "用户名或密码错误"}),
    ({"username": "test", "password": "test"}, {"ID": 1, "password": "test"}, {"code": 0, "msg": "登录成功"})
]

@pytest.mark.parametrize('json_body, target_user, res', param_login_check)
def test_login_check(json_body, target_user, res, monkeypatch):
    def mock_users_query_filter_by(username):
        def mock_first():
            if target_user is not None:
                user = Users(username=username,
                             password=target_user["password"],
                             email="spam@spam.com",
                             phone="None",
                             usertype=0,
                             userstatus=0)
                user.ID = target_user["ID"]
                return user
            else:
                return None
        return Mocker(first=mock_first)

    with monkeypatch.context() as m:
        session = {}
        monkeypatch.setattr("src.api.user_api.session", session)
        monkeypatch.setattr("src.api.user_api.Users.query", Mocker(filter_by=mock_users_query_filter_by))
        result = login_check(json_body)
        assert (isinstance(result, dict)
                and result["code"] == res["code"]
                and result["data"]["msg"] == res["msg"]
                and result["data"]["userid"] == target_user["ID"]
                and session["username"] == json_body["username"]
                and session["role"] == 0
                if target_user is not None and json_body["password"] == target_user["password"] else True)


"""
    @brief Test for add_user(username, password, email, phone, usertype, userstatus)
"""
param_add_user = [
    ("test", "password", "spam@spam.com", "88888888", "manager", 0, None, False),
    ("test", "password", "spam@spam.com", "88888888", "manager", 0, "supplier", False),
    ("test", "password", "spam@spam.com", "88888888", "manager", 0, "manager", True),
    ("test", "password", "spam@spam.com", "88888888", "supplier", 0, None, False),
    ("test", "password", "spam@spam.com", "88888888", "supplier", 0, "supplier", True),
    ("test", "password", "spam@spam.com", "88888888", "supplier", 0, "manager", True),
]

# @pytest.mark.parametrize('username, password, email, phone, usertype, userstatus, role, res', param_add_user)
# def test_add_user(username, password, email, phone, usertype, userstatus, role, res, monkeypatch):
#     def mock_db_add(user):
#         return

#     def mock_db_commit():
#         return

#     with monkeypatch.context() as m:
#         monkeypatch.setattr("src.api.user_api.session", {"role": role} if role is not None else {})
#         monkeypatch.setattr("src.api.user_api.db.session", Mocker(add=mock_db_add, commit=mock_db_commit))
#         result = add_user(username, password, email, phone, usertype, userstatus)
#         assert result == res


"""
    @brief Test for do_register(json_body)
"""
param_do_register = [
    ({"username": "test", "password": "test", "email": "spam@spam.com", "phone": "88888888", "role": "test"},
        None, False, {"code": 1, "msg": "没有权限"}),
    ({"username": "test", "password": "test", "email": "spam@spam.com", "phone": "88888888", "role": "test"},
        None, True, {"code": 0, "msg": "注册成功"}),
    ({"username": "test", "password": "test", "email": "spam@spam.com", "phone": "88888888", "role": "test"},
        {"ID": 1}, True, {"code": 1, "msg": "用户已存在"})
]


# @pytest.mark.parametrize('json_body, find_user, finished, res', param_do_register)
# def test_do_register(json_body, find_user, finished, res, monkeypatch):
#     def mock_users_query_filter_by(username):
#         def mock_first():
#             if find_user is not None:
#                 user = Users(username=username,
#                              password="test",
#                              email="spam@spam.com",
#                              phone="None",
#                              usertype=0,
#                              userstatus=0)
#                 user.ID = find_user["ID"]
#                 return user
#             else:
#                 return None
#         return Mocker(first=mock_first)

#     with monkeypatch.context() as m:
#         monkeypatch.setattr("src.api.user_api.Users.query", Mocker(filter_by=mock_users_query_filter_by))
#         monkeypatch.setattr("src.api.user_api.add_user", lambda *x : finished)
#         result = do_register(json_body)
#         assert (isinstance(result, dict)
#                 and result["code"] == res["code"]
#                 and result["data"]["msg"] == res["msg"])


"""
    @brief Test for do_logout()
"""

def test_do_logout(monkeypatch):
    session = {"username": "test", "password": "test"}
    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.user_api.session", session)
        result = do_logout()
        assert result == {"code": 0, "data": {"msg": "登出成功"}} and session == {}


"""
    @brief Test for get_user_info(userid)
"""
param_get_user_info = [
    (None, {"code": 1}),
    ({"ID": 1}, {"code": 0})
]

@pytest.mark.parametrize('target_user, res', param_get_user_info)
def test_get_user_info(target_user, res, monkeypatch):
    def mock_users_query_filter_by(ID):
        def mock_first():
            if target_user is not None:
                user = Users(username="test",
                             password="123456",
                             email="spam@spam.com",
                             phone="None",
                             usertype=0,
                             userstatus=0)
                user.ID = ID
                return user
            else:
                return None
        return Mocker(first=mock_first)

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.user_api.Users.query", Mocker(filter_by=mock_users_query_filter_by))
        result = get_user_info(1)
        assert isinstance(result, dict) and result["code"] == res["code"]


"""
    @brief Test for edit_user_info(userid, json_body)
"""
param_edit_user_info = [
    ({"username": "test", "password": "test", "email": "spam@spam.com", "phone": "88888888", "role": "test"},
        {"ID": 1}, {"role":"supplier", "username":"test"}, {"code": 1, "msg": "没有权限"}),
    ({"username": "test", "password": "test", "email": "spam@spam.com", "phone": "88888888", "role": "test"},
        {"ID": 1}, {"role":"manager", "username":"test1"}, {"code": 1, "msg": "没有权限"}),
    ({"username": "test", "password": "test", "email": "spam@spam.com", "phone": "88888888", "role": "test"},
        {"ID": 1}, {"role":"manager", "username":"test"}, {"code": 0, "msg": "修改成功"}),
]

# @pytest.mark.parametrize('json_body, find_user, session, res', param_edit_user_info)
# def test_edit_user_info(json_body, find_user, session, res, monkeypatch):
#     def mock_users_query_filter_by(ID):
#         def mock_first():
#             if find_user is not None:
#                 user = Users(username=json_body["username"],
#                              password="test",
#                              email="spam@spam.com",
#                              phone="None",
#                              usertype=0,
#                              userstatus=0)
#                 user.ID = ID
#                 return user
#             else:
#                 return None
#         return Mocker(first=mock_first)

#     with monkeypatch.context() as m:
#         monkeypatch.setattr("src.api.user_api.Users.query", Mocker(filter_by=mock_users_query_filter_by))
#         monkeypatch.setattr("src.api.user_api.session", session)
#         result = edit_user_info(0, json_body)
#         assert (isinstance(result, dict)
#                 and result["code"] == res["code"]
#                 and result["data"]["msg"] == res["msg"])

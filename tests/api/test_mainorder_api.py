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
from src.api.mainorder_api import *


"""
    @brief Test for get_main_order_supply()
"""
param_get_main_order_supply = [
    (None, 0),
    ([subOrders(mainorder=0,
              createdate=datetime.datetime.utcnow(),
              createuser=0,
              quantity=1,
              comments="None",
              phone="88888888",
              status=0)], 1)
]


@pytest.mark.parametrize('db_suborders, res', param_get_main_order_supply)
def test_get_main_order_supply(db_suborders, res, monkeypatch):
    def mock_suborders_query(p1, p2):
        return db_suborders

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.mainorder_api.subOrders.query", Mocker(filter=mock_suborders_query))
        result = get_main_order_supply(0)
        assert result == res and isinstance(result, int)


"""
    @brief Test for get_main_orders(skip, limit)
"""
param_get_main_orders = [
    (None, None, {"orders_num": 200}, {"orders_num": 200, "code": 0}),
    (None, 1, {"orders_num": 200}, {"orders_num": 1, "code": 0}),
    (1, None, {"orders_num": 200}, {"orders_num": 199, "code": 0}),
    (1, "-1", {"orders_num": 200}, {"orders_num": 199, "code": 0}),
    (1, 20, {"orders_num": 200}, {"orders_num": 20, "code": 0}),
]


@pytest.mark.parametrize('skip, limit, db_orders, res', param_get_main_orders)
def test_get_main_orders(skip, limit, db_orders, res, monkeypatch):
    def mock_orders_query_all():
        orders = []
        fake = Faker()
        for i in range(0, db_orders["orders_num"]):
            o = Orders(name=fake.name(),
                       summary="None",
                       createdate=fake.date_time(),
                       deadline=fake.date_time(),
                       address=fake.city(),
                       quantity=1,
                       price=1.0,
                       totalprice=1.0,
                       createuser=i,
                       comments="None",
                       phone=fake.phone_number(),
                       status=0,
                       progress=0)
            o.ID = i
            orders.append(o)
        return orders

    def mock_get_main_order_supply(id):
        fake = Faker()
        return fake.random_int()

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.mainorder_api.Orders.query", Mocker(all=mock_orders_query_all))
        monkeypatch.setattr("src.api.mainorder_api.get_main_order_supply", mock_get_main_order_supply)
        result = get_main_orders(skip, limit)
        assert isinstance(result, dict) and result["code"] == res["code"] \
            and isinstance(result["data"], dict) and len(result["data"]["orders"]) == res["orders_num"]


"""
    @brief Test for add_new_main_order(json_body)
"""
# TODO: add more tests, including erroneous inputs
param_add_new_main_order = [
    (
        {
            "name": "None",
            "summary": "None",
            "deadline": datetime.datetime.utcnow(),
            "address": "None",
            "quantity": "1",
            "price": "1",
            "comments": "None",
            "phone": "13538383838"
        },
        {
            "role" : "customer",
            "username" : "None"
        },
        {
            "ID" : 1,
        },
        {"code": 0, "msg": "提交成功", "id": 0}
    ),
    (
        {
            "name": "None",
            "summary": "None",
            "deadline": datetime.datetime.utcnow(),
            "address": "None",
            "quantity": "1",
            "price": "1",
            "comments": "None",
        },
        {
            "role" : "customer",
            "username" : "None"
        },
        {
            "ID" : 1,
        },
        {"code": 0, "msg": "提交成功", "id": 0}
    ),
]


@pytest.mark.parametrize('json_body,session, targets_user, res', param_add_new_main_order)
def test_add_new_main_order(json_body,session, targets_user, res, monkeypatch):
    def mock_db_add(order):
        order.ID = 0

    def mock_db_commit():
        return
    def mock_users_query_filter_by(username):
        def mock_first():
            if targets_user is not None:
                user = Users(username=username,
                             password="123456",
                             email="spam@spam.com",
                             phone="13588888888",
                             usertype=0,
                             userstatus=0)
                user.ID = targets_user["ID"]
                return user
            else:
                return None
        return Mocker(first=mock_first)

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.mainorder_api.session", session)
        monkeypatch.setattr("src.api.mainorder_api.Users.query", Mocker(filter_by=mock_users_query_filter_by))
        monkeypatch.setattr("src.api.mainorder_api.db.session",
                            Mocker(add=mock_db_add, commit=mock_db_commit))
        result = add_new_main_order(json_body)
        assert isinstance(result, dict) and result["code"] == res["code"] \
               and isinstance(result["data"], dict) and result["data"]["msg"] == res["msg"] \
                and result["data"]["id"] == res["id"]


"""
    @brief Test for get_main_order_with_id(mainOrderId)
"""
# TODO: add more tests, including erroneous inputs
param_get_main_order_with_id = [
    (None, {"code": 1, "msg": "该订单不存在"}),
    ({"ID": 1}, {"code": 0, "msg": "成功完成"})
]


@pytest.mark.parametrize('res_query_result, res', param_get_main_order_with_id)
def test_get_main_order_with_id(res_query_result, res, monkeypatch):
    def mock_orders_query_get(id):
        if res_query_result is not None:
            fake = Faker()
            order = Orders(name=fake.name(),
                           summary="None",
                           createdate=fake.date_time(),
                           deadline=fake.date_time(),
                           address=fake.city(),
                           quantity=1,
                           price=1.0,
                           totalprice=1.0,
                           createuser=0,
                           comments="None",
                           phone=fake.phone_number(),
                           status=0,
                           progress=0)
            order.ID = res_query_result["ID"] if res_query_result is not None else 0
            return order
        else:
            return None

    def mock_get_main_order_supply(id):
        return 10

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.mainorder_api.Orders.query", Mocker(get=mock_orders_query_get))
        monkeypatch.setattr("src.api.mainorder_api.get_main_order_supply", mock_get_main_order_supply)
        result = get_main_order_with_id(0)
        assert isinstance(result, dict) and result["code"] == res["code"] \
                and isinstance(result["data"], dict) and result["data"]["msg"] == res["msg"] \
                and (result["data"]["order"]["id"] == res_query_result["ID"]
                     and result["data"]["order"]["current_supply"] == 10) \
                    if "order" in result["data"] else True


"""
    @brief Test for post_main_order_with_id(mainOrderId, json_body)
"""
# TODO: add more tests, including erroneous inputs
param_post_main_order_with_id = [
    (None,
     {"name": "None",
      "summary": "None",
      "deadline": datetime.datetime.utcnow(),
      "address": "None",
      "quantity": "1",
      "price": "1",
      "createuser": "0",
      "comments": "None",
      "phone": "None"},
     {"code": 1, "msg": "该订单不存在"}),
    ({"ID": 1},
     {"name": "None",
      "summary": "None",
      "deadline": datetime.datetime.utcnow(),
      "address": "None",
      "quantity": "1",
      "price": "1",
      "createuser": "0",
      "comments": "None",
      "phone": "None"},
     {"code": 0, "msg": "成功完成"})
]


@pytest.mark.parametrize('res_query_result, json_body, res', param_post_main_order_with_id)
def test_post_main_order_with_id(res_query_result, json_body, res, monkeypatch):
    def mock_orders_query_get(id):
        if res_query_result is not None:
            fake = Faker()
            order = Orders(name=fake.name(),
                           summary="None",
                           createdate=fake.date_time(),
                           deadline=fake.date_time(),
                           address=fake.city(),
                           quantity=1,
                           price=1.0,
                           totalprice=1.0,
                           createuser=0,
                           comments="None",
                           phone=fake.phone_number(),
                           status=0,
                           progress=0)
            order.ID = res_query_result["ID"]
            return order
        else:
            return None

    def mock_db_commit():
        return

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.mainorder_api.Orders.query", Mocker(get=mock_orders_query_get))
        monkeypatch.setattr("src.api.mainorder_api.db.session", Mocker(commit=mock_db_commit))
        result = post_main_order_with_id(res_query_result["ID"] if res_query_result is not None else 0,
                                         json_body)
        assert isinstance(result, dict) and result["code"] == res["code"] \
               and isinstance(result["data"], dict) and result["data"]["msg"] == res["msg"]


"""
    @brief Test for post_finish_mainOrder_with_id(mainOrderId)
"""
# TODO: add more tests, including erroneous inputs
param_post_finish_mainOrder_with_id = [
    (None, {"code": 1, "msg": "该订单不存在"}),
    ({"ID": 1}, {"code": 0, "msg": "成功完成"})
]


@pytest.mark.parametrize('res_query_result, res', param_post_finish_mainOrder_with_id)
def test_post_finish_mainOrder_with_id(res_query_result, res, monkeypatch):
    def mock_orders_query_get(id):
        if res_query_result is not None:
            fake = Faker()
            order = Orders(name=fake.name(),
                           summary="None",
                           createdate=fake.date_time(),
                           deadline=fake.date_time(),
                           address=fake.city(),
                           quantity=1,
                           price=1.0,
                           totalprice=1.0,
                           createuser=0,
                           comments="None",
                           phone=fake.phone_number(),
                           status=0,
                           progress=0)
            order.ID = res_query_result["ID"]
            return order
        else:
            return None

    def mock_db_commit():
        return

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.mainorder_api.Orders.query", Mocker(get=mock_orders_query_get))
        monkeypatch.setattr("src.api.mainorder_api.db.session", Mocker(commit=mock_db_commit))
        result = post_finish_mainOrder_with_id(res_query_result["ID"] if res_query_result is not None else 0)
        assert isinstance(result, dict) and result["code"] == res["code"] \
               and isinstance(result["data"], dict) and result["data"]["msg"] == res["msg"]


"""
    @brief Test for post_cancel_mainOrder_with_id(mainOrderId)
"""
# TODO: add more tests, including erroneous inputs
param_post_cancel_mainOrder_with_id = [
    (None, {"code": 1, "msg": "该订单不存在"}),
    ({"ID": 1}, {"code": 0, "msg": "成功完成"})
]


@pytest.mark.parametrize('res_query_result, res', param_post_cancel_mainOrder_with_id)
def test_post_cancel_mainOrder_with_idd(res_query_result, res, monkeypatch):
    def mock_orders_query_get(id):
        if res_query_result is not None:
            fake = Faker()
            order = Orders(name=fake.name(),
                           summary="None",
                           createdate=fake.date_time(),
                           deadline=fake.date_time(),
                           address=fake.city(),
                           quantity=1,
                           price=1.0,
                           totalprice=1.0,
                           createuser=0,
                           comments="None",
                           phone=fake.phone_number(),
                           status=0,
                           progress=0)
            order.ID = res_query_result["ID"]
            return order
        else:
            return None

    def mock_db_commit():
        return

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.mainorder_api.Orders.query", Mocker(get=mock_orders_query_get))
        monkeypatch.setattr("src.api.mainorder_api.db.session", Mocker(commit=mock_db_commit))
        result = post_cancel_mainOrder_with_id(res_query_result["ID"] if res_query_result is not None else 0)
        assert isinstance(result, dict) and result["code"] == res["code"] \
               and isinstance(result["data"], dict) and result["data"]["msg"] == res["msg"]


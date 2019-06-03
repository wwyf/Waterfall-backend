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
from src.api.suborder_api import *

"""
    @brief Test for get_sub_orders(skip, limit)
"""
param_get_sub_orders = [
    (None, None, "manager", {"suborders_num": 200}, {"suborders_num": 100, "code": 0}),
    (None, 1, "manager", {"suborders_num": 200}, {"suborders_num": 1, "code": 0}),
    (1, None, "manager", {"suborders_num": 200}, {"suborders_num": 100, "code": 0}),
    (1, 20, "manager", {"suborders_num": 200}, {"suborders_num": 20, "code": 0}),
]


@pytest.mark.parametrize('skip, limit, role, db_suborders, res', param_get_sub_orders)
def test_get_sub_orders(skip, limit, role, db_suborders, res, monkeypatch):
    def mock_suborders_query_all():
        suborders = []
        fake = Faker()
        for i in range(0, db_suborders["suborders_num"]):
            o = subOrders(mainorder=0,
                          createdate=fake.date_time(),
                          createuser=0,
                          quantity=1,
                          comments="None",
                          phone=fake.phone_number(),
                          status=0)
            o.ID = 1
            suborders.append(o)
        return suborders

    def mock_get_main_order_supply(id):
        fake = Faker()
        return fake.random_int()

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.suborder_api.subOrders.query", Mocker(all=mock_suborders_query_all))
        monkeypatch.setattr("src.api.suborder_api.session", {"role": role})
        result = get_sub_orders(skip, limit)
        assert isinstance(result, dict) and result["code"] == res["code"] \
               and isinstance(result["data"], dict) and len(result["data"]["orders"]) == res["suborders_num"]


"""
    @brief Test for add_new_sub_order(json_body)
"""

param_add_new_sub_order = [
    ({"mainorder": "1",
      "quantity": "1",
      "createuser": "0",
      "comments": "None",
      "phone": "None"}, {"code": 0, "msg": "提交成功", "id": 0}),
    ({"mainorder": "1",
      "quantity": "10000",
      "createuser": "0",
      "comments": "None",
      "phone": "None"}, {"code": 2, "msg": "该子订单供应量超出了最大的限额", "remain_quantity": 100})
]


@pytest.mark.parametrize('json_body, res', param_add_new_sub_order)
def test_add_new_sub_order(json_body, res, monkeypatch):
    def mock_db_add(order):
        order.ID = 0

    def mock_db_commit():
        return

    def mock_users_query_filter_by(username):
        def mock_first():
            fake = Faker()
            user = Users(username=username,
                         password=fake.password(),
                         email=fake.email(),
                         phone=fake.phone_number(),
                         usertype=0,
                         userstatus=0)
            user.ID = 1
            return user

        return Mocker(first=mock_first)
    
    def mock_get_main_order_with_id(mainOrderId):
        return {
            'data':{
                'order' :{
                    'remain_quantity' : 100
                }
            }
        }

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.suborder_api.db.session", Mocker(add=mock_db_add, commit=mock_db_commit))
        monkeypatch.setattr("src.api.suborder_api.Users", Mocker(query=Mocker(filter_by=mock_users_query_filter_by)))
        monkeypatch.setattr("src.api.suborder_api.session", {"username": "test"})
        monkeypatch.setattr("src.api.mainorder_api.get_main_order_with_id", mock_get_main_order_with_id)
        result = add_new_sub_order(json_body)
        assert isinstance(result, dict) and result["code"] == res["code"]
        if result['code'] == 0:
            assert(result["data"]["msg"] == res["msg"] and result["data"]["id"] == res["id"])
        elif result['code'] == 2:
            assert(result["data"]["msg"] == res["msg"] and result["data"]["remain_quantity"] == res["100"])


"""
    @brief Test for get_sub_order_with_id(subOrderId)
"""

param_get_sub_order_with_id = [
    (None, {"code": 1, "msg": "该订单不存在"}),
    ({"ID": 1}, {"code": 0, "msg": "成功完成"})
]


@pytest.mark.parametrize('res_query_result, res', param_get_sub_order_with_id)
def test_get_sub_order_with_id(res_query_result, res, monkeypatch):
    def mock_suborders_query_get(id):
        if res_query_result is not None:
            fake = Faker()
            order = subOrders(mainorder=0,
                              createdate=fake.date_time(),
                              createuser=0,
                              quantity=1,
                              comments="None",
                              phone=fake.phone_number(),
                              status=0)
            order.ID = res_query_result["ID"] if res_query_result is not None else 0
            return order
        else:
            return None

    def mock_get_main_order_supply(id):
        return 10

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.suborder_api.subOrders.query", Mocker(get=mock_suborders_query_get))
        result = get_sub_order_with_id(0)
        assert isinstance(result, dict) and result["code"] == res["code"] \
               and isinstance(result["data"], dict) and result["data"]["msg"] == res["msg"] \
               and (result["data"]["order"]["id"] == res_query_result["ID"]
                    if "order" in result["data"] else True)


"""
    @brief Test for post_sub_order_with_id(subOrderId, json_body)
"""
# TODO: add more tests, including erroneous inputs
param_post_sub_order_with_id = [
    (None,
     {"mainorder": "0",
      "createdate": "1970-01-01 00:00:00",
      "createuser": "0",
      "quantity": "1",
      "comments": "None",
      "phone": "None",
      "status": "0"},
     {"code": 1, "msg": "该订单不存在"}),
    ({"ID": 1},
     {"mainorder": "0",
      "createdate": "1970-01-01 00:00:00",
      "createuser": "0",
      "quantity": "1",
      "comments": "None",
      "phone": "None",
      "status": "0"},
     {"code": 0, "msg": "成功完成"})
]


@pytest.mark.parametrize('res_query_result, json_body, res', param_post_sub_order_with_id)
def test_post_sub_order_with_id(res_query_result, json_body, res, monkeypatch):
    def mock_suborders_query_get(id):
        if res_query_result is not None:
            fake = Faker()
            order = subOrders(mainorder=0,
                              createdate=fake.date_time(),
                              createuser=0,
                              quantity=1,
                              comments="None",
                              phone=fake.phone_number(),
                              status=0)
            order.ID = res_query_result["ID"]
            return order
        else:
            return None

    def mock_db_commit():
        return

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.suborder_api.subOrders.query", Mocker(get=mock_suborders_query_get))
        monkeypatch.setattr("src.api.suborder_api.db.session", Mocker(commit=mock_db_commit))
        result = post_sub_order_with_id(res_query_result["ID"] if res_query_result is not None else 0,
                                        json_body)
        assert isinstance(result, dict) and result["code"] == res["code"] \
               and isinstance(result["data"], dict) and result["data"]["msg"] == res["msg"]


"""
    @brief Test for post_finish_sub_order_with_id(subOrderId)
"""
# TODO: add more tests, including erroneous inputs
param_post_finish_sub_order_with_id = [
    (None, {"code": 1, "msg": "该订单不存在"}),
    ({"ID": 1}, {"code": 0, "msg": "成功完成"})
]


@pytest.mark.parametrize('res_query_result, res', param_post_finish_sub_order_with_id)
def test_post_finish_sub_order_with_id(res_query_result, res, monkeypatch):
    def mock_suborders_query_get(id):
        if res_query_result is not None:
            fake = Faker()
            order = subOrders(mainorder=0,
                              createdate=fake.date_time(),
                              createuser=0,
                              quantity=1,
                              comments="None",
                              phone=fake.phone_number(),
                              status=0)
            order.ID = res_query_result["ID"]
            return order
        else:
            return None

    def mock_db_commit():
        return

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.suborder_api.subOrders.query", Mocker(get=mock_suborders_query_get))
        monkeypatch.setattr("src.api.suborder_api.db.session", Mocker(commit=mock_db_commit))
        result = post_finish_subOrder_with_id(res_query_result["ID"] if res_query_result is not None else 0)
        assert isinstance(result, dict) and result["code"] == res["code"] \
               and isinstance(result["data"], dict) and result["data"]["msg"] == res["msg"]


"""
    @brief Test for post_cancel_sub_order_with_id(subOrderId)
"""
# TODO: add more tests, including erroneous inputs
param_post_cancel_sub_order_with_id = [
    (None, {"code": 1, "msg": "该订单不存在"}),
    ({"ID": 1}, {"code": 0, "msg": "成功完成"})
]


@pytest.mark.parametrize('res_query_result, res', param_post_cancel_sub_order_with_id)
def test_post_cancel_sub_order_with_id(res_query_result, res, monkeypatch):
    def mock_suborders_query_get(id):
        if res_query_result is not None:
            fake = Faker()
            order = subOrders(mainorder=0,
                              createdate=fake.date_time(),
                              createuser=0,
                              quantity=1,
                              comments="None",
                              phone=fake.phone_number(),
                              status=0)
            order.ID = res_query_result["ID"]
            return order
        else:
            return None

    def mock_db_commit():
        return

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.suborder_api.subOrders.query", Mocker(get=mock_suborders_query_get))
        monkeypatch.setattr("src.api.suborder_api.db.session", Mocker(commit=mock_db_commit))
        result = post_cancel_subOrder_with_id(res_query_result["ID"] if res_query_result is not None else 0)
        assert isinstance(result, dict) and result["code"] == res["code"] \
               and isinstance(result["data"], dict) and result["data"]["msg"] == res["msg"]


"""
    @brief Test for get_sub_order_by_main_order(mainOrderId):
"""
param_get_sub_order_by_main_order = [
    (None, {"code": 1, "msg": "没有找到对应订单"}),
    ({"ID": 1}, {"code": 0})
]


@pytest.mark.parametrize('res_query_result, res', param_get_sub_order_by_main_order)
def test_get_sub_order_by_main_order(res_query_result, res, monkeypatch):
    def mock_suborders_query_filter_by(mainorder):
        if res_query_result is not None:
            fake = Faker()
            order = subOrders(mainorder=0,
                              createdate=fake.date_time(),
                              createuser=0,
                              quantity=1,
                              comments="None",
                              phone=fake.phone_number(),
                              status=0)
            order.ID = res_query_result["ID"]
            return [order]
        else:
            return None

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.suborder_api.subOrders.query", Mocker(filter_by=mock_suborders_query_filter_by))
        result = get_sub_order_by_main_order(res_query_result["ID"] if res_query_result is not None else 0)
        assert isinstance(result, dict) and result["code"] == res["code"] \
            and (isinstance(result["data"], dict) and result["data"]["msg"] == res["msg"]) \
            if "msg" in res else True

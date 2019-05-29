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
from src.api.wallet_api import *

"""
    @brief Test for get_wallet_balance(userId)
"""
param_get_wallet_balance = [
    (1, None, {"code": 1, "data":{"msg": "用户不存在"}}),
    (1, {"ID": 1, "balance": 1000}, {"code": 0, "data":{"balance": 1000}})
]


@pytest.mark.parametrize('user_id, target_user, res', param_get_wallet_balance)
def test_get_wallet_balance(user_id, target_user, res, monkeypatch):
    def mock_users_query_filter_by(ID):
        def mock_first():
            fake = Faker()
            if target_user is not None:
                user = Users(username="test",
                             password=fake.password(),
                             email=fake.email(),
                             phone=fake.phone_number(),
                             usertype=0,
                             userstatus=0)
                user.balance = target_user["balance"]
                user.ID = target_user["ID"]
                return user
            else:
                return None

        return Mocker(first=mock_first)

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.user_api.Users.query", Mocker(filter_by=mock_users_query_filter_by))
        result = get_wallet_balance(user_id)
        assert (isinstance(result, dict) and result == res)


"""
    @brief Test for deposit_wallet_balance(userId, amount)
"""
param_deposit_wallet_balance = [
    (1, None, 1000, {"code": 1, "data":{"msg": "用户不存在"}}),
    (1, {"ID": 1, "balance": 1000}, 1000, {"code": 0, "data":{"msg" : "已提交/操作成功"}})
]


@pytest.mark.parametrize('user_id, target_user, deposit, res', param_deposit_wallet_balance)
def test_deposit_wallet_balancee(user_id, target_user, deposit, res, monkeypatch):
    user = None
    def mock_users_query_filter_by(ID):
        def mock_first():
            nonlocal user
            fake = Faker()
            if target_user is not None:
                user = Users(username="test",
                             password=fake.password(),
                             email=fake.email(),
                             phone=fake.phone_number(),
                             usertype=0,
                             userstatus=0)
                user.balance = target_user["balance"]
                user.ID = target_user["ID"]
                return user
            else:
                return None

        return Mocker(first=mock_first)

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.user_api.Users.query", Mocker(filter_by=mock_users_query_filter_by))
        result = deposit_wallet_balance(user_id, deposit)
        assert isinstance(result, dict)
        assert result == res
        assert user.balance == target_user["balance"] + deposit if target_user is not None else True


"""
    @brief Test for withdraw_wallet_balance(userId, amount)
"""

param_withdraw_wallet_balance = [
    (1, None, 1000, {"code": 1, "data":{"msg": "用户不存在"}}),
    (1, {"ID": 1, "balance": 1000}, 10, {"code": 0, "data": {"msg": "已提交/操作成功"}}),
    (1, {"ID": 1, "balance": 1000}, 1000, {"code": 0, "data": {"msg": "已提交/操作成功"}}),
    (1, {"ID": 1, "balance": 1000}, 10000, {"code": 1, "data": {"msg": "余额不足"}})
]


@pytest.mark.parametrize('user_id, target_user, withdraw, res', param_withdraw_wallet_balance)
def test_withdraw_wallet_balance(user_id, target_user, withdraw, res, monkeypatch):
    user = None
    def mock_users_query_filter_by(ID):
        def mock_first():
            nonlocal user
            fake = Faker()
            if target_user is not None:
                user = Users(username="test",
                             password=fake.password(),
                             email=fake.email(),
                             phone=fake.phone_number(),
                             usertype=0,
                             userstatus=0)
                user.balance = target_user["balance"]
                user.ID = target_user["ID"]
                return user
            else:
                return None

        return Mocker(first=mock_first)

    with monkeypatch.context() as m:
        monkeypatch.setattr("src.api.user_api.Users.query", Mocker(filter_by=mock_users_query_filter_by))
        result = withdraw_wallet_balance(user_id, withdraw)
        correct_balance = 0
        if target_user is not None:
            if target_user["balance"] >= withdraw:
                correct_balance = target_user["balance"] - withdraw
            else:
                correct_balance = target_user["balance"]
        assert isinstance(result, dict)
        assert result == res
        assert user.balance == correct_balance if target_user is not None else True
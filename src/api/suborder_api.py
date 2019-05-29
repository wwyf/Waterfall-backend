from src.db.model import db, subOrders
import datetime
import traceback
import sys

def get_sub_orders(skip, limit):
    """
    获得订单列表

    Parameters:
        skip: int or None
            跳过skip个订单
        limit: int or None
            仅查看limit个订单
    Returns:
        返回订单列表，一个 [] 对象
        返回响应请求 res
    """
    if skip is None:
        skip = 0
    else:
        skip = int(skip)
    if limit is None:
        limit = 100
    else:
        limit = int(limit)
    res_query_results = subOrders.query.all()
    res_orders = []
    for i in res_query_results[skip:skip+limit]:
        res_orders.append(i.to_json())
    data_res = {
        "orders" : res_orders
    }
    res = {
        'code' : 0,
        'data' : data_res
    }
    return res

def add_new_sub_order(json_body):
    """
    传入一个post的body部分（已转换为json），生成一个新的订单，并在数据库中增加新的一行。

    Parameters:
        json_body : json对象 or dict
            包含订单所需的信息
    Returns:
        如果有错误，返回 -1 ,否则返回刚刚创建的新订单的id。
        返回响应请求 res
    """
    # default order
    mainOrderId = int(json_body['mainOrderId'])
    createdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    quantity = int(json_body['quantity'])
    createuser = int(json_body['createuser'])
    comments = json_body['comments']
    phone = json_body['phone']
    status = 1
    this_order = subOrders(
        mainOrderId,
        createdate,
        quantity,
        createuser,
        comments,
        phone,
        status
    )
    db.session.add(this_order)
    db.session.commit()
    # TODO: 处理异常情况？？
    data_res = {
        'msg' : '提交成功',
        'id' : this_order.ID
    }
    res = {
        'code' : 0,
        'data' : data_res
    }
    return res



def get_sub_order_with_id(subOrderId):
    """
    获得订单列表

    Parameters:
        subOrderId: int
    Returns:
        返回dict类型的一个订单
        返回响应请求 res
    """
    res_query_result = subOrders.query.get(subOrderId)
    if res_query_result is None:
        data_res = {
            "msg" : "该订单不存在"
        }
        code = 1
    else:
        data_res = {
            "order" : res_query_result.to_json(),
            "msg" : "成功完成"
        }
        code = 0
    res = {
        'code' : code,
        'data' : data_res
    }
    return res


def post_sub_order_with_id(subOrderId, json_body):
    """
    修改指定订单

    Parameters:
        subOrderId : int
        json_body : json对象 or dict
            包含订单所需的信息
    Returns:
        返回响应请求 res
    """
    res_query_result = subOrders.query.get(subOrderId)
    if res_query_result is None:
        return {
            'code' : 1,
            'data' : {
                'msg' : '该订单不存在'
            }
        }
    # 修改指定订单信息
    res_query_result.quantity = json_body['quantity']
    res_query_result.comments = json_body['comments']
    res_query_result.phone = json_body['phone']
    db.session.commit()
    return {
        'code' : 0,
        'data' : {
            'msg' : '成功完成'
        }
    }


def post_finish_subOrder_with_id(subOrderId):
    """
    尝试将subOrderId对应的母订单设置为完成状态。
    1 ： 正在进行中
    2 ： 已取消
    3 ： 已完成

    Parameters:
        subOrderId : int
    Returns:
        res: 返回json响应
    """
    res_query_result = subOrders.query.get(subOrderId)
    if res_query_result is None:
        return {
            'code' : 1,
            'data' : {
                'msg' : '该订单不存在'
            }
        }
    # 修改指定订单信息
    res_query_result.status = 3
    db.session.commit()
    return {
        'code' : 0,
        'data' : {
            'msg' : '成功完成'
        }
    }

def post_cancel_subOrder_with_id(subOrderId):
    """
    尝试将subOrderId对应的母订单设置为完成状态。
    1 ： 正在进行中
    
    3 ： 已完成
    4 ： 已取消

    Parameters:
        subOrderId : int
    Returns:
        res: 返回json响应
    """
    res_query_result = subOrders.query.get(subOrderId)
    if res_query_result is None:
        return {
            'code' : 1,
            'data' : {
                'msg' : '该订单不存在'
            }
        }
    # 修改指定订单信息
    res_query_result.status = 4
    db.session.commit()
    return {
        'code' : 0,
        'data' : {
            'msg' : '成功完成'
        }
    }

def get_sub_order_by_main_order(mainOrderId):
    res_query_result = subOrders.query.filter_by(mainorder=mainOrderId)
    res_list = []
    if res_query_result is None:
        return {
            "code" : 1,
            "data" : {
                "msg" : "没有找到对应订单"
            }
        }
    for order in res_query_result:
        res_list.append(order.to_json())
    return {
        "code" : 0,
        "data" : res_list
    }

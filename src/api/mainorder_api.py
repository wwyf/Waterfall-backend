from src.db.model import db, Orders
import datetime
import traceback
import sys



def get_main_orders(skip, limit):
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
    res_query_results = Orders.query.all()
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

def add_new_main_order(json_body):
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
    order_name = json_body['name']
    order_summary = json_body['summary']
    createdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    deadline = json_body['deadline']
    address = json_body['address']
    quantity = int(json_body['quantity'])
    price = int(json_body['price'])
    totalprice = quantity*price
    createuser = json_body['createuser']
    comments = json_body['comments']
    phone = json_body['phone']
    status = 1
    progress = 0
    this_order = Orders(
        order_name,
        order_summary,
        createdate,
        deadline,
        address,
        quantity,
        price,
        totalprice,
        createuser,
        comments,
        phone,
        status,
        progress
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

def get_main_order_with_id(mainOrderId):
    """
    获得订单列表

    Parameters:
        mainOrderId: int
    Returns:
        返回dict类型的一个订单
        返回响应请求 res
    """
    res_query_result = Orders.query.filter_by(ID=mainOrderId).first()
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


def post_main_order_with_id(mainOrderId, json_body):
    """
    修改指定订单

    Parameters:
        mainOrderId : int
        json_body : json对象 or dict
            包含订单所需的信息
    Returns:
        返回响应请求 res
    """
    res_query_result = Orders.query.get(mainOrderId)
    # 修改指定订单信息
    res_query_result.order_name = json_body['name']
    res_query_result.order_summary = json_body['summary']
    res_query_result.order_ddl = json_body['deadline']
    res_query_result.address = json_body['address']
    res_query_result.quantity = json_body['quantity']
    res_query_result.price = json_body['price']
    res_query_result.comments = json_body['comments']
    res_query_result.phone = json_body['phone']
    db.session.commit()
    if res_query_result is None:
        msg = "该订单不存在"
        code = 1
    else:
        msg = "成功完成"
        code = 0
    # 构造res
    data_res = {
        "msg" : msg
    }
    res = {
        'code' : code,
        'data' : data_res
    }
    return res

def post_finish_mainOrder_with_id(mainOrderId):
    """
    尝试将mainOrderId对应的母订单设置为完成状态。
    1 ： 正在进行中
    2 ： 已取消
    3 ： 已完成

    Parameters:
        mainOrderId : int
    Returns:
        res: 返回json响应
    """
    res_query_result = Orders.query.get(mainOrderId)
    # 修改指定订单信息
    res_query_result.status = 3
    db.session.commit()
    if res_query_result is None:
        msg = "该订单不存在"
        code = 1
    else:
        msg = "成功完成"
        code = 0
    # 构造res
    data_res = {
        "msg" : msg
    }
    res = {
        'code' : code,
        'data' : data_res
    }
    return res  

def post_cancel_mainOrder_with_id(mainOrderId):
    """
    尝试将mainOrderId对应的母订单设置为完成状态。
    1 ： 正在进行中
    
    3 ： 已完成
    4 ： 已取消

    Parameters:
        mainOrderId : int
    Returns:
        res: 返回json响应
    """
    res_query_result = Orders.query.get(mainOrderId)
    # 修改指定订单信息
    res_query_result.status = 4
    db.session.commit()
    if res_query_result is None:
        msg = "该订单不存在"
        code = 1
    else:
        msg = "成功完成"
        code = 0
    # 构造res
    data_res = {
        "msg" : msg
    }
    res = {
        'code' : code,
        'data' : data_res
    }
    return res  

import json
import pytest
import requests

"""
    @brief tester for user apis
"""
class UserAPITester:
    def __init__(self,
                 domain="127.0.0.1",
                 username="test_username",
                 password="test_password",
                 email="test@test.com",
                 phone="88888888",
                 role="provider"):
        self.domain = domain
        self.sess = requests.session()
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.role = role

    def api_get_login_status(self,
                             exp_code=0,
                             exp_msg="已经登录"):
        r = self.sess.get("http://" + self.domain + "/apis/user/login")
        j = r.json()
        assert j["code"] == exp_code
        assert j["data"]["msg"] == exp_msg
        return j

    def api_post_login_status(self,
                              exp_code=0,
                              exp_msg="登录成功"):
        r = self.sess.post("http://" + self.domain + "/apis/user/login",
                           data={
                               "username": self.username,
                               "password": self.password
                           })
        j = r.json()
        assert j["code"] == exp_code
        assert j["data"]["msg"] == exp_msg
        return j

    def api_post_register(self,
                          exp_code=0,
                          exp_msg="注册成功"):
        r = self.sess.post("http://" + self.domain + "/apis/user/register",
                           data={
                               "username": self.username,
                               "password": self.password,
                               "email": self.email,
                               "phone": self.phone,
                               "role": self.role
                           })
        j = r.json()
        assert j["code"] == exp_code
        assert j["data"]["msg"] == exp_msg
        return j

    def api_post_logout(self,
                        exp_code=0,
                        exp_msg="登出成功"):
        r = self.sess.post("http://" + self.domain + "/apis/user/logout")
        j = r.json()
        assert j["code"] == exp_code
        assert j["data"]["msg"] == exp_msg
        return j

    def api_get_user_info(self,
                          user_id,
                          exp_code=0):
        r = self.sess.get("http://" + self.domain + "/apis/user/register/%d" % user_id)
        j = r.json()
        assert j["code"] == exp_code
        return j

    def api_post_user_info(self,
                           user_id,
                           user_info,
                           exp_code=0,
                           exp_msg="修改成功"):
        r = self.sess.post("http://" + self.domain + "/apis/user/register/%d" % user_id,
                           data=user_info)
        j = r.json()
        assert j["code"] == exp_code
        assert j["data"]["msg"] == exp_msg
        return j

    def api_get_check_user(self,
                           exp_code=0,
                           exp_msg="用户名不存在"):
        r = self.sess.get("http://" + self.domain + "/apis/user/register/" + self.username)
        j = r.json()
        assert j["code"] == exp_code
        assert j["data"]["msg"] == exp_msg
        return j

param_user_api = [
    ({"domain": "127.0.0.1:5000"}, ["api_get_login_status"], [{}], [None])
]
"""
@pytest.mark.parametrize('init, exec_seq, exec_param, res_test', param_user_api)
def test_user_api(init, exec_seq, exec_param, res_test):
    tester = UserAPITester(**init)
    steps = len(exec_seq)
    assert len(exec_param) == steps and len(res_test) == steps
    for i in range(steps):
        res = getattr(tester, exec_seq[i])(**exec_param[i])
        if res_test[i] is not None:
            res_test[i](res)
"""
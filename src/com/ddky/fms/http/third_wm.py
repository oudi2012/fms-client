# coding='utf-8'
import time

import requests
import hashlib

from src.com.ddky.fms.entry.bill_entry import third_shop, key_config
from src.com.ddky.fms.entry.bill_url import wm_settle_url
from src.com.ddky.fms.jdbc.mysql_utils import MySQLHelper
from src.com.ddky.fms.jdbc.mysql_dml import querySQL


# url 连接地址 md5 加密
def md5_url(url):
    md = hashlib.md5()
    md.update(url.encode("utf-8"))
    return md.hexdigest()


# 组装 访问 url
def create_url(app_id=0, app_poi_code=0, start_date=0, end_date=0, offset=0, limit=10):
    params = "app_id=" + str(app_id) + "&app_poi_code=" + str(app_poi_code)
    params += "&end_date=" + str(end_date) + "&limit=" + str(limit) + "&offset=" + str(offset)
    params += "&request_source=sg_open_sdk-1.0.2-SNAPSHOT" + "&start_date=" + str(start_date)
    params += "&timestamp=" + str(int(time.time()))
    return params


# wm token
def token_wm():
    params = ("status", "platCode")
    cols = [item for item in key_config.keys()]
    str_cols = str(",".join(cols))
    select_sql = querySQL("fms_key_config", str_cols, params)
    sqlHelper = MySQLHelper()
    data_list = sqlHelper.queryByParam(select_sql, 10, (1, "mt"))
    for item in data_list:
        print(item)
    return data_list


# 美团店铺列表信息
def list_shop_wm():
    params = "platformId"
    cols = [item for item in third_shop.keys()]
    str_cols = str(",".join(cols))
    select_sql = querySQL("fms_third_shopinfo", str_cols, params)
    print(select_sql)
    sqlHelper = MySQLHelper()
    return sqlHelper.queryByParam(select_sql, 1000, 1)


# 获取三方店铺
def request_bill_wm():
    #tokens = token_wm()[0]
    shop_list = list_shop_wm()
    for item in shop_list:
        print(item)
        url_params = create_url(app_id=74, app_poi_code=205012, start_date=1606752000, end_date=1606924800)
        request_url = wm_settle_url + url_params
        url_secret = request_url + "de468c09092f8068dfa6193ebebe43a6"
        sign = md5_url(url_secret)
        request_url = request_url + "&sig=" + sign
        print(request_url)
        response = requests.get(request_url)
        print(response.text)


if __name__ == "__main__":
    request_bill_wm()

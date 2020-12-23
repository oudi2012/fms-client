# coding='utf-8'

import requests

# 获取三方token配置
from src.com.ddky.fms.entry.bill_entry import third_shop
from src.com.ddky.fms.jdbc.mysql_utils import MySQLHelper
from src.com.ddky.fms.jdbc.mysql_dml import insertSQL


# 获取三方店铺
def request_third_shops():
    response = requests.post("http://fms.ddky.com/wm_shop_info/query.htm")
    insertSql = insertSQL("fms_third_shopinfo", **third_shop)
    sqlHelper = MySQLHelper()
    for item in eval(response.text):
        _item = []
        for key in third_shop.keys():
            _item.append(item[key])
        print(_item)
        sqlHelper.insert(insertSql, _item)
    sqlHelper.dispose()


if __name__ == "__main__":
    request_third_shops()

# coding='utf-8'

import requests


# 获取三方token配置
from src.com.ddky.fms.entry.bill_entry import key_config
from src.com.ddky.fms.jdbc.mysql_utils import MySQLHelper
from src.com.ddky.fms.jdbc.mysql_dml import insertSQL


def request_key_configs():
    response = requests.post("http://fms.ddky.com/thirdPartConfig/query.htm")
    insertSql = insertSQL("fms_key_config", **key_config)
    sqlHelper = MySQLHelper()
    for item in eval(response.text):
        _item = []
        for key in key_config.keys():
            _item.append(item[key])
        print(_item)
        sqlHelper.insert(insertSql, _item)
    sqlHelper.dispose()


if __name__ == "__main__":
    request_key_configs()

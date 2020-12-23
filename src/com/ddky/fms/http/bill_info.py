# coding='utf-8'

import requests

# 获取美团账单
from src.com.ddky.fms.jdbc.mysql_dml import querySQLAndWhere
from src.com.ddky.fms.jdbc.mysql_utils import MySQLHelper


def request_wm_bills(settle_date):
    """
    @summary : 根据账单日期获取账单列表
    :param settle_date: 账单日期
    :return: list
    """
    response = requests.post("http://fms.ddky.com/thirdPartConfig/query.htm")
    for item in eval(response.text):
        print(item)


def cutStr():
    str_item = "select * from f_meituan_bill where name=a and settle_date=b and"
    print(str_item.rindex("and"))
    str_item = str(str_item[0: str_item.rindex("and")])
    print(str_item)


# 任务信息字段
task_cols = ["channelCode", "settleTime", "excelTotal",
             "opTotal", "opState", "rtState", "creator", "createDate",
             "startRead", "endRead", "startFormat", "endFormat", "startCheck", "endCheck"]

if __name__ == "__main__":
    sql_where = " where channelCode=%s and startRead>%s"
    select_sql = querySQLAndWhere("fms_task_info", ",".join(task_cols), sql_where)
    sql_helper = MySQLHelper()
    result = sql_helper.queryByParam(select_sql, 1, ('wm', 0))
    sql_helper.dispose()
    for item in result:
        for col in task_cols:
            print(col, " ", str(item[col]))

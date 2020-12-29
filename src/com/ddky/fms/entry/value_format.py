# coding='utf-8'

# 数据表显示数据格式化
from src.com.ddky.fms.entry.pay_type_enum import page_type


def format_value(name, value):
    if name == 'pageType':
        return page_type.get(value)
    elif name == 'money':
        return fenToYuan(value)
    elif name == 'billType':
        return billType(value)
    elif name == 'normal':
        return value


# 账单类型
def billType(value):
    if value is None or len(value) <= 0:
        return '收款'
    if int(value) == 1:
        return '收款'
    else:
        return '退款'


# 分 -> 元
def fenToYuan(value):
    if value is None or len(value) <= 0:
        return '0'
    return str(float(value) / 100)

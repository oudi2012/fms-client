# coding='utf-8'

# 根据文件名，将文件内的数据转换成三方账单
import xlrd
import logging
import time
import math

from src.com.ddky.fms.entry.bill_config import PER_BILL_COUNT, ENUM_CHANNEL_WM
from src.com.ddky.fms.entry.bill_entry import reading_task_start, formatting_task_start
from src.com.ddky.fms.jdbc.mysql_dml import insertSQL, querySQLAndWhere
from src.com.ddky.fms.jdbc.mysql_utils import MySQLHelper

logging.basicConfig(level=logging.INFO, filename='fms_log.log', datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)

# 任务信息字段
task_cols = ["channelCode", "settleTime", "excelTotal",
             "opTotal", "opState", "rtState", "creator", "createDate",
             "startRead", "endRead", "startFormat", "endFormat", "startCheck", "endCheck"]


# Excel列字母转数字, 用于获取数据
def excel_column_to_num(col):
    length = len(col)
    a_no = ord('A')
    result = 0
    for i in range(length):
        ch_no = ord(col[length - i - 1])
        ch_no = ch_no - a_no + 1
        ch_no *= math.pow(26, i)
        result += ch_no
    return int(result - 1)


# 判断如果已经存在任务，则退出创建
def init_task(channelCode):
    sql_where = " where channelCode=%s and startRead>%s"
    select_sql = querySQLAndWhere("fms_task_info", ",".join(task_cols), sql_where)
    sql_helper = MySQLHelper()
    result = sql_helper.queryByParam(select_sql, 1, (channelCode, 0))
    sql_helper.dispose()
    if not result:
        return 0
    else:
        return 1


# 读取excel 文件数据
def read_sheet(excel_name, sheet_index=0):
    insert_sql = insertSQL("fms_task_info", task_cols)
    has = init_task(ENUM_CHANNEL_WM)
    if has == 1:
        logging.info("方法 read_sheet 查询任务中已存在渠道： {} 的任务".format(ENUM_CHANNEL_WM))
        return
    startTime = int(time.time())
    sql_helper = MySQLHelper()
    wm_tuple = reading_task_start(ENUM_CHANNEL_WM, 'sys', task_cols)
    sql_helper.insert(insert_sql, wm_tuple)
    sql_helper.dispose()
    logging.info("方法:bill_wm_to_third 从文件 {} 中读取数据,开始时间：{}".format(excel_name, startTime))
    TC_workbook = xlrd.open_workbook(excel_name)
    endTime = int(time.time())
    logging.info("方法:bill_wm_to_third 从文件 {} 中读取数据,结束时间：{}, 读取时长：{} s".format(excel_name, endTime, endTime - startTime))
    sheet = TC_workbook.sheet_by_index(sheet_index)
    return sheet


# 保存账单到数据库
def save_bills(insert_sql, third_list, settleTime, excelTotal, cols, page_index=1, total=0):
    sql_helper = MySQLHelper()
    sql_helper.batchInsert(insert_sql, third_list)
    sql_helper.dispose()
    third_list.clear()
    logging.info("方法:save_bills 执行页码：{}, 条数：{} ".format(page_index, len(third_list)))
    # 更新任务状态
    startTime = int(time.time())
    sql_helper = MySQLHelper()
    wm_tuple = formatting_task_start(ENUM_CHANNEL_WM, settleTime, excelTotal, total, cols)
    sql_helper.insert(insert_sql, wm_tuple)
    sql_helper.dispose()
    endTime = int(time.time())
    logging.info("方法:save_bills 更新任务,开始时间：{}, 执行时长：{} s".format(startTime, endTime, endTime - startTime))


# 格式化 excel 数据到三方账单
def bill_wm_to_third(excel_name, sheet_index=0):
    sheet = read_sheet(excel_name, sheet_index)
    if sheet is None:
        return
    third_list = []
    cols = ["thirdOrderId", "payType", "amount", "status", "createdAt", "createdBy", "type", "checkAmount",
            "serviceCharge", "payAt", "channelDiscountPay", "orderPayAt", "receivePayTime", "businessTime",
            "diffAmount"]
    insert_sql = insertSQL("fms_third_bill", cols)
    total = 0
    page_index = 0
    settleTime = ""
    for row_item in range(sheet.nrows):
        if row_item == 0:
            continue
        third_item = item_to_third(sheet.row_values(row_item))
        settleTime = time.strptime(third_item["receivePayTime"], "%Y-%m-%d")
        tuple_item = item_to_tuple(third_item, cols)
        third_list.append(tuple_item)
        print(settleTime)
        if len(third_list) >= PER_BILL_COUNT:
            save_bills(insert_sql, third_list, int(time.mktime(settleTime)), sheet.nrows - 1, cols, page_index, total)
            total += PER_BILL_COUNT
            page_index += 1

    if len(third_list) > 0:
        total += len(third_list)
        page_index += 1
        save_bills(insert_sql, third_list, int(time.mktime(settleTime)), sheet.nrows - 1, cols, page_index, total)


def item_to_tuple(item, cols):
    tuple_item = []
    for col in cols:
        tuple_item.append(str(item[col]))
    return tuple(tuple_item)


# 美团取数逻辑如下：
# 1、整理W列数据，将“-”剔除；
# 2、订单号：H列；
# 3、下单时间：I列；
# 4、订单类型：若R列>=0，为收款；R列<0，为退款；
# 5、支付平台金额(计算结果保留两位小数): 若R列>=0，取S+V+AA-W；R列<0，取S+V-AA+W；
# 6、平台服务费：取X列；
# 7、渠道优惠：若R列>=0，取W ; R列<0，取  -W ；
# 8、 结算金额：支付平台金额+平台服务费+渠道优惠；
# 9、美团到账时间取数：P列“账单日期”；
# 10、业务时间取：P列“账单日期”；
def item_to_third(item):
    third_bill = {}
    idx_w = excel_column_to_num("W")
    if item[idx_w] == '':
        item[idx_w] = 0
    w_value = int(float(item[idx_w]) * 100)
    if w_value <= 0:
        w_value = w_value * -1
    idx_h = excel_column_to_num("H")
    third_bill['thirdOrderId'] = str(item[idx_h])
    third_bill['payType'] = 10
    idx_i = excel_column_to_num("I")
    third_bill['orderPayAt'] = str(item[idx_i])
    third_bill['payAt'] = str(item[idx_i])
    idx_x = excel_column_to_num("X")
    x_value = int(float(item[idx_x]) * 100)
    third_bill['serviceCharge'] = x_value
    idx_s = excel_column_to_num("S")
    s_value = int(float(item[idx_s]) * 100)
    idx_v = excel_column_to_num("V")
    v_value = int(float(item[idx_v]) * 100)
    idx_aa = excel_column_to_num("AA")
    aa_value = int(float(item[idx_aa]) * 100)
    idx_r = excel_column_to_num("R")
    settle_amount = int(float(item[idx_r]) * 100)
    if settle_amount >= 0:
        third_bill['type'] = 1
        third_bill['channelDiscountPay'] = w_value
        third_bill['amount'] = s_value + v_value + aa_value - w_value
    else:
        third_bill['type'] = 2
        third_bill['channelDiscountPay'] = w_value * -1
        third_bill['amount'] = s_value + v_value - aa_value + w_value
    third_bill['checkAmount'] = third_bill['amount'] + x_value + third_bill['channelDiscountPay']
    idx_p = excel_column_to_num("P")
    third_bill['receivePayTime'] = str(item[idx_p])
    third_bill['businessTime'] = str(item[idx_p])
    idx_u = excel_column_to_num("U")
    u_value = int(float(item[idx_u]) * 100)
    third_bill['diffAmount'] = settle_amount - third_bill['checkAmount'] + u_value
    third_bill['status'] = 1
    third_bill['createdBy'] = "sys"
    third_bill['createdAt'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return third_bill


if __name__ == "__main__":
    bill_wm_to_third("../excel/wm_02.xlsx")

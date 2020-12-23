# coding='utf-8'

# 三方 token
import time

key_config = {
    "id": 0,
    "city": "",
    "appKey": "",
    "appSecret": "",
    "token": "",
    "operator": "",
    "tokenName": "",
    "status": 0,
    "orgCode": 0,
    "orgName": "",
    "platCode": ""
}

# 三方店铺
third_shop = {
    "id": 0,
    "thirdShopId": "",
    "name": "",
    "shopId": 0,
    "platformId": 0,
    "thirdName": ""
}

# 美团参数
wm_param = {
    "app_id": 0,
    "app_poi_code": 0,
    "start_date": 0,
    "end_date": 0,
    "offset": 0,
    "limit": 0,
    "request_source": "sg_open_sdk-1.0.2-SNAPSHOT",
    "timestamp": 0
}

# 渠道信息
channel_info = {
    "id": 0,
    "channelCode": "",
    "channelName": "",
    "settleCircle": 0,
    "settleGetTime": "",
    "creator": "",
    "createDate": 0
}

# 任务信息
task_info = {
    "id": 0,
    "channelCode": "",
    "settleTime": 0,
    "excelTotal": 0,
    "opTotal": 0,
    "opState": "",
    "rtState": "",
    "creator": "",
    "createDate": 0,
    "startRead": 0,
    "endRead": 0,
    "startFormat": 0,
    "endFormat": 0,
    "startCheck": 0,
    "endCheck": 0,
    "startLoad": 0,
    "endLoad": 0
}

# 任务信息表头
task_info_map = {
    "id": "编号",
    "channelCode": "渠道编码",
    "settleTime": "结算时间",
    "excelTotal": "excel总数",
    "opTotal": "操作数量",
    "opState": "操作状态",
    "rtState": "返回状态",
    "creator": "创建人",
    "createDate": "创建日期",
    "startRead": "读取开始",
    "endRead": "读取结束",
    "startFormat": "转化开始",
    "endFormat": "转化结束",
    "startCheck": "核对开始",
    "endCheck": "核对结束",
    "startLoad": "加载开始",
    "endLoad": "加载结束"
}


# 初始化读取状态的任务对象(excel 方面 insert)
def reading_task_start(channelCode, creator, cols):
    task_tuple = []
    for col in cols:
        if col == 'channelCode':
            task_tuple.append(channelCode)
        elif col == 'creator':
            task_tuple.append(creator)
        elif col == 'startRead':
            task_tuple.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        elif col == 'opState':
            task_tuple.append('reading')
        elif col == 'rtState':
            task_tuple.append('running')
        elif col == 'createDate':
            task_tuple.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        else:
            task_tuple.append(str(task_info[col]))
    return tuple(task_tuple)


# 执行格式化数据状态的任务对象(excel 方面 update)
def formatting_task_start(channelCode, settleTime, excelTotal, opTotal, cols):
    task_tuple = []
    for col in cols:
        if col == 'settleTime':
            task_tuple.append(settleTime)
        elif col == 'channelCode':
            task_tuple.append(channelCode)
        elif col == 'excelTotal':
            task_tuple.append(excelTotal)
        elif col == 'opTotal':
            task_tuple.append(opTotal)
        elif col == 'endRead':
            task_tuple.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        elif col == 'startFormat':
            task_tuple.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        elif col == 'opState':
            task_tuple.append('formatting')
        elif col == 'rtState':
            task_tuple.append('running')
        else:
            task_tuple.append(str(task_info[col]))
    return tuple(task_tuple)


# 执行核对数据量状态的任务对象(excel 方面 update)
def checking_task_startAndEnd(channelCode, settleTime, cols):
    task_tuple = []
    for col in cols:
        if col == 'settleTime':
            task_tuple.append(settleTime)
        elif col == 'channelCode':
            task_tuple.append(channelCode)
        elif col == 'endFormat' or col == 'startCheck' or col == 'endCheck':
            task_tuple.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        elif col == 'opState':
            task_tuple.append('over')
        elif col == 'rtState':
            task_tuple.append('success')
        else:
            task_tuple.append(str(task_info[col]))
    return tuple(task_tuple)


# 三方账单
third_bill = {
    "id": 0,
    "thirdOrderId": "",
    "payType": 0,
    "amount": 0,
    "status": 0,
    "createdAt": "",
    "createdBy": "",
    "type": 0,
    "checkAmount": 0,
    "checkAt": "",
    "checkBy": "",
    "serviceCharge": 0,
    "payAt": "",
    "settleStatus": 0,
    "channelDiscountPay": 0,
    "orderPayAt": "",
    "receivePayTime": "",
    "businessTime": "",
    "diffAmount": 0,
    "deliverPay": 0,
    "accountDate": ""
}

# 三方账单表头对应字段
third_bill_map = {
    "id": "编号",
    "thirdOrderId": "三方编号",
    "payType": "支付类型",
    "status": "对账状态",
    "type": "类型",
    "amount": "账单金额",
    "serviceCharge": "平台服务费",
    "channelDiscountPay": "渠道优惠",
    "checkAmount": "结算金额",
    "receivePayTime": "到账时间",
    "createdAt": "导入时间",
    "createdBy": "操作人",
    "accountDate": "账单日期"
}

# 美团账单对象类
wm_bill = {
    "id": "",
    "bill_charge_type": 0,
    "charge_fee_desc": "",
    "user_pay_type": "",
    "wm_poi_order_push_day_seq": "",
    "wm_order_view_id": "",
    "order_time": "",
    "finish_time": "",
    "refund_time": "",
    "order_state": 0,
    "shipping_type": 0,
    "shipping_status": 0,
    "account_state": 0,
    "daliy_bill_date": 0,
    "settle_bill_desc": "",
    "settle_amount": 0,
    "total_food_amount": 0,
    "box_amount": 0,
    "activity_poi_amount": 0,
    "activity_meituan_amount": 0,
    "activity_agent_amount": 0,
    "platform_charge_fee": 0,
    "performance_service_fee": 0,
    "user_pay_shipping_amount": 0,
    "user_online_pay_amount": 0,
    "user_offline_pay_amount": 0,
    "rate": 0,
    "bottom": "",
    "refund_id": 0,
    "discount": 0,
    "settle_milli": 0,
    "settle_setting_id": "",
    "wm_donation_amount": 0,
    "wm_doggy_bag_amount": 0,
    "deal_tip": 0,
    "product_preferences": 0,
    "not_product_preferences": 0
}

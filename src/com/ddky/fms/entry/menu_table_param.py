# coding='utf-8'

from src.com.ddky.fms.entry.bill_entry import third_shop_map, third_bill_map, task_info_map, third_bill, third_shop, \
    task_info, excel_path, excel_path_map

param_menu_table = {
    'btn_third_shop': {
        "menu_name": '三方店铺',
        "btn_name": "btn_third_shop",
        "table_name": "fms_third_shopinfo",
        "page_size": 30,
        "default_value": third_shop,
        "entry_map": third_shop_map
    },
    'btn_third_bill': {
        "menu_name": '三方账单',
        "btn_name": "btn_third_bill",
        "table_name": "fms_third_bill",
        "page_size": 30,
        "default_value": third_bill,
        "entry_map": third_bill_map
    },
    'btn_task': {
        "menu_name": '任务列表',
        "btn_name": "btn_task",
        "table_name": "fms_task_info",
        "page_size": 30,
        "default_value": task_info,
        "entry_map": task_info_map
    },
    'btn_excel_path': {
        "menu_name": '路径配置',
        "btn_name": "btn_excel_path",
        "table_name": "fms_excel_path",
        "page_size": 30,
        "default_value": excel_path,
        "entry_map": excel_path_map
    }
}

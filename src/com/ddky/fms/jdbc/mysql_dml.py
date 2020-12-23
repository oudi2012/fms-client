# coding='utf-8'

def getValueByType(value):
    if type(value) == 'int':
        return value
    else:
        return "'" + value + "'"


def str_join(val_01, val_02):
    return val_01 + val_02


# 生成 select sql
def querySQLAndWhere(tableName, cols, where):
    sql = "select  " + cols + " from " + tableName + " " + where
    print(sql)
    return sql


# 生成 select sql
def querySQL(tableName, cols, params):
    sql = "select  " + cols + " from " + tableName
    if type(params) == str:
        sql = sql + " where " + str_join(params, "=%s")
    else:
        where = str(' and '.join(str_join(str(key), "=%s") for key in params))
        sql = sql + " where " + where
    print(sql)
    return sql


# 生成 insert sql
def insertSQL(tableName, args):
    sql = "insert into " + tableName
    cols = []
    values = []
    for item in args:
        cols.append(item)
        values.append("%s")
    sql = sql + " (" + ",".join(cols) + ") values (" + ",".join(values) + ")"
    print(sql)
    return sql


# 生成 update sql
def updateSQLById(tableName, _id, **kwargs):
    sql = "update " + tableName + " set "
    items = ""
    for key, value in kwargs.items():
        if _id == key:
            continue
        items += key + " = '" + value + "',"
    items = str([0, items.rindex(",")])
    return sql + items + " where id=" + _id

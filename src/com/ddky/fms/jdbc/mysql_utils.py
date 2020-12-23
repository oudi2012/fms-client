# coding='utf-8'

"""
执行语句查询有结果返回结果，没有返回0；增删改返回变更数据条数，没有返回0
"""
from src.com.ddky.fms.jdbc.mysql_conn import MySQLConnPool


class MySQLHelper(object):
    def __init__(self):
        # 从数据库连接池中获取连接
        self.db = MySQLConnPool()

    def __new__(cls, *args, **kwargs):
        # 单例
        if not hasattr(cls, 'inst'):
            cls.inst = super(MySQLHelper, cls).__new__(cls, *args, **kwargs)
        return cls.inst

    # 执行sql
    def execute(self, sql, param=None):
        if param is None:
            count = self.db.cursor.execute(sql)
        else:
            count = self.db.cursor.execute(sql, param)
        return count

    # 查询所有
    def queryByParam(self, sql, num=20, param=None):
        """
        @summary: 执行查询，并取出所有结果集
        :param num: 获取条数 默认 20
        :param sql: 查询 sql, 如果有查询条件，请只指定条件列表，并将条件值使用参数传递进来
        :param param:可选参数，条件列表值
        :return: result list(字典对象)/boolean 查询到的结果集
        """
        try:
            if param is None:
                count = self.db.cursor.execute(sql)
            else:
                count = self.db.cursor.execute(sql, param)
            if count > 0:
                result = self.db.cursor.fetchmany(num)
            else:
                result = False
            return result
        except Exception as e:
            print(e)
            return False

    def findOne(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        :param sql: 查询 sql ,如果有查询条件，请指定条件列表，并将条件值使用参数传递进来
        :param param: 可选参数，条件列表值
        :return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self.db.cursor.execute(sql)
        else:
            count = self.db.cursor.execute(sql, param)
        if count > 0:
            result = self.db.cursor.fetchone()
        else:
            result = False
        return result

    def batchInsert(self, sql, listItem):
        """
        向数据库添加多条记录
        :param sql: 要插入的 sql 格式
        :param listItem: 要插入的记录数据 list
        :return: count 受影响的行数
        """
        count = self.db.cursor.executemany(sql, listItem)
        return count

    def update(self, sql, param=None):
        """
        @summary: 更细腻数据表记录
        :param sql: sql,使用 %s 作为参数
        :param param: 要更新的值
        :return: count 受影响的行数
        """
        return self.execute(sql, param)

    def insert(self, sql, param=None):
        """
        @summary: 添加数据表记录
        :param sql: sql
        :param param: param
        :return: 行数
        """
        return self.execute(sql, param)

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        :param sql: sql
        :param param: param
        :return: 行数
        """
        return self.execute(sql, param)

    def begin(self):
        """
        @summary: 开启事务
        :return:
        """
        self.db.conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        :param option:
        :return:
        """
        if option == 'commit':
            self.db.conn.commit()
        else:
            self.db.conn.rollback()

    def dispose(self, isEnd=1):
        """
        @summary: 释放连接池资源
        :param isEnd:
        :return:
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self.db.cursor.close()
        self.db.conn.close()

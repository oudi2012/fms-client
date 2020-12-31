# encoding=utf-8

"""
@功能： 创建数据库连接池
"""
from dbutils.pooled_db import PooledDB
from pymysql.cursors import DictCursor

from src.com.ddky.fms.jdbc import mysql_config


class MySQLConnPool(object):
    __pool = None

    # 创建数据库连接 conn 和 游标 cursor
    def __init__(self):
        self.conn = self.__getConn()
        self.cursor = self.conn.cursor()

    def __getConn(self):
        if self.__pool is None:
            self.__pool = PooledDB(
                creator=mysql_config.DB_CREATOR,
                mincached=mysql_config.DB_MIN_CACHED,
                maxcached=mysql_config.DB_MAX_CACHED,
                host=mysql_config.DB_HOST,
                port=mysql_config.DB_PORT,
                user=mysql_config.DB_USER,
                passwd=mysql_config.DB_PASSWD,
                db=mysql_config.DB_NAME,
                use_unicode=True,
                charset=mysql_config.DB_CHARSET,
                cursorclass=DictCursor
            )
            return self.__pool.connection()

    # 释放连接池资源
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        self.cursor.close()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import base64
import json

'''
将 0001 题生成的 200 个激活码（或者优惠券）保存到 **MySQL** 关系型数据库中。 
'''
def base64_generator():
    message = {}
    codes = []
    for i in range(0, 200):
        message['id'] = i
        message['goods'] = 'product%d' % i
        raw_64 = base64.b64encode(json.dumps(message).encode(encoding='utf-8'))
        code = raw_64.decode().replace('=', '')
        codes.append(code[-8:])
    return codes


class MySql_init(object):
    """docstring for ."""

    def __init__(self, conn):
        self.conn = conn

    def connect(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='',
            db='coupons',
            charset='utf8'
        )

    def cursor(self):
        try:
            return self.conn.cursor()
        except Exception as e:
            self.connect()
            return self.conn.cursor()

    def commit(self):
        return self.conn.commit()

    def close(self):
        return self.conn.close()


def query(sql, conn):
    conn.execute(sql)
    rows = conn.fetchall()
    return rows


def create_table(conn):
    conn.execute('DROP TABLE IF EXISTS `user_key`')
    conn.execute('CREATE TABLE `user_key` (`code` varchar(50) NOT NULL)')


def insert_data(conn):
    codes = base64_generator()
    sql = 'INSERT INTO user_key VALUE (%(value)s)'
    param = [dict(value=v) for v in codes]
    conn.executemany(sql, param)


def delete_data(conn):
    sql = 'delete from user_key where `code` ="QxOTgifQ"'
    conn.execute(sql)
    pass


def query_data(conn):
    rows = query('select * from user_key', conn)
    print_result(rows)


def print_result(rows):
    if rows:
        for row in rows:
            print(row)
    else:
        print('sql execute is null')


def process(dbconn):
    dbconn.connect()
    conn = dbconn.cursor()
    create_table(conn)
    insert_data(conn)
    query_data(conn)
    #一定要执行commit不然不能添加到本地数据库
    dbconn.commit()
    conn.close()
    dbconn.close()


if __name__ == '__main__':
    dbconn = MySql_init(conn=None)
    process(dbconn)

import pymysql
import numpy as np

__metaclass__ = type


class DBHelper:
    @staticmethod
    def get_con(if_dict=True):
        config = {
            'host': 'localhost',
            'port': 3306,
            'user': '1160300103',
            'password': '19981017',
            'db': 'ics_db',
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor,
        }
        if not if_dict:
            config['cursorclass'] = pymysql.cursors.Cursor
        '''获取操作数据库的curcor即游标，首先的建立连接，需要服务器地址，端口号，用户名，密码和数据库名'''
        conn = pymysql.connect(**config)
        return conn

    @staticmethod
    def execute(sql, conn, args=None):
        if not conn:
            raise Exception("connect failed")
        cursor = conn.cursor()  # (pymysql.cursors.DictCursor)
        num = cursor.execute(sql, args)
        return cursor, num

    @staticmethod
    def close(conn=None, cursor=None):
        if conn:
            conn.close()
        if cursor:
            cursor.close()

    def write_data(self, name, data, conn):
        cursor = None
        try:
            sql = "insert into training_data (data_name,data) values (%s, %s)"
            cursor, num = self.execute(sql, args=(name, data), conn=conn)
        except Exception as e:
            conn.rollback()
            raise Exception("insert failed!")
        finally:
            conn.commit()
            DBHelper.close(cursor=cursor)

    def read_data(self, name, conn):
        sql = "select data from training_data where data_name = '{}'".format(name)
        cursor = None
        try:
            cursor, num = self.execute(sql, conn=conn)
            values = cursor.fetchall()
            data = np.frombuffer(values[0][0], dtype='f')
            data = data.reshape((1, 32, 32))
        except Exception as e:
            raise Exception("read failed!")
        finally:
            DBHelper.close(cursor=cursor)
        return data

    def get_files(self, conn):
        sql = "select data_name from training_data"
        cursor = None
        try:
            cursor, num = self.execute(sql, conn)
            values = cursor.fetchall()
        except Exception as e:
            raise Exception("read files name failed!")
        finally:
            DBHelper.close(cursor=cursor)
        return values

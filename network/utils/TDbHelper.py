import pymysql
import numpy as np

__metaclass__ = type


class TDBHelper:
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

    def write_data(self, name, data, label, conn):
        cursor = None
        try:
            sql = "insert into app_datas (data_name,data,label) values (%s, %s, %s)"
            cursor, num = self.execute(sql, args=(name, data, label), conn=conn)
        except Exception as e:
            conn.rollback()
            raise Exception("insert failed!")
        finally:
            conn.commit()
            TDBHelper.close(cursor=cursor)

    def read_data(self, name, conn):
        sql = "select data,label from app_datas where data_name = '{}'".format(name)
        cursor = None
        try:
            cursor, num = self.execute(sql, conn=conn)
            values = cursor.fetchall()
            item = values[0]
            data = np.frombuffer(item[0], dtype='f')
            data = data.reshape((1, 32, 32))
            label = item[1]
        except Exception as e:
            raise Exception("read failed!")
        finally:
            TDBHelper.close(cursor=cursor)
        return data, label

    def get_files(self, conn):
        sql = "select data_name from app_datas"
        cursor = None
        try:
            cursor, num = self.execute(sql, conn)
            values = cursor.fetchall()
        except Exception as e:
            raise Exception("read files name failed!")
        finally:
            TDBHelper.close(cursor=cursor)
        return values

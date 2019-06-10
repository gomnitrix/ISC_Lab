import pymysql
import threading
__metaclass__ = type


class DBHelper:
    @staticmethod

    def get_con(if_dict=True):
        config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '1026Lijing-=',
            'db': 'lsc_lab',
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor,
        }


        if not if_dict:
            config['cursorclass'] = pymysql.cursors.Cursor

        conn = pymysql.connect(**config)
        return conn

    @staticmethod
    def execute(sql,conn, args=None):

        if not conn:
            raise Exception("connect failed")
        cursor = conn.cursor()  # (pymysql.cursors.DictCursor)
        num = cursor.execute(sql, args)

        return cursor, num

    @staticmethod
    def close(conn,cursor=None):
        # if conn:
        #     conn.close()
        if cursor:
            cursor.close()

    def write_data(self,conn,proto,src_ip,dst_ip,sport,dport):
        cursor = None,
        try:
            sql = "insert into traffic_recognition_high_risk_traffic(proto,src_ip,dst_ip,sport,dport) values (%s, %s, %s, %s, %s)"
            cursor, num = self.execute(sql, args=(proto,src_ip,dst_ip,sport,dport), conn=conn)
        except Exception as e:
            conn.rollback()
            raise Exception("insert failed!")
        finally:
            conn.commit()
            DBHelper.close(conn,cursor=cursor)


    def  delete_all(self,conn):
        cursor = None
        try:
            sql = "delete from traffic_recognition_high_risk_traffic"
            cursor, num = self.execute(sql, conn=conn)
        except Exception as e:
            conn.rollback()
            raise Exception("delete failed!")
        finally:
            conn.commit()
            DBHelper.close(conn, cursor=cursor)

    def read_data(self,id,conn):
        sql = "select * from  traffic_recognition_high_risk_traffic where id > " + str(id)
        cursor = None
        try:
            cursor, num = self.execute(sql, conn=conn)
            values = cursor.fetchall()
        except Exception as e:
            raise Exception("read failed!")
        finally:
            DBHelper.close(conn,cursor=cursor)
        return values
    def change_auto(self,conn):
        cursor = None
        try:
            sql = "alter table  traffic_recognition_high_risk_traffic auto_increment=1"
            cursor, num = self.execute(sql, conn=conn)
        except Exception as e:
            conn.rollback()
            raise Exception("change_auto failed")
        finally:
            conn.commit()
            DBHelper.close(conn, cursor=cursor)

db = DBHelper()

def theard_write(proto,src_ip,dst_ip,sport,dport):
   t = threading.Thread(target=db.write_data,args=(DBHelper.get_con(),proto,src_ip,dst_ip,sport,dport,))
   t.start()
   return


def read(id):
    values = db.read_data(id,DBHelper.get_con())
    return values

def delete():
    db.delete_all(DBHelper.get_con())
    return

def set_auto():
    db.change_auto(DBHelper.get_con())
    return
def db_close():
    DBHelper.get_con().close()
    return
import pymysql

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
    def close(conn=None, cursor=None):
        if conn:
            conn.close()
        if cursor:
            cursor.close()

    def write_data(self,proto,src_ip,dst_ip,sport,dport,load):
        cursor = None
        conn = self.get_con()
        try:
            sql = "insert into traffic_recognition_high_risk_traffic(id,proto,src_ip,dst_ip,sport,dport,load) values (%d,%d, %s, %s, %d, %d, %s)"
            cursor, num = self.execute(sql, args=(proto,src_ip,dst_ip,sport,dport,load), conn=conn)
        except Exception as e:
            conn.rollback()
            raise Exception("insert failed!")
        finally:
            conn.commit()
            DBHelper.close(cursor=cursor)


    def  delete_all(self):
        sql = "delete from traffic_recognition_high_risk_traffic"
        self.execute(sql,conn=self.get_con())


    def read_data(self,id):
        sql = "select proto,src_ip,dst_ip,sport,dport,load from  traffic_recognition_high_risk_traffic where id = " + id
        cursor = None
        try:
            cursor, num = self.execute(sql, conn=self.get_con())
            values = cursor.fetchall()
        except Exception as e:
            raise Exception("read failed!")
        finally:
            DBHelper.close(cursor=cursor)
        return values



    def get_files(self):
        sql = "select data_name from app_datas"
        cursor = None
        try:
            cursor, num = self.execute(sql, self.get_con())
            values = cursor.fetchall()
        except Exception as e:
            raise Exception("read files name failed!")
        finally:
            DBHelper.close(cursor=cursor)
        return values

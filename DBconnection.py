import cx_Oracle
from impala.dbapi import connect

class DBConnection():
    def odsConnection(self,dbinfo):
        conn=cx_Oracle.connect(dbinfo)
        cursor=conn.cursor()
        return conn,cursor
        
    def hiveConnection(self,host,port,user,password,database):
        try:
            conn=connect(host=host,port=port,auth_mechanism='PLAIN',user=user,password=password,database=database)
            cursor=conn.cursor()
            print('链接数据库成功！')
            return conn,cursor
            
        except Exception:
            print('链接数据库失败！')
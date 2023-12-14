import requests
import psycopg2
#import password as pw  #測試用(.ipynb)
import socket
import os

myip = socket.gethostbyname(socket.gethostname())
if '172.17.0.0' <= myip <= '172.17.255.255':
    from . import password as pw  #from 從當前目錄 import package #相對路徑
    print("本機")
    DATABASE = pw.DATABASE
    USER = pw.USER
    PASSWORD = pw.PASSWORD
    HOST = pw.HOST
else:
    DATABASE = os.environ['DATABASE']
    USER = os.environ['USER']
    PASSWORD = os.environ['PASSWORD']
    HOST = os.environ['HOST']

print(f'我的ip是{myip}')

def lastest_datetime_data()->list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()              
    sql = '''
        select a.站點名稱, a.更新時間, a.行政區, a.地址, a.總車輛數, a.可借, a.可還  
        from 台北市youbike a join (select distinct 站點名稱,max(更新時間) 更新時間
        from 台北市youbike group by 站點名稱) b
        on a.更新時間=b.更新時間 and a.站點名稱=b.站點名稱
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return rows

def search_sitename(word:str) -> list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
        SELECT 站點名稱, 更新時間, 行政區, 地址, 總車輛數, 可借, 可還
        FROM 台北市youbike
        WHERE (更新時間,站點名稱) IN (
	          SELECT MAX(更新時間),站點名稱
	          FROM 台北市youbike
	            GROUP BY 站點名稱
        )  AND 站點名稱 like %s
        '''
    cursor.execute(sql,[f'%{word}%'])
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


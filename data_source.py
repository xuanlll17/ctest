import requests
import csv
import sqlite3
import os


def __download_credit_data() -> csv:

    '''地區別代碼【KLC: 基隆市, TPE: 臺北市, NTP: 新北市, TYC: 桃園市, HCC: 新竹市, HCH: 新竹縣, MLH: 苗栗縣, TCC: 臺中市, CHH: 彰化縣, NTH: 南投縣, YUH: 雲林縣, CYC: 嘉義市, CYH: 嘉義縣, TNC: 臺南市, KHC: 高雄市, PTH: 屏東縣, TTH: 臺東縣, HLH: 花蓮縣, YIH: 宜蘭縣, PHH: 澎湖縣, KMH: 金門縣, LCH: 連江縣, TWN: 臺灣, X1: 無縣市, LCSUM: 六都十六縣, MCT: 六都, LOC: 十六縣】

    Available values : KLC, TPE, NTP, TYC, HCC, HCH, MLH, TCC, CHH, NTH, YUH, CYC, CYH, TNC, KHC, PTH, TTH, HLH, YIH, PHH, KMH, LCH, TWN, X1, LCSUM, MCT, LOC

    產業類別代碼【FD: 食品餐飲類, CT: 服飾類, LG: 住宿類, TR: 交通類, EE: 文教康樂類, DP: 百貨類, X2: 無產業, OT: 其他類, ALL: 全部產業, IDSUM: 各產業類】
    Available values : FD, CT, LG, TR, EE, DP, X2, OT, ALL, IDSUM

    1:男性 2:女性
    63000000: 臺北市 64000000: 高雄市 65000000: 新北市 66000000: 臺中市 67000000: 臺南市 68000000: 桃園市
    10002000: 宜蘭縣 10004000: 新竹縣 10005000: 苗栗縣 10007000: 彰化縣 10008000: 南投縣 10009000: 雲林縣
    10010000: 嘉義縣 10020000: 嘉義市 10013000: 屏東縣 10014000: 臺東縣 10015000: 花蓮縣 10016000: 澎湖縣
    10017000: 基隆市 10018000: 新竹市 09020000: 金門縣 09007000: 連江縣

    '''


'''
area = ['KLC', 'TPE', 'NTP', 'TYC', 'HCC', 'HCH', 'MLH', 'TCC', 'CHH', 'NTH', 'YUH', 'CYC', 'CYH', 'TNC', 'KHC',' PTH', 'TTH', 'HLH', 'YIH', 'PHH', 'KMH', 'LCH', 'X1',' LCSUM', 'MCT', 'LOC']

industry = ['FD', 'CT', 'LG', 'TR', 'EE', 'DP', 'X2', 'OT', ' IDSUM', 'ALL']
'''
area = ['KLC', 'TPE', 'NTP', 'TYC', 'HCC', 'HCH', 'MLH', 'TCC', 'CHH', 'NTH', 'YUH', 'CYC', 'CYH', 'TNC', 'KHC',' PTH', 'TTH', 'HLH', 'YIH', 'PHH', 'KMH', 'LCH', 'X1',' LCSUM', 'MCT', 'LOC']

industry = ['FD', 'CT', 'LG', 'TR', 'EE', 'DP', 'X2', 'OT', ' IDSUM', 'ALL']
DataType = ['sex', 'job', 'incom', 'eduction']

# 兩性消費

for A in industry:
    for B in area:
        sex_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C01/sexconsumption/{B}/{A}"
        response_sex = requests.request("GET", sex_url)
        if len(response_sex.text) == 0:
            continue
        with open(f'./sex/job{B}_{A}.csv', 'wb') as file:
            file.write(response_sex.content)
            file.close()
print('性別消費資料讀取成功')


for E in industry:
    for F in area:
        job_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C04/jobsconsumption/{F}/{E}"
        response_job = requests.request("GET", job_url)
        if len(response_job.text) == 0:
            continue
        with open(f'./job/job{F}_{E}.csv', 'wb') as file:
            file.write(response_job.content)
            file.close()
print('職業類別消費資料讀取成功')

# 各年收入族群消費樣態資料(V)
for G in industry:
    for H in area:
        incom_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C03/incomegroupsconsumption/{H}/{G}"
        response_incom = requests.request("GET", incom_url)
        if len(response_incom.text) == 0:
            continue
        with open(f'./incom/incom{H}_{G}.csv', 'wb') as file:
            file.write(response_incom.content)
            file.close()
print('收入類別消費資料讀取成功')

# 各教育程度消費樣態資料(V)
for I in industry:
    for J in area:
        education_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C05/educationconsumption/{J}/{I}"
        response_education = requests.request("GET", education_url)
        if len(response_education.text) == 0:
            continue
        with open(f'./education/education{J}_{I}.csv', 'wb') as file:
            file.write(response_education.content)
            file.close()
print('教育程度資料讀取成功')


#===============建立資料庫欄位==================
def __create_table(conn:sqlite3.Connection):       
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE  IF NOT EXISTS 兩性類別消費資料(
            "id"	INTEGER,
            "年月"	TEXT NOT NULL,
            "地區"	TEXT NOT NULL,
            "產業別"	TEXT NOT NULL,
            "性別"	INTEGER NOT NULL,
            "信用卡交易筆數"	INTEGER,
            "信用卡交易金額[新台幣]"	INTEGER,            
            PRIMARY KEY("id" AUTOINCREMENT),
            UNIQUE(年月,性別) ON CONFLICT REPLACE
        );
        '''
    )
    conn.commit()
    cursor.close
    print("兩性類別資料庫建立成功")

    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE  IF NOT EXISTS 職業類別消費資料(
            "id"	INTEGER,
            "年月"	TEXT NOT NULL,
            "地區"	TEXT NOT NULL,
            "產業別"	TEXT NOT NULL,
            "職業類別"	INTEGER NOT NULL,
            "信用卡交易筆數"	INTEGER,
            "信用卡交易金額[新台幣]"	INTEGER,            
            PRIMARY KEY("id" AUTOINCREMENT),
            UNIQUE(年月,職業類別) ON CONFLICT REPLACE
        );
        '''
    )
    conn.commit()
    cursor.close
    print("職業類別資料庫建立成功")
        
    
    cursor = conn.cursor()
    cursor.execute(
            '''
            CREATE TABLE  IF NOT EXISTS 收入類別消費資料(
                "id"	INTEGER,
                "年月"	TEXT NOT NULL,
                "地區"	TEXT NOT NULL,
                "產業別"	TEXT NOT NULL,
                "收入類別"	INTEGER NOT NULL,
                "信用卡交易筆數"	INTEGER,
                "信用卡交易金額[新台幣]"	INTEGER,            
                PRIMARY KEY("id" AUTOINCREMENT),
                UNIQUE(年月,收入類別) ON CONFLICT REPLACE
            );
            '''
        )
    conn.commit()
    cursor.close
    print("收入類別資料庫建立成功")

    cursor = conn.cursor()
    cursor.execute(
            '''
            CREATE TABLE  IF NOT EXISTS 教育程度類別消費資料(
                "id"	INTEGER,
                "年月"	TEXT NOT NULL,
                "地區"	TEXT NOT NULL,
                "產業別"	TEXT NOT NULL,
                "教育程度類別"	INTEGER NOT NULL,
                "信用卡交易筆數"	INTEGER,
                "信用卡交易金額[新台幣]"	INTEGER,            
                PRIMARY KEY("id" AUTOINCREMENT),
                UNIQUE(年月,教育程度類別) ON CONFLICT REPLACE
            );
            '''
        )
    conn.commit()
    cursor.close
    print("教育程度類別消費建立成功")
#--------------------------------------------------

#===============建立讀取資料欄位==================

def __insert_data(conn:sqlite3.Connection,values:())->None:
    
    cursor = conn.cursor('兩性類別消費資料.db')    
    sql=   '''
    REPLACE INTO '兩性類別消費資料'(年月,地區,產業別,性別,信用卡交易筆數,信用卡交易金額[新台幣])VALUES(?,?,?,?,?,?)        '''    
    cursor.execute(sql,values)
    conn.commit()
    cursor.close()

    cursor = conn.cursor('職業類別消費資料.db')    
    sql=   '''
    REPLACE INTO '職業類別消費資料'(年月,地區,產業別,職業類別,信用卡交易筆數,信用卡交易金額[新台幣])VALUES(?,?,?,?,?,?)        '''    
    cursor.execute(sql,values)
    conn.commit()
    cursor.close()

    cursor = conn.cursor('收入類別消費資料.db')    
    sql=   '''
    REPLACE INTO '收入類別消費資料'(年月,地區,產業別,收入類別,信用卡交易筆數,信用卡交易金額[新台幣])VALUES(?,?,?,?,?,?)        '''    
    cursor.execute(sql,values)  
    conn.commit()
    cursor.close()

    cursor = conn.cursor('教育程度類別消費資料.db')    
    sql=   '''
    REPLACE INTO '教育程度類別消費資料'(年月,地區,產業別,教育程度類別,信用卡交易筆數,信用卡交易金額[新台幣])VALUES(?,?,?,?,?,?)        '''    
    cursor.execute(sql,values)  
    conn.commit()
    cursor.close()
#--------------------------------------------------


#===============下載並更新資料==================

def updata_sqlite_data()->None:
    
    '''
    下載,並更新資料庫
    '''
    data = __download_credit_data()
    conn = sqlite3.connect("兩性類別消費資料.db")
    __create_table(conn) 
    path = "./sex"
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            file_directory = os.path.join(path, filename)
            file = open(file_directory)
            reader = csv.reader(file)
            for item in reader:
                __insert_data(conn,(item('年月'),item('地區'),item('產業別'),item('性別'),item('信用卡交易筆數'),item('信用卡交易金額[新台幣]')))
            conn.close()
        else:
            continue 
    
    conn = sqlite3.connect("職業類別消費資料.db")
    __create_table(conn) 
    path = "./sex"
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            file_directory = os.path.join(path, filename)
            file = open(file_directory)
            reader = csv.reader(file)
            for item in reader:
                __insert_data(conn,(item('年月'),item('地區'),item('產業別'),item('職業類別'),item('信用卡交易筆數'),item('信用卡交易金額[新台幣]')))
            conn.close()
        else:
            continue
        
    conn = sqlite3.connect("收入類別消費資料.db")
    __create_table(conn) 
    path = "./sex"
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            file_directory = os.path.join(path, filename)
            file = open(file_directory)
            reader = csv.reader(file)
            for item in reader:
                __insert_data(conn,(item('年月'),item('地區'),item('產業別'),item('收入類別'),item('信用卡交易筆數'),item('信用卡交易金額[新台幣]')))
            conn.close()
        else:
            continue 

    conn = sqlite3.connect("教育程度類別消費資料.db")
    __create_table(conn) 
    path = "./sex"
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            file_directory = os.path.join(path, filename)
            file = open(file_directory)
            reader = csv.reader(file)
            for item in reader:
                __insert_data(conn,(item('年月'),item('地區'),item('產業別'),item('教育程度類別'),item('信用卡交易筆數'),item('信用卡交易金額[新台幣]')))
            conn.close()
        else:
            continue
    

#--------------------------------------------------

import requests
import os
import csv
import sqlite3
import pandas as pd

__all__=['csv_to_database']

'''
執行前,需先建立datasource資料夾,底下建立age/incom/education/job/sex資料夾
'''
# ---------下載資料---------#
def __download_credit_data() -> csv:
    area = [
        "KLC",
        "TPE",
        "NTP",
        "TYC",
        "HCC",
        "HCH",
        "MLH",
        "TCC",
        "CHH",
        "NTH",
        "YUH",
        "CYC",
        "CYH",
        "TNC",
        "KHC",
        "PTH",
        "TTH",
        "HLH",
        "YIH",
        "PHH",
        "KMH",
        "LCH",
        "X1",
        "LCSUM",
        "MCT",
        "LOC",
    ]
    area_code = {
        "63000000": "臺北市",
        "64000000": "高雄市",
        "65000000": "新北市",
        "66000000": "臺中市",
        "67000000": "臺南市",
        "68000000": "桃園市",
        "10002000": "宜蘭縣",
        "10004000": "新竹縣",
        "10005000": "苗栗縣",
        "10007000": "彰化縣",
        "10008000": "南投縣",
        "10009000": "雲林縣",
        "10010000": "嘉義縣",
        "10020000": "嘉義市",
        "10013000": "屏東縣",
        "10014000": "臺東縣",
        "10015000": "花蓮縣",
        "10016000": "澎湖縣",
        "10017000": "基隆市",
        "10018000": "新竹市",
        "9020000": "金門縣",
        "9007000": "連江縣",
    }
    industry = ["FD", "CT", "LG", "TR", "EE", "DP", "X2", "OT", " IDSUM", "ALL"]
    DataType = ["sex", "job", "incom", "education", "age"]
    sex = ["M", "F"]
    sex_code = {"1": "男性", "2": "女性"}

    #---兩性消費---#
    for A in industry:
        for B in area:
            sex_url = (
                f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C01/sexconsumption/{B}/{A}"
            )
            response_sex = requests.request("GET", sex_url)
            if len(response_sex.text) == 0:   #若csv無資料則繼續,不下載
                continue
            with open(f"./datasource/sex/sex{B}_{A}.csv", "wb") as file:
                file.write(response_sex.content)
    print("性別消費資料讀取成功")

    #---各職業類別消費---#
    for E in industry:
        for F in area:
            job_url = (
                f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C04/jobsconsumption/{F}/{E}"
            )
            response_job = requests.request("GET", job_url)
            if len(response_job.text) == 0:
                continue
            with open(f"./datasource/job/job{F}_{E}.csv", "wb") as file:
                file.write(response_job.content)
    print("職業類別消費資料讀取成功")

    #---各年收入族群消費---#
    for G in industry:
        for H in area:
            incom_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C03/incomegroupsconsumption/{H}/{G}"
            response_incom = requests.request("GET", incom_url)
            if len(response_incom.text) == 0:
                continue
            with open(f"./datasource/incom/incom{H}_{G}.csv", "wb") as file:
                file.write(response_incom.content)
    print("收入類別消費資料讀取成功")

    #---各教育程度消費---#
    for I in industry:
        for J in area:
            education_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C05/educationconsumption/{J}/{I}"
            response_education = requests.request("GET", education_url)
            if len(response_education.text) == 0:
                continue
            with open(f"./datasource/education/education{J}_{I}.csv", "wb") as file:
                file.write(response_education.content)
    print("教育程度資料讀取成功")

    #---兩性X各年齡層消費---#
    for A in industry:
        for B in area:
            for C in sex:
                age_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C11/GenderAgeGroup/{B}/{A}/{C}"
                response_age = requests.request("GET", age_url)
                if len(response_age.text) == 0:
                    continue
                folder_path = "./datasource/age/"
                file_name = f"age{B}_{A}_{C}.csv"
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "wb") as file:
                    file.write(response_age.content)
    print("年齡層消費資料讀取成功")

    # ---------合併csv---------#
    for item in DataType:
        path = f"./datasource/{item}/"  #要合併資料的路徑位置
        #取得指定路徑下所有的csv
        csv_files = [file for file in os.listdir(path) if file.endswith(".csv")]
        #建立空dataframe儲存合併資料
        merged_data = pd.DataFrame()
        #讀取csv資料內容合併到merged_data
        for file in csv_files:
            file_path = os.path.join(path, file)  #將路徑(path)與file連接,建立完整路徑位置
            data = pd.read_csv(file_path)  #讀取csv內容,並儲存在dataframe(data)中
            #pd.concat->將data與merged_data連接, ignore_index=True->忽略原始的index欄位(索引值),改採用合併後自動產生的index(索引值)
            merged_data = pd.concat([merged_data, data], ignore_index=True) 
        merged_data.drop_duplicates(inplace=True)  #在合併前去除重複的值
        merged_data.to_csv(f"{item}.csv", index=False)  #將merged_data寫入csv, index=False->不寫入dataframe的index(索引值)
        print(f"{item}.csv建立成功")

        with open(f"./{item}.csv", "r", encoding="UTF-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)  #使用DictReader+csv_reader.fieldnames->傳回csv的欄位名稱
            fieldnames = csv_reader.fieldnames  #取得欄位名稱

            #將格式轉換完畢的資料內容寫入csv中
            with open(f"./{item}_trans.csv", "w", encoding="utf-8", newline="") as file:  
                new_fieldnames = ["年", "月"] + fieldnames[1:]  #將年,月寫在欄位最前面, fieldnames[1:]->取得從2到最後的欄位名稱(原始fieldnames中年月是在第一個,所以從第二個開始)
                csv_writer = csv.DictWriter(file, fieldnames=new_fieldnames)
                csv_writer.writeheader()  #寫入第一列的欄位名稱

                for row in csv_reader:
                    #---找不到對應的值，則保持原本的值---#
                    row["地區"] = area_code.get(row["地區"], row["地區"])

                    if "性別" in fieldnames:
                        row["性別"] = sex_code.get(row["性別"], row["性別"])

                    #將原資料中的年月,拆開成年 月,ex:201401
                    year = row["年月"][:4]  #取出值,由開頭到3, 0-3, 2014
                    month = row["年月"][4:] #取出值,由4到最後, 4-5, 01
                    new_row = {"年": year, "月": month, "地區": row["地區"]}

                    if "性別" in fieldnames:  #找尋csv中有性別欄位的資料
                        new_row["性別"] = row["性別"]

                    new_row.update(row)  #將dictionary(new_row)更新並合併到另一個dictionary(row)
                    del new_row["年月"]  #刪除原csv裡的年月
                    csv_writer.writerow(new_row)  #將new_row資料寫入

                print(f"{item}_trans.csv建立成功")


# ---------輸入資料---------#
def csv_to_database() -> None:
    __download_credit_data()
    conn = sqlite3.connect("creditcard.db")
    DataType = ["sex", "job", "incom", "education", "age"]
    for item in DataType:
        file = f"./{item}_trans.csv"
        df = pd.read_csv(file)

        df.rename(columns={"信用卡交易金額[新台幣]": "信用卡金額"}, inplace=True)  #inplace=True->直接修改原始dataframe
        df.to_sql(item, conn, if_exists="replace", index=False)  #寫入資料庫中,if_exists="replace"->若table已經存在將其替換, index=False->不將dataframe的索引值寫入

    conn.close()



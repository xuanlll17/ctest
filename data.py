import requests
import os
import csv
import sqlite3
import pandas as pd


# ---------下載資料---------#
def __download_credit_data() -> csv:
    area = ["KLC","TPE","NTP","TYC","HCC","HCH","MLH","TCC","CHH","NTH","YUH","CYC","CYH","TNC","KHC","PTH","TTH","HLH","YIH","PHH","KMH","LCH","X1","LCSUM","MCT","LOC"]
    industry = ["FD", "CT", "LG", "TR", "EE", "DP", "X2", "OT", " IDSUM", "ALL"]
    DataType = ["sex", "job", "incom", "education", "age"]
    sex = ["M", "F"]

    # 兩性消費
    for A in industry:
        for B in area:
            sex_url = (
                f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C01/sexconsumption/{B}/{A}"
            )
            response_sex = requests.request("GET", sex_url)
            if len(response_sex.text) == 0:
                continue
            with open(f"./datasource/sex/job{B}_{A}.csv", "wb") as file:
                file.write(response_sex.content)
                file.close()
    print("性別消費資料讀取成功")

    # 各職業類別消費樣態資料
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
                file.close()
    print("職業類別消費資料讀取成功")

    # 各年收入族群消費樣態資料(V)
    for G in industry:
        for H in area:
            incom_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C03/incomegroupsconsumption/{H}/{G}"
            response_incom = requests.request("GET", incom_url)
            if len(response_incom.text) == 0:
                continue
            with open(f"./datasource/incom/incom{H}_{G}.csv", "wb") as file:
                file.write(response_incom.content)
                file.close()
    print("收入類別消費資料讀取成功")

    # 各教育程度消費樣態資料(V)
    for I in industry:
        for J in area:
            education_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C05/educationconsumption/{J}/{I}"
            response_education = requests.request("GET", education_url)
            if len(response_education.text) == 0:
                continue
            with open(f"./datasource/education/education{J}_{I}.csv", "wb") as file:
                file.write(response_education.content)
                file.close()
    print("教育程度資料讀取成功")

    # 兩性X各年齡層消費
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
                    file.close()
    print("年齡層消費資料讀取成功")

    # ---------合併csv---------#
    for D in DataType:
        path = f"./datasource/{D}/"
        csv_files = [file for file in os.listdir(path) if file.endswith(".csv")]
        merged_data = pd.DataFrame()
        for file in csv_files:
            file_path = os.path.join(path, file)
            data = pd.read_csv(file_path)

            data["年月"] = data["年月"].astype(str)

            data["年"] = data["年月"].str[:4]
            data["月"] = data["年月"].str[4:]

            columns = ["年", "月"] + [
                col for col in data.columns if col not in ["年", "月", "年月"]
            ]
            data = data[columns]

            merged_data = pd.concat([merged_data, data], ignore_index=True)
        merged_data.to_csv(f"{D}.csv", index=False)
        print(f"{D}.csv建立成功")



# ---------輸入資料---------#
def csv_to_database(conn: sqlite3.Connection) -> None:
    DataType = ["sex", "job", "incom", "education", "age"]
    for item in DataType:
        file = f"./{item}.csv"
        df = pd.read_csv(file)
        df.to_sql(item, conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()


def main() -> None:
    __download_credit_data()
    conn = sqlite3.connect("creditcard.db")

    csv_to_database(conn)


if __name__ == "__main__":
    main()

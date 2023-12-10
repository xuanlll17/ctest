import requests
import psycopg2

# import password as pw
from . import password as pw
import pandas as pd
import csv


def __download_creditcard_data():
    edu_url = (
        "https://bas.nccc.com.tw/nccc-nop/OpenAPI/C05/educationconsumption/MCT/ALL"
    )
    response = requests.request("GET", edu_url)
    with open(f"./six_e.csv", "wb") as file:
        file.write(response.content)
    print("職業類別消費資料讀取成功")


def trans_data():
    area_code = {
        "63000000": "臺北市",
        "64000000": "高雄市",
        "65000000": "新北市",
        "66000000": "臺中市",
        "67000000": "臺南市",
        "68000000": "桃園市",
    }

    df = pd.read_csv("six_e.csv")
    df["年月"] = df["年月"].astype(str)
    df["年"] = df["年月"].str[:4]
    df["月"] = df["年月"].str[4:]
    df = df[(df["產業別"] != "其他") & (df["教育程度類別"] != "其他")]
    df = df[df["年"] == "2023"]
    df["地區"] = df["地區"].apply(lambda x: area_code.get(x, x))
    df = df.drop(columns=["年月"])
    df = df[["年", "月"] + [col for col in df.columns if col not in ["年", "月"]]]
    df = df.rename(columns={"信用卡交易金額[新台幣]": "信用卡交易金額"})
    df.to_csv("six_e.csv", index=False, encoding="utf-8")

    with open("six_e.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        fieldnames = csv_reader.fieldnames
        with open("six_e_2023.csv", "w", encoding="utf-8", newline="") as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()

            for row in csv_reader:
                row["地區"] = area_code.get(row["地區"], row["地區"])

                new_row = {"地區": row["地區"]}
                new_row.update(row)
                csv_writer.writerow(new_row)


# ---------------create sql table----------------#
def __create_table(conn) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS education(
            "id" SERIAL,
            "年" INTEGER NOT NULL,
            "月" INTEGER NOT NULL,
            "地區" TEXT NOT NULL,
            "產業別" TEXT NOT NULL,
            "教育程度"	TEXT NOT NULL,
            "信用卡交易筆數" BIGINT NOT NULL,
            "信用卡交易金額" BIGINT NOT NULL,
            PRIMARY KEY("id")
        );
		"""
    )
    conn.commit()
    cursor.close()


# -----------------insert data-------------------#
def __insert_data(conn, values: list[any]) -> None:
    cursor = conn.cursor()
    sql = """
        INSERT INTO education (年, 月, 地區, 產業別, 教育程度, 信用卡交易筆數, 信用卡交易金額) 
        VALUES(%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()


def update_render_data() -> None:
    # ---------------連線到postgresql----------------#
    conn = psycopg2.connect(
        database=pw.DATABASE,
        user=pw.USER,
        password=pw.PASSWORD,
        host=pw.HOST,
        port="5432",
    )

    __create_table(conn)
    with open("six_e_2023.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for item in csv_reader:
            __insert_data(
                conn,
                values=[
                    item["年"],
                    item["月"],
                    item["地區"],
                    item["產業別"],
                    item["教育程度類別"],
                    item["信用卡交易筆數"],
                    item["信用卡交易金額"],
                ],
            )

    conn.close()


def lastest_datetime_data() -> list[tuple]:
    conn = psycopg2.connect(
        database=pw.DATABASE,
        user=pw.USER,
        password=pw.PASSWORD,
        host=pw.HOST,
        port="5432",
    )
    cursor = conn.cursor()
    sql = """
        select 年, 月, 地區, 產業別, 教育程度, 信用卡交易筆數, 信用卡交易金額  
        from education
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return rows

    # def main():
    __download_creditcard_data()
    trans_data()
    update_render_data()

    # if __name__ == "__main__":
    main()

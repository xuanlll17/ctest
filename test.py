import requests
import os
import csv
import sqlite3
import pandas as pd

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
        with open(f'./datasource/sex/job{B}_{A}.csv', 'wb') as file:
            file.write(response_sex.content)
            file.close()
print('性別消費資料讀取成功')

# 各職業類別消費樣態資料
for E in industry:
    for F in area:
        job_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C04/jobsconsumption/{F}/{E}"
        response_job = requests.request("GET", job_url)
        if len(response_job.text) == 0:
            continue
        with open(f'./datasource/job/job{F}_{E}.csv', 'wb') as file:
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
        with open(f'./datasource/incom/incom{H}_{G}.csv', 'wb') as file:
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
        with open(f'./datasource/education/education{J}_{I}.csv', 'wb') as file:
            file.write(response_education.content)
            file.close()
print('教育程度資料讀取成功')
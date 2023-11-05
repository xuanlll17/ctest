import requests
import csv


#處理中心金額及筆數資料(V)
sales_url = "https://bas.nccc.com.tw/nccc-nop/OpenAPI/A02/SalesVolumeand"   
response_sale = requests.request("GET",sales_url) 	
with open('sales.csv', 'wb') as file:
	file.write(response_sale.content)
	file.close()

#本中心會員機構發卡量資料(V)
cards = "https://bas.nccc.com.tw/nccc-nop/OpenAPI/A03/StatisticCardsCirculation"   
response_cards = requests.request("GET",cards)
with open('cards.csv', 'wb') as file:
	file.write(response_cards.content)
	file.close()

#本中心簽帳端末機裝機臺數資料(V)
pos = "https://bas.nccc.com.tw/nccc-nop/OpenAPI/A04/NumberPOS"
response_pos = requests.request("GET",pos)
data = response_pos.text
with open("pos.csv", "w", newline= '', encoding="utf-8") as file:
    file.write(data)



#本中心特約商店型態及比例資料(V)
Merchant_type = "https://bas.nccc.com.tw/nccc-nop/OpenAPI/A06/MerchantCategoriesPercentage"   
response_Merchant_type= requests.request("GET",Merchant_type)
with open('Merchant_type.csv', 'wb') as file:
	file.write(response_Merchant_type.content)
	file.close()

#本中心收單特約商店數資料(V)
Merchants = "https://bas.nccc.com.tw/nccc-nop/OpenAPI/A09/NumberNCCCAcquiredMerchants"   
response_Merchants = requests.request("GET",Merchants)
with open('Merchants.csv', 'wb') as file:
	file.write(response_Merchants.content)
	file.close()


#本中心特約商店分佈比例資料(V)
Merchant_area = "https://bas.nccc.com.tw/nccc-nop/OpenAPI/A10/NetworkNCCCServiceEstablishments"   
response_Merchant_area = requests.request("GET",Merchant_area)
with open('Merchant_area.csv', 'wb') as file:
	file.write(response_Merchant_area.content)
	file.close()


#各地區別消費樣態資料(V)
'''地區別代碼【KLC: 基隆市, TPE: 臺北市, NTP: 新北市, TYC: 桃園市, HCC: 新竹市, HCH: 新竹縣, MLH: 苗栗縣, TCC: 臺中市, CHH: 彰化縣, NTH: 南投縣, YUH: 雲林縣, CYC: 嘉義市, CYH: 嘉義縣, TNC: 臺南市, KHC: 高雄市, PTH: 屏東縣, TTH: 臺東縣, HLH: 花蓮縣, YIH: 宜蘭縣, PHH: 澎湖縣, KMH: 金門縣, LCH: 連江縣, TWN: 臺灣, X1: 無縣市, LCSUM: 六都十六縣, MCT: 六都, LOC: 十六縣】

Available values : KLC, TPE, NTP, TYC, HCC, HCH, MLH, TCC, CHH, NTH, YUH, CYC, CYH, TNC, KHC, PTH, TTH, HLH, YIH, PHH, KMH, LCH, TWN, X1, LCSUM, MCT, LOC'''


area = ['KLC', 'TPE', 'NTP', 'TYC', 'HCC', 'HCH', 'MLH', 'TCC', 'CHH', 'NTH', 'YUH', 'CYC', 'CYH', 'TNC', 'KHC',' PTH', 'TTH', 'HLH', 'YIH', 'PHH', 'KMH', 'LCH', 'X1',' LCSUM', 'MCT', 'LOC']
for A in area :
    area_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/B02/Location/{A}"   
    response_area = requests.request("GET",area_url)
    if len(response_area.text) == 0:
        continue
    with open(f'area_{A}.csv', 'wb') as file:
        file.write(response_area.content)
        file.close()



        
#各產業別消費樣態資料(V)
'''產業類別代碼【FD: 食品餐飲類, CT: 服飾類, LG: 住宿類, TR: 交通類, EE: 文教康樂類, DP: 百貨類, X2: 無產業, OT: 其他類, ALL: 全部產業, IDSUM: 各產業類】'''

industry = ['FD', 'CT', 'LG', 'TR', 'EE', 'DP', 'X2', 'OT', ' IDSUM', 'ALL']
for B in industry :
    industry_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/B01/Industry/{B}"   
    response_industry = requests.request("GET",industry_url)
    if len(response_industry.text) == 0:
        continue
    with open(f'industry_{B}.csv', 'wb') as file:
        file.write(response_industry.content)
        file.close()

#兩性消費
for C in industry :
    sexSum_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C01/sexconsumption/TWN/{C}"   
    response_sexSum = requests.request("GET",sexSum_url)
    if len(response_sexSum.text) == 0:
        continue
    with open(f'sexSum_{C}.csv', 'wb') as file:
        file.write(response_sexSum.content)

#各職業類別消費樣態資料(V)
jobSum_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C04/jobsconsumption/TWN/ALL"   
response_jobSum = requests.request("GET",jobSum_url)
with open(f'jobSum.csv', 'wb') as file:
	file.write(response_jobSum.content)
	file.close()

#各年收入族群消費樣態資料(V)
incomSum_url = f"https://bas.nccc.com.tw/nccc-nop/OpenAPI/C03/incomegroupsconsumption/TWN/ALL"   
response_incomSum = requests.request("GET",incomSum_url)
with open(f'incomSum.csv', 'wb') as file:
	file.write(response_incomSum.content)
	file.close()

import requests
import pandas as pd
import xml.etree.ElementTree as ET
import os
import time

# 아파트 실거래가 검색
def getRtData(LAWD_CD, DEAL_YMD):
    #LAWD_CD는  지역번호 (천안시 서북그 : 44133)
    #DEAL_YMD는 날짜
    key = 'moueEHwKWvcAlOWx8KbuFkzCwihNexLOFDAFsd%2B5kvMf%2B7OeeC8%2BvhCBZ2UV8MdSZTGf9VsngtjPvjNLcwHTlg%3D%3D'
    url = "	http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?"
    
    payload = "LAWD_CD=" + str(LAWD_CD) + "&" + \
              "DEAL_YMD=" + str(DEAL_YMD) + "&" + \
              "serviceKey=" + key + "&"

    return requests.get(url + payload)

# xml 해석
def get_item(response):
    root = ET.fromstring(response.content)
    item_list = []
    for child in root.find('body').find('items'):
        elements = child.findall('*')
        data = {}
        for element in elements:
            tag = element.tag.strip()
            text = element.text.strip()
            data[tag] = text
        item_list.append(data)
    return item_list

# 지역번호 추출
def get_LAND_CD(LAND_CD):
    codefile = 'C:/Users/c404/Desktop/sangjin/exchange/code.txt'
    code = pd.read_csv(codefile, sep='\t', encoding='cp949')
    code.columns = ['code', 'name', 'is_exist']
    code = code[code['is_exist'] == '존재']
    code['code'] = code['code'].apply(str)
    
    gu_code = code[ (code['name'].str.contains(LAND_CD)) ]
    gu_code = gu_code['code'].reset_index(drop=True)
    gu_code = str(gu_code[0])[0:5]
    return gu_code

# 날짜 선택
def get_date(StartTime, EndTime):

    year = [str("%02d" %(y)) for y in range(int(StartTime), int(EndTime) + 1)]
    month = [str("%02d" %(m)) for m in range(1,13)]
    
    datetime  = ["%s%s" %(y,m) for y in year for m in month]
    return datetime


Land = input("지역 검색\n > ")
Lands = get_LAND_CD(Land)

print(Lands)

Time = get_date(2015, 2024)

item_list = []
for i in Time:
    Response = getRtData(Lands, i)
    item_list += get_item(Response)
items = pd.DataFrame(item_list)
items = items.drop(['거래유형', '동', '등기일자', '매도자', '매수자', '중개사소재지', '해제사유발생일', '해제여부'], axis = 1)
for i in range(0, len(items)):
    a = items.loc[i, '거래금액']
    a = a.replace(',', '')
    items.loc[i, '거래금액'] = a

items.head()
items.to_csv(os.path.join("%s.csv" %Land), index = False, encoding='euc-kr')
# 정보만 가져오는 코드식

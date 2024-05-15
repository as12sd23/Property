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
    url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?"
    
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
    
    gu_code = code[ (code['name'].str.contains(LAND_CD) )]
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

StartTime = input("시작년도 입력(4자리)\n  예시) 2020\n > ")
EndTime= input ("종료년도 입력(4자리)\n  예시) 2024\n > ")
Time = get_date(StartTime, EndTime)

item_list = []
for i in Time:
    Response = getRtData(Lands, Time)
    item_list += get_item(Response)
items = pd.DataFrame(item_list)
items.head()
print(item_list)
items.to_csv(os.path.join("%s-%s~%s.csv" %(Land, Time[0], Time[1])), index = False, encoding='euc-kr')


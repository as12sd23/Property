import requests
import pandas as pd
import xml.etree.ElementTree as ET
import os
import time

class Rigion_Search:

    # 아파트 실거래가 데이터 받기
    def __Get_Data(LAWD_CD, DEAL_YMD):
        key = 'moueEHwKWvcAlOWx8KbuFkzCwihNexLOFDAFsd%2B5kvMf%2B7OeeC8%2BvhCBZ2UV8MdSZTGf9VsngtjPvjNLcwHTlg%3D%3D'
        url = "	http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?"
    
        payload = "LAWD_CD=" + str(LAWD_CD) + "&" + \
                  "DEAL_YMD=" + str(DEAL_YMD) + "&" + \
                  "serviceKey=" + key + "&"

        return requests.get(url + payload)

    # xml 해석
    def __Get_Xml(response):
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

    # 날짜 검색
    def __Get_Date(Start, End):
        year = [str("%02d" %(y)) for y in range(int(Start), int(End) + 1)]
        month = [str("%02d" %(m)) for m in range(1,13)]
    
        datetime  = ["%s%s" %(y,m) for y in year for m in month]
        return datetime

    # 지역 검색
    def __Get_Land(Land):
        codefile = 'C:/Users/c404/Desktop/sangjin/exchange/code.txt'
        code = pd.read_csv(codefile, sep='\t', encoding='cp949')
        code.columns = ['code', 'name', 'is_exist']
        code = code[code['is_exist'] == '존재']
        code['code'] = code['code'].apply(str)

        a = pd.DataFrame(code)
        a.to_csv("code.txt", index = False, sep = '\t')

        gu_code = code[ (code['name'].str.contains(Land)) ]
        gu_code = gu_code['code'].reset_index(drop=True)
        gu_code = str(gu_code[0])[0:5]
        return gu_code

    # 검색
    def Search():
        Land = input("지역 검색\n > ")
        Lands = __Get_Land(Land)

        Time = __Get_Date(2015, 2024)

        _item_ = []
        for i in Time:
            Response = __Get_Data(Lands, i)
            _item_ += __Get_Xml(Response)
        items = pd.DataFrame(_item_)
        items = items.drop(['거래유형', '동', '등기일자', '매도자', '매수자', '중개사소재지', '해제사유발생일', '해제여부'], axis = 1)
        for i in range(0, len(items)):
            a = items.loc[i, '거래금액']
            a = a.replace(',', '')
            items.loc[i, '거래금액'] = a

        items.head()
        items.to_csv(os.path.join("%s.csv" %Land), index = False, encoding='euc-kr')



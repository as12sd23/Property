import requests
import pandas as pd
import datetime
import xml.etree.ElementTree as ET
import os

class Search:
    def __init__(self, location, Year):
        # 지역 코드 생성
        self._get_Land(location)
        # 날짜 생성
        self._get_Date(Year, datetime.datetime.today().year)
        
        for i in self.datetime:
            self.response = self.__get_Data(i)
            self._get_Xml()
            
        # 데이터 프레임 생성 및 저장
        items = pd.DataFrame(self.item_list)
        items = items.drop(['거래유형', '동', '등기일자', '매도자', '매수자', '중개사소재지', '해제사유발생일', '해제여부'], axis = 1)
        for i in range(0, len(items)):
            a = items.loc[i, '거래금액']
            a = a.replace(',', '')
            items.loc[i, '거래금액'] = a

        items.head()
        items.to_csv(os.path.join("%s.csv" %Land), index = False, encoding='euc-kr')
        
    # 아파트 실거래가 데이터 받기
    def _get_Data(self, Time):
        key = "moueEHwKWvcAlOWx8KbuFkzCwihNexLOFDAFsd%2B5kvMf%2B7OeeC8%2BvhCBZ2UV8MdSZTGf9VsngtjPvjNLcwHTlg%3D%3D"
        url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?"
        payload = "LAWD_CD=" + str(self.gu_code) + "&" + \
                  "DEAL_YMD=" + str(Time) + "&" + \
                  "serviceKey=" + key + "&"

        return requests.get(url + payload)

    # 지역 검색
    def _get_Land(self, location):
        if os.path.isfile("C:/Users/c404/Desktop/sangjin/Property-main/Catecori.csv"):
            codefile = "C:/Users/c404/Desktop/sangjin/Property-main/Catecori.csv"
            code = pd.read_csv(codefile, encoding = "cp949")
            item_list = []
            for i in range(0, len(code)):
                data = {}
                data['code'] = code.loc[i, 'code']
                data['name'] = code.loc[i, 'name']
                item_list.append(data)
        else:
            codefile = 'C:/Users/c404/Desktop/sangjin/Property-main/code.txt'
            code = pd.read_csv(codefile, sep='\t', encoding='cp949')
            code.columns = ['code', 'name', 'is_exist']
            code = code[code['is_exist'] == '존재']
            code['code'] = code['code'].apply(str)
            
            a = pd.DataFrame(code)
            a.to_csv(os.path.join("Categori.csv"), index = False, sep = '\t')
            
        self.gu_code = code[ (code['name'].str.contains(location)) ]
        self.gu_code = self.gu_code['code'].reset_index(drop=True)
        self.gu_code = str(self.gu_code[0])[0:5]

    # 날짜 검색
    def _get_Date(self, Start, End):
        year = [str("%02d" %(y)) for y in range(Start, End + 1)]
        month = [str("%02d" %(m)) for m in range(1,13)]
    
        self.datetime  = ["%s%s" %(y,m) for y in year for m in month]

    # xml 해석
    def _get_Xml(self):
        root = ET.fromstring(self.response.content)
        self.item_list = []
        for child in root.find('body').find('items'):
            elements = child.findall('*')
            data = {}
            for element in elements:
                tag = element.tag.strip()
                text = element.text.strip()
                data[tag] = text
            self.item_list.append(data)

a = Search("불당동", 2015)

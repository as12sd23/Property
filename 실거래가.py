import requests
import pandas as pd
import xml.etree.ElementTree as ET


def get_items(response):
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

key = 'OADc2WewAVKTkOGZ%2BLNIqcVFTPXDRYkFpRvF2j4QmNmlN8I84zpQYsY%2BO8Y3D3ozVXrQvC%2B1owwXV6K%2FhhB%2Bpg%3D%3D'
url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?"
code_file = "C:\Users\c404\Desktop\sangjin\실거래가"
base_date = "202001"
gu_code = '44133'

payload = "LAWD_CD=" + gu_code + "&" + \
          "DEAL_YMD=" + base_date + "&" + \
          "serviceKey=" + key + "&"

res = requests.get(url + payload)

print(res)

item = get_items(res)
items = pd.DataFrame(item)
items.head()
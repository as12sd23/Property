import requests
import pandas as pd
import xml.etree.ElementTree as ET
import os
import time

# 해당 지역 정보 추출
def Search(player):
    data = pd.read_csv('C:/Users/c404/Desktop/sangjin/exchange/서북구.csv', encoding='cp949')
    item_list = []
    for i in range(0, len(data)):
        ImsiData = {}
        location = str(data.loc[i, '법정동'])
        
        if len(data.loc[i, '법정동']) > 3:
            location = location[0:3]
        
        if location == player:
            ImsiData['거래금액'] = data.loc[i, '거래금액']
            ImsiData['건축년도'] = data.loc[i, '건축년도']
            ImsiData['업로드'] = data.loc[i, '년']
            ImsiData['법정동'] = data.loc[i, '법정동']
            ImsiData['아파트'] = data.loc[i, '아파트']
            ImsiData['월'] = data.loc[i, '월']
            ImsiData['일'] = data.loc[i, '일']
            ImsiData['면적'] = data.loc[i, '전용면적']
            ImsiData['층'] = data.loc[i, '층']
            item_list.append(ImsiData)
            
    return item_list

# 정보 타입
def 


player = input('원하는 지역(동/읍/면) 입력\n > ')
a = Search(str(player))

for i in a:
    print(i)


'''
해당 지역의 최근 면적 당 가격 분포
해당 지역의 한 아파트 가격 변화량
지역별 구분(기본)

'''
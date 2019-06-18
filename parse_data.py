#__author__='ZHENGT'
# -*- coding: utf-8 -*-
import sys
import requests
import webbrowser
import pandas as pd
import urllib
import json

# reload(sys)
# sys.setdefaultencoding('utf-8')  # Python默认ascii,需要转成utf-8

# 39a9c50af2662024a1b11ccfd9384814 # 微信小程序
# d47b46b4ad38172cd1cce3e274c3a8bc # Web端
# 320f6fdbf528ac0ccd282b666c3cc7fb # Web服务
GAODE_KEY = '320f6fdbf528ac0ccd282b666c3cc7fb'

# 高德地址逆解析
def gaode_regeo(x, y):
    add = []
    location = x+','+y
    parameters = {'location': location, 'key': GAODE_KEY}
    base = 'http://restapi.amap.com/v3/geocode/regeo'
    response = requests.get(base, parameters)
    return response.json()

#高德地图地址解析获取经纬度
def gaode_geo(address):
    parameters = {'key': GAODE_KEY, 'address': address}
    base = 'https://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    return response.json()


def getStaticAmap(lonlat_str, str_city_center):  # <---获取静态高德地图--->
    # sh = '121.472644,31.231706'  # 上海中心点
    #高德地图-->静态地图API地址
    url = r'http://restapi.amap.com/v3/staticmap?location=%s&zoom=10&size=1024*768&key=<YOURKEY>'
    url_1 = url % str_city_center  # 加入城市
    url_amap = url_1+'&markers=mid,0xFF0000,A:'+lonlat_str  # 增加marker点
    print (url_amap)                                                     #
    webbrowser.open(url_amap)  # 打开

def openAmap():
    # https://restapi.amap.com/v3/staticmap?location=116.481485,39.990464&zoom=10&size=750*300&markers=mid,,A:116.481485,39.990464&key=<用户的key>
    base = ''
    parameters ={}
    # url = "https://restapi.amap.com/v3/staticmap?location=116.481485,39.990464&zoom=10&size=750*300&markers=mid,,A:116.481485,39.990464&key="+GAODE_KEY
    url = "https://uri.amap.com/marker?markers=116.480564,39.996374,望京SOHO|116.481590,39.989175,食尚坊美食广场&src=mypage&callnative=0"
    # webbrowser.open(url)
    webbrowser.open("amap.html")



if __name__ == '__main__':  # <---主程序--->
    print(gaode_geo('广州南站'))
    # openAmap()

# __author__='ZHENGT'
# -*- coding: utf-8 -*-
import sys
import requests
import webbrowser
import pandas as pd
import urllib
import json
import csv
import os

import time
import logging
import traceback

# reload(sys)
# sys.setdefaultencoding('utf-8')  # Python默认ascii,需要转成utf-8

# 39a9c50af2662024a1b11ccfd9384814 # 微信小程序
# d47b46b4ad38172cd1cce3e274c3a8bc # Web端
# 320f6fdbf528ac0ccd282b666c3cc7fb # Web服务
GAODE_KEY = '320f6fdbf528ac0ccd282b666c3cc7fb'
ori_csv_file = 'data/railway-stations-2018.csv'
logfile='log/main.log'
formatted_csv_file = 'data/railway-stations-formatted.csv'
# formatted_csv_file = 'data/railway-stations-formatted2.csv'
# formatted_csv_file = 'data/railway-stations-formatted3.csv'

# 高德地址逆解析
def gaode_regeo(x, y):
    add = []
    location = x+','+y
    parameters = {'location': location, 'key': GAODE_KEY}
    base = 'http://restapi.amap.com/v3/geocode/regeo'
    response = requests.get(base, parameters)
    return response.json()

# 高德地图地址解析获取经纬度


def gaode_geo(address):
    parameters = {'key': GAODE_KEY, 'address': address}
    base = 'https://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    return response.json()

# 通过高德地图查找高铁站的GPS位置信息


def csv_parse():
    # file exists
    if os.path.exists(ori_csv_file):
        print("start parsing!")
        logging.info("start parsing")
        startTime = time.time()
        correctcount = 0
        errorcount = 0
        nonecount = 0
        totalcount = 0
        with open(ori_csv_file, 'r') as file:
            # calLine = csv.reader(file)
            # totalLines = len(list(calLine))
            lines = csv.reader(file)
            for line in lines:
                lineNum = lines.line_num
                station = line[0]+line[1]
                stationName = station+"火车站"
                gaodeDict = json.loads(json.dumps(gaode_geo(str(stationName))))
                geocodes = gaodeDict.get('geocodes')
                location = ''
                try:
                    locationGeo = dict(json.loads(
                        json.JSONEncoder().encode(geocodes), encoding='utf-8')[0])
                    if 'location' in locationGeo:
                        location = str(locationGeo.get('location'))
                        correctcount += 1
                    else:
                        location = 'None'
                        nonecount += 1
                        print("Station: {}\nGAODE data:{}\n".format(
                            station, gaodeDict))
                        print("None count: {}".format(nonecount))
                        logging.info("Station: {}\nGAODE data:{}\nNone count:{}".format(station, gaodeDict, nonecount))
                except IndexError as e:
                    location = 'Error'
                    errorcount += 1
                    print("Station: {}\nGAODE data:{}\n".format(
                        station, gaodeDict))
                    print("Error count: {}".format(errorcount))
                    print(e)
                    logging.error("Station: {}\nGAODE data:{}\nError count:{}".format(
                        station, gaodeDict, errorcount))
                    pass
                try:
                    with open(formatted_csv_file, 'a') as newfile:  # 'a' means append
                        myWriter = csv.writer(newfile)
                        myWriter.writerow(
                            [line[0], line[1], line[2], line[3], stationName, location])
                        totalcount = lineNum
                        print("compelet: {}".format(totalcount))
                        # print("complete: {} of {}, {}%".format(totalcount,
                        #                                        totalLines, round(totalcount/totalLines, 4)*100))
                except Exception as e:
                    logging.info(traceback.format_exc())
                    logging.error(e)
        print("Parsing done! it took {}. Error: {}, None: {}, Total: {}".format(time.time() - startTime,
                                                                                       errorcount, nonecount, totalcount))
        logging.info("Parsing done! it took {}. Error: {}, None: {}, Total: {}".format(time.time() - startTime,
                                                                                                  errorcount, nonecount, totalcount))


def getStaticAmap(lonlat_str, str_city_center):  # <---获取静态高德地图--->
    # sh = '121.472644,31.231706'  # 上海中心点
    # 高德地图-->静态地图API地址
    url = r'http://restapi.amap.com/v3/staticmap?location=%s&zoom=10&size=1024*768&key=<YOURKEY>'
    url_1 = url % str_city_center  # 加入城市
    url_amap = url_1+'&markers=mid,0xFF0000,A:'+lonlat_str  # 增加marker点
    print(url_amap)                                                     #
    webbrowser.open(url_amap)  # 打开


def openAmap():
    # https://restapi.amap.com/v3/staticmap?location=116.481485,39.990464&zoom=10&size=750*300&markers=mid,,A:116.481485,39.990464&key=<用户的key>
    base = ''
    parameters = {}
    # url = "https://restapi.amap.com/v3/staticmap?location=116.481485,39.990464&zoom=10&size=750*300&markers=mid,,A:116.481485,39.990464&key="+GAODE_KEY
    # url = "https://uri.amap.com/marker?markers=116.480564,39.996374,望京SOHO|116.481590,39.989175,食尚坊美食广场&src=mypage&callnative=0"
    # webbrowser.open(url)
    webbrowser.open("amap.html")


if __name__ == '__main__':  # <---主程序--->
    logging.basicConfig(filename=logfile,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    # print(gaode_geo('杭州笕桥'))
    csv_parse()
    # openAmap()

# -*- coding: utf-8 -*-
import os
import sys
import urllib.request
from xml.dom.minidom import parseString

api_key = "RLDjSffZH9LGQNjQ9yvsyG4MmZmNtICxy1DWeO0pa85GfcANW71FTq5UumHdT%2F70HdjQKkm5DieR816U2FXQyw%3D%3D"

server = "http://apis.data.go.kr/B552657/ErmctInfoInqireService"

def extraHospitalData(strXml):
    from xml.etree import ElementTree
    hospLst = []
    tree = ElementTree.fromstring(strXml)
    print(strXml)
    ElementLst = tree.findall("body/items/item")
    for item in ElementLst:
        hospLst.append(item.find("dutyName").text)

    if len(hospLst) <= 0:
        hospLst.append("검색 결과 없음")
    return hospLst

def userURIBuilder(url, **user):
    str = url + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def getHospitalListFromData(city, town):
    global server

    city_url = urllib.parse.quote(city)
    town_url = urllib.parse.quote(town)
    url_s = server + "/getEgytListInfoInqire"
    url = userURIBuilder(url_s, serviceKey=api_key, Q0=city_url, Q1=town_url)
    resp = None

    req = urllib.request.Request(url)

    resp = urllib.request.urlopen(req)
    rescode = resp.getcode()
    if rescode == 200:
        resp_body = resp.read()
        return extraHospitalData(resp_body.decode('utf-8'))
    else:
        print("Error Code : " + rescode)



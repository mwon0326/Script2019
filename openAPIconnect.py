# -*- coding: utf-8 -*-
import os
import sys
import urllib.request
from xml.dom.minidom import parseString
from xml.etree import ElementTree

api_key = "RLDjSffZH9LGQNjQ9yvsyG4MmZmNtICxy1DWeO0pa85GfcANW71FTq5UumHdT%2F70HdjQKkm5DieR816U2FXQyw%3D%3D"
server = "http://apis.data.go.kr/B552657/ErmctInfoInqireService"

def extraHospitalData(strXml):
    hospLst = {}
    tree = ElementTree.fromstring(strXml)
    ElementLst = tree.findall("body/items/item")
    for item in ElementLst:
        hospLst[item.find("dutyName").text] = item.find("hpid").text

    if len(hospLst) <= 0:
        hospLst["검색결과 없음"] = ""
    return hospLst

def extraHospitalInfo(strXml):
    hospData = {}
    tree = ElementTree.fromstring(strXml)
    ElementLst = tree.findall("body/items/item")
    for item in ElementLst:
        hospData['주소'] = item.find("dutyAddr").text
        hospData['우편번호'] = item.find("postCdn1").text
        hospData['대표전화'] = item.find("dutyTel1").text
        hospData['응급실전화'] = item.find("dutyTel3").text
        if item.find("dutyHayn").text == '1':
            hospData['입원실가용여부'] = "입원 가능"
        else:
            hospData['입원실가용여부'] = "입원 불가능"
        hospData['진료과목'] = item.find("dgidIdName").text


    return hospData

def userURIBuilder(url, **user):
    str = url + "?"
    for key in user.keys():
        if user[key] != "":
            str += key + "=" + user[key] + "&"
    return str

def getHospitalListFromData(city, town, name):
    global server

    if city != "":
        city_url = urllib.parse.quote(city)
    else:
        city_url = ""
    if town != "":
        town_url = urllib.parse.quote(town)
    else:
        town_url = ""
    if name != "":
        name_url = urllib.parse.quote(name)
    else:
        name_url = ""

    url_s = server + "/getEgytListInfoInqire"
    url = userURIBuilder(url_s, serviceKey=api_key, Q0=city_url, Q1=town_url, QN=name_url)
    return openAPI(url, 1)

def getHospitalInfo(ID):
    global server
    url_s = server + "/getEgytBassInfoInqire"
    url = userURIBuilder(url_s, serviceKey=api_key, HPID=ID)
    return openAPI(url, 2)

def openAPI(url, mode):
    req, resp = None, None
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    rescode = resp.getcode()
    if rescode == 200:
        resp_body = resp.read()
        if mode == 1:
            return extraHospitalData(resp_body.decode('utf-8'))
        elif mode == 2:
            return extraHospitalInfo(resp_body.decode('utf-8'))
    else:
        print("Error Code : " + rescode)



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
        hospData['경도'] = item.find("wgs84Lon").text
        hospData['위도'] = item.find("wgs84Lat").text
    return hospData

def extraHospitalMessage(strXml):
    hospMessage = {}
    tree = ElementTree.fromstring(strXml)
    ElementLst = tree.findall("body/items/item")
    for item in ElementLst:
        try:
            hospMessage['메세지'] = item.find("symBlkMsg").text
        except:
            hospMessage['메세지'] = "없음"
    if len(hospMessage) < 1:
        hospMessage['메세지'] = "없음"
    return hospMessage

def extraHospitalBed(strXml):
    global id
    hospBed = {}
    tree = ElementTree.fromstring(strXml)
    ElementLst = tree.findall("body/items/item")
    for item in ElementLst:
        if id == item.find("hpid").text:
            try:
                hospBed["입력일시"] = item.find("hvidate").text
            except:
                hospBed["입력일시"] = "없음"
            try:
                hospBed["응급실"] = item.find("hvec").text
            except:
                hospBed["응급실"] = "정보 없음"
    return hospBed

def extraHospitalOper(strXml):
    hospLst = {}
    tree = ElementTree.fromstring(strXml)
    ElementLst = tree.findall("body/items/item")
    for item in ElementLst:
        name = item.find("dutyName").text
        operLst = []
        for i in range(1, 12):
            id = "MKioskTy" + str(i)
            operLst.append(item.find(id).text)
        hospLst[name] = operLst
    if len(hospLst) <= 0:
        hospLst["검색결과 없음"] = ""
    return hospLst

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

def getHospitalOper(city, town):
    global server
    url_s = server + "/getSrsillDissAceptncPosblInfoInqire"
    city_url = urllib.parse.quote(city)
    town_url = urllib.parse.quote(town)
    url = userURIBuilder(url_s, serviceKey=api_key, STAGE1=city_url, STAGE2=town_url)
    return openAPI(url, 5)

def getHospitalMessage(ID):
    global server
    url_s = server + "/getEmrrmSrsillDissMsgInqire"
    url = userURIBuilder(url_s, serviceKey=api_key, HPID=ID)
    return openAPI(url, 3)

def getHospitalBed(ID, city, town):
    global server, id
    id = ID
    if city != "":
        city_url = urllib.parse.quote(city)
    else:
        city_url = ""
    if town != "":
        town_url = urllib.parse.quote(town)
    else:
        town_url = ""

    url_s = server + "/getEmrrmRltmUsefulSckbdInfoInqire"
    url = userURIBuilder(url_s, serviceKey=api_key, STAGE1=city_url, STAGE2=town_url)
    return openAPI(url, 4)

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
        elif mode == 3:
            return extraHospitalMessage(resp_body.decode('utf-8'))
        elif mode == 4:
            return extraHospitalBed(resp_body.decode('utf-8'))
        elif mode == 5:
            return extraHospitalOper(resp_body.decode('utf-8'))
    else:
        print("Error Code : " + rescode)



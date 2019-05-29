# -*- coding: utf-8 -*-
# 실행 전 같이 저장된 폰트들을 설치해주세요!!

from tkinter import *
import tkinter.font
import json
import tkinter.ttk
import openAPIconnect
import tkinter.messagebox
import openMap

FONT = "스웨거 TTF"

window = Tk()
window.title("전국 응급 기관 정보 조회 서비스")
window.geometry("600x400+100+100")
window.resizable(False, False)
window.configure(background='white')

FONT= '스웨거 TTF'
font = tkinter.font.Font(family=FONT, size=18)
info_font = tkinter.font.Font(family='KBIZ한마음명조 R', size=12)
image = PhotoImage(file="logo.png")

info_hospital = {}
LISTNUM = 1
INFONUM = 0

def MainForm():
    global window, font, data, image
    global townCb, cityCb, searchE

    x, y = 110, 220
    json_data = open("listBox.json", "r", encoding='UTF8').read()
    data = json.loads(json_data)

    Label(window, image=image, bg='white').place(x=x + 60, y=y - 210)

    cityCb = tkinter.ttk.Combobox(window, width=15, value=data["CITY"], font=font)
    cityCb.set("시/도 선택")
    cityCb.place(x=x, y=y)

    townCb = tkinter.ttk.Combobox(window, width=15, value=data[cityCb.get()], postcommand=changeTownCb, font=font)
    townCb.set("시/구/군 선택")
    townCb.place(x=x + 200, y=y)

    Label(window, text="병원명", font=font, background='white').place(x=x + 20, y=y + 50)
    searchE = Entry(window, width=20, font=font)
    searchE.place(x=x + 80, y=y + 50)
    searchB = Button(window, text="검색", font=font, command=search, bg='white')
    searchB.place(x=x + 290, y=y + 50)

def changeTownCb():
    global data
    global townCb, cityCb
    townCb.configure(value=data[cityCb.get()])

def search():
    if townCb.get() == "시/구/군 선택":
            tkinter.messagebox.showinfo(message="다시 입력해주세요")
    else:
         SubForm()

def SubForm():
    global data,window, dataForm, font, info_text, frames, hospital_List, mapLB

    hospital_List = openAPIconnect.getHospitalListFromData(cityCb.get(), townCb.get(), searchE.get())
    if '검색결과 없음' in hospital_List:
        tkinter.messagebox.showinfo(message="검색 결과가 없습니다")
    else:
        dataForm = Toplevel(window)
        dataForm.title("전국 응급 의료기관 정보")
        dataForm.resizable(False, False)
        dataForm.configure(background='white')
        dataForm.geometry("600x400+200+200")

        frames = []

        frames.append(Frame(dataForm, width=600, height=400, bg='white'))
        frames[0].grid(row=0, column=0)

        frames.append(Frame(dataForm, width=600, height=400, bg='white'))
        frames[1].grid(row=0, column=0)

        text_frame = Frame(frames[INFONUM])
        text_frame.place(x=50,y=70)

        info_scroll = Scrollbar(text_frame)
        info_scroll.pack(side="right", fill="y")

        info_text = Text(text_frame, width=53, height=15, font=info_font, yscrollcommand=info_scroll.set)
        info_text.pack()
        Button(frames[INFONUM], text="뒤로", font=font, command=lambda : frames[LISTNUM].tkraise()).place(x=50,y=30)

        Button(frames[LISTNUM], text="상세정보", font=font, command=infoHospital, bg='white').place(x=150,y=60)
        Button(frames[LISTNUM], text="지도", font=font, command=mapHospital, bg='white').place(x=225,y=60)

        hospitalList()

def mapHospital():
    global info_hospital, frames, select, mapLB
    try:
        select = hosLst.get(hosLst.curselection())
    except:
        tkinter.messagebox.showinfo(message="병원을 선택해주세요")
    info_hospital = openAPIconnect.getHospitalInfo(hospital_List[select])
    openMap.saveMap(eval(info_hospital['위도']), eval(info_hospital['경도']), select)

def hospitalList():
    global townCb, cityCb, searchE, hosLst, hospital_List, frames
    x, y = 150, 100
    lstFrame = Frame(frames[LISTNUM])
    lstFrame.place(x=x,y=y)

    lstScroll = Scrollbar(lstFrame)
    lstScroll.pack(side='right', fill='y')

    hosLst = Listbox(lstFrame, width=30, font=font, yscrollcommand=lstScroll.set)

    i = 0
    for name in hospital_List.keys():
        hosLst.insert(i, name)
        i += 1
    hosLst.pack()

def infoHospital():
    global hosLst, hospital_List, info_text,frames, townCb, cityCb, info_hospital, select
    try:
        select = hosLst.get(hosLst.curselection())
    except:
        tkinter.messagebox.showinfo(message="병원을 선택해주세요")
    info_hospital = openAPIconnect.getHospitalInfo(hospital_List[select])
    message_hospital = openAPIconnect.getHospitalMessage(hospital_List[select])
    bed_hospital = openAPIconnect.getHospitalBed(hospital_List[select], cityCb.get(), townCb.get())

    frames[INFONUM].tkraise()
    info_text.configure(state='normal')
    info_text.delete(1.0, END)
    info_text.update()
    for key in info_hospital.keys():
        info_text.insert("current", key + " : " + info_hospital[key] + "\n")
    info_text.insert("current", "병원 메세지 : " + message_hospital['메세지'] + "\n")
    info_text.insert("current", "-------------------------------------------\n")
    info_text.insert("current", "입력일시 : " + bed_hospital['입력일시'] + "\n")
    info_text.insert("current", "응급실 가용병상 : " + bed_hospital['응급실'] + "\n")
    info_text.configure(state='disabled')

MainForm()
window.mainloop()



# -*- coding: utf-8 -*-
# 실행 전 같이 저장된 폰트들을 설치해주세요!!

from tkinter import *
import tkinter.font
import tkinter.ttk
import tkinter.messagebox
from PIL import Image,ImageTk
import openAPIconnect
import openMap
import Mail
import openImage

LISTNUM = 2
INFONUM = 1
MailNUM = 0

class SubForm:
    def __init__(self, cityName, townName, hospitalName, font, window):
        self.city_name = cityName
        self.town_name = townName
        self.hospital_name = hospitalName
        self.font = font
        self.window = window

        self.getHospitalList()

    def getHospitalList(self): # 서브 윈도우를 열 것인가 안 열 것인가
        self.hospital_list = openAPIconnect.getHospitalListFromData(self.city_name, self.town_name, self.hospital_name)
        if '검색결과 없음' in self.hospital_list:
            tkinter.messagebox.showinfo(message="검색 결과가 없습니다")
        else:
            self.openSubForm() # 서브 윈도우를 연다

    def openSubForm(self):
        self.dataForm = Toplevel(self.window)
        self.dataForm.title("전국 응급 의료기관 정보")
        self.dataForm.resizable(False, False)
        self.dataForm.configure(background='white')
        self.dataForm.geometry("600x400+200+200")

        self.frames = []

        self.frames.append(Frame(self.dataForm, width=600, height=400, bg='white'))
        self.frames[0].grid(row=0, column=0)

        self.frames.append(Frame(self.dataForm, width=600, height=400, bg='white'))
        self.frames[1].grid(row=0, column=0)

        self.frames.append(Frame(self.dataForm, width=600, height=400, bg='white'))
        self.frames[2].grid(row=0, column=0)

        self.hospitalList() # 병원 리스트 박스 생성
        self.informationHospital() # 병원 상세정보 프레임 생성
        self.mailHospital() # 병원 정보 메일 프레임 생성
        Button(self.frames[LISTNUM], text="상세정보", font=self.font, command=self.changeInformationFrame, bg='white').place(x=150, y=60)
        Button(self.frames[LISTNUM], text="지도", font=self.font, command=self.mapHospital, bg='white').place(x=225, y=60)
        Button(self.frames[LISTNUM], text="메일", font=self.font, command=self.changeMailFrame,
               bg='white').place(x=270, y=60)

    def mailHospital(self): # 병원 정보 메일 프레임 생성
        mx, my = 130, 250
        Button(self.frames[MailNUM], text="뒤로", font=self.font,
               command=lambda : self.frames[LISTNUM].tkraise()).place(x=50, y=30)
        Label(self.frames[MailNUM], text="받는 메일 주소 : ", font=self.font, bg='white').place(x=mx, y=my)
        self.mailE = Entry(self.frames[MailNUM], text="", font=self.font)
        self.mailE.place(x=mx + 120, y=my)
        Button(self.frames[MailNUM], text="보내기", font=self.font, command=self.sendMail).place(x=mx + 320, y=my)

        Label(self.frames[MailNUM], text="지도 첨부 : ", bg='white', font=self.font).place(x=mx, y=my+50)

        self.mapCheck = tkinter.IntVar()
        self.mapRB1 = Radiobutton(self.frames[MailNUM], text="첨부함", value=1,
                                  font=self.font, bg='white', variable=self.mapCheck).place(x=mx+100, y=my+50)
        self.mapRB2 = Radiobutton(self.frames[MailNUM], text="첨부하지 않음", value=2,
                                  font=self.font, bg='white', variable=self.mapCheck).place(x=mx+220, y=my+50)

    def sendMail(self):
        Mail.sendMail(self.mailE.get(), self.mail, self.mail_name, self.mapCheck.get(),
                      self.r, self.c)
        tkinter.messagebox.showinfo(message="보내기 완료")

    def changeMailFrame(self):
        try:
            self.mail_name = self.hospitalLB.get(self.hospitalLB.curselection())
            self.getInformationHospital(self.mail_name, 2) # 병원 정보 보낼 문자열 추가
            self.frames[MailNUM].tkraise()
        except:
            tkinter.messagebox.showinfo(message="병원을 선택해주세요")

    def informationHospital(self): # 병원 상세 정보 프레임 생성
        info_font = tkinter.font.Font(family='KBIZ한마음명조 R', size=12)
        text_frame = Frame(self.frames[INFONUM])
        text_frame.place(x=50, y=70)

        info_scroll = Scrollbar(text_frame)
        info_scroll.pack(side="right", fill="y")

        self.info_text = Text(text_frame, width=28, height=15, font=info_font, yscrollcommand=info_scroll.set)
        self.info_text.pack()
        Button(self.frames[INFONUM], text="뒤로", font=self.font,
               command=lambda: self.frames[LISTNUM].tkraise(), bg='white').place(x=50,y=30)

    def changeInformationFrame(self): # 병원 정보 프레임으로 프레임 전환
        try:
            select = self.hospitalLB.get(self.hospitalLB.curselection())
            self.getInformationHospital(select, 1) # 병원 정보 텍스트에 정보 추가
            self.frames[INFONUM].tkraise()
        except:
            tkinter.messagebox.showinfo(message="병원을 선택해주세요")

    def getInformationHospital(self, select, mode): # 병원 정보 텍스트에 정보 추가
        info_hospital = openAPIconnect.getHospitalInfo(self.hospital_list[select])
        message_hospital = openAPIconnect.getHospitalMessage(self.hospital_list[select])
        bed_hospital = openAPIconnect.getHospitalBed(self.hospital_list[select], self.city_name, self.town_name)

        if mode == 1:
            self.info_text.configure(state='normal')
            self.info_text.delete(1.0, END)
            self.info_text.update()
            for key in info_hospital.keys():
                if key != "경도" and key != "위도":
                    self.info_text.insert("current", key + " : " + info_hospital[key] + "\n")
            self.info_text.insert("current", "병원 메세지 : " + message_hospital['메세지'] + "\n")
            self.info_text.insert("current", "-------------------------------------------\n")
            self.info_text.insert("current", "입력일시 : " + bed_hospital['입력일시'] + "\n")
            self.info_text.insert("current", "응급실 가용병상 : " + bed_hospital['응급실'] + "\n")
            self.info_text.configure(state='disabled')

            if select == "의료법인명지의료재단명지병원" and self.city_name != "서울특별시":
                select += "1"
            image1 = openImage.openImage(select)
            image2 = image1.resize((280,200), Image.ANTIALIAS)
            self.hospital_image = ImageTk.PhotoImage(image2)
            Label(self.frames[INFONUM], width=200, height=280, image=self.hospital_image, bg='white').place(x=350, y= 70)

        elif mode == 2:
            self.r, self.c = eval(info_hospital['위도']), eval(info_hospital['경도'])
            self.mail = ""
            for key in info_hospital.keys():
                if key != "경도" and key != "위도":
                    self.mail += "[{0}] : {1}\n".format(key, info_hospital[key])
            self.mail += "[{0}] : {1}\n".format('병원 메세지', message_hospital['메세지'])
            self.mail += "[{0}] : {1}\n".format('입력일시', bed_hospital['입력일시'])
            self.mail += "[{0}] : {1}\n".format('응급실 가용병상', bed_hospital['응급실'])

    def mapHospital(self): # 지도 출력
        try:
            select = self.hospitalLB.get(self.hospitalLB.curselection())
            info_hospital = openAPIconnect.getHospitalInfo(self.hospital_list[select])
            openMap.saveMap(eval(info_hospital['위도']), eval(info_hospital['경도']), select)
        except:
            tkinter.messagebox.showinfo(message="병원을 선택해주세요")

    def hospitalList(self): # 병원 리스트 박스 생성
        lstFrame = Frame(self.frames[LISTNUM])
        lstFrame.place(x=150, y=100)

        lstScroll = Scrollbar(lstFrame)
        lstScroll.pack(side='right', fill='y')

        i = 0
        self.hospitalLB = Listbox(lstFrame, width=30, font=self.font, yscrollcommand=lstScroll.set)
        for name in self.hospital_list.keys():
            self.hospitalLB.insert(i, name)
            i += 1
        self.hospitalLB.pack()


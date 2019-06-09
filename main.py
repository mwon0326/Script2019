# -*- coding: utf-8 -*-
# 실행 전 같이 저장된 폰트들을 설치해주세요!!

from tkinter import *
import tkinter.font
import json
import tkinter.ttk
import tkinter.messagebox
import sub

class MainForm:
    def __init__(self):
        self.window = Tk()
        self.window.title("전국 응급 기관 정보 조회 서비스")
        self.window.geometry("600x400+100+100")
        self.window.resizable(False, False)
        self.window.configure(background='white')

        self.x, self.y = 110, 220

        self.image = PhotoImage(file="logo.png")
        self.font = tkinter.font.Font(family='스웨거 TTF', size=18)
        self.openJson()

        Label(self.window, image=self.image, bg='white').place(x=self.x, y=self.y - 100)

        self.cityCb = tkinter.ttk.Combobox(self.window, width=15, value=self.city_data["CITY"], font=self.font)
        self.cityCb.set("시/도 선택")
        self.cityCb.place(x=self.x, y=self.y)

        self.townCb = tkinter.ttk.Combobox(self.window, width=15, value=self.city_data[self.cityCb.get()],
                                      postcommand=self.changeTownCb, font=self.font)
        self.townCb.set("시/구/군 선택")
        self.townCb.place(x=self.x + 200, y=self.y)

        Label(self.window, text="병원명", font=self.font, background='white').place(x=self.x + 20, y=self.y + 50)
        self.searchE = Entry(self.window, width=20, font=self.font)
        self.searchE.place(x=self.x + 80, y=self.y + 50)
        self.searchB = Button(self.window, text="검색", font=self.font, command=self.searchHospital, bg='white')
        self.searchB.place(x=self.x + 290, y=self.y + 50)

        self.window.mainloop()

    def changeTownCb(self):
        self.townCb.configure(value=self.city_data[self.cityCb.get()])

    def searchHospital(self):
        if self.townCb.get() == "시/구/군 선택" and self.cityCb.get() != "세종특별자치시":
            tkinter.messagebox.showinfo(message="다시 입력해주세요")
        else:
            cityName = self.cityCb.get()
            townName = self.townCb.get()
            hospitalName = self.searchE.get()
            sub.SubForm(cityName, townName, hospitalName, self.font, self.window)

    def openJson(self):
        json_data = open("listBox.json", "r", encoding='UTF8').read()
        self.city_data = json.loads(json_data)



MainForm()
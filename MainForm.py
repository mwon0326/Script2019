# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.font
import json
import tkinter.ttk

FONT = "스웨거 TTF"

class MainForm:
    def __init__(self):
        window = Tk()
        window.title("전국 응급 기관 정보 조회 서비스")
        window.geometry("600x400+100+100")
        window.resizable(False, False)
        window.configure(background='white')

        x, y = 110, 220
        self.font = tkinter.font.Font(family=FONT, size=18)
        self.f = (FONT, '18')
        json_data = open("listBox.json", "r", encoding='UTF8').read()
        self.data = json.loads(json_data)

        image = PhotoImage(file='logo.png')
        Label(window,image=image, bg='white').place(x=x+60, y=y-210)

        self.cityCb = tkinter.ttk.Combobox(window, width=15, value=self.data["CITY"], font=self.f)
        self.cityCb.set("시/도 선택")
        self.cityCb.place(x=x,y=y)

        self.townCb = tkinter.ttk.Combobox(window, width=15, value=self.data[self.cityCb.get()], postcommand=self.changeTownCb, font= self.f)
        self.townCb.set("시/구/군 선택")
        self.townCb.place(x=x + 200,y=y)

        Label(window, text="병원명", font=self.font, background='white').place(x=x + 20, y=y+50)
        self.searchE = Entry(window, width=20, font=self.font)
        self.searchE.place(x=x+80, y=y+50)
        self.searchB = Button(window, text="검색", font=self.font, command=self.search, bg='white')
        self.searchB.place(x=x+290,y=y+50)

        window.mainloop()

    def changeTownCb(self):
        self.townCb.configure(value=self.data[self.cityCb.get()])

    def search(self):
        pass

MainForm()

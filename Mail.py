# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText # 제목과 본문 설정용
from email.mime.base import MIMEBase # 지도 첨부
from email.mime.image import MIMEImage
from email import encoders
import os
import openMap

myEmail = "mwon0326@gmail.com"
myPassword = "eutwbkvklnvfpjai"

def sendMail(addr, text, name, mapCheck, r, c):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(myEmail, myPassword)

    msg = MIMEBase('multipart', 'mixed')
    msg['Subject']= "[" + name + "] 병원 상세 정보 및 지도"
    msg['From'] = myEmail
    msg['To'] = addr

    if mapCheck == 1:
        path = name + ".png"
        if os.path.isfile(path) == False:
            openMap.saveMap(r, c, name)
        image = open(path, 'rb')
        imageP = MIMEImage(image.read())
        image.close()
        msg.attach(imageP)

    cont = MIMEText(text)
    if mapCheck == 1:
        imageP.add_header('Content-Disposition','attachment', filename=path)
    msg.attach(cont)
    s.sendmail(myEmail, addr, msg.as_string())
    s.quit()



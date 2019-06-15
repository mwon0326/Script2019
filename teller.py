import telepot
import noti
import openAPIconnect

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메세지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('지역') and len(args) > 1:
        replyHospitalData(chat_id, args[1], args[2])
    else:
        noti.sendMessage(chat_id, "모르는 명령어 입니다.\n 지역 [시/도] [시/군/구]를 양식에 맞춰 정확히 입력했는지 확인해주세요.")

def replyHospitalData(user, city, town):
    res_list = noti.getData(city, town)
    msg = ""
    for r in res_list:
        noti.sendMessage(user, r)


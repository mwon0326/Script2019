import telepot
import traceback
import sys
import openAPIconnect

token = "701127125:AAHvTPQZTsRtEXjU29zWL4gzYaDkQ8OS5RM"
bot = telepot.Bot(token)
oper_list = ['뇌출혈수술 : ', '뇌경색의재관류 : ', '심근경색의재관류 : ', '복부손상의수술 : ', '사지접합의수술 : ',
             '응급내시경 : ', '응급투석 : ', '조산산모 : ','정신질환자 : ', '신생아 : ', '중증화상 : ']

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def getData(city, town):
    global oper_list
    data = openAPIconnect.getHospitalOper(city, town)
    res_list = []
    for key in data:
        if key == "검색결과 없음":
            res_list.append("해당 지역엔 응급기관이 존재하지 않습니다.")
            return res_list
        msg = ''
        msg += key + "의 중증질환수용여부\n"
        for i in range(11):
            msg += oper_list[i]
            if data[key][i] == 'Y':
                msg += "수용가능\n"
            else:
                msg += "수용불가능\n"
        res_list.append(msg)
    return res_list




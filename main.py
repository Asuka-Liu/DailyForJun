from datetime import date, datetime
from borax.calendars.festivals import LunarSchema
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()



# 从github设置里面获取
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_id_1 = os.environ["USER_ID_1"]
user_id_2 = os.environ["USER_ID_2"]
template_id = os.environ["TEMPLATE_ID"]
start_date = os.environ['START_DATE']



def get_today():#获得对应的农历   
    numCn = ["天", "一", "二", "三", "四", "五", "六"]  
    year = datetime.now().year   
    month = datetime.now().month   
    day = datetime.now().day
    week=date(year,month,day).weekday()
    today='今天是 ' +str(year) + "年" + str(month) + "月" + str(day) + "日" +" 星期" + numCn[week] 
    return today  #  返回当前的日期信息

def get_weather_zz():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=郑州"
    res = requests.get(url).json()
    weathers = res['data']['list'][0]
    return weathers['weather'], math.floor(weathers['temp'])


def get_weather_hb():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=淮北"
    res = requests.get(url).json()
    weathers = res['data']['list'][0]
    return weathers['weather'], math.floor(weathers['temp'])


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days

def get_birthday_yang():  #计算阳历生日
  next = datetime.strptime(str(date.today().year) + "-" + "07-22", "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days


def get_birthday_nong():  # 计算农历生日
    result = LunarSchema(month=6, day=18)
    return result.countdown()


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)

today_words=get_today()
zz_weather, zz_temperature = get_weather_zz()
hb_weather, hb_temperature = get_weather_hb()

data = {  
          "today": {"value": today_words},
          "weather_zz": {"value": zz_weather},
          "temperature_zz": {"value": zz_temperature}, 
          "weather_hb": {"value": hb_weather},
          "temperature_hb": {"value": hb_temperature}, 
          "love_days": {"value": get_count()}, 
          "birthday_left_nong": {"value": get_birthday_nong()},  
          "birthday_left_yang": {"value": get_birthday_yang()},
          "words": {"value": get_words(), "color": get_random_color()}
        }
# print(data)
res1 = wm.send_template(user_id_1, template_id, data)
res2 = wm.send_template(user_id_2, template_id, data)

print(res1)
print(res2)

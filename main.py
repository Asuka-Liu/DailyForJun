from datetime import date, datetime
from unittest import result
from borax.calendars.festivals import LunarSchema 
import math

from pkg_resources import register_loader_type
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']

# birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather_zz():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=郑州"
  res = requests.get(url).json()
  weathers= res['data']['list'][0]
  return weathers['weather'], math.floor(weathers['temp'])

def get_weather_hb():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=淮北"
  res = requests.get(url).json()
  weathers = res['data']['list'][0]
  return weathers['weather'], math.floor(weathers['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

# def get_birthday():  #计算阳历生日
#   next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
#   if next < datetime.now():
#     next = next.replace(year=next.year + 1)
#   return (next - today).days

def get_birthday_nong():  #计算农历生日
  result=LunarSchema(month=7,day=22)
  return result.countdown

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)

zz_weather, zz_temperature = get_weather_zz()
hb_weather, hb_temperature = get_weather_hb()

data = {"weather_zz":{"value":zz_weather},"temperature_zz":{"value":zz_temperature},"weather_hb":{"value":hb_weather},"temperature_hb":{"value":hb_temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday_nong()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)

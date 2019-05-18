#!/usr/bin/env python
# -*- coding: utf-8 -*-
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
from response import response
#import MySQLdb
import datetime
import requests
from login import isLogin, isAdmin, login
#from secret import tokenVK #вынес пароль в отдельный файл
from admin import adminresponce
import bs4

#from tokens import generateUsers, getTokens

keyb="""{
  "one_time": false,
  "buttons": [
    [{
      "action": {
        "type": "text",
        "label": "Nice answer!"
      },
      "color": "positive"
    },
      {
        "action": {
          "type": "text",
          "label": "Normal answer."
        },
        "color": "positive"
      }],
    [{
      "action": {
        "type": "text",
        "label": "Bad answer!"
      },
      "color": "default"
    }]
  ]
}"""


usernames = dict()

def get_name(user_id):
  if user_id in usernames:
    return usernames[user_id]
  usernames[user_id] = str(_get_user_name_from_vk_id(user_id))
  return usernames[user_id]


def _get_user_name_from_vk_id(user_id):
    request = requests.get("https://vk.com/id"+str(user_id))
    bs = bs4.BeautifulSoup(request.text, "html.parser")
    user_name = str(bs.findAll("title")[0])
    user_name = user_name.replace("<title>","")
    return user_name.split()[0]


def main():
    badansw=0
    normalansw=0
    niceansw=0
    print("start")

    tok = 'PUT UR VK TOKEN HERE'
    vk_session = vk_api.VkApi(token=tok)

    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
          text = str(event.text)
          time = str(datetime.datetime.now())
          time = time[:19]
          

          if isAdmin(str(event.user_id)):
                try:
                    print(str(event.user_id)+"  "+text)
                    res = str(get_name(event.user_id))+", "+adminresponce(text)
                    vk.messages.send(user_id = event.user_id, message = res, random_id = randint(0, 9999),keyboard=keyb)
                except Exception as e:
                    requests.post("http://danr0.pythonanywhere.com/api/err/", data = str(event.user_id)+"$"+str(e)+"$"+time)
                    print(str(e))
          elif isLogin(str(event.user_id)):
                try:
                    print(str(event.user_id)+"  "+text)
                    if text == "Nice answer!":
                        niceansw+=1
                        res="Уже "+str(niceansw)+" nice answers"
                    elif text == "Bad answer!":
                        badansw+=1
                        res="Уже "+str(badansw)+" bad answers"
                    elif text == "Normal answer.":
                        normalansw+=1
                        res="Уже "+str(normalansw)+" normal answers"
                    else:
                        text = text.replace("\n",'')
                        res = get_name(event.user_id)+", "+response(text)#заглушка со стандартнами ответами, потом сюда прикрутим нормальные ответы
                    vk.messages.send(user_id = event.user_id, message = res, random_id = randint(0, 9999),keyboard=keyb)
                except Exception as e:
                #логирование ошибок
                    requests.post("http://danr0.pythonanywhere.com/api/err/", data = str(event.user_id)+"$"+str(e)+"$"+time)
                    print(str(e))
          else:
                try:
                    res = login(str(event.user_id), text)
                    vk.messages.send(user_id = event.user_id, message = res, random_id = randint(0, 9999),keyboard=keyb)
                    print(str(event.user_id)+"  "+text)
                except Exception as e:
                    #логирование ошибок
                    requests.post("http://danr0.pythonanywhere.com/api/err/", data = str(event.user_id)+"$"+str(e)+"$"+time)
                    print(str(e))


if __name__ == '__main__':
    print("start the bot")
    main()
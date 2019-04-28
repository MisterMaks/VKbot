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
from secret import tokenVK #вынес пароль в отдельный файл
from admin import adminresponce
#from tokens import generateUsers, getTokens


def main():

    tok = tokenVK()
    vk_session = vk_api.VkApi(token=tok)

    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if isAdmin(str(event.user_id)):
                try:
                    text = (event.text).encode('utf-8')
                    time = str(datetime.datetime.now())
                    time = time[:19]
                    print(str(event.user_id)+"  "+text)
                    res = adminresponce(text)
                    vk.messages.send(user_id = event.user_id, message = res, random_id = randint(0, 9999))
                except Exception as e:
                    requests.post("http://danr0.pythonanywhere.com/api/err/", data = str(event.user_id)+"$"+str(e)+"$"+time)
                    print(str(e.message))
            elif isLogin(str(event.user_id)):
                try:
                    text = (event.text).encode('utf-8')
                    time = str(datetime.datetime.now())
                    time = time[:19]
                    text = str(text.encode('base64'))
                    text = text.replace("\n",'')
                    print(str(event.user_id)+"  "+text)
                    res = response(text)#заглушка со стандартнами ответами, потом сюда прикрутим нормальные ответы
                    vk.messages.send(user_id = event.user_id, message = res, random_id = randint(0, 9999))
                    requests.post("http://danr0.pythonanywhere.com/api/req/", data = str(event.user_id)+"$"+str(text)+"$"+time)
                except Exception as e:
                #логирование ошибок
                    requests.post("http://danr0.pythonanywhere.com/api/err/", data = str(event.user_id)+"$"+str(e)+"$"+time)
                    print(str(e.message))
            else:
                try:
                    text = (event.text).encode('utf-8')
                    time = str(datetime.datetime.now())
                    time = time[:19]
                    res = login(str(event.user_id), text)
                    vk.messages.send(user_id = event.user_id, message = res, random_id = randint(0, 9999))
                    print(str(event.user_id)+"  "+text)
                    text = str(text.encode('base64'))
                    text = text.replace("\n",'')
                    requests.post("http://danr0.pythonanywhere.com/api/req/", data = str(event.user_id)+"$"+str(text)+"$"+time)
                except Exception as e:
                    #логирование ошибок
                    requests.post("http://danr0.pythonanywhere.com/api/err/", data = str(event.user_id)+"$"+str(e)+"$"+time)
                    print(str(e.message))


        '''
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and isAdmin(str(event.user_id)):
            try:
                text = (event.text).encode('utf-8')
                time = str(datetime.datetime.now())
                time = time[:19]
                print(str(event.user_id)+"  "+text)
                #if '/gen' in str(text):
                #    generateUsers(1)
                #res = str(getTokens())
                res = adminresponce(text)
                vk.messages.send(user_id = event.user_id, message = res, random_id = randint(0, 9999))
                #requests.post("http://danr0.pythonanywhere.com/api/req/", data = str(event.user_id)+"$"+str(text)+"$"+time)
            except Exception as e:
                #логирование ошибок
                requests.post("http://danr0.pythonanywhere.com/api/err/", data = str(event.user_id)+"$"+str(e)+"$"+time)
                print(str(e.message))

        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and isLogin(str(event.user_id)):
            try:
                text = (event.text).encode('utf-8')
                time = str(datetime.datetime.now())
                time = time[:19]
                text = str(text.encode('base64'))
                text = text.replace("\n",'')
                print(str(event.user_id)+"  "+text)
                res = response(text)#заглушка со стандартнами ответами, потом сюда прикрутим нормальные ответы
                vk.messages.send(user_id = event.user_id, message = res, random_id = randint(0, 9999))
                requests.post("http://danr0.pythonanywhere.com/api/req/", data = str(event.user_id)+"$"+str(text)+"$"+time)
            except Exception as e:
                #логирование ошибок
                requests.post("http://danr0.pythonanywhere.com/api/err/", data = str(event.user_id)+"$"+str(e)+"$"+time)
                print(str(e.message))

        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and not isLogin(str(event.user_id)):
            try:
                text = (event.text).encode('utf-8')
                time = str(datetime.datetime.now())
                time = time[:19]
                res = login(str(event.user_id), text)
                vk.messages.send(user_id = event.user_id, message = res, random_id = randint(0, 9999))
                print(str(event.user_id)+"  "+text)
                text = str(text.encode('base64'))
                text = text.replace("\n",'')
                requests.post("http://danr0.pythonanywhere.com/api/req/", data = str(event.user_id)+"$"+str(text)+"$"+time)
            except Exception as e:
                #логирование ошибок
                requests.post("http://danr0.pythonanywhere.com/api/err/", data = str(event.user_id)+"$"+str(e)+"$"+time)
                print(str(e.message))
                '''

if __name__ == '__main__':
    main()
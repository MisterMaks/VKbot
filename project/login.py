#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from tokens import isValid
cashe = list()
admins = list()
notindb = list()
admins.append('199707448')

def isLogin(name):
    if name in cashe:
        return True
    if name in notindb:
        return False
    r = requests.get("http://danr0.pythonanywhere.com/api/users/"+str(name))
    if 'user' in str(r.text):
        cashe.append(name)
        return True
    return False

def isAdmin(name):
    if name in admins:
        return True
    if name in notindb:
        return False
    r = requests.get("http://danr0.pythonanywhere.com/api/users/"+str(name))
    if 'admin' in str(r.text):
        admins.append(name)
        return True
    return False

def login(name, password):
    if not (name in notindb) and not isAdmin(name) and not isLogin(name):
        notindb.append(name)
    val = isValid(str(password))
    if (val and len(password) > 30):
        r = requests.post("http://danr0.pythonanywhere.com/api/users/", data = name+"$admin")
        admins.append(name)
        if '200' in str(r):
            return u"Токен валиден. Вам доступны права администратора"
        return u"Токен валиден. Вам доступны права администратора  в течение сессии"
    if (val):
        r = requests.post("http://danr0.pythonanywhere.com/api/users/", data = name+"$user")
        cashe.append(name)
        if '200' in str(r):
            return u"Токен валиден. Вам доступны права пользоваетля"
        return u"Токен валиден. Вам доступны права пользоваетля в течение сессии"
    return u"Токен невалиден. Введите токен для авторизации"

#print(login(123, "ыввы"))
#print(isLogin(1))
#s = "(('1', 'user'), ('1', 'user'), ('1', 'user'), ('1', 'user'))"
#if 'user' in s:
        #cashe.append(name)
 #       print("dd")
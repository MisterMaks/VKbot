#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tokens import generateUsers, getTokens, generateAdmins
from response import response

def adminresponce(text):
    text = str(text)
    if '/' in text:
        if '/genadmin ' in str(text):
            n =  text.replace('/genadmin ', '')
            if n.isdigit():
                n = int(n)
                generateAdmins(n)
                return u'Токены сгенерированы'
            else:
                return u'Пример команды: /genadmin 3'
        if '/gen' in str(text):
            n =  text.replace('/gen ', '')
            if n.isdigit():
                n = int(n)
                generateUsers(n)
                return u'Токены сгенерированы'
            else:
                return u'Пример команды: /gen 3'
        if '/tokens' in str(text):
            return ('\n'.join(getTokens()))
        return u'команды: /gen - сгенерировать токены юзеров \n/genadmin  сгенерировать токены админов \n/tokens - вывести токены \n'
    return response(text)

#print(adminresponce('/gen 3'))
#print(adminresponce('/genadmin 3'))
#print(adminresponce('/tokens'))
#print(adminresponce('/t'))
#print(adminresponce('привет'))
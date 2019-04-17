#!/usr/bin/env python
# -*- coding: utf-8 -*-

def response(text):
    #text = text.decode('utf-8','ignore')
    text = text.decode('base64')
    text = text.decode('utf-8','ignore')
    text = text.lower()
    print(text)
    #text = str(text)
    if len(text) > 50 :
        return u"Слишком длинный запрос"
    if u"привет" in text:
        return "Привет!"
    if u"пока" in text or u"bye" in text:
        return u"Пока"
    if u"?" in text:
        return u"Это вопрос!"
    if u"кто ты" in text or u"помощь" in text or u"help" in text:
        return "я бот"
    return u"Я пока такое не умею"

#print(response("0L/RgNC40LLQtdGC"))
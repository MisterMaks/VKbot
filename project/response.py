#!/usr/bin/env python
# -*- coding: utf-8 -*-
from true_project import *
import warnings
warnings.filterwarnings('ignore')

def response(text):
    text = str(text)
    text = text.lower()
    print(text)
    if not (text.replace(" ","")).isalnum():
        return u"Допустимы только буквы и цифры"
    if len(text) > 50 :
        return u"Слишком длинный запрос"
    return good_answer(str(text), df_stack_questions, df_stack_answers, df_quest_ans_mail_ans)
    '''
    if u"привет" in text:
        return "Привет!"
    if u"пока" in text or u"bye" in text:
        return u"Пока"
    if u"?" in text:
        return u"Это вопрос!"
    if u"кто ты" in text or u"помощь" in text or u"help" in text:
        return "я бот"
    return u"Я пока такое не умею"
    '''

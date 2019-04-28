#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import secrets
import random
import string
#import secrets //заменить потом из-за безопасности

admintokenlen =40
usertokenlen = 20
tokens = list()

def isValid(token):
    if token in tokens:
        tokens.remove(token)
        return True
    return False

def getTokens():
    return tokens

def generateToken(n):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    tokens.append(''.join(random.choice(lettersAndDigits) for i in range(n)))
    return tokens[-1]

def generateUsers(n):
    out = list()
    for _ in range(n):
        out.append(generateToken(usertokenlen))
    return out

def generateAdmins(n):
    out = list()
    for _ in range(n):
        out.append(generateToken(admintokenlen))
    return out


#x = secrets.token_hex(10)
#print(x)
'''
print(generateUsers(4))
print(generateAdmins(3))
print(tokens)'''

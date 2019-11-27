#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests, sys, os

MAX_TRY = 10
BASE_URL = 'http://jiltedonion.net/4ad/images/'

try:
    os.mkdir(".\out")
except OSError:
    print("Creation of the directory failed")
else:
    print("Successfully created the directory")

i = 1#11
fail = 0
while True:
    #name = 'dungroom_'+str(i)+'.png'
    name='entroom_'+str(i)+'.png'
    response = requests.get(BASE_URL+name)
    print(BASE_URL+name,'-',response.status_code)
    if(response.status_code != 200):
        fail+=1
        if(fail>MAX_TRY):
            break
    else:
        open('.\out\\'+name, 'wb').write(response.content)
        fail = 0
    i+=1
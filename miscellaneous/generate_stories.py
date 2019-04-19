#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, random, itertools, sys, codecs, string

stringheIn = [line.rstrip('\n') for line in open("listaStringhe.txt")]
nomiList = [line.rstrip('\n') for line in open("listaNomi.txt")]
cognomiList = [line.rstrip('\n') for line in open("listaCognomi.txt")]
datePeriodList = [line.rstrip('\n') for line in open("datePeriod.txt")]

intenti = [
{'slot':["EntityString","EntityDigit","EntityDateFrom","EntityDateTo",
         "EntityTime","EntityPeriod", "EntityNumberTo","EntityNumberFrom",
         "EntityName","EntitySurname",
         "ndg","EntityCodFisc"],
 'name':"Nome Intento",
 'azione':'    - action_change_page',
 },
]

slotsDict = {
    "EntityTime":'"EntityTime":"{0}"',
    "EntityNumber":'"EntityNumber":"{0}"',
    "EntityCode":'"EntityCode":"{0}"',
    "EntityString":'"EntityString":"{0}"',
    "EntityDateFrom":'"EntityDateFrom":"{0}"',
    "EntityDateTo":'"EntityDateTo":"{0}"',
    "EntityPeriod":'"EntityPeriod":"{0}"',
    "EntityName":'"EntityName":"{0}"',
    "EntitySurname":'"EntitySurname":"{0}"',
    "EntityNumberFrom":'"EntityNumberFrom":"{0}"',
    "EntityNumberTo":'"EntityNumberTo":"{0}"',
    "EntityDigit":'"EntityDigit":"{0}"',
    "EntityCodFisc":'"EntityCodFisc":"{0}"'
    }



domains = {
    "EntityTime":lambda _: "201{0}-{1}-{2}T00:00:00.000Z".format(random.randint(1, 9),str(random.randint(1, 12)).zfill(2),str(random.randint(1, 28)).zfill(2)),
    "EntityNumber":lambda _: random.randint(100, 999),
    "EntityCode":lambda _: ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
    "EntityString":lambda _: random.choice(stringheIn),
    "EntityDateFrom":lambda _: "{2}/{1}/201{0}".format(random.randint(1, 4),str(random.randint(1, 12)).zfill(2),str(random.randint(1, 28)).zfill(2)),
    "EntityDateTo":lambda _: "{2}/{1}/201{0}".format(random.randint(5, 9),str(random.randint(1, 12)).zfill(2),str(random.randint(1, 28)).zfill(2)),
    "EntityPeriod":lambda _: random.choice(datePeriodList),
    "EntityName":lambda _: random.choice(nomiList),
    "EntitySurname":lambda _: random.choice(cognomiList),
    "EntityNumberFrom":lambda _: random.randint(100, 1000),
    "EntityNumberTo":lambda _: random.randint(1001, 5000),
    "EntityDigit":lambda _: randNumPrev(),
    "EntityCodFisc":lambda _: ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)),
    }

def getCombos(slots, i):
    return list(itertools.combinations(slots,i))

def randNumPrev(a = 1111, b = 999999 ):
    return str(int((b-a)*random.random() + a))

  
for i in range(len(intenti)):
    slots = intenti[i]['slot']
    name = intenti[i]['name']
    fine = intenti[i]['azione']
    for j in range(1, len(slots)+1):
        for subset in getCombos(slots, j):
            rngDom = dict((el,domains[el](True)) for el in subset)
            if("EntityDateFrom" not in rngDom.keys()):
                rngDom["EntityDateFrom"] = domains["EntityDateFrom"](True)
            if("EntityDateTo" not in rngDom.keys()):
                rngDom["EntityDateTo"] = domains["EntityDateTo"](True)
            print()
            print("## Generated Story ")
            print()
            pars = ','.join(map(lambda s : slotsDict[s].format(rngDom[s]), subset))
            print('* '+name + '{'+pars+'}')
            for slt in subset:
                print('    - slot{'+slotsDict[slt].format(rngDom[slt])+'}')
            if any(x in subset for x in ["EntityDateFrom","EntityDateTo","EntityPeriod","EntityTime"]):
                print('    - action_convert_date')
                print('    - slot{'+slotsDict["EntityDateFrom"].format(rngDom["EntityDateFrom"])+'}')
                print('    - slot{'+slotsDict["EntityDateTo"].format(rngDom["EntityDateTo"])+'}')
            print(fine)


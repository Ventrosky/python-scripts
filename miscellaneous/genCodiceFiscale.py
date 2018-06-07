#!/usr/bin/python
import sys
from re import findall



fnameCC="codicicatastali2.txt"

consonanti=r'[^aeiou]'
vocali=r'[aeiou]'

person = {
	'nome':"giorgione",
	'cognome':"orwello",
	'anno':1961,
	'mese':"giugno",
	'giorno':12,
	'comune':"ROMA (RM)",
	'sesso' : "M"
}

months = {
	'gennaio' : 'a',
	'febbraio' : 'b',
	'marzo' : 'c',
	'aprile' : 'd',
	'maggio' : 'e',
	'giugno': 'h',
	'luglio' : 'l',
	'agosto' : 'm',
	'settembre' : 'p',
	'ottobre' : 'r',
	'novembre' : 's',
	'dicembre' : 't'
}

charCtrl={
	'0':(1,0),
	'A':(1,0),
	'1':(0,1),
	'B':(0,1),
	'2':(5,2),
	'C':(5,2),
	'3':(7,3),
	'D':(7,3),
	'4':(9,4),
	'E':(9,4),
	'5':(13,5),
	'F':(13,5),
	'6':(15,6),
	'G':(15,6),
	'7':(17,7),
	'H':(17,7),
	'8':(19,8),
	'I':(19,8),
	'9':(21,9),
	'J':(21,9),
	'K':(2,10),
	'L':(4,11),
	'M':(18,12),
	'N':(20,13),
	'O':(11,14),
	'P':(3,15),
	'Q':(6,16),
	'R':(8,17),
	'S':(12,18),
	'T':(14,19),
	'U':(16,20),
	'V':(10,21),
	'W':(22,22),
	'X':(25,23),
	'Y':(24,24),
	'Z':(23,25)
}

dictCC = {}

def loadCodCat(fname, dictCC):
	with open(fname) as f:
    		content = f.readlines()
		for line in content:
			values = line.split("\t")
			dictCC[values[2].strip('\n')] = (values[0] , values[1])	
	return dictCC


def addSumm(c, x):
  return chr(ord(c)+x)

def getControllo(partial):
	sum = 0
	odd = 0
	even = 1
	for c in range(0,len(partial),2):
		sum+=charCtrl[partial[c]][odd]
	for c in range(1,len(partial),2):
		sum+=charCtrl[partial[c]][even]
	resto = sum % 26
	return addSumm('a',resto)

def getDay(giorno, sex):
	return giorno if (sex == 'M') else (giorno + 40)

#test , taken has at least 3 cons
def treCons(str,isName):
	consos= findall(consonanti, str)
	vocals= findall(vocali,str)
	i = 0
	while len(consos) < 3:
		consos.append(vocals[i] if (i < len(vocals)) else 'x')
	if (len(consos)==3):
		return ''.join(consos)
	if(not isName):
		return ''.join(consos[:3])
	else:
		return consos[0]+consos[2]+consos[3]

def buildCF(person):
	cogn= treCons(person["cognome"].lower(),False)
	nome= treCons(person["nome"].lower(),True)
	anno = str(person["anno"])[2:]
	mese = months[person['mese'].lower()]
	gior = str(getDay(person["giorno"], person['sesso'].upper()))
	if (len(gior)==1):
		gior = "0"+gior
	comu = dictCC[person["comune"].upper()][1]
	cfPartial=(cogn+nome+anno+mese+gior+comu).upper()
	cont = getControllo(cfPartial)
	cf =(cfPartial+cont).upper() 
	print "RISULTATO:"
	print person["nome"].upper(),person["cognome"].upper(),", ",person["sesso"]
	print person["giorno"],person["mese"].upper(),person["anno"]," - ", person["comune"].upper()
	print cf

def inputPerson():
	newPerson = {}
	print "Nome e Cognome e Sesso"
	newPerson["nome"] = raw_input("Nome: ")
	newPerson["cognome"] = raw_input("Cognome: ")
	newPerson["sesso"] = raw_input("Sesso: ")
	print "Data di nascita"
	newPerson["giorno"] = int(raw_input("Giorno: "))
	newPerson["mese"] = raw_input("Mese: ")
	newPerson["anno"] = int(raw_input("Anno: "))
	chiave = raw_input("Comune: ")
	if chiave.upper() in dictCC.keys():
		newPerson["comune"] = chiave.upper()
	else:
		print "Formato Comune Errato"
		exit(0)
	print
	return newPerson

def main(option):
	loadCodCat(fnameCC,dictCC)
	cfPerson = person
	if (option):
		cfPerson = inputPerson()
	buildCF(cfPerson)

option = sys.argv[1] if (len(sys.argv)>1) else False
main(option)

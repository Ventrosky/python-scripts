#!/usr/bin/python
# -*- coding: utf-8 -*-

# Progetto di Linguistica  Computazionale - A.A. 2016/2017
#   Programma 1
#   Salvatore Ventrone - 539872

import sys, codecs, nltk, re

def usage():
    print '-'*80
    print "Progetto di Linguistica  Computazionale - Programma 1"
    print
    print "Usage: project1.py text_file1 text_file2"
    print 
    print "Confrontate i due testi sulla base delle seguenti informazioni statistiche:"
    print "- numero  di token;"
    print "- lunghezza media delle frasi in termini di token;"
    print "- grandezza del vocabolario all'aumento del corpus per porzioni incrementali di 1000 token;"
    print "- ricchezza lessicale calcolata attraverso la Type Token Ratio (TTR) all'aumento del corpus;"
    print "- rapporto tra sostantivi e verbi (indice che caratterizza variazioni di registro linguistico);"
    print "- la densità lessicale, (|Sostantivi|+|Verbi|+|Avverbi|+|Aggettivi|)/(TOT-( |.|+|,| ) );"
    print
    print "Examples: "
    print "python project1.py clinton.txt trump.txt"
    print "./project1.py clinton.txt trump.txt > output1.txt"
    print ""
    print '-'*80
    sys.exit(0)

# tokenizza frasi, calcola lunghezza media delle frasi in termini di token;
def estraiTokens(frasi):
    tokensTOT = []
    lenMedia = 0 
    for frase in frasi:
        tokens = nltk.word_tokenize(frase)
        tokensTOT = tokensTOT + tokens # costruisco vettore tokens
        lenMedia = lenMedia + len(frase)
    lenMedia = lenMedia / len(frasi)  # calcolo lunghezza media delle frasi
    return tokensTOT, lenMedia

# apre e tokenizza file di testo, restituisce tokens e lunghezza media frasi 
def openTextFile(file1):
    fileInput = codecs.open(file1, "r", "utf-8")
    raw = fileInput.read()
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    frasi = sent_tokenizer.tokenize(raw)
    tokensTesto, lenMedia = estraiTokens(frasi) # creo il vettore con tokens
    return tokensTesto, lenMedia

#  grandezza del vocabolario e TTR all'aumento del corpus per porzioni incrementali
def analisiInc(t_tokens, max_n, step):
    vocab = set([])
    porzioni = []
    for i in range(step,max_n,step):
        vocab.update(t_tokens[i-step:i]) # aggiorno il vocabolario
        lenV = len(vocab)
        lenC = i
        ttr = (lenV *0.1) / (lenC *0.1) # Type Token Ratio
        porzioni.append((lenC,lenV, ttr))
    return porzioni

# rapporto sostantivi/verbi e densità lessicale
def analisiPOS(t_tokens):
    testoPOS = nltk.pos_tag(t_tokens) # analisi morfo-sintattica
    dictPOS = {}
    dictPOS["sostantivi"] = 0
    dictPOS["verbi"] = 0
    dictPOS["avverbi"] = 0
    dictPOS["aggettivi"] = 0
    dictPOS["puntegg."] = 0
    # conto i diversi POS rilevanti
    for bigramma in testoPOS:
        # controllo la categoria del POS verificandone i primi 2 caratteri
        if re.search(r'^NN', bigramma[1]): 
            dictPOS["sostantivi"] = dictPOS["sostantivi"] + 1
        elif re.search(r'^VB', bigramma[1]):
            dictPOS["verbi"] = dictPOS["verbi"] + 1
        elif re.search(r'^RB', bigramma[1]):
            dictPOS["avverbi"] = dictPOS["avverbi"] + 1
        elif re.search(r'^JJ', bigramma[1]):
            dictPOS["aggettivi"] = dictPOS["aggettivi"] + 1
        elif bigramma[1] in ['.', ',']:
            dictPOS["puntegg."] = dictPOS["puntegg."] + 1
    # indice che caratterizza variazioni di registro linguistico
    idxVarRegistro = (dictPOS["sostantivi"] *0.1) / (dictPOS["verbi"] *0.1) 
    densitaLessicale = ((dictPOS["sostantivi"] + dictPOS["verbi"] + dictPOS["avverbi"] + dictPOS["aggettivi"]) *0.1)/ ((len(testoPOS) - dictPOS["puntegg."]) *0.1)
    return idxVarRegistro, densitaLessicale

def main():
    if not len(sys.argv[1:]):
        usage()
    # nomi dei file passati come argomenti
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    print '-'*80
    print " Progetto di Linguistica  Computazionale"
    print " Programma 1 "
    print '-'*80
    # tokens del testo e lunghezza media delle frasi
    tokensText1, lenMediaFrasi1 = openTextFile(file1)
    tokensText2, lenMediaFrasi2 = openTextFile(file2)
    print '-'*80
    print " Numero di token"
    print '-'*80
    print "", file1, "\t=", len(tokensText1)
    print "", file2, "\t=", len(tokensText2)
    print '-'*80
    print " Lunghezza media delle frasi"
    print '-'*80
    print "", file1, "\t=", lenMediaFrasi1, "token"
    print "", file2, "\t=", lenMediaFrasi2, "token"
    print '-'*80
    # calcolo grandezza del vocabolario  e TTR  all'aumento  del  corpus per porzioni  incrementali
    porzioniInc1 = analisiInc(tokensText1, len(tokensText1), 1000)
    porzioniInc2 = analisiInc(tokensText2, len(tokensText2), 1000)
    print '-'*80
    print " Grandezza vocabolario e TTR all'aumento del corpus per porzioni  incrementali"
    print '-'*80
    print ' Testo',' '*15, '|C|',' '*6, '|V|',' '*6, 'Type Token Ration'
    print '-'*80
    for i in range(min(len(porzioniInc1),len(porzioniInc2))): # se |C1| != |C2| stampo i confronti fino alla cardinalità minore
        C1, V1, TTR1 = porzioniInc1[i]
        C2, V2, TTR2 = porzioniInc2[i]
        print " {: <21}{: <12}{: <15}{: <10}".format(file1, C1, V1, TTR1)
        print " {: <21}{: <12}{: <15}{: <10}".format(file2, C2, V2, TTR2)
    print '-'*80
    # calcolo rapporto sostantivi/verbi e densità lessicale
    idxVarRegistro1, densitaLessicale1 = analisiPOS(tokensText1)
    idxVarRegistro2, densitaLessicale2 = analisiPOS(tokensText2)
    print '-'*80
    print " Rapporto tra sostantivi e verbi"
    print '-'*80
    print "", file1, "\t= %.4f" % idxVarRegistro1
    print "", file2, "\t= %.4f" % idxVarRegistro2
    print '-'*80
    print " Densità lessicale"
    print '-'*80
    print "", file1, "\t= %.4f" % densitaLessicale1
    print "", file2, "\t= %.4f" % densitaLessicale2
    print '-'*80
    sys.exit(2)

main() 

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Progetto di Linguistica  Computazionale - A.A. 2016/2017
#   Programma 2
#   Salvatore Ventrone - 539872

import sys, codecs, nltk, re, math
from nltk import bigrams, trigrams
from decimal import Decimal, ROUND_DOWN

def usage():
    print '-'*80
    print "Progetto di Linguistica  Computazionale - Programma 2"
    print
    print "Usage: project2.py text_file1 text_file2"
    print 
    print "Estraete ed ordinate in ordine di frequenza decrescente, indicando la relativa frequenza:"
    print "- le  10 PoS (Part-of-Speech)  più  frequenti;"
    print "- i 20 token  più  frequenti  escludendo  la  punteggiatura;"
    print "- i 20 bigrammi di token più frequenti che non contengono punteggiatura, articoli e congiunzioni;"
    print "- i 20 trigrammi di token più frequenti che non contengono punteggiatura, articoli e congiunzioni;"
    print "Estraete ed ordinate i 20 bigrammi (Aggettivo, Sostantivo) dove ogni frequenza(token) > 2:"
    print "- con probabilità congiunta massima, indicandone la probabilità;"
    print "- con probabilità condizionata massima, indicandone la probabilità;"
    print "- con forza associativa (Local Mutual Information) massima, indicandone forza associativa;"
    print "Le due frasi con probabilità più alta:"
    print "- prima frase calcolata attraverso un modello di Markov di ordine 0;"
    print "- seconda con un modello di Markov  di  ordine  1;"
    print "- i due modelli devono usare le statistiche estratte dal corpus che contiene le frasi;"
    print "- frasi lunghe almeno 10 token, ogni token deve avere una frequenza maggiore di 2;"
    print "Dopo aver individuato e classificato le Entità Nominate (NE) presenti nel testo, estraete:"
    print "- i 20 nomi propri di persona più frequenti (tipi), ordinati per frequenza;"
    print "- i 20 nomi propri di luogo più frequenti (tipi), ordinati per frequenza."
    print
    print "Examples: "
    print "python project2.py clinton.txt trump.txt"
    print "./project2.py clinton.txt trump.txt > output2.txt"
    print ""
    print '-'*80
    sys.exit(0)

# tutti tokens con almeno freq. 2
def frasiPerMarkov(frasi, tokensTOT):
    distrFreq = nltk.FreqDist(tokensTOT)
    frasiMarkov = []
    for frase in frasi: # frasi gia di len >= 10
        freq = list(map(lambda x: distrFreq[x], frase)) # creo vettore di frequenze dei token
        if not 1 in freq: # controllo se nessun token appare solo 1 volta nel testo 
            frasiMarkov.append(frase)
    return frasiMarkov

# tokenizza frasi
def estraiTokens(frasi):
    tokensTOT = []
    frasiLunghe = [] # vettore frasi almeno 10 token
    for frase in frasi:
        tokens = nltk.word_tokenize(frase)
        if len(tokens) > 9:
            frasiLunghe.append(tokens)
        tokensTOT = tokensTOT + tokens # costruisco vettore tokens
    frasiMarkov = frasiPerMarkov(frasiLunghe, tokensTOT) # ogni token deve avere una frequenza maggiore di 2 
    return tokensTOT, frasiMarkov

# apre e tokenizza file di testo, restituisce tokens
def openTextFile(file1):
    fileInput = codecs.open(file1, "r", "utf-8")
    raw = fileInput.read()
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    frasi = sent_tokenizer.tokenize(raw)
    tokensTesto, frasiMarkov = estraiTokens(frasi) # creo il vettore con tokens, restituisco frasi per esercizio Markov
    return tokensTesto, frasiMarkov, frasi

#inserisce elementi POS in una lista
def estraiSeqPOS(testoPOS):
    listaPOS = []
    for bigramma in testoPOS:
        listaPOS.append(bigramma[1])
    return listaPOS

# analisi morfosintattica ed Entità Nominate (NE)
def analisiLing(frasi):
    namedEntityDict = { "PERSON" : [], "GPE" : []}
    tokensPOStot=[]
    for frase in frasi:
        tokens = nltk.word_tokenize(frase)
        tokensPOS = nltk.pos_tag(tokens)
        analisi = nltk.ne_chunk(tokensPOS)
        for nodo in analisi: # ciclo albero scorrendo nodi
            NE = ''
            if hasattr(nodo, 'label'): #controlla se chunk è un nodo intermedio
                if nodo.label() in ["PERSON", "GPE"]: # nomi propri di persona o luogo
                    for partNE in nodo.leaves(): # ciclo foglie nodo selezionato
                        NE = NE+' '+partNE[0]
                    namedEntityDict[nodo.label()].append(NE)
        tokensPOStot = tokensPOStot + tokensPOS 
    return tokensPOStot, namedEntityDict 

# 10 PoS (Part-of-Speech)  più  frequenti;"
def top10POS(tokensPOS):
    seqPOS = estraiSeqPOS(tokensPOS)
    freqDist = nltk.FreqDist(seqPOS)
    return freqDist.most_common(10)

# restituisce i bigrammi
def getBigrams(tokens):
    bigrams1 = list(bigrams(tokens))
    return bigrams1

# restituisce i trigrammi
def getTrigrams(tokens):
    trigrams1 = list(trigrams(tokens))
    return trigrams1

# 20 token più frequenti
def top20Tokens(tokens1):
    esclusi = [',','.',':',';'] #non contenenti punteggiatura
    nonPunteggiatura = [ a[0] for (a, b) in tokens1 if not (a[1] in esclusi)]
    fdist = nltk.FreqDist(nonPunteggiatura)
    return fdist.most_common(20)
    
# 20 bigrammi di token più frequenti
def top20Bigrams(bigrams1):
    esclusi = [',','.',':',';','DT','CC'] #non contenenti punteggiatura, articoli e congiunzioni
    nonPunteggiatura = [(a[0], b[0]) for (a, b) in bigrams1 if not (b[1] in esclusi) and not (a[1] in esclusi)]
    fdist = nltk.FreqDist(nonPunteggiatura)
    return fdist.most_common(20)
    
# 20 trigrammi di token più frequenti
def top20Trigrams(trigrams1):
    esclusi = [',','.',':',';','DT','CC'] #non contenenti punteggiatura, articoli e congiunzioni
    nonPunteggiatura = [(a[0], b[0], c[0]) for (a, b, c) in trigrams1 if not (b[1] in esclusi) and not (a[1] in esclusi) and not (c[1] in esclusi)]
    fdist = nltk.FreqDist(nonPunteggiatura)
    return fdist.most_common(20)

# restituisce vero se il PoS tag si riferisce ad aggettivo e sostantivo
def isAggAndSos(tag1, tag2):
    return (re.search(r'^JJ', tag1) and re.search(r'^NN', tag2))

# bigrammi aggettivo e sostantivo, frequenza(token) > 2
def bigrammiAggSos(tokensPOS):
    bigramsAggSos = [(a[0], b[0]) for (a, b) in tokensPOS if isAggAndSos(a[1],b[1])] 
    return bigramsAggSos

# dizionario {"token" : (freq_as, freq_rel)}
def dictVocabFreq(vocab, t_tokens):
    v = {}
    c = len(t_tokens)
    freq = 0
    for tok in vocab:
        freq=t_tokens.count(tok)
        v[tok] = (freq, (freq *1.0 / c *1.0))
    return v

# dato dizionario ordina per valore
def ordinaDict(dictFreq):
    return sorted(dictFreq.items(), key = lambda x: x[1], reverse = True)

# dato dizionario ordina per valore v[4] # P(u,v)
def ordinaProbCongiunta(dictFreq):
    return sorted(dictFreq.items(), key = lambda x: x[1][4], reverse = True)

# dato dizionario ordina per valore v[3] # P(v|u) 
def ordinaProbCondizionata(dictFreq):
    return sorted(dictFreq.items(), key = lambda x: x[1][3], reverse = True)

# crea dizionario {"bigramma" : (F(u,v), F(u), F(v), P(v|u), P(u,v))}
def infoBigrams(bigrams1, setBigramsAggSost,vocabFreq):
    b_infos = {}
    freq = 0
    for b in setBigramsAggSost:
        freq = bigrams1.count(b)
        u = b[0]
        v = b[1]
        f_u = vocabFreq[u][0] #freq. assoluta di u
        f_u_r = vocabFreq[u][1] #freq. relativa di u
        f_v = vocabFreq[v][0]
        p_uv1 = (freq *1.0 / f_u *1.0) # P(v|u) probabilità condizionata
        p_uv2 = (f_u_r * p_uv1) # P(u,v) probabilità congiunta
        b_infos[b] = (freq, f_u, f_v, p_uv1, p_uv2) # memorizzo F(u,v), F(u), F(v), P(v|u), P(u,v)
    return b_infos

# calcola Local Mutual Information dei bigrammi
def getLocalMutualInformation(bigramsDict, vocabFreq):
    mi = {}
    for k,v in bigramsDict.items():
        u1 = k[0]
        u2 = k[1]
        p_uv = v[4] # P(u,v)
        mi1 = (p_uv / (vocabFreq[u1][1] * vocabFreq[u2][1])) # mi1 = P(u,v)/(P(u)*P(v))
        mi[k] = math.log( mi1, 2) * v[0] # log2(mi1) * f(<u,v>) = Local Mutual Information
    return mi

# Calcola Probabilita Frase Markov 0
def probabilitaMarkov0(lenCorpus, distrFreq, frase):
    probabilita = 1.0
    for tok in frase:
        probabilitaToken = (distrFreq[tok]*1.0 / lenCorpus*1.0)
        probabilita = probabilita * probabilitaToken # P(w1, w2,...,wn)=P(w1)*P(w2)*...*P(wn)
    return probabilita

# restituisce la frase Markov 0 con probabilità più alta
def maxProbMarkov0(lenCorpus, distrFreq, frasi):
    probFraseMax = 0
    topFrase = []
    for frase in frasi:
        p = probabilitaMarkov0(lenCorpus, distrFreq, frase) # Probabilita Frase Markov 0 
        if p > probFraseMax:
            probFraseMax = p
            topFrase = frase
    return topFrase, probFraseMax

# Calcola Probabilita Frase Markov 1; bigramInfos = { bigramma : (F(u,v), F(u), F(v), P(v|u), P(u,v))}
def probabilitaMarkov1(lenCorpus, frase, bigramInfos): 
    probabilita = 1
    w1 = frase[0]
    primaParola = True
    for tok in frase[1:]:
        w2 = tok
        if primaParola:
            probabilita = ( bigramInfos[(w1,w2)][2] *1.0 / lenCorpus*1.0) #calcolo prob prima parola
            primaParola = False
        probabilitaBigramma = bigramInfos[(w1,w2)][3] # P(v|u)
        probabilita = probabilita * probabilitaBigramma #P(w1, w2,...,wn)=P(w1)*P(w2|w1)*P(w3|w2)*...*P(wn|wn-1)
        w1 = w2
    return probabilita

# restituisce la frase Markov 1 con probabilità più alta
def maxProbMarkov1(lenCorpus, frasi, bigramInfos):
    probFraseMax = 0
    topFrase = []
    for frase in frasi:
        p = probabilitaMarkov1(lenCorpus, frase, bigramInfos) # Probabilita Frase Markov 1 
        if p > probFraseMax:
            probFraseMax = p
            topFrase = frase
    return topFrase, probFraseMax

def main():
    if not len(sys.argv[1:]):
        usage()
    # nomi dei file passati come argomenti
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    print '-'*80
    print " Progetto di Linguistica  Computazionale"
    print " Programma 2 "
    print '-'*80
    tokensText1, frasiMarkov1, frasi1 = openTextFile(file1) # tokens del testo, frasi per es. Markov
    tokensText2, frasiMarkov2, frasi2 = openTextFile(file2)
    tokensPOS1, namedEntityDict1 = analisiLing(frasi1) # processo di annotazione ed NE
    tokensPOS2, namedEntityDict2  = analisiLing(frasi2)
    top10POS1 = top10POS(tokensPOS1) #10 PoS più frequenti
    top10POS2 = top10POS(tokensPOS2)
    print '-'*80
    print " 10 PoS (Part-of-Speech) più frequenti"
    print '-'*80
    print ' Testo:', file1,' '*12, '| Testo:', file2
    print '-'*80
    for i in range(min(len(top10POS1),len(top10POS2))): # stampa il confronto
        pos1, freq1 = top10POS1[i]
        pos2, freq2 = top10POS2[i]
        print " {: <20}{: <12}| {: <20}{: <12}".format(pos1, freq1, pos2, freq2)
    print '-'*80
    print " 20 Token più  frequenti"
    print '-'*80
    print ' Testo:', file1,' '*12, '| Testo:', file2
    print '-'*80
    topTokens1 = top20Tokens(getBigrams(tokensPOS1)) #20 Token più  frequenti
    topTokens2 = top20Tokens(getBigrams(tokensPOS2))
    for i in range(min(len(topTokens1),len(topTokens2))): # stampa il confronto
        tok1, freq1 = topTokens1[i]
        tok2, freq2 = topTokens2[i]
        print " {: <25}{: <7}| {: <25}{: <7}".format(tok1.encode('utf-8'), freq1, tok2.encode('utf-8'), freq2)
    print '-'*80
    print '-'*80
    print " 20 Bigrammi più frequenti"
    print '-'*80
    print ' Testo:', file1,' '*12, '| Testo:', file2
    print '-'*80
    bigrammi1 = getBigrams(tokensPOS1) # Bigrammi del testo annotati
    bigrammi2 = getBigrams(tokensPOS2)
    topBigrams1 = top20Bigrams(bigrammi1) #20 Bigrammi più frequenti
    topBigrams2 = top20Bigrams(bigrammi2)
    for i in range(min(len(topBigrams1),len(topBigrams2))): # stampa il confronto
        big1, freq1 = topBigrams1[i]
        big2, freq2 = topBigrams2[i]
        print " {: <25}{: <7}| {: <25}{: <7}".format(big1[0].encode('utf-8') + " " +big1[1].encode('utf-8'), freq1, big2[0].encode('utf-8') + " " +big2[1].encode('utf-8'), freq2)
    print '-'*80
    print " 20 Trigrammi più frequenti"
    print '-'*80
    print ' Testo:', file1,' '*18, '| Testo:', file2
    print '-'*80
    topTrigrams1 = top20Trigrams(getTrigrams(tokensPOS1)) #20 Trigrammi più frequenti
    topTrigrams2 = top20Trigrams(getTrigrams(tokensPOS2))
    for i in range(min(len(topTrigrams1),len(topTrigrams2))): # stampa il confronto
        tri1, freq1 = topTrigrams1[i]
        tri2, freq2 = topTrigrams2[i]
        print " {: <35}{: <3}| {: <35}{: <3}".format(tri1[0].encode('utf-8')+" "+tri1[1].encode('utf-8')+" "+tri1[2].encode('utf-8'), freq1, tri2[0].encode('utf-8') +" "+tri2[1].encode('utf-8')+" "+tri2[2].encode('utf-8'), freq2)
    print '-'*80
    print '-'*80
    print " 20 Bigrammi - Aggettivo e Sostantivo"
    print '-'*80
    setBigramsAggSost1 = bigrammiAggSos(bigrammi1) # Set di Bigrammi: aggettivo , sostantivo
    setBigramsAggSost2 = bigrammiAggSos(bigrammi2)
    vocabFreq1 = dictVocabFreq(set(tokensText1), tokensText1) # dizionario con tokens e frequenze
    vocabFreq2 = dictVocabFreq(set(tokensText2), tokensText2)
    bigrams1 = getBigrams(tokensText1) # Bigrammi del testo non annotati
    bigrams2 = getBigrams(tokensText2)
    dictBigrammi1 = infoBigrams(bigrams1, setBigramsAggSost1, vocabFreq1) # dizionario con info bigrammi_AggSost : (F(u,v), F(u), F(v), P(v|u), P(u,v))
    dictBigrammi2 = infoBigrams(bigrams2, setBigramsAggSost2, vocabFreq2)
    forzaAssoc1 = getLocalMutualInformation(dictBigrammi1, vocabFreq1) # Local Mutual Information
    forzaAssoc2 = getLocalMutualInformation(dictBigrammi2, vocabFreq2) 
    print " Con probabilità congiunta massima P(u,v):"
    print ' Testo:', file1,' '*12, '|    Testo:', file2
    print '-'*80
    probCongiunta1 = ordinaProbCongiunta(dictBigrammi1)[:20]
    probCongiunta2 = ordinaProbCongiunta(dictBigrammi2)[:20]
    for i in range(min(len(probCongiunta1), len(probCongiunta2))): # stampa il confronto
        big1, p1 = probCongiunta1[i]
        big2, p2 = probCongiunta2[i]
        p1 = Decimal(str(p1[4])).quantize(Decimal('.00001'), rounding=ROUND_DOWN)
        p2 = Decimal(str(p2[4])).quantize(Decimal('.00001'), rounding=ROUND_DOWN)
        print " {: <25}{: <7}|    {: <25}{: <7}".format(big1[0].encode('utf-8') + " " +big1[1].encode('utf-8'), p1, big2[0].encode('utf-8') + " " +big2[1].encode('utf-8'), p2)
    
    print '-'*80
    print " Con probabilità condizionata massima P(v|u):"
    print ' Testo:', file1,' '*12, '|    Testo:', file2
    print '-'*80
    probCondizionata1 = ordinaProbCondizionata(dictBigrammi1)[:20]
    probCondizionata2 = ordinaProbCondizionata(dictBigrammi2)[:20]
    for i in range(min(len(probCondizionata1),len(probCondizionata2))): # stampa il confronto
        big1, p1 = probCondizionata1[i]
        big2, p2 = probCondizionata2[i]
        p1 = Decimal(str(p1[3])).quantize(Decimal('.0001'), rounding=ROUND_DOWN)
        p2 = Decimal(str(p2[3])).quantize(Decimal('.0001'), rounding=ROUND_DOWN)
        print " {: <25}{: <7}|    {: <25}{: <7}".format(big1[0].encode('utf-8') + " " +big1[1].encode('utf-8'), p1, big2[0].encode('utf-8') + " " +big2[1].encode('utf-8'), p2)
    
    print '-'*80
    print " Con forza associativa massima (LMI):"
    print ' Testo:', file1,' '*12, '|    Testo:', file2
    print '-'*80
    topLMI1 = ordinaDict(forzaAssoc1)[:20]
    topLMI2 = ordinaDict(forzaAssoc2)[:20]
    for i in range(min(len(topLMI1),len(topLMI2))): # stampa il confronto
        big1, lmi1 = topLMI1[i]
        big2, lmi2 = topLMI2[i]
        lmi1 = Decimal(str(lmi1)).quantize(Decimal('.001'), rounding=ROUND_DOWN)
        lmi2 = Decimal(str(lmi2)).quantize(Decimal('.001'), rounding=ROUND_DOWN)
        print " {: <25}{: <7}|    {: <25}{: <7}".format(big1[0].encode('utf-8') + " " +big1[1].encode('utf-8'), lmi1, big2[0].encode('utf-8') + " " +big2[1].encode('utf-8'), lmi2)
    print '-'*80
    print '-'*80
    print " Le due frasi con probabilità più alta"
    print '-'*80
    distrFreq1 = nltk.FreqDist(tokensText1)
    topFrase1, probFraseMax1 = maxProbMarkov0(len(tokensText1),distrFreq1, frasiMarkov1) # frase Markov 0 con probabilità più alta
    print " 1° Frase calcolata attraverso un modello di Markov di ordine 0:"
    print '-'*80
    print ' Testo:', file1
    print ' "'," ".join(topFrase1).encode('utf-8'),'"'
    print " Probabilità:", probFraseMax1
    print
    distrFreq2 = nltk.FreqDist(tokensText2)
    topFrase2, probFraseMax2 = maxProbMarkov0(len(tokensText2),distrFreq2, frasiMarkov2) # frase Markov 0 con probabilità più alta
    print ' Testo:', file2
    print ' "'," ".join(topFrase2).encode('utf-8'),'"'
    print " Probabilità:", probFraseMax2
    print '-'*80
    infoBigrammi1 = infoBigrams(bigrams1, set(bigrams1), vocabFreq1) # dizionario con info bigrammi : (F(u,v), F(u), F(v), P(v|u), P(u,v))
    infoBigrammi2 = infoBigrams(bigrams2, set(bigrams2), vocabFreq2)
    topFrase1, probFraseMax1 = maxProbMarkov1(len(tokensText2),frasiMarkov1, infoBigrammi1) # frase Markov 1 con probabilità più alta    
    print " 2° Frase calcolata attraverso un modello di Markov di ordine 1:"
    print '-'*80
    print ' Testo:', file1
    print ' "'," ".join(topFrase1).encode('utf-8'),'"'
    print " Probabilità:", probFraseMax1
    print
    distrFreq2 = nltk.FreqDist(tokensText2)
    topFrase2, probFraseMax2 = maxProbMarkov1(len(tokensText2),frasiMarkov2, infoBigrammi2) # frase Markov 1 con probabilità più alta
    print ' Testo:', file2
    print ' "'," ".join(topFrase2).encode('utf-8'),'"'
    print " Probabilità:", probFraseMax2
    print '-'*80
    print '-'*80
    print " 20 nomi propri di persona più frequenti"
    print ' Testo:', file1,' '*18, '|    Testo:', file2
    print '-'*80
    topPerson1 = nltk.FreqDist(namedEntityDict1["PERSON"]).most_common(20) #i 20 nomi propri di persona più frequenti
    topPerson2 = nltk.FreqDist(namedEntityDict2["PERSON"]).most_common(20)
    for i in range(min(len(topPerson1),len(topPerson2))): # stampa il confronto
        tok1, freq1 = topPerson1[i]
        tok2, freq2 = topPerson2[i]
        print " {: <35}{: <3}| {: <35}{: <3}".format(tok1.encode('utf-8'), freq1, tok2.encode('utf-8'), freq2)
    print '-'*80
    print " 20 nomi propri di luogo più frequenti"
    print ' Testo:', file1,' '*18, '|    Testo:', file2
    print '-'*80
    topGpe1 = nltk.FreqDist(namedEntityDict1["GPE"]).most_common(20) #i 20 nomi propri di luogo più frequenti
    topGpe2 = nltk.FreqDist(namedEntityDict2["GPE"]).most_common(20)
    for i in range(min(len(topGpe1),len(topGpe2))): # stampa il confronto
        tok1, freq1 = topGpe1[i]
        tok2, freq2 = topGpe2[i]
        print " {: <35}{: <3}| {: <35}{: <3}".format(tok1.encode('utf-8'), freq1, tok2.encode('utf-8'), freq2)
    print '-'*80
    sys.exit(2)

main() 


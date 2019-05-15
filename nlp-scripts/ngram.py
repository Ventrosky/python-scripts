# -*- coding: utf-8 -*-
from pprint import pprint
import sys, nltk, codecs, json
from nltk.tokenize import TweetTokenizer

def estraiTokens(frasi):
    tokensTOT = []
    lenMedia = 0 
    for frase in frasi:
        tokens = nltk.word_tokenize(frase)
        tokensTOT = tokensTOT + tokens 
        lenMedia = lenMedia + len(frase)
    lenMedia = lenMedia / len(frasi)
    return tokensTOT, lenMedia

def openTextFile(file1):
    fileInput = codecs.open(file1, "r", "utf-8", errors='ignore')
    raw = fileInput.read()
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    frasi = sent_tokenizer.tokenize(raw)
    #tokenizer = TweetTokenizer()
    #frasi = tokenizer.tokenize(raw)
    tokens, media = estraiTokens(frasi)
    return tokens, media

def remapKeys(mapping):
    return dict((' '.join(map(str, key)), dict(value)) for (key, value) in mapping.items())

def filterNgrams(ngrams):
    return [p for p in ngrams if all(w != '.' for w in p)] 

def makeTrigramFreq(tokens):
    tgs = filterNgrams(list(nltk.trigrams(tokens)))
    a,b,c = list(zip(*tgs))
    bgs = list(zip(a,b))
    cfd = nltk.ConditionalFreqDist(list(zip(bgs, c)))
    with open('freqTrigrams.json', 'w') as f:
        json.dump(remapKeys(cfd),f)
    return cfd

def makeBigramFreq(tokens):
    bgs = filterNgrams(list(nltk.bigrams(tokens)))
    cfd = nltk.ConditionalFreqDist(bgs)
    with open('freqBigrams.json', 'w') as g:
        json.dump(cfd, g)
    return cfd

def prediction(string):
    words=string.split()
    n=len(words)
    if n==1:
        return json.dumps(bgs_freq[(string)].most_common(5))
    elif n>1:
        return json.dumps(tgs_freq[(words[n-2],words[n-1])].most_common(5))

     
if __name__=="__main__":
    tokens, lenMedia = openTextFile('corpusTrick.txt')
    bgs_freq = makeBigramFreq(tokens)
    tgs_freq = makeTrigramFreq(tokens)
    #print(prediction("vorrei emettere una"))
    #print(prediction("vorrei visualizzare"))
    #print(prediction("cerca"))

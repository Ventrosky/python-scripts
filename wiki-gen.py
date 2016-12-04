# -*- coding: utf-8 -*-

import wikipedia
import nltk
import random
import codecs
import sys
import getopt
import warnings

# global variables
min_tokens = 1000
prefixes = ["en","simple"]
file_name = "wikiC"
info = False

def usage():
    print '-'*80
    print "Wikipedia Corpus Generator"
    print " Generates two corpus using summaries from wikipedia ['en','simple']"
    print
    print "Usage: wiki-gen.py -n 'file_name'"
    print "-n --name=file           - generated corpus file name"
    print "-e --en                  - generate only 1 corpus from wiki 'en'" 
    print "-t --tokens=min          - minimum number of tokens for each corpus, default 1000"
    print "-i --info                - generate informations file"
    print
    print
    print "Examples: "
    print "wiki-gen.py -n 'corpus' -i"
    print "wiki-gen.py -n 'corpus' -e -t 10000"
    print ""
    print '-'*80
    sys.exit(0)

def getTitle():
  return wikipedia.random(pages=1)

def getPage(title):
  return wikipedia.page(title)

def getSummary(title):
  p = ""
  try:
    p = wikipedia.summary(title)
  except wikipedia.exceptions.DisambiguationError as e:
    p = getSummary(random.choice(e.options))
  except wikipedia.exceptions.PageError as e:
    return None  
  return p

def findSummary(t):
  new_title = getTitle()
  while new_title in t:
    new_title = getTitle()
  return (new_title, getSummary(new_title))

def lenFrasi(summary):
  sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
  frasi = sent_tokenizer.tokenize(summary)
  lunghezza = 0
  tokensTot = []
  for frase in frasi:
    tokens = nltk.word_tokenize(frase)
    tokensTot = tokensTot + tokens
  lunghezza = len(tokensTot)
  return (lunghezza, tokensTot)

def minCorpus(min, n, titles, corpus):
  while n < min:
    t,s = findSummary(titles)
    if not s is None:
        titles.append(t)
        corpus = corpus + "\n\n" + s
        l, t = lenFrasi(s)
        n = n + l
  return (corpus, titles, n)

def writeCorpus(name, c):
  file = codecs.open(name, "w", "utf-8")
  file.write(c)
  file.close()
  print "File name:", name

def createCorpus(fileName, prefix, tokens_min, info):
  i = ""
  for p in prefix:
    wikipedia.set_lang(p)
    corpus, titles, act_tokens = minCorpus(tokens_min,0,[],"")
    i = i + makeDescription(titles, act_tokens, p) + "\n"
    writeCorpus(fileName+"_"+p+".txt", corpus)
  if info:
      writeCorpus("info_corpus.txt", i)
      
def makeDescription(titles, act_tokens, prefix):
  desc = "Corpus created from Wikipidia "+prefix+"\nSummaries from the following pages:\n"
  for t in titles:
    desc = desc + " " + t +";"
  desc = desc + "\n Number of tokens: " + str(act_tokens) + "\n\n"
  return desc

def main():
    global min_tokens
    global prefixes
    global file_name
    global info
    
    if not len(sys.argv[1:]):
        usage()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'n:et:ih', ['name=', 'en', 'tokens=', 'info', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-n', '--name'):
            file_name = arg
        elif opt in ('-e', '--en'):
            prefixes = ['en']
        elif opt in ('-t', '--tokens'):
            min_tokens = int(arg)
        elif opt in ('-i', '--info'):
            info = True
        else:
            usage()
            sys.exit(2)
            
    print '-'*80
    print "Wikipedia Corpus Generator"
    print '-'*80
    warnings.filterwarnings('error')
    try:
        createCorpus(file_name,prefixes, min_tokens, info)
    except UserWarning:
        print 'Suppressed warnings'
        createCorpus(file_name,prefixes, min_tokens, info)
    print '-'*80
    print "Process Completed"
    print '-'*80
    sys.exit(2)
    
main() 

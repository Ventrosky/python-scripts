#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import nltk
import codecs
import re
import math
from decimal import Decimal, ROUND_DOWN
from nltk import bigrams, trigrams

# global variables
codec1              = "utf-8"
text1               = ""
text1tokens         = []
vocab1              = set([])
max_freq            = 0
hapax               = False
normalize           = False
vocabolary          = False
growth              = 0
bigrams_infos       = False
text1bigrams        = []
mutual_info         = False
text1trigrams       = []
trigrams_infos      = False

def usage():
    print '-'*80
    print "Texts and Words Tool"
    print
    print "Usage: tw-tool.py -t text_file1"
    print "-m --max_freq=char_num   - find the token (len >= char_num) with maximum frequency"
    print "-x --hapax               - print hapax and their distribution"
    print "-e --encoding=codec      - select character sets, default 'utf-8'"
    print "-n --normalize           - remove curly quotes"
    print "-v --vocabolary          - informations on type words"
    print "-g --growth=step         - growth of statistical indexes, inc text by [step]"
    print "-b --bigrams_infos       - bigrams infos: F(u,v), F(u), F(v), P(v|u), P(u,v)"
    print "-i --mutual-information  - print the Mutual Information of each bigram"
    print "-r --trigrams_infos      - top 50 frequent trigrams"
    print
    print
    print "Examples: "
    print "tw-tool.py -t alice.txt -n -m 4 -x"
    print "tw-tool.py -t 1984.txt -e ascii -n -v"
    print "tw-tool.py -t hacethi.txt -e ascii -g 50"
    print "tw-tool.py -t rome.txt -b -i -r"
    print ""
    print '-'*80
    sys.exit(0)

#  "normalize" spaces, hyphens, quotation marks # TO DO
def textNormalize(words):
    re_sub_table = {
        r'\u200[23456]' : ' ',
        r'\u201[012345]': '-',
        r'\u201[89ab]'  : "'",
        r'\u201[cdef]'  : '"',
        }
    return words      

# (max frequence, token)
def maxFreqToken(t_tokens, vocab, n):
    max_tok = ""
    max_freq = 0
    for tok in vocab:
        if len(tok) >= n:
            freq_tok=t_tokens.count(tok)
            if freq_tok > max_freq:
                max_freq = freq_tok
                max_tok = tok
    return (max_freq, max_tok)

# vocabolary infos
def infoVocab(vocab, t_tokens):
    v = {}
    c = len(t_tokens)
    freq = 0
    for tok in vocab:
        freq=t_tokens.count(tok)
        v[tok] = (freq, (freq *1.0 / c *1.0))
    return v

# bigrams infos
def infoBigrams(bigrams1, bigrams1diff,v_infos):
    b_infos = {}
    freq = 0
    for b in bigrams1diff:
        freq = bigrams1.count(b)
        # store F(u,v), F(u), F(v), P(v|u), P(u,v)
        u = b[0]
        v = b[1]
        f_u = v_infos[u][0]#absolute freq. of u
        f_u_r = v_infos[u][1] #relative freq of u
        f_v = v_infos[v][0]
        p_uv1 = (freq *1.0 / f_u *1.0) # P(v|u)
        p_uv2 = (f_u_r * p_uv1) # P(u,v)
        b_infos[b] = (freq, f_u, f_v, p_uv1, p_uv2)
    return b_infos

# calculate Mutual Information 
def getMutualInformation(bigs_info, f_vocab):
    mi = {}
    for k,v in bigs_info.items():
        u1 = k[0]
        u2 = k[1]
        p_uv = v[4]
        mi1 = (p_uv / (f_vocab[u1][1] * f_vocab[u2][1]))
        mi[k] = math.log( mi1, 2) # log2(P(u,v)/(P(u)*P(v)))
    return mi

# hapaxs and distribution
def getHapaxs(t_tokens, vocab):
    lst = []
    for tok in vocab:
        if t_tokens.count(tok) == 1:
            lst.append(tok)
    dist = len(lst) * 1.0 / len (t_tokens) * 1.0    
    return lst, dist

# returns a dict of freq. classes
def freqClasses(classes, vocab):
    freq_c = {}
    freqs = vocab.values()
    for c in classes:
        freq_c[c] = freqs.count(c)
    return freq_c

# statistical indexes growth
def indexGrowth(t_tokens, max_n, step):
    si_growth = {}
    #vocab = set([])
    vocab = {}
    for i in range(step,max_n,step):
        for tok in t_tokens[i-step:i]:
            if tok in vocab:
                vocab[tok] = vocab[tok]+1
            else:
                vocab[tok] = 1
            f_class = freqClasses([1, 5, 10, 15], vocab)
            d = f_class[1] * 1.0 / i * 1.0
            si_growth[i] = (len(vocab), d, f_class[5], f_class[10], f_class[15])
    return si_growth

# return bigrams
def getBigrams(t_tokens):
    bigrams1 = list(bigrams(t_tokens))
    bigrams1diff = set(bigrams1)
    return (bigrams1, bigrams1diff)

# list of tokens from file
def readLocalFile(file1, codec, norm):
    f = codecs.open(file1, "r", codec)
    raw = f.read()
    tokens_tot = []
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_tokenizer.tokenize(raw)
    for sentence in sentences:
        tokens=nltk.word_tokenize(sentence)
        tokens_tot = tokens_tot + tokens
    if norm: # remove quotes -> to be replaced with future textNormalize()
        if codec == 'utf-8':
            tokens_tot = [w.replace(u"\u2018",'').replace(u"\u2019",'').replace(u"\u201C","").replace(u"\u201D","") for w in tokens_tot]
        elif codec == 'ascii':
            tokens_tot = [w.replace(u"'","") for w in tokens_tot]
    return tokens_tot, set(tokens_tot)

# key fun to sort info vocab
def vocabOrder(t):
    return t[0].lower()

# key fun to sort info bigrams
def bigramsFreqOrder(t):
    return (-t[1][0],t[0][0].lower(),t[0][1].lower())

# key fun to sort mutual information
def mutualInfoOrder(t):
    return (-t[1], t[0][0].lower(), t[0][1].lower())

def main():
    global codec1
    global text1
    global text1tokens
    global vocab1
    global max_freq
    global hapax
    global normalize
    global vocabolary
    global growth
    global bigrams_infos
    global text1bigrams
    global mutual_info
    global text1trigrams
    global trigrams_infos

    if not len(sys.argv[1:]):
        usage()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 't:m:e:xnvg:birh', ['text=', 'max_freq=', 'encoding=', 'hapax', 'normalize', 'vocabolary', 'growth=', 'bigrams_infos', 'mutual-information', 'trigrams_infos', 'help'])
    except getopt.GetoptError:
        print str(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-t', '--text'):
            text1 = arg
        elif opt in ('-m', '--max_freq'):
            max_freq = int(arg)
        elif opt in ('-e', '--encoding'):
            codec1 = arg
        elif opt in ('-x', '--hapax'):
            hapax = True
        elif opt in ('-n', '--normalize'):
            normalize = True
        elif opt in ('-v', '--vocabolary'):
            vocabolary = True
        elif opt in ('-g', '--growth'):
            growth = int(arg)
        elif opt in ('-b', '--bigrams_infos'):
            bigrams_infos = True
        elif opt in ('-i', '--mutual-information'):
            mutual_info = True
        elif opt in ('-r', '--trigrams_infos'):
            trigrams_infos = True
        else:
            usage()
            sys.exit(2)
            
    text1tokens, vocab1 = readLocalFile(text1, codec1, normalize)
    lenC = len(text1tokens)
    lenV = len(vocab1)
    ttr  = (lenV *0.1) / (lenC *0.1)
    print '-'*80
    print "File:", text1
    print "|C|:", lenC,"- |V|:", lenV
    print "Type Token Ratio: %.6f" % ttr
    print '-'*80
    if max_freq:
        f,t = maxFreqToken(text1tokens, vocab1, max_freq)
        print '-'*80
        print "The token (>=",max_freq,"chars) with max frequence is '", t,"':",f
        print '-'*80
    if hapax:
        hs, d = getHapaxs(text1tokens, vocab1)
        print '-'*80
        print "The distribution of the hapaxs |V1|/|C| is '", d
        #print hs
        print '-'*80
    freq_vocab = {}
    if vocabolary:
        freq_vocab = infoVocab(vocab1, text1tokens)
        print '-'*60
        print "Vocabolary:"
        print ' Type Word', ' ' * 13, 'Frequence', ' ' * 8, 'Absolute Frequence'
        print '-'*80
        for k, v in sorted(freq_vocab.items(), key=vocabOrder):
            fa, fr = v
            fr = Decimal(str(fr)).quantize(Decimal('.0000001'), rounding=ROUND_DOWN)
            print " {: <25}{: <20}{: <10}".format(k, fa, fr)
        print '-'*80
    if growth:
        t_growth = indexGrowth(text1tokens, lenC, growth)
        print '-'*80
        print "Statistical indexes growth"
        print ' |C|',' '*5, '|V|',' '*5, '|V1|/|C|',' '*5, '|V5|',' '*5, '|V10|',' '*5, '|V15|'
        print '-'*80
        for k,v in sorted(t_growth.items()):
            lenV, d, v5, v10, v15 = v
            d = Decimal(str(d)).quantize(Decimal('.000001'), rounding=ROUND_DOWN)
            print " {: <10}{: <10}{: <16}{: <12}{: <12}{: <10}".format(k, lenV, d, v5, v10, v15)
        print '-'*80
    bigs_info = {}
    if bigrams_infos:
        if freq_vocab == {}:
            freq_vocab = infoVocab(vocab1, text1tokens)
        text1bigrams, diff_bigrams = getBigrams(text1tokens)
        bigs_info = infoBigrams(text1bigrams, diff_bigrams, freq_vocab)
        print '-'*80
        print "Bigrams Infos" #F(u,v), F(u), F(v), P(v|u), P(u,v)
        print ' (u,v)',' '*15, 'F(u,v)',' '*6, 'F(u)',' '*6, 'F(v)',' '*8, 'P(v|u)',' '*4, 'P(v,u)'
        print '-'*80
        for k, v in sorted(bigs_info.items(), key=bigramsFreqOrder):
            f_uv, f_u, f_v, p_uv1, p_uv2 = v
            p_uv1 = Decimal(str(p_uv1)).quantize(Decimal('.000001'), rounding=ROUND_DOWN)
            p_uv2 = Decimal(str(p_uv2)).quantize(Decimal('.000001'), rounding=ROUND_DOWN)
            prettyB = k[0] + " , " + k[1]
            print " {: <25}{: <12}{: <12}{: <12}{: <12}{: <10}".format(prettyB, f_uv, f_u, f_v, p_uv1, p_uv2)
        print '-'*80
    if mutual_info:
        if freq_vocab == {}:
            freq_vocab = infoVocab(vocab1, text1tokens)
        if bigs_info == {}:
            text1bigrams, diff_bigrams = getBigrams(text1tokens)
            bigs_info = infoBigrams(text1bigrams, diff_bigrams, freq_vocab)
        mi = getMutualInformation(bigs_info, freq_vocab)
        print '-'*80
        print "Mutual Information"
        print ' (u,v)',' '*28, 'MI',' '*5
        print '-'*80
        for k,v in sorted(mi.items(), key=mutualInfoOrder):
            prettyB = k[0] + " , " + k[1]
            d = Decimal(str(v)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
            print " {: <35}{: <12}".format(prettyB, d)
        print '-'*80
    if trigrams_infos:
        text1trigrams = list(trigrams(text1tokens))
        #freq_dist = nltk.FreqDist(text1tokens)
        freq_dist_tri = nltk.FreqDist(text1trigrams)
        print '-'*80
        print "Trigrams Infos"
        print ' (u,v,z)',' '*35, 'Freq.',' '*5
        print '-'*80
        for elem in freq_dist_tri.most_common(50):
            prettyT = elem[0][0] + " , " + elem[0][1] + " , " + elem[0][2]
            print " {: <45}{: <12}".format(prettyT, elem[1])
    sys.exit(2)
    
main()   

#!/usr/bin/python
# -*- coding: utf-8 -*-

import PyPDF2, sys, getopt, re

fileName = ""
selection = [(0,15),(19,48),(50,89),(123,131),(136,153),(430,471),(475,507),(705,730)]

def usage():
    print '-'*80
    print "Simple script to extract page intervals from pdf file"
    print
    print "Usage: pdfExtract.py -i file-name.pdf -e pages-intervals"
    print
    print "Examples: "
    print "./pdfExtract.py -i file-name.pdf -e 1,16-20,49-124,132-137,154"
    print '-'*80
    sys.exit(0)

def myWriter(pdfReader, pdfWriter, p1, p2):
    for pageNum in range(p1,p2):
        pageObj = pdfReader.getPage(pageNum) 
        pdfWriter.addPage(pageObj)
    return pdfWriter

def findPages(sel):
    selection = []
    pages = re.findall(r'([0-9]+),([0-9]+)', sel) 
    for section in pages:#page 1 has index 0
        number = (int(section[0])-1,int(section[1]))
        selection.append(number)
    return selection

def main():
    global fileName
    global selection
    
    if not len(sys.argv[1:]):
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:e:h', ['input=', 'extract=', 'help'])
    except getopt.GetoptError:
        print str(err)
        usage()
        sys.exit(2)
        
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-i', '--input'):
            fileName = arg
        elif opt in ('-e', '--extract'):
            selection = findPages(arg)
        else:
            usage()
            sys.exit(2)
         
    pdf1File = open(fileName, 'rb')
    pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
    pdfWriter = PyPDF2.PdfFileWriter()

    for sel in selection:
        p1,p2 = sel
        pdfWriter = myWriter(pdf1Reader, pdfWriter, p1, p2)

    pdfOutputFile = open('selected_'+fileName+'.pdf', 'wb')
    pdfWriter.write(pdfOutputFile)
    pdfOutputFile.close()
    pdf1File.close()
    print 'selected_'+fileName+'.pdf created'

main()

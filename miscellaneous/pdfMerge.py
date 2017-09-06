#!/usr/bin/python
# -*- coding: utf-8 -*-

import PyPDF2, sys, getopt, re

selection = []

def usage():
    print '-'*80
    print "Simple script to merge pdf files"
    print
    print "Usage: pdfMerge.py file-name-1.pdf ... file-name-N.pdf"
    print
    print "Examples: "
    print "./pdfMerge.py file1.pdf file2.pdf file3.pdf"
    print '-'*80
    sys.exit(0)

def myWriter(pdfWriter, selection):
    for selected in selection:
        pdf1File = open(selected, 'rb')
        pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
        for i in range(pdf1Reader.getNumPages()):
            pageObj = pdf1Reader.getPage(i) 
            pdfWriter.addPage(pageObj)
        #pdf1File.close()
    return pdfWriter


def main():
    global selection
    
    if not len(sys.argv[1:]):
        usage()

    selection = sys.argv[1:]
    
    pdfWriter = PyPDF2.PdfFileWriter()

    pdfWriter = myWriter(pdfWriter, selection)

    pdfOutputFile = open('pdfMerge_out.pdf', 'wb')
    pdfWriter.write(pdfOutputFile)
    pdfOutputFile.close()
    
    print 'pdfMerge_out.pdf created'

main()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, sys, os, re
from multiprocessing.dummy import Pool as ThreadPool

BASE_URL = "https://www.google.com/"
FILE_TYPE = "filetype:pdf"
MAX_PAGES = 15
searchArgs = ""

urls = []

def getPageHtml(url):
    try:
        import urllib2

        request_headers = {
                "Accept-Language": "en-US,en;q=0.5",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": BASE_URL,
                "Connection": "keep-alive"
        }

        request = urllib2.Request(url, headers = request_headers)
        return urllib2.urlopen(request).read()
    except:
        return "error"

def inputUrl(searchArgs, searchIndex):
	url = BASE_URL + "search?q=" + searchArgs + "+" + FILE_TYPE + "&start=" + str(searchIndex)
	htmlCode = getPageHtml(url);
        if htmlCode !="error":
            return htmlCode
        print("\nCouldn't connect to web\n")
        
def crawlPage(htmlCode,searchIndex):
	urls = re.findall(r'href=[\'"]?([^\'" >]+)', htmlCode)
        myFile = open("output_"+str(searchIndex)+".txt", "a")
	for url in urls:
		mySplit = os.path.splitext(os.path.basename(url))
		if (mySplit[1] == ".pdf"):
			myFile.write(url + '\n')
			name = mySplit[0] + mySplit[1]
			urllib.urlretrieve(url,name)
	myFile.close()

def worker(searchIndex):
	print "[*] Starting:", str(searchIndex) 
	try:
		htmlCode = inputUrl(searchArgs, searchIndex)
		crawlPage(htmlCode, searchIndex)
	except IOError as ex:
		print "[!]",str(ex),  str(searchIndex)


def startGoogling():
	global searchArgs
	
	if len(sys.argv[1:]):
		searchArgs = '+'.join(sys.argv[1:])
	else:
		searchArgs = "fascicolo+informativo+-auto"
	searchIndex = 0
	pool = ThreadPool(MAX_PAGES)
	pool.map(worker,range(0,MAX_PAGES * 10, 10))
	pool.close()
	pool.join()
	print "[*] Pool completed"
		
startGoogling();

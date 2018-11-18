#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, sys, os, re

BASE_URL = "https://www.google.com/"
FILE_TYPE = "filetype:pdf"
MAX_PAGES = 15

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
        
def crawlPage(htmlCode):
	urls = re.findall(r'href=[\'"]?([^\'" >]+)', htmlCode)
	print urls
        myFile = open("output.txt", "a")
	for url in urls:
		mySplit = os.path.splitext(os.path.basename(url))
		if (mySplit[1] == ".pdf"):
			myFile.write(url + '\n')
			name = mySplit[0] + mySplit[1]
			urllib.urlretrieve(url,name)
	myFile.close()

def startGoogling():
	searchArgs = ""
	if len(sys.argv[1:]):
		searchArgs = '+'.join(sys.argv[1:])
	else:
		searchArgs = "fascicolo+informativo+-auto"
	searchIndex = 0
	while searchIndex < MAX_PAGES:
		htmlCode = inputUrl(searchArgs, searchIndex)
		crawlPage(htmlCode)
		searchIndex = searchIndex + 1
		

startGoogling();
#!/usr/bin/python
# -*- coding: utf-8 -*-
import random, string, os, sys
import ntpath, shutil, glob, zipfile
from optparse import OptionParser
from xml.sax import make_parser
from xml.sax.saxutils import XMLFilterBase, XMLGenerator

ntpath.basename("a\\b\\c")

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

parser = OptionParser()
parser.add_option("-f", "--file", dest="fInput",
                  help="path FILE zip INPUT", metavar="FILE")
parser.add_option("-o", "--out", dest="fOutput",
                  help="path FILE zip OUTPUT")
(options, args) = parser.parse_args()


def randomChars():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(12))

def randomMixed():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(18))

def randomDigits():
    return ''.join(random.choice(string.digits) for _ in range(6))


class OblioFilter(XMLFilterBase):

    def __init__(self, tag_names_oblio, parent=None):
        super().__init__(parent)
        self._tag_name = ""
        self.tag_names_oblio = tag_names_oblio

    def startElement(self, name, attrs):
        if name in self.tag_names_oblio:
            self._tag_name = name
        super().startElement(name, attrs)

    def endElement(self, name):
        if name in self.tag_names_oblio:
            super().characters(self.tag_names_oblio[self._tag_name]())
            self._tag_name = ""
        super().endElement(name)

    def characters(self, content):
        if self._tag_name != "":
            super().characters("")
        else:
            super().characters(content)

def main():
    tag_oblio = {
        'INDIRIZZO': randomMixed,
        'DESTINATARIO': randomChars,
        'INDIRIZZO': randomMixed,
        'CAP': randomDigits,
        'COMUNE': randomChars,
        'PROVINCIA': randomChars,
        'CODFISCALEIVA': randomDigits,
        'DTDECORCO': lambda: '00/00/0000',
        'DTSCADCO': lambda: '00/00/0000',
        'DSPROD': randomChars,
        'NUPOLIZ': randomDigits,
        'POLIZZA': randomDigits,
        'DSCOGNOME': randomChars,
        'CDPIVA': randomDigits,
        'DETT_IMLORAPRE': randomDigits,
        'DETT_IMLOPRPRE': randomDigits,
        'DTEFFSOS': lambda: '00/00/0000',
        'DTEFFPRE': lambda: '00/00/0000',
        'DTINIZIOPERIOD': lambda: '00/00/0000',
        }
    
    
    reader = OblioFilter(tag_oblio, make_parser())

    try:
        os.mkdir(options.fOutput)
        os.mkdir(".\out")
        tempDir = options.fOutput + '/' + randomMixed()
        os.mkdir(tempDir)
    except OSError:
        print("Creation of the directory %s failed" % options.fOutput)
        sys.exit(0)
    else:
        print("Successfully created the directory %s " % options.fOutput)

    zf = zipfile.ZipFile(options.fInput, 'r')
    zf.extractall(options.fOutput)
    zf.close()
    xmlList = glob.glob("%s/*.xml" % options.fOutput)
    for path in xmlList:
        print("processing:",path)
        with open("%s\%s" % (tempDir,path_leaf(path)), 'w') as f:
            print(tempDir,path_leaf(path))
            handler = XMLGenerator(f)
            reader.setContentHandler(handler)
            reader.parse(path)
    zf = zipfile.ZipFile(".\out\%s" % path_leaf(options.fInput), "w")
    for filename in glob.glob("%s/*.xml" % tempDir):
        zf.write(os.path.join(".", filename), path_leaf(filename), zipfile.ZIP_DEFLATED)
    zf.close()
    shutil.rmtree(options.fOutput, ignore_errors=True)

if __name__ == "__main__":
    main()

# es. > python .\oblio-xml.py -f 'C:\SOSCO\2019_10_07_52269_536.zip' -o '.\temp'
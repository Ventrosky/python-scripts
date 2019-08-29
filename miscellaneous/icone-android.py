#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, getopt
from PIL import Image

folders = {
    "xxxhdpi": (192,192),
    "xxhdpi": (144,144),
    "xhdpi": (96,96),
    "hdpi": (72,72),
    "mdpi": (48,48),
    "ldpi": (36,36),
}
prefixes = ["mipmap","drawable-port","drawable-land"]

def createIcons(img):
    root = './res'
    print("[*] Creazione Icone in:",root)
    if not os.path.exists(root):
        os.mkdir(root)
    for prefix in prefixes:
        for folder in folders.keys():
            path = root + "/" + prefix + "-" + folder
            if not os.path.exists(path):
                os.mkdir(path)
                img.thumbnail(folders[folder])
                img.save(path+'/'+'icon.png') 

def usage():
    print()
    print("Generatore icone Android")
    print("-f, --file=       file img originale")
    print()
    print("esempio:")
    print("PS> python icone-android.py --file=\"../../art/icona_mobile_2.png\"")
    print()

def main():
    path = ""
    dirname = os.path.dirname(__file__)
    if len(sys.argv) != 2:
        usage()
        sys.exit(2)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:", ["help", "file="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-f", "--file"):
            path = os.path.join(dirname, a)
            print("[*] Immagine originale:", path)
        else:
            assert False, "[!] Opzione non gestita"
    if path == "":
        usage()
        sys.exit(2)
    img = Image.open(path)
    createIcons(img)
    print("[!] Sostituire i file da './res' in '../mobile/platforms/android/res'")
    print("[*] Completato")

if __name__ == "__main__":
    main()
#!/usr/bin/python

from PIL import Image  
import os, math, sys

pathImgs = ""

if (len(sys.argv)>1): 
	pathImgs = sys.argv[1]
else:
	print "Missing path argument"
	print "usage: 'toSprite.py img/'"
	sys.exit(2) 

files = os.listdir(pathImgs)  
files.sort()

print
print "Frames found:",", ".join(files)

frames = map(Image.open, map(lambda s: pathImgs+s, files)) 

widths, heights = zip(*(i.size for i in frames))

print "Frames width:",str(widths)
print "Frames height:",str(heights)

widthTot = sum(widths)
heightTot = max(heights)

spriteImg = Image.new('RGBA', (widthTot, heightTot))

offsetX = 0
for img in frames:
  spriteImg.paste(img, (offsetX,0))
  offsetX += img.size[0]

spriteImg.save(pathImgs+'sprite.png',"PNG")
print
print "Sprite image:", pathImgs+'_sprite.png'
print "Width:", widthTot
print "Height:",heightTot


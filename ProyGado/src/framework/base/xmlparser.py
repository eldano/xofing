# Mauricio Eguia
# Distributed under GNU GPL v3.0

from xml.dom import minidom
import string
import pygame

imgNodeName = "img"
animsNodeName = "animations"
attrFilename = "filename"
attrGroupName = "groupName"
spriteNodeName = "sprite"
keyColorNodeName = "keycolor"
attrAnimName = "name"
attrAnimType = "type"
attrFrameId = "spriteId"
attrFrameDelay = "delay"
attrFrameOrder = "order"
attrRed = "red"
attrGreen = "green"
attrBlue = "blue"


attrId = "id"
attrX = "x"
attrY = "y"
attrW = "w"
attrH = "h"
attrHSX = "hsx"
attrHSY = "hsy"

def parseKeyColor(keycolorElement):
	attrs = keycolorElement.attributes
	if attrs.length != 3:
		raise Exception("el tag "+keycolorElement.nodeName+" tiene que tener los atributos [red,green,blue]")
	red = int(attrs.getNamedItem(attrRed).value)
	green = int(attrs.getNamedItem(attrGreen).value)
	blue = int(attrs.getNamedItem(attrBlue).value)
	return red,green,blue

def parseSprite(spriteElem):
	attrs = spriteElem.attributes
	if attrs.length != 7:
		raise Exception("el tag "+spriteElem.nodeName+" tiene que tener los atributos [id,x,y,w,h,hsx,hsy]")
	id = int(attrs.getNamedItem(attrId).value)
	x = int(attrs.getNamedItem(attrX).value)
	y = int(attrs.getNamedItem(attrY).value)
	w = int(attrs.getNamedItem(attrW).value)
	h = int(attrs.getNamedItem(attrH).value)
	hsx = int(attrs.getNamedItem(attrHSX).value)
	hsy = int(attrs.getNamedItem(attrHSY).value)
	return id,pygame.Rect(x,y,w,h),(hsx,hsy)
	

def parseImg(imgElem):
	attrs = imgElem.attributes
	if attrs.length < 1:
		raise Exception("falta el atributo ["+imgElem.nodeName+".filename]")
	filename = str(attrs.getNamedItem(attrFilename).value)
	spriteCol = {}
	keyColor = None
	for element in imgElem.childNodes:
		if element.nodeType == minidom.Node.ELEMENT_NODE and element.nodeName == spriteNodeName:
			id,rect,hotSpot = parseSprite(element)
			spriteCol[id] = (rect,hotSpot)
		elif element.nodeType == minidom.Node.ELEMENT_NODE and element.nodeName == keyColorNodeName:
			keyColor = parseKeyColor(element)
	return filename, spriteCol, keyColor

def parseFrame(frameElement):
	attrs = frameElement.attributes
	if attrs.length != 3:
		raise Exception("el elemento "+frameElement.nodeName+" tiene que tener tres atributos: [spriteID, delay, order]")
	spriteID = int(attrs.getNamedItem(attrFrameId).value)
	delay = int(attrs.getNamedItem(attrFrameDelay).value)
	order = int(attrs.getNamedItem(attrFrameOrder).value)
	return spriteID, delay, order

def parseAnimation(animationElement):
	attrs = animationElement.attributes
	if attrs.length != 2:
		raise Exception("el elemento "+animationElement.nodeName+" tiene que tener dos atributos: [name, type]")
	name = str(attrs.getNamedItem(attrAnimName).value)
	type = str(attrs.getNamedItem(attrAnimType).value)
	list = []
	for frame in animationElement.childNodes:
		if frame.nodeType == minidom.Node.ELEMENT_NODE:
			list.append(parseFrame(frame))
	list.sort(lambda x,y:cmp(x[2],y[2])) 
	return name, type, map(lambda (x,y,z):(x,y), list)

def parseAnimations(animElem):
	anims = {}
	for animation in animElem.childNodes:
		if animation.nodeType == minidom.Node.ELEMENT_NODE:
			name,type, list = parseAnimation(animation)
			anims[name] = (type, list)
	return anims

def parseGroup(spriteGroup, node):
	img = None
	animations = {}
	attrs = spriteGroup.attributes
	if attrs.length < 1:
		raise Exception("falta el atributo ["+spriteGroup.nodeName+".groupName]")
	groupName = str(attrs.getNamedItem(attrGroupName).value)
	
	for elem in spriteGroup.childNodes:
		if elem.nodeType == minidom.Node.ELEMENT_NODE:
			if elem.nodeName == imgNodeName:
				img = parseImg(elem)
			elif elem.nodeName == animsNodeName:
				animations = parseAnimations(elem)
	return groupName, img, animations
				
	
def parseDocument(docElement):
	rootTag = docElement.firstChild # este es el tag <spriteDef>
	salida = {}
	for spriteGroup in docElement.childNodes:
		if spriteGroup.nodeType == minidom.Node.ELEMENT_NODE:
			groupName, img, anims = parseGroup(spriteGroup, docElement)
			salida[groupName] = (img, anims)
	return salida


def parseSpriteFile(file):
	reader = minidom.parse(file)
	return parseDocument(reader.documentElement)

#a = parseSpriteFile("last.xml")
#print "resultado --> "
#for i in a.keys():
#	print "\n",i, a[i]

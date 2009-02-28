from framework.base.base import *

# This module offers drag and drop functionality and the ability to build a full form like GUI.

uimanager = None

class GComponent(Component):
    
    def __init__(self, name, x, y, width, height):
        Component.__init__(self, name)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def paint(self, screen):
        None   
    
    def nextFrame(self, elapsed):
        None
        
    def hit(self, x, y):
        if self.x < x and self.x + self.width > x:
            if self.y < y and self.y + self.height > y:
                return True
            else:
                return False
        else:
            return False
    
    def onMouseDown(self):
        None
    
    def onMouseUp(self):
        None
        
    def onMouseOver(self):
        None
        
    def onMouseOut(self):
        None
    
    def onClick(self):
        global uimanager
        Component.__raiseEvent__(self, EventObject(uimanager, 'click', None))
    
    def drag(self, x1, y1, x2, y2):
        None
    
class Container(GComponent):
    def __init__(self,name,x,y,width,height):
        GComponent.__init__(self,name,x,y,width,height)
        self.lastFocus = None
        self.click = False
        self.__child__ = []
        self.__rchild__ = []
        
    def paint(self, screen):
        for ch in self.__child__:
            ch.paint(screen);
        
    def nextFrame(self, elapsed):
        self.__postEvents__()
        
    def addChild(self, obj):
        obj.x = obj.x + self.x
        obj.y = obj.y + self.y
        self.__child__.append(obj)
        self.__rchild__.reverse()
        self.__rchild__.append(obj)
        self.__rchild__.reverse()
        
        if isinstance(obj, Container):
            obj.__moved__(self.x, self.y)
        
    def __moved__(self, dx, dy):
        for ch in self.__child__:
            ch.x = ch.x + dx
            ch.y = ch.y + dy
            if isinstance(ch, Container):
                ch.__moved__(dx, dy)
        
    def __postEvents__(self):
        (x, y) = pygame.mouse.get_pos()
        someHit = False
        
        # MouseOver and Out events
        
        for ch in self.__rchild__:
            if ch.hit(x,y):
                someHit = True
                ch.onMouseOver()
                if self.lastFocus != None and self.lastFocus != ch:
                    self.lastFocus.onMouseOut()
                    if self.click:
                        ch.onMouseDown()
                        self.lastFocus.onMouseUp()
                else:
                    if (self.lastFocus != ch) and (self.click):
                        ch.onMouseDown()
                self.lastFocus = ch
                break
        
        if not someHit:
            if self.lastFocus != None:
                self.lastFocus.onMouseOut()
                if self.click:
                    self.lastFocus.onMouseUp()
                self.lastFocus = None
        else:
            if isinstance(self.lastFocus, Container):
                self.lastFocus.__postEvents__()
                return
        
        # Click event
        (left, middle, right) = pygame.mouse.get_pressed()
        if left == 0 and self.click:
            if self.lastFocus != None:
                self.lastFocus.onMouseUp()
                self.lastFocus.onClick()
            else:
                self.onMouseUp()
                self.onClick()
            self.click = False
                    
        if self.click:
            if (self.lx != x or self.ly != y):
                if (self.lastFocus != None):
                    self.lastFocus.drag(self.lx, self.ly, x, y)
                else:
                    self.drag(self.lx, self.ly, x, y)
                
        if left == 1:
            if not self.click:
                if (self.lastFocus != None):
                    self.lastFocus.onMouseDown()
                else:
                    self.onMouseDown()
            self.click = True
            self.lx = x
            self.ly = y

# This class should be programmed to check for already covered regions
class Region:    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
    
    def hit(self, x, y):
        if self.x < x and self.x + self.width > x:
            if self.y < y and self.y + self.height > y:
                return True
            else:
                return False
        else:
            return False
# This is the only component you should setup to the frame in order for the z-order to work properly
class GUIManager(Container):
    
    def __init__(self, name):
        Container.__init__(self, name, 0,0,0,0)
        self.name = name
        self.click = False
        self.lx = 0
        self.ly = 0

    def createWindow(self, name, x, y, w, h, title, font, size, fixed):
        return Window(name, x,y,w,h,title,font,size, fixed)
    
    def setTop(self, comp):
        self.__child__.remove(comp)
        self.__rchild__.remove(comp)
        self.addChild(comp)

    def paint(self, screen):
        Container.paint(self, screen)

class Bevel(GComponent):
    def __init__(self, name, x, y, width, height):
        GComponent.__init__(self, name, x, y, width, height)
        self.color = (150,150,150)
        self.lightBorder = (140,200,180)
        self.darkBorder =(130,170,170)
        self.pressed = False
        self.mouseOver = False
    
    def __colorIncreaser__(self, color, inc):
        ncolor = (color[0] + inc[0], color[1] + inc[1], color[2] + inc[2])
        return ncolor
    
    def drag(self, x1, y1, x2, y2):
        None
    
    def onMouseOver(self):
        GComponent.onMouseOver(self)
        self.mouseOver = True
    
    def onMouseOut(self):
        GComponent.onMouseOut(self)
        self.mouseOver = False
                
    def paint(self, screen):
        screen.fill(self.color, (self.x+2, self.y+2, self.width-3, self.height-3))
        if self.mouseOver:
            pygame.draw.rect(screen, self.lightBorder, (self.x, self.y, self.width, self.height), 2)
        else:
            pygame.draw.rect(screen, self.darkBorder, (self.x, self.y, self.width, self.height), 2)
        GComponent.paint(self, screen)

# Buttons

class Button(Bevel):    
    def __init__(self, name, x, y, texto, font, size):
        Bevel.__init__(self, name, x, y, 0, 0)
        fontFullFileName = pygame.font.match_font(font)
        self.border = 4;
        self.text = texto
        self.font = pygame.font.Font(fontFullFileName, size)
        (self.width, self.height) = self.font.size(self.text)
        self.width = self.width + 2*self.border
        self.height = self.height + 2*self.border
        
    def onMouseDown(self):
        GComponent.onMouseDown(self)
        self.color = (self.color[0]+20, self.color[1]+20, self.color[2]+20)
    
    def onMouseUp(self):
        GComponent.onMouseUp(self)
        self.color = (self.color[0]-20, self.color[1]-20, self.color[2]-20)
        
    def paint(self, screen):
        Bevel.paint(self, screen)
        render = self.font.render(self.text, False, (1,0,0))
        screen.blit(render, (self.x+self.border,self.y+self.border))

class ToggleButton(Bevel):
    def __init__(self, name, x, y, texto, font, size):
        Bevel.__init__(self, name, x, y, 0, 0)
        fontFullFileName = pygame.font.match_font(font)
        self.border = 4;
        self.text = texto
        self.font = pygame.font.Font(fontFullFileName, size)
        (self.width, self.height) = self.font.size(self.text)
        self.width = self.width + 2*self.border
        self.height = self.height + 2*self.border
        self.pressed = False
        
    def onMouseDown(self):
        GComponent.onMouseDown(self)
        self.color = (self.color[0]+20, self.color[1]+20, self.color[2]+20)
    
    def onMouseUp(self):
        GComponent.onMouseUp(self)
        self.color = (self.color[0]-20, self.color[1]-20, self.color[2]-20)
    
    def onClick(self):
        GComponent.onClick(self)
        self.pressed = not self.pressed
        if self.pressed:
            self.color = self.__colorIncreaser__(self.color, (40,30,30))
            self.lightBorder = self.__colorIncreaser__(self.lightBorder, (40,30,30))
            self.darkBorder = self.__colorIncreaser__(self.darkBorder, (40,30,30))
        else:
            self.color = self.__colorIncreaser__(self.color, (-40,-30,-30))
            self.lightBorder = self.__colorIncreaser__(self.lightBorder, (-40,-30,-30))
            self.darkBorder = self.__colorIncreaser__(self.darkBorder, (-40,-30,-30))
    
    def paint(self, screen):
        Bevel.paint(self, screen)
        render = self.font.render(self.text, False, (1,0,0))
        screen.blit(render, (self.x+self.border,self.y+self.border))

# Windows and panels
        
class Panel(Container):
    def __init__(self, name, x, y , width, height):
        Container.__init__(self, name, x, y, width, height)
        self.color = (150,150,150)
        
    def paint(self, screen):
        screen.fill(self.color, (self.x, self.y, self.width, self.height))
        Container.paint(self, screen)
        
class Window(Bevel, Container):
    def __init__(self, name, x, y, w, h, title, font, size, fixed):
        Bevel.__init__(self, name, x, y, w, h)
        Container.__init__(self, name, x, y, w, h)
        fontFullFileName = pygame.font.match_font(font)
        self.border = 4;
        self.title = title
        self.titleColor = (50,100,255)
        self.font = pygame.font.Font(fontFullFileName, size)
        self.topMost = False
        self.fixed = fixed

    def addChild(self, obj):
        Container.addChild(self, obj)
        (tw, th) = self.font.size(self.title)
        obj.y = obj.y + th + 2 * self.border
        if isinstance(obj, Container):
            obj.__moved__(0, th + 2 * self.border)

    def onClick(self):        
        if not self.topMost:
            manager = getUIManager()
            manager.setTop(self)
            self.topMost = True

    def drag(self, x1, y1, x2, y2):       
        if self.lastFocus == None:
            if not self.topMost:
                manager = getUIManager()
                manager.setTop(self)
                self.topMost = True
        
        
            if not self.fixed:
                dx = x2-x1
                dy = y2-y1
                self.x = self.x + dx
                self.y = self.y + dy
                self.__moved__(dx, dy)
                    
    def onMouseOut(self):
        Bevel.onMouseOut(self)
        self.topMost = False

    def paint(self, screen):
        Bevel.paint(self, screen)
        (tw, th) = self.font.size(self.title)
        screen.fill(self.titleColor, (self.x+2, self.y+2, self.width-3, th+2*self.border))
        
        render = self.font.render(self.title, False, (1,0,0))
        screen.blit(render, (self.x+self.border,self.y+self.border))
        Container.paint(self, screen)

# Layout managers

class YLayout(Container):
    def __init__(self, name, x, y, width, height):
        Container.__init__(self, name, x, y, width, height)
        self.lastY = 0
        self.border = 4
    
    def addChild(self, obj):
        Container.addChild(self, obj)
        # Asume x e y como 0, 0
        print 'add'
        obj.y = self.lastY
        self.lastY = self.lastY + obj.height + self.border      

def getUIManager():
    global uimanager
    if uimanager == None:
        uimanager = GUIManager('uimanager')
    return uimanager
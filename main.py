# Copyright (c) 1998, Regents of the University of California
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of California, Berkeley nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import kivy
kivy.require('1.0.9') # replace with your current kivy version !

from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics.texture import Texture
from kivy.graphics.instructions import Callback
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.image import Image
from kivy.graphics.context_instructions import Scale,Rotate,Translate,PushMatrix,PopMatrix
from math import sqrt

from plane import Plane
from vector2d import Vector2d
from mobile import Mobile
from world import World,Landingzone
from background import Layer,Background
from camera import Camera
from mobile import Mobile,Body,Shape
from gui import Gui
from xml.dom.minidom import parse, parseString

class TextureHelper:
  @staticmethod
  def generateGradient(sx,sy):
    texture = Texture.create(size=(sx, sy))   
    # create 64x64 rgb tab, and fill with value from 0 to 255
    # we'll have a gradient from black to white
    #size = sx * sy * 3
    buf = [int(x * 255 / size) for x in xrange(size)]
    # then, convert the array to a ubyte string
    buf = ''.join(map(chr, buf))
    # then blit the buffer
    texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
    return texture
  @staticmethod
  def loadTextureFromFile(filename):
    return Image(filename).texture

class Game:
  world = 0
  camera = 0
  background = 0
  gui = 0
  mainbody = 0
  gameResult = 0
  currentLevel = 1
  def __init__(self):
    self.world = World()
    self.camera = Camera()
  def setupMenu(self):
    self.gui = Gui()
    self.gui.setupMenu(self)
    self.setupBackground('level01.xml')
  def setupLevel(self, *largs):
    print "CURRENT LEVEL %d"%self.currentLevel
    if self.currentLevel == 1:
      self.gui.messaging.reset()
      self.gameResult = 0
      self.setupWorld('level01.xml')
      self.setupBackground('level01.xml')
      self.setupShip('level01.xml')
      self.gui.messaging.displayText('Level %d'%(self.currentLevel),150)

    if self.currentLevel == 2:
      self.gui.messaging.reset()
      self.gameResult = 0
      self.setupWorld('level02.xml')
      self.setupBackground('level02.xml')
      self.setupShip('level02.xml')
      self.gui.messaging.displayText('Level %d'%(self.currentLevel),150)

    if self.currentLevel > 2:
      self.gui.messaging.reset()
      self.mainbody = 0
      self.setupWorld('endgame.xml')
      self.setupBackground('endgame.xml')
      self.gui.messaging.displayText('Congratulations ! !',-1)   

  def checkVictoryCondition(self):
    if self.mainbody.isStable() == 0:
      return 0
    landingzone = self.world.getLandingzone()
    if landingzone.checkBody(self.mainbody) == 1:
      return 1
    else :
      return -1
  def gameIsRunning(self):
    if self.mainbody != 0 and self.gameResult == 0:
      return 1
  def setupBackground(self,filename):
    self.background = Background()
    domLevel = parse(filename)
    backgroundNodes = domLevel.getElementsByTagName("background")
    backgroundNode = backgroundNodes[0]
    for node in backgroundNode.childNodes:
      if node.localName == "layer":
        texturename = 0
        tilesizex = 0
        tilesizey = 0
        positionx = 0
        positiony = 0
        layersizex = 0
        layersizey = 0
        offsetx = 0
        offsety = 0
        for childnode in node.childNodes:
          if childnode.localName == "texture":
            texturename = childnode.getAttribute('value')
          if childnode.localName == "tilesize":
            values = childnode.getAttribute('value').split(',')
            if values[0] == 'screenw': 
              tilesizex = Config.getint('graphics', 'width')
            else:
              tilesizex = float(values[0])
            if values[1] == 'screenh': 
              tilesizey = Config.getint('graphics', 'height')
            else:
              tilesizey = float(values[1])
          if childnode.localName == "position":
            values = childnode.getAttribute('value').split(',')
            if values[0] == 'screenw':
              positionx = Config.getint('graphics', 'width')
            else:
              positionx = float(values[0])
            if values[1] == 'screenh':
              positiony = Config.getint('graphics', 'height')
            else:
              positiony = float(values[1])

          if childnode.localName == "offset":
            values = childnode.getAttribute('value').split(',')
            if values[0] == 'screenw': 
              offsetx = Config.getint('graphics', 'width')
            else:
              offsetx = float(values[0])
            if values[1] == 'screenh': 
              offsety = Config.getint('graphics', 'height')
            else:
              offsety = float(values[1])
          if childnode.localName == "layersize":
            values = childnode.getAttribute('value').split(',')
            if values[0] == 'screenw': 
              layersizex = Config.getint('graphics', 'width')
            else:
              layersizex = float(values[0])
            if values[1] == 'screenh': 
              layersizey = Config.getint('graphics', 'height')
            else:
              layersizey = float(values[1])
        layer = Layer(TextureHelper.loadTextureFromFile(texturename),tilesizex,tilesizey,positionx,positiony,offsetx,offsety,layersizex,layersizey)
        self.background.addLayer(layer)
    
  def setupShip(self,filename):
    domLevel = parse(filename)
    shipNodes = domLevel.getElementsByTagName("ship")
    shipNode = shipNodes[0]
    self.mainbody = Body()
    for node in shipNode.childNodes:
      if node.localName == "position":
        position = node.getAttribute('value')
        values = position.split(',')
        self.mainbody.setPosition(float(values[0]),float(values[1]))
      if node.localName == "mobile":
        m = Mobile()
        for childnode in node.childNodes:
          if childnode.localName == "position":
            values = childnode.getAttribute('value').split(',')
            m.setPosition(float(values[0]),float(values[1]))
          if childnode.localName == "velocity":
            values = childnode.getAttribute('value').split(',')
            m.setVelocity(float(values[0]),float(values[1]))
          if childnode.localName == "thrust":
            values = childnode.getAttribute('value').split(',')
            m.setThrustVector(float(values[0]),float(values[1]))                         
          if childnode.localName == "mass":
            value = childnode.getAttribute('value')
            m.setMass(float(value))      
          if childnode.localName == "radius":
            value = childnode.getAttribute('value')
            m.setRadius(float(value))  
          if childnode.localName == "texture":
            value = childnode.getAttribute('value')
            m.setTexture(TextureHelper.loadTextureFromFile(value))
          if childnode.localName == "physicalPoints":
            for ppointnode in childnode.childNodes:
              if ppointnode.localName == "point":
                values = ppointnode.getAttribute('value').split(',')
                m.addPhysicalPoint(Vector2d(float(values[0]),float(values[1])))
        self.mainbody.addMobile(m)
    self.mainbody.init()
    focus_position = self.mainbody.getPosition()
    self.world.addMobile(self.mainbody)

  def setupWorld(self,filename):
    self.world.reset()
    domLevel = parse(filename)
    worldNodes = domLevel.getElementsByTagName("world")
    for node in worldNodes[0].childNodes:
      if node.localName == "gravity":
        values = node.getAttribute('value').split(',')
        self.world.setGravity(float(values[0]),float(values[1]))
      if node.localName == "landingzone":
        values = node.getAttribute('value').split(',')
        self.world.setLandingzone(Landingzone(float(values[0]),float(values[1]),float(values[2]),float(values[3]),TextureHelper.loadTextureFromFile('checker.png')))

    h = Config.getint('graphics', 'height')
    w = Config.getint('graphics', 'width')
    p0 = Plane(1,0,-10)
    p1 = Plane(0,-1,h-10)
    p2 = Plane(-1,0,w-10)
    p3 = Plane(0,1,-64)
    self.world.addPlane(p0)
    self.world.addPlane(p1)
    self.world.addPlane(p2)
    self.world.addPlane(p3)

    #self.world.setGravity(0.0,-1.8)

  def setupGame(self):
    self.setupMenu()

  def updateGame(self,canvas):
    #if self.mainbody != 0:
    #  self.camera.follow(self.mainbody)
    self.camera.setup(canvas)
    self.background.draw(canvas)

    
    self.world.draw(canvas)

    self.gui.draw(canvas)
    self.world.step(1/60.)
    if self.gameIsRunning():
      res = self.checkVictoryCondition()
      if res != 0:
        if res == -1:
          self.gui.messaging.displayText('FAIL ! !',200) 
          self.gameResult = -1
          Clock.schedule_once(self.setupLevel, 5)
        if res == 1:
          self.gui.messaging.displayText('SUCCESS ! !',200)
          self.gameResult = 1
          self.currentLevel += 1 
          Clock.schedule_once(self.setupLevel, 5)
  def on_touch_down(self, touch):
    self.world.on_touch_down(touch)
    self.gui.on_touch_down(touch)

class YourWidget(Widget):
  game = 0
  def __init__(self, **kwargs):
    super(YourWidget, self).__init__(**kwargs)
    self.game = Game() 
    self.game.setupGame()
    Clock.schedule_interval(self.update_graphics, 1 / 60.)

  def on_touch_down(self, touch):
    # transform the touch coordinate to local space
    touch.apply_transform_2d(self.to_local)
    #print 'The touch is at position', touch.pos

    self.game.on_touch_down(touch)

  def update_graphics(self, *largs):
    self.canvas.clear()
    self.game.updateGame(self.canvas)
    self.canvas.ask_update()
    #self.camera.focus(self.mobile1.getPosition(),self.mobile2.getPosition())


class LandingZoneApp(App):
    def build(self):
        return YourWidget()

if __name__ == '__main__':
    LandingZoneApp().run()

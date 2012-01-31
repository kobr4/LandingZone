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

from kivy.config import Config
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics.texture import Texture
from kivy.logger import Logger

class Layer:
  texture = 0
  repeatx = 0
  repeaty = 0
  offsetx = 0
  offsety = 0
  tilex = 64
  tiley = 64
  positionx = 0
  positiony = 0
  screenh = Config.getint('graphics', 'height')
  screenw = Config.getint('graphics', 'width')
  def __init__(self, texture,sx,sy,positionx,positiony,offsetx,offsety,screenw = Config.getint('graphics', 'width'),screenh=Config.getint('graphics', 'height')):
    self.texture = texture
    self.tilex = sx
    self.tiley = sy
    self.positionx = positionx
    self.positiony = positiony
    self.offsetx = offsetx
    self.offsety = offsety
    self.currentoffsetx = 0
    self.currentoffsety = 0
    self.screenh = screenh
    self.screenw = screenw

  def draw(self,canvas):
    self.currentoffsetx = (self.currentoffsetx+self.offsetx)%self.tilex
    self.currentoffsety = (self.currentoffsety+self.offsety)%self.tiley
    #Logger.info('BACKGROUND %d %d'%(self.offsetx,self.positionx - self.tilex + self.currentoffsetx))
    with canvas:
      position = [self.positionx - self.tilex + self.currentoffsetx, self.positiony]
      while position[1] < self.screenh:
        while position[0] < self.screenw:
          Rectangle(texture=self.texture, pos=position, size=(self.tilex, self.tiley))
          position[0] += self.tilex
        position[0] = self.positionx - self.tilex + self.currentoffsetx
        position[1] += self.tiley

class Background:
  def __init__(self):
    self.layers = []
  def addLayer(self,layer):
    self.layers.append(layer)
  def draw(self,canvas):
    for layer in self.layers:
      layer.draw(canvas)


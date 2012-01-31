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
from kivy.uix.button import Button
from kivy.uix.label import Label
import sys

class Messaging:
  message_array = 0
  lifetime_array = 0
  maxcount = 0
  h = Config.getint('graphics', 'height')
  w = Config.getint('graphics', 'width')
  def __init__(self,maxcount):
    self.message_array = []
    self.lifetime_array = []
    self.maxcount = maxcount
    for i in range(0,maxcount):
      self.lifetime_array.append(0)
      self.message_array.append(0)
  def reset(self):
    for i in range(0,self.maxcount):
      self.lifetime_array[i] = 0
      self.message_array[i] = 0    
  def displayText(self,text,lifetimetick=-1):
    i = 0
    while i < self.maxcount:
      if self.lifetime_array[i] == 0:
        self.message_array[i] = Label(text=text,pos=(self.w/2-50,self.h/2),font_size=45)
        self.lifetime_array[i] = lifetimetick
        i = self.maxcount
      i += 1
  def draw(self,canvas):
    i = 0
    while i < self.maxcount:
      if self.lifetime_array[i] != 0:
        canvas.add(self.message_array[i].canvas)
        self.lifetime_array[i] = self.lifetime_array[i] - 1
      i += 1

class Gui:
  menuWidgets = 0
  ingameWidgets = 0
  messaging = 0
  h = Config.getint('graphics', 'height')
  w = Config.getint('graphics', 'width')
  state = 0
  def __init__(self):
    self.menuWidgets = []
    self.ingameWidgets = []
    self.messaging = Messaging(10)
  def setupMenu(self,game):
    def callback(instance):
      sys.exit()
    def cbStartGame(instance):
      self.state = 1  
      game.setupLevel()
    b = Button(text='Start Game',pos=(self.w/2-75, self.h/2+30),size=(150, 50), font_size=14)
 
    b.bind(on_press=cbStartGame)
    self.menuWidgets.append(b)
    b = Button(text='Quit',pos=(self.w/2-75, self.h/2-30),size=(150, 50), font_size=14)
    b.bind(on_press=callback)
    self.menuWidgets.append(b)
  def registerMenu(self,widget):
    for cwidget in self.menuWidgets:
      widget.add_widget(cwidget)
  def on_touch_down(self, touch):
    if self.state == 0:
      for cwidget in self.menuWidgets:
        cwidget.on_touch_down(touch)
    if self.state == 1:
      for cwidget in self.ingameWidgets:
        cwidget.on_touch_down(touch)    
  def draw(self,canvas):
    self.messaging.draw(canvas)
    if self.state == 0:
      for cwidget in self.menuWidgets:
        canvas.add(cwidget.canvas)

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

from kivy.graphics.context_instructions import Scale,Rotate,Translate,PushMatrix,PopMatrix
from kivy.config import Config

from vector2d import Vector2d


class Camera:
  scale = 1.0
  position = Vector2d(0,0)
  screenh = Config.getint('graphics', 'height')
  screenw = Config.getint('graphics', 'width')  
  def screenToWorld(self,x,y):
    return Vector2d(x/self.scale+self.position.getX(),y/self.scale+self.position.getY())
  def getPosition(self):
    return self.position
  def setup(self,canvas):
    with canvas:
      Scale(self.scale)
      Translate(-self.getPosition().getX(),-self.getPosition().getY(),0)
      #self.getPosition().set(self.getPosition().getX()+1,self.getPosition().getY())
  #def translateTo(self,x,y):
  
  def follow(self,p1):
    target = p1.getPosition().copy()
    current = self.screenToWorld(self.screenw/2.0,self.screenh/2.0)
    distance = Vector2d.distance(target,current)
    target.sub(current)
    target.mulScalar(1.0/distance)
    p = self.screenToWorld(0,0)
    p2 = self.screenToWorld(self.screenw,self.screenh)
    x = target.getX()
    y = target.getY()
    currentp = self.position.copy()
    currentp.add(target)
    if p.getX() < 0.0 and target.getX() < 0.0 :
      x = 0.0
    if p2.getX() > self.screenw and target.getX() > 0.0 :
      x = 0.0 
    if p.getY() < 0.0 and target.getY() < 0.0 : 
      y = 0.0
    if p2.getY() > self.screenh and target.getY() > 0.0 :
     y = 0.0

    #p2.display()
    target.set(x,y)
    self.position.add(target)  
  
  def focus(self,p1,p2):
    top = self.screenToWorld(self.screenw,self.screenh)
    bottom = self.screenToWorld(0,0)
    centerx = (p1.getX() + p2.getX())/2.0
    centery = (p1.getY() + p2.getY())/2.0
    dx = centerx - p1.getX()
    if dx < 0:
      dx = -dx
    dy = centery - p1.getY()
    if dy < 0:
      dy = -dy

    focusstep = 2.0
    print "CENTER %f - %f POSITION %f - %f"%(centerx,centery,self.position.getX(),self.position.getY())
    print "DX %f - %f X=%f X=%f"%(dx,dy,centerx-dx,centerx+dx)

    posx = self.position.getX()
    posy = self.position.getY()
    if (centerx - dx) > self.position.getX() + focusstep:
      
      self.position.set(self.position.getX() + focusstep,self.position.getY())
    if (centerx - dx) < (self.position.getX() - focusstep):
      self.position.set(self.position.getX() - focusstep,self.position.getY()) 
    #if centery > self.position.getY() + focusstep:
    #  self.position.set(self.position.getX(),self.position.getY() + focusstep)
    #if (centerx + dx) < (posx - focusstep):
    #  self.position.set(posx - focusstep,posy)
    #if centery < self.position.getY() - focusstep:
    #  self.position.set(self.position.getX(),self.position.getY() - focusstep)    


    if p1.getX() > bottom.getX() and p1.getX() < top.getX() and p2.getX() > bottom.getX() and p2.getX() < top.getX() and p1.getY() > bottom.getY() and p1.getY() < top.getY() and p2.getY() > bottom.getY() and p2.getY() < top.getY():
      if self.scale < 10:
        self.scale = self.scale + 0.005
    else :
      if self.scale > 1.05:
        self.scale = self.scale - 0.005 

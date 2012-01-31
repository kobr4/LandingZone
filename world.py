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

from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.image import Image

from vector2d import Vector2d
from mobile import Mobile
from particle import ParticleEmitter,ParticleManager

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
    return Image('gfx/' + filename).texture

class Landingzone:
  top = 0
  bottom = 0
  texture = 0
  def __init__(self,bx,by,tx,ty,texture):
    self.top = Vector2d(tx,ty)
    self.bottom = Vector2d(bx,by)
    self.texture = texture
  def draw(self,canvas):
    with canvas:
      Rectangle(texture=self.texture,pos=(self.bottom.getX(),self.bottom.getY()), size=(self.top.getX()-self.bottom.getX(), self.top.getY()-self.bottom.getY()))
  def checkBody(self,body):
    return body.inVerticalBound(self.bottom.getX(),self.top.getX())

class GroundCollider:
  emitter = 0
  def __init__(self,pamanager):
    self.emitter = pamanager.createParticleEmitter()
  def collideEvent(self,point):
    self.emitter.setSource(Vector2d(point.getX()-10.0,point.getY()),Vector2d(point.getX()+10.0,point.getY()))
    self.emitter.setLifetime(0.5,1.0)
    self.emitter.setSpeed(Vector2d(0,10.0),Vector2d(0,10.0))
    self.emitter.emit()

class World:
  particlemanager = 0
  landingzone = 0
  groundcollider = 0
  def __init__(self):
    self.mobiles = []
    self.planes = []
    self.gravity = Vector2d(0.0,0.0)
    self.particlemanager = ParticleManager(1000)
    self.groundcollider = GroundCollider(self.particlemanager)
  def reset(self):
    self.mobiles = []
    self.planes = []    
  def addPlane(self,plane):
    self.planes.append(plane)
  def addMobile(self,mobile):
    self.mobiles.append(mobile)
    mobile.setupParticleEmitters(self.particlemanager,TextureHelper.loadTextureFromFile('star.png'))
  def setGravity(self,x,y):
    self.gravity.set(x,y)
  def setLandingzone(self,landingzone):
    self.landingzone = landingzone
  def getLandingzone(self):
    return self.landingzone
  def step(self,step):
    for mobile in self.mobiles:
      mobile.applyStep(step)
      grav = self.gravity.copy()
      grav.mulScalar(mobile.getMass())
      #grav.rotate(mobile.getAngle())
      mobile.applyForce(step,grav)
      for mobile2 in self.mobiles:
        if mobile != mobile2:
          if mobile.isBound(mobile2.getPosition(),mobile2.getRadius()) == 1:
            n = Vector2d.normal(mobile2.getPosition(),mobile.getPosition())
            vn = Vector2d.dotProduct(mobile.getVelocity(),n)
            if vn < 0:
              #mobile.getVelocity().display()
              #n.display()    
              Mobile.solveCollide(mobile,mobile2)
	      mobile.applyStep(step)
              mobile2.applyStep(step)
      for plane in self.planes:
        #d = plane.distancePoint(mobile.getPosition())
        #vn = Vector2d.dotProduct(mobile.getVelocity(),plane.getNormal())
        #if d < 0 and vn < 0:
        #  plane.reflective(mobile)
        
        for submobile in mobile.getMobiles():
          d = plane.distancePoint(submobile.getPhysicalPosition())
          vn = Vector2d.dotProduct(submobile.getVelocity(),plane.getNormal())
          if d < submobile.getRadius() and vn < 0:
            #ADDED CONDITION OVER PHYSICAL POINTS
            if submobile.getUpdatedPhysicalPoints().count > 0:
              ppcollide = 0
              for point in submobile.getUpdatedPhysicalPoints():
                if plane.distancePoint(point) < 0:
                  self.groundcollider.collideEvent(point)
                  n = plane.getNormal().copy()
                  n.normalize()
                  n.mulScalar(-plane.distancePoint(point))
                  #n.display()
                  mobile.getPosition().add(n)
                  mobile.updateMobiles()
                  
                  ppcollide = 1
                  
              if ppcollide == 1:
                plane.reflective(submobile)
                for submobile2 in mobile.getMobiles():
                  v = submobile2.getVelocity()
                  v.set(0.0,v.getY())
                mobile.angularVelocity = mobile.angularVelocity * 0.8

  def draw(self,canvas):

    if self.landingzone != 0:
      self.landingzone.draw(canvas)
    for mobile in self.mobiles:
      #p = mobile.getPosition()
      mobile.draw(canvas)
      #mobile.drawPhysical(canvas)
      #print "MOBILE %d %d\n"%(p.getX(),p.getY())
    if self.particlemanager != 0:
      self.particlemanager.update(1.0/60.0)
      self.particlemanager.draw(canvas)   
  def on_touch_down(self, touch):
    for mobile in self.mobiles:
      mobile.on_touch_down(touch)   

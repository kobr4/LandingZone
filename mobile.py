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
from kivy.graphics.context_instructions import Scale,Rotate,Translate,PushMatrix,PopMatrix
from math import sqrt,pi,fabs

from vector2d import Vector2d
#from particle import ParticleManager,ParticleEmitter

class Mobile:

  def __init__(self):
    self.position = Vector2d(0,0)
    self.physicalPosition = Vector2d(0,0)
    self.velocity = Vector2d(0,0)
    self.mass = 0.0
    self.radius = 0.0
    self.color = [1, 1, 1]
    self.thrustVector = Vector2d(0,0)
    self.initialThrustVector = Vector2d(0,0)
    self.texture = 0
    self.physicalPoints = []
    self.updatedPhysicalPoints = []
    self.emitter = 0
  def emit(self):
    if self.emitter != 0:
      self.emitter.setSource(self.physicalPosition,self.physicalPosition)
      speedv = self.thrustVector.copy()
      speedv.mulScalar(-100.0)
      #print 'EMITTER TEXTURE=%d'%self.emitter.texture
      self.emitter.setSpeed(speedv,speedv)
      self.emitter.setLifetime(0.5,1.0)
      self.emitter.emit()
  def setParticleEmitter(self,emitter):
    self.emitter = emitter
  def inVerticalBound(self,by,ty):
    for point in self.updatedPhysicalPoints:
      if point.getX() < by or point.getX() > ty:
        return 0
    return 1
  def setupPhysicalPoint(self):
     p = Vector2d(self.position.getX()-self.radius,self.position.getY()+self.radius)
     self.addPhysicalPoint(p)
     p = Vector2d(self.position.getX()-self.radius,self.position.getY()-self.radius)
     self.addPhysicalPoint(p)
     p = Vector2d(self.position.getX()+self.radius,self.position.getY()+self.radius)
     self.addPhysicalPoint(p)
     p = Vector2d(self.position.getX()+self.radius,self.position.getY()+self.radius)
     self.addPhysicalPoint(p)
  def addPhysicalPoint(self,point):
    self.physicalPoints.append(Vector2d(point.getX(),point.getY()))
    self.updatedPhysicalPoints.append(Vector2d(point.getX(),point.getY()))
  def getUpdatedPhysicalPoints(self):
    return self.updatedPhysicalPoints
  def updatePhysicalPoints(self,position,angle):
    for i in range(0,len(self.updatedPhysicalPoints)):
      self.updatedPhysicalPoints[i].set(self.physicalPoints[i].getX(),self.physicalPoints[i].getY())
      self.updatedPhysicalPoints[i].rotate(angle)
      self.updatedPhysicalPoints[i].add(position)

  def setTexture(self,texture):
    self.texture = texture
  def setThrustVector(self,x,y):
    self.thrustVector.set(x,y)
  def getThrustVector(self):
    return self.thrustVector
  def setInitialThrustVector(self,x,y):
    self.initialThrustVector.set(x,y)
  def getInitialThrustVector(self):
    return self.initialThrustVector
  def getColor(self):
    return self.color
  def setColor(self,r,g,b):
    self.color[0] = r
    self.color[1] = g
    self.color[2] = b
  def setPosition(self,x,y):
    self.position.set(x,y)
    self.physicalPosition.set(x,y)
  def setPhysicalPosition(self,x,y):
    self.physicalPosition.set(x,y)
  def setVelocity(self,x,y):
    self.velocity.set(x,y)
  def getPhysicalPosition(self):
    return self.physicalPosition
  def getPosition(self):
    return self.position
  def getVelocity(self):
    return self.velocity
  def setRadius(self,r):
    self.radius = r
  def getRadius(self):
    return self.radius
  def setMass(self,m):
    self.mass = m
  def getMass(self):
    return self.mass
  def applyStep(self,step):
    v = self.getVelocity().copy()
    v.mulScalar(step)
    self.getPosition().add(v)
  def applyForce(self,step,vector):
    v = vector.copy()
    v.mulScalar(step)
    velocity = self.getVelocity()
    velocity.add(v)
  def isInbound(self,point):
    if point.getX() > self.getPhysicalPosition().getX() - self.getRadius() and point.getX() < self.getPhysicalPosition().getX() + self.getRadius() and point.getY() > self.getPhysicalPosition().getY() - self.getRadius() and point.getY() < self.getPhysicalPosition().getY() + self.getRadius():
      return 1
    else :
      return 0

  def getAngle(self):    
    return self.angle
  def setAngle(self,a):
    self.angle = a
  def drawForce(self,canvas):
    sx = self.getPhysicalPosition().getX()
    sy = self.getPhysicalPosition().getY()
    dx = sx + self.getVelocity().getX() * 5
    dy = sy + self.getVelocity().getY() * 5
    with canvas:
      Color(1.0,1.0,1.0)
      Line(points=(sx,sy,dx,dy))

  def draw(self,canvas):
    with canvas:
      #r = Rectangle(texture=self.texture, pos=(p.getX()-10,p.getY()-10), size=(20, 20))  
      Color(self.getColor()[0],self.getColor()[1],self.getColor()[2])
      Rectangle(texture=self.texture,pos=(self.getPosition().getX()-self.getRadius(),self.getPosition().getY()-self.getRadius()), size=(self.getRadius()*2, self.getRadius()*2))
      #Ellipse(pos=(self.getPosition().getX()-self.getRadius(),self.getPosition().getY()-self.getRadius()),size=(self.getRadius()*2,self.getRadius()*2))
    #self.drawForce(canvas)
  def isBound(self,point,radius):
    d = Vector2d.distance(self.position,point)
    if d < 0:
	d = -d
    d = d - radius - self.radius
    #print "distance: %f\n"%d
    #d = d - self.radius
    if d < 0:
      return 1
    else:
      return 0
  def on_touch_down(self, touch):
    touchpos = Vector2d(touch.pos[0],touch.pos[1])
    if self.isInbound(touchpos) == 1:
      #self.setColor(1.0,0,0)
      self.applyForce(100,self.thrustVector)
      #self.getVelocity().display()
      self.emit()
    

  @staticmethod
  def getImpulse(m1,m2):
    vr = m1.getVelocity().copy()
    vr.sub(m2.getVelocity())
    n = Vector2d.normal(m2.getPosition(),m1.getPosition())
    impulse = n.copy()
    #m1.getPosition().display()
    #m2.getPosition().display()
    #impulse.display()
    s = Vector2d.dotProduct(vr,n)*(1 + 0.5)
    impulse.mulScalar(s)
    return impulse
  @staticmethod
  def solveCollide(m1,m2):
    i = Mobile.getImpulse(m1,m2)
    k = 1.0 / (m1.getMass() + m2.getMass())
    v1 = i.copy()
    v1.mulScalar(-m2.getMass() * k)
    m1.setVelocity(v1.getX(),v1.getY())
    
    v2 = i.copy()
    v2.mulScalar(m1.getMass() * k)
    #i.display()
    #print "MASS: %f\n" %(m1.getMass() * k)
    m2.setVelocity(v2.getX(),v2.getY())

class Shape(Mobile):
  def __init__(self):
    self.position = Vector2d(0,0)
    self.center = Vector2d(0,0)
    self.velocity = Vector2d(0,0)
    self.mobiles = []
    self.angle = 0.0  
  def addMobile(self, mobile):
    self.mobiles.append(mobile)
  def draw(self,canvas):
    with canvas:
      PushMatrix()
      Translate(self.getPosition().getX(),self.getPosition().getY(),0)
      Rotate(self.getAngle(),0,0,1)
    for mobile in self.mobiles:
      mobile.draw(canvas)
    with canvas:
      PopMatrix()

class Body(Mobile):
  def __init__(self):
    self.position = Vector2d(0,0)
    self.physicalPosition = Vector2d(0,0)
    self.center = Vector2d(0,0)
    self.velocity = Vector2d(0,0)
    self.mass = 0.0
    self.mobiles = []
    self.angle = 0.0
    self.angularVelocity = 0.0
    self.shape = Shape()
    self.stable = 0
    self.stablecount = 0
    self.oldposition = Vector2d(0,0)
    self.oldangle = 0.0
  def setupParticleEmitters(self,pmanager,texture):
    for mobile in self.mobiles:
      emitter = pmanager.createParticleEmitter()
      emitter.setTexture(texture)
      mobile.setParticleEmitter(emitter)
  
  def inVerticalBound(self,by,ty):
    for mobile in self.mobiles:
       if mobile.inVerticalBound(by,ty) == 0:
         return 0
    return 1 
  def isStable(self):
    return self.stable
  def addMobile(self, mobile):
    self.shape.addMobile(mobile)
    self.mobiles.append(mobile)
  def init(self):
    self.computeCenter()
    self.computeMass()
  def computeCenter(self):
    self.center.set(0,0)
    for mobile in self.mobiles:
      self.center.add(mobile.getPosition())
    size = len(self.mobiles)
    self.center.mulScalar(1.0/size)
  def computeMass(self):
    self.mass = 0
    for mobile in self.mobiles:
      self.mass += mobile.getMass()
    size = len(self.mobiles)
    self.mass = self.mass / size
  def applyForce(self,step,vector):
    #self.angularVelocity = 0.0
    #v = self.getVelocity()
    #v.add(vector)
    for mobile in self.mobiles:
      mobile.applyForce(step,vector)

  def applyStep(self,step):
    v = self.getVelocity()
    v.set(0.0,0.0)
    #self.angularVelocity = 0.0
    for mobile in self.mobiles:
      vmobile = mobile.getVelocity().copy()
      v.add(vmobile)

      #vmobile = mobile.getVelocity()

      om = mobile.getPhysicalPosition().copy()
      om.sub(self.getPosition())
      #om.display()
      vmobile.mulScalar(mobile.getMass())
      if om.length() != 0.0 :
        av = Vector2d.vtangent(om,vmobile) / om.length()
        av = -av
      else :
       av = 0.0

      if om.getX() < 0.0:
        av = -av
      if vmobile.getY() > 0.0:
        av = -av
      #print "ANGULAR VELOCITY AV=%f OM=%f MASS=%f"%(av,om.length(),mobile.getMass())
      self.angularVelocity += av * 0.5

    v.mulScalar(step)
    self.getPosition().add(v)
    #print "ANGULAR VELOCITY=%f"%(self.angularVelocity)
    
    self.angle += self.angularVelocity * step*0.001   
    #self.angularVelocity = self.angularVelocity / 2.0
    self.updateMobiles()
 
    #print 'TOTO: %d %d'%(self.stablecount,self.stable)
    #print '%f - %f'%(self.angle,self.oldangle)
    #print '%d'%int(fabs(self.getPosition().getX()-self.oldposition.getX()))
    #print '%d - %f - %f'%(int(fabs(self.getPosition().getY()-self.oldposition.getY())),self.getPosition().getY(),self.oldposition.getY())
    if int(self.angle) == int(self.oldangle) and int(fabs(self.getPosition().getX()-self.oldposition.getX())) <= 1 and int(fabs(self.getPosition().getY()-self.oldposition.getY())) <= 1 :
      self.stablecount += 1
      if self.stablecount > 180:
        self.stable = 1
    else :
      self.stablecount = 0

    self.oldposition.set(self.getPosition().getX(),self.getPosition().getY())
    self.oldangle = self.angle
    #self.getPosition().display()
    #v = Vector2d(0,0)
    #for mobile in self.mobiles:
    #  v.add(mobile.getVelocity())

    #translate = v
    #translate.mulScalar(step)
     
  def updateMobiles(self):
    for mobile in self.mobiles:
      p = mobile.getPosition()
      mobile.getPhysicalPosition().set(p.getX(),p.getY())
      mobile.getPhysicalPosition().rotate(self.angle)      
      mobile.getPhysicalPosition().add(self.getPosition())
      mobile.getThrustVector().set(mobile.getInitialThrustVector().getX(),mobile.getInitialThrustVector().getY())
      mobile.getThrustVector().rotate(self.angle)
      mobile.updatePhysicalPoints(self.getPosition(),self.angle)
      mobile.getThrustVector().display()

  def getMobiles(self):
    return self.mobiles
  def getAngle(self):
    return self.angle 
  def draw(self,canvas):
    with canvas:
      PushMatrix()
      Translate(self.getPosition().getX(),self.getPosition().getY(),0)
      Rotate(self.getAngle()*180/pi,0,0,1)
    self.shape.draw(canvas)
    with canvas:
      PopMatrix()
  def drawPhysical(self,canvas):
    for mobile in self.mobiles:
      with canvas:
        #PushMatrix()
        #Translate(self.getPhysicalPosition().getX(),self.getPhysicalPosition().getY(),0)
        Color(1.0,1.0,1.0)
        Ellipse(pos=(mobile.getPhysicalPosition().getX()-mobile.getRadius(),mobile.getPhysicalPosition().getY()-mobile.getRadius()),size=(mobile.getRadius()*2,mobile.getRadius()*2))
        #mobile.drawForce(canvas)
        #with canvas:
        #  PopMatrix()
  def on_touch_down(self, touch):
    for mobile in self.mobiles:
      mobile.on_touch_down(touch)




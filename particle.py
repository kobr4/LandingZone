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
from mobile import Mobile
from vector2d import Vector2d
import random

class Particle(Mobile):
  lifetime = 0
  isActive = 0
  texture = 0
  def getX(self):
    return self.getPosition().getX()
  def getY(self):
    return self.getPosition().getY()
  def setLifetime(self,t):
    self.lifetime = t
  def setIsActive(self,a):
    self.isActive = a
  def setTexture(self,t):
    self.texture = t
  def getLifetime(self):
    return self.lifetime
  def update(self,step):
    self.lifetime = self.lifetime - step
    if self.lifetime < 0:
      self.isActive = 0
    
    if self.isActive == 1:
      self.applyStep(step)
      #print 'particle %f'%step
      #self.velocity.display()
      #self.position.display()
  def draw(self,canvas):
    Color(0.5,0.5,0.5)
    if self.texture != 0:
      with canvas:
        Rectangle(texture=self.texture, pos=(self.getX()-self.getRadius(),self.position.getY()-self.getRadius()), size=(self.getRadius()*2,self.getRadius()*2))
    else:
      with canvas:
        Color(1.0,1.0,1.0)
        Ellipse(pos=(self.getX()-self.getRadius(),self.getY()-self.getRadius()),size=(self.getRadius()*2,self.getRadius()*2))

class ParticleEmitter:
  sourcep1 = 0
  sourcep2 = 0
  intersource = 0
  frequency = 0
  speedp1 = 0
  speedp2 = 0
  interspeed = 0
  particleManager = 0
  texture = 0
  lifetime_max = 0
  lifetime_min = 0
  active = 0
  emitter_lifetime = -1
  def __init__(self,pmanager):
    self.sourcep1 = Vector2d(0,0)
    self.sourcep2 = Vector2d(0,0)
    self.intersource = Vector2d(0,0)
    self.speedp1 = Vector2d(0,0)
    self.speedp2 = Vector2d(0,0)
    self.interspeed = Vector2d(0,0)
    self.particleManager = pmanager
  def spawnParticle(self,p):
    f = random.random()
    p.setPosition(self.sourcep2.getX() + self.intersource.getX() * f, self.sourcep2.getY() + self.intersource.getY() * f)
    p.setVelocity(self.speedp2.getX() + self.interspeed.getX() * f, self.speedp2.getY() + self.interspeed.getY() * f)
    p.setIsActive(1)
    p.setLifetime(self.lifetime_min + (self.lifetime_max - self.lifetime_min) * f)
    p.setTexture(self.texture)
    p.setRadius(10)
    #p.getPosition().display()
    #p.getVelocity().display()
  def setFrequency(self,f):
    self.frequency = f
  def setTexture(self,texture):
    self.texture = texture
  def setLifetime(self,mn,mx):
    self.lifetime_max = mx
    self.lifetime_min = mn 
  def setSource(self,p1,p2):
    self.sourcep1.set(p1.getX(),p1.getY())
    self.sourcep2.set(p2.getX(),p2.getY())
    self.intersource.set(self.sourcep2.getX() - self.sourcep1.getX(),self.sourcep2.getY()-self.sourcep1.getY())
  def setSpeed(self,p1,p2):
    self.speedp1.set(p1.getX(),p1.getY())
    self.speedp2.set(p2.getX(),p2.getY())
    self.interspeed.set(self.speedp2.getX() - self.speedp1.getX(),self.speedp2.getY()-self.speedp1.getY())
  def isActive(self):
    return self.active
  def setIsActive(self,active):
    self.active = active
  def emit(self):
    p = self.particleManager.getParticle()
    if p != 0:
      self.spawnParticle(p)   

  def update(self):
    for i in range(0,self.frequency):
      p = self.particleManager.getParticle()
      if p != 0:
        self.spawnParticle(p)
        
class ParticleManager:
  particles = []
  particleEmitters = []
  def __init__(self,size):
    i = 0
    while i < size:
      self.particles.append(Particle())
      i += 1
  def getParticle(self):
    for particle in self.particles:
      if particle.isActive == 0:
        return particle
    return 0
  def createParticleEmitter(self):
    particleEmitter = ParticleEmitter(self)
    self.particleEmitters.append(particleEmitter)
    return particleEmitter
  def update(self,step):
    for particle in self.particles:
      particle.update(step)
    for particleEmitter in self.particleEmitters:
      if particleEmitter.isActive() == 1:
        particleEmitter.update()
        if particleEmitter.getEmitterLifetime() > 0:
          particleEmitter.setEmitterLifetime(particleEmitter.getEmitterLifetime()-1)
        if particleEmitter.getEmitterLifetime() == 0:
          particleEmitter.setIsActive(1)        

  def draw(self,canvas):
    for particle in self.particles:
      if particle.isActive == 1:
        particle.draw(canvas)   

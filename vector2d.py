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

from math import sqrt,pi
from kivy.vector import Vector

class Vector2d:
  def __init__(self,x,y):
    self.data = [0,0]
    self.data[0] = x
    self.data[1] = y
  def set(self,x,y):
    self.data[0] = x
    self.data[1] = y
  def getX(self):
    return self.data[0]
  def getY(self):
    return self.data[1]
  def add(self,vector):
    self.add(vector.getX(),vector.getY())
  def display(self):
    print "x=%f y=%f\n"%(self.data[0],self.data[1])
  @staticmethod
  def dotProduct(v1,v2):
    return v1.getX() * v2.getX() + v1.getY() * v2.getY()
  @staticmethod
  def distance(v1,v2):
    return sqrt( (v2.getX() - v1.getX())*(v2.getX() - v1.getX()) + (v2.getY() - v1.getY())*(v2.getY() - v1.getY())) 
  def length(self):
    v0 = Vector2d(0,0)
    return Vector2d.distance(self,v0)
  def mulScalar(self,f):
    self.data[0] = self.data[0] * f
    self.data[1] = self.data[1] * f
  def sub(self,v):
    self.data[0] -= v.getX()
    self.data[1] -= v.getY()
  def add(self,v):
    self.data[0] += v.getX()
    self.data[1] += v.getY()
  def copy(self):
    return Vector2d(self.data[0],self.data[1])
  @staticmethod
  def normal(p1,p2):
    n = p2.copy()
    n.sub(p1)
    n.normalize()
    return n
  def normalize(self):
    d = Vector2d.distance(Vector2d(0,0),self)
    self.data[0] = self.data[0] / d 
    self.data[1] = self.data[1] / d
  @staticmethod
  def vparallel(m1,m2):
    vp = Vector2d.dotProduct(m1,m2)
    return vp / m1.length()
  @staticmethod
  def vtangent(m1,m2):
    v = m2.copy()
    nom = m1.copy()
    nom.normalize()
    vp = Vector2d.vparallel(m1,m2)
    #m1.display()
    #m2.display()
    nom.mulScalar(vp)
    v.sub(nom)
    return v.length()
  def rotate(self,angle):
    #angle = 0.0
    v = Vector(self.data[0],self.data[1]).rotate(angle*180/pi)
    #v = Vector(self.data[0],self.data[1]).rotate(angle)
    #v.rotate(angle*180/pi)
    #v = Vector(100, 0).rotate(0)
    #print "=>%f %f %f %f"%(v.x,v.y,v.length(),angle*180/pi)
    self.set(v.x,v.y)


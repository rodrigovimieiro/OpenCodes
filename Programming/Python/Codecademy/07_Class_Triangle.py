"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""

class Triangle(object):
  number_of_sides = 3
  def __init__(self,angle1,angle2,angle3):
    self.angle1 = angle1
    self.angle2 = angle2
    self.angle3 = angle3
  def check_angles(self):
    sum =  self.angle1 +  self.angle2 +  self.angle3
    if sum == 180:
      return True
    else:
      return False

class Equilateral(Triangle):
  angle = 60
  def __init__(self):
    self.angle1 = self.angle
    self.angle2 = self.angle
    self.angle3 = self.angle

my_triangle = Triangle(90,30,60)
my_equilateral = Equilateral()

print(my_triangle.number_of_sides, my_triangle.check_angles())
print(my_equilateral.number_of_sides, my_equilateral.check_angles())
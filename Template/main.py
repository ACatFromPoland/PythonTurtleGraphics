import time 
import turtle
import keyboard
import math
import random

from turtle import *


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getXY(self):  # Used for printing
        return (self.x, self.y)
    
    def add(self, vector):
       return Vector(self.x + vector.x, self.y + vector.y)

    def div(self, float):
        return Vector(self.x / float, self.y / float)
    
    def mul(self, float):
        return Vector(self.x * float, self.y * float)
    
class Object:
    def __init__(self):
        self.type = "object"
        self.position = Vector(0, 0)
        self.angle = 0
        self.mesh = []
        #self.center = Vector(0, 0)

    def setPosition(self, Vector):
        self.position = Vector

    def setRotation(self, angle):
        self.angle = angle

    def getCenter(self):  # Gets the center of the mesh
        total = 0
        center = [0,0]
        for point in self.mesh:
            center[0] = center[0] + point.x
            center[1] = center[1] + point.y
            total += 1
        return Vector(center[0] / total, center[1] / total)

class ScreenObject(Object):
    def __init__(self):
        Object.__init__(self)
        self.turtle = Turtle()
        self.turtle.speed(0)
        self.turtle.hideturtle()
        self.turtle.pensize(2)
        self.turtle.pencolor("black")

    def setTurtle(self):            # I can't remember why I made this lol, probably does something.
        self.turtle = Turtle()
        self.turtle.speed(0)
        self.turtle.hideturtle()
        self.turtle.pensize(2)
        self.turtle.pencolor("black")

    def getTurtle(self):
        return self.turtle

class Rectangle(ScreenObject):
    def __init__(self):
        ScreenObject.__init__(self)
        self.type = "rectangle"
        self.size = Vector(1,1)
        self.mesh = [
            Vector(self.position.x, self.position.y),
            Vector(self.position.x + self.size.x, self.position.y),
            Vector(self.position.x + self.size.x, self.position.y + self.size.y),
            Vector(self.position.x, self.position.y + self.size.y)
        ]
    
    def updateMesh(self): # Basically updates the position of the Vectors in the mesh of the rect when you draw it
        self.mesh = [
            Vector(self.position.x, self.position.y),
            Vector(self.position.x + self.size.x, self.position.y),
            Vector(self.position.x + self.size.x, self.position.y + self.size.y),
            Vector(self.position.x, self.position.y + self.size.y)
        ]

    def setSize(self, vector):
        self.size = vector

class Convex(ScreenObject):
    def __init__(self):
        ScreenObject.__init__(self)
        self.type = "convex"
        self.oldmesh = self.mesh
    
    def setPointCount(self, count):  # This is how you init the shape
        for _ in range(count):
            self.mesh.append(Vector(0,0))

    def setPoint(self, index, vector): # This is how you build it
        self.mesh[index] = vector


    def updateMesh(self):
        for i in range(len(self.mesh)):
            self.mesh[i] = Vector(self.oldmesh[i].x + self.position.x, self.oldmesh[i].y + self.position.y)

def getRotation(pivot, point, angle):  # Returns the new rotated point (Around a pivot)
    rads = (math.pi / 180) * angle

    cosTheta = math.cos(rads)
    sinTheta = math.sin(rads)

    rotated = [0, 0]
    rotated[0] = (cosTheta * (point.x - pivot.x ) + sinTheta * (point.y - pivot.y) + pivot.x)
    rotated[1] = (sinTheta * (point.x - pivot.x ) - cosTheta * (point.y - pivot.y) + pivot.y)

    return Vector(rotated[0], rotated[1])

class RenderScreen:
    def __init__(self):
        self.window = turtle.Screen()
        self.window.bgcolor("white")
        self.width = 600
        self.height = 600
        self.window.screensize(self.width, self.height)

    def clear(self):
        self.window.clear()
        self.window.bgcolor("white")

    def draw(self, object):  # Drawing the ScreenObject
        object.updateMesh()
        tr = object.getTurtle()
        tr.penup()
        for point in object.mesh:
            projpoint = getRotation(object.getCenter(), point, object.angle)
            tr.goto(projpoint.x, projpoint.y)
            tr.pendown()

        origin = getRotation(object.getCenter(), object.mesh[0], object.angle)
        tr.goto(origin.x, origin.y)



def main():
    window = RenderScreen()


    # As you can tell its similar to the SFML lib
    box = Rectangle()
    box.setPosition(Vector(50, 50))
    box.setRotation(30)
    box.setSize(Vector(50, 50))

    while (1):
        window.draw(box)

        time.sleep(0.5)
        window.clear()
        
main()
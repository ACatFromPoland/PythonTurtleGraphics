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

    def getXY(self):
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

    def getCenter(self):
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

    def setTurtle(self):
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
    
    def updateMesh(self):
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
    
    def setPointCount(self, count):
        for _ in range(count):
            self.mesh.append(Vector(0,0))

    def updateMesh(self):
        for i in range(len(self.mesh)):
            self.mesh[i] = Vector(self.oldmesh[i].x + self.position.x, self.oldmesh[i].y + self.position.y)

    def setPoint(self, index, vector):
        self.mesh[index] = vector

def getRotation(pivot, point, angle):
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

    def draw(self, object):
        object.updateMesh()
        tr = object.getTurtle()
        tr.penup()
        for point in object.mesh:
            projpoint = getRotation(object.getCenter(), point, object.angle)
            tr.goto(projpoint.x, projpoint.y)
            tr.pendown()

        origin = getRotation(object.getCenter(), object.mesh[0], object.angle)
        tr.goto(origin.x, origin.y)

class Bullet:
    def __init__(self):
        self.rect = Rectangle()
        self.rect.setSize(Vector(1,1))

        self.position = Vector(0, 0)
        self.velocity = Vector(0, 0)

    def update(self):
        self.position = self.position.add(self.velocity)
        self.rect.setPosition(self.position)


class Spaceship:
    def __init__(self):
        self.rect = Convex()
        self.rect.setPointCount(3)
        self.rect.setPoint(0, Vector(0, 0 ))
        self.rect.setPoint(1, Vector(30, 10))
        self.rect.setPoint(2, Vector(0, 20 ))      

        self.positon = Vector(0, 0)
        self.velocity = Vector(0, 0)
        self.speed = 3
    
    def update(self):
        self.positon = self.positon.add(self.velocity)
        self.render()

    def shoot(self):
        addBullet(self.rect.mesh[1], self.rect.angle, self.rect.getCenter())

    def move(self):
        radions = (self.rect.angle) * 0.0174533
        direction = Vector(math.cos(radions), math.sin(radions))
        self.velocity = direction.mul(self.speed)

    def render(self):
        self.rect.setPosition(self.positon)

bulletVector = []
def addBullet(ppos, angle, center):
    b = Bullet()
    direction = Vector(math.cos(angle * 0.0174533), math.sin(angle * 0.0174533))
    b.position = getRotation(center, ppos, angle).add(direction)
    b.velocity = direction.mul(80)
    bulletVector.append(b)

asteroidVector = []
def addAsteroid():
    return

def outside(pos):
    if (pos.x > 500):
        return True
    elif (pos.x < -500):
        return True
    elif (pos.y < -500):
        return True
    elif (pos.y > 500):
        return True
    else:
        return False

def main():
    window = RenderScreen()

    player = Spaceship()


    while (1):  
        if (keyboard.is_pressed('w')):
            player.move()
        if (keyboard.is_pressed('x')):
            player.shoot()
        if (keyboard.is_pressed('a')):
            player.rect.setRotation(player.rect.angle + 15)
        if (keyboard.is_pressed('d')):
            player.rect.setRotation(player.rect.angle - 15)

        player.update()
        
        for i in range(len(bulletVector)):
            try:
                if (outside(bulletVector[i].rect.position)):
                    del bulletVector[i]
                    continue
                bulletVector[i].update()
                window.draw(bulletVector[i].rect)
            except:
                pass
        window.draw(player.rect)
        #qt = Turtle()
        #qt.speed(0)
        #qt.goto(rect.getCenter().x, rect.getCenter().y)
        window.clear()
        player.rect.setTurtle()



main()

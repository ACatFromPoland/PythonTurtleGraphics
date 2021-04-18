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
        self.turtle.pencolor("white")

    def setTurtle(self):
        self.turtle = Turtle()
        self.turtle.speed(0)
        self.turtle.hideturtle()
        self.turtle.pensize(2)
        self.turtle.pencolor("white")

    def getTurtle(self):
        return self.turtle

class Rectangle(ScreenObject):
    def __init__(self):
        ScreenObject.__init__(self)
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
        self.window.bgcolor("black")
        self.width = 600
        self.height = 600
        self.window.screensize(self.width, self.height)

    def clear(self):
        self.window.clear()
        self.window.bgcolor("black")

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

class Player(ScreenObject):
    def __init__(self, id):
        self.rect = Rectangle()
        self.dim = Vector(10, 60)
        if (id == 0):
            self.position = Vector(-450, self.dim.y / 2)
        else:
            self.position = Vector(450, self.dim.y / 2)
        
        self.rect.setPosition(self.position)
        self.rect.setSize(self.dim)

class Ball(ScreenObject):
    def __init__(self):
        self.rect = Rectangle()
        self.dim = Vector(5, 5)
        self.position = Vector(0,0)
        self.velocity = Vector((random.randint(-100, 100) / 100) * 100, (random.randint(-10, 10) / 10) * 20)

        self.rect.setPosition(self.position)
        self.rect.setSize(self.dim)
    
    def update(self):
        self.position = self.position.add(self.velocity)
        self.rect.setPosition(self.position)

def main():
    window = RenderScreen()

    player1 = Player(0)
    player2 = Player(1)
    ball = Ball()

    while (1):  
        if (keyboard.is_pressed('w')):
            player1.rect.setPosition(player1.rect.position.add(Vector(0,20)))
        if (keyboard.is_pressed('s')):
            player1.rect.setPosition(player1.rect.position.add(Vector(0,-20)))

        if (keyboard.is_pressed('i')):
            player2.rect.setPosition(player2.rect.position.add(Vector(0,20)))
        if (keyboard.is_pressed('k')):
            player2.rect.setPosition(player2.rect.position.add(Vector(0,-20)))

        ball.update()
        if (ball.position.x > 465):
            ball.velocity = Vector(ball.velocity.x * -1 + (random.randint(-15, 15) / 10), ball.velocity.y)
        if (ball.position.x < -460):
            ball.velocity = Vector(ball.velocity.x * -1 + (random.randint(-15, 15) / 10), ball.velocity.y)

        if (ball.position.y > 370):
            ball.velocity = Vector(ball.velocity.x, ball.velocity.y * -1 + (random.randint(-15, 15) / 10))
        if (ball.position.y < -360):
            ball.velocity = Vector(ball.velocity.x, ball.velocity.y * -1+ (random.randint(-15, 15) / 10))

        window.draw(player1.rect)
        window.draw(player2.rect)
        window.draw(ball.rect)
        #time.sleep(0.1)
        #window.clear()
        #player1.rect.setTurtle()
        #player2.rect.setTurtle()



main()

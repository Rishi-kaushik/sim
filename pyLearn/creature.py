import random
from graphics import *

import Learn

class Creature:

    def __init__(self,type):
        self.type=type
        x=random.randrange(0,Learn.width)
        y=random.randrange(0,Learn.height)
        health=100
        age=0
        #sight=3
        #record
        self.draw()


    def draw(self):
        if type==0:
            point=Point(self.x,self.y)
            point.draw(Learn.win)

    def move(self):
        pass
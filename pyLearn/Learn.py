from graphics import *
import random

width, height, spread = 100, 100, 8
pop = 2
speed = 0.3
max_pop = 2


class Creature:
    def __init__(self, type, x=-1, y=-1):
        self.alive = True
        self.type = type
        self.lastPoint = Point(0, 0)
        if x == -1 or y == -1:
            self.x = random.randint(width * 0.4, width * 0.6)
            self.y = random.randint(height * 0.4, height * 0.6)
            map[self.x][self.y] = self.type
        else:
            self.x = random.randint(x - spread, x + spread)
            self.y = random.randint(y - spread, y + spread)
            map[self.x][self.y] = self.type
        if type == 1:
            self.health = random.randint(0, 6)
        elif type == 2:
            self.health = random.randint(10, 15)
        elif type == 3:
            self.health = random.randint(10, 15)
        self.age = 0
        # self.sight=3
        # self.record

    def move(self):
        if self.type == 1:  # plant (producer)
            self.health += 1
            if self.health >= 10 and len(a) < max_pop:
                a.remove(self)
                a.append(Creature(self.type, self.x, self.y))
                a.append(Creature(self.type, self.x, self.y))
                self.alive = False
        else:  # herbivore  (eats plant) or carnivore (eats herbivore)
            # self.health -= 1
            if self.health <= 0:
                a.remove(self)
                self.alive = False
            else:
                if map[self.x + 1][self.y] == self.type - 1:
                    self.x += 1
                    i = 0
                    while i < len(a):
                        if a[i].type == self.type - 1:
                            if a[i].x == self.x and a[i].y == self.y:
                                a[i].lastPoint.undraw()
                                a.pop(i)
                        i += 1
                    a.remove(self)
                    self.alive = False
                    map[self.x][self.y] = 0
                    a.append(Creature(self.type, self.x, self.y))
                    a.append(Creature(self.type, self.x, self.y))
                elif map[self.x - 1][self.y] == self.type - 1:
                    self.x -= 1
                    i = 0
                    while i < len(a):
                        if a[i].type == self.type - 1:
                            if a[i].x == self.x and a[i].y == self.y:
                                a[i].lastPoint.undraw()
                                a.pop(i)
                        i += 1
                    a.remove(self)
                    self.alive = False
                    map[self.x][self.y] = 0
                    a.append(Creature(self.type, self.x, self.y))
                    a.append(Creature(self.type, self.x, self.y))
                elif map[self.x][self.y + 1] == self.type - 1:
                    self.y += 1
                    i = 0
                    while i < len(a):
                        if a[i].type == self.type - 1:
                            if a[i].x == self.x and a[i].y == self.y:
                                a[i].lastPoint.undraw()
                                a.pop(i)
                        i += 1
                    a.remove(self)
                    self.alive = False
                    map[self.x][self.y] = 0
                    a.append(Creature(self.type, self.x, self.y))
                    a.append(Creature(self.type, self.x, self.y))
                elif map[self.x][self.y - 1] == self.type - 1:
                    self.y -= 1
                    i = 0
                    while i < len(a):
                        if a[i].type == self.type - 1:
                            if a[i].x == self.x and a[i].y == self.y:
                                a[i].lastPoint.undraw()
                                a.pop(i)
                        i += 1
                    a.remove(self)
                    self.alive = False
                    map[self.x][self.y] = 0
                    a.append(Creature(self.type, self.x, self.y))
                    a.append(Creature(self.type, self.x, self.y))
                else:
                    i = random.randint(1, 4)
                    if i == 1:
                        self.x += 1
                    elif i == 2:
                        self.x -= 1
                    elif i == 3:
                        self.y += 1
                    elif i == 4:
                        self.y -= 1
        self.draw()

    def draw(self):
        self.lastPoint.undraw()
        map[int(self.lastPoint.x)][int(self.lastPoint.y)] = 0
        if self.alive:
            point = Point(self.x, self.y)
            if self.type == 1:
                point.setFill('green')
                point.draw(win)
            elif self.type == 2:
                point.setFill('cyan')
                point.draw(win)
            elif self.type == 3:
                point.setFill('red')
                point.draw(win)
            self.lastPoint = point
            map[self.x][self.y] = self.type


# Shit starts here .....

win = GraphWin('sim', width, height)
win.setBackground('black')

map = []
for i in range(0, height):
    line = []
    for j in range(0, width):
        line.append(0)
    map.append(line)

a = []
# for i in range(0, pop):
#     a.append(Creature(random.randint(1, 3)))
a.append(Creature(3))
a.append(Creature(2))


while len(a) > 0:
    time.sleep(speed)  # used to slow simulation
    j = 0
    while j < len(a):
        a[j].move()
        j += 1
        print(len(a), '  ', j)  # for testing


        # to do
        #   make a 2d array of map (done)
        #   make movement and ai for 1 & 2 (partial)
        #   add max pop for sim speed
        #   similar rules for all

import math

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def distanceTo(self, otherPos):
        return math.sqrt((self.x - otherPos.x)**2 + (self.y - otherPos.y)**2)


    def asTuple(self):
        return (int(self.x), int(self.y))


    def distanceSquaredTo(self, otherPos):
        return (self.x - otherPos.x)**2 + (self.y - otherPos.y)**2
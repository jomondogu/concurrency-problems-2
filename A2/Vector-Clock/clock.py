# Clock object storing thread-side vector clock
# merges implementations from https://github.com/eugene-eeo/vclock/blob/master/vclock.py and https://github.com/ethanfrey/vclock/blob/master/vclock/clock.py

class Clock(object):

    def __init__(self, vector):
        self.vector = vector

    #increments own vector at given index
    def increment(self, index):
        self.vector = self.vector[:index] + [self.vector[index] + 1] + self.vector[index+1:]

    #returns -1 if self < other, 1 if self > other, and 0 if self & other are concurrent or identical
    def compare(self, other):
        v1 = self.vector
        v2 = other.vector
        greater = False
        less = False
        for x, y in zip(v1,v2):
            greater |= x > y
            less |= x < y
            if greater and less:
                break
        return int(greater) - int(less)

    #returns true if self and other are different and concurrent, false otherwise
    def concurrent(self, other):
        v1 = self.vector
        v2 = other.vector
        return (v1 != v2) and compare (self, other) == 0

    #merges own vector with other vector, increments own vector at given index
    def merge(self, other, index):
        self.vector = [max(x,y) for x, y in zip(self.vector,other.vector)]
        self.increment(index)

    def __str__(self):
        return str(self.vector)

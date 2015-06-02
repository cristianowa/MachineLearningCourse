import random
import math
from configs import config, Singleton
@Singleton
class Tau:
    def __init__(self, val = 1, step = 0.9):
        self.val = val
        self.current = val 
        self.step = 0.1
    def reload(self):
        self.current = self.val
    def get(self):
        return self.current
    def decrease(self):
        self.current *= self.step
tau = Tau.Instance()

class State:
    
    def __init__(self, start = False, end = False, cliff = False, up = -1.5, down = -1.5, left = -1.5, right = -1.5, analysed = False, reward = -1, policy = "greedy", episilon = 0.1):
        self.start = start
        self.end = end
        self.cliff = cliff
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.analysed = analysed
        self.reward = reward
        self.policy = policy
    def dir(self, direction):
        return getattr(self,direction)
    def actionSum(self):
        acc = 0
        for val in  [self.up, self.down, self.left, self.right]:
            acc += val
        return acc
    def getBestAction(self):
        """ here is were the policy is defined
        we are using a greedy policy best action"""
        directions = [self.up, self.down, self.left, self.right]
        directions_names = ["up","down","left","right"]
        if self.policy == "greedy":
           best = directions.index(max(directions))
        elif self.policy == "random":
            best = random.randint(0,3)
        elif self.policy == "e-greedy":
            e = 1/randint.randint(0,100)
            if e < self.episilon:
                best = random.randint(0,3)
            else:
                best = directions.index(max(directions))
        elif self.policy == "softmax":
            qsum = self.actionSum()
            policies = dict(zip(directions_names, directions))
            for p in policies:
                q = policies[p]
                policies[p] = pow(math.e, q / tau.get()) / qsum
            tau.decrease()
        return directions_names[best]
    def setDir(self, direction, new_value):
        setattr(self,direction,new_value)
    def maxQ(self):
        directions = [self.up, self.down, self.left, self.right]
        return max(directions)
    def __str__(self):
        s = ""


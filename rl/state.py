import math
from configs import config
from policy import evaluate_policy
class State:
    
    def __init__(self, start = False, end = False, cliff = False, up = -1.5, down = -1.5, left = -1.5, right = -1.5, analysed = False, reward = -1):
        self.start = start
        self.end = end
        self.cliff = cliff
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.analysed = analysed
        self.reward = reward
        self.policy = config.policy
    def dir(self, direction):
        return getattr(self,direction)
    def actionSum(self):
        acc = 0
        for val in  [self.up, self.down, self.left, self.right]:
            acc += val
        return acc
    def getBestAction(self):
        directions = [self.up, self.down, self.left, self.right]
        directions_names = ["up","down","left","right"]

        return evaluate_policy(self.policy, directions, directions_names)
    def setDir(self, direction, new_value):
        setattr(self,direction,new_value)
    def maxQ(self):
        directions = [self.up, self.down, self.left, self.right]
        return max(directions)
    def __str__(self):
        s = ""


import random

class State:
    def __init__(self, start = False, end = False, cliff = False, up = 0.25, down = 0.25, left = 0.25, right = 0.25, analysed = False, reward = -1, policy = "greedy"):
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
            return 0
        return directions_names[best]
    def setDir(self, direction, new_value):
        setattr(self,direction,new_value)
    def maxQ(self):
        directions = [self.up, self.down, self.left, self.right]
        return max(directions)
    def __str__(self):
        s = ""


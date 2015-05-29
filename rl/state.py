class State:
    def __init__(self, start = False, end = False, cliff = False, up = 0.25, down = 0.25, left = 0.25, right = 0.25, analysed = False, reward = -1):
        self.start = start
        self.end = end
        self.cliff = cliff
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.analysed = analysed
        self.reward = reward
    def dir(self, direction):
        return getattr(self,direction)

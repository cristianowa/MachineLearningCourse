from singleton import Singleton
@Singleton
class Configs:
    def __init__(self):
#### HERE THE CONFIGS ARE CHANGED ! ##########    
        self.rows =  4
        self.columns = 12
        self.cliff = [(0,1,1,11)]
        self.maxsteps = 25
        self.start = (0,0)
        self.end = (0,11)
        self.column_witdh = 8
        self.stop_success = False
        self.stop_best = False
        self.episodes = 1000
        self.policy = "greedy"
        self.valid_policies = ["greedy","random", "e-greedy", "softmax"]
        self.episilon = 0.1
config = Configs.Instance()

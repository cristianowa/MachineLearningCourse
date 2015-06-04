from singleton import Singleton
import random

@Singleton
class Tau:
    def __init__(self, val = 1, step = 0.999):
        self.val = val
        self.current = val 
        self.step = step
    def reload(self):
        self.current = self.val
    def get(self):
        return self.current
    def decrease(self):
        self.current *= self.step
tau = Tau.Instance()

def evaluate_policy(policy, values, names):
   if policy == "greedy":
      best = values.index(max(values))
   elif policy == "random":
       best = random.randint(0,3)
   elif policy == "e-greedy":
       e = 1/random.randint(1,100)
       if e < config.episilon:
           best = random.randint(0,3)
       else:
           best = values.index(max(values))
   elif policy == "softmax":
       qsum = self.actionSum()
       policies = dict(zip(names, values))
       for p in policies:
           q = policies[p]
           policies[p] = pow(math.e, q / tau.get()) / qsum
       best = names.index(max(policies))
       tau.decrease()
   return names[best]


import sys
import main_table
import asciart
from copy import copy
from configs import config
import state
import argparse


class Sim:
    def __init__(self, maxActions = 50):
        self.maxActions = maxActions
        self.rows = config.rows
        self.columns = config.columns
        self.cliff = config.cliff
        self.states = main_table.buildTable(self.rows, self.columns, self.cliff, config.start, config.end)
    def show(self):
        main_table.print_all_tables(self.states)
    def walk(self, direction):
        #TODO:border values are hardcoded
        self.nextState = copy(self.state)

        if direction == "left":
            if self.state[1] == 0:
                return False
            else :
                self.nextState[1]-=1
        elif direction == "right":
            if self.state[1] == 11:
                return False
            else:
                self.nextState[1] +=1
        elif direction == "up":
            if self.state[0] == 3:
                return False
            else:
                self.nextState[0] += 1

        elif direction == "down":
            if self.state[0] == 0:
                return False
            else:
                self.nextState[0] -= 1
        else:
            raise Exception("Are you flying ? ")
        return True
        print "PREVIUS: " + str(self.state)
        print "NEXT : " + str(self.nextState)

    def currentState(self):
        return self.states[self.state[0]][self.state[1]]
    def getNextState(self):
        return self.states[self.nextState[0]][self.nextState[1]]
    def runEpisode(self, count = 1):
        for i in range(count):
#            print "Episode:" + str(i)
            self.state = [0,0]
            run = True
            step = 0
            while run:
                step += 1
                if step > config.maxsteps:
                    break
                action = self.currentState().getBestAction()
                alpha = 1.0/step #(maxsteps-step)/steps
                dowalk = self.walk(action) # updates current state
                reward = self.getNextState().reward
                #print "step:"  + str(step) + " action[" + str(action) + "]",
                #print " nextState[" + str(self.nextState) + "]",
                #print " currentState[" +str(self.state) + "]"
                if self.getNextState().cliff:
                   # print "fall in the cliff "
                    run = False
                    #we have to stop the execution of this episode
                q = self.currentState().dir(action)
                gamma = 1
                q += alpha*(reward + gamma*(self.getNextState().maxQ() - self.currentState().dir(action)))
                self.currentState().setDir(action,q)
                if dowalk:
                    self.state = self.nextState
                self.currentState().analysed = True
            #Episode tear down
            state.tau.reload()
            #TODO: check if end is reached
            #TODO: check if best path was found
            if config.stop_success:
                pass
            
        self.show() 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Q-learning  exercise")
    parser.add_argument("-e","--episodes", help = "Number of episodes to be executed"       , dest = "episodes"      , default = config.episodes)
    parser.add_argument("-s","--steps"   , help = "Maximum numbef of steps for each episode", dest = "steps"         , default = config.maxsteps)
    parser.add_argument("-stop-success"  , help = "Stops if end is reached"                 , dest = "stop_success"  , action = "store_true")
    parser.add_argument("-stop-best"     , help = "Stops if best path is found"             , dest = "stop_best"     , action = "store_true")
    parser.add_argument("-p", "-policy"  , help = "Defined policy from " + str(config.valid_policies), dest = "policy"        , default = config.policy)
    parser.add_argument("-episilon"      , help = "Episilon for e-greedy policy"            , dest = "episilon"      , default = config.episilon)
    args = parser.parse_args()
    config.maxsteps = int(args.steps)
    config.stop_best = args.stop_best
    config.stop_success = args.stop_success
    if args.policy not in config.valid_policies:
        print "Invalid policy"
        sys.exit(0)
    config.policy = args.policy
    config.episodes = int(args.episodes)
    config.episilon = float(args.episilon)
    sim = Sim()
    sim.runEpisode(config.episodes)



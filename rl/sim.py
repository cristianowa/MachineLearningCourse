import sys
import main_table
import asciart
from copy import copy
from configs import config
import state
from policy import tau


class Sim:
    def __init__(self, maxActions = 50):
        self.maxActions = maxActions
        self.rows = config.rows
        self.columns = config.columns
        self.cliff = config.cliff
        self.states = main_table.buildTable(self.rows, self.columns, self.cliff, config.start, config.end)
        self.firstEpisodedReached = None
        self.firstEpisodeBestReached = None
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

    def currentState(self):
        return self.states[self.state[0]][self.state[1]]
    def getNextState(self):
        return self.states[self.nextState[0]][self.nextState[1]]
    def report(self):
        self.show()
        if self.firstEpisodedReached != None:
            print "First episode that reached end is : " + str(self.firstEpisodedReached)
        if self.firstEpisodeBestReached != None:
            print "First episode that reached optimum path is :" + str(self.firstEpisodeBestReached)
    def checkReach(self, episode):
        if self.firstEpisodedReached != None:
            return False
        if self.state == [0,11]:
            self.firstEpisodedReached = episode
            return True
        return False
    def checkBest(self, episode):
        if self.firstEpisodeBestReached != None:
            return False
        oracle = ["up"] + ["right"] *11 + ["down"]
        states_to_check = [[0,0],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11]]
        ok = True
        for i in range(len(states_to_check)):
            st = states_to_check[i]
            if self.states[st[0]][st[1]].getBestAction() != oracle[i]:
                ok = False
        if ok :
            self.firstEpisodeBestReached = episode
            return True
        return False
    def runEpisode(self, count = 1):
        for i in range(count):
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
            tau.reload()
            if self.checkReach(i) and config.stop_success:
                break
            if self.checkBest(i) and config.stop_best:
                break

        self.report()




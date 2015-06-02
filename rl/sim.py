import main_table
import asciart
from copy import copy
from configs import config


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
        print "PREVIUS: " + str(self.state)
        print "NEXT : " + str(self.nextState)

    def currentState(self):
        return self.states[self.state[0]][self.state[1]]
    def getNextState(self):
        return self.states[self.nextState[0]][self.nextState[1]]
    def runEpisode(self, count = 1):
        for i in range(count):
            print "Episode:" + str(i)
            self.state = [0,0]
            run = True
            step = 0
            while run:
                step += 1
                if step > config.maxsteps:
                    break
                action = self.currentState().getBestAction()
                alpha = 1.0/step #(maxsteps-step)/steps
                self.walk(action) # updates current state
                reward = self.getNextState().reward
                print "step:"  + str(step) + " action[" + str(action) + "] alpha[" + str(alpha) + "] nextState[" + str(self.nextState) + "]"
                if self.getNextState().cliff:
                    print "fall in the cliff "
                    run = False
                    #we have to stop the execution
                q = self.currentState().dir(action)
                print "=========="
                print alpha
                print reward
                print self.getNextState().maxQ()
                print self.currentState().dir(action)
                print "=========="
                q += reward + alpha*(self.getNextState().maxQ() - self.currentState().dir(action))
                print "setting " + str(self.state) + "action " + action + " with " + str(q)
                self.currentState().setDir(action,q)
                self.currentState().analysed = True
            self.show() 

if __name__ == "__main__":
    sim = Sim()
    sim.runEpisode()



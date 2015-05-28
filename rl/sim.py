import main_table
import asciart
rows = 4
columns = 12
cliff = [(0,1,1,11)]
maxsteps = 50
class Sim:
    def __init__(self, maxActions = 50):
        self.maxActions = maxActions
        self.rows = rows
        self.columns = columns
        self.cliff = cliff
    def show(self):
        tbp = main_table.fill_table(self.states)
        print asciart.format_table(tbp, [8] * 12)
    def inits(self):
        self.states = main_table.buildTable(self.rows, self.columns, self.cliff)
        self.states[0][0]["is_start"] = True
        self.states[0][11]["is_end"] = True
        self.states[0][11]["reward"] = 1000
    def runEpisode(self, count = 1):
        for i in range(count):
            self.tab = self.inits()
            state = (0,0)
            run = True
            step = 0
            while run:
                step += 1
                if step > maxsteps:
                    break
                
                a = 1 / steps

            self.show() 

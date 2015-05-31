

import asciart
try:
    from termcolor import colored
except:
    def colored(x, y):
        return x
from state import State
#directions
directions = ["up", "down", "left", "right"]

def cliff_expand(cliff):
    total = []
    for conj in cliff:
        x1 = conj[0]
        x2 = conj[1]
        y1 = conj[2]
        y2 = conj[3]
        for i in range(x1,x2):
            for j in range(y1,y2):
                total.append((i,j))
    return total
def buildTable(row, column, cliff, start = (0,0), end = (0,11) ):
    """ build the table with row and column sizes
        row = number of lines
        column = number of columns
        cliff = cell that are part of the cliff
        each cell is defined by a tuple(is_cliff - boolean, direction ( "up", "down", "left", "right", None), accumlated reward value 
    """
    maintable = [None] * row
    cliffs = cliff_expand(cliff)
    for i in range(row):
        maintable[i] = [None] * column
    for i in range(row):
        for j in range(column):
            is_cliff = False
            reward= -1
            if (i,j) in cliffs:
                is_cliff = True
                reward = -100
            maintable[i][j] = State(cliff = is_cliff, reward = reward)
    maintable[start[0]][start[1]].start = True
    maintable[start[0]][start[1]].reward = 1000
    maintable[end[0]][end[1]].end = True
    return maintable

def fill_table(table, direction):
    print_table = [None] * len(table)
    for i in range(len(print_table)):
        print_table[i] = [""] * len(table[0])
    for i in range(len(table)):
        for j in range(len(table[0])):
            if table[i][j].cliff:
                print_table[i][j] = " " + colored(asciart.symbols["x"],"blue") * 7 
            elif table[i][j].start:
                print_table[i][j] = " S "
            elif table[i][j].end:
                print_table[i][j] = " G "
            elif direction == "gradient":
                if table[i][j].analysed:
                    print_table[i][j] = colored(asciart.arrows[print_table[i][j].getBestAction()])
            else:
                print_table[i][j] += "  " + colored(str(round(table[i][j].dir(direction),5)), "cyan") + "  "
    return print_table

def print_all_tables(table):
    for d in directions:
        
        tbp = fill_table(table, d)
        print "=========== " + d + " ============="
        print asciart.format_table(tbp, [8]*12)
    print "=========== Gradient ============="
    tbp = fill_table(table, "gradient")
    print asciart.format_table(tbp, [8] * 12)
if __name__ == "__main__":
    tb = buildTable(4,12,[(0,1,1,11)])
    print_all_tables(tb)

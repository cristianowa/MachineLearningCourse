

import asciart
try:
    from termcolor import colored
except:
    def colored(x, y):
        return x

#directions
up = "up"
down = "down"
left = "left"
right = "right"

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
def buildTable(row, column, cliff):
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
            maintable[i][j] = { 
                "is_cliff": is_cliff,
                "dir": None, 
                "val" : 0,
                "reward" : reward,
                "is_start":False,
                "is_end":False}
    return maintable

def fill_table(table):
    print_table = [None] * len(table)
    for i in range(len(print_table)):
        print_table[i] = [None] * len(table[0])
    for i in range(len(table)):
        for j in range(len(table[0])):
            if table[i][j]["is_cliff"]:
                print_table[i][j] = asciart.symbols["x"] * 5 
            elif table[i][j]["is_start"]:
                print_table[i][j] = " S "
            elif table[i][j]["is_end"]:
                print_table[i][j] = " G "
            elif table[i][j]["dir"] == None:
                 print_table[i][j] = ""
            else:
                print_table[i][j] = " " + colored(asciart.arrows[table[i][j]["dir"]],"red")
                print_table[i][j] += " " + colored(str(round(table[i][j]["val"],5)), "cyan") + "  "
    return print_table

if __name__ == "__main__":
    tb = buildTable(4,12,[(0,1,1,11)])
    tb[3][3]["val"] = 3.3
    tb[3][3]["dir"] = up
    tb[3][4]["dir"] = up
    tb[3][4]["val"] = 3.4
    tb[0][0]["is_start"] = True
    tb[0][11]["is_end"] = True
    tbp = fill_table(tb)
    print asciart.format_table(tbp, [8]*12)

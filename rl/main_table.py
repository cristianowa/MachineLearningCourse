try:
    from termcolor import cprint
except:
    def cprint(x,y):
        print(x)
#arrows
arrows = {
    "up"    : unicode(u'\u2191'),
    "left"  : unicode(u'\u2190'),
    "right" : unicode(u'\u2192'),
    "down"  : unicode(u'\u2193')
}
#corners

corners = {
    "left" : {
        "up":      unicode(u'\u2554'),
        "down":    unicode(u'\u255A'),
        "middle":  unicode(u'\u2560'),
    },
    "right" : {
        "up":      unicode(u'\u2557'),
        "down":    unicode(u'\u255D'),
        "middle":  unicode(u'\u2563'),
    },
    "vertical": {
        "normal": unicode(u'\u2551')
    },
    "horizontal": {
        "normal": unicode(u'\u2550'),
        "middle" : unicode(u'\u256C'),
        "up"  : unicode(u'\u2566'),
        "down": unicode(u'\u2569'),
    }
}

symbols = {
    "x": unicode(u'\u2573')
    }


def board_line(tp, column_witdh):
    ret = corners["left"][tp]
    for c in range(len(column_witdh)):
        for i in range(column_witdh[c] +1):
            ret += corners["horizontal"]["normal"]
        if c != len(column_witdh) - 1:
            ret+= corners["horizontal"][tp]
    ret += corners["right"][tp]
    return ret + "\n"
def content_line(column_witdh, content):
    ret = ""
    for i in range(len(column_witdh)):
        ret += corners["vertical"]["normal"]
        ret += content[i].rjust(column_witdh[i]) + " "
    ret += corners["vertical"]["normal"]
    return ret +"\n"
def format_table( content, column_witdh=None, backward = True):
    if column_witdh == None:
        column_witdh = [5] * len(content[0])
    ret = ""
    myrange = range(-1,len(content))
    if backward:
        myrange.reverse()
        first = "down"
        last = "up"
    else:
        first = "up"
        last = "down"
    for line in myrange:
        if line == -1:
            if not backward:
                ret += content_line(column_witdh, content[line])
            ret += board_line(first, column_witdh)
        elif not backward and line == len(content) -1:
            ret += content_line(column_witdh, content[line])
            ret += board_line(last, column_witdh)
        elif backward and line == 0:
            ret += content_line(column_witdh, content[line])
        elif backward and line == len(content) - 1:
            ret += board_line(last, column_witdh)
            ret += content_line(column_witdh, content[line])
            ret += board_line("middle", column_witdh)
        else:
            ret += content_line(column_witdh, content[line])
            ret += board_line("middle", column_witdh)
    return ret

if __name__ == "__main__":
    print format_table([["um","dois","tres"],["quatro","cinco", "seis"]],[7,6,6])


class Base:
    def __print__(self, message):
        msg = self.name + "[ " + message + "]"
        if self.logFile == None:
            print msg
        else:
            f = open(logFile,"a")
            f.writeline(msg)
            f.close()
        

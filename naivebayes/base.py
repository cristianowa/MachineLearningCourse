import time
class Base:
    def __print__(self, message):
        now = time.localtime()
        msg = self.name + "[" + str(now.tm_hour) + ":" 
        msg += str(now.tm_min) + ":" + str(now.tm_sec)
        msg += "[ " + message + "]"
        if self.logFile == None:
            print msg
        else:
            f = open(logFile,"a")
            f.writeline(msg)
            f.close()
        

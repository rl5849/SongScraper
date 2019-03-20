##Author: rl5849
import datetime

class Logging:
    def logInfo(self, message):
        currentDT = datetime.datetime.now()

        f = open("log.txt", "a")
        f.write(currentDT.strftime("%Y-%m-%d %H:%M:%S") + ": " + message+"\n")
        f.close()
        return
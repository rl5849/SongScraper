##Author: rl5849
import datetime
import secrets

class Logging:
    loggingDir = secrets.logging_path

    def logInfo(self, message):
        currentDT = datetime.datetime.now()

        f = open(self.loggingDir, "a")
        f.write("INFO: " + currentDT.strftime("%Y-%m-%d %H:%M:%S") + ": " + message+"\n")
        f.close()
        return

    def logError(self, message):
        currentDT = datetime.datetime.now()

        f = open(self.loggingDir, "a")
        f.write("ERROR: " + currentDT.strftime("%Y-%m-%d %H:%M:%S") + ": " + message+"\n")
        f.close()
        return
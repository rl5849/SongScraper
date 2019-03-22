##Author: rl5849
import datetime
import secrets

class Logging:
    def logInfo(self, message):
        currentDT = datetime.datetime.now()

        f = open(secrets.logging_path, "a")
        f.write("INFO: " + currentDT.strftime("%Y-%m-%d %H:%M:%S") + ": " + message+"\n")
        f.close()
        return

    def logError(self, message):
        currentDT = datetime.datetime.now()

        f = open(secrets.logging_path, "a")
        f.write("ERROR: " + currentDT.strftime("%Y-%m-%d %H:%M:%S") + ": " + message+"\n")
        f.close()
        return
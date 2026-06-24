import os
import config

def createDB():
    if not os.path.exists(config.LONG_TERM_MEMORY):
        file = open(config.LONG_TERM_MEMORY,"x")
        file.close()
    if not os.path.exists(config.SHORT_TERM_MEMORY):
        file = open(config.SHORT_TERM_MEMORY,"x")
        file.close()
    if not os.path.exists(config.USER_PROFILE):
        file = open(config.USER_PROFILE,"x")
        file.close

def updateHistory(sessionHistory: list, prompt, reply):
    sessionHistory.append("user:"+prompt)
    sessionHistory.append("AI:"+reply)
    return sessionHistory
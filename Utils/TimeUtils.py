
import time
import datetime

def getCurrentEpochTime() -> int:
    return int(time.time())

def epochToLocal(epochTime: int) -> str:
    return time.strftime("%I:%M %p", time.localtime(epochTime))

def getCurrentDate() -> str:
    return datetime.datetime.now().strftime("%b_%d_%Y")

def wait(seconds: int):
    time.sleep(seconds)

import time
import datetime

def getCurrentEpochTime() -> int:
    return int(time.time())

def epochToLocalTime(epochTime: int) -> str:
    return time.strftime("%I:%M %p", time.localtime(epochTime))

def epochToLocalDateAndTime(epochTime: int) -> str:
    return time.strftime("%b %d %Y %I:%M %p", time.localtime(epochTime))

def getCurrentDate() -> str:
    return datetime.datetime.now().strftime("%Y_%m_%d")

def wait(minutes: int):
    time.sleep(60 * minutes)

import time

def getCurrentEpochTime() -> int:
    return int(time.time())

def epochToLocal(epochTime: int) -> str:
    return time.strftime("%I:%M %p", time.localtime(epochTime))

# count down in hh:mm:ss format
def countDown(seconds: int):
    
    while seconds > 0:
    
        timeLeft = time.strftime("%H:%M:%S", time.gmtime(seconds))
        print(timeLeft, end="\r")
        time.sleep(1)
        seconds -= 1
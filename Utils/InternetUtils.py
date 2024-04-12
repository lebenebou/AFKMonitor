
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)

import sys
sys.path.append("..")

from Utils.CmdUtils import runCommand
import psutil

class InternetState:

    def __init__(self):
        
        self.isConnected = isConnected()

        ioCounters = psutil.net_io_counters()
        self.bytesSent = ioCounters.bytes_sent
        self.bytesRecv = ioCounters.bytes_recv

def isConnected() -> bool:
    return runCommand("ping -n 1 www.google.com").returncode == 0

if __name__=="__main__":
    print(isConnected())
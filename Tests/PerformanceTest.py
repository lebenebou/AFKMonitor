
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)

import sys
sys.path.append("..")
from ComputerState import ComputerState

import time

def benchMarkComputerState() -> int:
    
    startTime = time.time()
    ComputerState()
    endTime = time.time()
    
    return int((endTime - startTime) * 1000)

if __name__=="__main__":
    
    testCount = 20
    MsThreshold = 2000
    
    averageTimeMs = 0

    print(f"Running {testCount} tests...\n")
    for i in range(testCount):

        timeMs = benchMarkComputerState()
        assert timeMs <= MsThreshold, f"Test {i+1} failed: took {timeMs} ms"

        print(f"Test {i+1}\tgetComputerState: {timeMs} ms", flush=True)

        averageTimeMs += timeMs

    averageTimeMs /= testCount
    print(f"\nTests finished. Average time: {averageTimeMs} ms")

import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)

import sys
sys.path.append("..")

from ComputerState import ComputerState

from Utils.InternetUtils import isConnected
from Utils.BatteryUtils import getBatteryPercentage
from Utils.ProcessUtils import MemoryState

import time

def benchMarkFuntion(func) -> int:
    
    startTime = time.time()
    func()
    endTime = time.time()
    
    return int((endTime - startTime) * 1000)

def runPerformanceTest(func, testCount: int, msThreshold: int):

    averageTimeMs = 0
    functionName = func.__name__

    print(f"\nRunning {testCount} tests for {functionName}...", flush=True)
    for i in range(1, testCount+1):

        timeMs = benchMarkFuntion(func)
        assert timeMs <= msThreshold, f"Test {i+1} failed: {functionName} took {timeMs} ms"

        print(f"Test {i} passed. {functionName} took {timeMs} ms", end="\r", flush=True)

        averageTimeMs += timeMs

    averageTimeMs /= testCount
    print(f"Tests finished. Average time for {functionName}: {averageTimeMs} ms", flush=True)

if __name__=="__main__":
    
    runPerformanceTest(testCount=10, msThreshold=500, func=isConnected)
    runPerformanceTest(testCount=10, msThreshold=500, func=MemoryState)
    runPerformanceTest(testCount=10, msThreshold=50, func=getBatteryPercentage)
    
    runPerformanceTest(testCount=10, msThreshold=1000, func=ComputerState)

    print("\nAll tests passed.", flush=True)
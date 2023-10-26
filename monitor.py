
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)
import sys
import argparse
import time
import pandas

from Utils import AutomationUtils
from Utils import BatteryUtils
from Utils import InternetUtils
from Utils import TimeUtils

from ComputerState import ComputerState

def getCurrentComputerState() -> ComputerState:

    return ComputerState(
        
        TimeUtils.getCurrentEpochTime(),
        BatteryUtils.getBatteryPercentage(),
        BatteryUtils.getChargingState(),
        InternetUtils.isConnected()
    )

def getDailyCsvPath() -> str:

    currentDate = TimeUtils.getCurrentDate()
    csvFileName = f"{currentDate}.csv"
    return os.path.join(".\\Reports", csvFileName)

def batchExportToDailyCsv(states: list[ComputerState]):

    if len(states) == 0:
        return
    
    dailyCsvPath = getDailyCsvPath()
    
    if not os.path.exists(dailyCsvPath):

        columnTitles = states[0].toDict().keys()
        columnTitles = pandas.DataFrame(columns=columnTitles)
        columnTitles.to_csv(dailyCsvPath, index=False, header=True)

    dataFrames = [state.toDataFrame() for state in states]
    combinedDataFrame = pandas.concat(dataFrames, ignore_index=True)
    combinedDataFrame.to_csv(dailyCsvPath, mode="a", index=False, header=True)

if __name__=="__main__":

    os.system("cls")
    parser = argparse.ArgumentParser()
    parser.add_argument("minuteInterval", type=int, help="Check computer state every interval")
    parser.add_argument("batteryThreshold", type=int, help="Battery percentage threshold (negative to shutdown when unplugged)")
    parser.add_argument("maxBufferSize", type=int, nargs="?", default=5, help="[optional] Maximum size of state buffer before exporting to CSV")

    args = parser.parse_args()
    minuteInterval = args.minuteInterval
    batteryThreshold = args.batteryThreshold
    maxStateBufferSize = args.maxBufferSize
    
    if minuteInterval < 1 or minuteInterval > 60:

        print("Monitor interval must be at least 1 minute, and at most 60", file=sys.stderr)
        exit(1)

    if maxStateBufferSize < 0 or maxStateBufferSize > 50:

        print("maxBufferSize is invalid, must be between 0 and 100", file=sys.stderr)
        exit(1)

    currentState = getCurrentComputerState()
    
    if batteryThreshold < 0 and not currentState.pluggedIn:
        
        print("Battery threshold is negative and computer is already unplugged.", file=sys.stderr)
        exit(1)

    if currentState.batteryPercent <= batteryThreshold:

        print(f"Battery threshold cannot be lower than current battery percentage ({currentState.batteryPercent}%).", file=sys.stderr)
        exit(1)

    stateBuffer: list[ComputerState] = []

    os.system("cls")
    # START MONITORING
    if batteryThreshold < 0:
        print(f"Monitoring every {minuteInterval} minutes until unplugged...\n")
    else:
        print(f"Monitoring every {minuteInterval} minutes with a battery threshold of {batteryThreshold}%...\n")
    
    while True:

        currentState = getCurrentComputerState()
        print(currentState, end="\t")

        stateBuffer.append(currentState)

        if len(stateBuffer) >= maxStateBufferSize:
            
            try:
                batchExportToDailyCsv(stateBuffer)
                print("(Saved to CSV)", end="")
                stateBuffer.clear()

            except PermissionError:
                print("(Unable to save, daily CSV is open)", end="")

        print(end="\n", flush=True)

        if currentState.batteryPercent <= batteryThreshold:

            print("Battery threshold reached. Shutting down...")
            AutomationUtils.shutdown()
            exit(0)

        if batteryThreshold < 0 and not currentState.pluggedIn:
            
            print("Computer was unplugged. Shutting down...")
            AutomationUtils.shutdown()
            exit(0)

        time.sleep(60 * minuteInterval)
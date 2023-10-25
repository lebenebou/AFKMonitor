
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)
import sys
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

def exportStateToCsv(state: ComputerState, csvFilePath: str):

    if not os.path.exists(csvFilePath):

        columnTitles = state.toDict().keys()
        columnsDataFrame = pandas.DataFrame(columns=columnTitles)
        columnsDataFrame.to_csv(csvFilePath, index=False, header=True)

    state.toDataFrame().to_csv(csvFilePath, mode="a", index=False, header=False)

def getDailyCsvPath() -> str:

    currentDate = TimeUtils.getCurrentDate()
    csvFileName = f"{currentDate}.csv"
    return os.path.join(".\\Reports", csvFileName)

def exportStateToDailyCsv(state: ComputerState):

    dailyCsvPath = getDailyCsvPath()
    exportStateToCsv(state, dailyCsvPath)

def batchExportToDailyCsv(states: list[ComputerState]):

    dailyCsvPath = getDailyCsvPath()

    for state in states:
        exportStateToCsv(state, dailyCsvPath)

def printUsageMessage():

    usageMessage = "Usage: python monitor.py <interval> <battery threshold> (Negative threshold to shutdown when unplugged)"
    print(usageMessage, file=sys.stderr)

if __name__=="__main__":

    os.system("cls")
    if len(sys.argv) != 3:

        printUsageMessage()
        exit(1)

    try:
        int(sys.argv[1])
        int(sys.argv[2])
    except ValueError:
        print("Invalid arguments", file=sys.stderr)
        printUsageMessage()
        exit(1)

    minuteInterval = int(sys.argv[1])
    batteryThreshold = int(sys.argv[2])
    
    if minuteInterval < 1 or minuteInterval > 60:

        print("Monitor interval must be at least 1 minute, and at most 60", file=sys.stderr)
        exit(1)

    currentState = getCurrentComputerState()
    
    if batteryThreshold < 0 and not currentState.pluggedIn:
        
        print("Battery threshold is negative and computer is already unplugged.", file=sys.stderr)
        exit(1)

    if currentState.batteryPercent <= batteryThreshold:

        print("Battery threshold cannot be lower than current battery percentage.", file=sys.stderr)
        exit(1)

    stateBuffer: list[ComputerState] = []
    maxStateBufferSize = 5

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
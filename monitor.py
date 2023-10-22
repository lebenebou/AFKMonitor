
import os
currentDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(currentDir)
import sys
import time
import datetime
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

    dataFrame = pandas.DataFrame([state.toDict()])
    
    if not os.path.exists(csvFilePath):

        columnTitles = state.toDict().keys()
        dataFrame = pandas.DataFrame(columns=columnTitles)
        dataFrame.to_csv(csvFilePath, index=False, header=True)

    dataFrame = pandas.DataFrame([state.toDict()])

    dataFrame.replace({True: "Yes", False: "No"}, inplace=True)
    dataFrame["time"] = dataFrame["time"].apply(TimeUtils.epochToLocal)

    dataFrame.to_csv(csvFilePath, mode="a", index=False, header=False)

def exportStateToDailyCsv(state: ComputerState):

    currentDate = datetime.datetime.now().strftime("%b_%d_%Y")
    csvFileName = f"{currentDate}.csv"
    savePath = os.path.join(".\\Reports", csvFileName)

    exportStateToCsv(state, savePath)

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

    currentState = getCurrentComputerState()

    if minuteInterval < 1:

        print("Monitor interval must be at least 1 minute.", file=sys.stderr)
        exit(1)

    if batteryThreshold < 0 and not currentState.pluggedIn:
        
        print("Battery threshold is negative and computer is already unplugged.", file=sys.stderr)
        exit(1)

    if currentState.batteryPercent <= batteryThreshold:

        print("Battery threshold cannot be lower than current battery percentage.", file=sys.stderr)
        exit(1)

    os.system("cls")
    # START MONITORING
    if batteryThreshold < 0:
        print(f"Monitoring every {minuteInterval} minutes until unplugged...\n")
    else:
        print(f"Monitoring every {minuteInterval} minutes with a battery threshold of {batteryThreshold}%...\n")
    
    while True:

        currentState = getCurrentComputerState()
        print(currentState, end="\t")

        try:
            exportStateToDailyCsv(currentState)
            print("(Saved to CSV)")
        except PermissionError:
            print("(Unable to save, CSV is open)")

        if currentState.batteryPercent <= batteryThreshold:

            print("Battery threshold reached. Shutting down...")
            AutomationUtils.shutdown()
            exit(0)

        if batteryThreshold < 0 and not currentState.pluggedIn:
            
            print("Computer was unplugged. Shutting down...")
            AutomationUtils.shutdown()
            exit(0)

        time.sleep(60 * minuteInterval)
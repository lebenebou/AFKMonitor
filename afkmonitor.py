
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)

import sys
import argparse

from ComputerState import ComputerState
from Utils.CmdUtils import runPythonScriptInNewWindow

from Utils.TimeUtils import wait
from Utils.ExportUtils import exportStates

def safeExit(stateBuffer: list[ComputerState], scriptPath: str = None):

    try:
        exportStates(stateBuffer)
    except PermissionError:
        print("Unable to exit, please close open CSV files.", file=sys.stderr)
        return

    if scriptPath is not None:
        print(f"Running {scriptPath}", end="\n", flush=True)
        runPythonScriptInNewWindow(scriptPath)

    exit(0)

def handleKeyboardInterrupt(stateBuffer: list[ComputerState]):

    if len(stateBuffer) == 0:
        exit(0)

    single: bool = (len(stateBuffer) == 1)
    message = f"\nYou still have {len(stateBuffer)} unsaved state{(not single)*'s'} in the buffer!\nDo you want to save {'it' if single else 'them'} to CSV? (y/n): "
    
    if input(message).strip().lower() != "y":
        exit(0)
    
    safeExit(stateBuffer)

def startMonitoring(batteryThreshold: int = 20, scriptPath: str = None, minuteInterval: int = 5, maxStateBufferSize: int = 5):

    os.system("cls")
    print(f"Monitoring until ", end="")
    if batteryThreshold < 0:
        print(f"unplugged.")
    else:
        print(f"battery reaches {batteryThreshold}%.")

    if scriptPath is not None:
        print(f"Running {scriptPath} when done.")

    print(end="\n", flush=True)

    currentState = ComputerState()
    stateBuffer: list[ComputerState] = []
    
    while True:

        currentState.update()
        print(currentState, end="\t")

        stateBuffer.append(currentState)

        if len(stateBuffer) >= maxStateBufferSize:
            
            try:
                exportStates(stateBuffer)
                print("(Saved to CSV)", end="")
                stateBuffer.clear()

            except PermissionError:
                print("(Unable to save, CSV is open)", end="")

        print(end="\n", flush=True)

        if batteryThreshold < 0 and not currentState.pluggedIn:
            print("Computer unplugged. Stopping...")
            safeExit(stateBuffer, scriptPath)

        if currentState.batteryPercent <= batteryThreshold:
            print("Battery threshold reached. Stopping...")
            safeExit(stateBuffer, scriptPath)

        try:
            wait(minuteInterval)
        except KeyboardInterrupt:
            handleKeyboardInterrupt(stateBuffer)

if __name__=="__main__":

    os.system("cls")
    parser = argparse.ArgumentParser()
    parser.add_argument("batteryThreshold", type=int, help="Battery percentage threshold (-1 to shutdown when unplugged)")
    parser.add_argument("--scriptPath", type=str, help="path to python script to run when monitoring ends")

    args = parser.parse_args()
    batteryThreshold = args.batteryThreshold
    scriptPath = args.scriptPath

    currentState = ComputerState()
    
    if batteryThreshold < 0 and not currentState.pluggedIn:
        print("Battery threshold is negative and computer is already unplugged.", file=sys.stderr, flush=True)
        exit(1)

    if currentState.batteryPercent <= batteryThreshold:
        print(f"Battery threshold cannot be higher than current battery percentage: {currentState.batteryPercent}%", file=sys.stderr, flush=True)
        exit(1)

    if args.scriptPath is not None and not args.scriptPath.endswith(".py"):
        print("Script must be a python file", file=sys.stderr, flush=True)
        exit(1)

    if args.scriptPath is not None and not os.path.isfile(args.scriptPath):
        print(f"Path does not exist: {args.scriptPath}", file=sys.stderr, flush=True)
        exit(1)

    del currentState
    startMonitoring(batteryThreshold, args.scriptPath)
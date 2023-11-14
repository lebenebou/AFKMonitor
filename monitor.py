
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)

import sys
import argparse

from ComputerState import ComputerState

from Utils.CmdUtils import shutdown
from Utils.TimeUtils import wait
from Utils.ExportUtils import exportStates

def handleKeyboardInterrupt(stateBuffer: list[ComputerState]):

    if len(stateBuffer) == 0:
        exit(0)

    single: bool = (len(stateBuffer) == 1)
    message = f"\nYou still have {len(stateBuffer)} unsaved state{(not single)*'s'} in the buffer!\nDo you want to save {'it' if single else 'them'} to CSV? (y/n): "
    
    if input(message).strip().lower() != "y":
        exit(0)

    try:
        exportStates(stateBuffer)

    except PermissionError:
        print("Unable to save, please close all open CSVs.\n")
        return
        
    exit(0)

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

        print("maxBufferSize is invalid, must be between 0 and 50", file=sys.stderr)
        exit(1)

    currentState = ComputerState()
    
    if batteryThreshold < 0 and not currentState.pluggedIn:
        
        print("Battery threshold is negative and computer is already unplugged.", file=sys.stderr)
        exit(1)

    if currentState.batteryPercent <= batteryThreshold:

        print(f"Battery threshold cannot be higherthan current battery percentage ({currentState.batteryPercent}%).", file=sys.stderr)
        exit(1)

    os.system("cls")
    # START MONITORING
    if batteryThreshold < 0:
        print(f"Monitoring every {minuteInterval} minutes until unplugged...\n")
    else:
        print(f"Monitoring every {minuteInterval} minutes with a battery threshold of {batteryThreshold}%...\n")

    stateBuffer: list[ComputerState] = []
    
    while True:

        currentState = ComputerState()
        print(currentState, end="\t")

        stateBuffer.append(currentState)

        if len(stateBuffer) >= maxStateBufferSize:
            
            try:
                exportStates(stateBuffer)
                print("(Saved to CSV)", end="")
                stateBuffer.clear()

            except PermissionError:
                print("(Unable to save, CSVs are open)", end="")

        print(end="\n", flush=True)

        if batteryThreshold < 0 and not currentState.pluggedIn:
            
            print("Computer was unplugged. Shutting down...")
            shutdown()
            exit(0)

        if currentState.batteryPercent <= batteryThreshold:

            print("Battery threshold reached. Shutting down...")
            shutdown()
            exit(0)

        try:
            wait(minuteInterval)
        except KeyboardInterrupt:
            handleKeyboardInterrupt(stateBuffer)
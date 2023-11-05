
import json
import pandas

from Utils.TimeUtils import getCurrentEpochTime, epochToLocal
from Utils.InternetUtils import isConnected
from Utils.BatteryUtils import getBatteryPercentage, getChargingState
from Utils.ProcessUtils import getCurrentMemoryState

class ComputerState:

    def __init__(self):

        self.epochTime = getCurrentEpochTime()

        self.batteryPercent = getBatteryPercentage()
        self.pluggedIn = getChargingState()
        self.connectedWiFi = isConnected()

        memoryState = getCurrentMemoryState()
        self.runningProcesses = memoryState.runningProcesses
        self.TotalMemoryUsageMB = memoryState.totalMemoryUsageMB
        self.HungriestProcessName = memoryState.hungriestProcessName
        self.HungriestProcessMemoryUsageMB = memoryState.hungriestProcessMemoryUsageMB

    def localTime(self) -> str:
        return epochToLocal(self.epochTime)

    def __str__(self) -> str:

        state = self.localTime() + "\t"
        state += f"Battery: {self.batteryPercent}%\t"
        state += f"Charging: {'YES' if self.pluggedIn else 'NO'}\t"
        state += f"Connected: {'YES' if self.connectedWiFi else 'NO'}\t"
        state += f"MemUsage: {self.TotalMemoryUsageMB:.2f} MB\t"

        return state

    def toDict(self) -> dict:

        return {
            "time": self.epochTime,

            "batteryPercent": self.batteryPercent,
            "charging": self.pluggedIn,
            "connected": self.connectedWiFi,

            "runningProc": self.runningProcesses,
            "memUsageMB": self.TotalMemoryUsageMB,
            "hungriestProc": self.HungriestProcessName,
            "hungryProcMem": self.HungriestProcessMemoryUsageMB
        }

    def toJson(self) -> str:
        return json.dumps(self.toDict())
    
    def toDataFrame(self) -> pandas.DataFrame:

        dataFrame = pandas.DataFrame([self.toDict()])
        
        # boolean values
        dataFrame.replace({True: "Yes", False: "No"}, inplace=True)

        # convert time from echop to local. example: 2:15 PM instead of 1612341234
        dataFrame["time"] = dataFrame["time"].apply(epochToLocal)

        # round floats to 2 decimal places
        dataFrame["memUsageMB"] = dataFrame["memUsageMB"].apply(lambda x: round(x, 2))
        dataFrame["hungryProcMem"] = dataFrame["hungryProcMem"].apply(lambda x: round(x, 2))
        
        return dataFrame

import json
import pandas

from Utils.TimeUtils import getCurrentEpochTime, epochToLocal
from Utils.InternetUtils import getInternetState
from Utils.BatteryUtils import getBatteryPercentage, getChargingState
from Utils.ProcessUtils import MemoryState

class ComputerState:

    def __init__(self):

        self.epochTime = getCurrentEpochTime()

        self.batteryPercent = getBatteryPercentage()
        self.pluggedIn = getChargingState()
        
        internetState = getInternetState()
        self.isConnected = internetState.isConnected
        self.bytesSent = internetState.bytesSent
        self.bytesReceived = internetState.bytesRecv

        memoryState = MemoryState()
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
        state += f"Connected: {'YES' if self.isConnected else 'NO'}\t"
        state += f"MemUsage: {self.TotalMemoryUsageMB:.2f} MB\t"

        return state

    def toDict(self) -> dict:

        return {
            "time": self.epochTime,
            "localTime": self.localTime(),

            "batteryPercent": self.batteryPercent,
            "charging": self.pluggedIn,

            "connected": self.isConnected,
            "bytesSent": self.bytesSent,
            "bytesReceived": self.bytesReceived,

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

        # round floats to 2 decimal places
        dataFrame["memUsageMB"] = dataFrame["memUsageMB"].apply(lambda x: round(x, 2))
        dataFrame["hungryProcMem"] = dataFrame["hungryProcMem"].apply(lambda x: round(x, 2))
        
        return dataFrame
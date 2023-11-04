
import json
import pandas

from Utils import TimeUtils, BatteryUtils, InternetUtils, ProcessUtils

class ComputerState:

    def __init__(self):

        self.epochTime = TimeUtils.getCurrentEpochTime()

        self.batteryPercent = BatteryUtils.getBatteryPercentage()
        self.pluggedIn = BatteryUtils.getChargingState()
        self.connectedWiFi = InternetUtils.isConnected()

        memoryState = ProcessUtils.getCurrentMemoryState()
        self.runningProcesses = memoryState.runningProcesses
        self.TotalMemoryUsageMB = memoryState.totalMemoryUsageMB
        self.HungriestProcessName = memoryState.hungriestProcessName
        self.HungriestProcessMemoryUsageMB = memoryState.hungriestProcessMemoryUsageMB

    def localTime(self) -> str:
        return TimeUtils.epochToLocal(self.epochTime)

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
        
        dataFrame.replace({True: "Yes", False: "No"}, inplace=True)
        dataFrame["time"] = dataFrame["time"].apply(TimeUtils.epochToLocal)
        
        return dataFrame
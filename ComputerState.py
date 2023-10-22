
import json
import pandas
from Utils import TimeUtils

class ComputerState:

    def __init__(self, epochTime: int, batteryPercent: int, pluggedIn: bool, connectedWiFi: bool):

        self.epochTime = epochTime
        self.batteryPercent = batteryPercent
        self.pluggedIn = pluggedIn
        self.connectedWiFi = connectedWiFi

    def localTime(self) -> str:
        return TimeUtils.epochToLocal(self.epochTime)

    def __str__(self):

        state = self.localTime() + "\t"
        state += f"Battery: {self.batteryPercent}%\t"
        state += f"Charging: {'yes' if self.pluggedIn else 'no'}\t"
        state += f"Connected: {'yes' if self.connectedWiFi else 'no'}"
        return state

    def toDict(self) -> dict:

        return {
            "time": self.epochTime,
            "batteryPercent": self.batteryPercent,
            "charging": self.pluggedIn,
            "connected": self.connectedWiFi
        }

    def toJson(self) -> str:
        return json.dumps(self.toDict())
    
    def toDataFrame(self) -> pandas.DataFrame:

        dataFrame = pandas.DataFrame([self.toDict()])
        
        dataFrame.replace({True: "Yes", False: "No"}, inplace=True)
        dataFrame["time"] = dataFrame["time"].apply(TimeUtils.epochToLocal)
        
        return dataFrame
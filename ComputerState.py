
import json
import pandas

from Utils import TimeUtils, BatteryUtils, InternetUtils

class ComputerState:

    def __init__(self):

        self.epochTime = TimeUtils.getCurrentEpochTime()
        self.batteryPercent = BatteryUtils.getBatteryPercentage()
        self.pluggedIn = BatteryUtils.getChargingState()
        self.connectedWiFi = InternetUtils.isConnected()

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
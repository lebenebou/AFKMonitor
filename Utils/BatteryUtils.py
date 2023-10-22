
import psutil

def getBatteryPercentage() -> int:

    return int(psutil.sensors_battery().percent)

def getChargingState() -> bool:

    return psutil.sensors_battery().power_plugged
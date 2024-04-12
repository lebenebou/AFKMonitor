
from UserInputs import AFKMonitorInputs
from afkmonitor import startMonitoring

if __name__ == "__main__":

    userInputs = AFKMonitorInputs()
    startMonitoring(userInputs.batteryLimit, userInputs.scriptToRun)
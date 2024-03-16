
import sys
import os
from ComputerState import ComputerState

class Condition:

    def __init__(self, function: callable, errorMessage: str):

        self.validatorFunction = function
        self.errorMessage = errorMessage.strip().capitalize().strip(".") + "."
        
    def check(self, value: int) -> bool:
        return self.validatorFunction(value)

class InputValue:

    def __init__(self, name: str):

        self.name = name.strip()
        self.conditions: list[Condition] = []

    def addCondition(self, function: callable, errorMessage: str):
        self.conditions.append(Condition(function, errorMessage))

    def __validate(self, value: int) -> bool:

        for condition in self.conditions:

            if not condition.check(value):
                print(condition.errorMessage, file=sys.stderr)
                return False

        return True

    def getValueFromUser(self) -> int:

        while True:

            try:
                value = int(input(f"Enter {self.name}: "))

                if not self.__validate(value):
                    continue # error message is printed
                
                return value
                
            except ValueError:
                print("Value must be an integer.")
                continue

class AFKMonitorInputs:

    def __init__(self):

        self.getInputsFromUser()

    def getInputsFromUser(self):
        
        currentState = ComputerState()

        intervalInput = InputValue("monitoring interval (min)")
        intervalInput.addCondition(lambda x: x > 0 and x <= 60, "monitoring interval must be between 1 and 60 minutes")
        intervalInput.addCondition(lambda x: currentState.pluggedIn or x > currentState.batteryPercent, "PC might shutdown before anything is monitored")
        self.monitoringInterval = intervalInput.getValueFromUser()

        monitoringDurationInput = InputValue("monitoring duration (hours)")
        monitoringDurationInput.addCondition(lambda x: x > 0, "monitoring duration must be greater than 0")
        monitoringDurationInput.addCondition(lambda x: self.monitoringInterval != 60 or x!=1, "no need to monitor for 1 hour if monitoring interval is 60 minutes")
        self.monitoringDuration = monitoringDurationInput.getValueFromUser()

        batteryLimitInput = InputValue("battery limit (%)")
        batteryLimitInput.addCondition(lambda x: x >= 0 and x < currentState.batteryPercent, f"battery limit must be between 0 and current battery")
        self.batteryLimit = batteryLimitInput.getValueFromUser()


if __name__ == "__main__":

    inputs = AFKMonitorInputs()

    os.system("cls")
    print(f"Monitoring interval: {inputs.monitoringInterval} minutes.")
    print(f"Monitoring duration: {inputs.monitoringDuration} hours.")
    print(f"Battery limit: {inputs.batteryLimit}%.")
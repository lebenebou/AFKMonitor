
import sys
import os
from ComputerState import ComputerState

class Condition:

    def __init__(self, predicate: callable, errorMessage: str, isCritical = True):

        self.predicate = predicate
        self.errorMessage = errorMessage.strip().capitalize().strip(".") + "."
        self.isCritical = isCritical
        
    def isMet(self, value: int) -> bool:
        return self.predicate(value)

class InputValue:

    def __init__(self, name: str):

        self.name = name.strip()
        self.conditions: list[Condition] = []

    def addCondition(self, predicate: callable, errorMessage: str, isCritical = True):
        self.conditions.append(Condition(predicate, errorMessage, isCritical))

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

    # private
    def __validate(self, value: int) -> bool:

        for condition in self.conditions:

            if not condition.isMet(value):

                print(condition.errorMessage, file=sys.stderr)

                if not condition.isCritical and self.__userWantsToContinueAnyway():
                    continue

                return False

        return True

    # private
    def __userWantsToContinueAnyway(self) -> bool:

        response = input("Continue anyway? (y/n): ").strip().lower()
        return response == "y"

class AFKMonitorInputs:

    def __init__(self):

        self.__getInputsFromUser()

    # private
    def __getInputsFromUser(self):
        
        currentState = ComputerState()

        intervalInput = InputValue("monitoring interval (min)")
        intervalInput.addCondition(lambda m: m > 0 and m <= 60, "monitoring interval must be between 1 and 60 minutes")
        intervalInput.addCondition(lambda m: currentState.pluggedIn or m > currentState.batteryPercent, "PC might shutdown before anything is monitored", isCritical=False)
        self.monitoringInterval = intervalInput.getValueFromUser()

        monitoringDurationInput = InputValue("monitoring duration (hours)")
        monitoringDurationInput.addCondition(lambda h: h > 0, "monitoring duration must be greater than 0")
        monitoringDurationInput.addCondition(lambda h: self.monitoringInterval != 60 or h != 1, "no need to monitor for 1 hour if monitoring interval is 60 minutes")
        self.monitoringDuration = monitoringDurationInput.getValueFromUser()

        batteryLimitInput = InputValue("battery limit (%)")
        batteryLimitInput.addCondition(lambda p: p >= 0 and p < currentState.batteryPercent, f"battery limit must be between 0 and current battery")
        self.batteryLimit = batteryLimitInput.getValueFromUser()


if __name__ == "__main__":

    inputs = AFKMonitorInputs()

    os.system("cls")
    print(f"Monitoring interval: {inputs.monitoringInterval} minutes.")
    print(f"Monitoring duration: {inputs.monitoringDuration} hours.")
    print(f"Battery limit: {inputs.batteryLimit}%.")
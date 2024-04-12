
import sys
import os
from ComputerState import ComputerState
from tkinter import filedialog

class Condition:

    def __init__(self, predicate: callable, errorMessage: str, isCritical = True):

        self.predicate = predicate
        self.errorMessage = errorMessage.strip().capitalize().strip(".") + "."
        self.isCritical = isCritical
        
    def isMet(self, value) -> bool:

        try:
            return self.predicate(value)
        except:
            try:
                return self.predicate(int(value))
            except:
                return False

class InputValue:

    def __init__(self, name: str):

        self.name = name.strip()
        self.conditions: list[Condition] = []

    def addCondition(self, predicate: callable, errorMessage: str, isCritical = True):
        self.conditions.append(Condition(predicate, errorMessage, isCritical))

    def getValueFromUser(self) -> str:

        while True:

            value = input(f"Enter {self.name}: ")

            if not self.__validate(value):
                continue # error message is printed
            
            return value

    def getFilePathFromUser(self) -> str:

        while True:

            value = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])

            if not self.__validate(value):
                continue # error message is printed
            
            return value

    # private
    def __validate(self, value) -> bool:

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

        batteryLimitInput = InputValue("battery limit (%)")
        batteryLimitInput.addCondition(lambda p: p == -1 or (p >= 0 and p < currentState.batteryPercent), "battery limit must be between 0 and current battery, or -1 to stop when unlpugged")
        batteryLimitInput.addCondition(lambda p: p != -1 or currentState.pluggedIn, "PC is already unplugged")
        self.batteryLimit = int(batteryLimitInput.getValueFromUser())

        self.scriptToRun = None

        if input("Would you like to run a python script when monitoring ends? (y/n): ").strip().lower() != "y":
            return

        scriptToRun = InputValue("python file path to run when monitoring ends")
        scriptToRun.addCondition(lambda f: f is not None, "no file chosen")
        scriptToRun.addCondition(lambda f: os.path.exists(f) and f.endswith(".py"), "file must be a python file that exists")
        self.scriptToRun = scriptToRun.getFilePathFromUser()


if __name__ == "__main__":

    inputs = AFKMonitorInputs()
    os.system("cls")

    print(f"Battery limit: {inputs.batteryLimit}%.")
    print(f"File to run: {inputs.scriptToRun}")
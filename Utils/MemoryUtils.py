
from Utils.CmdUtils import runCommand
import re

class MemoryState:

    tasklistRegex = re.compile(r"^(\S+)\s+\d+\s+\S+\s+\d\s+(\S+) K$", re.MULTILINE)

    def __init__(self):
        
        tasklist = runCommand("tasklist /nh").stdout

        memUsage = dict()

        hungriestProcessName: str = None
        hungriestProcessMemUsageKB: float = 0
        totalMemUsageKB: float = 0

        for reMatch in MemoryState.tasklistRegex.finditer(tasklist):

            name, memKB = reMatch.group(1), float(reMatch.group(2).replace(",", ""))

            memUsage.setdefault(name, 0)
            memUsage[name] += memKB

            totalMemUsageKB += memKB

            if memUsage[name] > hungriestProcessMemUsageKB:

                hungriestProcessName = name
                hungriestProcessMemUsageKB = memUsage[name]

        self.runningProcesses = len(memUsage)
        self.totalMemoryUsageMB = totalMemUsageKB / 1000
        self.hungriestProcessMemUsageMB = hungriestProcessMemUsageKB / 1000
        self.hungriestProcessName = hungriestProcessName

if __name__ == "__main__":

    currentMemoryState = MemoryState()

    print(f"Total running processes: {currentMemoryState.runningProcesses}")
    print(f"Total memory usage: {currentMemoryState.totalMemoryUsageMB} MB")
    print(f"Hungriest process: {currentMemoryState.hungriestProcessName} ({currentMemoryState.hungriestProcessMemUsageMB} MB)")
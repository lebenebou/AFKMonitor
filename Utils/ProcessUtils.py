
from Utils.CmdUtils import runCommand

class Process:

    def __init__(self, name: str, memoryUsageMB: float):

        self.name = name
        self.memoryUsageMB = memoryUsageMB

    @staticmethod
    def extractProcessFromLine(line: str):

        line = line.strip().replace(",", "").replace("N/A", "0")
        values = line.split("\"\"")
        values = [value.strip("\"") for value in values]
        values[4] = values[4].strip(" K")

        name = values[0]
        memoryUsageMB = float(values[4]) / 1000

        return Process(name, memoryUsageMB)

    @staticmethod
    def getRunningProcesses() -> list:

        commandOutput = runCommand("tasklist /fo csv /nh").stdout
        lines = commandOutput.splitlines()

        processes = [Process.extractProcessFromLine(line) for line in lines]
        memUsage = dict()

        for process in processes:
            
            memUsage.setdefault(process.name, 0)
            memUsage[process.name] += process.memoryUsageMB

        processes = [Process(name, memUsage[name]) for name in memUsage]
        return processes

class MemoryState:

    def __init__(self):
        
        processList = Process.getRunningProcesses()

        self.runningProcesses = len(processList)
        self.totalMemoryUsageMB = sum([process.memoryUsageMB for process in processList])

        hungriestProcess = max(processList, key=lambda process: process.memoryUsageMB)

        self.hungriestProcessName = hungriestProcess.name
        self.hungriestProcessMemoryUsageMB = hungriestProcess.memoryUsageMB

def getCurrentMemoryState() -> MemoryState:

    return MemoryState()
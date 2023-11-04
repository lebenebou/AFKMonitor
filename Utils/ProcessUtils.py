
from Utils import CmdUtils

class Process:

    def __init__(self, name: str, memoryUsageMB: float):

        self.name = name
        self.memoryUsageMB = round(memoryUsageMB, 2)

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

        commandOutput = CmdUtils.runCommand("tasklist /fo csv /nh").stdout
        lines = commandOutput.splitlines()

        processes = [Process.extractProcessFromLine(line) for line in lines]
        memUsage = dict()

        for process in processes:
            
            memUsage.setdefault(process.name, 0)
            memUsage[process.name] += process.memoryUsageMB

        processes = [Process(name, memUsage[name]) for name in memUsage]
        return processes

class MemoryState:

    def __init__(self, runningProcesses: int, totalMemoryUsageMB: float, hungriestProcessName: str, hungriestProcessMemoryUsageMB: float):
        
        self.runningProcesses = runningProcesses
        self.totalMemoryUsageMB = round(totalMemoryUsageMB, 2)
        self.hungriestProcessName = hungriestProcessName
        self.hungriestProcessMemoryUsageMB = round(hungriestProcessMemoryUsageMB, 2)

def getCurrentMemoryState() -> MemoryState:

    processes = Process.getRunningProcesses()
    
    totalMemoryUsageMB = sum([process.memoryUsageMB for process in processes])
    hungriestProcess = max(processes, key=lambda process: process.memoryUsageMB)

    return MemoryState(
        
        len(processes),
        totalMemoryUsageMB,
        hungriestProcess.name,
        hungriestProcess.memoryUsageMB
        )
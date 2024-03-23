
from Utils.CmdUtils import runCommand

class Process:

    def __init__(self, name: str, memoryUsageKB: float):

        self.name = name
        self.memoryUsageKB = memoryUsageKB

    def getMemoryUsageMB(self) -> float:
        return self.memoryUsageKB / 1000

def extractProcessFromLine(stdoutLine: str) -> Process:

    stdoutLine = stdoutLine.replace('"', '')

    fields = stdoutLine.split(",")

    name = fields[0]
    memUsageKbString = fields[-1].strip(" K").strip()
    
    if len(fields) > 5:
        memUsageKbString = fields[-2] + memUsageKbString

    memUsageKb = float(memUsageKbString)
    return Process(name, memUsageKb)

def getRunningProcesses() -> list[Process]:

    commandOutput = runCommand("tasklist /fo csv /nh").stdout

    processes = [extractProcessFromLine(line) for line in commandOutput.splitlines()]

    memUsage = dict()
    for process in processes:
        
        memUsage.setdefault(process.name, 0)
        memUsage[process.name] += process.memoryUsageKB

    processes = [Process(name, memUsage[name]) for name in memUsage]
    return processes

class MemoryState:

    def __init__(self):
        
        processList = getRunningProcesses()

        self.runningProcesses = len(processList)
        self.totalMemoryUsageMB = sum([process.getMemoryUsageMB() for process in processList])

        hungriestProcess = max(processList, key=lambda process: process.memoryUsageKB)

        self.hungriestProcessName = hungriestProcess.name
        self.hungriestProcessMemoryUsageMB = hungriestProcess.getMemoryUsageMB()

if __name__ == "__main__":

    currentMemoryState = MemoryState()

    print(f"Total running processes: {currentMemoryState.runningProcesses}")
    print(f"Total memory usage: {currentMemoryState.totalMemoryUsageMB} MB")
    print(f"Hungriest process: {currentMemoryState.hungriestProcessName} ({currentMemoryState.hungriestProcessMemoryUsageMB} MB)")
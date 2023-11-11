
import subprocess

def runCommand(command: str) -> subprocess.CompletedProcess:

    command = subprocess.run(command, capture_output=True, text=True)
    return command

def shutdown():
    runCommand("shutdown /s /t 0")
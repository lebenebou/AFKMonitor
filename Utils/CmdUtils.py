
import subprocess

def runCommand(command: str) -> subprocess.CompletedProcess:

    command = subprocess.run(command, capture_output=True, text=True)
    return command

def runPythonScriptInNewWindow(scriptPath: str):

    command = f"start cmd /c python {scriptPath}"
    subprocess.Popen(command, shell=True)
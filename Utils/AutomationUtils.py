
import time
import pyautogui
import subprocess

# Power Utils
def executePowerHotkey(key: str):

    pyautogui.hotkey("win", "x")
    pyautogui.press("u")
    pyautogui.press(key)

def sleep():
    executePowerHotkey("s")

def shutdown():
    executePowerHotkey("u")

def restart():
    executePowerHotkey("r")

def signOut():
    executePowerHotkey("i")

# App Utils
def minimizeAllApps():

    pyautogui.hotkey("win", "m")

def searchForAndOpenApp(appName: str):

    pyautogui.hotkey("win", "s")
    time.sleep(1)
    pyautogui.write(appName)
    time.sleep(1)
    pyautogui.press("enter")

def openApp(appName: str):

    subprocess.Popen(appName)

import time
import pyautogui
import subprocess

# Power Utils
def executePowerHotkey(key: str):

    pyautogui.hotkey("win", "x")
    pyautogui.press("u")
    pyautogui.press(key)

def shutdown():
    executePowerHotkey("u")
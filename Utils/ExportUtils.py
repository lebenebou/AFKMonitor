
import os
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.dirname(UTILS_DIR)
os.chdir(MAIN_DIR)

import pandas

from ComputerState import ComputerState

from Utils.TimeUtils import getCurrentDate

def getDailyCsvPath() -> str:

    currentDate = getCurrentDate()
    csvFileName = f"{currentDate}.csv"
    return os.path.join(MAIN_DIR, "Reports", csvFileName)

def batchExportToDailyCsv(states: list[ComputerState]):

    if len(states) == 0:
        return
    
    dailyCsvPath = getDailyCsvPath()

    if not os.path.isdir(os.path.join(MAIN_DIR, "Reports")):
        os.mkdir(os.path.join(MAIN_DIR, "Reports"))
    
    if not os.path.exists(dailyCsvPath):

        columnTitles = states[0].toDict().keys()
        columnTitles = pandas.DataFrame(columns=columnTitles)
        columnTitles.to_csv(dailyCsvPath, index=False, header=True)

    dataFrames = [state.toDataFrame() for state in states]
    combinedDataFrames = pandas.concat(dataFrames, ignore_index=True)
    combinedDataFrames.to_csv(dailyCsvPath, mode="a", index=False, header=False)
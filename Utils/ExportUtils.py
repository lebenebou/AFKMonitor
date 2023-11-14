
import os
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_REPO_DIR = os.path.dirname(UTILS_DIR)
os.chdir(MAIN_REPO_DIR)

import pandas
from ComputerState import ComputerState
from Utils.TimeUtils import getCurrentDate, epochToLocalDateAndTime

def statesToDataFrame(states: list[ComputerState]) -> pandas.DataFrame:

    dataFrames = [singleState.toDataFrame() for singleState in states]
    return pandas.concat(dataFrames, ignore_index=True)

def isCsvOpen(csvFilePath: str) -> bool:

    try:
        os.access(csvFilePath, os.W_OK)
        return False
    
    except PermissionError:
        return True

def exportToCsv(statesDataFrame: pandas.DataFrame, csvFilePath:str, includeDay: bool):
    
    if includeDay:

        statesDataFrame["localTime"] = statesDataFrame["time"].apply(epochToLocalDateAndTime)

    if not os.path.exists(csvFilePath):
        
        columnTitles = pandas.DataFrame(columns = statesDataFrame.columns)
        columnTitles.to_csv(csvFilePath, index=False, header=True)
        
    statesDataFrame.to_csv(csvFilePath, index=False, mode="a", header=False)

def exportStates(states: list[ComputerState]):

    if len(states) == 0:
        return
    
    reportsDir = os.path.join(MAIN_REPO_DIR, "Reports")

    if not os.path.isdir(reportsDir):
        os.mkdir(reportsDir)
    
    dailyCsvFilePath = os.path.join(reportsDir, f"{getCurrentDate()}.csv")
    fullReportCsvFilePath = os.path.join(reportsDir, "FullReport.csv")

    if isCsvOpen(dailyCsvFilePath) or isCsvOpen(fullReportCsvFilePath):
        raise PermissionError("One of the CSV files is open, unable to save")

    fullDataFrame = statesToDataFrame(states)
    exportToCsv(fullDataFrame, dailyCsvFilePath, includeDay=False)
    exportToCsv(fullDataFrame, fullReportCsvFilePath, includeDay=True)
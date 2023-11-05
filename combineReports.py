
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(CURRENT_DIR, "Reports")
os.chdir(REPORTS_DIR)

import pandas

def getDataFramePlusDate(csvFilePath: str) -> pandas.DataFrame:

    date = os.path.basename(csvFilePath).strip(".csv").replace("_", " ")
    dataFrame = pandas.read_csv(csvFilePath)
    dataFrame["localTime"] = dataFrame["localTime"].apply(lambda time: f"{date} {time}")

    return dataFrame

def getCombinedReports() -> pandas.DataFrame:

    reports = [file for file in os.listdir(REPORTS_DIR) if file.endswith(".csv") and not file.startswith("FullReport")]

    combinedDataFrame = pandas.concat([getDataFramePlusDate(report) for report in reports], ignore_index=True)
    combinedDataFrame.sort_values(by=["time"], inplace=True, ascending=False)

    return combinedDataFrame

if __name__ == "__main__":
    
    combinedDataFrame = getCombinedReports()

    try:
        combinedDataFrame.to_csv("FullReport.csv", index=False, header=True)

    except PermissionError:
        print("FullReport.csv is open, please close it and try again")
        exit(1)
        
    os.startfile("FullReport.csv")
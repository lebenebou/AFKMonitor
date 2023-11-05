
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)

import sys
sys.path.append("..")

from Utils.InternetUtils import isConnected

def runTests(trueInternetState: bool, testCount: int):

    for i in range(testCount):

        print(f"Running test {i+1}...", end="\r", flush=True)
        assert isConnected() == trueInternetState, f"isConnected() returned {not trueInternetState}"

    print(f"{testCount} tests passed." + " "*20, flush=True)

def testFalseNegatives(testCount: int):
    runTests(trueInternetState=True, testCount=testCount)

def testFalsePositives(testCount: int):
    runTests(trueInternetState=False, testCount=testCount)

if __name__=="__main__":

    testCount = 20
    
    input("\nMake sure you are connected to the internet and press enter to continue...")
    print(f"\nRunning {testCount} tests")

    testFalseNegatives(testCount)

    print("All tests passed. isConnected never returned False.")
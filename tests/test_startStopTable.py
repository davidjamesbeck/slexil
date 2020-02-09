# test_startStopTable.py
#----------------------------------------------------------------------------------------------------
import re
import sys
sys.path.append("..")

from audioExtractor import *
#----------------------------------------------------------------------------------------------------
def runTests():

    test_makestartStopTable()

def test_makestartStopTable():

    print("--- test_makestartStopTable")
    ea = AudioExtractor("../testData/inferno-threeLines/inferno-threeLines.wav",
                        "../testData/inferno-threeLines/inferno-threeLines.eaf",
                        "../testData/inferno-threeLines/audio")
    ea.extract()

if __name__ == '__main__':
    runTests()


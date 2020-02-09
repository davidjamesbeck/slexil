import re
import sys
sys.path.append("..")
from text import *
import importlib
import os
import pdb
from audioExtractor import AudioExtractor
#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
#----------------------------------------------------------------------------------------------------
def runTests(display=False):
    test_HowDaylightWasStolen(display)
    test_MonkeyAndThunder(display)
    test_prayer(display)
    test_aktzini(display)

#----------------------------------------------------------------------------------------------------
def test_HowDaylightWasStolen(display):

    print("--- test_HowDaylightWasStolen")
    audioFilename = "daylight_1_4.wav"
    elanXmlFilename="../testData/harryMosesDaylight/daylight_1_4.eaf"
    targetDirectory = "../testData/harryMosesDaylight/audio"
    soundFile = os.path.join(targetDirectory,audioFilename)
    projectDirectory="../testData/harryMosesDaylight"
    tierGuideFile="../testData/harryMosesDaylight/tierGuide.yaml"
    grammaticalTermsFile="../testData/harryMosesDaylight/grammaticalTerms.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)#,
# 				startStopTable=times)

# 	text.getTable(1)

    htmlText = text.toHTML()
    if(display):
       filename = "daylight.html"
       f = open(filename, "w")
       f.write(indent(htmlText))
       f.close()
       os.system("open %s" % filename)

#----------------------------------------------------------------------------------------------------
def test_MonkeyAndThunder(display):

    print("--- test_MonkeyAndThunder")
    audioFilename = "AYA1_MonkeyandThunder-32bit.wav"
    elanXmlFilename="../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    targetDirectory = "../testData/monkeyAndThunder/audio"
    soundFile = os.path.join(targetDirectory,audioFilename)
    projectDirectory="../testData/monkeyAndThunder"
    tierGuideFile="../testData/monkeyAndThunder/tierGuide.yaml"
    grammaticalTermsFile="../testData/monkeyAndThunder/grammaticalTerms.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)# ,
# 				startStopTable=times)

# 	text.getTable(1)

    htmlText = text.toHTML()
    if(display):
       filename = "monkeyAndThunder.html"
       f = open(filename, "w")
       f.write(indent(htmlText))
       f.close()
       os.system("open %s" % filename)


#----------------------------------------------------------------------------------------------------
def test_prayer(display):

    print("--- test_prayer")
    audioFilename = "SJQ-2009_Cruz.wav"
    elanXmlFilename="../testData/prayer/20150717_Prayer_community_one.eaf"
    targetDirectory = "../testData/prayer/audio"
    soundFile = os.path.join(targetDirectory,audioFilename)
    projectDirectory="../testData/prayer"
    tierGuideFile="../testData/prayer/tierGuide.yaml"
    grammaticalTermsFile="../testData/prayer/grammaticalTerms.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)# ,
# 				startStopTable=times)

# 	text.getTable(0)

    htmlText = text.toHTML(0)

    if(display):
       filename = "prayer.html"
       f = open(filename, "w")
       f.write(indent(htmlText))
       f.close()
       os.system("open %s" % filename)


#----------------------------------------------------------------------------------------------------
def test_aktzini(display):

    print("--- test_aktzini")

    text = Text("../testData/aktzini/18-06-03Aktzini-GA.eaf",
                "../testData/aktzini/audio",
				tierGuideFile='../testData/aktzini/tierGuide.yaml',
                projectDirectory='../testData/aktzini',
                grammaticalTermsFile=None,
                quiet=False)

# 	text.getTable(1)

    htmlText = text.toHTML()
    if(display):
       filename = "aktzini.html"
       f = open(filename, "w")
       f.write(indent(htmlText))
       f.close()
       os.system("open %s" % filename)


#----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    runTests()

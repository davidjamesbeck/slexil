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
    test_praying(display)
    test_aktzini(display)

#----------------------------------------------------------------------------------------------------
def test_HowDaylightWasStolen(display):

    print("--- test_HowDaylightWasStolen")
    audioFilename = "HMDL.wav"
    elanXmlFilename="../testData/HMDLsafe/HMDL.eaf"
    targetDirectory = "../testData/HMDLsafe/audio"
    soundFile = os.path.join(targetDirectory,audioFilename)
    projectDirectory="../testData/HMDLsafe"
    tierGuideFile="../testData/HMDLsafe/tierGuide.yaml"
    grammaticalTermsFile="../testData/HMDLsafe/grammaticalTerms.txt"
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
    audioFilename = "AYAMT-32bit.wav"
    elanXmlFilename="../testData/AYAMT/AYAMT.eaf"
    targetDirectory = "../testData/AYAMT/audio"
    soundFile = os.path.join(targetDirectory,audioFilename)
    projectDirectory="../testData/AYAMT"
    tierGuideFile="../testData/AYAMT/tierGuide.yaml"
    grammaticalTermsFile="../testData/AYAMT/grammaticalTerms.txt"
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
       filename = "AYAMT.html"
       f = open(filename, "w")
       f.write(indent(htmlText))
       f.close()
       os.system("open %s" % filename)


#----------------------------------------------------------------------------------------------------
def test_praying(display):

    print("--- test_praying")
    audioFilename = "SJQ-2009_Cruz.wav"
    elanXmlFilename="../testData/praying/praying.eaf"
    targetDirectory = "../testData/praying/audio"
    soundFile = os.path.join(targetDirectory,audioFilename)
    projectDirectory="../testData/praying"
    tierGuideFile="../testData/praying/tierGuide.yaml"
    grammaticalTermsFile="../testData/praying/grammaticalTerms.txt"
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
       filename = "praying.html"
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

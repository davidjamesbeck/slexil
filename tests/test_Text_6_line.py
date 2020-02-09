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
	test_Chatino_6_Line_from_webapp(display)

#----------------------------------------------------------------------------------------------------
def test_Chatino_6_Line_from_webapp(display):

	print("--- test_Chatino_6_Line_from_webappn")
	audioFilename = "20150717_Prayer_community_one.wav"
	elanXmlFilename="../testData/s/20150717_Prayer_community_one.eaf"
	targetDirectory = "../testData/s/audio"
	soundFile = os.path.join(targetDirectory,audioFilename)
	projectDirectory="../testData/s"
	tierGuideFile="../testData/s/tierGuide.yaml"
	grammaticalTermsFile="../testData/s/grammaticalTerms.txt"
	ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
	ae.determineStartAndEndTimes()
	times = ae.startStopTable	
	text = Text(elanXmlFilename,
				soundFile,
				grammaticalTermsFile=grammaticalTermsFile,
				tierGuideFile=tierGuideFile,
				projectDirectory=projectDirectory)# ,
# 				startStopTable=times)

	#text.getTable(1)
	display=False
	htmlText = text.toHTML()
	if(display):
	   filename = "6test.html"
	   f = open(filename, "w")
	   f.write(indent(htmlText))
	   f.close()
	   os.system("open %s" % filename)
	
#----------------------------------------------------------------------------------------------------
def test_HowDaylightWasStolen(display):

	print("--- test_HowDaylightWasStolen")
	
	text = Text("../testData/harryMosesDaylight/daylight_1_4.eaf",
				"../testData/harryMosesDaylight/audioPhrases",
				grammaticalTermsFile=None,
				tierGuideFile="../testData/harryMosesDaylight/tierGuide.yaml",
				projectDirectory="../testData/harryMosesDaylight")

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

	text = Text("../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf",
				"../testData/monkeyAndThunder/audioPhrases",
				grammaticalTermsFile="../testData/monkeyAndThunder/grammaticalTerms.txt")
	 
	text.getTable(1)

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

	text = Text("../testData/prayer/20150717_Prayer_community_one.eaf",
				"../testData/prayer/audioPhrases",
				grammaticalTermsFile=None,
				quiet=False)

	text.getTable(0)

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
				"../testData/aktzini/audioPhrases",
				grammaticalTermsFile=None,
				quiet=False)

	text.getTable(1)

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

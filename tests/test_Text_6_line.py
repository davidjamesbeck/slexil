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
	test_praying_6_Line_from_webapp(display)

#----------------------------------------------------------------------------------------------------
def test_praying_6_Line_from_webapp(display):

	print("--- test_praying_6_Line_from_webappn")
	audioFilename = "praying.wav"
	elanXmlFilename="../testData/s/praying.eaf"
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
	
	text = Text("../testData/HMDLsafe/HMDL.eaf",
				"../testData/HMDLsafe/audioPhrases",
				grammaticalTermsFile=None,
				tierGuideFile="../testData/HMDLsafe/tierGuide.yaml",
				projectDirectory="../testData/HMDLsafe")

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

	text = Text("../testData/AYAMT/AYAMT.eaf",
				"../testData/AYAMT/audioPhrases",
				grammaticalTermsFile="../testData/AYAMT/grammaticalTerms.txt")
	 
	text.getTable(1)

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

	text = Text("../testData/praying/praying.eaf",
				"../testData/praying/audioPhrases",
				grammaticalTermsFile=None,
				quiet=False)

	text.getTable(0)

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

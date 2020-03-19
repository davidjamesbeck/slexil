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

	test_constructor()
	test_toHTML(display)

def createText():
	audioFilename = "../testData/aktzini/18-06-03Aktzini-GA.wav"
	elanXmlFilename="../testData/aktzini/18-06-03Aktzini-GA.eaf"
	targetDirectory = "../testData/aktzini/audio"
	soundFile = os.path.join(targetDirectory,audioFilename)
	projectDirectory="../testData/aktzini"
	tierGuideFile="../testData/aktzini/tierGuide.yaml"
	grammaticalTermsFile="../testData/aktzini/grammaticalTerms.txt"
	ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
	ae.extract()
	ae.determineStartAndEndTimes()
	times = ae.startStopTable	
	text = Text(elanXmlFilename,
				audioFilename,
				grammaticalTermsFile=grammaticalTermsFile,
				tierGuideFile=tierGuideFile,
				projectDirectory=projectDirectory,
				quiet=False)
	return(text)

def test_constructor():

	print("--- test_constructor")
	text = createText()
	assert(text.validInputs())

def test_toHTML(display):

	print("--- test_toHTML")

	text = createText()
# 	text.getTable(0)

	htmlText = text.toHTML()
	filename = "../testData/aktzini/aktzini.html"
	f = open(filename, "w")
	f.write(indent(htmlText))
	f.close()

	if(display):
		os.system("open %s" % filename)

if __name__ == '__main__':
	runTests()

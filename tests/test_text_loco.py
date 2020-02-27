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
	audioFilename = "SJQ-2009_Cruz.wav"
	elanXmlFilename="../testData/loco/loco.eaf"
	targetDirectory = "../testData/loco/audio"
	soundFile = os.path.join(targetDirectory,audioFilename)
	projectDirectory="../testData/loco"
	tierGuideFile="../testData/loco/tierGuide.yaml"
	grammaticalTermsFile="../testData/loco/grammaticalTerms.txt"
	ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
	ae.determineStartAndEndTimes()
	times = ae.startStopTable	
	text = Text(elanXmlFilename,
				soundFile,
				grammaticalTermsFile=grammaticalTermsFile,
				tierGuideFile=tierGuideFile,
				projectDirectory=projectDirectory)# ,
# 				startStopTable=times)

	return(text)

def test_constructor():

	print("--- test_constructor")
	text = createText()
	assert(text.validInputs())
	tbl = text.getTierSummary()
	assert(tbl.shape == (4,3))
	assert(list(tbl['key']) == ['speech', 'translation', 'morpheme', 'morphemeGloss'])
	assert(list(tbl['value']) == ['Orthographic represntation', 'English translation', 'morpheme', 'gloss'])
	assert(list(tbl['count']) == [344, 344, 1857, 1857])

def test_traverseStructure():

	print("--- test_traverseStructure")
	text = createText()
	text.traverseStructure()

def exploreMapping():

	text = createText()
	tbl = text.getLineAsTable(0)


def test_toHTML(display):

	print("--- test_toHTML")

	text = createText()
	text.getLineAsTable(0)

	htmlText = text.toHTML()
	# filename = "../testData/loco/loco.html"
	# f = open(filename, "w")
	# f.write(indent(htmlText))
	# f.close()

	if(display):
		os.system("open %s" % filename)

if __name__ == '__main__':
	runTests()

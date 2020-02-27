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

def createText():
	audioFilename = "praying.wav"
	elanXmlFilename="../testData/praying_6Line/praying.eaf"
	targetDirectory = "../testData/praying_6Line/audio"
	soundFile = os.path.join(targetDirectory,audioFilename)
	projectDirectory="../testData/praying_6Line"
	tierGuideFile="../testData/praying_6Line/tierGuide.yaml"
	grammaticalTermsFile="../testData/praying_6Line/grammaticalTerms.txt"
	ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
	ae.determineStartAndEndTimes()
	times = ae.startStopTable

	text = Text(elanXmlFilename,
				soundFile,
				grammaticalTermsFile=grammaticalTermsFile,
				tierGuideFile=tierGuideFile,
				#startStopTable=times,
				projectDirectory=projectDirectory,
				quiet=True)

	return(text)

def runTests(display=False):

	test_constructor()
	test_toHTML(display)

def test_constructor():

	print("--- test_constructor")

	text = createText()
	assert(text.validInputs())
	tbl = text.getTierSummary()
	print(list(tbl['key']))
	assert(tbl.shape == (6,3))
	assert(list(tbl['key']) == ['speech', 'translation', 'morpheme', 'morphemeGloss','translation2','transcription2'])
	assert(list(tbl['value']) == ['SZC-Chatino', 'English Translation', 'Tokenization-cp', 'POS-cp','second translation','phonetic transcription'])
	assert(list(tbl['count']) == [9, 9, 111, 111, 9, 9])

def test_toHTML(display):

	print("--- test_toHTML")

	text = createText()
	tbl = text.getLineAsTable(0)

	htmlText = text.toHTML()
	# filename = "../testData/praying_6Line/praying6.html"
	# f = open(filename, "w")
	# f.write(indent(htmlText))
	# f.close()

	if(display):
		os.system("open %s" % filename)

if __name__ == '__main__':
	runTests()

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
	audioFilename = "inferno-threeLines.wav"
	elanXmlFilename="../testData/inferno-threeLines/inferno-threeLines.eaf"
	targetDirectory = "../testData/inferno-threeLines/audio"
	soundFile = os.path.join(targetDirectory,audioFilename)
	projectDirectory="../testData/inferno-threeLines"
	tierGuideFile="../testData/inferno-threeLines/tierGuide.yaml"
	grammaticalTermsFile="../testData/inferno-threeLines/grammaticalTerms.txt"
	ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
	ae.determineStartAndEndTimes()

	text = Text(elanXmlFilename,
				audioFilename,
				grammaticalTermsFile=grammaticalTermsFile,
				tierGuideFile=tierGuideFile,
				projectDirectory=projectDirectory,
				quiet=True)

	return(text)


def test_constructor():

	print("--- test_constructor")

	text = createText()
	assert(text.validInputs())
	tbl = text.getTierSummary()
	try:
		assert(tbl.shape == (3,3))
	except AssertionError as e:
		raise Exception(tbl.shape)
	# pdb.set_trace()
	try:
		assert(list(tbl['key']) == ['morpheme', 'morphemeGloss', 'speech'])
	except AssertionError as e:
		raise Exception(list(tbl['key']))
	try:
		assert(list(tbl['value']) == ['morphemes', 'morphemeGloss', 'italianSpeech'])
	except AssertionError as e:
		raise Exception(list(tbl['value']))
	try:
		assert(list(tbl['count']) == [3, 3, 3])
	except AssertionError as e:
		raise Exception(list(tbl['count']))

def test_toHTML(display=False):

	print("--- test_toHTML")

	text = createText()

	text.getLineAsTable(1)

	htmlText = text.toHTML()
	filename = "daylight.html"
	f = open(filename, "w")
	f.write(indent(htmlText))
	f.close()
	if(display):
	   os.system("open %s" % filename)

if __name__ == '__main__':
	runTests()

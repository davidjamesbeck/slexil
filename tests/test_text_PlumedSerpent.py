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

def runTests():

	test_constructor()
	test_toHTML(display=False)

def createText():
	audioFilename = "Chicahuaxtla Triqui - La serpiente emplumada 04-28-2016.wav"
	elanXmlFilename="../testData/plumedSerpent/TRS_Plumed_Serpent_Legend_05-15-2017.eaf"
	targetDirectory = "../testData/plumedSerpent/audioPhrases"
	soundFile = os.path.join(targetDirectory,audioFilename)
	ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
	ae.determineStartAndEndTimes()
	times = ae.startStopTable
	text = Text(elanXmlFilename,
				soundFile,
				grammaticalTermsFile="../testData/plumedSerpent/grammaticalTerms.txt",
				tierGuideFile="../testData/plumedSerpent/tierGuide.yaml",
				projectDirectory="../testData/plumedSerpent",
				#startStopTable=times,
				quiet=False)
	return(text)

def test_constructor():

	print("--- test_constructor")
	text = createText()
	assert(text.validInputs())
	tbl = text.getTierSummary()
	try:
		assert(tbl.shape == (5,3))
	except AssertionError as e:
		raise Exception(tbl.shape)
	try:
		assert(list(tbl['key']) == ['morpheme', 'morphemeGloss', 'speech', 'transcription2', 'translation'])
	except AssertionError as e:
		raise Exception(list(tbl['key']))
	try:
		assert(list(tbl['value']) == ['Tokenization-cp', 'Tokenization-Gloss-cp', 'TRS-Ortho', 'TRS Broad IPA', 'Free Translation'])
	except AssertionError as e:
		raise Exception(list(tbl['value']))
	try:
		assert(list(tbl['count']) == [15, 15, 15, 141, 141])
	except AssertionError as e:
		raise Exception(list(tbl['count']))

def test_toHTML(display):

	print("--- test_toHTML")
	text = createText()	

	tbl = text.getLineAsTable(0)
	try:
		assert(tbl.shape == (11, 14))
	except AssertionError as e:
		raise Exception(tbl.shape)

	htmlText = text.toHTML()
	filename = "plumedSerpent.html"
	f = open(filename, "w")
	f.write(indent(htmlText))
	f.close()

	if(display):
		os.system("open %s" % filename)

if __name__ == '__main__':
	runTests()

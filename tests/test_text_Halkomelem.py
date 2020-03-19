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

	test_AMCuervo(display)

def test_AMCuervo(display):
	try:
		assert (os.path.exists("../testTextPyData/Cuervo/audio"))
	except AssertionError:
		os.mkdir("../testTextPyData/Cuervo/audio")

	audioFilename = "../testData/Cargos.ogg"
	elanXmlFilename="newcuervo.eaf"
	targetDirectory = "../testTextPyData/Cuervo/audio"
	soundFile = os.path.join(targetDirectory,"Cargos.ogg")
	projectDirectory="../testTextPyData/Cuervo"
	tierGuideFile="../testTextPyData/Cuervo/tierGuide.yaml"
	elanFile = os.path.join(projectDirectory,elanXmlFilename)
	ae = AudioExtractor(audioFilename, elanFile, targetDirectory)
	ae.determineStartAndEndTimes()
	ae.extract()
	times = ae.startStopTable
	text = Text(elanFile,
				audioFilename,
				grammaticalTermsFile=None,
				tierGuideFile=tierGuideFile,
				projectDirectory=projectDirectory)

	print("--- test_toHTML")

	text.getLineAsTable(0)

	htmlText = text.toHTML()
	# filename = "../testTextPyData/Cuervo/CuervoNew.html"
	# f = open(filename, "w")
	# f.write(indent(htmlText))
	# f.close()

	if(display):
		os.system("open %s" % filename)


if __name__ == '__main__':
	runTests()

import re
import sys

sys.path.append("..")
from text import *
import os
import pdb
from ijalLine import *
from audioExtractor import AudioExtractor
from xml.etree import ElementTree as etree
from ijalLine import IjalLine as Line

# ----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)


# ----------------------------------------------------------------------------------------------------
def runTests(display=False):
    test_Aktzini_plus_one(True)

# ----------------------------------------------------------------------------------------------------
def test_Aktzini_plus_one(display):
    '''tests .eaf file with empty and missing line or translation annotations'''

    print("--- test_Aktzini_plus_one")

    audioFilename = "../testData/test_alignable/18-06-03Aktzini-GA.wav"
    elanXmlFilename = "../testData/test_alignable/Aktzini_plus_one.eaf"
    targetDirectory = "../testData/test_alignable/audio"
    projectDirectory = "../testData/test_alignable"
    tierGuideFile = "../testData/test_alignable/tierGuide.yaml"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()

    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile=None,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    htmlText = text.toHTML()
    if (display):
        filename = "../testData/test_alignable/Aktzini_plus_one.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)

# ----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    runTests()

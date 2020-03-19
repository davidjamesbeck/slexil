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
    learn_TierStructure()
    test_GhostWagon_build(display)

# ----------------------------------------------------------------------------------------------------
def learn_TierStructure():
    filename = "../testTextPyData/GhostInWagon/GhostInWagon.eaf"
    xmlDoc = etree.parse(filename)
    x = Line(xmlDoc, lineNumber=0, tierGuide=None, grammaticalTerms=[])
    print(x.tblRaw["TIER_ID"].tolist())


# ----------------------------------------------------------------------------------------------------
def test_GhostWagon_build(display):
    '''tests .eaf file with empty and missing line or translation annotations'''

    print("--- test_GhostWagon")

    audioFilename = "../testTextPyData/GhostInWagon/GhostInWagon.ogg"
    elanXmlFilename = "../testTextPyData/GhostInWagon/GhostInWagon.eaf"
    targetDirectory = "../testTextPyData/GhostInWagon/audio"
    soundFile = os.path.join(targetDirectory, "GhostInWagon.ogg")
    projectDirectory = "../testTextPyData/GhostInWagon"
    tierGuideFile = "../testTextPyData/GhostInWagon/tierGuide.yaml"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    times = ae.startStopTable

    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile=None,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    htmlText = text.toHTML()
    if (display):
        filename = "../testTextPyData/GhostInWagon/GhostInWagon.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)

# ----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    runTests()

import re
import sys

sys.path.append("..")
from text import *
import importlib
import os
import pdb
from audioExtractor import AudioExtractor

# ----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)


# ----------------------------------------------------------------------------------------------------
def runTests(display=False):
    test_wav(display)
    test_ogg(display)
    test_mp3(display)

# ----------------------------------------------------------------------------------------------------
def test_wav(display):

    print("--- test_wav")
    audioFilename = "inferno-threeLines.wav"
    elanXmlFilename = "../testData/inferno-threeLines/inferno-threeLines.eaf"
    targetDirectory = "../testData/inferno-threeLines/audio"
    projectDirectory = "../testData/inferno-threeLines"
    soundFile = os.path.join(projectDirectory, audioFilename)
    print(soundFile)
    tierGuideFile = "../testData/inferno-threeLines/tierGuide.yaml"
    grammaticalTermsFile = "../testData/inferno-threeLines/grammaticalTerms.txt"
    ae = AudioExtractor(soundFile, elanXmlFilename, targetDirectory)
    ae.validInputs()
    ae.extract(False)
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    htmlText = text.toHTML()
    if (display):
        filename = "../testData/inferno-threeLines/inferno-threeLineswav.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)

# ----------------------------------------------------------------------------------------------------
def test_mp3(display):

    print("--- test_mp3")
    audioFilename = "inferno-threeLines.mp3"
    elanXmlFilename = "../testData/inferno-threeLines/inferno-threeLines.eaf"
    targetDirectory = "../testData/inferno-threeLines/audio"
    projectDirectory = "../testData/inferno-threeLines"
    soundFile = os.path.join(projectDirectory, audioFilename)
    print(soundFile)
    tierGuideFile = "../testData/inferno-threeLines/tierGuide.yaml"
    grammaticalTermsFile = "../testData/inferno-threeLines/grammaticalTerms.txt"
    ae = AudioExtractor(soundFile, elanXmlFilename, targetDirectory)
    ae.validInputs()
    try:
        ae.extract(False)
    except RuntimeError:
        print('mp3 file format not supported')
        pass
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    htmlText = text.toHTML()
    if (display):
        filename = "../testData/inferno-threeLines/inferno-threeLinesmp3.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)

# ----------------------------------------------------------------------------------------------------
def test_ogg(display):

    print("--- test_ogg")
    audioFilename = "inferno-threeLines.ogg"
    elanXmlFilename = "../testData/inferno-threeLines/inferno-threeLines.eaf"
    targetDirectory = "../testData/inferno-threeLines/audio"
    projectDirectory = "../testData/inferno-threeLines"
    soundFile = os.path.join(projectDirectory, audioFilename)
    print(soundFile)
    tierGuideFile = "../testData/inferno-threeLines/tierGuide.yaml"
    grammaticalTermsFile = "../testData/inferno-threeLines/grammaticalTerms.txt"
    ae = AudioExtractor(soundFile, elanXmlFilename, targetDirectory)
    ae.validInputs()
    ae.extract(False)
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    htmlText = text.toHTML()
    if (display):
        filename = "../testData/inferno-threeLines/inferno-threeLinesogg.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)

# ----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    runTests()

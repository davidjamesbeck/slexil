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
import yaml

# ----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 10)

# ----------------------------------------------------------------------------------------------------
def runTests(display=False):
    test_Aktzini_plus_one(False)
    test_HMDL_TimeCodes()
    test_aktzini_TimeCodes()
    test_Ghost_TimeCodes()
    test_inferno_TimeCodes()
    test_Jagpossum_TimeCodes()
    test_inferno_plus_TimeCodes()
    test_inferno_plus_extraction()
    # test_Lazy_extraction()
    
# ----------------------------------------------------------------------------------------------------
def test_Lazy_extraction():
    elanXmlFilename = "../testTextPyData/Lazybones/Lazybones.eaf"
    targetDirectory = "../testTextPyData/Lazybones/audio"
    projectDirectory = "../testTextPyData/Lazybones"
    tierGuideFile = "../testTextPyData/Lazybones/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Lazybones/abbreviations.txt"
    audioFilename ="/Users/David/OpenSource/github/OldSlexilTestData/TEX_Lazy/4_TEX_TheLazyWoman.wav"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.extract()
    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)


# ----------------------------------------------------------------------------------------------------
def test_inferno_plus_extraction():
    print("--- test_inferno_plus_extraction")

    elanXmlFilename = "../testData/test_alignable/inferno-threeLines_plus_one.eaf"
    audioFilename = "../testData/test_alignable/inferno-threeLines.wav"
    targetDirectory = "../testData/test_alignable/audio"
    projectDirectory = "../testData/test_alignable"
    tierGuideFile = "../testData/test_alignable/tierGuideInferno.yaml"
    grammaticalTermsFile = "../testData/test_alignable/grammaticalTerms.txt"
    try:
        fileList = os.listdir(targetDirectory)
    except FileNotFoundError:
        os.mkdir(targetDirectory)
        fileList = []

    for f in fileList:
        target = os.path.join(targetDirectory,f)
        os.remove(target)
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.safe_load(f)

    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    htmlText = text.toHTML()

    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert(len(fileList) == 4)
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 4" %len(fileList))
        raise Exception(len(fileList)) from e

    display = False
    if (display):
        filename = "../testData/test_alignable/inferno-threeLines_plus.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)

# ----------------------------------------------------------------------------------------------------
def test_inferno_plus_TimeCodes():
    print("--- test_inferno_plus_TimeCodes")

    filename = "../testData/test_alignable/inferno-threeLines_plus_one.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testTextPyData/inferno/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 1, tierGuide)
    x3.parse()
    tbl = x3.getTable()
    startTime = x3.getStartTime()
    endTime = x3.getEndTime()
    print(startTime,endTime)

# ----------------------------------------------------------------------------------------------------
def test_HMDL_TimeCodes():
    print("--- test_HMDL_TimeCodes")

    filename = "../testData/HMDLsafe/HMDL.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testData/HMDLsafe/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 1, tierGuide)
    x3.parse()
    tbl = x3.getTable()
    startTime = x3.getStartTime()
    endTime = x3.getEndTime()
    print(startTime,endTime)

# ----------------------------------------------------------------------------------------------------
def test_aktzini_TimeCodes():
    print("--- test_aktzini_TimeCodes")

    filename = "../testData/aktzini/18-06-03Aktzini-GA.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testData/aktzini/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 1, tierGuide)
    x3.parse()
    tbl = x3.getTable()
    startTime = x3.getStartTime()
    endTime = x3.getEndTime()
    print(startTime,endTime)

# ----------------------------------------------------------------------------------------------------
def test_Ghost_TimeCodes():
    print("--- test_Ghost_TimeCodes")

    filename = "../testTextPyData/GhostInWagon/GhostInWagon.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testTextPyData/GhostInWagon/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 1, tierGuide)
    x3.parse()
    tbl = x3.getTable()
    startTime = x3.getStartTime()
    endTime = x3.getEndTime()
    print(startTime,endTime)

# ----------------------------------------------------------------------------------------------------
def test_inferno_TimeCodes():
    print("--- test_inferno_TimeCodes")

    filename = "../testTextPyData/inferno/inferno-threeLines.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testTextPyData/inferno/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 1, tierGuide)
    x3.parse()
    tbl = x3.getTable()
    startTime = x3.getStartTime()
    endTime = x3.getEndTime()
    print(startTime,endTime)

# ----------------------------------------------------------------------------------------------------
def test_Jagpossum_TimeCodes():
    print("--- test_Jagpossum_TimeCodes")

    filename = "../testTextPyData/Jagpossum/Jagpossum.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testTextPyData/Jagpossum/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 1, tierGuide)
    x3.parse()
    tbl = x3.getTable()
    startTime = x3.getStartTime()
    endTime = x3.getEndTime()
    print(startTime,endTime)
    # assert (startTime == 8850.0)
    # assert (endTime == 10570.0)

# ----------------------------------------------------------------------------------------------------
def test_Aktzini_plus_one(display):
    '''tests .eaf file with empty and missing line or translation annotations'''

    print("--- test_Aktzini_plus_one")

    audioFilename = "../testData/test_alignable/18-06-03Aktzini-GA.wav"
    elanXmlFilename = "../testData/test_alignable/Aktzini_plus_one.eaf"
    targetDirectory = "../testData/test_alignable/audio"
    projectDirectory = "../testData/test_alignable"
    tierGuideFile = "../testData/test_alignable/tierGuide.yaml"
    try:
        fileList = os.listdir(targetDirectory)
    except FileNotFoundError:
        os.mkdir(targetDirectory)
        fileList = []

    for f in fileList:
        target = os.path.join(targetDirectory,f)
        os.remove(target)

    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile=None,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    htmlText = text.toHTML()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]

    try:
        assert (len(fileList) == 17)
        print("There are %d audiophrases for 16 lines and the full sound file" % len(fileList))
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 17" % len(fileList))
        raise Exception(len(fileList)) from e

    if (display):
        filename = "../testData/test_alignable/Aktzini_plus_one.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)

# ----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    runTests()

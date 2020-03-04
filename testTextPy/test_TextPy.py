import re
import sys

sys.path.append("..")
from text import *
import importlib
import os
import pdb
from ijalLine import *
from errors import *
import logging
from audioExtractor import AudioExtractor
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)


# ----------------------------------------------------------------------------------------------------
def runTests(display=False):
    test_AYAFW(display)
    test_Merchant(display)
    test_Jagpossum(display)
    test_Sanchizo(display)
    test_Caterpillar(display)
    test_Lazybones(display)
    test_Zelf(display)
    test_Prayer(display)
    test_Inferno(display)
    test_aym(display)
    test_Cuervo(display)
    test_Cuervo_errors(display)

# ----------------------------------------------------------------------------------------------------
def test_Cuervo_errors(display):
    '''tests .eaf file with empty and missing line or translation annotations'''

    print("--- test_Cuervo_with_errors")

    audioFilename = "../testData/Cargos.wav"
    elanXmlFilename = "../testTextPyData/Cuervo/newcuervo_all_errors.eaf"
    targetDirectory = "../testTextPyData/Cuervo/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.wav")
    projectDirectory = "../testTextPyData/Cuervo"
    tierGuideFile = "../testTextPyData/Cuervo/tierGuide.yaml"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable

    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=None,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    htmlText = text.toHTML()
    if (display):
        filename = "../testTextPyData/Cuervo/badraven.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)


# ----------------------------------------------------------------------------------------------------
def test_Cuervo(display):
    print("--- test_Cuervo")

    audioFilename = "../testData/Cargos.wav"
    elanXmlFilename = "../testTextPyData/Cuervo/newcuervo.eaf"
    targetDirectory = "../testTextPyData/Cuervo/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.wav")
    projectDirectory = "../testTextPyData/Cuervo"
    tierGuideFile = "../testTextPyData/Cuervo/tierGuide.yaml"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=None,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    htmlText = text.toHTML()
    if (display):
        filename = "../testTextPyData/Cuervo/newcuervo.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)

# ----------------------------------------------------------------------------------------------------
def test_aym(display):
    print("--- test_aym")

    audioFilename = "../testData/Cargos.wav"
    elanXmlFilename = "../testTextPyData/aym/aym-final.eaf"
    targetDirectory = "../testTextPyData/aym/Audio"
    soundFile = os.path.join(targetDirectory, "Cargos.wav")
    projectDirectory = "../testTextPyData/aym"
    tierGuideFile = "../testTextPyData/aym/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/aym/List of abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # startStopTable=times)

    # IjalLine.getTable(1)

    htmlText = text.toHTML()
    if (display):
        filename = "../testTextPyData/aym/aym.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)


# ----------------------------------------------------------------------------------------------------
def test_Inferno_numbering(display):
    print("--- test_Inferno_numbering")

    audioFilename = "inferno-threeLines.wav"
    elanXmlFilename = "../explorations/playAudioInSequence/Inferno/inferno-threeLines.eaf"
    targetDirectory = "../explorations/playAudioInSequence/Inferno/Audio"
    soundFile = os.path.join(targetDirectory, audioFilename)
    projectDirectory = "../explorations/playAudioInSequence/Inferno"
    tierGuideFile = "../explorations/playAudioInSequence/Inferno/tierGuide.yaml"
    grammaticalTermsFile = "../explorations/playAudioInSequence/Inferno/abbreviations.txt"
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    # IjalLine.getTable(1)

    htmlText = text.toHTML()

    soup = BeautifulSoup(htmlText, 'html.parser')
    lines = soup.find_all("div", {"class": "line-wrapper"})
    for line in lines:
        id = line.get('id')
        textLineNumber = line.find("div", {"class": "line-sidebar"}).text[:-2]
        audioTag = line.find("source")
        audioFile = audioTag.get('src')
        fileID = audioFile[7:-5]
        print(id, textLineNumber, fileID)
        assert (id == textLineNumber == fileID)

    if (display):
        filename = "../explorations/playAudioInSequence/Inferno/inferno-threeLines.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)


# ----------------------------------------------------------------------------------------------------
def test_aym_numbering(display):
    print("--- test_aym_numbering")

    audioFilename = "../testData/Cargos.wav"
    elanXmlFilename = "../testTextPyData/aym/aym-final.eaf"
    targetDirectory = "../testTextPyData/aym/Audio"
    soundFile = os.path.join(targetDirectory, "Cargos.wav")
    projectDirectory = "../testTextPyData/aym"
    tierGuideFile = "../testTextPyData/aym/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/aym/List of abbreviations.txt"
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    # IjalLine.getTable(1)

    htmlText = text.toHTML()

    soup = BeautifulSoup(htmlText, 'html.parser')
    lines = soup.find_all("div", {"class": "line-wrapper"})
    for line in lines:
        id = line.get('id')
        textLineNumber = line.find("div", {"class": "line-sidebar"}).text[:-2]
        audioTag = line.find("source")
        audioFile = audioTag.get('src')
        fileID = audioFile[7:-4]
        assert (id == textLineNumber == fileID)

    if (display):
        filename = "../testTextPyData/aym/aym.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)


# ----------------------------------------------------------------------------------------------------
def test_Inferno(display):
    print("--- test_Inferno")

    audioFilename = "inferno-threeLines.wav"
    elanXmlFilename = "../explorations/playAudioInSequence/Inferno/inferno-threeLines.eaf"
    targetDirectory = "../explorations/playAudioInSequence/Inferno/Audio"
    soundFile = os.path.join(targetDirectory, audioFilename)
    projectDirectory = "../explorations/playAudioInSequence/Inferno"
    tierGuideFile = "../explorations/playAudioInSequence/Inferno/tierGuide.yaml"
    grammaticalTermsFile = "../explorations/playAudioInSequence/Inferno/abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # 				startStopTable=times)

    # IjalLine.getTable(1)

    htmlText = text.toHTML()
    if (display):
        filename = "../explorations/playAudioInSequence/Inferno/inferno-threeLines.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)

# ----------------------------------------------------------------------------------------------------
def test_AYAFW(display):
    print("--- test_AYAFW")
    audioFilename = "../testData/Cargos.wav"
    elanXmlFilename = "../testTextPyData/AYAFW/AYAFW.eaf"
    targetDirectory = "../testTextPyData/AYAFW/Audio"
    soundFile = os.path.join(targetDirectory, "Cargos.wav")
    projectDirectory = "../testTextPyData/AYAFW"
    tierGuideFile = "../testTextPyData/AYAFW/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/AYAFW/abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # 				startStopTable=times)

    # IjalLine.getTable(1)

    htmlText = text.toHTML()
    if (display):
        filename = "../testTextPyData/AYAFW/test_AYAFW.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)


# ----------------------------------------------------------------------------------------------------
def test_Merchant(display):
    print("--- test_Merchant")
    audioFilename = "../testData/Cargos.wav"
    elanXmlFilename = "../testTextPyData/JITZ/JITZ.eaf"
    targetDirectory = "../testTextPyData/JITZ/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.wav")
    projectDirectory = "../testTextPyData/JITZ"
    tierGuideFile = "../testTextPyData/JITZ/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/JITZ/grammaticalTerms.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # 				startStopTable=times)

    # IjalLine.getTable(1)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "test_Merchant.html"
            f = open(filename, "w")
            f.write(indent(htmlText))
            f.close()
            os.system("open %s" % filename)
    except TooManyMorphsError as e:
        print(
            "EAF error: There are more morphs (%d) than glosses (%d) in line %s." % (e.morphs, e.glosses, e.lineNumber))
    except TooManyGlossesError as e:
        print(
            "EAF error: There are more glosses (%d) than morphs (%d) in line %s." % (e.glosses, e.morphs, e.lineNumber))
    except EmptyTiersError as e:
        print("EAF error: There are empty tiers or incomplete glosses after line %s" % e.lineNumber)


# ----------------------------------------------------------------------------------------------------
def test_Jagpossum(display):
    print("--- test_Jagpossum")
    audioFilename = "../testData/Cargos.wav"
    elanXmlFilename = "../testTextPyData/Jagpossum/Jagpossum.eaf"
    targetDirectory = "../testTextPyData/Jagpossum/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.wav")
    projectDirectory = "../testTextPyData/Jagpossum"
    tierGuideFile = "../testTextPyData/Jagpossum/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Jagpossum/abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    # IjalLine.getTable(1)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "test_Jagpossum.html"
            f = open(filename, "w")
            f.write(indent(htmlText))
            f.close()
            os.system("open %s" % filename)
    except TooManyMorphsError as e:
        print(
            "EAF error: There are more morphs (%d) than glosses (%d) in line %s." % (e.morphs, e.glosses, e.lineNumber))
    except TooManyGlossesError as e:
        print(
            "EAF error: There are more glosses (%d) than morphs (%d) in line %s." % (e.glosses, e.morphs, e.lineNumber))
    except EmptyTiersError as e:
        print("EAF error: There are empty tiers or incomplete glosses after line %s" % e.lineNumber)


# ----------------------------------------------------------------------------------------------------
def test_Sanchizo(display):
    print("--- test_Sanchizo")
    audioFilename = "../testData/Cargos.wav"
    elanXmlFilename = "../testTextPyData/Sanchizo/Sanchizo.eaf"
    targetDirectory = "../testTextPyData/Sanchizo/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.wav")
    projectDirectory = "../testTextPyData/Sanchizo"
    tierGuideFile = "../testTextPyData/Sanchizo/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Sanchizo/abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # 				startStopTable=times)

    # IjalLine.getTable(1)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "test_Sanchizo.html"
            f = open(filename, "w")
            f.write(indent(htmlText))
            f.close()
            os.system("open %s" % filename)
    except TooManyMorphsError as e:
        print(
            "EAF error: There are more morphs (%d) than glosses (%d) in line %s." % (e.morphs, e.glosses, e.lineNumber))
    except TooManyGlossesError as e:
        print(
            "EAF error: There are more glosses (%d) than morphs (%d) in line %s." % (e.glosses, e.morphs, e.lineNumber))
    except EmptyTiersError as e:
        print("EAF error: There are empty tiers or incomplete glosses after line %s" % e.lineNumber)


# ----------------------------------------------------------------------------------------------------
def test_Caterpillar(display):
    print("--- test_Caterpillar")
    audioFilename = "../testData/Cargos.wav"
    elanXmlFilename = "../testTextPyData/Caterpillar/Caterpillar.eaf"
    targetDirectory = "../testTextPyData/Caterpillar/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.wav")
    projectDirectory = "../testTextPyData/Caterpillar"
    tierGuideFile = "../testTextPyData/Caterpillar/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Caterpillar/abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # 				startStopTable=times)

    # IjalLine.getTable(1)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "test_Caterpillar.html"
            f = open(filename, "w")
            f.write(indent(htmlText))
            f.close()
            os.system("open %s" % filename)
    except TooManyMorphsError as e:
        print(
            "EAF error: There are more morphs (%d) than glosses (%d) in line %s." % (e.morphs, e.glosses, e.lineNumber))
    except TooManyGlossesError as e:
        print(
            "EAF error: There are more glosses (%d) than morphs (%d) in line %s." % (e.glosses, e.morphs, e.lineNumber))
    except EmptyTiersError as e:
        print("EAF error: There are empty tiers or incomplete glosses after line %s" % e.lineNumber)


# ----------------------------------------------------------------------------------------------------
def test_Lazybones(display):
    print("--- test_Lazybones")

    audioFilename = "../testData/Cargos.wav"
    elanXmlFilename = "../testTextPyData/Lazybones/Lazybones.eaf"
    targetDirectory = "../testTextPyData/Lazybones/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.wav")
    projectDirectory = "../testTextPyData/Lazybones"
    tierGuideFile = "../testTextPyData/Lazybones/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Lazybones/abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # 				startStopTable=times)

    # IjalLine.getTable(1)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "test_Lazybones.html"
            f = open(filename, "w")
            f.write(indent(htmlText))
            f.close()
            os.system("open %s" % filename)
    except TooManyMorphsError as e:
        print(
            "EAF error: There are more morphs (%d) than glosses (%d) in line %s." % (e.morphs, e.glosses, e.lineNumber))
    except TooManyGlossesError as e:
        print(
            "EAF error: There are more glosses (%d) than morphs (%d) in line %s." % (e.glosses, e.morphs, e.lineNumber))
    except EmptyTiersError as e:
        print("EAF error: There are empty tiers or incomplete glosses after line %s" % e.lineNumber)


# ----------------------------------------------------------------------------------------------------
def test_Zelf(display):
    print("--- test_Zelf")
    audioFilename = "../testData/Cargos.wav"
    elanXmlFilename = "../testTextPyData/Zelfmar/Zelfmar.eaf"
    targetDirectory = "../testTextPyData/Zelfmar/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.wav")
    projectDirectory = "../testTextPyData/Zelfmar"
    tierGuideFile = "../testTextPyData/Zelfmar/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Zelfmar/abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # 				startStopTable=times)

    # IjalLine.getTable(1)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "test_Zelf.html"
            f = open(filename, "w")
            f.write(indent(htmlText))
            f.close()
            os.system("open %s" % filename)
    except TooManyMorphsError as e:
        print(
            "EAF error: There are more morphs (%d) than glosses (%d) in line %s." % (e.morphs, e.glosses, e.lineNumber))
    except TooManyGlossesError as e:
        print(
            "EAF error: There are more glosses (%d) than morphs (%d) in line %s." % (e.glosses, e.morphs, e.lineNumber))
    except EmptyTiersError as e:
        print("EAF error: There are empty tiers or incomplete glosses after line %s" % e.lineNumber)


# ----------------------------------------------------------------------------------------------------
def test_Prayer(display):
    print("--- test_Prayer")
    audioFilename = "../testData/Cargos.wav"
    elanXmlFilename = "../testTextPyData/Prayer_superscript/praying.eaf"
    targetDirectory = "../testTextPyData/Prayer_superscript/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.wav")
    projectDirectory = "../testTextPyData/Prayer_superscript"
    tierGuideFile = "../testTextPyData/Prayer_superscript/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Prayer_superscript/grammaticalTerms.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    times = ae.startStopTable
    text = Text(elanXmlFilename,
                soundFile,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # 				startStopTable=times)

    # IjalLine.getTable(1)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "test_Prayer.html"
            f = open(filename, "w")
            f.write(indent(htmlText))
            f.close()
            os.system("open %s" % filename)
    except TooManyMorphsError as e:
        print(
            "EAF error: There are more morphs (%d) than glosses (%d) in line %s." % (e.morphs, e.glosses, e.lineNumber))
    except TooManyGlossesError as e:
        print(
            "EAF error: There are more glosses (%d) than morphs (%d) in line %s." % (e.glosses, e.morphs, e.lineNumber))
    except EmptyTiersError as e:
        print("EAF error: There are empty tiers or incomplete glosses after line %s" % e.lineNumber)


# ----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    runTests()

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
def runTests(display=False,extract=False):
    if os.path.exists("../testTextPyData/Cargos.wav"):
        print("testing with .wav")
        audioFilename = "../testTextPyData/Cargos.wav"
    else:
        print("testing with .ogg")
        audioFilename = "../testData/Cargos.ogg"
    test_AYAFW(display,audioFilename,extract)
    test_Merchant(display,audioFilename,extract)
    test_Jagpossum(display,audioFilename,extract)
    test_Sanchizo(display,audioFilename,extract)
    test_Caterpillar(display,audioFilename,extract)
    test_Lazybones(display,audioFilename,extract)
    test_Zelf(display,audioFilename,extract)
    test_Prayer(display,audioFilename,extract)
    test_Inferno(display,audioFilename,extract)
    test_aym(display,audioFilename,extract)
    test_Cuervo(display,audioFilename,extract)
    test_Cuervo_errors(display,audioFilename,extract)
    # test_GhostWagon(display,extract) # this file bizarre, all tiers of type alignable, prob not worth handling
    test_aktzini(display,extract)

# ----------------------------------------------------------------------------------------------------
def test_aktzini(display,extract):
    '''tests .eaf file with empty and missing line or translation annotations'''

    print("--- test_aktzini")

    audioFilename = "../testData/aktzini/18-06-03Aktzini-GA.wav"
    elanXmlFilename = "../testData/aktzini/18-06-03Aktzini-GA.eaf"
    targetDirectory = "../testData/aktzini/audio"
    projectDirectory = "../testData/aktzini"
    tierGuideFile = "../testData/aktzini/tierGuide.yaml"
    grammaticalTermsFile = "../testData/aktzini/grammaticalTerms.txt"
    # ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    # if extract:
    #     ae.extract()
    # times = ae.startStopTable

    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    htmlText = text.toHTML()
    if (display):
        filename = "../testData/aktzini/Aktzini-GA.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)


# ----------------------------------------------------------------------------------------------------
def test_GhostWagon(display,extract):
    '''tests .eaf file with empty and missing line or translation annotations'''

    print("--- test_GhostWagon")

    audioFilename = "../testTextPyData/GhostInWagon/GhostInWagon.ogg"
    elanXmlFilename = "../testTextPyData/GhostInWagon/GhostInWagon_original.eaf"
    targetDirectory = "../testTextPyData/GhostInWagon/audio"
    soundFile = os.path.join(targetDirectory, "GhostInWagon.ogg")
    projectDirectory = "../testTextPyData/GhostInWagon"
    tierGuideFile = "../testTextPyData/Cuervo/tierGuide.yaml"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    if extract:
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
def test_Cuervo_errors(display,audioFilename,extract):
    '''tests .eaf file with empty and missing line or translation annotations'''

    print("--- test_Cuervo_with_errors")

    # audioFilename = "../testData/Cargos.ogg"
    elanXmlFilename = "../testTextPyData/Cuervo/newcuervo_all_errors.eaf"
    targetDirectory = "../testTextPyData/Cuervo/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.ogg")
    projectDirectory = "../testTextPyData/Cuervo"
    tierGuideFile = "../testTextPyData/Cuervo/tierGuide.yaml"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    if extract:
        ae.extract()
    times = ae.startStopTable

    text = Text(elanXmlFilename,
                audioFilename,
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
def test_Cuervo(display,audioFilename,extract):
    print("--- test_Cuervo")

    # audioFilename = "../testData/Cargos.ogg"
    elanXmlFilename = "../testTextPyData/Cuervo/newcuervo.eaf"
    targetDirectory = "../testTextPyData/Cuervo/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.ogg")
    projectDirectory = "../testTextPyData/Cuervo"
    tierGuideFile = "../testTextPyData/Cuervo/tierGuide.yaml"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    if extract:
        ae.extract()
    text = Text(elanXmlFilename,
                audioFilename,
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
def test_aym(display,audioFilename,extract):
    print("--- test_aym")

    # audioFilename = "../testData/Cargos.ogg"
    elanXmlFilename = "../testTextPyData/aym/aym-final.eaf"
    targetDirectory = "../testTextPyData/aym/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.ogg")
    projectDirectory = "../testTextPyData/aym"
    tierGuideFile = "../testTextPyData/aym/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/aym/List of abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract(True)
    text = Text(elanXmlFilename,
                audioFilename,
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
def test_Inferno_numbering(display,audioFilename,extract):
    print("--- test_Inferno_numbering")

    # audioFilename = "inferno-threeLines.wav"
    elanXmlFilename = "../explorations/playAudioInSequence/Inferno/inferno-threeLines.eaf"
    targetDirectory = "../explorations/playAudioInSequence/Inferno/Audio"
    soundFile = os.path.join(targetDirectory, audioFilename)
    projectDirectory = "../explorations/playAudioInSequence/Inferno"
    tierGuideFile = "../explorations/playAudioInSequence/Inferno/tierGuide.yaml"
    grammaticalTermsFile = "../explorations/playAudioInSequence/Inferno/abbreviations.txt"
    text = Text(elanXmlFilename,
                audioFilename,
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
def test_aym_numbering(display,audioFilename,extract):
    print("--- test_aym_numbering")

    # audioFilename = "../testData/Cargos.ogg"
    elanXmlFilename = "../testTextPyData/aym/aym-final.eaf"
    targetDirectory = "../testTextPyData/aym/Audio"
    soundFile = os.path.join(targetDirectory, "Cargos.ogg")
    projectDirectory = "../testTextPyData/aym"
    tierGuideFile = "../testTextPyData/aym/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/aym/List of abbreviations.txt"
    text = Text(elanXmlFilename,
                audioFilename,
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
def test_Inferno(display,audioFilename,extract):
    print("--- test_Inferno")
    try:
        assert(os.path.exists("../testTextPyData/Inferno/audio"))
    except AssertionError:
        os.mkdir("../testTextPyData/Inferno/audio")

    # audioFilename = "../testTextPyData/Inferno/inferno-threeLines.wav"
    elanXmlFilename = "../testTextPyData/Inferno/inferno-threeLines.eaf"
    targetDirectory = "../testTextPyData/Inferno/audio"
    soundFile = os.path.join(targetDirectory, audioFilename)
    projectDirectory = "../testTextPyData/Inferno"
    tierGuideFile = "../testTextPyData/Inferno/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Inferno/abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    if extract:
        ae.extract()
    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    htmlText = text.toHTML()
    if (display):
        filename = "../testTextPyData/Inferno/inferno-threeLines.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)

# ----------------------------------------------------------------------------------------------------
def test_AYAFW(display,audioFilename,extract):
    print("--- test_AYAFW")
    # audioFilename = "../testData/Cargos.ogg"
    elanXmlFilename = "../testTextPyData/AYAFW/AYAFW.eaf"
    targetDirectory = "../testTextPyData/AYAFW/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.ogg")
    projectDirectory = "../testTextPyData/AYAFW"
    tierGuideFile = "../testTextPyData/AYAFW/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/AYAFW/abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    if extract:
        ae.extract()
    text = Text(elanXmlFilename,
                audioFilename,
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
def test_Merchant(display,audioFilename,extract):
    print("--- test_Merchant")
    # audioFilename = "../testData/Cargos.ogg"
    elanXmlFilename = "../testTextPyData/JITZ/JITZ.eaf"
    targetDirectory = "../testTextPyData/JITZ/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.ogg")
    projectDirectory = "../testTextPyData/JITZ"
    tierGuideFile = "../testTextPyData/JITZ/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/JITZ/grammaticalTerms.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    if extract:
        ae.extract()
    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # 				startStopTable=times)

    # IjalLine.getTable(1)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "../testTextPyData/JITZ/test_Merchant.html"
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
def test_Jagpossum(display,audioFilename,extract):
    print("--- test_Jagpossum")
    # audioFilename = "../testData/Cargos.ogg"
    elanXmlFilename = "../testTextPyData/Jagpossum/Jagpossum.eaf"
    targetDirectory = "../testTextPyData/Jagpossum/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.ogg")
    projectDirectory = "../testTextPyData/Jagpossum"
    tierGuideFile = "../testTextPyData/Jagpossum/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Jagpossum/abbreviations.txt"
    # ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    # if extract:
    #     ae.extract()
    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile,
                tierGuideFile,
                projectDirectory)

    # IjalLine.getTable(1)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "../testTextPyData/Jagpossum/test_Jagpossum.html"
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
def test_Sanchizo(display,audioFilename,extract):
    print("--- test_Sanchizo")
    # audioFilename = "../testData/Cargos.ogg"
    elanXmlFilename = "../testTextPyData/Sanchizo/Sanchizo.eaf"
    targetDirectory = "../testTextPyData/Sanchizo/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.ogg")
    projectDirectory = "../testTextPyData/Sanchizo"
    tierGuideFile = "../testTextPyData/Sanchizo/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Sanchizo/abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    if extract:
        ae.extract()
    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # 				startStopTable=times)

    # IjalLine.getTable(1)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "../testTextPyData/Sanchizo/test_Sanchizo.html"
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
def test_Caterpillar(display,audioFilename,extract):
    print("--- test_Caterpillar")
    # audioFilename = "../testData/Cargos.ogg"
    elanXmlFilename = "../testTextPyData/Caterpillar/Caterpillar.eaf"
    targetDirectory = "../testTextPyData/Caterpillar/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.ogg")
    projectDirectory = "../testTextPyData/Caterpillar"
    tierGuideFile = "../testTextPyData/Caterpillar/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Caterpillar/abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    if extract:
        ae.extract()
    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # 				startStopTable=times)

    # IjalLine.getTable(1)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "../testTextPyData/Caterpillar/test_Caterpillar.html"
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
def test_Lazybones(display,audioFilename,extract):
    print("--- test_Lazybones")

    # audioFilename = "../testData/Cargos.ogg"
    elanXmlFilename = "../testTextPyData/Lazybones/Lazybones.eaf"
    targetDirectory = "../testTextPyData/Lazybones/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.ogg")
    projectDirectory = "../testTextPyData/Lazybones"
    tierGuideFile = "../testTextPyData/Lazybones/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Lazybones/abbreviations.txt"
    # audioFilename ="/Users/David/OpenSource/github/OldSlexilTestData/TEX_Lazy/4_TEX_TheLazyWoman.wav"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    if extract:
        ae.extract()
    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "../testTextPyData/Lazybones/test_Lazybones.html"
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
def test_Zelf(display,audioFilename,extract):
    print("--- test_Zelf")
    # audioFilename = "../testData/Cargos.ogg"
    elanXmlFilename = "../testTextPyData/Zelfmar/Zelfmar.eaf"
    targetDirectory = "../testTextPyData/Zelfmar/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.ogg")
    projectDirectory = "../testTextPyData/Zelfmar"
    tierGuideFile = "../testTextPyData/Zelfmar/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Zelfmar/abbreviations.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    if extract:
        ae.extract()
    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # 				startStopTable=times)

    # IjalLine.getTable(1)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "../testTextPyData/Zelfmar/test_Zelf.html"
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
def test_Prayer(display,audioFilename,extract):
    print("--- test_Prayer")
    # audioFilename = "../testData/Cargos.ogg"
    elanXmlFilename = "../testTextPyData/Prayer_superscript/praying.eaf"
    targetDirectory = "../testTextPyData/Prayer_superscript/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.ogg")
    projectDirectory = "../testTextPyData/Prayer_superscript"
    tierGuideFile = "../testTextPyData/Prayer_superscript/tierGuide.yaml"
    grammaticalTermsFile = "../testTextPyData/Prayer_superscript/grammaticalTerms.txt"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    if extract:
        ae.extract()
    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory)  # ,
    # 				startStopTable=times)

    # IjalLine.getTable(1)

    try:
        htmlText = text.toHTML()
        if (display):
            filename = "../testTextPyData/Prayer_superscript/test_Prayer.html"
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

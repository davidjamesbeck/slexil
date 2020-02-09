import re
import sys
sys.path.append("..")
import audioExtractor
from ijalLine import *
import importlib
import os
import pdb
import yaml
import pandas as pd
import pickle
#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
#----------------------------------------------------------------------------------------------------
def runTests():

    test_buildTable()
    test_getStartStopTimes()
    #
    test_lokono_line_3()    # each morpheme and gloss are separate xml tier elements
    test_extractAudio()   # only works when LARGE monkeyAndThunder files is present
    test_lokono_toHTML(False, sampleOfLinesOnly=True)
    #
    test_monkeyAndThunder_line_6() # morphemes and glosses are each packed into in
    #                                # a single tab-delimited tier element
    test_monkeyAndThunder_toHTML(False)
    test_plumedSerpent_toHTML(False)
    test_aktzini_toHTML()
    test_prayer_toHTML(displayPage=False)

#----------------------------------------------------------------------------------------------------
def test_buildTable():

    print("--- test_buildTable")

    filename = "../testData/lokono/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testData/lokono/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 3, tierGuide,'1')
    x3.parse()
    tbl = x3.getTable()
    assert(tbl.shape == (10,14))
    assert(tbl.columns.tolist() == ['ANNOTATION_ID', 'LINGUISTIC_TYPE_REF', 'START', 'END',
                                    'TEXT', 'ANNOTATION_REF', 'TIME_SLOT_REF1', 'TIME_SLOT_REF2',
                                    'PARENT_REF', 'TIER_ID', 'TEXT_LENGTH', 'HAS_TABS', 'HAS_SPACES',
                                    'category'])

    assert(tbl['category'].tolist() == ['speech', 'translation', 'morpheme', 'morphemeGloss',
                                        'morpheme', 'morphemeGloss', 'morpheme', 'morphemeGloss',
                                        'morpheme', 'morphemeGloss'])

    assert(tbl['ANNOTATION_ID'].tolist() == ['a26', 'a969', 'a20533', 'a22390', 'a20534', 'a22391',
                                             'a20535', 'a22392', 'a20536', 'a22393'])

    assert(tbl['TIER_ID'].tolist() == ['Orthographic represntation', 'English translation', 'morpheme', 'gloss',
                                        'morpheme', 'gloss', 'morpheme', 'gloss', 'morpheme', 'gloss'])

        # first element is empty, confusingly parsed out of xml as math.nan.  don't test for it - too peculiar
    assert(tbl['ANNOTATION_REF'].tolist()[1:] == ['a26', 'a12134', 'a12134', 'a12135', 'a12135', 'a12136',
                                                   'a12136', 'a12137', 'a12137'])

#----------------------------------------------------------------------------------------------------
def test_getStartStopTimes():

    print("--- test_getStartStopTimes")

    filename = "../testData/lokono/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testData/lokono/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 3, tierGuide) # ,audioData='a,b,c')
    x3.parse()
    tbl = x3.getTable()
    startTime = x3.getStartTime()
    endTime = x3.getEndTime()
    assert(startTime == 8850.0)
    assert(endTime == 10570.0)

#----------------------------------------------------------------------------------------------------
def test_lokono_line_3():

    """
      used for early exploration and development of the IjalLine class
    """
    print("--- test_lokono_line_3")

    filename = "../testData/lokono/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testData/lokono/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.safe_load(f)

    grammaticalTerms = ['fem','poss','indf']
    x3 = IjalLine(doc, 3, tierGuide, grammaticalTerms)
    x3.parse()

    assert(x3.speechRow == 0)
    assert(x3.translationRow == 1)
    assert(x3.morphemeRows == [2, 4, 6, 8])
    assert(x3.morphemeGlossRows == [3, 5, 7, 9])

    assert(x3.getSpokenText() == 'thusa, aba hiyaro kiba.')
    try:
        assert(x3.getTranslation() == "‘[a] child, a woman as well.’")
    except AssertionError as e:
        raise Exception(x3.getTranslation()) from e
    assert(x3.getMorphemes() == ['tʰ–ɨsa', 'aba', 'hijaro', 'kiba'])
    assert(x3.getMorphemeGlosses() == ['3FEM.POSS–child', 'INDF', 'woman', 'too'])
    assert(x3.getMorphemeSpacing() == [16, 5, 7, 5])   # word width + 1

#----------------------------------------------------------------------------------------------------
def test_extractAudio():

    print("--- test_extractAudio")
    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    assert(os.path.exists(filename))
    xmlDoc = etree.parse(filename)
    mediaDescriptors = xmlDoc.findall("HEADER/MEDIA_DESCRIPTOR")
    assert(len(mediaDescriptors) == 1)
    soundFileElement = mediaDescriptors[0]
    soundFileURI = soundFileElement.attrib["RELATIVE_MEDIA_URL"]
    directory = os.path.dirname(os.path.abspath(filename))
    fullPath = os.path.join(directory, soundFileURI)
    print("fullPath: %s" % fullPath)
    assert(os.path.exists(fullPath))

#----------------------------------------------------------------------------------------------------
def test_lokono_toHTML(displayPage=False, sampleOfLinesOnly=True):

    print("--- test_lokono_toHTML")

    filename = "../testData/lokono/LOKONO_IJAL_2.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 41

    tierGuideFile = "../testData/lokono/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.safe_load(f)

    lines = []

    if(sampleOfLinesOnly):
        maxLines = 10
    else:
        maxLines = lineCount

    grammarTerms = ["hab","past"]
    for i in range(maxLines):
       line = IjalLine(xmlDoc, i, tierGuide, grammarTerms)
       if(line.tierCount < 4):
          print("skipping line %d, tierCount %d" %(i, line.tierCount))
       else:
          # print("parsing line %d" % i)
          line.parse()
          lines.append(line)

    # print("parsed %d/%d complete lines" % (len(lines), lineCount))

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
       with htmlDoc.tag('head'):
           htmlDoc.asis('<meta charset="UTF-8">')
           htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
           htmlDoc.asis('<script src="ijalUtils.js"></script>')
           with htmlDoc.tag('body'):
               for line in lines:
                  line.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    #displayPage = True
    if(displayPage):
       filename = "tmp.html"
       f = open(filename, "w")
       f.write(indent(htmlText))
       f.close()
       os.system("open %s" % filename)


#----------------------------------------------------------------------------------------------------
def test_monkeyAndThunder_line_6():

    """
      used for early exploration and development of the IjalLine class
    """
    print("--- test_monkeyAndThunder_line_6")

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)

    tierGuideFile = "../testData/monkeyAndThunder/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.safe_load(f)

    grammaticalTermsFile = "../testData/monkeyAndThunder/grammaticalTerms.txt"
    grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    assert("MOUTH" in grammaticalTerms)

    x6 = IjalLine(doc, 6, tierGuide, grammaticalTerms)
    x6.parse()

    assert(x6.speechRow == 0)
    assert(x6.translationRow == 2)
    assert(x6.morphemeRows == [1])
    assert(x6.morphemeGlossRows == [3])

    assert(x6.getSpokenText() == 'Ke jejn makput. Makndüj mbeʹ ii maknhwej maj.')
    assert(x6.getTranslation() == '‘He left. He went looking for someone who could shout louder.’')
    try:
        assert(x6.getMorphemes() == ['que', 'heM', 'mak=put', 'mak=nǝh', 'meʔ', 'ʔiː', 'mak=ŋ•weh', 'mas'])
    except AssertionError as e:
        raise Exception(x6.getMorphemes()) from e
    assert(x6.getMorphemeGlosses() == ['that', 'there', 'CMP=exit', 'CMP=go', 'DIST', 'who', 'CMP=MOUTH•cry', 'more'])
    assert(x6.getMorphemeSpacing() == [5, 6, 9, 8, 5, 4, 14, 5])  # word width + 1

    htmlDoc = Doc()
    x6.toHTML(htmlDoc)
    htmlText = htmlDoc.getvalue()
    assert(htmlText.count("grammatical-term") == 5)
    #print(indent(htmlText))

#----------------------------------------------------------------------------------------------------
def test_monkeyAndThunder_line_0():

    """
      neither morphemes nor glosses in this line: just spanish and english
    """
    print("--- test_monkeyAndThunder_line_0")

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)

    tierGuideFile = "../testData/monkeyAndThunder/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.safe_load(f)

    x0 = IjalLine(doc, 0, tierGuide)
    x0.parse()

    assert(x0.speechRow == 0)
    assert(x0.translationRow == 1)
    assert(x0.morphemeRows == [])
    assert(x0.morphemeGlossRows == [])

    assert(x0.getSpokenText() == 'Por ejemplo el, como se llama, el mono,')
    assert(x0.getTranslation() == '‘For example it, what do you call it, the monkey,’')
    assert(x0.getMorphemes() == [])
    assert(x0.getMorphemeGlosses() == [])
    assert(x0.getMorphemeSpacing() == [])

#----------------------------------------------------------------------------------------------------
def test_monkeyAndThunder_toHTML(displayPage=False):

    print("--- test_monkeyAndThunder_toHTML")

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    grammaticalTermFile = "../testData/monkeyAndThunder/grammaticalTerms.txt"
    with open(grammaticalTermFile,'r') as f:
        grammaticalTerms = f.read().split('\n')
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 41

    tierGuideFile = "../testData/monkeyAndThunder/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.safe_load(f)

    lines = []
    for i in range(lineCount):
        line = IjalLine(xmlDoc, i, tierGuide, grammaticalTerms)
        #if(line.tierCount < 4):
        #    print("skipping line %d, tierCount %d" %(i, line.tierCount))
        #else:
        line.parse()
        lines.append(line)

    #print("parsed %d/%d complete lines" % (len(lines), lineCount))

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
       with htmlDoc.tag('head'):
           htmlDoc.asis('<meta charset="UTF-8">')
           htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
           htmlDoc.asis('<script src="ijalUtils.js"></script>')
           with htmlDoc.tag('body'):
               for line in lines:
                  line.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()

    if(displayPage):
       filename = "tmp.html"
       f = open(filename, "w")
       f.write(indent(htmlText))
       f.close()
       os.system("open %s" % filename)

#----------------------------------------------------------------------------------------------------
def test_aktzini_toHTML(displayPage=False):

    print("--- test_aktzini_toHTML")

    filename = "../testData/aktzini/18-06-03Aktzini-GA.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 16

    lineNumber = 0
    for lineNumber in range(lineCount):
       rootElement = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
       allElements = findChildren(xmlDoc, rootElement)
       tmpTbl = buildTable(xmlDoc, allElements)
       print("---- line %d" % lineNumber)
       #print(tmpTbl)

       # every line has exactly two tiers: "Line"  "L3Gloss"
       # skipping this text for now

#----------------------------------------------------------------------------------------------------
def test_plumedSerpent_toHTML(displayPage=False):

    print("--- test_plumedSerpent_toHTML")

    filename = "../testData/plumedSerpent/TRS_Plumed_Serpent_Legend_05-15-2017.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 15
    #print(lineCount)

    for lineNumber in range(lineCount):
       rootElement = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
       allElements = findChildren(xmlDoc, rootElement)
       tmpTbl = buildTable(xmlDoc, allElements)
       #print("---- line %d" % lineNumber)
       #print(tmpTbl)

    tierGuideFile = "../testData/plumedSerpent/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.safe_load(f)

    lines = []
    grammaticalTerms = ["hab","past"]
    for i in range(lineCount):
        line = IjalLine(xmlDoc, i, tierGuide, grammaticalTerms)
        if(line.tierCount < 4):
            print("skipping line %d, tierCount %d" %(i, line.tierCount))
        else:
           line.parse()
           lines.append(line)

    # print("parsed %d/%d complete lines" % (len(lines), lineCount))

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
       with htmlDoc.tag('head'):
           htmlDoc.asis('<meta charset="UTF-8">')
           htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
           htmlDoc.asis('<script src="ijalUtils.js"></script>')
           with htmlDoc.tag('body'):
               for line in lines:
                  line.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()

    if(displayPage):
       filename = "tmp.html"
       f = open(filename, "w")
       f.write(indent(htmlText))
       f.close()
       os.system("open %s" % filename)


#----------------------------------------------------------------------------------------------------
def test_prayer_toHTML(displayPage=False):

    print("--- test_prayer_toHTML")

    filename = "../testData/prayer/20150717_Prayer_community_one.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 9
    # print(lineCount)

    for lineNumber in range(lineCount):
       rootElement = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
       allElements = findChildren(xmlDoc, rootElement)
       tmpTbl = buildTable(xmlDoc, allElements)
       #print("---- line %d" % lineNumber)
       #print(tmpTbl)

    tierGuideFile = "../testData/prayer/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.safe_load(f)

    lines = []
    grammaticalTerms = ["hab","past"]
    for i in range(lineCount):
        line = IjalLine(xmlDoc, i, tierGuide, grammaticalTerms)
        if(line.tierCount < 4):
            print("skipping line %d, tierCount %d" %(i, line.tierCount))
        else:
           line.parse()
           lines.append(line)

    #print("parsed %d/%d complete lines" % (len(lines), lineCount))

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
       with htmlDoc.tag('head'):
           htmlDoc.asis('<meta charset="UTF-8">')
           htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
           htmlDoc.asis('<script src="ijalUtils.js"></script>')
           with htmlDoc.tag('body'):
               for line in lines:
                  line.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()

    if(displayPage):
       filename = "tmp.html"
       f = open(filename, "w")
       f.write(indent(htmlText))
       f.close()
       os.system("open %s" % filename)


#----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    runTests()

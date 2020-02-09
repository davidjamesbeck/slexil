# -*- coding: utf-8 -*-

import sys,os
sys.path.append("..")
from grammaticalTerms import *
#------------------------------------------------------------------------------------------------------------------------
sampleLines = ["HAB=3A=MOUTH•cry",
               "1S=walk–INC",
               "HAB=3A=work=IAM",
               "PROG=1A=know–INTR",
               "more",
               "1OBJ",
               "PL^black.dog<masc>+pl"
               ]


#----------------------------------------------------------------------------------------------------
grammaticalTermsFiles = ["../testData/monkeyAndThunder/grammaticalTerms.txt",
                         "../testData/inferno-threeLines/grammaticalTerms.txt"]
grammaticalTerms = []
for file in grammaticalTermsFiles:
   newTerms = open(file).read().split("\n")
   grammaticalTerms += newTerms[:-1]


#----------------------------------------------------------------------------------------------------
def runTests():

    test_constructor()
    test_inferno()
    test_toHTML_sampleLine_0()
    test_toHTML_sampleLine_1()
    test_toHTML_sampleLine_2()
    test_toHTML_sampleLine_3()
    test_toHTML_sampleLine_4()
    test_toHTML_sampleLine_5()
    test_nDashes()
    test_Sub_and_Sup()
    test_Additional_Delimiters()
    test_toHTML_sampleLine_6()
    
def test_constructor():

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    gt = GrammaticalTerms(sampleLines[0], grammaticalTerms)


def test_toHTML_sampleLine_0(displayPage=False):
    """
      create an empty htmlDoc, then render the MorhphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_0")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    gt = GrammaticalTerms(sampleLines[0], grammaticalTerms)
    gt.parse()
    assert(gt.getParts() == ['hab', '=', '3A', '=', 'mouth', '•', 'cry'])

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                gt.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    assert(htmlText.count('<span class="grammatical-term">') == 3)  # HAB, A, MOUTH

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")

def test_toHTML_sampleLine_1(displayPage=False):
    """
      create an empty htmlDoc, then render the MorhphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_1")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    gt = GrammaticalTerms(sampleLines[1], grammaticalTerms)
    gt.parse()
    assert(gt.getParts() == ['1S', '=', 'walk', '–', 'inc'])

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                gt.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    assert(htmlText.count('<span class="grammatical-term">') == 2)  # S  INC

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")

def test_toHTML_sampleLine_2(displayPage=False):
    """
      create an empty htmlDoc, then render the MorhphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_2")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    gt = GrammaticalTerms(sampleLines[2], grammaticalTerms)
    gt.parse()
    gt.getParts()
    assert(gt.getParts() == ['hab', '=', '3A', '=', 'work', '=', 'iam'])

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                gt.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    assert(htmlText.count('<span class="grammatical-term">') == 3)  # HAB A IAM

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")

def test_toHTML_sampleLine_3(displayPage=False):
    """
      create an empty htmlDoc, then render the MorhphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_3")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    gt = GrammaticalTerms(sampleLines[3], grammaticalTerms)
    gt.parse()
    gt.getParts()
    assert(gt.getParts() == ['prog', '=', '1A', '=', 'know', '–', 'intr'])

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                gt.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    assert(htmlText.count('<span class="grammatical-term">') == 3)  # PROG A INTR

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")

def test_toHTML_sampleLine_4(displayPage=False):
    """
      create an empty htmlDoc, then render the MorhphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_4")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    gt = GrammaticalTerms(sampleLines[4], grammaticalTerms)
    gt.parse()
    gt.getParts()
    assert(gt.getParts() == ['more'])

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                gt.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    assert(htmlText.count('<span class="grammatical-term">') == 0)  # none in this gloss

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")


def test_toHTML_sampleLine_5(displayPage=False):
    """
      create an empty htmlDoc, then render the MorhphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_5")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    gt = GrammaticalTerms(sampleLines[5], grammaticalTerms)
    gt.parse()
    gt.getParts()
    try:
       assert(gt.getParts() == ['1obj'])
    except AssertionError as e:
       raise Exception(gt.getParts()) from e

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                gt.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    assert(htmlText.count('<span class="grammatical-term">') == 1)  # PRO

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")


# def test_inferno(displayPage=False):
#     """
#       a bunch of new terms came with this text.  test them all out here
#     """
#     print("--- test_inferno")
# 
#     gt = GrammaticalTerms("in=DEF-MASC-SG", grammaticalTerms)
#     gt.parse()
#     assert(gt.getParts() == ['in', '=', 'def', '–', 'masc', '–', 'sg'])
# 
#     gt = GrammaticalTerms("middle-MASC", grammaticalTerms); gt.parse()
#     assert(gt.getParts() == ['middle', '–', 'masc'])
# 
#     gt = GrammaticalTerms("of=DEF-MASC-SG", grammaticalTerms); gt.parse();
#     assert(gt.getParts() == ['of', '=', 'def', '–', 'masc', '–', 'sg'])
# 
#     gt = GrammaticalTerms("journey-MASC", grammaticalTerms); gt.parse();
#     assert(gt.getParts() == ['journey', '–', 'masc'])
# 
#     gt = GrammaticalTerms("our-FEM-SG", grammaticalTerms); gt.parse();
#     assert(gt.getParts() == ['our', '–', 'fem', '–', 'sg'])
# 
#     gt = GrammaticalTerms("life-FEM", grammaticalTerms); gt.parse();
#     assert(gt.getParts() == ['life', '–', 'fem'])
# 
#     gt = GrammaticalTerms("be-3SG-IMPF", grammaticalTerms); gt.parse();
#     assert(gt.getParts() == ['be', '–', '3sg', '–', 'impf'])
# 
#     gt = GrammaticalTerms("found–1SG-INDEF-REM-PAST", grammaticalTerms); gt.parse();
#     assert(gt.getParts() ==  ['found', '–', '1sg', '–', 'indef', '–', 'rem', '–', 'past'])

def test_nDashes(displayPage=False):
    """
      test for hyphens
    """
    print("--- test_nDashes")

    gt = GrammaticalTerms("in=DEF-MASC-3SG", grammaticalTerms)
    gt.parse()
    assert(gt.getParts() ==  ['in', '=', 'def', '–', 'masc', '–', '3sg'])

def test_Sub_and_Sup(displayPage=False):
    """
      test input with subscripts and superscripts
    """
    print("--- test_Sub_and_Sup")

    gt = GrammaticalTerms("gu<sup>1</sup>hin<sub>MASC</sub>-PL", ["masc","pl"])
    gt.parse()
    assert(gt.getParts() ==  ['gu', '<sup>', '1', '</sup>', 'hin', '<sub>', 'masc', '</sub>', '–', 'pl'])

def test_Additional_Delimiters(displayPage=False):
    """
      customizable test to make sure added delimiters don't cause problems
      Currently configured for: ^, +, < >
    """
    print("--- test_Additional_Delimiters")

    gt = GrammaticalTerms("PL^Dog<masc>+pl", ["masc","pl"])
    gt.parse()
    try:
       assert(gt.getParts() ==  ['pl', '^', 'Dog', '<', 'masc','>', '+', 'pl'])
    except AssertionError as e:
       raise Exception(gt.getParts()) from e

def test_toHTML_sampleLine_6(displayPage=True):
    """
      create an empty htmlDoc, then render the MorphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_6")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    gt = MorphemeGloss("PL^black.dog<masc>+pl", ["masc","pl"])
    gt.parse()
    gt.getParts()
    try:
       assert(gt.getParts() ==  ['pl', '^', 'black', '.', 'dog', '<', 'masc', '>', '+', 'pl'])
    except AssertionError as e:
       raise Exception(gt.getParts()) from e
       pass

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                gt.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    #print(htmlText.count('<span class="grammatical-term">'))
    assert(htmlText.count('<span class="grammatical-term">') == 3)  # PRO

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")


if __name__ == '__main__':
    runTests()


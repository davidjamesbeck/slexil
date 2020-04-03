from xml.etree import ElementTree as etree
import sys, os
sys.path.append("..")
import yaml
from ijalLine import IjalLine as line
import pandas as pd
pd.set_option('display.max_columns', 500)
#----------------------------------------------------------------------------------------------------

def runListTiers():
    testInferno() # tests alignable speech tier, no exta alignable tiers
    testInfernoPlusOne() # tests alignable speech tier plus extra alignable, daughter of speechTier
    testInfernoPlusSister() # tests alignable speech tier plus extra alignable, sister of speechTier
    testJagpossum() # tests non-alignable speech tier one level down, no extra alignables
    testInfernoDeep() # tests non-alignable speech tier two levels down, no extra alignables
    testInfernoDeepPlusOne() # tests non-alignable speech tier two levels down, extra alignable
    testAktziniPlusOne()

#----------------------------------------------------------------------------------------------------
def testAktziniPlusOne():
    print("===testAktziniPlusOne===")
    eafFile = '../testData/findingSpeechTiers/Aktzini_plus_one.eaf'
    tierGuide = '../testData/findingSpeechTiers/tierGuideAktz.yaml'
    tierList, speechTierList = listTiers(eafFile, tierGuide)
    try:
        assert(len(speechTierList) == 16)
    except AssertionError:
        print("!!!Looking for 16 lines!!!")
        pass

#----------------------------------------------------------------------------------------------------
def testInfernoDeepPlusOne():
    print("===testInfernoDeepPlusOne===")
    eafFile = '../testData/findingSpeechTiers/infernoDeep_plus_one.eaf'
    tierGuide = '../testData/findingSpeechTiers/tierGuide.yaml'
    tierList, speechTierList = listTiers(eafFile, tierGuide)
    try:
        assert(len(speechTierList) == 3)
    except AssertionError:
        print("!!!Looking for 3 lines!!!")
        pass

#----------------------------------------------------------------------------------------------------
def testInferno():
    print("===testInferno===")
    eafFile = '../testData/findingSpeechTiers/inferno-threeLines.eaf'
    tierGuide = '../testData/findingSpeechTiers/tierGuide.yaml'
    tierList, speechTierList = listTiers(eafFile, tierGuide)
    assert(len(speechTierList) == 3)

# ----------------------------------------------------------------------------------------------------
def testJagpossum():
    print("===testJagpossum===")
    eafFile = '../testData/findingSpeechTiers/Jagpossum.eaf'
    tierGuide = '../testData/findingSpeechTiers/tierGuideJP.yaml'
    tierList, speechTierList = listTiers(eafFile, tierGuide)
    try:
        assert(len(speechTierList) == 136)
    except AssertionError:
        print("!!!Looking for 136 lines!!!")
        pass

#----------------------------------------------------------------------------------------------------
def testInfernoDeep():
    print("===testInfernoDeep===")
    eafFile = '../testData/findingSpeechTiers/infernoDeep.eaf'
    tierGuide = '../testData/findingSpeechTiers/tierGuide.yaml'
    tierList, speechTierList = listTiers(eafFile, tierGuide)
    try:
        assert(len(speechTierList) == 3)
    except AssertionError:
        print("!!!Looking for 3 lines!!!")
        pass

#----------------------------------------------------------------------------------------------------
def testInfernoPlusOne():
    print("===testInfernoPlusOne===")
    eafFile = '../testData/findingSpeechTiers/inferno-threeLines_plus_one.eaf'
    tierGuide = '../testData/findingSpeechTiers/tierGuide.yaml'
    tierList, speechTierList = listTiers(eafFile, tierGuide)
    assert(len(speechTierList) == 3)

#----------------------------------------------------------------------------------------------------
def testInfernoPlusSister():
    print("===testInfernoPlusSister===")
    eafFile = '../testData/findingSpeechTiers/inferno-threeLines_plus_sister.eaf'
    tierGuide = '../testData/findingSpeechTiers/tierGuide.yaml'
    tierList, speechTierList = listTiers(eafFile, tierGuide)
    assert(len(speechTierList) == 3)

#----------------------------------------------------------------------------------------------------
def listTiers(doc,guide):
    doc = etree.parse(doc)
    with open(guide, 'r') as f:
        tierGuide = yaml.safe_load(f)
    speechTier = tierGuide['speech']
    tierList = doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")
    speechTierList = doc.findall("TIER[@TIER_ID='%s']/ANNOTATION/ALIGNABLE_ANNOTATION" %speechTier)
    refTierList = doc.findall("TIER[@TIER_ID='%s']/ANNOTATION/REF_ANNOTATION" %speechTier)
    if len(speechTierList) == 0:
        '''CASE III: speech-tier is not alignable, daughter of only alignable tier ==> use tierlist'''
        '''CASE IV: speech-tier is not alignable, there is another alignable tier ==> ???'''
        print("Cases III and IV")
        speechTierList = refTierList
    else:
        '''CASE I: speech-tier is only alignable tier ==> use speechTierList'''
        '''CASE II: speech-tier is alignable, but not the only alignable ==> use speechTierList'''
        print("Cases I and II: use speechTierList")
    print("%d alignable annotations, %d speech annotations" %(len(tierList), len(speechTierList)))
    ln = line(doc,1,tierGuide)
    ln.parse()
    print(ln.getStartTime())
    return tierList, speechTierList

if __name__ == '__main__':
    runListTiers()

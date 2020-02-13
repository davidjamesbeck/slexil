# test_AudioExtractor.py
#----------------------------------------------------------------------------------------------------
import re
import sys
sys.path.append("..")

from audioExtractor import *
#----------------------------------------------------------------------------------------------------
def runTests():

    test_constructor()
    test_determineStartAndEndTimes()
    test_extract_HMDLsafe()
    test_extract_monkeyAndThunder()
    test_extract_prayer()
    test_extract_aktzini()
    test_extract_plumedSerpent()
    test_extract_Aymara_final()


def test_constructor():

    print("--- test_constructor")

    ea = AudioExtractor("../testData/HMDLsafe/HMDL.wav",
                        "../testData/HMDLsafe/HMDL.eaf",
                        "../testData/HMDLsafe/audio")
    assert(ea.validInputs)

def test_determineStartAndEndTimes():

    print("--- test_determineStartAndEndTimes")
    ea = AudioExtractor("../testData/HMDLsafe/HMDL.wav",
                        "../testData/HMDLsafe/HMDL.eaf",
                        "../testData/HMDLsafe/audio")
    tbl = ea.determineStartAndEndTimes()
    # print(tbl)
    assert(tbl.shape == (4, 5))
    assert(list(tbl.columns) == ["lineID", "start", "end", "t1", "t2"])
    (a4_start, a4_end) = tbl.loc[tbl['lineID'] == 'a4'][['start', 'end']].iloc[0].tolist()
    assert(a4_start == 17800)
    assert(a4_end == 22938)

def test_extract_HMDLsafe():

    print("--- test_extract_HMDLsafe")

    ea = AudioExtractor("../testData/HMDLsafe/HMDL.wav",
                        "../testData/HMDLsafe/HMDL.eaf",
                        "../testData/HMDLsafe/audio")
    ea.extract(quiet=True)
    fileList = [f for f in os.listdir("../testData/HMDLsafe/audio") if not f.startswith('.')]
    try:
        assert(len(fileList) == 4)
    except AssertionError as e:
        raise Exception(fileList) from e

def test_extract_Aymara_final():

    print("--- test_extract_Aymara_final")

    ea = AudioExtractor("../testTextPyData/Aymara_final/Final-Edwin-historia-del-oso_no_anotado__ch1.wav",
                        "../testTextPyData/Aymara_final/Aymara-final.eaf",
                        "../testTextPyData/Aymara_final/audio")
    ea.extract(quiet=True)
    fileList = [f for f in os.listdir("../testTextPyData/Aymara_final/audio") if not f.startswith('.')]
    try:
        assert(len(fileList) == 146)
    except AssertionError as e:
        raise Exception(len(fileList)) from e

def test_extract_monkeyAndThunder():
    print("--- test_extract_monkeyAndThunder")
    ea = AudioExtractor("../testData/monkeyAndThunder/AYA1_MonkeyandThunder-32bit.wav",
                        "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf",
                        "../testData/monkeyAndThunder/audio")
    ea.extract(quiet=True)
    fileList = [f for f in os.listdir("../testData/monkeyAndThunder/audio") if not f.startswith('.')]
    try:
        assert(len(fileList) == 41)
    except AssertionError as e:
        raise Exception(fileList) from e


def test_extract_prayer():
    print("--- test_extract_prayer")
    ea = AudioExtractor("../testData/prayer/SJQ-2009_Cruz.wav",
                        "../testData/prayer/20150717_Prayer_community_one.eaf",
                        "../testData/prayer/audio")
    fileList = [f for f in os.listdir("../testData/prayer/audio") if not f.startswith('.')]
    ea.extract(quiet=True)
    assert(len(fileList) == 9)

def test_extract_aktzini():
    print("--- test_extract_aktzini")
    ea = AudioExtractor("../testData/aktzini/18-06-03Aktzini-GA.wav",
                        "../testData/aktzini/18-06-03Aktzini-GA.eaf",
                        "../testData/aktzini/audio")
    ea.extract(quiet=True)
    fileList = [f for f in os.listdir("../testData/aktzini/audio") if not f.startswith('.')]
    assert(len(fileList) == 16)

def test_extract_plumedSerpent():
    print("--- test_extract_plumedSerpent")
    ea = AudioExtractor("../testData/plumedSerpent/Chicahuaxtla Triqui - La serpiente emplumada 04-28-2016.wav",
                        "../testData/plumedSerpent/TRS_Plumed_Serpent_Legend_05-15-2017.eaf",
                        "../testData/plumedSerpent/audio")
    ea.extract(quiet=True)
    fileList = [f for f in os.listdir("../testData/plumedSerpent/audio") if not f.startswith('.')]
    assert(len(fileList) == 16)


if __name__ == '__main__':
    runTests()

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
    test_extract_AYAMT()
    test_extract_praying()
    test_extract_aktzini()
    test_extract_featherSnake()
    test_extract_aym_final()
    test_extract_Ghost()
    # test_tierGuide_specific_extraction() #this test is not longer relevant (AE doesn't use the tierguide)

def clearAudioDirectory(targetDirectory):
    fileList=os.listdir(targetDirectory)
    for f in fileList:
        os.remove(os.path.join(targetDirectory,f))

def test_tierGuide_specific_extraction():
    print("--- test tierGuide-specific extraction")
    print("-- TEST 1: aktzini")
    clearAudioDirectory("../testData/aktzini/audio")
    ea = AudioExtractor("../testData/aktzini/18-06-03Aktzini-GA.wav",
                        "../testData/aktzini/18-06-03Aktzini-GA.eaf",
                        "../testData/aktzini/audio",
                        "../testData/aktzini/tierGuide.yaml")
    ea.extract(quiet=True)
    fileList = [f for f in os.listdir("../testData/aktzini/audio") if not f.startswith('.')]

    try:
        assert (len(fileList) == 16)
    except AssertionError as e:
        raise Exception(len(fileList)) from e

    print("-- TEST 2: Jagpossum")
    clearAudioDirectory("../testTextPyData/Jagpossum/audio")
    ea = AudioExtractor("../testData/Cargos.ogg",
                        "../testTextPyData/Jagpossum/Jagpossum.eaf",
                        "../testTextPyData/Jagpossum/audio",
                        "../testTextPyData/Jagpossum/tierGuide.yaml")
    ea.extract(True)
    fileList = [f for f in os.listdir("../testTextPyData/Jagpossum/audio") if not f.startswith('.')]

    try:
        assert (len(fileList) == 136)
    except AssertionError as e:
        raise Exception(len(fileList)) from e

    print("-- TEST 3: GhostWagon")
    clearAudioDirectory("../testTextPyData/GhostInWagon/audio")
    ea = AudioExtractor("../testTextPyData/GhostInWagon/GhostInWagon.ogg",
                        "../testTextPyData/GhostInWagon/GhostInWagon.eaf",
                        "../testTextPyData/GhostInWagon/audio",
                        "../testTextPyData/GhostInWagon/tierGuide.yaml")
    ea.extract(True)
    fileList = [f for f in os.listdir("../testTextPyData/GhostInWagon/audio") if not f.startswith('.')]

    try:
        assert (len(fileList) == 55)
    except AssertionError as e:
        raise Exception(len(fileList)) from e

    print("-- TEST 4: loco")
    clearAudioDirectory("../testData/loco/audio")
    ea = AudioExtractor("../testData/Cargos.ogg",
                        "../testData/loco/loco.eaf",
                        "../testData/loco/audio",
                        "../testData/loco/tierGuide.yaml")
    ea.extract(True)
    fileList = [f for f in os.listdir("../testData/loco/audio") if not f.startswith('.')]

    try:
        assert (len(fileList) == 344)
    except AssertionError as e:
        raise Exception(len(fileList)) from e


def test_extract_Ghost():
    print("--- test_extract_Ghost")
    try:
        assert(os.path.exists("../testTextPyData/GhostInWagon/audio"))
        clearAudioDirectory("../testTextPyData/GhostInWagon/audio")
    except AssertionError:
        os.mkdir("../testTextPyData/GhostInWagon/audio")
    ea = AudioExtractor("../testTextPyData/GhostInWagon/GhostInWagon.ogg",
                        "../testTextPyData/GhostInWagon/GhostInWagon.eaf",
                        "../testTextPyData/GhostInWagon/audio")
    ea.extract(quiet=True)
    fileList = [f for f in os.listdir("../testTextPyData/GhostInWagon/audio") if not f.startswith('.')]
    try:
        assert(len(fileList) == 55)
    except AssertionError as e:
        raise Exception(len(fileList)) from e


def test_constructor():

    print("--- test_constructor")

    ea = AudioExtractor("../testData/Cargos.ogg",
                        "../testData/HMDLsafe/HMDL.eaf",
                        "../testData/HMDLsafe/audio")
    assert(ea.validInputs)

def test_determineStartAndEndTimes():

    print("--- test_determineStartAndEndTimes")
    ea = AudioExtractor("../testData/Cargos.ogg",
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
    clearAudioDirectory("../testData/HMDLsafe/audio")
    ea = AudioExtractor("../testData/Cargos.ogg",
                        "../testData/HMDLsafe/HMDL.eaf",
                        "../testData/HMDLsafe/audio")
    ea.extract(quiet=True)
    fileList = [f for f in os.listdir("../testData/HMDLsafe/audio") if not f.startswith('.')]
    try:
        assert(len(fileList) == 4)
    except AssertionError as e:
        raise Exception(fileList) from e

def test_extract_aym_final():

    print("--- test_extract_aym_final")
    clearAudioDirectory("../testTextPyData/aym/audio")
    ea = AudioExtractor("../testData/Cargos.ogg",
                        "../testTextPyData/aym/aym-final.eaf",
                        "../testTextPyData/aym/audio")
    ea.extract(quiet=True)
    fileList = [f for f in os.listdir("../testTextPyData/aym/audio") if not f.startswith('.')]
    try:
        assert(len(fileList) == 145)
    except AssertionError as e:
        raise Exception(len(fileList)) from e

def test_extract_AYAMT():
    print("--- test_extract_AYAMT")
    clearAudioDirectory("../testData/AYAMT/audio")
    ea = AudioExtractor("../testData/Cargos.ogg",
                        "../testData/AYAMT/AYAMT.eaf",
                        "../testData/AYAMT/audio")
    ea.extract(quiet=True)
    fileList = [f for f in os.listdir("../testData/AYAMT/audio") if not f.startswith('.')]
    try:
        assert(len(fileList) == 41)
    except AssertionError as e:
        raise Exception(fileList) from e


def test_extract_praying():
    print("--- test_extract_praying")
    clearAudioDirectory("../testData/praying/audio")
    ea = AudioExtractor("../testData/Cargos.ogg",
                        "../testData/praying/praying.eaf",
                        "../testData/praying/audio")
    ea.extract(quiet=False)
    fileList = [f for f in os.listdir("../testData/praying/audio") if not f.startswith('.')]
    try:
        assert(len(fileList) == 9)
    except AssertionError as e:
        raise Exception(len(fileList)) from e

def test_extract_aktzini():
    print("--- test_extract_aktzini")
    clearAudioDirectory("../testData/aktzini/audio")
    ea = AudioExtractor("../testData/aktzini/18-06-03Aktzini-GA.wav",
                        "../testData/aktzini/18-06-03Aktzini-GA.eaf",
                        "../testData/aktzini/audio")
    ea.extract(quiet=True)
    fileList = [f for f in os.listdir("../testData/aktzini/audio") if not f.startswith('.')]
    try:
        assert(len(fileList) == 16)
    except AssertionError as e:
        raise Exception(len(fileList)) from e

def test_extract_featherSnake():
    print("--- test_extract_featherSnake")
    clearAudioDirectory("../testData/featherSnake/audio")
    ea = AudioExtractor("../testData/Cargos.ogg",
                        "../testData/featherSnake/featherSnake.eaf",
                        "../testData/featherSnake/audio")
    ea.extract(quiet=True)
    fileList = [f for f in os.listdir("../testData/featherSnake/audio") if not f.startswith('.')]
    try:
        assert(len(fileList) == 15)
    except AssertionError as e:
        raise Exception(len(fileList)) from e

if __name__ == '__main__':
    runTests()

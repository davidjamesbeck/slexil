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
pd.set_option('display.max_columns', 10)

# ----------------------------------------------------------------------------------------------------
def runTests():
    test_inferno()
    test_inferno_plus()
    test_aktzini()
    test_AYAMT()
    test_featherSnake()
    test_HMDLsafe()
    test_Inundación()
    test_loco()
    test_praying()
    test_AYAFW()
    test_aym()
    test_Caterpillar()
    test_Cuervo()
    test_GhostInWagon()
    test_GhostInWagon_original()
    test_JITZ()
    test_Lazybones()
    test_Sanchizo()
    test_Zelfmar()

# ----------------------------------------------------------------------------------------------------
def test_Zelfmar():
    print("--- test_Zelfmar")

    elanXmlFilename = "../testTextPyData/Zelfmar/Zelfmar.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testTextPyData/Zelfmar/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 109)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 109" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_Sanchizo():
    print("--- test_Sanchizo")

    elanXmlFilename = "../testTextPyData/Sanchizo/Sanchizo.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testTextPyData/Sanchizo/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 102)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 102" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_Lazybones():
    print("--- test_Lazybones")

    elanXmlFilename = "../testTextPyData/Lazybones/Lazybones.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testTextPyData/Lazybones/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 396)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 396" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_JITZ():
    print("--- test_JITZ")

    elanXmlFilename = "../testTextPyData/JITZ/JITZ.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testTextPyData/JITZ/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 69)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 69" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_Jagpossum():
    print("--- test_Jagpossum")

    elanXmlFilename = "../testTextPyData/Jagpossum/Jagpossum.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testTextPyData/Jagpossum/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 136)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 136" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_GhostInWagon_original():
    print("--- test_GhostInWagon_original")

    elanXmlFilename = "../testTextPyData/GhostInWagon/GhostInWagon_original.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testTextPyData/GhostInWagon/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 55)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 55" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_GhostInWagon():
    print("--- test_GhostInWagon")

    elanXmlFilename = "../testTextPyData/GhostInWagon/GhostInWagon.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testTextPyData/GhostInWagon/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 55)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 55" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_Cuervo():
    print("--- test_Cuervo")

    elanXmlFilename = "../testTextPyData/Cuervo/newcuervo.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testTextPyData/Cuervo/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 207)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 207" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_Caterpillar():
    print("--- test_Caterpillar")

    elanXmlFilename = "../testTextPyData/Caterpillar/Caterpillar.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testTextPyData/Caterpillar/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 112)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 112" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_aym():
    print("--- test_aym")

    elanXmlFilename = "../testTextPyData/aym/aym-final.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testTextPyData/aym/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 145)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 145" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_AYAFW():
    print("--- test_AYAFW")

    elanXmlFilename = "../testTextPyData/AYAFW/AYAFW.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testTextPyData/AYAFW/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 77)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 77" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_praying():
    print("--- test_praying")

    elanXmlFilename = "../testData/praying/praying.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testData/praying/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 9)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 9" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_praying():
    print("--- test_praying")

    elanXmlFilename = "../testData/praying/praying.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testData/praying/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 9)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 9" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_loco():
    print("--- test_loco")

    elanXmlFilename = "../testData/loco/loco.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testData/loco/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 323)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 323" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_Inundación():
    print("--- test_Inundación")

    elanXmlFilename = "../testData/Inundación/Inundacion.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testData/Inundación/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 112)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 3" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_HMDLsafe():
    print("--- test_HMDLsafe")

    elanXmlFilename = "../testData/HMDLsafe/HMDL.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testData/HMDLsafe/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 4)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 3" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_featherSnake():
    print("--- test_featherSnake")

    elanXmlFilename = "../testData/featherSnake/featherSnake.eaf"
    audioFilename = "../testData/Cargos.ogg"
    targetDirectory = "../testData/featherSnake/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 15)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 3" % len(fileList))


# ----------------------------------------------------------------------------------------------------
def test_AYAMT():
    print("--- test_AYAMT")

    elanXmlFilename = "../testData/AYAMT/AYAMT.eaf"
    audioFilename = "../testData/AYAMT/AYAMT.ogg"
    targetDirectory = "../testData/AYAMT/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 41)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 3" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_aktzini():
    print("--- test_aktzini")

    elanXmlFilename = "../testData/aktzini/18-06-03Aktzini-GA.eaf"
    audioFilename = "../testData/aktzini/18-06-03Aktzini-GA.wav"
    targetDirectory = "../testData/aktzini/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 16)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 3" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_inferno():
    print("--- test_inferno")

    elanXmlFilename = "../testData/inferno-threeLines/inferno-threeLines.eaf"
    audioFilename = "../testData/inferno-threeLines/inferno-threeLines.wav"
    targetDirectory = "../testData/inferno-threeLines/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory, f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert (len(fileList) == 3)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 3" % len(fileList))

# ----------------------------------------------------------------------------------------------------
def test_inferno_plus():
    print("--- test_inferno_plus")

    elanXmlFilename = "../testData/test_alignable/inferno-threeLines_plus_one.eaf"
    audioFilename = "../testData/test_alignable/inferno-threeLines.wav"
    targetDirectory = "../testData/test_alignable/audio"
    fileList = os.listdir(targetDirectory)
    for f in fileList:
        target = os.path.join(targetDirectory,f)
        os.remove(target)
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()
    ae.extract()
    fileList = [f for f in os.listdir(targetDirectory) if not f.startswith('.')]
    try:
        assert(len(fileList) == 3)
        print("There is the correct number of audiophrases.")
    except AssertionError as e:
        print("Error: There are %d audiophrases rather than 3" %len(fileList))

# ----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    runTests()

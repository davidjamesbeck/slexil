import sys
# import base64
import xmlschema
from xml.etree import ElementTree as etree
sys.path.append("..")
from text import *
import os
from audioExtractor import AudioExtractor

# ----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)


# ----------------------------------------------------------------------------------------------------

def createText():
    audioFilename = "../testData/Cargos.ogg"
    print("--- testing normal file")
    elanXmlFilename = "../infernoDemo/inferno-threeLines.eaf"
    validFile = validate_EAF(elanXmlFilename)
    print("--- testing file with broken HTML tags")
    elanXmlFilename = "../testData/praying/Prayer_broken-HTML_tags.eaf"
    validFile = validate_EAF(elanXmlFilename)
    if not validFile:
        return False
    print("--- testing file with HTML tags")
    elanXmlFilename = "../testData/praying/Prayer_HTML_tags.eaf"
    validFile = validate_EAF(elanXmlFilename)
    if not validFile:
        print("=== failed to validate file with tags")
    targetDirectory = "../testData/praying/audio"
    soundFile = os.path.join(targetDirectory, "Cargos.ogg")
    projectDirectory = "../testData/praying"
    ae = AudioExtractor(audioFilename, elanXmlFilename, targetDirectory)
    ae.determineStartAndEndTimes()

    text = Text(elanXmlFilename,
                audioFilename,
                grammaticalTermsFile="../testData/praying/grammaticalTerms.txt",
                tierGuideFile="../testData/praying/tierGuide.yaml",
                projectDirectory=projectDirectory,
                quiet=True)
    return (text)

def validate_EAF(filename):
    print("--- testing %s" %filename)
    assert(os.path.isfile(filename))
    with open(filename, "r") as fp:
        # contents = fp.read()
        # data = contents.encode("utf8").split(b";base64,")[1]
        # fp.write(base64.decodebytes(data))
        fileSize = os.path.getsize(filename)
        print("eaf file size: %d" % fileSize)
        try:
            etree.parse(filename)
        except etree.ParseError as e:
            print("Invalid XML: %s" %e)
            return False
        schema = xmlschema.XMLSchema('http://www.mpi.nl/tools/elan/EAFv3.0.xsd')
        validXML = schema.is_valid(fp)
        eaf_validationMessage = "File %s (%d bytes) is valid XML." % (filename, fileSize)
        if (not validXML):
            try:
                schema.validate(filename)
            except xmlschema.XMLSchemaValidationError as e:
                failureReason = e.reason
                eaf_validationMessage = "Invalid EAF file: %s [File: %s]" % (failureReason, filename)
        print(eaf_validationMessage)
        return True
        # return eaf_validationMessage, filename

def runTests(display=False):
    test_for_HTML_tags(display)


def test_for_HTML_tags(display):
    print("--- test_for_HTML_tags")

    text = createText()
    if text == False:
        return
    assert (text.validInputs())
    tbl = text.getTierSummary()
    assert (tbl.shape == (4, 3))
    assert (list(tbl['key']) == ['speech', 'translation', 'morpheme', 'morphemeGloss'])
    assert (list(tbl['value']) == ['SZC-Chatino', 'English Translation-cp-cp', 'Tokenization-cp', 'POS-cp'])
    assert (list(tbl['count']) == [9, 9, 111, 111])

    htmlText = text.toHTML()
    # filename = "praying.html"
    # f = open(filename, "w")
    # f.write(indent(htmlText))
    # f.close()

    if (display):
        os.system("open %s" % filename)

if __name__ == '__main__':
    runTests()

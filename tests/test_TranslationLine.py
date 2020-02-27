# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------
# test_TranslationLine.pyt
#----------------------------------------------------------------------------------------------------
import sys
sys.path.append("..")
from translationLine import *
import re
from xml.etree import ElementTree as etree
import yaml
from ijalLine import IjalLine
#----------------------------------------------------------------------------------------------------
def runTests():
	"""
	  ensure we can handle all proper and improper translation lines
	  the eaf xml schema only requires that they be character strings
	  we require that each line
		- begins with a left curly single quote
		- ends with a right curly single quote
		- has no leading or trailing whitespace
	  we use the intentionally flawed text "praying_FaultyAuthorExamples" to collect all
	  the improper translation lines we imagine, or encounter over time, to ensure
	  that we can render them into our proper form
	"""
	from xml.etree import ElementTree as etree
	filename = "../testData/praying_FaultyAuthorExamples/praying.eaf"
	doc = etree.parse(filename)
	pattern = "TIER[@TIER_ID='English Translation-cp-cp']/ANNOTATION/REF_ANNOTATION/ANNOTATION_VALUE"
	childElements = doc.findall(pattern)
	assert(len(childElements) >= 9)
	cases = [element.text for element in childElements]
	for case in cases:
		translationLine = TranslationLine(case)
		standardizedLine = translationLine.getStandardized()
		print(standardizedLine)
		test_begins_and_ends_with_squo(standardizedLine)
		test_extraneous_whitespace(standardizedLine)
		test_punctuation_outside_quote(standardizedLine)
		test_straight_apostrophes(standardizedLine)
		test_straight_dquo(standardizedLine)
		test_thin_spaces(standardizedLine)

	test_loco_line_3()

#----------------------------------------------------------------------------------------------------
def test_begins_and_ends_with_squo(standardizedLine):
	'''makes sure the first and last character of the translation is a single quote'''

	try:
		assert(standardizedLine[0] == '‘' and standardizedLine[-1] == '’')
	except AssertionError as e:
		raise Exception(standardizedLine) from e
#----------------------------------------------------------------------------------------------------
def test_extraneous_whitespace(standardizedLine):
	'''checks to make sure author did not have whitespaces at either end of the translation line'''

	regex = re.compile(u'‘\u0020')   # opening curly single quote followed by whitespace
	assert(len(regex.findall(standardizedLine)) == 0)
	regex = re.compile(u'\u0020’')   # close curly single quote preceded by whitespace
	assert(len(regex.findall(standardizedLine)) == 0)

#----------------------------------------------------------------------------------------------------
def test_punctuation_outside_quote(standardizedLine):
	'''checks to make sure author did not have a punctuation mark outside a close quote'''

	regex = re.compile("’[\.,!?\)]’")   # punctuation preceded by rsquo
	assert(len(regex.findall(standardizedLine)) == 0)

#----------------------------------------------------------------------------------------------------
def test_straight_apostrophes(standardizedLine):
	'''checks to make sure author did not use straight apostrophes rather than squo'''

	regex = re.compile("‘'")   # initial straight apostrophe
	assert(len(regex.findall(standardizedLine)) == 0)
	regex = re.compile("'’")   # final straight apostrophe
	assert(len(regex.findall(standardizedLine)) == 0)

#----------------------------------------------------------------------------------------------------
def test_straight_dquo(standardizedLine):
	'''checks to make sure author did not use straight double quotes'''

	regex = re.compile('"')   # check for double quotes
	assert(len(regex.findall(standardizedLine)) == 0)

#----------------------------------------------------------------------------------------------------
def test_thin_spaces(standardizedLine):
	'''checks to make sure thin spaces separate quotes'''

	regex = re.compile('‘“')   # check for adjacent lsquo and ldquo
	regex2 = re.compile('”’')   # check for adjacent rsquo and rdquo
	try:
		assert(len(regex.findall(standardizedLine)) == 0)
		assert(len(regex2.findall(standardizedLine)) == 0)
	except AssertionError as e:
		raise Exception(standardizedLine) from e

#----------------------------------------------------------------------------------------------------
def test_loco_line_3():

	'''an illegal line: ‘[a] child, a woman as well.'’
	   note curly quotes at beginning and end, and a straight single quote (an apostrophe)
	   just before that closeing curly quote
	   we here ensure that the TranslationLine class detects and repairs this error
	'''

	print("--- test_loco_line_3")

	filename = "../testData/loco/loco.eaf"
	doc = etree.parse(filename)
	tierGuideFile = "../testData/loco/tierGuide.yaml"
	with open(tierGuideFile, 'r') as f:
	   tierGuide = yaml.safe_load(f)

	x3 = IjalLine(doc, 3, tierGuide,'a,b,c')
	x3.parse()

		# first, check that we get the illegal line back from the IjalLine class
		# we may need to disable this check once the TranslationLine class
		# is used throughout by IjalLine

	try:
		assert(x3.getTranslation() == "‘[@] ch@ld, @ w@m@n @s w@ll.’")
	except AssertionError as e:
		raise Exception(x3.getTranslation()) from e

		# now do our new processing
	translationLine = TranslationLine(x3.getTranslation())
	standardizedLine = translationLine.getStandardized()

		# check that the stray straight single quote has bee eliminated
		# try with both of python's standard string quotes, single and double straight quotes

	assert(standardizedLine == '‘[@] ch@ld, @ w@m@n @s w@ll.’')
	assert(standardizedLine == "‘[@] ch@ld, @ w@m@n @s w@ll.’")

#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	runTests()

import pandas as pd
from xml.etree import ElementTree as etree
from morphemeGloss import *
from pprint import pprint
from yattag import *
import pdb
import formatting
from translationLine import *
from errors import *
import logging
#------------------------------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------------------------------
class IjalLine:

	tierInfo = []
	spokenTextID = ""
	rootElement = None
	rootID = None
	tierElements = []
	doc = None
	lineNumber = None
	soundFile = None
	grammaticalTerms = None

	def __init__(self, doc, lineNumber, tierGuide, audioData, grammaticalTerms=[]):
		self.doc = doc
		self.lineNumber = lineNumber
		self.tierGuide = tierGuide
		self.audioData = audioData
		self.grammaticalTerms = grammaticalTerms
		self.rootElement = self.doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
		self.allElements = findChildren(self.doc, self.rootElement)
		self.tblRaw = buildTable(doc, self.allElements)
		self.tierCount = self.tblRaw.shape[0]

	def parse(self):
		if not self.tierCount >=2:
			 raise EmptyTiersError(self.lineNumber)
		self.tbl = standardizeTable(self.tblRaw, self.tierGuide)
		self.tbl.index = range(len(self.tbl.index))
		self.categories = categories = self.tbl["category"].tolist()
		self.speechRow = self.categories.index("speech")
#		print(self.lineNumber,self.speechRow)
		if 'translation' in self.categories:
			self.translationRow = self.categories.index("translation")
		else:
			self.translationRow = None
		tierCount = self.tbl.shape[0]
		# pdb.set_trace()
		self.morphemeRows = [i for i in range(tierCount) if self.categories[i] == "morpheme"]
		self.morphemeGlossRows = [i for i in range(tierCount) if self.categories[i] == "morphemeGloss"]
		#handle the case of a secondary translation
		if 'translation2' in self.categories:
			self.translation2Row = self.categories.index("translation2")
		else:
			self.translation2Row = None
		#handle the case of a second transcription line
		if 'transcription2' in self.categories:
			self.transcription2Row = self.categories.index("transcription2")
		else:
			self.transcription2Row = None
		self.morphemes = self.extractMorphemes()
		self.morphemeGlosses = self.extractMorphemeGlosses()
		self.calculateMorphemeSpacing()
		self.rootID = self.audioData.split(',')[0]#self.tbl.ix[self.speechRow, "ANNOTATION_ID"]

	def getTierCount(self):
		 return(self.getTable().shape[0])

	def getTable(self):
		return(self.tbl)

	def getStartTime(self):
                return(self.tbl.ix[self.speechRow]["START"])

	def getEndTime(self):
                return(self.tbl.ix[self.speechRow]["END"])

	#----------------------------------------------------------------------------------------------------
	def show(self):

		pprint(vars(self))

	#----------------------------------------------------------------------------------------------------
	def getSpokenText(self):

		#categories = self.tbl["category"].tolist()
		#row = categories.index("speech")
		return(self.tbl.ix[self.speechRow, "TEXT"])

	#----------------------------------------------------------------------------------------------------
	def getTranslation(self):

		#categories = self.tbl["category"].tolist()
		#row = categories.index("translation")
		# pdb.set_trace()
		if self.translationRow == None:
			logging.warning("missing translation at line %d" %(int(self.lineNumber) + 1))
			return(None)
		translation = self.tbl.ix[self.translationRow, "TEXT"]
		translationLine = TranslationLine(translation)
		return(translationLine.getStandardized())

	#----------------------------------------------------------------------------------------------------
	def getTranslation2(self):
		if self.translation2Row != None:
			translation2 = self.tbl.ix[self.translation2Row, "TEXT"]
			translationLine2 = TranslationLine(translation2)
			return(translationLine2.getStandardized())
		else:
			return(None)

	#----------------------------------------------------------------------------------------------------
	def getTranscription2(self):
		if self.transcription2Row != None:
			transcription2 = self.tbl.ix[self.transcription2Row, "TEXT"]
			return(transcription2)
		else:
			return(None)

	#----------------------------------------------------------------------------------------------------
	def extractMorphemes(self):

		if(self.morphemeRows == []):
			return([])

		rawMorphemeList = self.tbl["TEXT"].iloc[self.morphemeRows].tolist()
		rawMorphemes = ''.join(rawMorphemeList)
		if "\t" in rawMorphemes:
			 rawMorphemeText = self.tbl["TEXT"].iloc[self.morphemeRows].tolist()[0]
			 rawMorphemeList = rawMorphemeText.split('\t')

		morphemes = replaceHyphensWithNDashes(rawMorphemeList)
		return(morphemes)

	#----------------------------------------------------------------------------------------------------
	def extractMorphemeGlosses(self):

		if(self.morphemeGlossRows == []):
			return([])

		rawMorphemeGlossList = self.tbl["TEXT"].iloc[self.morphemeGlossRows].tolist()
		rawMorphemeGlosses = ''.join(rawMorphemeGlossList)
		if "\t" in rawMorphemeGlosses:
			 rawMorphemeGlossText = self.tbl["TEXT"].iloc[self.morphemeGlossRows].tolist()[0]
			 rawMorphemeGlossList = rawMorphemeGlossText.split('\t')

		morphemeGlosses = replaceHyphensWithNDashes(rawMorphemeGlossList)
		return(morphemeGlosses)

	#----------------------------------------------------------------------------------------------------
	def getMorphemes (self):

		return(self.morphemes)

	#----------------------------------------------------------------------------------------------------
	def getGrammaticalTerms(self,terms):
		try:
			if terms[-1] == '':
				terms = terms[:-1]
			return newTerms
		except IndexError:
			return

	#----------------------------------------------------------------------------------------------------
	def getMorphemeGlosses (self):

		return(self.morphemeGlosses)

	#----------------------------------------------------------------------------------------------------
	def calculateMorphemeSpacing(self):

		"""
		 the spacing is used to create a styleString, specifying grid cell widths which
		 accomodate the widest of each morpheme/gloss pair, so that they each member of
		 each pair is vertically aligned:
			 m1		m2		----m3-----
			 g1	---g2---		 g3
		"""
		morphemes = self.getMorphemes()
		glosses = self.getMorphemeGlosses()

		if (len(morphemes) > len(glosses)):
			logging.warning("EAF error: There are more morphs (%d) than glosses (%d) in line %s." %(len(morphemes),len(glosses),int(self.lineNumber)+1))
			theDifference = len(morphemes) - len(glosses)
			for i in range(0,theDifference):
				glosses.append("⚠️")
# 			raise TooManyMorphsError(self.lineNumber,len(morphemes),len(glosses))
		elif (len(morphemes) < len(glosses)):
			logging.warning("EAF error: There are more glosses (%d) than morphs (%d) in line %s." %(len(glosses),len(morphemes),int(self.lineNumber)+1))
			theDifference = len(glosses) - len(morphemes)
			for i in range(0,theDifference):
				morphemes.append("⚠️")
# 			raise TooManyGlossesError(self.lineNumber,len(morphemes),len(glosses))

		self.morphemeSpacing = []

		for i in range(len(morphemes)):
			if "<su" in morphemes[i]:
				newmorph = morphemes[i].replace("<sub>","")
				newmorph = newmorph.replace("</sub>","")
				newmorph = newmorph.replace("<sup>","")
				newmorph = newmorph.replace("</sup>","")
				morphemeSize = len(newmorph)
			else:
				morphemeSize = len(morphemes[i])
			if "<su" in glosses[i]:
				newGloss = glosses[i].replace("<sub>","")
				newGloss = newGloss.replace("</sub>","")
				newGloss = newGloss.replace("<sup>","")
				newGloss = newGloss.replace("</sup>","")
				glossSize = len(newGloss)
			else:
				glossSize = len(glosses[i])
			self.morphemeSpacing.append(max(morphemeSize, glossSize) + 1)

	#----------------------------------------------------------------------------------------------------
	def getMorphemeSpacing(self):

		 return(self.morphemeSpacing)

	#----------------------------------------------------------------------------------------------------
	def htmlLeadIn(self, htmlDoc, audioDirectory):

		text = "%d)" % (self.lineNumber + 1)
		htmlDoc.text(text)
		lineID = self.rootID
		audioTag = '<audio id="a%s"><source src="%s/a%s.wav"/></audio>' % (lineID, audioDirectory, lineID)
		htmlDoc.asis(audioTag)
#		 imageURL = "https://www.americanlinguistics.org/wp-content/uploads/speaker.png"
		onError = "this.style.display=\'none\'"
		buttonTag = '<button onclick="playSample(\'a%s\')">🔈</button>' % (lineID)
		#buttonTag = '<button onclick="playSample(\'%s\')"><img src="%s"/></button>' % (lineID, self.getSpeakerImage())
		htmlDoc.asis(buttonTag)


	#----------------------------------------------------------------------------------------------------
	def toHTML(self, htmlDoc):

			with htmlDoc.tag("div", klass="line-content"):
				with htmlDoc.tag("div", klass="line"):
					 styleString = "grid-template-columns: %s;" % ''.join(["%dch " % p for p in self.morphemeSpacing])
					 with htmlDoc.tag("div", klass="speech-tier"):
							htmlDoc.asis(self.getSpokenText())

							transcription2 = self.getTranscription2()
							if transcription2 != None:
								with htmlDoc.tag("div", klass="secondTranscription-tier"):
									htmlDoc.asis(self.getTranscription2())

							morphemes = self.getMorphemes()
							#print(morphemes)
							if(len(morphemes) > 0):
								with htmlDoc.tag("div", klass="morpheme-tier", style=styleString):
									for morpheme in morphemes:
										#print(morpheme)
										with htmlDoc.tag("div", klass="morpheme-cell"):
											htmlDoc.asis(morpheme)

							morphemeGlosses = self.getMorphemeGlosses()
							if(len(morphemeGlosses) > 0):
								with htmlDoc.tag("div", klass="morpheme-tier", style=styleString):
									for morphemeGloss in self.getMorphemeGlosses():
										with htmlDoc.tag("div", klass="morpheme-cell"):
											mg = MorphemeGloss(morphemeGloss, self.grammaticalTerms)
											mg.parse()
											mg.toHTML(htmlDoc)

							translation = self.getTranslation()
							if translation:
								with htmlDoc.tag("div", klass="freeTranslation-tier"):
									htmlDoc.asis(self.getTranslation())

							translation2 = self.getTranslation2()
							if translation2 != None:
								with htmlDoc.tag("div", klass="freeTranslation-tier"):
									 htmlDoc.text(translation2)


#------------------------------------------------------------------------------------------------------------------------
def findChildren(doc, rootElement):

	elementsToDo = [rootElement]
	elementsCompleted = []

	while(len(elementsToDo) > 0):
		currentElement = elementsToDo[0]
		parentRef = currentElement.attrib["ANNOTATION_ID"]
		pattern = "TIER/ANNOTATION/REF_ANNOTATION[@ANNOTATION_REF='%s']" % parentRef
		childElements = doc.findall(pattern)
		elementsToDo.remove(currentElement)
		elementsCompleted.append(currentElement)
		if(len(childElements) > 0):
			elementsToDo.extend(childElements)

	return(elementsCompleted)

#------------------------------------------------------------------------------------------------------------------------
def buildTable(doc, lineElements):

	tbl_elements = pd.DataFrame(e.attrib for e in lineElements)
	#print(tbl_elements)

	#pdb.set_trace()
	startTimeSlotID = tbl_elements.ix[0, 'TIME_SLOT_REF1']
	pattern = "TIME_ORDER/TIME_SLOT[@TIME_SLOT_ID='%s']" % startTimeSlotID
	startTime = int(doc.find(pattern).attrib["TIME_VALUE"])
	startTimes = [startTime]
	rowCount = tbl_elements.shape[0]
	for i in range(1, rowCount):
		startTimes.append(float('NaN'))

	endTimeSlotID	= tbl_elements.ix[0, 'TIME_SLOT_REF2']
	pattern = "TIME_ORDER/TIME_SLOT[@TIME_SLOT_ID='%s']" % endTimeSlotID
	endTime = int(doc.find(pattern).attrib["TIME_VALUE"])
	endTimes = [endTime]
	for i in range(1, rowCount):
		endTimes.append(float('NaN'))
	tbl_times = pd.DataFrame({"START": startTimes, "END": endTimes})
	#print(tbl_times)


	ids = [e.attrib["ANNOTATION_ID"] for e in lineElements]
	tierInfo = []
	text = []

	for id in ids:
		parentPattern = "*/*/*/[@ANNOTATION_ID='%s']/../.." % id
		tierAttributes = doc.find(parentPattern).attrib
		tierInfo.append(tierAttributes)
		childPattern = "*/*/*/[@ANNOTATION_ID='%s']/ANNOTATION_VALUE" % id
		elementText = doc.find(childPattern).text
		if(elementText is None):
			elementText = ""
		#print("elementText: %s" % elementText)
		text.append(elementText.strip())

	tbl_tierInfo = pd.DataFrame(tierInfo)

	tbl_text = pd.DataFrame({"TEXT": text})

	# print("---- tbl_elements")
	# print(tbl_elements)
	#
	# print("---- tbl_tierInfo")
	# print(tbl_tierInfo)
	#
	# print("---- tbl_times")
	# print(tbl_times)
	#
	# print("---- tbl_text")
	# print(tbl_text)

	tbl = pd.concat([tbl_elements, tbl_tierInfo, tbl_times, tbl_text], axis=1)
	preferredColumnOrder = ["ANNOTATION_ID", "LINGUISTIC_TYPE_REF", "START", "END", "TEXT", "ANNOTATION_REF", "TIME_SLOT_REF1", "TIME_SLOT_REF2",
									"PARENT_REF", "TIER_ID"]
	tbl = tbl[preferredColumnOrder]
	textLengths = [len(t) for t in tbl["TEXT"].tolist()]
	tbl["TEXT_LENGTH"] = textLengths
	hasTabs = ["\t" in t for t in tbl["TEXT"].tolist()]
	tbl["HAS_TABS"] = hasTabs
	hasSpaces = [" " in t for t in tbl["TEXT"].tolist()]
	tbl["HAS_SPACES"] = hasSpaces
		# eliminate rows with no text
		# leave it in for now, take the tiers at face value, handle empty lines in toHTML
	tbl = tbl.query("TEXT != ''").reset_index(drop=True)
	return(tbl)

#------------------------------------------------------------------------------------------------------------------------
def standardizeTable(tbl, tierGuide):

	tierNames = tbl["TIER_ID"].tolist()
	permittedNames = [tierGuide[k] for k in tierGuide]
	shared = set(tierNames).intersection(permittedNames)

	tbl_trimmed = tbl.loc[tbl['TIER_ID'].isin(shared)]

	tierNames = tbl_trimmed["TIER_ID"].tolist()

		# reverse the guide so we can map from user-supplied and often idiosyncratic
		# TIER_ID values, to the IJAL standard types: speech, translation, morpheme, morphemeGloss

	revGuide = {v: k for k, v in tierGuide.items()}
	ids = tbl_trimmed["TIER_ID"]
	standardIDs = [revGuide[key] for key in ids]

		# add a new column to the table.  we will use this later to assemble the html
	tbl_final = tbl_trimmed.assign(category=standardIDs)

	return(tbl_final)

#------------------------------------------------------------------------------------------------------------------------
def replaceHyphensWithNDashes(list):
		''' replace hyphens with n-dashes
		'''
		newList = []
		for text in list:
			text = text.replace('-','–')
			newList.append(text)
		return(newList)

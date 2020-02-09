# learn the tier ID names used by the recording linguist to identify the four
# crucial tiers, put them into the text's tierGuide.yaml file
#
# speech:
# translation:
# morpheme:
# morpehemGloss:
# morphemePacking: tabs|tiers
#
filename = "../testData/harryMosesDaylight/daylight_1_4.eaf"
xmlDoc = etree.parse(filename)
x = Line(xmlDoc, lineNumber=0, tierGuide=None, grammaticalTerms=[])
x.tblRaw["TIER_ID"].tolist()

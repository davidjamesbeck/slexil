# learn the tier ID names used by the recording linguist to identify the four
# crucial tiers, put them into the text's tierGuide.yaml file
#
# speech:
# translation:
# morpheme:
# morpehemGloss:
# morphemePacking: tabs|tiers
#
import sys
sys.path.append("..")
from xml.etree import ElementTree as etree
from ijalLine import IjalLine as Line

filename = "../testData/HMDLsafe/HMDL.eaf"
xmlDoc = etree.parse(filename)
x = Line(xmlDoc, lineNumber=0, tierGuide=None, grammaticalTerms=[])
x.tblRaw["TIER_ID"].tolist()

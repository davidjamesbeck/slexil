import pandas as pd
from xml.etree import ElementTree as etree


class DataFrame:

    def __init__(self, doc, allElements, tierGuide):
        self.doc = doc
        self.allElements = allElements
        self.tierGuide = tierGuide
        self.speechTier = self.tierGuide["speech"]

        self.tbl = buildTable(doc,self.allElements)

    def buildTable(doc, lineElements):
        tbl_elements = pd.DataFrame(e.attrib for e in lineElements)
        # print(tbl_elements)

        startTimeSlotID = tbl_elements.iloc[0, tbl_elements.columns.values.tolist().index('TIME_SLOT_REF1')]
        pattern = "TIME_ORDER/TIME_SLOT[@TIME_SLOT_ID='%s']" % startTimeSlotID
        startTime = int(doc.find(pattern).attrib["TIME_VALUE"])
        startTimes = [startTime]
        rowCount = tbl_elements.shape[0]
        for i in range(1, rowCount):
            startTimes.append(float('NaN'))

        endTimeSlotID = tbl_elements.iloc[0, tbl_elements.columns.values.tolist().index('TIME_SLOT_REF2')]
        pattern = "TIME_ORDER/TIME_SLOT[@TIME_SLOT_ID='%s']" % endTimeSlotID
        endTime = int(doc.find(pattern).attrib["TIME_VALUE"])
        endTimes = [endTime]
        for i in range(1, rowCount):
            endTimes.append(float('NaN'))
        tbl_times = pd.DataFrame({"START": startTimes, "END": endTimes})
        # print(tbl_times)

        ids = [e.attrib["ANNOTATION_ID"] for e in lineElements]
        tierInfo = []
        text = []

        for id in ids:
            parentPattern = "*/*/*/[@ANNOTATION_ID='%s']/../.." % id
            tierAttributes = doc.find(parentPattern).attrib
            tierInfo.append(tierAttributes)
            childPattern = "*/*/*/[@ANNOTATION_ID='%s']/ANNOTATION_VALUE" % id
            elementText = doc.find(childPattern).text
            if (elementText is None):
                elementText = ""
            # print("elementText: %s" % elementText)
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
        preferredColumnOrder = ["ANNOTATION_ID", "LINGUISTIC_TYPE_REF", "START", "END", "TEXT", "ANNOTATION_REF",
                                "TIME_SLOT_REF1", "TIME_SLOT_REF2",
                                "PARENT_REF", "TIER_ID"]
        try:
            tbl = tbl[preferredColumnOrder]
        except KeyError:
            preferredColumnOrder = ["ANNOTATION_ID", "LINGUISTIC_TYPE_REF", "START", "END", "TEXT",
                                    "TIME_SLOT_REF1", "TIME_SLOT_REF2", "TIER_ID"]
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
        return (tbl)


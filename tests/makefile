all: morphemeGloss ijalLine audioExtractor text_daylight text_monkeyAndThunder  text_PlumedSerpent text_prayer test_chatino5 test_chatino6 test_Text_6_line test_Text test_TranslationLine text_lokono test_TextPy test_text_Halkomelem test_XML_schema test_aktzini


morphemeGloss:
	python3 test_MorphemeGloss.py

ijalLine:
	python3 test_IjalLine.py

audioExtractor:
	python3 test_AudioExtractor.py
	python3 test_startStopTable.py
	python3 test_Audio_formats.py

text_monkeyAndThunder:
	python3 test_text_MonkeyAndThunder.py

text_daylight:
	python3 test_text_HowDaylightWasStolen.py

text_PlumedSerpent:
	python3 test_text_PlumedSerpent.py

text_prayer:
	python3 test_text_prayer.py

text_inferno:
	python3 test_text_inferno.py

# takes several minutes to run, but a worthwhile test, now not run out of the "all" target above
text_lokono:
	python3 test_text_lokono.py

test_chatino5:
	python3 test_text_Chatino_5Line.py

test_chatino6:
	python3 test_text_Chatino_6Line.py

test_Text_6_line:
	python3 test_Text_6_line.py

test_Text:
	python3 test_Text.py

test_TranslationLine:
	python3 test_TranslationLine.py

test_TextPy:
	python3 ../testTextPy/test_TextPy.py

test_text_Halkomelem:
	python3 test_text_Halkomelem.py

test_XML_schema:
	python3 test_XML_schema.py

test_aktzini
    python3 test_text_aktzini.py

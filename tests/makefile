all: morphemeGloss ijalLine audioExtractor text_HDWS text_AYAMT text_featherSnake text_praying test_chatino5 test_chatino6 test_Text_6_line test_Text test_TranslationLine text_loco test_TextPy test_text_Halkomelem test_XML_schema test_aktzini


morphemeGloss:
	python3 test_MorphemeGloss.py

ijalLine:
	python3 test_IjalLine.py
	python3 learnTierStructure.py

audioExtractor:
	python3 test_AudioExtractor.py
	python3 test_startStopTable.py
	python3 test_Audio_formats.py
	python3 test_startStopTable.py

text_AYAMT:
	python3 test_text_AYAMT.py

text_HDWS:
	python3 test_text_HDWS.py

text_featherSnake:
	python3 test_text_featherSnake.py

text_praying:
	python3 test_text_praying.py

text_inferno:
	python3 test_text_inferno.py

# takes several minutes to run, but a worthwhile test, now not run out of the "all" target above
text_loco:
	python3 test_text_loco.py

test_chatino5:
	python3 test_text_praying_5Line.py

test_chatino6:
	python3 test_text_praying_6Line.py

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

test_aktzini:
	python3 test_text_aktzini.py

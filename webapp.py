import datetime
import base64
import pdb
import xmlschema
import os
import scipy.io.wavfile as wavfile
import dash
import pandas as pd
import dash_table
import yaml
import io
import webbrowser
from flask import Flask
import flask
from textwrap import dedent
from zipfile import *
from shutil import copy
#----------------------------------------------------------------------------------------------------
import sys
#sys.path.append("../ijal_interlinear")
from audioExtractor import *
from text import *
#----------------------------------------------------------------------------------------------------
UPLOAD_DIRECTORY = "UPLOADS"
PROJECTS_DIRECTORY = "PROJECTS"
#----------------------------------------------------------------------------------------------------
# the webapp requires a PROJECTS_DIRECTORY in the current working directory.  this is
#
assert(os.path.exists(PROJECTS_DIRECTORY))
#----------------------------------------------------------------------------------------------------
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, static_folder='PROJECTS')
app.config['suppress_callback_exceptions'] = True
app.title = "IJAL Text Upload"

app.scripts.config.serve_locally = True

#------------------------------------------------------------------------------------------------------------------------
# this route handles the download of zipped up "demo input" zip file,
# in this case, infernoDemo.zip, which a new slexil user can run through the webapp to
# learn the ropes
# we may want to further qualify the route path to something like '/demos/<filename>'
# for better separation in the slexil webapp direcotry structure
#----------------------------------------------------------------------------------------------------
@app.server.route('/demos/<filename>')
def downloadZip(filename):
    path = os.path.join("demos", filename)
    return flask.send_file(path,
                           mimetype='application/zip',
                           as_attachment=True)



#----------------------------------------------------------------------------------------------------
# this route handles the download of zipped up assembled slexil projects
# which, by convention, are  ./PROJECTS/<someName>/webpage.zip:
#    PROJECTS/daylight/webpage.zip
#    PROJECTS/lokono/webpage.zip
# we do not actually do the assembly here in this demo exploratory app. instead an appropriate
# file has been placed, ahead of time, in the appropriate directory.
#----------------------------------------------------------------------------------------------------
@app.server.route('/PROJECTS/<path:urlpath>')
def downloadProjectZipFile(urlpath):
   print("--- serve_static_file")
   print("urlpath:  %s" % urlpath)
   fullPath = os.path.join("PROJECTS", urlpath)
   dirname = os.path.dirname(fullPath)
   filename = os.path.basename(fullPath)
   print("about to send %s, %s" % (dirname, filename))
   return flask.send_file(fullPath,
                          mimetype='application/zip',
                          as_attachment=True)


# @app.server.route('/PROJECTS/<path:urlpath>')
# def serve_static_file(urlpath):
#    print("--- serve_static_file")
#    print("urlpath:  %s" % urlpath)
#    fullPath = os.path.join("PROJECTS", urlpath)
#    dirname = os.path.dirname(fullPath)
#    filename = os.path.basename(fullPath)
#    print("about to send %s, %s" % (dirname, filename))
#    return flask.send_from_directory(dirname, filename)
#

buttonStyle = {'width': '140px',
               'height': '60px',
               'color': 'gray',
               'fontFamily': 'HelveticaNeue',
               'margin-right': 10,
               'lineHeight': '60px',
               'borderWidth': '1px',
               'borderStyle': 'solid',
               'borderRadius': '5px',
               'textAlign': 'center',
               'text-decoration': 'none',
               'display': 'inline-block'
               }
disabledButtonStyle = buttonStyle
disabledButtonStyle["disabled"] = True
#----------------------------------------------------------------------------------------------------
def create_eafUploader():

    uploader = dcc.Upload(id='upload-eaf-file',
                          children=html.Div([html.A('Select File', className='button')]),
                          multiple=False,
                          style={'display': 'inline-block'})

    return uploader

#----------------------------------------------------------------------------------------------------
def create_setTitleTab():

##   style = {'border': '5px solid purple',
##            'border-radius': '5px',
##            'padding': '10px'}

   setTitleInput = dcc.Input(id="setTitleTextInput",
                         placeholder='enter convenient, concise text title here, no spaces please!',
                         value="",
                         style={'width': '512px', 'fontSize': 20})

   setTitleButton = html.Button(id='setTitleButton', type='submit', children='Submit',className="button")

   children = [html.Br(),
               setTitleInput,
               html.Br(),
               html.Br(),
               setTitleButton
               #tierIDsBlankDiv
               ]

   div = html.Div(children=children, id='setTitleDiv')

   return div

#----------------------------------------------------------------------------------------------------
def create_eafUploaderTab():

#    style = {'border': '5px solid purple',
#             'border-radius': '5px',
#             'padding': '10px'}

   textArea = dcc.Textarea(id="eafUploadTextArea",
                           placeholder='xml validation results go here',
                           value="",
                           style={'width': 600, 'height': 300})

   children = [html.Br(),
               html.Div([create_eafUploader()],
                        style={'display': 'inline-block'}),
               html.Br(),
               html.Br(),
               textArea
               ]

   div = html.Div(children=children, id='eafUploaderDiv') #, style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_soundFileUploader():

    uploader = dcc.Upload(id='upload-sound-file',
                          children=html.Div([html.A('Select File', className='button')]),
                          multiple=False,
                          style={'display': 'inline-block'})

    return uploader

#----------------------------------------------------------------------------------------------------
def create_soundFileUploaderTab():

#    style = {'border': '5px solid purple',
#             'border-radius': '5px',
#             'padding': '10px'}

   textArea = dcc.Textarea(id="soundFileUploadTextArea",
                           placeholder='sound file validation results go here',
                           value="",
                           style={'width': 600, 'height': 300})

   children = [html.Br(),
               html.Div([create_soundFileUploader()],
                        style={'display': 'inline-block'}),
               html.Br(),
               html.Br(),
               textArea
               ]

   div = html.Div(children=children, id='soundFileUploaderDiv')

   return div

#----------------------------------------------------------------------------------------------------
def create_grammaticalTermsUploaderTab():

#    style = {'border': '5px solid purple',
#             'border-radius': '5px',
#             'padding': '10px'}

   textArea = dcc.Textarea(id="grammaticalTermsUploadTextArea",
                           placeholder='grammatical terms will be displayed here',
                           value="",
                           style={'width': 600, 'height': 300})

   button =  html.Button('No Grammatical Terms', id='noGrammaticalTermsButton', style={"margin": "20px"})

   children = [html.Br(),
               button,
               html.Div([create_grammaticalTermsFileUploader()],
                        style={'display': 'inline-block'}),
               html.Br(),
               html.Br(),
               textArea
               ]

   div = html.Div(children=children, id='grammaticalTermsFileUploaderDiv')

   return div

#----------------------------------------------------------------------------------------------------
def create_grammaticalTermsFileUploader():

    uploader = dcc.Upload(id='upload-grammaticalTerms-file',
                          children=html.Div([html.A('Select File', className='button')]),
                          multiple=False,
                          style={'display': 'inline-block'})

    return uploader

#----------------------------------------------------------------------------------------------------
def create_associateEAFandSoundTab():

#    style = {'border': '5px solid purple',
#             'border-radius': '5px',
#             'padding': '10px'}

   button =  html.Button('Extract Sounds By Phrase', id='extractSoundsByPhraseButton', style={"margin": "20px"})

   textArea = dcc.Textarea(id="associateEAFAndSoundInfoTextArea",
                           placeholder='eaf + soundFile',
                           value="",
                           style={'width': 600, 'height': 300})

   children = [html.Br(), button, html.Br(), textArea]

   div = html.Div(children=children, id='associateEAFandSoundDiv', style={'display': 'block'})

   return div

#----------------------------------------------------------------------------------------------------
def create_webPageCreationTab():

#    style = {'border': '5px solid purple',
#             'border-radius': '5px',
#             'padding': '10px'}

   #createButton =  html.Button('Create Web Page', id='createWebPageButton', style={"margin": "20px", "margin-top": 0})
   createAndDisplayButton =  html.Button('Create & Display', id='createAndDisplayWebPageButton',
                                         style={"margin": "20px", "margin-top": 0})

   #displayButton =  html.Button('Display Web Page', id='displayIJALTextButton', style={"margin": "20px", "margin-top": 0})
   downloadLinkAndButton = html.A(id="downloadURL",
                                  children=[html.Button('Download newly assembled text',
                                                        id="downloadAssembledTextButton",
                                                        style={"width": 300})], # ,disabled="False")],
                                  href='')

   createWebpageStatus = html.Span(id="createWebPageStatus", children="cwpita", style={'display': 'none'})

   webPageIframe = html.Iframe(id="storyIFrame", src="<h3>the story goes here</h3>", width=1200, height=800)

##   saveWebpageStatus = html.Span(id="saveWebpageProgressTextArea", children="Creating webpage display")
##                                              #placeholder='progress info will appear here',
##                                              #alue="",
##                                              #style={'width': 600, 'height': 30})

   confirmDownLoadObject = dcc.ConfirmDialogProvider(
        children=html.Button('Save...'),
        id='confirmDownLoadObject',
        message='Save HTML, audio, JavaSCript, and CSS to your local computer?'
    )

   buttonDiv = html.Div(children=[createAndDisplayButton, downloadLinkAndButton],
                        style={'display': 'flex', 'justify-content': 'left'})

   children = [html.Br(), buttonDiv,
               html.Br(), createWebpageStatus,
               html.Br(), webPageIframe]
               #html.Br(), saveWebpageStatus, webPageIframe]

   div = html.Div(children=children, id='createWebPageDiv')

   return div

#----------------------------------------------------------------------------------------------------
def create_masterDiv():
   '''appears not to be in use'''

   style = {'border': '1px solid green',
            'border-radius': '5px',
            'padding': '10px'}

   title = html.H4("Status")
   eafStatus = html.Label("EAF: ", id="eafStatusLabel", style={"font-size": 14})
   soundStatus = html.Label("Sound: ")
   tierMapStatus = html.Label("Tier map: ")
   grammaticalTermsStatus = html.Label("Grammatical terms: ")
   run_button = html.Button("Run", className='button')

   children = [title, eafStatus, soundStatus, tierMapStatus, grammaticalTermsStatus,
               html.Br(), run_button]

   div = html.Div(children=children, id='master-div', className="four columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_tierMapGui():

#    style = {'border': '1px solid purple',
#             'border-radius': '5px',
#             'padding': '10px'}

   helpText = dcc.Markdown(dedent('''There are four standard interlinear tiers.'''))

   helpTextDisplay = html.Div(children=helpText,
                        style={'margin': 100,
                               'margin-top': 10,
                               'margin-bottom': 10,
                               'border': '1px solid gray',
                               'border-radius': 5,
                               'padding': 20,
                               'width': "80%"})

   dropDownMenus = html.Div(id="tierMappingMenus")

   submitInteractiveTierMapButton =  html.Button("Submit", className='button', id="submitInteractiveTierMapButton")

   textArea = dcc.Textarea(id='writeTierGuideFileTextArea',
                           placeholder='tier guide write status goes here',
                           value="",
                           style={'width': 600, 'height': 50})

   div = html.Div(children=[helpTextDisplay,
                            dropDownMenus,
                            submitInteractiveTierMapButton,
                            html.Br(),
                            textArea],
                  id='tierMapGui-div', className="twelve columns") #, style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_allDivs():

   children = [
       html.H4("", className="banner", id='pageTitleH4'),
       html.Div(create_introduction(), className="introduction"),
       html.Details([html.Summary('Set Title',className="summary"), html.Div(create_setTitleTab())], className="allDivs"),
       html.Details([html.Summary('EAF',className="summary"), html.Div(create_eafUploaderTab())], className="allDivs"),
       html.Details([html.Summary('Sound',className="summary"), html.Div(create_soundFileUploaderTab())], className="allDivs"),
       html.Details([html.Summary('Tier Guide',className="summary"), html.Div(create_tierMapGui())], className="allDivs"),
       html.Details([html.Summary('GrammaticalTerms',className="summary"), html.Div(create_grammaticalTermsUploaderTab())], className="allDivs"),
       html.Details([html.Summary('EAF+Sound',className="summary"), html.Div(create_associateEAFandSoundTab())], className="allDivs"),
       html.Details([html.Summary('Create Web Page',className="summary"), html.Div(create_webPageCreationTab())], className="allDivs")]

   div = html.Div(children=children, id='main-div', className="mainDiv")

   return div

#----------------------------------------------------------------------------------------------------
def create_introduction():

   text = ("SLEXIL is software for preparing animated HTML files from texts prepared "
           "in ELAN. Users can use this site to upload the .eaf and .wav portions of "
           "ELAN projects and download an HTML file and accompanying CSS, JavaScript, "
           "and parsed audio files that can be embedded on a webpage or viewed in a "
           "browser on any computer. There is a video tutorial on YouTube and you can "
           "download a demo by clicking on the button to the right.")

   cell1 = html.Td(text,className='introduction')
   cell2 = html.Td(html.A(html.Button('Download Demo',className='button'),href='demos/infernoDemo.zip'),className="buttonCell")
   row = [html.Tr(children=[cell1,cell2])]

   div = html.Table(children=row, id='preamble')

   return div
#----------------------------------------------------------------------------------------------------
def create_tierMapDiv():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   children = [html.Label('tierMapDiv'),
               html.Label('tierMap upload'),
               html.Label('tierMap display')]

   div = html.Div(children=children, id='tierMap-div', className="three columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
#  tmpDoc = etree.parse(filename)
#  tierIDs = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
#  print(tierIDs)
def createPulldownMenu(menuName, tierChoices):

   options = []
   for item in tierChoices:
       newElement={"label": item, "value": item}
       options.append(newElement)

   idName = "tierGuideMenu-%s" % menuName
   menu = dcc.Dropdown(options=options, clearable=False, id=idName, className="tierMenuPulldown")
   return(menu)

#----------------------------------------------------------------------------------------------------
def createTierMappingMenus(eafFilename):

   print("--- createTierMappingMenus: %s [exists: %s]" % (eafFilename, os.path.exists(eafFilename)))
   dropDownMenus = html.H5("failure in extracting tierIDs from %s" % eafFilename)

   if(os.path.exists(eafFilename)):
      tmpDoc = etree.parse(eafFilename)
      userProvidedTierNamesToAssignToStandardTiers = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
      print(userProvidedTierNamesToAssignToStandardTiers)

      tierChoices = userProvidedTierNamesToAssignToStandardTiers
      #tierChoices = ["pending EAF file selection"]

      dropDownMenus = html.Table(id='tierMappingMenus', children=[
         html.Tr([html.Th("Standard interlinear tiers",className="first"), html.Th("",className="second"), html.Th("User tier names (from EAF file)",className="third")]),
         html.Tr([html.Td("line"), html.Td("i'ktzó'hli'"), html.Td(createPulldownMenu("speech", tierChoices))]),
         html.Tr([html.Td("alternate transcription"), html.Td("ḭktsó̰ʔlḭ"), html.Td(createPulldownMenu("transcription2", tierChoices))]),
         html.Tr([html.Td("morphological analysis"), html.Td("ḭk–tso̰ʔ–lḭ̰"), html.Td(createPulldownMenu("morpheme", tierChoices))]),
         html.Tr([html.Td("morpheme glosses"), html.Td(children=[
             html.Div("1sg.sub–",style={'font-variant':'small-caps','display':'inline-block'}),
             html.Div("write",style={'display':'inline-block'}),
             html.Div("–pfv",style={'font-variant':'small-caps','display':'inline-block'})]), html.Td(createPulldownMenu("morphemeGloss", tierChoices))]),
         html.Tr([html.Td("translation"), html.Td("‘I wrote it.’"), html.Td(createPulldownMenu("translation", tierChoices))]),
         html.Tr([html.Td("second translation"), html.Td("‘Lo escribí.’"), html.Td(createPulldownMenu("translation2", tierChoices))]),
         html.Tr([html.Td("morphemePacking"), html.Td(""), html.Td(createPulldownMenu("morphemePacking", ["tabs", "lines"]))])
         ], className="tiermap"
         )

   saveTierMappingChoicesButton = html.Button('Save Choices', id='saveTierMappingSelectionsButton',
                                       style={"margin-left": 100, "margin-top": 10, "margin-bottom": 20})

   tierMappingChoicesResultDisplay = html.Span(id="tierMappingChoicesResultDisplay", children="tmcrd",
                                               style={"border": 1, "margin-left": 10})
   enclosingDiv = html.Div(children=[dropDownMenus, saveTierMappingChoicesButton, tierMappingChoicesResultDisplay])
   #return dropDownMenus
   return(enclosingDiv)

#----------------------------------------------------------------------------------------------------
def create_grammaticalTermsDiv():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   children = [html.Label('grammaticalTermsDiv'),
               html.Label('grammaticalTerms upload'),
               html.Label('grammaticalTerms display')]

   div = html.Div(children=children, id='grammaticalTerms-div', className="three columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
def parse_eaf_upload(contents, filename, date):

   print("filename selected: %s" % filename)
   #pdb.set_trace()
   content_type, content_string = contents.split(',')
   nchar = len(content_string)
   print("%s (%s): %d characters" % (filename, content_type, nchar))
   return(nchar)

#----------------------------------------------------------------------------------------------------
app.layout = html.Div(
    children=[
        create_allDivs(),
        html.P(id='projectTitle_hiddenStorage',              children="", style={'display': 'none'}),
        html.P(id='projectDirectory_hiddenStorage',          children="", style={'display': 'none'}),
        html.P(id='eaf_filename_hiddenStorage',              children="", style={'display': 'none'}),
        html.P(id='sound_filename_hiddenStorage',            children="", style={'display': 'none'}),
        html.P(id='audioPhraseDirectory_hiddenStorage',      children="", style={'display': 'none'}),
        html.P(id='grammaticalTerms_filename_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='tierGuide_filename_hiddenStorage',        children="", style={'display': 'none'}),
        html.P(id='speechTier_hiddenStorage',                children="", style={'display': 'none'}),
        html.P(id='transcription2Tier_hiddenStorage',        children="", style={'display': 'none'}),      
        html.P(id='morphemeTier_hiddenStorage',              children="", style={'display': 'none'}),
        html.P(id='morphemeGlossTier_hiddenStorage',         children="", style={'display': 'none'}),       
        html.P(id='translationTier_hiddenStorage',           children="", style={'display': 'none'}),
        html.P(id='translation2Tier_hiddenStorage',          children="", style={'display': 'none'}),
        html.P(id='morphemePacking_hiddenStorage',           children="", style={'display': 'none'}),
        ],
    className="row",
    id='outerDiv'
    )

#----------------------------------------------------------------------------------------------------
@app.callback(Output('eafUploadTextArea', 'value'),
              [Input('upload-eaf-file', 'contents')],
              [State('upload-eaf-file', 'filename'),
               State('upload-eaf-file', 'last_modified'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_eafUpload(contents, name, date, projectDirectory):
    if name is None:
        return("")
    print("on_eafUpload, name: %s" % name)
    data = contents.encode("utf8").split(b";base64,")[1]
    filename = os.path.join(projectDirectory, name)
    with open(filename, "wb") as fp:
         fp.write(base64.decodebytes(data))
         fileSize = os.path.getsize(filename)
         print("eaf file size: %d" % fileSize)
         schema = xmlschema.XMLSchema('http://www.mpi.nl/tools/elan/EAFv3.0.xsd')
         validXML = schema.is_valid(filename)
         eaf_validationMessage = "%s: (%d bytes), valid XML: %s" % (filename, fileSize, validXML)
         if(not validXML):
            try:
               schema.validate(filename)
            except xmlschema.XMLSchemaValidationError as e:
               failureReason = e.reason
               eaf_validationMessage = "%s failure.  error: %s" % (filename, failureReason)
         return eaf_validationMessage

#----------------------------------------------------------------------------------------------------
@app.callback(Output('soundFileUploadTextArea', 'value'),
              [Input('upload-sound-file', 'contents')],
              [State('upload-sound-file', 'filename'),
               State('upload-sound-file', 'last_modified'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_soundUpload(contents, name, date, projectDirectory):
    if name is None:
        return("")
    print("=== on_soundUpload")
    data = contents.encode("utf8").split(b";base64,")[1]
    filename = os.path.join(projectDirectory, name)
    with open(filename, "wb") as fp:
       fp.write(base64.decodebytes(data))
       fileSize = os.path.getsize(filename)
       errorMessage = ""
       validSound = True
       try:
          rate, mtx = wavfile.read(filename)
       except ValueError as e:
          print("exeption in wavfile: %s" % e)
          rate = -1
          validSound = False
          errorMessage = str(e)
       print("sound file size: %d, rate: %d" % (fileSize, rate))
       sound_validationMessage = "%s:  (%d bytes), valid sound: %s %s" % (filename, fileSize,
                                                                          validSound, errorMessage)
       return sound_validationMessage

#----------------------------------------------------------------------------------------------------
@app.callback(Output('tierMapUploadTextArea', 'value'),
              [Input('upload-tierMap-file', 'contents')],
              [State('upload-tierMap-file', 'filename'),
               State('upload-tierMap-file', 'last_modified'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_tierMapUpload(contents, name, date, projectDirectory):
    if name is None:
        return("")
    print("=== on_tierMapUpload")
    encodedString = contents.encode("utf8").split(b";base64,")[1]
    decodedString = base64.b64decode(encodedString)
    s = decodedString.decode('utf-8')
    yaml_list = yaml.load(s)
    filename = os.path.join(projectDirectory, name)
    with open(filename, "w") as fp:
       fp.write(s)
       fp.close()

    return("%s:\n %s" % (filename, s))

#----------------------------------------------------------------------------------------------------
@app.callback(Output('grammaticalTermsUploadTextArea', 'value'),
              [Input('upload-grammaticalTerms-file', 'contents')],
              [State('upload-grammaticalTerms-file', 'filename'),
               State('upload-grammaticalTerms-file', 'last_modified'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_grammaticalTermsUpload(contents, name, date, projectDirectory):
    if name is None:
        return("")
    print("=== on_grammaticalTermsUpload")
    encodedString = contents.encode("utf8").split(b";base64,")[1]
    decodedString = base64.b64decode(encodedString)
    s = decodedString.decode('utf-8')
    yaml_list = yaml.load(s)
    filename = os.path.join(projectDirectory, name)
    with open(filename, "w") as fp:
       fp.write(s)
       fp.close()

    return("%s: %s" % (filename, s))

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('associateEAFAndSoundInfoTextArea', 'value'),
    [Input('extractSoundsByPhraseButton', 'n_clicks')],
    [State('sound_filename_hiddenStorage', 'children'),
     State('eaf_filename_hiddenStorage',   'children'),
     State('projectTitle_hiddenStorage',   'children'),
     State('projectDirectory_hiddenStorage',   'children'),
    ])
def on_extractSoundPhrases(n_clicks, soundFileName, eafFileName, projectTitle, projectDirectory):
    if n_clicks is None:
        return("")
    print("=== on_extractSoundPhrases")
    print("n_clicks: %d" % n_clicks)
    if soundFileName is None:
        return("")
    if eafFileName is None:
        return("")
    soundFileName = soundFileName
    eafFileName = eafFileName
    eafFileFullPath = eafFileName # os.path.join(UPLOAD_DIRECTORY, eafFileName)
    soundFileFullPath = soundFileName # os.path.join(UPLOAD_DIRECTORY, soundFileName)
    print("soundFileName: %s" % soundFileName)
    print("eafFileName: %s" % eafFileName)
    phraseFileCount = extractPhrases(soundFileFullPath, eafFileFullPath, projectDirectory)
    print("after extractPhrases")
    return("%s: %d phrases" % (projectDirectory, phraseFileCount))

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('sound_filename_hiddenStorage', 'children'),
    [Input("soundFileUploadTextArea", 'value')])
def storeSoundFilename(value):
    print("storeSoundFilename, by soundFileUploadTextArea change: %s" % value)
    soundFileName = value.split(":")[0]
    return(soundFileName)

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('eaf_filename_hiddenStorage', 'children'),
    [Input("eafUploadTextArea", 'value')])
def storeEafFilename(value):
    print("=== storeEafFilename, callback triggered by eafUploadTextArea change: %s" % value)
    eafFileName = value.split(":")[0]
    return(eafFileName)

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('tierMapGui-div', 'children'),
    [Input("eaf_filename_hiddenStorage", 'children')])
def createTierMappingMenusCallback(eafFilename):
    print("createTierMappingMenusCallback, eaf_filename_hiddenStorage trigger")
    if(eafFilename == ""):
       return("")
    print("=== extract tier ids from %s" % (eafFilename))
    #return(html.H4("infinite loop?"))
    return(createTierMappingMenus(eafFilename))

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('audioPhraseDirectory_hiddenStorage', 'children'),
    [Input('associateEAFAndSoundInfoTextArea', 'value')])
def update_output(value):
    print("=== callback triggered by assocateEAFAndSoundTextArea change: %s" % value)
    phraseDirectory = value.split(":")[0]
    return(phraseDirectory)

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('grammaticalTerms_filename_hiddenStorage', 'children'),
    [Input('grammaticalTermsUploadTextArea', 'value')])
def update_output(value):
    print("=== callback triggered by grammaticalTermsUploadTextArea change: %s" % value)
    grammaticalTermsFile  = value.split(":")[0]
    return(grammaticalTermsFile)

#----------------------------------------------------------------------------------------------------
# @app.callback(
#     Output('tierIDsBlankDiv', 'children'),
#     [Input('extractTierIDsButton', 'n_clicks')],
#     [State('eaf_filename_hiddenStorage', 'children')])
# def createTierMappingMenusCallback(n_clicks, eafFilename):
#     if n_clicks is None:
#         return("")
#     print("=== extract tier ids from %s: %d" % (eafFilename, n_clicks))
#     #return(html.H4("infinite loop?"))
#     return(createTierMappingMenus(eafFilename))

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('tierGuide_filename_hiddenStorage', 'children'),
    [Input('tierMapUploadTextArea', 'value')])
def update_output(value):
    print("=== callback triggered by grammaticalTermsUploadTextArea change: %s" % value)
    tierGuideFile  = value.split(":")[0]
    return(tierGuideFile)

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('createWebPageStatus', 'children'),
    [Input('createAndDisplayWebPageButton', 'n_clicks')],
    [State('sound_filename_hiddenStorage', 'children'),
     State('eaf_filename_hiddenStorage',   'children'),
     State('projectDirectory_hiddenStorage', 'children'),
     State('grammaticalTerms_filename_hiddenStorage', 'children'),
     State('projectTitle_hiddenStorage', 'children')])
     #State('tierGuide_filename_hiddenStorage', 'children')])
def createWebPageCallback(n_clicks, soundFileName, eafFileName, projectDirectory,
                          grammaticalTermsFile,projectTitle):
    if n_clicks is None:
        return("")
    print("=== create web page callback")
    print("        eaf: %s" % eafFileName)
    print(" phrases in: %s" % projectDirectory)
    if(grammaticalTermsFile == ""):
        grammaticalTermsFile = None
    html = createWebPage(eafFileName, projectDirectory, grammaticalTermsFile,
                         os.path.join(projectDirectory, "tierGuide.yaml"))
    absolutePath = os.path.abspath(os.path.join(projectDirectory, "text.html"))
    file = open(absolutePath, "w")
    file.write(html)
    file.close()
    #projectTitle="Inferno"
    createZipFile(projectDirectory,projectTitle)
    #url = 'http://0.0.0.0:8050/%s/text.html' % projectDirectory
    #webbrowser.open(url, new=2)
    return("wrote file")


#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('projectTitle_hiddenStorage', 'children'),
    [Input('setTitleButton', 'n_clicks'),
     Input('setTitleTextInput', 'value')]
    )
def setTitle(n_clicks, newTitle):
    print("=== title callback")
    if n_clicks is None:
        print("n_clicks is None")
        return("")
    print("nClicks: %d, currentTitle: %s" % (n_clicks, newTitle))
    print("--- set project title")
    #projectDirectory = os.path.join(PROJECTS_DIRECTORY, newTitle)
    #print("   creating projectDirectory if needed: %s" % projectDirectory)
    #if(not os.path.exists(projectDirectory)):
    #   os.mkdir(projectDirectory)
    return(newTitle)

@app.callback(
    Output('projectDirectory_hiddenStorage', 'children'),
    [Input('projectTitle_hiddenStorage', 'children')]
    )
def update_output(projectTitle):
    if(len(projectTitle) == 0):
        return('')
    print("=== project title has been set, now create project directory: '%s'" % projectTitle)
    projectDirectory = os.path.join(PROJECTS_DIRECTORY, projectTitle)
    print("   creating projectDirectory if needed: %s" % projectDirectory)
    if(not os.path.exists(projectDirectory)):
        os.mkdir(projectDirectory)
    return(projectDirectory)

@app.callback(
    Output('pageTitleH4', 'children'),
    [Input('projectDirectory_hiddenStorage', 'children')]
    )
def update_pageTitle(projectDirectory):
    if(len(projectDirectory) == 0):
        return('')
    print("=== projectDirectory_hiddenStorage has been set, now change project pageTitle: '%s'" % projectDirectory)
    #pdb.set_trace()
    newProjectTitle = projectDirectory.replace(PROJECTS_DIRECTORY, "")
    newProjectTitle = newProjectTitle.replace("/", "")
    print("IJAL Upload: %s" % newProjectTitle)
    return('')


@app.callback(
    Output('storyIFrame', 'src'),
    [Input('createWebPageStatus', 'children'),
     Input('projectDirectory_hiddenStorage', 'children')])
def displayText(createWebPageStatus, projectDirectory):
   print("=== displayText '%s'" % createWebPageStatus)
   if createWebPageStatus is None:
      return("")
   if(len(createWebPageStatus) == 0):
      return("")
   pathToHTML = os.path.join(projectDirectory, "text.html")
   return(pathToHTML)

# @app.callback(
#    Output('saveWebpageProgressTextArea', 'value'),
#    [Input('downloadWebpageButton', 'n_clicks'),
#     Input('projectTitle_hiddenStorage', 'children')])
# def saveWebpage(n_clicks, projectTitle):
#    if n_clicks is None:
#       return("")
#    createZipFile(projectTitle)
#   return("wrote web page as zip file")


@app.callback(
    Output('speechTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-speech', 'value')])
def updateSpeechTier(value):
    print("speech tier user name: %s" % value)
    return value

@app.callback(
    Output('translationTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-translation', 'value')])
def updateTranslationTier(value):
    print("translation tier user name: %s" % value)
    return value

@app.callback(
    Output('morphemeTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-morpheme', 'value')])
def updateMorphemeTier(value):
    print("morpheme tier user name: %s" % value)
    return value

@app.callback(
    Output('morphemeGlossTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-morphemeGloss', 'value')])
def updateMorphemeGlossTier(value):
    print("morphemeGloss tier user name: %s" % value)
    return value

@app.callback(
    Output('morphemePacking_hiddenStorage', 'children'),
    [Input('tierGuideMenu-morphemePacking', 'value')])
def updateMorphemePackingUserChoice(value):
    print("morphemePacking: %s" % value)
    return value

@app.callback(
    Output('translation2Tier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-translation2', 'value')])
def updateTranslation2Tier(value):
    print("translation2 tier user name: %s" % value)
    return value

@app.callback(
    Output('transcription2Tier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-transcription2', 'value')])
def updateTranscription2Tier(value):
    print("transcription2 tier user name: %s" % value)
    return value

@app.callback(
    Output('tierMappingChoicesResultDisplay', 'children'),
    [Input('saveTierMappingSelectionsButton', 'n_clicks')],
    [State('speechTier_hiddenStorage',        'children'),
     State('transcription2Tier_hiddenStorage',   'children'),
     State('morphemeTier_hiddenStorage',      'children'),
     State('morphemeGlossTier_hiddenStorage', 'children'),
     State('translationTier_hiddenStorage',   'children'),
     State('translation2Tier_hiddenStorage',   'children'),
     State('morphemePacking_hiddenStorage',   'children'),
     State('projectDirectory_hiddenStorage',  'children')])
def saveTierMappingSelection(n_clicks, speechTier, transcription2Tier, morphemeTier, morphemeGlossTier, 
                             translationTier, translation2Tier, morphemePacking, projectDirectory):
    if n_clicks is None:
        return("")
    print("saveTierMappingSelectionsButton: %d" % n_clicks)
    if len(speechTier) == 0:
        print("speechTier not mapped")
        return("You must specify a tier for the first line.")

    if len(translationTier) == 0:
        print("translationTier not mapped")
        return("You must specify a tier for the translation.")
    
    if len(morphemePacking) == 0:
        print("morphemePacking not specified")
        return("You must specify whether morphemes are delimited with tabs or ELAN tiers.")
    
##    if(any([len(x) == 0 for x in [speechTier, transcription2Tier, morphemeTier, morphemeGlossTier, translationTier, translation2Tier, morphemePacking]])):
##       print("not all tiers mapped")
##       return("Some choices not yet made.")

    print("time to write tierGuide.yaml")
    print("speechTier: %s" % speechTier)
    print("transcription2Tier: %s" % transcription2Tier)
    print("morphemeTier: %s" % morphemeTier)
    print("morphemeGlossTier: %s" % morphemeGlossTier)
    print("translationTier: %s" % translationTier)
    print("translation2Tier: %s" % translation2Tier)
    print("morphemePacking: %s" % morphemePacking)
    saveTierGuide(projectDirectory, speechTier, transcription2Tier, morphemeTier, morphemeGlossTier, translationTier, translation2Tier, morphemePacking)
    return("Saved your selection to 'tierGuide.yaml'")

@app.callback(Output('saveWebpageProgressTextArea', 'children'),
              [Input('confirmDownLoadObject', 'submit_n_clicks')],
              [State('projectTitle_hiddenStorage', 'children')])
def confirmDownload(submit_n_clicks, projectTitle):
    if not submit_n_clicks:
        return ''
    print("creating zip file")
    fullPath = createZipFile(projectTitle)
    return("saved web page: %s" % fullPath)

#----------------------------------------------------------------------------------------------------
# there can be multiple dash callbacks triggered by the same Input event.
# here we execute a second change to the webpage, returning the path to the project-specific
# webpage.zip, which is written into the href field of the html.A (or link) which nests the
# assembleTextButton
#----------------------------------------------------------------------------------------------------
@app.callback(Output('downloadURL', 'href'),
              [Input('projectDirectory_hiddenStorage', 'children')],
              [State('projectTitle_hiddenStorage', 'children')])
def updateDownloadTextButtonHref(directory,projectTitle):
   print("============= projectDirectory_hiddenStorage changed, updateDownloadTextButtonHref: %s" % directory)
   projectTitle += '.zip'
   print(projectTitle)
   pathToZip = os.path.join(directory,projectTitle)
   return(pathToZip)
   #return("%s/webpage.zip" % directory)


#----------------------------------------------------------------------------------------------------
def saveTierGuide(projectDirectory, speechTier, transcription2Tier, morphemeTier, morphemeGlossTier, translationTier, translation2Tier, morphemePacking):

    dict = {"speech": speechTier,
            "transcription2": transcription2Tier,
            "morpheme": morphemeTier,
            "morphemeGloss": morphemeGlossTier,
            "translation": translationTier,
            "translation2": translation2Tier,
            "morphemePacking": morphemePacking}

    filename =  os.path.join(projectDirectory, "tierGuide.yaml")

    with open(filename, 'w') as outfile:
        yaml.dump(dict, outfile, default_flow_style=False)

    print("saved tierMap to %s" % filename)

#----------------------------------------------------------------------------------------------------
def extractPhrases(soundFileFullPath, eafFileFullPath, projectDirectory):

    print("------- entering extractPhrases")
    print("soundFileFullPath: %s" % soundFileFullPath)
    print("projectDirectory: %s" % projectDirectory)
    audioDirectory = os.path.join(projectDirectory, "audio")

    if not os.path.exists(audioDirectory):
        os.makedirs(audioDirectory)

    ea = AudioExtractor(soundFileFullPath, eafFileFullPath, audioDirectory)
    assert(ea.validInputs)
    ea.extract(quiet=True)
    phraseFileCount = len(os.listdir(audioDirectory))
    return(phraseFileCount)

#----------------------------------------------------------------------------------------------------
def createWebPage(eafFileName, projectDirectory, grammaticalTermsFileName, tierGuideFileName):

    print("-------- entering createWebPage")
    #audioDirectory = os.path.join(projectDirectory, "audio")
    audioDirectoryRelativePath = "audio"
    print("eafFileName: %s" % eafFileName)
    print("projectDirectory: %s" % projectDirectory)
    print("audioDirectoryRelativePath: %s" % audioDirectoryRelativePath)
    print("grammaticalTermsFile: %s" % grammaticalTermsFileName)
    print("tierGuideFile: %s" % tierGuideFileName)

    text = Text(eafFileName,
                audioDirectoryRelativePath,
                grammaticalTermsFileName,
                tierGuideFileName)

    return(text.toHTML())

#----------------------------------------------------------------------------------------------------
def createZipFile(projectDir,projectTitle):

   currentDirectoryOnEntry = os.getcwd()
   #projectDir = os.path.join(PROJECTS_DIRECTORY, projectName)
   os.chdir(projectDir)
   print(projectDir)

   audioDir = "audio"
   filesToSave = [os.path.join("audio", f) for f in os.listdir(audioDir) if f.endswith('.wav')]
   
   #should name .html file according to title of project/text?   
   filesToSave.insert(0, "text.html")
   
   #zipfile should also be named for project
   zipFilename = "%s.zip" %projectTitle
   zipFilenameFullPath = os.path.join(currentDirectoryOnEntry, projectDir, zipFilename)
   zipHandle = ZipFile(zipFilename, 'w')

   #filesToSave needs to include ijal.css, ijalUtils.js
##   parentDir = os.path.abspath(os.path.join(projectDir, os.pardir))
##   print(parentDir)
   CSSfile = os.path.join(currentDirectoryOnEntry,"ijal.css")
   scriptFile = os.path.join(currentDirectoryOnEntry,"ijalUtils.js")
   copy(CSSfile, os.getcwd())
   copy(scriptFile, os.getcwd())
   filesToSave.append("ijal.css")
   filesToSave.append("ijalUtils.js")

   for file in filesToSave:
      zipHandle.write(file)

   zipHandle.close()

   os.chdir(currentDirectoryOnEntry)
   return(zipFilenameFullPath)

#----------------------------------------------------------------------------------------------------
server = app.server

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=60041)

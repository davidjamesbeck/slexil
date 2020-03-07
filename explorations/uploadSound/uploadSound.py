import base64
from zipfile import ZipFile
import os
import soundfile as soundfile
import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import xmlschema
from dash.dependencies import Input, Output, State
from shutil import copy
from pathlib import Path
import sys
sys.path.insert(1,Path(__file__).parents[2])
from audioExtractor import *
# from text import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
app.title = "SLEXIL"

app.scripts.config.serve_locally = True
server = app.server

## ----------------------------------------------------------------------------------------------------
def create_eafUploader():
    hyperLink = html.A(id='upload-eaf-link', children='select file')
    uploader = dcc.Upload(children=['Drag and drop or ', hyperLink], id='upload-eaf-file', multiple=False)

    return uploader


# ----------------------------------------------------------------------------------------------------
def create_eafUploaderTab():
    children = [html.Div("Add .eaf file", className="stepTitle"),
                # html.Div([dcc.Loading(create_eafUploader())], className="dragDropArea"),
                html.Div(create_eafUploader(), className="dragDropArea"),
                dcc.Loading("This can take a minute or two for large texts.", id="eafuploadStatus",
                         className="timewarning")
                ]

    div = html.Div(children=children, id='eafUploaderDiv', className="selectionBox")

    return div


# ----------------------------------------------------------------------------------------------------
def create_soundFileUploader():
    hyperLink = html.A(id='upload-sound-link', children='select file')
    uploader = dcc.Upload(id='upload-sound-file', children=['Drag and drop or ', hyperLink], multiple=False,
                          disabled=True)

    return uploader


# ----------------------------------------------------------------------------------------------------
def create_soundFileUploaderTab():
    children = [html.Div("Add sound file", className="stepTitle"),
                # html.Div([dcc.Loading(create_soundFileUploader())],
                html.Div(create_soundFileUploader(),
                        className="dragDropArea"),
                dcc.Loading(children="This can take a minute or two for large files.", id="soundUploadStatus",
                         className="timewarning")
                ]

    div = html.Div(children=children, id='soundFileUploaderDiv', className="selectionBox")

    return div

# ----------------------------------------------------------------------------------------------------
def create_componentsUploaderTab():
    children = [create_eafUploaderTab(),
                create_soundFileUploaderTab(),
                html.P(id='eaf_filename_hiddenStorage', children="", style={'display': 'none'}),
                html.P(id='projectDirectory_hiddenStorage', children="", style={'display': 'none'}),
                html.P(id='soundUploadStatus_hiddenStorage', children="", style={'display': 'none'}),
                html.P(id='sound_filename_hiddenStorage', children="", style={'display': 'none'})]

    div = html.Div(children=children, id='uploadComponents-div', className='tierDiv')

    return div


# ----------------------------------------------------------------------------------------------------
app.layout = html.Div(create_componentsUploaderTab())

# ----------------------------------------------------------------------------------------------------
@app.callback(Output('soundUploadStatus_hiddenStorage', 'contents'),
              [Input('upload-sound-file', 'loading_state')])
def checkLoadingState(upLoadState):
    print("@@@@ checking loading state")
    if upLoadState == True:
        print("@@@@ uploading")
        return False
    else:
        return True

# ----------------------------------------------------------------------------------------------------
@app.callback([Output('eafuploadStatus', 'children'),
               Output('eafuploadStatus', 'className'),
               Output('eaf_filename_hiddenStorage', 'children'),
               Output('upload-sound-file', 'disabled')],
              [Input('upload-eaf-file', 'contents')],
              [State('upload-eaf-file', 'filename'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_eafUpload(contents, name, projectDirectory):
    if name is None:
        return ("This can take a minute or two for large texts.", "timewarning", "",True)
    print("on_eafUpload, name: %s" % name)
    data = contents.encode("utf8").split(b";base64,")[1]
    filename = os.path.join(projectDirectory, name)
    if not filename[-4:] == '.eaf':
        eaf_validationMessage = '☠️ Please select a valid ELAN project (.eaf) file.'
        return eaf_validationMessage, "timewarning", '', True
    with open(filename, "wb") as fp:
        fp.write(base64.decodebytes(data))
        fileSize = os.path.getsize(filename)
        print("eaf file size: %d" % fileSize)
        schema = xmlschema.XMLSchema('http://www.mpi.nl/tools/elan/EAFv3.0.xsd')
        validXML = schema.is_valid(filename)
        eaf_validationMessage = "👍︎ File %s (%d bytes) is valid." % (name, fileSize)
        print("=== enabling next sequence (Upload audio)")
        if (not validXML):
            try:
                schema.validate(filename)
            except xmlschema.XMLSchemaValidationError as e:
                failureReason = e.reason
                eaf_validationMessage = "☠️ XML parsing error: %s [File: %s]" % (failureReason, filename)
                return eaf_validationMessage, "timewarning", '', True
        return eaf_validationMessage, "information", filename, False


# ----------------------------------------------------------------------------------------------------
def extractSoundPhrases(soundFileName, eafFileName, projectDirectory):
    print("=== extractSoundPhrases")
    soundFile = os.path.basename(soundFileName)
    eafFile = os.path.basename(eafFileName)
    print("soundFileName: %s" % soundFileName)
    print("eafFileName: %s" % eafFile)
    soundFileFullPath = os.path.join(projectDirectory, soundFile)
    phraseFileCount = extractPhrases(soundFileFullPath, eafFileName, projectDirectory)
    print("=== enable next button in sequence (upload abbreviations)")
    return "parsed into %d lines." % (phraseFileCount)


# ----------------------------------------------------------------------------------------------------
@app.callback([Output('soundUploadStatus', 'children'),
               Output('soundUploadStatus', 'className'),
               Output('sound_filename_hiddenStorage', 'children')],
              [Input('upload-sound-file', 'contents')],
              [State('upload-sound-file', 'filename'),
               State('eaf_filename_hiddenStorage', 'children'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_soundUpload(contents, name, eafilename, projectDirectory):
    if name is None:
        return "This can take a minute or two for large files.", "timewarning", ""  # , 1, 1
    print("=== on_soundUpload")
    data = contents.encode("utf8").split(b";base64,")[1]
    filename = os.path.join(projectDirectory, name)
    print("=== opening file")
    with open(filename, "wb") as fp:
        fp.write(base64.decodebytes(data))
        fileSize = os.path.getsize(filename)
        errorMessage = ""
        validSound = True
        try:
            mtx, rate = soundfile.read(filename)
        except (ValueError, RuntimeError) as e:
            print("exeption in .wav file: %s" % e)
            rate = -1
            validSound = False
            errorMessage = str(e)
        print("sound file size: %d, rate: %d" % (fileSize, rate))
        if validSound:
            sound_validationMessage = "👍︎ Sound file: %s (%d bytes), " % (name, fileSize)
            extractionMessage = extractSoundPhrases(name, eafilename, projectDirectory)
            sound_validationMessage += extractionMessage
            return sound_validationMessage, "information", filename  # , 0, 0
        else:
            if "Unsupported bit depth: the wav file has 24-bit data" in errorMessage:
                sound_validationMessage = "☠️ File %s (%d byes) has 24-bit data, must be minimum 32-bit." % (
                    name, fileSize)
            elif "File contains data in an unknown format" in errorMessage:
                sound_validationMessage = "☠️ File %s unsupported format (see About SLEXIL)." % (
                    name)
            else:
                sound_validationMessage = "☠️ Bad sound file: %s [File: %s (%d bytes)]" % (errorMessage, name, fileSize)
            return sound_validationMessage, "timewarning", filename  # , 1, 1

# ----------------------------------------------------------------------------------------------------
def extractPhrases(soundFileFullPath, eafFileFullPath, projectDirectory):
    print("=== entering extractPhrases")
    print("soundFileFullPath: %s" % soundFileFullPath)
    print("projectDirectory: %s" % projectDirectory)
    audioDirectory = os.path.join(projectDirectory, "audio")

    if not os.path.exists(audioDirectory):
        os.makedirs(audioDirectory)
    copy(soundFileFullPath, audioDirectory)
    ea = AudioExtractor(soundFileFullPath, eafFileFullPath, audioDirectory)
    assert (ea.validInputs)
    ea.extract(quiet=True)
    phraseFileCount = len(os.listdir(audioDirectory)) - 1
    return (phraseFileCount)





if __name__ == '__main__':
    app.run_server(debug=True)



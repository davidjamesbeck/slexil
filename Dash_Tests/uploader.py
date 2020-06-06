import dash
import flask
import os
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pdb
import base64
import xmlschema
from xml.etree import ElementTree as etree
from zipfile import ZipFile
from shutil import copy

import soundfile as soundfile
#app = dash.Dash()
server = flask.Flask(__name__)
app = dash.Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
# ----------------------------------------------------------------------------------------------------

def create_eafUploader():
    hyperLink = html.A(id='upload-eaf-link', children='select file')
    uploader = dcc.Upload(children=['Drag and drop or ', hyperLink], id='upload-eaf-file', multiple=False)

    return uploader


# ----------------------------------------------------------------------------------------------------

children = [html.Div("Add .eaf file", className="stepTitle"),
                html.Div([create_eafUploader()], className="dragDropArea"),
                dcc.Loading("This can take a minute or two for large texts.", id="eafuploadStatus",
                            className="timewarning")
                ]

app.layout = html.Div(children=children)


# ----------------------------------------------------------------------------------------------------

@app.callback(Output('eafuploadStatus', 'children'),
              [Input('upload-eaf-file', 'contents')],
              [State('upload-eaf-file', 'filename')])
def on_eafUpload(contents, name):
    print("===entering on_eafUpLoad")
    if name is None:
        return ("This can take a minute or two for large texts.")
    print("on_upload-eaf-file, name: %s" % name)
    projectDirectory = 'TempProjects'
    filename = os.path.join(projectDirectory, name)
    # data = base64.b64decode(contents)
    # pdb.set_trace()
    data = contents.encode("utf8").split(b";base64,")[1]
    if len(data) == 0:
        data = contents.encode("utf8").split(b";base64,")[0]
    if not filename[-4:] == '.eaf':
        eaf_validationMessage = '☠️ Please select a valid ELAN project (.eaf) file.'
        return eaf_validationMessage
    with open(filename, "wb") as fp:
        fp.write(base64.decodebytes(data))
    print("Filename: %s" %filename)
    assert(os.path.isfile(filename))
    fileSize = os.path.getsize(filename)
    print("eaf file size: %d" % fileSize)
    schema = xmlschema.XMLSchema('http://www.mpi.nl/tools/elan/EAFv3.0.xsd')
    try:
        validXML = schema.is_valid(filename)
    except etree.ParseError as e:
        import xml.parsers.expat
        error = xml.parsers.expat.errors.messages[e.code]
        eaf_validationMessage = "☠️ XML parsing error: %s [File: %s]" % (error, name)
        return eaf_validationMessage
    eaf_validationMessage = "👍︎ File %s (%d bytes) is valid." % (name, fileSize)
    if (not validXML):
        try:
            schema.validate(filename)
        except xmlschema.XMLSchemaValidationError as e:
            failureReason = e.reason
            eaf_validationMessage = "☠️ XML parsing error: %s [File: %s]" % (failureReason, name)
            return eaf_validationMessage
        # eaf_validationMessage = "👍︎ File %s (%d bytes) is valid." % (name, fileSize)
        print("=== enabling next sequence (Upload audio)")
        return eaf_validationMessage


# ----------------------------------------------------------------------------------------------------

def validate_EAF(filename):
    print("--- testing %s" %filename)
    assert(os.path.isfile(filename))
    with open(filename,"r") as fp:
        contents = fp.read()
    with open(filename, "rwb") as fp:
        data = contents.encode("utf8").split(b";base64,")[1]
        fp.write(base64.decodebytes(data))
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
# ----------------------------------------------------------------------------------------------------


@app.server.route('/static/<path:urlpath>')
def serve_static(urlpath):
    print("serve static, path: %s" % urlpath)
    root_dir = os.getcwd()
    # return flask.send_file("static/Inferno.html")
    return flask.send_from_directory(os.path.join(root_dir, 'static'), path)
#
if __name__ == '__main__':
    app.run_server(debug=True)

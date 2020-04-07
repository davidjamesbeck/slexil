import dash
import flask
import os
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pdb
import base64
from zipfile import ZipFile

import soundfile as soundfile
#app = dash.Dash()
server = flask.Flask(__name__)
app = dash.Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
# ----------------------------------------------------------------------------------------------------

hyperLink = html.A(id='upload-sound-link', children='select file', className='fakebuttonOff')
uploader = dcc.Upload(id='upload-sound-file', children=hyperLink, multiple=False)
textArea = dcc.Textarea(id="soundFileUploadTextArea",
                        placeholder='sound file validation results go here',
                        value="",
                        className="textarea")

progress = html.Div(id="progressBar", children=[""])

children = [html.Div(uploader),
            textArea,
            html.Div("This can take a minute or two for large files.", className="soundfiletimewarning"),
            progress
            ]

app.layout = html.Div(children=children)

# ----------------------------------------------------------------------------------------------------
@app.callback(
    [Output("progress", "value"), Output("progress", "children"), Output('soundFileUploadTextArea', 'value')],
    [Input("progress-interval", "n_intervals")],
    [State('upload-sound-file', 'contents'),
     State('upload-sound-file', 'filename')]
)
def update_progress(n,contents,name):
    # check progress of some background process, in this example we'll just
    # use n_intervals constrained to be in 0-100

    if uploader.loading_state.is_loading == 1:
        progress = min(n % 110, 100)
    else:
        progress = min(0 % 110, 100)
    # only add text after 5% progress to ensure text isn't squashed too much


    return progress, f"{progress} %" if progress >= 5 else "", ""
# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output('progressBar', 'children'),
     [Input('upload-sound-file', 'contents')],
      [State('upload-sound-file', 'filename')])
def progressBarOn(contents,name):
    if name is None:
        return ""
    print("=== on_soundUpload")
    # data = contents.encode("utf8").split(b";base64,")[1]
    children =[dcc.Interval(id="progress-interval", n_intervals=0, interval=500),
        dbc.Progress(id="progress", striped=True)]
    return children
# ----------------------------------------------------------------------------------------------------


@app.server.route('/static/<path:urlpath>')
def serve_static(urlpath):
    print("serve static, path: %s" % urlpath)
    root_dir = os.getcwd()
    return flask.send_file("static/Inferno.html")
    #return flask.send_from_directory(os.path.join(root_dir, 'static'), path)

if __name__ == '__main__':
    app.run_server(debug=True)

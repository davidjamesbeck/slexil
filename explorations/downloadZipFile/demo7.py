# derived from https://community.plot.ly/t/allowing-users-to-download-csv-on-click/5550/13
import flask
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import os

buttonStyle = {"margin-left": 30, "margin-top": 20, "font-size": 24};

app = dash.Dash(__name__)

app.layout = html.Div([
    ##dcc.Store(id='storage_projectDirectory', storage_type='local'),
    html.Div(id='storage_projectDirectory', children="abc", style={'display': 'none'}),
    html.A(html.Button('Download the Inferno Demo', style=buttonStyle), href='infernoDemo.zip'),
    html.H4("choose a project to assemble: ", style={"margin-left": 30}),
    dcc.Dropdown(id='projectChooser',
                 options=[{'label': 'Lokono', 'value': 'lokono'}, {'label': 'Daylight', 'value': 'daylight'}],
                 style={"width": 100, "margin-left": 30, "width": 200}),

    html.Br(),
    html.Button('Pretend to assemble the text', id="assembleTextButton", style=buttonStyle, disabled="True"),
    html.Br(),
    html.A(id="downloadURL",
           children=[html.Button('Download newly assembled text',
                                 id="downloadAssembledTextButton",
                                 style=buttonStyle,
                                 disabled="True")],
           href=''),
    ])

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

@app.server.route('/<filename>')
def downloadZip(filename):
    return flask.send_file(filename,
                           mimetype='application/zip',
                           as_attachment=True)

@app.callback(Output('assembleTextButton', 'disabled'),
              [Input('storage_projectDirectory', 'children')])
def set_button_enabled_state(children):
    print("============= storage_projectDirectory changed, enabling assembleTextButton: %s" % children)
    if (children == None):
      return True
    return False

# @app.callback(Output('downloadAssembledTextButton', 'disabled'),
#               [Input('storage_projectDirectory', 'children')])
# def set_button_enabled_state(children):
#     print("============= storage_projectDirectory changed, disabling downloadAssembledTextButton: %s" % children)
#     if (children == None):
#       return True
#     return False


#----------------------------------------------------------------------------------------------------
# the assembleTextButton, when clicked, has these consequences:
#  -  text is assembled (simulated here in a call to a function stub
#  -  the downloadAssembledText button is enabled, setting up that action
#----------------------------------------------------------------------------------------------------
@app.callback(Output('downloadURL', 'href'),
              [Input('storage_projectDirectory', 'children')])
def updateDownloadTextButtonHref(directory):
   print("============= storage_projectDirectory changed, updateDownloadTextButtonHref: %s" % directory)
   return ("PROJECTS/%s/webpage.zip" % directory)

# @app.callback(Output('downloadAssembledTextButton', 'disabled'),
#              [Input('storage_projectDirectory', 'children')])
# def disableDownloadTextButton(directory):
#    return True

@app.callback(Output('downloadAssembledTextButton', 'disabled'),
              [Input('assembleTextButton', 'n_clicks')],
              [State('storage_projectDirectory', 'children')])
def set_button_enabled_state(n_clicks, projectDirectory):
    print("assembleTextButton callback")
    if(n_clicks is None):
        return(True)
    assembleText(projectDirectory)
    return False

#----------------------------------------------------------------------------------------------------
# a new selection in the  projectChooser pulldown widgets has these consequences
#   that choice is saved in a local storage object
#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('storage_projectDirectory', 'children'),
    [Input('projectChooser', 'value')])
def updateStorage(value):
    print("projectChooser new value, updating storage_projectDirectory: %s" % value)
    return value;

# @app.callback(
#     Output('downloadURL', 'href'),
#     [Input(
#     [State('storage_projectDirectory', 'children')])
# def updateDownloadURL(data):
#     print("storage_projectDirectory input changes")
#     if(data is None):
#         return("")
#     print("   data: %s" % data);
#     return ("PROJECTS/%s/webpage.zip" % data)

#----------------------------------------------------------------------------------------------------
def assembleText(projectDirectory):

    print("assemble text in %s" % projectDirectory)

#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server()


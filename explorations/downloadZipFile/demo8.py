import flask
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import os

buttonStyle = {"margin-left": 30, "margin-top": 20, "font-size": 24};

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(id='projectDirectory_hiddenStorage', children="abc", style={'display': 'none'}),
    html.A(html.Button('Download the Inferno Demo', style=buttonStyle), href='demos/infernoDemo.zip'),
    html.H4("choose a project to assemble: ", style={"margin-left": 30}),
    dcc.Dropdown(id='projectChooser',
                 options=[{'label': 'Lokono', 'value': 'loco'}, {'label': 'Daylight', 'value': 'daylight'}],
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

#----------------------------------------------------------------------------------------------------
# this route handles the download of zipped up assembled slexil projects
# which, by convention, are  ./PROJECTS/<someName>/webpage.zip:
#    PROJECTS/daylight/webpage.zip
#    PROJECTS/loco/webpage.zip
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

#----------------------------------------------------------------------------------------------------
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
# the first user event will be to select in the name of the project to work on.  this action is
# performed in the projectChooser dropdown widget.  the only direct consequence is to assign the
# project's name into a hidden div, whose name is "projectDirectory_hiddenStorage"
# this is an incredibly, embarrassingly awkward hack, the dash mechanism for local (in-browser)
# state.
#
# other app.callbacks watch for this assignment, triggering other changes on the web page, most
# obviously, enabling the "Pretend to assemble the text" button.
#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('projectDirectory_hiddenStorage', 'children'),
    [Input('projectChooser', 'value')])
def updateStorage(value):
    print("projectChooser new value, updating projectDirectory_hiddenStorage: %s" % value)
    return value;

#----------------------------------------------------------------------------------------------------
# as described just above, this callback enables the assembleTextButton
#----------------------------------------------------------------------------------------------------
@app.callback(Output('assembleTextButton', 'disabled'),
              [Input('projectDirectory_hiddenStorage', 'children')])
def set_button_enabled_state(children):
    print("============= projectDirectory_hiddenStorage changed, enabling assembleTextButton: %s" % children)
    if (children == None):
      return True
    return False

#----------------------------------------------------------------------------------------------------
# there can be multiple dash callbacks triggered by the same Input event.
# here we execute a second change to the webpage, returning the path to the project-specific
# webpage.zip, which is written into the href field of the html.A (or link) which nests the
# assembleTextButton
#----------------------------------------------------------------------------------------------------
@app.callback(Output('downloadURL', 'href'),
              [Input('projectDirectory_hiddenStorage', 'children')])
def updateDownloadTextButtonHref(directory):
   print("============= projectDirectory_hiddenStorage changed, updateDownloadTextButtonHref: %s" % directory)
   return ("PROJECTS/%s/webpage.zip" % directory)

#----------------------------------------------------------------------------------------------------
# the project has been chosen; the downloadURL has been updated so now we want to enable the
# the downloadAssembledTextButton.  as a side effect, we call a function which pretends to actually
# assemble the text.  thus, two things happen here:
#   we assemble the text
#   we enable the downloadAssembledText utton
# recall that the downloadAssembledText button is nested within an html anchor tag whose href
# was updated, triggered in the preceeding callback when projectDirectory_hiddenStorage changed
# (which was itself triggered by the dropdown menu change
#----------------------------------------------------------------------------------------------------
@app.callback(Output('downloadAssembledTextButton', 'disabled'),
              [Input('assembleTextButton', 'n_clicks')],
              [State('projectDirectory_hiddenStorage', 'children')])
def assembleTextAndEnableDownloadButton(n_clicks, projectDirectory):
    print("assembleTextButton callback")
    if(n_clicks is None):
        return(True)
    assembleText(projectDirectory)
    return False

#----------------------------------------------------------------------------------------------------
def assembleText(projectDirectory):

    print("assemble text in %s" % projectDirectory)

#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server()


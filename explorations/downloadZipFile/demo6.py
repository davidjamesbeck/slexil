# derived from https://community.plot.ly/t/allowing-users-to-download-csv-on-click/5550/13
import flask
import dash
import dash_html_components as html
from dash.dependencies import Output, Input

buttonStyle = {"margin-left": 30, "margin-top": 20, "font-size": 24};

app = dash.Dash(__name__)

app.layout = html.Div([
    html.A(html.Button('Download the Inferno Demo', style=buttonStyle), href='infernoDemo.zip'),
    html.Br(),
    html.Button('Pretend to assemble the text', id="assembleTextButton", style=buttonStyle),
    html.Br(),
    html.A(html.Button('Download newly assembled text', id="downloadAssembledTextButton", style=buttonStyle, disabled="True"),
           href='webpage.zip'),
    ])

@app.server.route('/<filename>')
def download_zip(filename):
    return flask.send_file(filename,
                           mimetype='application/zip',
                           as_attachment=True)

@app.callback(Output('downloadAssembledTextButton', 'disabled'),
             [Input('assembleTextButton', 'n_clicks')])
def set_button_enabled_state(n_clicks):
    if(n_clicks is None):
        return(True)
    assembleText()
    return False

#----------------------------------------------------------------------------------------------------
def assembleText():

    print("a stub function in which we pretend to assemble the IJAL text from its parts")

#----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server()


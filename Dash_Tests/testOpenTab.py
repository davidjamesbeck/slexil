import dash
import flask
import os
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
app.title = "SLEXIL"

app.scripts.config.serve_locally = True
server = app.server

port = 5000

server = flask.Flask(__name__)

createAndDisplayButton = html.Button('Make page', id='button',
                                     className="button")
previewLink = html.A('open preview', id="previewLink", href='', target='_blank')
createWebpageStatus = html.Div(id="createWebPageStatus", children=[previewLink, " in a new tab"],
                               className="previewoff")  # , style={'display': 'none'})
children = html.Div(children=[createAndDisplayButton, createWebpageStatus],
                         className="webFrameButtonBox")
app.layout = html.Div(children)


@app.callback([Output("createWebPageStatus", "className"),
               Output('previewLink', 'href')],
              [Input("button", "n_clicks")]
              )
def on_Button_Click(n_clicks):
    if n_clicks is None:
        return 'previewoff',''
    print('=== button clicked')
    previewURL = '/static/Inferno.html'
    return "previewon", previewURL

def open_tab(source):
    print("=== open new tab")
    webbrowser.open_new_tab(source)

@app.server.route('/static/<path:urlpath>')
def serve_static(urlpath):
    print('serving file')
    print("serve static, path: %s" % urlpath)
    root_dir = os.getcwd()
    # return flask.send_file("static/Inferno.html")
    # return flask.send_from_directory(os.path.join(root_dir, 'static'), path)
    webbrowser.open_new("./static/Inferno.html")




# if __name__ == '__main__':
#     app.run_server(debug=True)

# enable these lines if running with gunicorn
if __name__ == "__main__":
    server = app.server
    app.run()

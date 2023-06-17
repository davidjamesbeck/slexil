import dash
import flask
import os
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import pdb

#app = dash.Dash()
server = flask.Flask(__name__)
app = dash.Dash(__name__,server=server)
app.layout = html.Div(children=[
    html.H1(children='Test cases',className="banner"),
    html.Iframe(id="storyIFrame",
                src='static/Inferno.html',
                className="webpageFrame"),
    html.Button("press here",id="button")
    ])


@app.callback(Output("storyIFrame","src"),
              [Input("button","n_clicks")]
    )
def on_Button_Click(n_clicks):
    if n_clicks is None:
        return('')
    print('=== button clicked')
    return('static/Inferno.html')

@app.server.route('/static/<path:urlpath>')
def serve_static(urlpath):
    print("serve static, path: %s" % urlpath)
    root_dir = os.getcwd()
    return flask.send_file("static/Inferno.html")
    #return flask.send_from_directory(os.path.join(root_dir, 'static'), path)

if __name__ == '__main__':
    app.run_server(debug=True)

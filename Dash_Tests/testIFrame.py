import dash
import flask
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html

#app = dash.Dash()
server = flask.Flask(__name__)
app = dash.Dash(__name__,server=server)
app.layout = html.Div(children=[
    html.H1(children='Test cases',className="banner"),
    html.Iframe(id="storyIFrame",         src='Users/David/OpenSource/github/Dash_Tests/Inferno.html',     className="webpageFrame")
    ])

@server.route('/static/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, 'static'), path)

if __name__ == '__main__':
    app.run_server(debug=True)

import dash
import flask
import os
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import webbrowser

app = dash.Dash(__name__)
port = 5000  # or simply open on the default `8050` port
# app = dash.Dash()
server = flask.Flask(__name__)
# app = dash.Dash(__name__,server=server)
app.layout = html.Div(children=[
    html.H1(children='Test cases', className="banner"),
    html.Iframe(id="storyIFrame",
                # src='static/Inferno.html',
                className="webpageFrame"),
    html.Button("press here", id="button"),
    dcc.Textarea(id="textDiv"),
    html.Div(children=[html.A('display new page', href='file://static/Inferno.html', target='_blank')])
    ])


@app.callback([Output("storyIFrame", "src"),
               Output('textDiv', 'value')],
              [Input("button", "n_clicks")]
              )
def on_Button_Click(n_clicks):
    if n_clicks is None:
        return '',''
    print('=== button clicked')
    # pdb.set_trace()
    open_tab("file:///Users/David/OpenSource/github/slexil/Dash_Tests/static/Inferno.html")
    webbrowser.open("static/Inferno.html")
    with open("static/Inferno.html", "r") as f:
        print('reading')
        text = f.read()
    return 'static/Inferno.html', text

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


def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))


if __name__ == '__main__':
    app.run_server(debug=True)

# if __name__ == '__main__':
#     Timer(1, open_browser).start();
#     app.run_server(debug=True, port=port)

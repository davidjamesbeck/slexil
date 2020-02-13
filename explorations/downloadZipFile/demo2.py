import os
import dash
from flask import send_from_directory

import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc


app = dash.Dash()

app.layout = html.Div([

	html.A(
        'Download Zip',
        id='download-zip',
        download = "webpage.zip",
        href="",
        target="_blank",
        n_clicks = 0
	    )
	])

@app.callback(
    Output('download-zip', 'href'),
    [Input('download-zip', 'n_clicks')])
def doDownload(n_clicks):


STATIC_PATH = os.path.join(app.server.root_path, 'static')
# define layout...
#  add links with, for example: href='/static/test.csv'

@app.server.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory(STATIC_PATH, filename)


if __name__ == '__main__':
	app.run_server() # debug = True)


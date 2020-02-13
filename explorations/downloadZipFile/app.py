from flask import send_file
import dash
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

def generate_report_url(n_clicks):

	return '/dash/urldownload'

@app.server.route('/dash/urldownload')

def generate_report_url():

	return send_file('webpage.zip', attachment_filename = 'example.zip', as_attachment = True)

if __name__ == '__main__':
	app.run_server() # debug = True)


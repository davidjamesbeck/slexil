# from https://community.plot.ly/t/allowing-users-to-download-csv-on-click/5550/13
import io

import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(id='my-dropdown', value='default',
                 options=[
                     {'label': 'New York City', 'value': 'NYC'},
                     {'label': 'Montréal', 'value': 'MTL'},
                     {'label': 'San Francisco', 'value': 'SF'}
                 ]
                 ),
    html.A('Download demo', id='download_infernoDemo', style={"margin": 100}),
    html.Br(),
    html.A('Download webpage.zip', id='download_newText', style={"margin": 100})
)
])


@app.callback(Output('download_newText', 'href'),
              [Input('my-dropdown', 'value')])
def update_link(value):
    #return '/dash/urlToDownload?value={}'.format(value)
    return 'webpage.zip'

@app.callback(Output('download_infernoDemo', 'href'),
              [Input('my-dropdown', 'value')])
def update_link(value):
    #return '/dash/urlToDownload?value={}'.format(value)
    return 'infernoDemo.zip'


@app.server.route('/<filename>')
def download_zip(filename):
    return flask.send_file(filename,
                           #mimetype='application/zip',
                           #attachment_filename='webpage.zip',
                           as_attachment=True)


if __name__ == '__main__':
    app.run_server()


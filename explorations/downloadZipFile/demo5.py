# derived from https://community.plot.ly/t/allowing-users-to-download-csv-on-click/5550/13
import flask
import dash
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.A(html.Button('Download the Inferno Demo', style={"margin-left": 30}), href='infernoDemo.zip'),
    html.Br(),
    html.A(html.Button('Download newly assembled text', style={"margin-left": 30}), href='webpage.zip'),
    ])

@app.server.route('/<filename>')
def download_zip(filename):
    return flask.send_file(filename,
                           mimetype='application/zip',
                           as_attachment=True)

if __name__ == '__main__':
    app.run_server()


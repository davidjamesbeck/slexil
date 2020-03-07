import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
app.title = "StyleTester"

app.scripts.config.serve_locally = True
server = app.server
app.layout = html.Div([
    dcc.ConfirmDialogProvider(
        children=html.Button(
            'Click Me',
        ),
        id='danger-danger',
        message='Danger danger! Are you sure you want to continue?'
    ),
    html.Div(id='output')
])


@app.callback(Output('output', 'children'),
              [Input('danger-danger', 'submit_n_clicks')])
def update_output(submit_n_clicks):
    if not submit_n_clicks:
        return ''
    return """
        It was dangerous but we did it!
        Submitted {} times
    """.format(submit_n_clicks)

if __name__ == '__main__':
    app.run_server(debug=True)



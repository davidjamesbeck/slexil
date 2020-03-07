import dash
import dash_core_components as dcc
import dash_html_components as html
import flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
app.title = "SLEXIL"

app.scripts.config.serve_locally = True
server = app.server

# ----------------------------------------------------------------------------------------------------
def create_webPageCreationTab():
    createAndDisplayButton = html.Button('Make page', id='createAndDisplayWebPageButton',
                                         className="button")

    downloadLinkAndButton = html.A(id="downloadURL",
                                   children=[html.Button('Download',
                                                         id="downloadAssembledTextButton",
                                                         className='button')],
                                   href='')

    previewLink = html.A('open preview', id="previewLink", href='', target='_blank')
    createWebpageStatus = html.Div(id="createWebPageStatus", children=[previewLink, "  in a new tab"],
                                   className="previewon")

    errorMessages = html.Span(id="createPageErrorMessages", children="Wrote file. Check error log for formatting issues",
                              className="formatWarningOn")

    children = [html.Hr(className="divider"),
                html.Div(children=[createAndDisplayButton, downloadLinkAndButton, createWebpageStatus, errorMessages],
                         className="webFrameButtonBox")]

    div = html.Div(children=children, id='createWebPageDiv')

    return div


app.layout = html.Div(create_webPageCreationTab())



if __name__ == '__main__':
    app.run_server(debug=True)



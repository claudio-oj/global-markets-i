"""
GM Insights
dash app
"""
import dash
import dash_auth

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css'] chinito_youtube.css

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# sin explicitar "external_stylesheets" apunta implicitamente a chinito_youtube.css en ./Assets
app = dash.Dash(__name__)

credentials = [
    ['admin','108'],
    ['gjara', 'chile2019'],
	['fferrada', 'ptosfernando2020'],
	['jzamora', 'basispapurri2029'],
	['cgomez','binary'],
	['fberly','fabi'],
	['dlizana','golf1'],
	['crosas','pizza'],
]

auth = dash_auth.BasicAuth(app,credentials)
app.title = 'Global-Markets Insights'
app.config.suppress_callback_exceptions = True

server = app.server
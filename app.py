"""
GM Insights
dash app
"""
import dash

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css'] chinito_youtube.css

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# sin explicitar "external_stylesheets" apunta implicitamente a chinito_youtube.css en ./Assets
app = dash.Dash(__name__)

app.title = 'Global-Markets Insights'
app.config.suppress_callback_exceptions = True

server = app.server
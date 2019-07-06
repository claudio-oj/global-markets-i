"""
GM Insights
dash app
"""
import dash

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__)

app.title = 'GMI Binary Analytics'
app.config.suppress_callback_exceptions = True

server = app.server
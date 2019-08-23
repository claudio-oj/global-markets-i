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
    ['admin','108801'],
	['cortiz','108801'],
	['ddiaz','davidivad'],
	['fvizcaino','3981'],
	['jara','binaryanalytics'], # jara euroamarica

    ['gjara', 'chile2019'], #gte tradition
	['mandrades','xt.e498B'], # gte TI tradition
	['fferrada', 'ptosfernando2020'], # broker tradition
	# ['jzamora', 'basispapurri2029'], # broker tradition


	# ['cgomez','binary'], # Christian Gomez
	# ['fberly','fabi'], #contacto CO en Santander
	# ['adiaz','happyhour'], #contacto CO en Santander

	# ['dlizana','golf1'], # diego lizana, hsbc
	# ['crosas','pizza'], # cristobal rosas, hsbc
	# ['jtrombert','elvalordelapolitica'], # jorge trombert, hsbc

	# ['mastaburuaga','masta'], # manuel astaburuaga, credicorp

	# ['cgonzalez','Carogonz76'], # carolina gonzalez, GFI
]

auth = dash_auth.BasicAuth(app,credentials)
app.title = 'Global-Markets Insights'
app.config.suppress_callback_exceptions = True

server = app.server
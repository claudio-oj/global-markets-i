import dash_core_components as dcc
import dash_html_components as html

from app import app


layout = html.Div(
	className='nine columns offset-by-one',
	children=[
		html.Br(),
		html.Br(),
		html.Div(
			html.Img(src='https://static.wixstatic.com/media/963559_aa62287269154585a1a8c607ecf64fc4~mv2.gif',
					 style={'width': '125px'}),
			style={'textAlign': 'center'},
		),
		html.H2("Global-Markets Insights", style={'textAlign':'center'}),
		html.P("Interbank markets financial data processing in the back-end ... for friendly assessment in the front-end. ",
			   style={
				   'textAlign':'center',
				   'font-style': 'italic',
			   }
		),
		dcc.Markdown('''---'''),

		html.Br(),
		# html.Br(),
		# html.Br(),

		html.Div(
			style={'display':'flex','justify-content':'center','fontSize':13}, # http://howtocenterincss.com/
			children=[dcc.Markdown('''
Host| [BinaryAnalytics.cl](http://www.BinaryAnaytics.cl) | |
:-------- | :---------: | :---------:
Website | [global-markets-i.herokuapp.com](https://global-markets-i.herokuapp.com/) | |
Latest Release| v2 beta Chile | 05-Aug-2019 |
Tutorial | [binaryanalytics.cl/gmi-tutorial](https://www.binaryanalytics.cl/gmi-tutorial) | password: *binaryanalytics*
Requirements | Google Chrome desktop > 13' | |
| Contact | [contacto@binaryanalytics.cl](mailto:contacto@binaryanalytics.cl) | |
'''
					)],
		),

		html.Br(),
		html.Br(),
	],
)


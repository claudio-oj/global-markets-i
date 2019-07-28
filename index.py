"""
GM Insights
dash app
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from header import tabs_gmi

from app import app, server
import app_home, app_fx, app_upload


""" DESPLIEGA LA APP """

app.layout = html.Div(
	children=[

	dcc.Location(id='url',refresh=False),

	html.Div([
		# html.Img(src='static/ba_logo.gif',
		# 	 className='one column',
		# 	 style={
		# 		'height': '3%',
		# 		'width': '3%',
		# 	 },
		# 		 ),
		html.H6("Global-Markets Insights",
				className='three columns',
				style={'color':'#FFF',
					   'fontSize':19,
					   'fontWeight':700,
					   "text-decoration": "none",
					   'margin':0,
					   'padding-left':20,
					   'padding-top':'10px',
					   'textAlign':'left',
					   # 'float': 'left',
					   },
				),
		html.Div([
			html.A(
				'Home',
				href='/home',
				className='links-sup',
				),
			html.A(
				'FX',
				href='/fx',
				className='links-sup',
			),
			html.A(
				'Basis',
				href='/basis',
				className='links-sup',
			),
			html.A(
				'IR cam',
				href='/ircam',
				className='links-sup',
			),
			html.A(
				'Sov Bonds',
				href='/bonds',
				className='links-sup',
			),
			html.A(
				'Inflation',
				href='/inflation',
				className='links-sup',
			),
			html.A(
				'Middle-Office',
				href='/middleoffice',
				className='links-sup',
			),

			],
			 className='six columns',
			 style={'textAlign' :'center',
					'float':'center',
					'fontWeight': 'bold',
					'padding-top':15,
					'fontSize':13},
			 ),
		html.Div(
			[
				html.A(
				'www.BinaryAnalytics.cl',
				href='http://www.binaryanalytics.cl',
				target="_blank",
				style={'color': '#FFF',"text-decoration": "none",'padding-left':10,},
				),
			],
			className='three columns',
			style={'textAlign' :'right',
					'fontWeight': 'bold',
					'padding-top':15,
					'padding-right':10,
					'fontSize':13},
			 ),

		],
		className='row',
		style={'backgroundColor':'#240E8B','borderRadius':'8px',
			   'marginBottom':4,
			   'height':'15%',
			   }
	),

	html.Div(id='page-content'),

	html.Div(
		html.Div('Global-Markets Insights, Chile - v2 beta edition. ® copyright 2019'),
		className="footer",
	),

	],

	style={
		'margin-right':8,
		'margin-left':8,
	},

)


@app.callback(Output('page-content', 'children'),
			  [Input('url', 'pathname')])
def display_page(pathname):
	if pathname == '/home':
		return app_home.layout
	elif pathname == '/fx' or pathname=='/':
		return app_fx.layout
	elif pathname == '/basis':
		return '¡ app basis en desarollo !'
	elif pathname == '/ircam':
		return '¡ app IR CAM en desarollo !'
	elif pathname == '/bonds':
		return '¡ app Sov Bonds en desarollo !'
	elif pathname == '/inflation':
		return '¡ app Inflation en desarollo !'
	elif pathname == '/middleoffice':
		return app_upload.layout
	else :
		return '404: url equivocado. correcto, por ej: global-markets-i.herokuapp.com/fx'


if __name__ == '__main__':
	app.run_server(debug=True)

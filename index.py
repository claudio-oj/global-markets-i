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
	html.Div([
		html.Img(src='static/ba_logo.gif',
			 className='one column',
			 style={
				'height': '3%',
                'width': '3%',
			 },
				 ),
		html.H6("Global-Markets Insights",
				className='five columns',
				style={'color':'#FFF',
					   'fontSize':15,
					   'fontWeight':700,
					   "text-decoration": "none",
					   'margin':0,
					   'padding-left':10,
					   'padding-top':'15px',
					   'float': 'left',
					   },
				),
		html.Div(
			html.A(
				'www.BinaryAnalytics.cl',
				href='http://www.binaryanalytics.cl',
				target="_blank",
				style={'color': '#FFF',"text-decoration": "none"},
				),
				 className='six columns',
				 style={'textAlign' :'right',
						'fontWeight': 'bold',
						'padding-top':15,
						'fontSize':13},
				 ),
		],
		className='row',
		style={'backgroundColor':'#4176A4','borderRadius':'8px',
			   'marginBottom':4,
			   'height':'15%',
			   }
	),


	html.Div(
		# className='custom-tabs',
		children=[tabs_gmi],
		# style={'borderRadius':'30px'},
	),

	html.Div(id='tab-output',
			 # style={'borderRadius':'30px'},
			 ),

	html.Div(
        className="footer",
        children=[
            html.Div('Global-Markets Insights, Chile - v1 beta edition. ® copyright 2019')
        ]
    )],
	style={
		'margin-right':8,
		'margin-left':8,
	},


	# className="twelve columns offset-by-two",
)



@app.callback(Output('tab-output', 'children'),
              [Input('tabs_gmi'  , 'value')])
def show_content(tab_value):
	if tab_value == 'tab-1':
		return app_home.layout
	if tab_value == 'tab-2':
		return app_fx.layout
	if tab_value == "tab-7":
		return app_upload.layout
	else:
		return html.P('en desarrollo...', style={"text-align":"center","vertical-align":"middle", 'marginTop': 200})


if __name__ == '__main__':
	app.run_server(debug=False)

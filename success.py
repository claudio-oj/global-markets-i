
import warnings
# Dash configuration
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from header import header_logo, header_link, tabs_gmi

from app import app, server
import app_home, app_fx, app_upload

warnings.filterwarnings("ignore")

layout = html.Div(
	children=[
     html.Div([
		html.Img(src='static/ba_logo.gif',
			 className='one column',
			 style={
				'height': '3%',
                'width': '3%',
                'margin-top':'0.05%'
				# 'float': 'right',
				# 'position': 'relative',
				# 'margin-top': 20,
				# 'margin-right': 20
				# 'padding-top':2,
			 },
				 ),
		html.H6("Global-Markets Insights",
				className='five columns',
				style={'color':'#FFF',
					   'fontSize':'17px',
					   'fontWeight':700,
					   "text-decoration": "none",
					   # 'padding-left':2,
					   'padding-top':'0.5%',
					   'float': 'left'
					   },
				),
		html.Div(header_link,
				 className='six columns',
				 style={"text-decoration": "none" ,'textAlign' :'right',
						'color': '#4176A4' ,'fontWeight': 'bold',
						'padding-top':'1.1%',
						'fontSize':15},
				 ),
		],
		className='row',
		style={'backgroundColor':'#4176A4','borderRadius':'8px',
			   'marginBottom':4,
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
            html.Div('Global-Markets Insights, Chile - v1 beta edition. Binary Analytics ® copyright 2019')
        ]
    )],
	style={
		'margin-right':8,
		'margin-left':8
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

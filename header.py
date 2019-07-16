
import dash_core_components as dcc
import dash_html_components as html


""" BANDA TITULO INICIAL GMI, ICONO BINARY, LINK 
https://community.plot.ly/t/how-to-manage-the-layout-of-division-figures-in-dash/6484/5 """

header_logo = html.Div(
			style={'display':'inline'},
			children=[
			html.Img(
				className='header-Binary-logo-titulo',
				src='static/ba_logo.gif',
				width=75,
				),
			html.Div('Global-Markets Insights',
				 className='titulo-GMI-estilo'),
			],
		)


header_link = html.A(
	'www.BinaryAnalytics.cl',
	href='http://www.binaryanalytics.cl',
	target="_blank",
	style={"text-decoration": "none" ,'textAlign' :'right',
		   'color': '#FFF' ,'fontWeight': 'bold'},
	)

""" TABS """

tabs_gmi = dcc.Tabs(
	id='tabs_gmi',
	value='tab-2',
	children=[
		dcc.Tab(label='Home'             ,value='tab-1', className='custom-tab', selected_className='custom-tab--selected'),
		dcc.Tab(label='FX Points'        ,value='tab-2', className='custom-tab', selected_className='custom-tab--selected'),
		dcc.Tab(label='IR Basis'         ,value='tab-3', className='custom-tab', selected_className='custom-tab--selected'),
		dcc.Tab(label='IR Swaps'         ,value='tab-4', className='custom-tab', selected_className='custom-tab--selected'),
		dcc.Tab(label='Sov Bonds'        ,value='tab-5', className='custom-tab', selected_className='custom-tab--selected'),
		dcc.Tab(label='Inflation'        ,value='tab-6', className='custom-tab', selected_className='custom-tab--selected'),
		dcc.Tab(label='Middle-Office'    ,value='tab-7', className='custom-tab', selected_className='custom-tab--selected'),
	],
)





import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import dash_table
from dash_table.Format import Format  # https://dash.plot.ly/datatable/typing
import plotly.graph_objs as go

from app import app



##
""" Corre INICIO procesos NECESARIOS. Crea tabla de puntos fwd , basis, ibasis,
importa funciones numericas y funciones crea graficos """
import pandas as pd

fra_historic = pd.read_csv("fra_history.csv")
indicator = pd.read_csv("indicator.csv")

pd.options.mode.chained_assignment = None #apaga warning set with copy

import numpy as np
from numbers import Number

from funcs_co import imp_spot, imp_clos_t, live, cam_os_simp, fra1m, fra1m_v2,iptos, ibasis
from funcs_co import weird_division, round_conv_basis, round_2d, float_or_zero

from graphs import crea_fra_scatter_graph, crea_fra_hist_line

spoty= imp_spot() #spot yesterday closing
spot = 650.58

# importa data closing tradition + crea df
df = imp_clos_t()

# lee precios live de cam y libor swap
df.ptos      = df.ptosy.copy(True)
# df.odelta    = 0
# df.ddelta    = 0
# df.carry     = 0
df.icam      = live(col='icam')
df.ilib      = live(col='ilib')
# df.icam_os   = 0
df.fracam_os = 3.6
df.basis     = df.basisy.copy(True)
df.tcs       = 6.5
# df.i_ptos    = 0
# df.i_basis   = 0


def table1_update(df):
	try:
		for c in ['ptos','ptosy']:
			df[c] = df[c].map(float_or_zero)

		df.odelta = df['ptos'] - df['ptosy']
		df.ddelta = 100 * df.apply(lambda x: weird_division(x.odelta, x.carry_days),axis=1)

		df.carry  = df.apply(lambda x: df.days[4] * weird_division(x.ptos, x.carry_days),axis=1)

		df.icam_os= df.apply(lambda x: cam_os_simp(x.carry_days if x.carry_days!=0 else float('Nan'),
												   spot, x.ptos , x.ilib),axis=1)

		df.fracam_os = fra1m_v2(df[['tenor', 'carry_days', 'icam_os']], interp=False)

		df.i_ptos = df.apply(lambda x: iptos(t=x.carry_days if x.carry_days!=0 else float('nan'),
								 spot=spot, iusd=x.ilib, icam=x.icam, b= x.basis,
								 tcs=x.tcs),axis=1)

		df.i_basis = df.apply(lambda x: ibasis(t=x.carry_days if x.carry_days!=0 else float('nan'),
								 spot=spot, iusd=x.ilib, icam=x.icam, ptos= x.ptos,
								 tcs=x.tcs),axis=1)

		df = df.applymap(round_2d)
		df[['basis','i_basis']] = df[['basis','i_basis']].applymap(round_conv_basis)

		return df

	except:
		return df

df = table1_update(df)


##

layout = html.Div(
	# className='row',
	# style={
		# 'margin':'0px',
		# 'textAlign':'justify',
		# 'padding-left':'25px',
	# },
	children=[
		html.Div(
			className='four columns',
			children=[
				dash_table.DataTable(
					id='table1',
					data= df.to_dict('records'),
					columns= [
						{'id':'ind',       'name':'ind',      'editable':False, 'hidden':True, 'type': 'numeric'},
						{'id':'tenor',     'name':'tenor',    'editable':False, 'hidden': False,'width': '40px'},
						{'id':'daysy',     'name':'daysy',    'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'days',      'name':'days',     'editable':False, 'hidden': False, 'type': 'numeric'},
						{'id':'ptosy',     'name':'ptosy',    'editable':False, 'type': 'numeric'},
						{'id':'ptos',      'name':'ptos',     'editable':True, 'type': 'numeric'},
						{'id':'odelta',    'name':'change',   'editable':False, 'hidden': False, 'type': 'numeric'},
						{'id':'ddelta',    'name':'ddelta',   'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'carry',     'name':'carry',    'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'icam',      'name':'icam',     'editable':True, 'hidden': False, 'type': 'numeric'},
						{'id':'ilib',      'name':'ilib',     'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'tcs',       'name':'tcs',      'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'icam_os',   'name':'icam-os',  'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'fracam_os', 'name':'f1m-os',   'editable':False, 'hidden': False, 'type': 'numeric'},
						{'id':'basisy',    'name':'basisy',   'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'basis',     'name':'basis',    'editable':True, 'type': 'numeric'},
						{'id':'i_ptos',    'name':'i_ptos',   'editable':False, 'type': 'numeric'},
						{'id':'i_basis',   'name':'i_basis',  'editable':False, 'type': 'numeric'},
						],
					style_as_list_view= True,
					n_fixed_rows=1,
					style_table={
						# 'margin':'5px',
						# 'maxHeight': '250',
						'overflowY': 'auto'
						},
					# css=[{
						#     'selector': '.dash-cell div.dash-cell-value',
						#     'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
						# }],
						# style_cell={

						# 'minWidth': '10px',
						# 'width': '15px',
						# 'maxWidth': '20px',
						# 'whiteSpace': 'no-wrap',
						# },
						# style_header={
							# 'column_id': 'ptos',
							# 'height':'35px',
							# 'textOverflow': 'clip',
							# 'borderBottom':'0px',
							# 'border': '1px solid white',
							# 'backgroundColor': 'white',
						# },
						style_cell_conditional=[
							{'if': {'column_id':'tenor'}, 'width': '40px'},
							{'if': {'column_id':'ptosy'}, 'width': '40px',
							 'color': 'rgb(204, 205, 206)'},
							{'if': {'column_id':'ptos'}, 'width': '45px',
							 'fontWeight': 600, 'color': '#4176A4'},
							{'if': {'column_id':'odelta'}, 'width': '48px'},
							{'if': {'column_id':'ddelta'}, 'width': '48px'},
							{'if': {'column_id':'carry'}, 'width': '48px'},
							{'if': {'column_id':'icam'}, 'width': '48px'},
							{'if': {'column_id':'ilib'}, 'width': '48px'},
							{'if': {'column_id':'fracam_os'}, 'width': '50px'},
							{'if': {'column_id':'basis'}, 'width': '48px',
							 'fontWeight': 600, 'color': '#4176A4'},
							{'if': {'column_id':'i_ptos'},  'width': '50px', 'fontWeight': 600,'color':'#801A86'},
							{'if': {'column_id':'i_basis'}, 'width': '50px', 'fontWeight': 600,'color':'#801A86'},
						],
						editable=True,
					),
				# dcc.Markdown('''Prueba Markdown'''),
				]
			),

		html.Div(
			className='four columns',
			# style={
			# 	# 'margin': '40px',
			# 	'display': 'inline',
			# 	# 'max-height':'600px',
			# 	'width': '40%',
			# 	'textAlign': 'justify',
			# 	'height': '70vh',
			# 	},
			children=[
				dcc.Graph(id='id-fra-line-graph',
						  style={
							  # 'text-align':'left',
							  # 'height':'40vh',
							  # 'margin-bottom':'0px',
							},
							hoverData={'points': [{'customdata': 'm1'}]}),
				# dcc.Store(id='intermediate-value-fra',storage_type='memory',data={}),
				],
   				style={"width": "50%", "display": "none"}
			),
			html.Div(
				[
					html.Div(
						[
							html.Div(
								[
									dcc.Dropdown(
										id="crossfilter-xaxis-column",
										options=[
											{"label": i, "value": i}
											for i in indicator["indicator"].unique()
										],
										value="A",
									)
								],
								style={"width": "50%", "display": "none"},
							)
						]
					),  # inline-block
					html.Div(
						[
							dcc.Graph(
								id="crossfilter-indicator",
								hoverData={"points": [{"customdata": "1m"}]},
							)
						],
						style={"width": "32%", "display": "inline-block", "padding": "0 20"},
					),
					html.Div(
						[dcc.Graph(id="x-time-series")],
						style={"width": "32%", "display": "inline-block"},
					),
				]
			),
		],
	className='row',
	)


@app.callback(
	Output('table1','data'),
	[Input('table1','data_timestamp')],
	[State('table1','data')])
def update_columns(timestamp,rows):
	dfr = pd.DataFrame.from_dict(rows)
	dfr = dfr[df.columns.copy()]
	dfr = table1_update(dfr)

	return dfr.to_dict('records')


@app.callback(
	Output('id-fra-line-graph', 'figure'),
	[Input('table1', 'data')],
	# [State('table1', 'data')]
	)
def display_outputtt(rows):
	dfr = pd.DataFrame.from_dict(rows).copy()
	dfr = dfr['fracam_os'][4:14].values
	return crea_fra_scatter_graph(dfr)


@app.callback(
    Output("crossfilter-indicator", "figure"),
    [Input('table1', 'data'),
     Input("crossfilter-xaxis-column", "value")],
)
def update_graph(rows, xaxis_column_name):
    
	l = ['1m', '2m', '3m', '4m', '5m', '6m', '9m', '12m', '18m', '2y']
    
	dfr = pd.DataFrame.from_dict(rows).copy()
	auxiliar = dfr.iloc[4:14, [18, 4, 7]] # * Crea archivo tenor.csv
	auxiliar.insert(3, "indicator", "A")
	# auxiliar.to_csv("tenors.csv", index=False)

	df = auxiliar.loc[auxiliar["indicator"] == xaxis_column_name]
 
	trace_fra = go.Scatter(
        x=l,
        y=df["fracam_os"],
        customdata=auxiliar["tenor"],
        mode='lines+markers+text',
        name='lines+markers',
        line=dict(
            shape='spline',
            color=('#4176A4')
        ),
        opacity=0.8,
        text=np.array([str(round(x, 2)) for x in auxiliar["fracam_os"]]),
        textposition='top center',
        textfont=dict(size=12),
    )
 
	layout = dict(
	    title='FRA 1 month IRS CAM off-shore (f1m-os) ',
	    titlefont=dict(size=13),
	    xaxis=dict(
	        zeroline=False,
	        automargin=True
	    ),
	    yaxis=dict(
	        zeroline=False,
	        automargin=True,
	        titlefont=dict(size=10, ),
	        # size=8,
	    ),
	    # height=400,
	    margin=dict(l=55, b=50, r=65),
	)

	fig = dict(data=[trace_fra], layout=layout)
 
	return fig
 
 
def create_time_series(dff):

    return {
        "data": [go.Scatter(x=dff.iloc[:, 0], y=dff.iloc[:, 1]*100, 
                            mode="lines+markers",
                            name='FRA history',
                            line=dict(
         		   				shape='spline',
            					color=('#4176A4')
        					),
        					opacity=0.8
             				)],
        "layout": go.Layout(
            title="IRS CAM off-shore: FRA 1 month history",
        	titlefont=dict(size=13),
        # 	xaxis=dict(
        #    automargin=True,
        #    rangeselector=dict(buttons=list([
        #        dict(count=1, label='1m', step='month', stepmode='backward'),
        #        dict(count=6, label='6m', step='month', stepmode='backward'),
        #        dict(step='all'),
        #    ])),
        #    rangeslider=dict(visible=True),
        #    type='date',
        #    titlefont=dict(size=10)
        #	),
         	yaxis=dict(
            	automargin=True,
            	titlefont=dict(size=10),
				hoverformat = '.2f'
        	),
        	margin=dict(l=55, b=50, r=65)
        ),
    }

@app.callback(
    Output("x-time-series", "figure"),
    [Input("table1", "data"),
     Input("crossfilter-indicator", "hoverData")],
)

def update_y_timeseries(rows, hoverData):
    
	dfr = pd.DataFrame.from_dict(rows).copy()	
	auxiliar = dfr.iloc[4:14, [18, 4, 7]] # * Crea archivo tenor.csv
	auxiliar.insert(3, "indicator", "A")
	col_name = hoverData["points"][0]["customdata"]
	row_value = auxiliar.loc[auxiliar["tenor"] == col_name].iloc[:, 2]
	dff = fra_historic[["date", col_name]]
	dff.iloc[-1, dff.columns.get_loc(col_name)] = float(row_value / 100)
	dff = dff.iloc[0:390]
	return create_time_series(dff)


""" https://community.plot.ly/t/two-graphs-side-by-side/5312 """








































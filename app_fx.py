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
pd.options.mode.chained_assignment = None #apaga warning set with copy

import numpy as np
from numbers import Number

from funcs_co import imp_spot, imp_clos_t, live, cam_os_simp, fra1m, fra1m_v2,fra1w,iptos, ibasis
from funcs_co import weird_division, round_conv_basis, round_2d, float_or_zero, fra1w_v

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

		df.icam_os = df.apply(lambda x: cam_os_simp(x.carry_days, spot, x.ptos, x.ilib), axis=1)

		# df.icam_os= df.apply(lambda x: cam_os_simp(x.carry_days if x.carry_days!=0 else float('Nan'),
		# 										   spot, x.ptos , x.ilib),axis=1)

		# df.fracam_os = fra1m_v2(df[['tenor', 'carry_days', 'icam_os']], interp=False)

		df.fracam_os = fra1w_v(df[['days','icam_os']])

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
						{'id':'days',      'name':'days',     'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'ptosy',     'name':'ptosy',    'editable':False, 'type': 'numeric'},
						{'id':'ptos',      'name':'ptos',     'editable':True,  'type': 'numeric'},
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
							}),

				# ! guarda un objeto escondido, utilitario, la curva fra de hoy
				dcc.Store(id='intermediate-value-fra',storage_type='memory',data={}),

				]
			),
		html.Div(
			dcc.Graph(id='id-fra-hist-line-graph',
					style={
						# 'textAlign':'right',
						# 'height':'50vh',
						# 'margin-top':'0px',
						}),
			className='four columns',
			),
		],
	className='row',
	)


@app.callback(
	Output('table1','data'),
	[Input('table1','data_timestamp')],
	[State('table1','data')]) # ! este q "state" creo que pega la tabla html en la app.
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
	Output('id-fra-hist-line-graph', 'figure'),
	[Input('intermediate-value-fra', 'modified_timestamp')],
	[State('intermediate-value-fra', 'data')])
def update_fra_hist_graph(timestamp, data):
	if timestamp is None:
		raise PreventUpdate
	print(crea_fra_hist_line( data['4'] ))
	return crea_fra_hist_line( data['4'] )


""" https://community.plot.ly/t/two-graphs-side-by-side/5312 """








































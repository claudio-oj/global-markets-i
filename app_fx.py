import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import dash_table
from dash_table.Format import Format  # https://dash.plot.ly/datatable/typing
import plotly.graph_objs as go

import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
from numbers import Number


""" CORRE INICIO PROCESOS """

from app import app

import funcs_co as fc
from graphs import crea_fra_scatter_graph

# importa fechas batch fec0, y fecha de uso fec1 = fec0 + 1
fec0,fec1 = pd.read_excel('./batch/bbg_hist_dnlder_excel.xlsx', sheet_name='valores', header=None).iloc[0:2,1]

fra_historic = pd.read_csv("./batch/fra_history.csv")
fra_hist_total = pd.read_pickle("./batch/hist_total_fra.pkl")
indicator = pd.read_csv("indicator.csv")
dfNone = pd.DataFrame(data=None,index=np.arange(1,11,1,int),columns=['spread','fra'])


""" SECCION INICIALIZA TABLA PRINCIPAL """
df1 = pd.read_pickle("./batch/table1_init.pkl")


""" SECCION INICIALIZA TABLA CALCULADORA FX """ # lo hago al inicio para no duplicar el proceso en la func del callback
df2 = pd.DataFrame(index=[0, 1, 2],columns=['name', 'pub_days','dates','ptos','4','5','6'])
df2.loc[0, 'name':'pub_days'] = ['short-leg', 7]
df2.loc[1, 'name':'pub_days'] = ['long-leg', 30]


def table1_update(df):
	try:
		for c in ['ptos','ptosy','odelta']:
			df[c] = df[c].map(fc.float_or_zero)

		spot = df.odelta[0]

		df[1:].odelta = df[1:].ptos - df[1:].ptosy
		# if x==0 for x in

		df.ddelta = 100 * df.apply(lambda x: fc.weird_division(x.odelta, x.carry_days),axis=1)

		df.carry  = df.apply(lambda x: df.days[4] * fc.weird_division(x.ptos, x.carry_days),axis=1)

		df.icam_os = df.apply(lambda x: fc.cam_os_simp(x.carry_days, spot, x.ptos, x.ilib), axis=1)

		df.fracam_os = fc.fra1w_v(df[['days','icam_os']])

		df.i_ptos = df.apply(lambda x: fc.iptos(t=x.carry_days if x.carry_days!=0 else float('nan'),
								 spot=spot, iusd=x.ilib, icam=x.icam, b= x.basis,
								 tcs=x.tcs),axis=1)

		df.i_basis = df.apply(lambda x: fc.ibasis(t=x.carry_days if x.carry_days!=0 else float('nan'),
								 spot=spot, iusd=x.ilib, icam=x.icam, ptos= x.ptos,
								 tcs=x.tcs),axis=1)

		df = df.applymap(fc.round_2d)
		df[['basis','i_basis']] = df[['basis','i_basis']].applymap(fc.round_conv_basis)
		return df

	except:
		return df
df1 = table1_update(df1)

# noinspection PyUnboundLocalVariable
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
					data= df1.to_dict('rows_table1'),
					columns= [
						{'id':'ind',       'name':'ind',      'editable':True, 'hidden':True, 'type': 'numeric'},
						{'id':'tenor',     'name':'t',    'editable':True, 'hidden': False,'width': '40px'},
						{'id':'daysy',     'name':'daysy',    'editable':True, 'hidden': True, 'type': 'numeric'},
						{'id':'days',      'name':'days',     'editable':True, 'hidden': True, 'type': 'numeric'},
						{'id':'ptosy',     'name':'ptsy',    'editable':True, 'type': 'numeric'},
						{'id':'ptos',      'name':'pts',     'editable':True,  'type': 'numeric'},
						{'id':'odelta',    'name':'+-',   'editable':True, 'hidden': False, 'type': 'numeric'},
						{'id':'ddelta',    'name':'ddelta',   'editable':True, 'hidden': True, 'type': 'numeric'},
						{'id':'carry',     'name':'carry',    'editable':True, 'hidden': True, 'type': 'numeric'},
						{'id':'icam',      'name':'icam',     'editable':True, 'hidden': False, 'type': 'numeric'},
						{'id':'ilib',      'name':'ilib',     'editable':True, 'hidden': False, 'type': 'numeric'},
						{'id':'tcs',       'name':'tcs',      'editable':True, 'hidden': True, 'type': 'numeric'},
						{'id':'icam_os',   'name':'icam-os',  'editable':True, 'hidden': True, 'type': 'numeric'},
						{'id':'fracam_os', 'name':'fra-os',   'editable':True, 'hidden': False, 'type': 'numeric'},
						{'id':'basisy',    'name':'basisy',   'editable':True, 'hidden': True, 'type': 'numeric'},
						{'id':'basis',     'name':'basis',    'editable':True, 'type': 'numeric'},
						{'id':'i_ptos',    'name':'i-pts',   'editable':True, 'type': 'numeric'},
						{'id':'i_basis',   'name':'i-basis',  'editable':True, 'type': 'numeric'},
						{'id':'blank',   'name':'',  'editable':True},
						],
					style_as_list_view= True,
					n_fixed_rows=1,
					# fixed_rows={ 'headers': True, 'data': 0 },
					style_table={
						# 'margin':'5px',
						'height': '460px',
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
						{'if': {'column_id':'tenor'}, 'width': '31px'},
						{'if': {'column_id':'days'}, 'width': '32px'},
						{'if': {'column_id':'ptosy'}, 'width': '40px', 'color': 'rgb(204, 205, 206)'},
						{'if': {'column_id':'ptos'}, 'width': '45px', 'fontWeight': 600, 'color': '#4176A4'},
						{'if': {'column_id':'odelta'}, 'width': '42px'},
						{'if': {'column_id':'ddelta'}, 'width': '48px'},
						{'if': {'column_id':'carry'}, 'width': '48px'},
						{'if': {'column_id':'icam'}, 'width': '48px'},
						{'if': {'column_id':'ilib'}, 'width': '48px'},
						{'if': {'column_id':'fracam_os'}, 'width': '50px'},
						{'if': {'column_id':'basis'}, 'width': '48px', 'fontWeight': 600, 'color': '#81C3D7'},
						{'if': {'column_id':'i_ptos'}, 'width': '50px','fontWeight': 600,'color':'#4176A4','backgroundColor':'rgb(251,251,251)'}, #20A4F3
						{'if': {'column_id':'i_basis'}, 'width': '50px','fontWeight': 600,'color':'#81C3D7','backgroundColor':'rgb(251,251,251)'},
						{'if': {'column_id':'blank'}, 'width': '2px', 'backgroundColor':'rgb(251,251,251)'},
						],
					editable=True,
					style_data_conditional=[
						{
							'if':{
								'column_id':'odelta',
								'filter':'{odelta} >= 0.01',
							},
							'color':'mediumseagreen',
						},
						{
							'if':{
								'column_id':'odelta',
								'filter':'{odelta} <= -0.01',
							},
							'color':'red',
						},
					]
					),
				dash_table.DataTable(
					id='table2',
					data=df2.to_dict('rows_table2'),
					columns=[
						{'id':'name', 'name':'name', 'editable':True},
						{'id':'pub_days', 'name':'pub-days', 'editable':True, 'type': 'numeric'},
						{'id':'dates', 'name':'dates', 'editable':True},
						{'id':'ptos', 'name':'pts'},
						{'id':'4', 'name':' '},
						{'id':'5', 'name':' '},
						{'id':'6', 'name':' '},
					],
					editable=True,
					style_as_list_view= True,
					style_data_conditional=[
						{
							'if':{'row_index': 2},
							'fontWeight': 600,
							'color':'#4176A4',
						},
					]
					# style_table={'width':'170px'},
					),
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
				html.Div(
					[
						dcc.Graph(
							id="grafico1",
							hoverData={"points": [{"customdata": "1m"}]},
						)
					],
					# style={"width": "32%", "display": "inline-block", "padding": "0 20"},
				),
				html.Div(dcc.Graph(id='grafico3')),
				],
			),
			html.Div(
				[
					html.Div(
						[
							html.Div(
								[
									dcc.Dropdown(
										id="data-escondida",
										options=[
											{"label": i, "value": i}
											for i in indicator["indicator"].unique()
										],
										value="A",
									)
								],
								style={"display": "none"},
							)
						]
					),

					html.Div(
						[dcc.Graph(id="grafico2")],
						# style={"width": "100%", "display": "inline-block"},
					),
					html.Div(
						[
							dcc.Input(id='spread-finder-input-days',type='text',value='7,45',
									  style={'width':'20%'}),
							dcc.Input(id='spread-finder-input-gap' ,type='text',value='5,10',
									  style={'width':'20%'}),
							html.Button('Submit', id='spreads-finder-button'),
						],
						className="dcc-inputs-css",
					),
					# html.Div(
					# 	[
					#
					# 	],
					# 	className="dcc-button-css",
					# ),
					html.Div(
						[
							dash_table.DataTable(
								id='table-cheap',
								columns=[
									{'id':'spread', 'name':'spread'},
									{'id':'fra', 'name':'fra'},
								],
								data=dfNone.to_dict('records'),
								style_as_list_view= True,
								style_table={'width':'50%'},
							),
							dash_table.DataTable(
								id='table-rich',
								columns=[
									{'id':'spread', 'name':'spread'},
									{'id':'fra', 'name':'fra'},
								],
								data=dfNone.to_dict('records'),
								style_as_list_view= True,
								style_table={'width':'50%'},
							),
						],
						style={"display": "inlineBlock"},
					),
				],
			className='four columns',
			),

		dcc.Store(id='data-grafico3', storage_type='local')
	],
	className='row',
	style={'height': '50%','width':'100%','max-height':'600px'},
)


"""
##################################################################################
##################################################################################
"""

@app.callback(
	[Output('table1','data'), Output('table2','data'), Output('data-grafico3','data')],
	[Input('table1','data_timestamp'), Input('table2','data_timestamp')],
	[State('table1','data'), State('table2','data')])
def update_tables_cback(timestamp1,timestamp2,rows1,rows2):
	dft1 = pd.DataFrame.from_dict(rows1)
	dft2 = pd.DataFrame.from_dict(rows2)

	# SANITY CHECKS: pisa las col según data original. para bloquear typos ...
	dft1.tenor = df1.tenor
	dft1.ptosy = df1.ptosy
	if dft2.loc[0,'pub_days'] > 370:
		dft2.loc[0, 'pub_days'] = 370
	if dft2.loc[1,'pub_days'] > 370:
		dft2.loc[1, 'pub_days'] = 370
	if dft2.loc[0,'pub_days'] >= dft2.loc[1,'pub_days']:
		dft2.loc[1, 'pub_days'] = dft2.loc[0,'pub_days'] + 1


	# ordena las columnas según orden original (el dict las "ordena" alfabeticamente)
	dft1 = dft1[df1.columns.copy()]
	dft2 = dft2[df2.columns.copy()]

	""" FUNCIÓN UPDATE TABLE1 """
	dft1 = table1_update(dft1)

	""" FUNCIÓN UPDATE TABLE2 """
	dft2['name'] = ['short-leg','long-leg','spread']

	for c in ['pub_days','ptos']:
		dft2[c] = dft2[c].map(fc.float_or_None)
	dft2.loc[:2, 'ptos'] = np.interp(x=dft2.loc[:2,'pub_days'],xp=dft1[:14].days.values,fp=dft1[:14].ptos.values).round(2)

	# calcula la fra implicita en el spread TODO: Aquiiiiiiiiiiiiiii fracam_os
	fras_array = np.interp(x=dft2.loc[:2,'pub_days'], xp=dft1.days.values,fp=dft1.icam_os.values).round(2)
	dft2.loc[2, '4'] = round(fc.fra1w(w2=dft2.iloc[1, 1], w1=dft2.iloc[0, 1], i2=fras_array[1], i1=fras_array[0]),2)

	# ultima fila ptos la resta de las dos primeras
	dft2.loc[2, 'ptos'] = round(dft2.loc[1, 'ptos'] - dft2.loc[0, 'ptos'], 2)

	# setea nombres en la fila
	dft2.loc[1, '4':'6'] = ['fra','rank_tod','rank_his']

	# calcula rank percentil "transversal" de la fra del spread
	_ = fc.rank_perc(x=dft2.loc[2,'4'],array=np.interp(x=np.arange(1,371,1,int),xp=dft1.days.values,fp=dft1.fracam_os.values))
	dft2.loc[2, '5'] = str( _ ) + '/100'

	# calcula rank percentil "historico" de la fra del spread
	w2 = dft2.iloc[1,1]
	w1 = dft2.iloc[0,1]
	slice_ = fra_hist_total[[w1,w2]]
	slice_['fra'] = slice_.apply(lambda x: round( fc.fra1w(w2=w2,w1=w1,i2=x[w2],i1=x[w1]), 2) , axis=1)
	_ = fc.rank_perc(x=dft2.loc[2, '4'],array=slice_.fra)
	dft2.loc[2, '6'] = str( _ ) + '/100'

	# append fra de hoy en dataframe "slice_" , es input para --> grafico3
	slice_.loc[fec1] = [None,None,dft2.loc[2,'4']]

	return dft1.to_dict('rows_table1'), dft2.to_dict('rows_table2'), slice_.fra.to_json()



@app.callback(
    Output("grafico1", "figure"),
    [Input('table1', 'data'),
     Input("data-escondida", "value")],
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
        # opacity=0.8,
        text=np.array([str(round(x, 2)) for x in auxiliar["fracam_os"]]),
		hoverinfo='x',
        textposition='top center',
        textfont=dict(size=12),
    )

	layout = dict(
	    title='IRS CAM FRA-os per tenor ',
	    titlefont=dict(size=13),
	    xaxis=dict(
	        zeroline=False,
			showgrid=False,
	        automargin=True
	    ),
	    yaxis=dict(
	        zeroline=False,
			showgrid=False,
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
                            mode="lines",
                            name='FRA history',
                            line=dict(
         		   				shape='spline',
            					color=('#73BA9B')  #92B6B1 otro verde ...
        					),
        					opacity=0.8
             				)],
        "layout": go.Layout(
            title="IRS CAM FRA-os history",
        	titlefont=dict(size=13),
        	xaxis=dict(
				showgrid=False,
        #    automargin=True,
        #    rangeselector=dict(buttons=list([
        #        dict(count=1, label='1m', step='month', stepmode='backward'),
        #        dict(count=6, label='6m', step='month', stepmode='backward'),
        #        dict(step='all'),
				),
        #    rangeslider=dict(visible=True),
        #    type='date',
        #    titlefont=dict(size=10)
        #	),
         	yaxis=dict(
            	# automargin=True,
				range= [0, 4.3],
				zeroline=False,
				showgrid=False,
            	titlefont=dict(size=10),
				hoverformat = '.2f'
        	),
        	margin=dict(l=55, b=50, r=65)
        ),
    }

@app.callback(
    Output("grafico2", "figure"),
    [Input("table1", "data"),
     Input("grafico1", "hoverData")],
)
def update_y_timeseries(rows, hoverData):
	dfr = pd.DataFrame.from_dict(rows).copy()
	auxiliar = dfr.iloc[4:14, [18, 4, 7]] # * Crea archivo tenor.csv
	auxiliar.insert(3, "indicator", "A")
	col_name = hoverData["points"][0]["customdata"]
	row_value = auxiliar.loc[auxiliar["tenor"] == col_name].iloc[:, 2]
	dff = fra_historic[["date", col_name]]
	dff.iloc[-1, dff.columns.get_loc(col_name)] = float(row_value / 100) # TODO: aqui esta la division por 100 q quiero elminar
	dff = dff.iloc[0:390]
	return create_time_series(dff)



@app.callback(
	Output('grafico3','figure'),
	[Input('table2','data_timestamp'),Input('data-grafico3','data')]
)
def update_grafico3(timestamp,rows):
	series = pd.read_json(rows,typ='series')

	trace = go.Scatter(
        x=series.index,
        y=series,
        # customdata=auxiliar["tenor"],
        mode='lines',
        # name='lines+markers',
        line=dict(
            shape='spline',
            color=('#73BA9B')
        ),
        opacity=0.8,
        # text=np.array([str(round(x, 2)) for x in auxiliar["fracam_os"]]),
        textposition='top center',
        textfont=dict(size=12),
    )

	layout = dict(
	    title='FRA-os implicit in spread ',
	    titlefont=dict(size=13),
	    xaxis=dict(
	        zeroline=False,
			showgrid=False,
	        automargin=True
	    ),
	    yaxis=dict(
	        zeroline=False,
			showgrid=False,
	        automargin=True,
	        titlefont=dict(size=10, ),
	        # size=8,
	    ),
	    # height=400,
	    margin=dict(l=55, b=50, r=65),
	)

	fig = dict(data=[trace], layout=layout)

	return fig


@app.callback(
	[Output('table-cheap','data'),Output('table-rich','data')],
	[Input('spreads-finder-button','n_clicks')],
	[State('spread-finder-input-days','value'),State('spread-finder-input-gap','value'),
	 State('table1','data')],
)
def run_spread_finder(n_clicks,range_days,gap,rows):
	dft1 = pd.DataFrame.from_dict(rows)
	dft1 = dft1.set_index('days')['icam_os']
	range_days = [int(x) for x in range_days.split(',')]
	gap        = [int(x) for x in gap.split(',')]

	dfaux = fc.spreads_finder(range_days=range_days,gap=gap,icamos=dft1)

	# return tables cheap & rich
	return dfaux['cheap'].to_dict('rows-table-cheap'), dfaux['rich'].to_dict('rows-table-rich')






































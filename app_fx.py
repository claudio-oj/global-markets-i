import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import dash_table
from dash_table.Format import Format  # https://dash.plot.ly/datatable/typing

# import plotly.plotly as py
import plotly.graph_objs as go
# from plotly.tools import make_subplots

import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
from numbers import Number


""" CORRE INICIO PROCESOS """

from app import app

import funcs_co as fc
import funcs_calendario_co as fcc
import graphs as graphs

# importa fechas batch fec0, y fecha de uso fec1 = fec0 + 1
fec0,fec1      = pd.read_excel('./batch/bbg_hist_dnlder_excel_v2.xlsx', sheet_name='valores', header=None).iloc[0:2,1]
spot0          = pd.read_pickle("./batch/p_clp_spot.pkl")[-1]
fra_historic   = pd.read_csv("./batch/fra_history.csv",index_col=0)
spread_hist    = pd.read_csv("./batch/spread_g2_history.csv",index_col=0)
fra_hist_total = pd.read_pickle("./batch/hist_total_fra.pkl")
calendario_fx  = pd.read_csv("./batch/calendario_app_fx.csv")
teo            = pd.read_pickle("./batch/ptos_teoricos.pkl")

dfNone = pd.DataFrame(data=' ',index=np.arange(1,6,1,int),columns=['days','int','Px','ΔPx'])


""" SECCION INICIALIZA TABLA PRINCIPAL """
df1 = pd.read_pickle("./batch/table1_init.pkl")


""" SECCION INICIALIZA TABLA CALCULADORA FX """ # lo hago al inicio para no duplicar el proceso en la func del callback
df2 = pd.DataFrame(index=[0, 1, 2],columns=['name', 'pub_days','dates','ptos','4','5','6'])
df2.loc[0, 'name':'pub_days'] = ['short-leg', 7]
df2.loc[1, 'name':'pub_days'] = ['long-leg', 28]


def table1_update(df,spot):
	try:
		for c in ['ptos','ptosy','odelta']:
			df[c] = df[c].map(fc.float_or_zero)

		df[1:].odelta = df[1:].ptos - df[1:].ptosy
		df.odelta = df.odelta.round(2)

		# estas metricas no las estamos mostrando --> x eso están desactivadas
		# df.ddelta = 100 * df.apply(lambda x: fc.weird_division(x.odelta, x.carry_days),axis=1)
		# df.carry  = df.apply(lambda x: df.days[4] * fc.weird_division(x.ptos, x.carry_days),axis=1)

		#interpolate icam, ilib, en los plazos que no son operables.
		days_interp = df.set_index('tenor').drop(labels=['TOM', '1w', '2w', '1m', '2m', '4m', '5m'])['carry_days'].values
		for c in ['icam','ilib']:
			i_interp = df.set_index('tenor').drop(labels=['TOM','1w','2w','1m','2m','4m','5m'])[c].values
			df[c] = np.round(np.interp(x=df.carry_days,xp=days_interp,fp=i_interp),2)

		df.ptoso[5:] = df.ptoso_p[5:] + df.ptos[4]

		df.ilibz = df.apply(lambda x: fc.comp_a_z(x.carry_days, x.ilib, periodicity=90), axis=1)
		df.icam_osz = df.apply(lambda x: fc.cam_os_simp(x.carry_days, spot, x.ptos, x.ilibz), axis=1)
		df.icam_os[:13] = df.icam_osz[:13]
		df.icam_os[13:] = df[13:].apply(lambda x: fc.z_a_comp(x.carry_days, x.icam_osz), axis=1)

		df.fracam_os = fc.fra1w_v(df[['carry_days','icam_os']])

		df.icamz[:13] = df.icam[:13].values
		df.icamz[13:] = df[13:].apply(lambda x: fc.comp_a_z(x.carry_days, x.icam, periodicity=180), axis=1)

		df.i_ptos = df.apply(lambda x: fc.iptos(t=x.carry_days if x.carry_days!=0 else float('nan'),
								 spot=spot, iusd=x.ilib, icam=x.icam, b= x.basis,
								 tcs=x.tcs),axis=1)

		df.i_basis = df.apply(lambda x: fc.ibasis(t=x.carry_days if x.carry_days!=0 else float('nan'),
								 spot=spot, iusd=x.ilib, icam=x.icam, ptos= x.ptos,
								 tcs=x.tcs),axis=1)

		df[['basis','i_basis']] = df[['basis','i_basis']].applymap(fc.round_conv_basis)
		df = df.applymap(fc.round_2d)

		df['show'] = [1,0,0,0,0,0,1,0,0]+[1 for x in range(1,14)] # para style cell conditional, define si se muestra

		return df

	except:
		return df
df1 = table1_update(df1,spot=spot0)

def table2_update(dft1,dft2):
	""" actualiza la tabla 2
	:param:
		dft1: pd.Dataframe imagen inicio table1
		dft1: pd.Dataframe imagen inicio table2
	:return: pd.Dataframe 	"""

	dft2['name'] = ['short-leg', 'long-leg', 'spread']

	# Sanity checks
	if dft2.loc[0,'pub_days'] > 370:
		dft2.loc[0, 'pub_days'] = 370
	if dft2.loc[1,'pub_days'] > 370:
		dft2.loc[1, 'pub_days'] = 370
	if dft2.loc[0,'pub_days'] >= dft2.loc[1,'pub_days']:
		dft2.loc[1, 'pub_days'] = dft2.loc[0,'pub_days'] + 1

	for c in ['pub_days', 'ptos']:
		dft2[c] = dft2[c].map(fc.float_or_None)
	dft2.loc[:2, 'ptos'] = np.interp(x=dft2.loc[:2, 'pub_days'], xp=dft1[:14].days.values,
									 fp=dft1[:14].ptos.values).round(2)

	dft2[:2]['dates'] = (dft2[:2].apply(lambda x: fcc.date_output(fec1, x.pub_days), axis=1)).to_list()

	# calcula la fra implicita en el spread
	fras_array = np.interp(x=dft2.loc[:2, 'pub_days'], xp=dft1.carry_days.values, fp=dft1.icam_os.values)
	dft2.loc[2, '4'] = round(fc.fra1w(w2=dft2.iloc[1, 1], w1=dft2.iloc[0, 1], i2=fras_array[1], i1=fras_array[0]), 2)

	# ultima fila ptos la resta de las dos primeras
	dft2.loc[2, 'ptos'] = round(dft2.loc[1, 'ptos'] - dft2.loc[0, 'ptos'], 2)

	# setea nombres en la fila
	dft2.loc[1, '4':'6'] = ['icam-os', 'rank_tod', 'rank_his']

	# calcula rank percentil "transversal" de la fra del spread
	rt = fc.rank_perc(x=dft2.loc[2, '4'],
					 array=np.interp(x=np.arange(1, 371, 1, int), xp=dft1.days.values, fp=dft1.fracam_os.values))
	dft2.loc[2, '5'] = str(rt) + '/100'

	# calcula rank percentil "historico" de la fra del spread
	w2 = dft2.iloc[1, 1]
	w1 = dft2.iloc[0, 1]
	slice_ = fra_hist_total[[w1, w2]]
	slice_['fra'] = slice_.apply(lambda x: round(fc.fra1w(w2=w2, w1=w1, i2=x[w2], i1=x[w1]), 2), axis=1)
	slice_.loc[fec1] = [None, None, dft2.loc[2, '4']]

	rh = fc.rank_perc(x=dft2.loc[2, '4'], array=slice_.fra)
	dft2.loc[2, '6'] = str(rh) + '/100'

	t1 = "This spread on 'Today's Curve' ranking is at {}/100 --> {}".format(rt,fc.parse_perc_range(rt))
	t2 = "This spread on '1yr Self History' ranking is at {}/100 --> {}".format(rh,fc.parse_perc_range(rh))

	return dft2, slice_.fra, t1, t2
df2,slice_fra, t1, t2 = table2_update(df1,df2)



layout = html.Div(
	# style={'display':'block'},
	children=[
		html.Div(
		className='row',
		style={'height': '50%', 'width': '100%', 'max-height': '600px'},
		children=[
			html.Div(
				className='four columns',
				children=[
					html.Div(
						className='row',
						style={'fontSize': '12px','float':'center'},
						children=[
							html.Div([
								dcc.Input(id='spot-input', type='number', value=spot0,
										  style={'height': '50%',
												 'width': '75%',
												 'padding-top':'6px',
												 'marginTop':4,
												 }),
							],
							className='three columns',
							),

							html.Div([
								html.P('Ready to use on {}'.format(fec1.date()),
									   style={'padding-top': '10px',
											  'marginBottom': 5,
										},
								),
							],
							className='five columns',
							),

							html.Div([
								dcc.RadioItems(
									id='radio-item',
									options=[
										{'label': 'local', 'value': 'lcl'},
										{'label': 'off-shore', 'value': 'os'},
									],
									value='lcl',
									labelStyle={'display': 'inline-block'},
								),
							],
							className='four columns',
							style={'padding-top': '10px',},
							),
						],
					),


					dash_table.DataTable(
						id='table1',
						data= df1.to_dict('rows_table1'),
						columns= [
							{'id':'ind',       'name':'ind',      'editable':True, 'hidden':True, 'type': 'numeric'},
							{'id':'tenor',     'name':'t',    'editable':True, 'hidden': False,'width': '40px'},
							{'id':'daysy',     'name':'daysy',    'editable':True, 'hidden': True, 'type': 'numeric'},
							{'id':'days',      'name':'days',     'editable':True, 'hidden': True, 'type': 'numeric'},
							{'id':'ptosy',     'name':'ptsy',    'editable':True, 'hidden': True, 'type': 'numeric'},
							{'id':'ptos',      'name':'ptslcl',     'editable':True,  'type': 'numeric'},

							{'id':'odelta',    'name':'+-',   'editable':True, 'hidden': False, 'type': 'numeric'},
							{'id':'ptoso_p',   'name':'ptsos',     'editable':True,  'type': 'numeric'},

							{'id':'ddelta',    'name':'ddelta',   'editable':True, 'hidden': True, 'type': 'numeric'},
							{'id':'carry',     'name':'carry',    'editable':True, 'hidden': True, 'type': 'numeric'},
							{'id':'icam',      'name':'icam',     'editable':True, 'hidden': False, 'type': 'numeric'},
							{'id':'ilib',      'name':'irslibor',     'editable':True, 'hidden': False, 'type': 'numeric'},
							{'id':'tcs',       'name':'tcs',      'editable':True, 'hidden': True, 'type': 'numeric'},
							{'id':'icam_os',   'name':'icamos',  'editable':True, 'hidden': True, 'type': 'numeric'},
							{'id':'fracam_os', 'name':'fra',   'editable':True, 'hidden': True, 'type': 'numeric'},
							{'id':'basisy',    'name':'bsisy',   'editable':True, 'hidden': True, 'type': 'numeric'},
							{'id':'basis',     'name':'bsis',    'editable':True, 'type': 'numeric'},
							{'id':'i_ptos',    'name':'ipts',   'editable':True, 'type': 'numeric'},
							{'id':'i_basis',   'name':'ibsis',  'editable':True, 'type': 'numeric'},
							{'id':'blank',   'name':'',  'editable':True},
							],
						style_as_list_view= True,
						n_fixed_rows=1,
						style_header={'textAlign':'right'},
						# fixed_rows={ 'headers': True, 'data': 0 },
						style_table={
							# 'margin':'5px',
							'height': '460px',
							'width':'100%',
							'overflowY': 'auto',
							},
						style_cell_conditional=[
							# {'if': {'column_id':'tenor'}, 'width': '30px'},
							# {'if': {'column_id':'days'}, 'width': '32px'},
							# {'if': {'column_id':'ptosy'}, 'width': '39px', 'color': 'rgb(204, 205, 206)'},
							{'if': {'column_id':'ptos'}, 'fontWeight': 600, 'color': '#3C4CAD'},
							{'if': {'column_id':'ptoso_p'}, 'fontWeight': 600, 'color': '#F04393'},
							# {'if': {'column_id':'odelta'}, 'width': '42px'},
							# {'if': {'column_id':'ddelta'}, 'width': '48px'},
							# {'if': {'column_id':'carry'}, 'width': '48px'},
							# {'if': {'column_id':'icam'}, 'width': '45px'},
							# {'if': {'column_id':'ilib'}, 'width': '45px'},
							# {'if': {'column_id':'icam_os'}, 'width': '45px'},
							# {'if': {'column_id':'fracam_os'}, 'width': '45px'},
							{'if': {'column_id':'basis'}, 'fontWeight': 600, 'color': '#59C3C3'},
							{'if': {'column_id':'i_ptos'}, 'fontWeight': 600,'color':'#3C4CAD','backgroundColor':'rgb(250,250,250)'}, #20A4F3
							{'if': {'column_id':'i_basis'}, 'fontWeight': 600,'color':'#59C3C3','backgroundColor':'rgb(250,250,250)'},
							{'if': {'column_id':'blank'}, 'backgroundColor':'rgb(250,250,250)'},
							],
						editable=True,
						style_data_conditional=[
							{
								'if':{
									'column_id':'odelta',
									'filter':'{odelta} = 0',
								},
								'color':'white',
							},
							{
								'if':{
									'column_id':'odelta',
									'filter':'{odelta} > 0',
								},
								'color':'mediumseagreen',
							},
							{
								'if':{
									'column_id':'odelta',
									'filter':'{odelta} < 0',
								},
								'color':'#F04393', #rojo
							},
							{
								'if':{
									'column_id':'icam',
									'filter':'{show} eq 0',
									},
								'color': 'lightgray ',
							},
							{
								'if': {
									'column_id': 'ilib',
									'filter': '{show} eq 0',
								},
								'color': 'lightgray ',
							},
						]
						),
					dash_table.DataTable(
						id='table2',
						data=df2.to_dict('rows_table2'),
						columns=[
							{'id':'name', 'name':'name'},
							{'id':'pub_days', 'name':'pub-days', 'editable':True, 'type': 'numeric'},
							{'id':'dates', 'name':'dates'},
							{'id':'ptos', 'name':'pts'},
							{'id':'4', 'name':' '},
							{'id':'5', 'name':' '},
							{'id':'6', 'name':' '},
						],
						editable=True,
						style_header={'textAlign':'right'},
						style_as_list_view= True,
						style_data_conditional=[
							{
								'if':{'row_index': 2},
								'fontWeight': 600,
								'color':'#3C4CAD',
							},
						]
						),
					html.Div(
						id='output-table2-text1',
						style={'display':'inlineBlock', 'fontSize':'12px'},
					),
					html.Div(
						id='output-table2-text2',
						style={'display': 'inlineBlock', 'fontSize': '12px'},
					)
					]
				),

			html.Div(
				className='four columns',
				children=[
					html.Div(
						dcc.Graph(
							id='ubicacion1',
							),
						),
					html.Div(
						[
							dcc.Graph(
								id="ubicacion2",
							)
						],
					),
					],
				),

				html.Div(
					className='four columns',
					children=[
						html.Div([dcc.Graph(id="ubicacion3")]),
						html.Div([
							html.P(id='ptos-teoricos-texto1',style={'margin-block-end':0}),
							html.P(id='ptos-teoricos-texto2',style={'margin-block-end':0}),
							],
							style={
								'fontSize': '13px',
								'padding-top': '5px',
								'marginBottom': 5,

							},
						),
						html.Div(
							[
								dcc.Input(id='spread-finder-input-days',type='text',value='7-45',
										  style={'height':'50%','width':'15%'}),
								dcc.Input(id='spread-finder-input-gap' ,type='text',value='5-15',
										  style={'height':'50%','width':'15%'}),
								html.Button('Finder', id='spreads-finder-button',
											style={'width':'15%',"padding": "0 0 0 0"}),
								html.Div(id='output-finder-button',
										 style={'width':'85%',"padding": "0 0 0 0",'margin':'1px','display':'inlineBlock'}),
							],
							style={'fontSize':12,'display':'inlineBlock','padding-top':'10px'}
						),
						html.Div(
							[
								dash_table.DataTable(
									id='table-cheap',
									columns=[
										{'id':'days', 'name':'days'},
										{'id':'int', 'name':'int'},
										{'id':'p', 'name':'Px'},
										{'id':'c', 'name':'ΔPx'},
									],
									data=dfNone.to_dict('records'),
									style_as_list_view= True,
									style_cell={'minWidth': '50px', 'width': '80px', 'maxWidth': '85px'},
									style_table={'width':'50%','float':'left','textAlign':'left'},
									style_header={'textAlign':'right'},
								),
								dash_table.DataTable(
									id='table-rich',
									columns=[
										{'id':'days', 'name':'days'},
										{'id':'int', 'name':'int'},
										{'id':'p', 'name':'Px'},
										{'id':'c', 'name':'ΔPx'},
									],
									data=dfNone.to_dict('records'),
									style_as_list_view= True,
									style_cell={'minWidth': '50px', 'width': '80px', 'maxWidth': '85px'},
									style_table={'width':'50%','float':'right', 'padding-right': '50%',},
									style_header={'textAlign':'right'},
								),
							],
							style={"display": "inlineBlock"},
						),
					],
				),
		],
	),

	html.Div(
		className='row',
		style={'width': '35%', 'margin-top':'50px','float':'left','textAlign':'left'},
		children=[
			dash_table.DataTable(
				id='calendario-fx',
				data=calendario_fx.to_dict('records'),
				columns=[{"name": i, "id": i} for i in ['tenor','pubdays','fix','pub','val']],
				style_header={'textAlign':'center'},
			),
		]
	)

	]
)



"""
##################################################################################
##################################################################################
"""


@app.callback(
	[Output('table1','data'), Output('table2','data'),Output('output-table2-text1','children'),Output('output-table2-text2','children')],
	[Input('table1','data_timestamp'), Input('table2','data_timestamp'),Input('spot-input','n_blur')],
	[State('table1','data'), State('table2','data'),State('spot-input','value')])
def update_tables_cback(timestamp1,timestamp2,spot_submit,rows1,rows2,spot):

	dft1 = pd.DataFrame.from_dict(rows1)
	dft2 = pd.DataFrame.from_dict(rows2)

	# SANITY CHECKS: pisa las col según data original. para bloquear typos ...
	dft1.tenor = df1.tenor
	dft1.ptosy = df1.ptosy
	if dft2.loc[0,'pub_days'] not in np.arange(1,371,1,int) :
		dft2.loc[0, 'pub_days'] = 7
	if dft2.loc[1,'pub_days'] not in np.arange(1,371,1,int):
		dft2.loc[1, 'pub_days'] = 30
	if dft2.loc[0,'pub_days'] >= dft2.loc[1,'pub_days']:
		dft2.loc[1, 'pub_days'] = dft2.loc[0,'pub_days'] + 1

	# ordena las columnas según orden original (el dict las "ordena" alfabeticamente)
	dft1 = dft1[df1.columns.copy()]
	dft2 = dft2[df2.columns.copy()]

	dft1 = table1_update(dft1,spot=spot)
	dft2, slice_fra, t1, t2 = table2_update(dft1,dft2)

	return dft1.to_dict('rows_table1'), dft2.to_dict('rows_table2'), t1, t2



@app.callback(
	[Output('ubicacion1','figure')],
	[Input('table1','data')])
def update_ubicacion2(rows):
	df = pd.DataFrame.from_dict(rows)
	df = df.loc[2:13,['tenor','icamz','icam_osz','icam_os','fracam_os']]
	return [graphs.crea_graf_fra_lcl_os_spread(df)] # fig



@app.callback(
	Output('click-data','children'),
	[Input('ubicacion1','clickData')])
def display_click_data(clickData):
	return json.dumps(clickData)



@app.callback(
	Output("ubicacion2", "figure"),
	[Input('table1', 'data'), Input('radio-item','value')])
def update_graph1(rows,radioitem):
	radioitem
	df = pd.DataFrame.from_dict(rows)
	df = df.set_index('tenor')[['ptos','ptoso','ptoso_p']]
	df['ptos_lcl_1x'] = df.ptos - df.ptos['1m']

	if radioitem=='lcl':
		return graphs.graf_arb_lcl(df.applymap(fc.round_2d))
	else:
		return graphs.graf_arb_os(df.applymap(fc.round_2d))



@app.callback(
	[Output('ubicacion3','figure'),Output('ptos-teoricos-texto1','children'),Output('ptos-teoricos-texto2','children')],
	[Input('table1','data'),Input('ubicacion1','clickData'),Input('spot-input','value')])
def update_ubicacion3(rows,click,spot,fec1=fec1,teo=teo):
	try:
		t = click['points'][0]['x']
	except:
		t='12m'

	df = pd.DataFrame.from_dict(rows)

	cols = ['carry_days','ilibz','icamz','ptos']
	teo[t].loc[fec1, cols] = df.set_index('tenor').loc[t,cols]

	teo[t].loc[fec1,'ice_libor'] = teo[t].loc[fec1,'ilibz']+teo[t].loc[fec0,'ice_libor']-teo[t].loc[fec0,'ilibz']
	teo[t].loc[fec1, 'tab']      = teo[t].loc[fec1, 'icamz'] + teo[t].loc[fec0, 'tab'] - teo[t].loc[fec0, 'icamz']
	teo[t].loc[fec1, 'ptosteo']  = fc.ptos_teoricos(spot,teo[t].carry_days[-1],teo[t].ice_libor[-1],teo[t].tab[-1])
	teo[t].loc[fec1, 'spread']   = (36000/teo[t].carry_days[-1]) * (teo[t].ptos[-1] - teo[t].ptosteo[-1])/spot

	teo[t].loc[fec1,'spread_5':'spread_95'] = teo[t].loc[fec0,'spread_5':'spread_95']

	teo[t].loc[fec1, 'ptos_5']  = teo[t].carry_days[-1] * teo[t].spread_5[-1] * spot / 36000 + teo[t].ptosteo[-1]
	teo[t].loc[fec1, 'ptos_50'] = teo[t].carry_days[-1] * teo[t].spread_50[-1] * spot / 36000 + teo[t].ptosteo[-1]
	teo[t].loc[fec1, 'ptos_95'] = teo[t].carry_days[-1] * teo[t].spread_95[-1] * spot / 36000 + teo[t].ptosteo[-1]

	perc_ptos = fc.rank_perc(teo[t].spread[-1],teo[t].spread)

	df = teo[t][['ptos','ptos_5','ptos_50','ptos_95']]
	df.loc[fec1] = df.loc[fec1].map(fc.round_2d)

	""" texto para la bajada del grafico """
	texto1 = '`Fwd Points {}` at {} is {}, compared to rates differential index.'.format(t,df.ptos[-1],fc.parse_perc_range(perc_ptos))
	texto2=  '{} is at {}th percentile'.format(df.ptos[-1],perc_ptos)

	return graphs.crea_ptos_teo(t,df,fec1,perc_ptos) , texto1, texto2




# Ubicación 4
@app.callback(
	[Output('table-cheap','data'),Output('table-rich','data'),Output('output-finder-button','children')],
	[Input('spreads-finder-button','n_clicks')],
	[State('spread-finder-input-days','value'),State('spread-finder-input-gap','value'),
	 State('table1','data'),State('spot-input','value')])
def run_spread_finder(n_clicks,range_days,gap,rows,spot):
	dft1 = pd.DataFrame.from_dict(rows)
	icamos = dft1.set_index('carry_days')['icam_os']
	ptos = dft1.set_index('carry_days')['ptos']
	range_days = [int(x) for x in range_days.split('-')]

	if gap=='':
		dic_dfs = fc.suelto_finder(range_days=range_days,icamos=icamos, valuta=df1.days[0], fec=fec1,spot=spot,ptos=ptos)
		t = "Top-10 NDF:   within {}d - {}d curve. Results: Cheap on the left, Rich on the right".format(range_days[0],range_days[1])
		return dic_dfs['cheap'].to_dict('rows-table-cheap'), dic_dfs['rich'].to_dict('rows-table-rich'), t

	else:
		gap = [int(x) for x in gap.split('-')]
		dic_dfs = fc.spreads_finder(range_days=range_days,gap=gap,icamos=icamos, valuta=df1.days[0],fec=fec1,spot=spot,ptos=ptos)
		t = 'Top-10 out of {} Fx spreads:   within {}d - {}d curve , and {} to {} days gap. Results: Cheap on the left, Rich on the right'.format(dic_dfs['num_s'],
															range_days[0],range_days[1],gap[0],gap[1])

	# return tables cheap & rich
	return dic_dfs['cheap'].to_dict('rows-table-cheap'), dic_dfs['rich'].to_dict('rows-table-rich'), t





import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import dash_table
from dash_table.Format import Format  # https://dash.plot.ly/datatable/typing
import plotly.graph_objs as go

import pandas as pd
pd.options.mode.chained_assignment = None #apaga warning set with copy
import numpy as np
from numbers import Number


""" Corre INICIO procesos """

from app import app

import funcs_co as fc
from graphs import crea_fra_scatter_graph

fra_historic = pd.read_csv("./batch/fra_history.csv")
indicator = pd.read_csv("indicator.csv")

# importa fechas batch (fec0) + fecha de uso (fec1)
fec0,fec1 = pd.read_excel('./batch/bbg_hist_dnlder_excel.xlsx', sheet_name='valores', header=None).iloc[0:2,1]



""" SECCION INICIALIZA TABLA PRINCIPAL """
spot = 650.58 # TODO: insertar de alguna manera un input eficiente para el spot (para el cliente)
df1 = pd.read_pickle("./batch/table1_init.pkl")


""" SECCION INICIALIZA TABLA CALCULADORA FX """
# lo hago al inicio para no duplicar el proceso en la func del callback
df2 = pd.DataFrame(data=None, index=[0, 1, 2], columns=['name', 'pub_days', 'fix', 'pub', 'val', 'fra', 'fra_rank_hoy', 'fra_rank_hist'])
df2.loc[0, 'name':'pub_days'] = ['short-leg', 7]
df2.loc[1, 'name':'pub_days'] = ['long-leg', 30]



def table1_update(df):
	try:
		for c in ['ptos','ptosy']:
			df[c] = df[c].map(fc.float_or_zero)

		df.odelta = df['ptos'] - df['ptosy']
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

def table2_update(df):
	df.loc[2, 'pub_days'] = df.loc[1, 'pub_days'] - df.loc[0, 'pub_days']

	return df




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
						{'id':'ind',       'name':'ind',      'editable':False, 'hidden':True, 'type': 'numeric'},
						{'id':'tenor',     'name':'t',    'editable':False, 'hidden': False,'width': '40px'},
						{'id':'daysy',     'name':'daysy',    'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'days',      'name':'days',     'editable':False, 'hidden': False, 'type': 'numeric'},
						{'id':'ptosy',     'name':'ptosy',    'editable':False, 'type': 'numeric'},
						{'id':'ptos',      'name':'ptos',     'editable':True,  'type': 'numeric'},
						{'id':'odelta',    'name':'+-',   'editable':False, 'hidden': False, 'type': 'numeric'},
						{'id':'ddelta',    'name':'ddelta',   'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'carry',     'name':'carry',    'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'icam',      'name':'icam',     'editable':True, 'hidden': False, 'type': 'numeric'},
						{'id':'ilib',      'name':'ilib',     'editable':True, 'hidden': False, 'type': 'numeric'},
						{'id':'tcs',       'name':'tcs',      'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'icam_os',   'name':'icam-os',  'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'fracam_os', 'name':'fra-os',   'editable':False, 'hidden': False, 'type': 'numeric'},
						{'id':'basisy',    'name':'basisy',   'editable':False, 'hidden': True, 'type': 'numeric'},
						{'id':'basis',     'name':'basis',    'editable':True, 'type': 'numeric'},
						{'id':'i_ptos',    'name':'i-ptos',   'editable':False, 'type': 'numeric'},
						{'id':'i_basis',   'name':'i-basis',  'editable':False, 'type': 'numeric'},
						{'id':'blank',   'name':'',  'editable':False},
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
						{'if': {'column_id':'tenor'}, 'width': '31px'},
						{'if': {'column_id':'days'}, 'width': '32px'},
						{'if': {'column_id':'ptosy'}, 'width': '40px', 'color': 'rgb(204, 205, 206)'},
						{'if': {'column_id':'ptos'}, 'width': '45px', 'fontWeight': 600, 'color': '#4176A4'},
						{'if': {'column_id':'odelta'}, 'width': '35px'},
						{'if': {'column_id':'ddelta'}, 'width': '48px'},
						{'if': {'column_id':'carry'}, 'width': '48px'},
						{'if': {'column_id':'icam'}, 'width': '48px'},
						{'if': {'column_id':'ilib'}, 'width': '48px'},
						{'if': {'column_id':'fracam_os'}, 'width': '50px'},
						{'if': {'column_id':'basis'}, 'width': '48px', 'fontWeight': 600, 'color': '#4176A4'},
						{'if': {'column_id':'i_ptos'}, 'width': '50px','fontWeight': 600,'color':'#81C3D7','backgroundColor':'rgb(251,251,251)'}, #20A4F3
						{'if': {'column_id':'i_basis'}, 'width': '50px','fontWeight': 600,'color':'#81C3D7','backgroundColor':'rgb(251,251,251)'},
						{'if': {'column_id':'blank'}, 'width': '2px', 'backgroundColor':'rgb(251,251,251)'},
						],
					editable=True,
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
				dcc.Graph(id='id-fra-line-graph',
						  style={
							  # 'text-align':'left',
							  # 'height':'40vh',
							  # 'margin-bottom':'0px',
							},
							hoverData={'points': [{'customdata': 'm1'}]}),
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
		html.Div(
			children=[
				dash_table.DataTable(
					id='table2',
					data=df2.to_dict('rows_table2'),
					columns=df2.columns.to_list(),
					editable=True,
					),
				],
			),
	],
	className='row',
)


@app.callback(
	[Output('table1','data'), Output('table2','data')],
	[Input('table1','data_timestamp'), Input('table2','data_timestamp')],
	[State('table1','data'), State('table2','data')])
def update_tables_cback(timestamp1,timestamp2,rows1,rows2):
	dft1 = pd.DataFrame.from_dict(rows1)
	dft2 = pd.DataFrame.from_dict(rows2)

	dft1 = dft1[df1.columns.copy()]
	dft2 = dft2[df2.columns.copy()]

	# print(dft1,'\n',dft2)

	dft1 = table1_update(dft1)
	dft2 = table2_update(dft2)
	return dft1.to_dict('rows_table1'), dft2.to_dict('rows_table2')


@app.callback(
	Output('id-fra-line-graph', 'figure'),
	[Input('table1', 'data')],
	# [State('table1', 'data')]
	)
def display_outputtt(rows):
	dfr = pd.DataFrame.from_dict(rows)
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
            					color=('#4176A4')
        					),
        					opacity=0.8
             				)],
        "layout": go.Layout(
            title="IRS CAM off-shore: FRA 1 month history",
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
	dff.iloc[-1, dff.columns.get_loc(col_name)] = float(row_value / 100) # TODO: aqui esta la division por 100 q quiero elminar
	dff = dff.iloc[0:390]
	return create_time_series(dff)









































import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
# import plotly.offline
#
# import pandas as pd
import numpy as np




def crea_graf_fra_lcl_os_spread(df):
	""" este es el grafico original fra + lcl - os spread bars"""

	tr_fra = go.Scatter(
		name='fra',
		x=df.tenor,
		y=df["fracam_os"],
		mode='lines+markers+text',
		line=dict(
			shape='spline',
			color=('#3C4CAD')
		),
		opacity=0.8,
		text=np.array([str(round(x, 2)) for x in df["fracam_os"]]),
		# hoverinfo='x',
		textposition='top center',
		textfont=dict(size=11),
		showlegend=True,
	)

	tr_icamos = go.Scatter(
		name='icam-os',
		x=df.tenor,
		y=df["icam_os"],
		mode='lines+markers',
		line=dict(
			shape='spline',
			color=('#3C4CAD'),
			dash='dash',
		),
		opacity=0.8,
		textposition='top center',
		textfont=dict(size=10),
		showlegend=True,
	)

	tr_bar = go.Bar(
		name='os-spread',
		x=df.tenor,
		y=df.icam_osz - df.icamz,
		yaxis='y2',
		showlegend=True,
		marker_color='#F04393',
		opacity=0.2,
	)

	layout = dict(
		title='Camara off shore curve spot v/s fra (line - LHS) v/s synthethic spread (bars - RHS) ',
		titlefont=dict(size=11),
		xaxis=dict(
			zeroline=False,
			showgrid=False,
			automargin=True,
			fixedrange=True,
		),
		yaxis=dict(
			zeroline=False,
			showgrid=False,
			automargin=True,
			titlefont=dict(size=10),
		),
		yaxis2=dict(
			overlaying='y',
			anchor='x',
			side='right',
			showgrid=True,
		),
		legend=dict(
			orientation='h',
			x=0.6,
			y=1.08,
			xanchor='center',
			font=dict(
				size=10,
			),
			bgcolor='rgba(0,0,0,0)',
		),
		height=350,
		margin=dict(l=45, b=20, r=50, t=55),
	)

	fig = dict(data=[tr_fra, tr_icamos, tr_bar], layout=layout)

	return fig




def crea_time_series(tenor,last_fra,last_spr,fec1):
	""" funcion q crea grafico linea historia fra + spread os-lcl

	 ahora pisar la pultima fila con la data actual de mercado  !!!

	 # fra_h = pd.read_csv('fra_history.csv')
	 # dfe = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
	"""

	import pandas as pd
	aux = pd.read_csv('./batch/fra_history.csv', index_col=0)
	aux2 = pd.read_csv('./batch/spread_g2_history.csv', index_col=0)

	f_series = aux[tenor]
	f_series.loc[fec1] = last_fra

	s_series = aux2[tenor]
	s_series.loc[fec1] = last_spr
	mean = [s_series.mean() for x in s_series]


	tr_fra = go.Scatter(
		x=f_series.index,
		y=f_series,
		mode = 'lines',
		name='fra',
		line=dict(
			shape='spline',
			color=('#240E8B'),
			width=1,
		),
		opacity=0.8,
	)

	tr_spr = go.Scatter(
		x=s_series.index,
		y=s_series,
		yaxis='y2',
		mode ='lines',
		name='os-lcl spread',
		line=dict(
			shape='spline',
			color=('#F04393'),
			width=1,
		),
		opacity=0.8,
	)

	tr_spr_m = go.Scatter(
		x=s_series.index,
		y=mean,
		yaxis='y2',
		mode ='lines',
		name='mean spread',
		line=dict(
			shape='spline',
			color=('#F04393'),
			width=1,
		),
		opacity=0.8,
		hoverinfo='skip',
	)

	layout = dict(
		title="Camara off shore "+tenor+" fra history (LHS)  v/s  synthetic "+tenor+" spread history (RHS)",
		titlefont=dict(size=12),
		xaxis=dict(
			automargin=True,
			showgrid=False,
			type='date',
			titlefont=dict(size=8),
		),
		yaxis=dict(
			zeroline=False,
			showgrid=False,
			automargin=True,
			titlefont=dict(size=8),
		),
		yaxis2=dict(
			zeroline=False,
			showgrid=True,
			overlaying='y',
			anchor='x',
			side='right',
			titlefont=dict(size=8),
		),
		legend=dict(
			orientation='h',
			x=0.6,
			y=1.08,
			xanchor='center',
			font=dict(
				size=10,
			),
			bgcolor='rgba(0,0,0,0)',
		),
		shape=dict(
			type='line',
		),
		height=375,
		margin=dict(l=20, b=20, r=40, t=55),
	)

	layout.update(
		annotations=[dict(
			x=fec1,
			y=last_fra,
			align='right',
			text=str(last_fra),
			showarrow=False,
			xref='x',
			yref='y',
			bordercolor="#c7c7c7",
			borderwidth=2,
			borderpad=2,
			bgcolor="#240E8B",
			opacity=0.8,
			font=dict(
				size=11,
				color='#ffffff',
			),
		),
		dict(
			x=fec1,
			y=last_spr,
			align='right',
			text=str(last_spr),
			showarrow=False,
			xref='x',
			yref='y2',
			bordercolor="#c7c7c7",
			borderwidth=2,
			borderpad=2,
			bgcolor="#F04393",
			opacity=0.9,
			font=dict(
				size=11,
				color='#ffffff',
			),
		),
		]
	)

	fig = dict(data=[tr_fra,tr_spr, tr_spr_m], layout=layout)
	return fig




# def crea_grafico3(spread_d,series):
# 	""" crea graf3 .... no confundir con update_graf3"""
# 	trace = go.Scatter(
# 		x=series.index,
# 		y=series,
# 		# customdata=auxiliar["tenor"],
# 		mode='lines',
# 		# name='lines+markers',
# 		line=dict(
# 			shape='spline',
# 			color=('#73BA9B'),
# 			width=1.5,
# 		),
# 		opacity=1,
# 		# text=np.array([str(round(x, 2)) for x in auxiliar["fracam_os"]]),
# 		textposition='top center',
# 		textfont=dict(size=10),
# 	)
#
# 	layout = dict(
# 		title='FRA-os implicit in spread: ' + str(int(spread_d[0])) + 'x' + str(int(spread_d[1])),
# 		titlefont=dict(size=11),
# 		xaxis=dict(
# 			zeroline=False,
# 			showgrid=False,
# 			automargin=True
# 		),
# 		yaxis=dict(
# 			zeroline=False,
# 			showgrid=True,
# 			automargin=True,
# 			titlefont=dict(size=10, ),
# 			# size=8,
# 		),
# 		height=300,
# 		margin=dict(l=45, b=20, r=50, t=35),
# 	)
#
# 	fig = dict(data=[trace], layout=layout)
#
# 	return fig




def crea_graf_ptos_lcl(df):
	""" crea grafico de ptos forward, con X axis convención local"""
	l = ['2m', '3m', '4m', '5m', '6m', '9m', '12m', '18m', '2y']
	dif = df.ptoso - df.ptos

	# tr_ptos_lcl = go.Scatter(
	# 	name='ptos-lcl',
	# 	x=l,
	# 	y=df['ptos'],
	# 	mode='markers',
	# 	line=dict(
	# 		shape='spline',
	# 		color=('#240E8B'),
	# 		width=1.5,
	# 	),
	# 	opacity=0.5,
	# 	# hoverinfo='x',
	# 	textposition='top center',
	# 	textfont=dict(size=10),
	# 	showlegend=False,
	# )

	# tr_ptos_os = go.Scatter(
	# 	name='ptos-os',
	# 	x=l,
	# 	y=df['ptoso'],
	# 	mode='markers',
	# 	line=dict(
	# 		shape='spline',
	# 		color=('#81C3D7'),
	# 		width=1.5,
	# 	),
	# 	opacity=0.5,
	# 	# hoverinfo='x',
	# 	textposition='top center',
	# 	textfont=dict(size=10),
	# 	showlegend=False,
	# )

	tr_bars = go.Scatter(
		name='ptos os-lcl',
		mode='markers',
		x=l,
		y=dif,
		yaxis='y2',
		text=np.array([str(round(x, 2)) for x in dif]),
		# textposition='outside',
		textfont=dict(
			size=11,
		),
		hoverinfo='x',
		showlegend=False,
		marker_color='#59C3C3',
		opacity=0.6,
	)

	layout = dict(
		title='ptos (LHS)  v/s  os-lcl spread (RHS)',
		titlefont=dict(size=11),
		xaxis=dict(
			zeroline=False,
			showgrid=False,
			automargin=True,
			fixedrange=True,
		),
		yaxis=dict(
			zeroline=False,
			showgrid=False,
			automargin=True,
			titlefont=dict(size=10),
			# size=8,
		),
		yaxis2=dict(
			overlaying='y',
			anchor='x',
			side='right',
			showgrid=True,
		),
		height=350,
		margin=dict(l=45, b=20, r=50, t=55),
		# legend=dict(
		# 	orientation='h',
		# 	x=0.5,
		# 	y=1,
		# ),
	)

	fig = dict(data=[
		# tr_ptos_lcl, tr_ptos_os,
		tr_bars], layout=layout)
	return fig



def prueba():
	tr1 = go.Scatter(
		x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
		y=[0, 1, 3, 2, 4, 3, 4, 6, 5],
	)

	tr2 = go.Scatter(
		x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
		y=[0, 4, 5, 1, 2, 2, 3, 4, 2],
	)

	layout = dict(
		showlegend=False,
	)

	layout.update(
		annotations=[dict(
			x=2,
			y=5,
			xref="x",
			yref="y",
			text="max=5",
			showarrow=True,
			font=dict(
				family="Courier New, monospace",
				size=16,
				color="#ffffff"
			),
			align="center",
			arrowhead=2,
			arrowsize=1,
			arrowwidth=2,
			arrowcolor="#636363",
			ax=-60,
			ay=30,
			bordercolor="#c7c7c7",
			borderwidth=2,
			borderpad=4,
			bgcolor="#ff7f0e",
			opacity=0.8
		)]
	)

	return dict(data=[tr1,tr2], layout=layout)


def annot_tito_1(x,y,t):
	annotation = dict(
		x=x,
		y=y,
		xref="x",
		yref="y",
		text=t,
		showarrow=True,
		font=dict(
			family="Courier New, monospace",
			size=16,
			color="#ffffff"
		),
		align="center",
		arrowhead=2,
		arrowsize=1,
		arrowwidth=2,
		arrowcolor="#636363",
		ax=0,
		ay=5,
		bordercolor="#c7c7c7",
		borderwidth=2,
		borderpad=4,
		bgcolor="#ff7f0e",
		opacity=0.8
	)
	return annotation


def graf_arbit_lcl_os(df):
	# https://plot.ly/python/v3/subplots/
	l = ['2m', '3m', '4m', '5m', '6m', '9m', '12m', '18m', '2y']

	tr_spr = go.Bar(
		name='arbitrage',
		x=l,
		y=df.loc['2m':'2y'].ptoso_p - df.loc['2m':'2y'].ptos_lcl_1x,
		marker_color='#59C3C3',
		opacity=0.8,
	)

	tr_lcl = go.Scatter(
		name='pts off-shore',
		x=l,
		y=df.loc['2m':'2y'].ptoso_p,
		yaxis='y2',
	)

	tr_ofs = go.Scatter(
		name='pts lcl (1x)',
		x=l,
		y=df.loc['2m':'2y'].ptos_lcl_1x,
		yaxis='y2',
	)

	layout = go.Layout(
		title='Arbitrage os-lcl: 1x convention',
		titlefont=dict(size=12),
		yaxis=dict(
			domain=[0,0.33],
		),
		yaxis2=dict(
			domain=[0.33, 1],
		),
		showlegend=True,
		legend=dict(
			orientation='h',
			x=0.6,
			y=1.05,
			xanchor='center',
			font=dict(
				size=10,
			),
			bgcolor='rgba(0,0,0,0)',
		),
		height=350,
		margin=dict(l=45, b=20, r=50, t=35),
	)

	layout.update(
		annotations=[annot_tito_1(x=df.loc['2m':'2y'].index,y=df.loc['2m':'2y'].ptoso_p,t=x1) for x1 in df.loc['2m':'2y'].ptoso_p]
	)



	return go.Figure(data=[tr_lcl,tr_ofs,tr_spr], layout=layout)
# import plotly.plotly as py
import plotly.graph_objs as go
# import plotly.offline
#
# import pandas as pd
import numpy as np


def crea_fra_scatter_graph(dfrfracam_os):
	""" dfrfracam_os es un diccionario, con key,val para x,y: values , i.e. numpy array"""

	l = ['1m', '2m', '3m', '4m', '5m', '6m', '9m', '12m', '18m', '2y']

	trace_fra = go.Scatter(
		x=l,
		y=dfrfracam_os,
		mode='lines+markers+text',
		name='lines+markers',
		line=dict(
			shape='spline',
			color=('#240E8B'),  # color azul Binary
			# width=2,
		),
		opacity=0.8,
		text=np.array([str(round(x, 2)) for x in dfrfracam_os]),
		textposition='top center',
		# marker = dict(size=8 ),
		textfont=dict(size=12),
		# yaxis = dict(size=10, color='#240E8B')
	)

	layout = dict(
		title='FRA 1 month IRS CAM off-shore (f1m-os) ',
		titlefont=dict(size=13),
		xaxis=dict(
			zeroline=False,
			automargin=True,
			# title='Tenor',
			# titlefont=dict(
			#    size=10,
			# ),
			# size=8,
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



def crea_fra_hist_line(tenor,last_fra,fec1):
	""" funcion q crea grafico linea historia fra

	 ahora pisar la pultima fila con la data actual de mercado  !!!

	 # fra_h = pd.read_csv('fra_history.csv')
	 # dfe = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
	"""

	import pandas as pd
	df = pd.read_csv('./batch/fra_history.csv', index_col=0)
	s = df[tenor]
	s.loc[fec1] = last_fra

	tr_fra = go.Scatter(
		x=s.index,
		y=s,
		mode = 'lines',
		name='FRA history',
		line=dict(
			shape='spline',
			color=('#240E8B'),
			width=1,
		),
		opacity=0.8,

	)

	layout = dict(
		title="Camara off shore "+tenor+" fra history (LHS)  v/s  synthetic "+tenor+" spread history",
		titlefont=dict(size=12),
		# margin=dict(t=50,b=50),
		xaxis=dict(
			automargin=True,
			showgrid=False,
			type='date',
			titlefont=dict(size=10, ),
		),
		yaxis=dict(
			automargin=True,
			titlefont=dict(size=10, ),
		),
		height=375,
		margin=dict(l=45, b=20, r=50, t=55),
	)
	fig = dict(data=[tr_fra], layout=layout)
	return fig




def crea_grafico3(spread_d,series):
	""" crea graf3 .... no confundir con update_graf3"""
	trace = go.Scatter(
		x=series.index,
		y=series,
		# customdata=auxiliar["tenor"],
		mode='lines',
		# name='lines+markers',
		line=dict(
			shape='spline',
			color=('#73BA9B'),
			width=1.5,
		),
		opacity=1,
		# text=np.array([str(round(x, 2)) for x in auxiliar["fracam_os"]]),
		textposition='top center',
		textfont=dict(size=10),
	)

	layout = dict(
		title='FRA-os implicit in spread: ' + str(int(spread_d[0])) + 'x' + str(int(spread_d[1])),
		titlefont=dict(size=11),
		xaxis=dict(
			zeroline=False,
			showgrid=False,
			automargin=True
		),
		yaxis=dict(
			zeroline=False,
			showgrid=True,
			automargin=True,
			titlefont=dict(size=10, ),
			# size=8,
		),
		height=300,
		margin=dict(l=45, b=20, r=50, t=35),
	)

	fig = dict(data=[trace], layout=layout)

	return fig




def crea_graf_ptos_lcl(df):
	""" crea grafico de ptos forward, con X axis convención local"""
	l = ['2m', '3m', '4m', '5m', '6m', '9m', '12m', '18m', '2y']
	dif = df.ptoso - df.ptos

	tr_ptos_lcl = go.Scatter(
		name='ptos-lcl',
		x=l,
		y=df['ptos'],
		mode='markers',
		line=dict(
			shape='spline',
			color=('#240E8B'),
			width=1.5,
		),
		opacity=0.5,
		# hoverinfo='x',
		textposition='top center',
		textfont=dict(size=10),
		showlegend=False,
	)

	tr_ptos_os = go.Scatter(
		name='ptos-os',
		x=l,
		y=df['ptoso'],
		mode='markers',
		line=dict(
			shape='spline',
			color=('#81C3D7'),
			width=1.5,
		),
		opacity=0.5,
		# hoverinfo='x',
		textposition='top center',
		textfont=dict(size=10),
		showlegend=False,
	)

	tr_bars = go.Bar(
		name='ptos os-lcl',
		x=l,
		y=dif,
		yaxis='y2',
		text=np.array([str(round(x, 2)) for x in dif]),
		textposition='outside',
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
		height=325,
		margin=dict(l=45, b=20, r=50, t=35),
		# legend=dict(
		# 	orientation='h',
		# 	x=0.5,
		# 	y=1,
		# ),
	)

	fig = dict(data=[tr_ptos_lcl, tr_ptos_os, tr_bars], layout=layout)
	return fig




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
		opacity=1,
		text=np.array([str(round(x, 2)) for x in df["fracam_os"]]),
		# hoverinfo='x',
		textposition='top center',
		textfont=dict(size=10),
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
		opacity=1,
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
			# size=8,
		),
		yaxis2=dict(
			overlaying='y',
			anchor='x',
			side='right',
			showgrid=True,
		),
		legend=dict(
			orientation='h',
		),
		height=375,
		margin=dict(l=45, b=20, r=50, t=55),
	)

	fig = dict(data=[tr_fra, tr_icamos, tr_bar], layout=layout)

	return fig





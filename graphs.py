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
			color='#3C4CAD',
		),
		opacity=0.8,
		text=np.array([str(round(x, 2)) for x in df["fracam_os"]]),
		hoverinfo='x+y+name',
		textposition='top center',
		textfont=dict(size=11),
		showlegend=True,
	)

	tr_icamos = go.Scatter(
		name='icam-os',
		x=df.tenor,
		y=df["icam_os"],
		mode='lines',
		line=dict(
			shape='spline',
			color='#92B4F4',
			dash='dot',
		),
		opacity=0.4,
		# textposition='top center',
		# textfont=dict(size=10),
		showlegend=True,
	)

	tr_bar = go.Bar(
		name='os-lcl spread',
		x=df.tenor,
		y=df.icam_osz - df.icamz,
		yaxis='y2',
		showlegend=True,
		marker_color='#62BEC1',
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
			zerolinecolor='lightGrey',
			overlaying='y',
			anchor='x',
			side='right',
			showgrid=True,
		),
		legend=dict(
			orientation='h',
			x=0.6,
			y=1.09,
			xanchor='center',
			font=dict(
				size=10,
			),
			bgcolor='rgba(0,0,0,0)',
		),
		height=325,
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
	mean = [round(s_series.mean(),2) for x in s_series]


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
			color='#62BEC1',
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
			color='#62BEC1',
			width=3,
		),
		opacity=0.8,
		# hoverinfo='skip',
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
			bgcolor="#62BEC1",
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




def annot_tito(x,y,t,ay,fc,bgc):
	""" función crea "anotacion" para el grafico de arbitraje"""
	annotation = dict(
		x=x,
		y=y,
		xref="x",
		yref="y2",
		text=t,
		showarrow=True,
		font=dict(
			family="Courier New, monospace",
			size=13,
			color=fc,
		),
		align="center",
		arrowhead=1,
		arrowsize=1,
		arrowwidth=1,
		arrowcolor="rgba(0,0,0,0)",
		ax=0,
		ay=ay,
		bordercolor="#c7c7c7",
		borderwidth=1,
		borderpad=1,
		bgcolor=bgc,
		opacity=0.8,
	)
	return annotation


def graf_arb_os(df): # https://plot.ly/python/v3/subplots/

	l = ['2m', '3m', '4m', '5m', '6m', '9m', '12m', '18m', '2y']
	df['dif'] = df.ptoso_p - df.ptos_lcl_1x
	dif = df.loc['2m':'2y'].ptoso_p - df.loc['2m':'2y'].ptos_lcl_1x

	""" esta seccion es la + dificil de la app. Que no se superpongan las etiquetas. Cree una escala centavos/pixel manual
	con el objetivo de reescalar la ubicación de las anotaciones (tarjetas) par que no se superpongan """
	yrange = 100 * (0.10+ df.loc['TOD':'2y',['ptos','ptoso']].max().max() - df.loc['TOD':'2y',['ptos','ptoso']].min().min())

	suple = 6.5 # es un numero inventado que permite reescalar el ratio centavos/pixels
	scale = yrange / (147.5 + yrange/suple)

	df['ubic_graf'] = np.where(df.dif>=0, (-30-df.dif*100)/scale, (30-df.dif*100)/scale)

	tr_spr = go.Bar(
		name='arbitrage',
		x=l,
		y=dif,
		marker_color='#F04393',
		text=[str(x) for x in dif.round(2)],
		textposition='auto',
		textangle=0,
		textfont=dict(
			size=10,
		),
		opacity=0.6,
		hoverinfo='x+y+name',
	)

	tr_lcl = go.Scatter(
		name='pts off-shore',
		mode='markers',
		visible='legendonly',
		x=l,
		y=df.loc['2m':'2y'].ptoso_p,
		yaxis='y2',
	)

	tr_ofs = go.Scatter(
		name='pts lcl (1x)',
		mode='markers',
		visible='legendonly',
		x=l,
		y=df.loc['2m':'2y'].ptos_lcl_1x,
		yaxis='y2',
	)

	layout = go.Layout(
		title='Arbitrage os-lcl <br> 1x convention',
		titlefont=dict(size=12),
		yaxis=dict(
			domain=[0,0.5],
			range=[min(-0.1,dif.min()), max(0.1, dif.max())],
		),
		yaxis2=dict(
			domain=[0.5, 1],
			visible=False,
			fixedrange=True,
			zeroline=False,
		),
		showlegend=False,
		height=350,
		margin=dict(l=45, b=20, r=50, t=35),
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
		)],
	)

	l_a= []
	for ind,row in df.loc['2m':'2y'].iterrows():
		l_a.append(annot_tito(ind, row['ptoso_p'], str(row['ptoso_p']), 0, '#ffffff', '#F04393') )  #F04393
		l_a.append(annot_tito(ind, row['ptos_lcl_1x'], str(row['ptos']), -row['ubic_graf'],'#808080','#ffffff') ) #3C4CAD

	layout.update(annotations=l_a)

	return go.Figure(data=[tr_lcl,tr_ofs,tr_spr], layout=layout)



def graf_arb_lcl(df): # https://plot.ly/python/v3/subplots/

	l = ['2m', '3m', '4m', '5m', '6m', '9m', '12m', '18m', '2y']
	df['dif'] = df.ptos - df.ptoso
	dif = df.loc['2m':'2y'].ptos - df.loc['2m':'2y'].ptoso

	""" esta seccion es la + dificil de la app. Que no se superpongan las etiquetas. Cree una escala centavos/pixel manual
	con el objetivo de reescalar la ubicación de las anotaciones (tarjetas) par que no se superpongan """
	yrange= 100 * (0.10 + df.loc['TOD':'2y',['ptos','ptoso']].max().max() - df.loc['TOD':'2y',['ptos','ptoso']].min().min())

	suple = 6.5 # es un numero inventado que permite reescalar el ratio centavos/pixels
	scale = yrange / (147.5 + yrange/suple)

	# define la ubicación de las anotaciones (etiquetas) en el grafico
	df['ubic_graf'] = np.where(df.dif>=0, (-30-df.dif*100)/scale, (30-df.dif*100)/scale)

	tr_spr = go.Bar(
		name='arbitrage',
		x=l,
		y=dif,
		marker_color='#3C4CAD',
		text=[str(x) for x in dif.round(2)],
		textposition='auto',
		textangle=0,
		textfont=dict(
			size=10,
		),
		opacity=0.6,
		hoverinfo='x+y+name',
	)

	tr_lcl = go.Scatter(
		name='pts off-shore',
		mode='markers',
		visible='legendonly',
		x=l,
		y=df.loc['2m':'2y'].ptos,
		yaxis='y2',
	)

	tr_ofs = go.Scatter(
		name='pts lcl (1x)',
		mode='markers',
		visible='legendonly',
		x=l,
		y=df.loc['2m':'2y'].ptoso,
		yaxis='y2',
	)

	layout = go.Layout(
		title='Arbitrage os-lcl: Local convention',
		titlefont=dict(size=12),
		yaxis=dict(
			domain=[0,0.5],
			range=[min(-0.1,dif.min()), max(0.1, dif.max())],
		),
		yaxis2=dict(
			domain=[0.5, 1],
			visible=False,
			fixedrange=True,
			zeroline=False,
		),
		showlegend=False,
		height=350,
		margin=dict(l=45, b=20, r=50, t=35),
	)

	l_a= []
	for ind,row in df.loc['2m':'2y'].iterrows():
		l_a.append(annot_tito(ind, row['ptos'], str(row['ptos']), 0, '#ffffff', '#3C4CAD') )  #F04393
		l_a.append(annot_tito(ind, row['ptoso'], str(row['ptoso_p']), -row['ubic_graf'],'#808080','#ffffff') ) #3C4CAD

	layout.update(annotations=l_a)

	return go.Figure(data=[tr_lcl,tr_ofs,tr_spr], layout=layout)





def annot_ptos_teo(fec1,y,t,ax,ay,fc,bgc,o):
	""" anotación para el gráfico de puntos teoricos """
	annotation = dict(
		x=fec1,
		y=y,
		xref='x',
		yref='y',
		text=t,
		showarrow=True,
		font=dict(
			# family="Courier New, monospace",
			size=12,
			color=fc,
		),
		align="center",
		arrowhead=1,
		arrowsize=1,
		arrowwidth=1,
		arrowcolor="rgba(0,0,0,0)",
		ax=ax,
		ay=ay,
		bordercolor="#000000", #c7c7c7
		borderwidth=1,
		borderpad=1,
		bgcolor=bgc,
		opacity=o,
	)
	return annotation


def crea_ptos_teo(tenor,df,fec1,perc_ptos):

	tra95 = go.Scatter(
		x=df.index,
		y=df.ptos_95,
		line=dict(
			color = 'rgba(298,66,102,0.8)',  # 298,66,102 rojo
		),
		name='95th',
		line_width=0.6,
	)

	tra50 = go.Scatter(
		x=df.index,
		y=df.ptos_50,
		fill='tonexty',
		fillcolor='rgba(298,66,102,0.3)', #298,66,102 rojo
		line=dict(
			color='rgba(192,192,192,0.8)',  # silver
			width=0.6,
		),
		name='50th',
	)

	tra5 = go.Scatter(
		x=df.index,
		y=df.ptos_5,
		fill='tonexty',
		fillcolor='rgba(89,195,195,0.3)', #89,195,195 verde
		line_color='rgba(89,195,195,0.8)', #89,195,195 verde
		name='5th',
		line_width=0.6,
	)

	traptos = go.Scatter(
		x=df.index,
		y=df.ptos,
		name='ptos',
		line=dict(
			shape='spline',
			color='#3C4CAD',
			width=1.5,
		),
	)

	layout = dict(
		title="Forward Points '"+tenor+"' v/s theoric usd.clp rates spread <br> 5th,50th,95th percentiles",
		titlefont=dict(size=12),
		xaxis=dict(
			automargin=True,
			showgrid=False,
			type='date',
			titlefont=dict(size=8),
		),
		yaxis=dict(
			# zeroline=True,
			showgrid=True,
			automargin=True,
			titlefont=dict(size=8),
		),
		showlegend=False,
		height=400,
		margin=dict(l=20, b=20, r=40, t=55),
	)

	l_a    = []
	texto  = [' ('+str(perc_ptos)+'/100)','','','']
	l_posx = [-27, 27, 27, 27]
	l_posy = [0, 10, 0, -10]
	l_fc   = ['#ffffff','#000000','#000000','#000000']
	l_bgc  = ['#3C4CAD','rgba(89,195,195,0.8)','rgba(192,192,192,0.8)','rgba(298,66,102,0.8)']
	l_opac = [0.8,1,1,1]
	for col,t,posx,posy,fc,bgc,o in zip(df.columns,texto,l_posx,l_posy,l_fc,l_bgc,l_opac):
		l_a.append(annot_ptos_teo(fec1, df[col][-1], str(df[col][-1])+t, posx, posy, fc, bgc,o) )

	layout.update(annotations=l_a)
	fig = dict(data=[tra95,tra50,tra5,traptos], layout=layout)
	return fig
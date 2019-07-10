import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline

import pandas as pd
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
            color=('#4176A4'),  # color azul Binary
            # width=2,
        ),
        opacity=0.8,
        text=np.array([str(round(x, 2)) for x in dfrfracam_os]),
        textposition='top center',
        # marker = dict(size=8 ),
        textfont=dict(size=12),
        # yaxis = dict(size=10, color='#4176A4')
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


# x = {'0': None, '1': None, '2': None, '3': None, '4': 2.74, '5': 2.7, '6': 2.85, '7': 2.9, '8': 2.93, '9': 2.67, '10': 2.78, '11': 2.7, '12': 2.65, '13': 2.92, '14': None, '15': None, '16': None, '17': None,
# 	 '18': None, '19': None, '20': None, '21': None}

# plotly.offline.plot( crea_fra_scatter_graph(x), filename = 'styled-scatter.html')


def crea_fra_hist_line(last_val):
    """ funcion q crea grafico linea historia fra

	 ahora pisar la pultima fila con la data actual de mercado  !!!

	 # fra_h = pd.read_csv('fra_history.csv')
	 # dfe = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
	"""

    import pandas as pd
    dfh = pd.read_csv('fra_history.csv')

    print(last_val)

    y1 = dfh['1m'].copy()
    y1.iloc[
        -1] = last_val / 100  # divido x 100 porq el val en el dict viene asi para el graf

    trace = go.Scatter(
        x=dfh['date'],
        y=100 * y1,  # 1 mes
        # mode = 'lines',
        name='FRA history',
        line=dict(
            shape='spline',
            color=('#4176A4'),
            # width=1,
        ),
        opacity=0.8,
    )

    data = [trace]

    layout = dict(
        title="IRS CAM off-shore: FRA 1 month history",
        titlefont=dict(size=13),
        # margin=dict(t=50,b=50),
        xaxis=dict(
            automargin=True,
            rangeselector=dict(buttons=list([
                dict(count=1, label='1m', step='month', stepmode='backward'),
                dict(count=6, label='6m', step='month', stepmode='backward'),
                dict(step='all'),
            ])),
            rangeslider=dict(visible=True),
            type='date',
            titlefont=dict(size=10, ),
        ),
        yaxis=dict(
            automargin=True,
            titlefont=dict(size=10, ),
        ),
        margin=dict(l=55, b=50, r=65),
    )
    fig = dict(data=data, layout=layout)
    return fig


# plotly.offline.plot( crea_fra_hist_line(fra_h), filename = "Time Series with Rangeslider.html")

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
# pd.set_eng_float_format(accuracy=2, use_eng_prefix=True)

import numpy as np
from numbers import Number

from funcs_co import imp_spot, imp_clos_t, live, cam_os_simp, fra1m, iptos, ibasis, round_conv_basis

from graphs import crea_fra_scatter_graph, crea_fra_hist_line

spoty= imp_spot() #spot yesterday closing
spot = 650.58

# importa data closing tradition + crea df
df = imp_clos_t()

# lee precios live de cam y libor swap
df.ptos= df.ptosy.copy(True)
df.icam= live(col='icam')
df.ilib= live(col='ilib')
df.basis= df.basisy.copy(True)
df.tcs= 6.5


# dfg = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')



##

layout = html.Div(
            # className="row",
			style={
                # 'margin': '0px',
                # 'textAlign': 'justify',
                # 'padding-left':'25px',
                   },
            children=[
                    html.Div(
                            className="five columns",
							# style={'display': 'inline-block'},
                            children=[
                                    html.Div(
                                        className='row',
                                        style={'display':'inline-block'},
                                            children=[
                                                dash_table.DataTable(
                                                    # https://dash.plot.ly/datatable/reference
                                                    # https://dash.plot.ly/datatable/sizing
                                                    id='table1',
                                                    data=df.to_dict('rows'),

                                                    columns=[{'id': 'ind', 'name': 'ind', 'hidden': True},
                                                             {'id': 'tenor', 'name': 'tenor', 'hidden': False,
                                                              'width': '40px'},
                                                             {'id': 'daysy', 'name': 'daysy', 'hidden': True},
                                                             {'id': 'days', 'name': 'days', 'hidden': True},
                                                             {'id': 'ptosy', 'name': 'ptos-y'},
                                                             {'id': 'ptos', 'name': 'ptos', 'type': 'numeric'},
                                                             {'id': 'odelta', 'name': 'delta', 'hidden': False},
                                                             {'id': 'ddelta', 'name': 'd-delta', 'hidden': False},
                                                             {'id': 'carry', 'name': 'carry-mo', 'hidden': False},
                                                             {'id': 'icam', 'name': 'icam', 'hidden': True},
                                                             {'id': 'ilib', 'name': 'ilib', 'hidden': True},
                                                             {'id': 'tcs', 'name': 'tcs', 'hidden': True},
                                                             {'id': 'icam_os', 'name': 'icam-os', 'hidden': True},
                                                             {'id': 'fracam_os', 'name': 'fra-os', 'hidden': False},
                                                             {'id': 'basisy', 'name': 'basisy', 'hidden': True},
                                                             {'id': 'basis', 'name': 'basis', 'type': 'numeric'},
                                                             {'id': 'i_ptos', 'name': 'i_ptos'},
                                                             {'id': 'i_basis', 'name': 'i_basis', 'type': 'numeric'},
                                                             ],
                                                    style_as_list_view=True,
                                                    n_fixed_rows=1,
                                                    style_table={
                                                        # 'margin':'5px',
                                                        # 'maxHeight': '250',
                                                        # 'overflowY': 'scroll'
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
                                                    style_header={
                                                        # 'column_id': 'ptos',
                                                        # 'height':'35px',
                                                        'textOverflow': 'clip',
                                                        # 'borderBottom':'0px',
                                                        'border': '1px solid white',
                                                        'backgroundColor': 'white'},
                                                    style_cell_conditional=[
                                                        {'if': {'column_id': 'tenor'}, 'width': '40px'},
                                                        {'if': {'column_id': 'ptosy'}, 'width': '45px',
                                                         'color': 'rgb(204, 205, 206)'},
                                                        {'if': {'column_id': 'ptos'}, 'width': '55px',
                                                         'fontWeight': 600, 'color': '#4176A4'},
                                                        {'if': {'column_id': 'odelta'}, 'width': '50px'},
                                                        {'if': {'column_id': 'ddelta'}, 'width': '55px'},
                                                        {'if': {'column_id': 'carry'}, 'width': '55px'},
                                                        {'if': {'column_id': 'icam'}, 'width': '50px'},
                                                        {'if': {'column_id': 'ilib'}, 'width': '50px'},
                                                        {'if': {'column_id': 'fracam_os'}, 'width': '50px'},
                                                        {'if': {'column_id': 'basis'}, 'width': '50px',
                                                         'fontWeight': 600, 'color': '#4176A4'},
                                                        {'if': {'column_id': 'i_ptos'}, 'width': '50px'},
                                                        {'if': {'column_id': 'i_basis'}, 'width': '50px'},

                                                    ],
                                                    editable=True,
                                                ),
                                                dcc.Markdown('''Prueba'''),
                                            ],

                            ),
                                    ],
                    ),

                    html.Div(
                            className="seven columns",
							style={
                                # 'margin': '40px',
                                'display':'inline',
                                # 'max-height':'600px',
                                'width': '40%',
                                'textAlign': 'justify',
                                'height':'70vh',
                                   },
                            children=[
                                html.Div(
                                    children=[html.Div(
                                        style={'textAlign': 'right',
                                               'height':'85vh',},
                                        children=[
                                                html.Div([ dcc.Graph(id='id-fra-line-graph',
                                                                     style={
                                                                     'text-align':'left',
                                                                         'height':'40vh',
                                                                     #     'margin-bottom':'0px',
                                                                     })],
                                                ),
                                                html.Div([ dcc.Graph(id = 'id-fra-hist-line-graph',
                                                                     style={
                                                                     'text-align':'right',
                                                                         'height':'50vh',
                                                                     #     'margin-top':'0px'
                                                                         }
                                                                     )],
                                                ),
                                                dcc.Store(id='intermediate-value-fra', storage_type='memory', data={}),
                                                             ])

                                                ],
                                            )],

                                        ),

        ])


@app.callback(
    [Output('table1','data'), Output('intermediate-value-fra','data')],
    [Input('table1','data_timestamp')],
    [State('table1','data')])
def update_columns(timestamp,rows):
    # print(timestamp)

    d_fra = {}.fromkeys([x for x in range(4, 14)], None)   # inicializa diccionario para guardar FRA's, con tenors as keys, y valores vacios

    for row in rows:
        try:
            row['odelta' ]= float(row['ptos']) - float(row['ptosy'])
            row['ddelta' ]= 100* float(row['odelta']) / float( row['days'] - df.days[0] )
            row['carry'  ]= df.days[4] * row['ptos'] / (row['days'] - df.days[0])
            row['icam_os']= cam_os_simp(dias = row['days'] - df.days[0], spot=spot, ptos=row['ptos'], iusd = row['ilib'], comp = True)
        except:
            pass


        """ CALCULANDO FRA's"""

        # escribe la 1era fra.... la de 1 mes.
        if row['ind']==4:
            row['fracam_os'] = row['icam_os']
            d_fra[row['ind']]= row['icam_os']

        if row['ind'] in [5,6,7,8,9]: #plazos de 2m a 6m
            try:
                row['fracam_os']= fra1m(d_c=days_lag, ispot_c=icamos_lag, d_l=row['days'], ispot_l=row['icam_os'], interp=False)
                d_fra[row['ind']] = row['fracam_os']
            except:
                pass

        if row['ind'] in range(10,14): #plazos de 9m a 18m. Despues me falta hacerlo con las tasas compuestas
            # x mientras esta 13=2yrs... de cuchufleta, dp lo arreglo ...
            try:
                row['fracam_os']  = fra1m(d_c=days_lag, ispot_c=icamos_lag, d_l=row['days'], ispot_l=row['icam_os'], interp=True)
                d_fra[row['ind']] = row['fracam_os']
            except:
                pass


        """ CALCULANDO I-PUNTOS y I-BASIS"""
        if row['ind'] > 10:
            try:
                row['i_ptos'] = iptos(t=row['days'], spot=spot, iusd=row['ilib'], icam=row['icam'], b=row['basis'],
                                         tcs=row['tcs'], comp=True)
                row['i_basis'] = ibasis(t=row['days'], spot=spot, iusd=row['ilib'], icam=row['icam'], ptos=row['ptos'],
                                           tcs=row['tcs'], comp=True)
            except:
                pass


        # guarda estas variables acá al final del loop, para la próxima iteración
        days_lag  = row['days']
        icamos_lag= row['icam_os']

    # formatea el output, con dos decimales
    for row in rows:
        for r in row:
            if r == 'i_basis':  # redondea en convención pantalla basis, decimal cero o cinco.
                row[r] = round_conv_basis(row[r]) if isinstance(row[r],Number)==True else row[r]
            else:
                row[r] = round(row[r],2) if isinstance(row[r],Number)==True else row[r]

    return rows, d_fra


@app.callback(
    Output('id-fra-line-graph', 'figure'),
    [Input('intermediate-value-fra', 'modified_timestamp')],
    [State('intermediate-value-fra', 'data')]
    )
def display_output(timestamp, data):
    if timestamp is None:
        raise PreventUpdate
    return crea_fra_scatter_graph(data)


@app.callback(
    Output('id-fra-hist-line-graph', 'figure'),
    [Input('intermediate-value-fra', 'modified_timestamp')],
    [State('intermediate-value-fra', 'data')])
def update_fra_hist_graph(timestamp, data):
    if timestamp is None:
        raise PreventUpdate

    print('Data 4 es {}'.format(data['4']) )

    return crea_fra_hist_line( data['4'] )


""" https://community.plot.ly/t/two-graphs-side-by-side/5312 """



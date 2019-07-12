import dash_core_components as dcc
import dash_html_components as html

from app import app

layout_1 = html.Div([
    html.Br(),
    html.Details(children=[
        html.Br(),
        html.Summary("FX Points"),
        html.Div(children=[html.H3("Contenido"),
                           html.P("Próximamente...")])
    ])
],
                    style={'margin-left': '85px'})

layout_2 = html.Div([
    html.Br(),
    html.Details(children=[
        html.Br(),
        html.Summary("IR Basis"),
        html.Div(children=[html.H3("Contenido"),
                           html.P("Próximamente...")])
    ])
],
                    style={
                        'margin-left': '665px',
                        'margin-top': '-25px'
                    })

layout_3 = html.Div([
    html.Br(),
    html.Details(children=[
        html.Br(),
        html.Summary("Middle Office"),
        html.Div(children=[html.H3("Contenido"),
                           html.P("Próximamente...")])
    ])
],
                    style={
                        'margin-left': '1245px',
                        'margin-top': '-25px'
                    })

layout = [layout_1, layout_2, layout_3]
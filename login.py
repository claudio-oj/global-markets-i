import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app, User
from flask_login import login_user
from werkzeug.security import check_password_hash

layout_1 = html.Div(
		className='topper',
		style={'backgroundColor':'#4176A4',
               'height': '2000px',
               'margin-left': '-20px',
	})

layout_2 = html.Div(style={'margin-top': '220px', 'width': '100%'},
    children=[
        html.Div([html.Div(
            style={'position': 'relative'},
            className="loginuser",
            children=[html.Img( 
                src='assets/ba_logo_letras_transp.png',
                style={
                    'height': '32%',
                    'width': '35%',
                    'float': 'center',
                    'margin-top': '35px',
                    'margin-left': '0px'
                }),
                dcc.Location(id='url_login', refresh=True),
                html.Div('''Please log in to continue:''', id='h1', style={'margin-top':'25px'}),
                html.Div(
                    # method='Post',
                    children=[
                        dcc.Input(
                            placeholder='Enter your username',
                            type='text',
                            id='uname-box',
                            style={'margin-left':'0px'}
                        ),
                        html.Br(),
                        html.P(),
                        dcc.Input(
                            placeholder='Enter your password',
                            type='password',
                            id='pwd-box',
                            style={'margin-left':'0px'}
                        ),
                        html.Br(),
                        html.P(),
                        html.Button(
                            children='Login',
                            n_clicks=0,
                            type='submit',
                            id='login-button',
                            style={'margin-left':'0px', 'margin-bottom': '25px'}
                        ),
                        html.Div(children='', id='output-state')
                    ]
                ),
            ]
        )], style={'background-color':'#4176a4'}),
    ]
)

layout_3 = html.Div(
		className='botter',
		style={'backgroundColor':'#4176A4',
               'height': '220px'
	})

layout=[layout_1, layout_2]

@app.callback(Output('url_login', 'pathname'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def sucess(n_clicks, input1, input2):
    user = User.query.filter_by(username=input1).first()
    if user:
        if check_password_hash(user.password, input2):
            login_user(user)
            return '/success'
        else:
            pass
    else:
        pass


@app.callback(Output('output-state', 'children'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def update_output(n_clicks, input1, input2):
    if n_clicks > 0:
        user = User.query.filter_by(username=input1).first()
        if user:
            if check_password_hash(user.password, input2):
                return ''
            else:
                return 'Incorrect username or password'
        else:
            return 'Incorrect username or password'
    else:
        return ''

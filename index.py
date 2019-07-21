#!/usr/bin/env python3
# chmod +x index.py

# index page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from flask_login import logout_user, current_user

from header import header_logo, header_link, tabs_gmi
import app_home, app_fx, app_upload
import success, login, login_fd, logout

app.layout = html.Div([
    html.Div([
        html.Div(html.Div(id='page-content', className='content'),
                 className='content-container'),
    ],
             className='container-width'),
    dcc.Location(id='url', refresh=False),
])


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return login.layout
    elif pathname == '/login':
        return login.layout
    elif pathname == '/success':
        if current_user.is_authenticated:
            return success.layout
        else:
            return login_fd.layout
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout.layout
        else:
            return logout.layout
    else:
        return '404'


@app.callback(Output('user-name', 'children'),
              [Input('page-content', 'children')])
def cur_user(input1):
    if current_user.is_authenticated:
        return html.Div('Current user: ' + current_user.username)
        # 'User authenticated' return username in get_id()
    else:
        return ''


@app.callback(Output('logout', 'children'),
              [Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A('Logout', href='/logout')
    else:
        return ''


if __name__ == '__main__':
    app.run_server(debug=True)
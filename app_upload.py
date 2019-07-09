import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
from app import app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload')
])

# TODO: agregar el if para xlsx y resumir código
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:

            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email.mime.base import MIMEBase
            from email import encoders
            import pandas as pd
            

            # ! cambiar correo por otro con clave de desarrollador 
            email_user = 'r2019curso@gmail.com'
            email_password = 'gtcybxienrydeqix'
            email_send = 'contacto@binaryanalytics.cl'

            if filename == "tenor.csv":

                subject = 'Datos Tenor'

                msg = MIMEMultipart()
                msg['From'] = email_user
                msg['To'] = email_send
                msg['Subject'] = subject

                body = 'Hola, enviado desde Python!'
                msg.attach(MIMEText(body, 'plain'))

                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8'))
                )

                df.to_csv(filename, index=False)

                filename_csv = filename
                attachment = open(filename_csv, 'rb')

                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                "attachment; filename= "+filename)

                msg.attach(part)
                text = msg.as_string()
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email_user, email_password)

                server.sendmail(email_user, email_send, text)
                server.quit()

            else:

                subject = 'Datos Bloomberg'

                msg = MIMEMultipart()
                msg['From'] = email_user
                msg['To'] = email_send
                msg['Subject'] = subject

                body = 'Hola, enviado desde Python!'
                msg.attach(MIMEText(body, 'plain'))

                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8'))
                )

                df.to_csv(filename, index=False)

                filename_csv = filename
                attachment = open(filename_csv, 'rb')

                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                "attachment; filename= "+filename)

                msg.attach(part)
                text = msg.as_string()
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email_user, email_password)

                server.sendmail(email_user, email_send, text)
                server.quit()

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


# if __name__ == '__main__':
#    app.run_server(debug=True)

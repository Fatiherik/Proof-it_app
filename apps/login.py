import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Output, Input, State
import pandas_datareader.data as web
from datetime import datetime
import pathlib
import sqlite3
from app import app



layout =  html.Div([
                dcc.Location(id='url2', refresh=False),
                html.Div([
                    html.H4("Welcome Back!", id="welcome"),
                    dcc.Input(id='email', type='text', placeholder='Enter e-mail address...'),
                    dcc.Input(id='password', type='text', placeholder='Password...'),
                    html.A('Login', href='/trader', id='login-button'),
                    html.A('Forget Password?', href='/trader',id='forget-pass'),
                    html.A('Create an Account', href='/signup',id='create-account')
                ], id="login-panel")
            ]),


# @app.callback(
#               Output(component_id='url-2', component_property='pathname'),
#               [Input(component_id='login-button', component_property='n_clicks')],
#               [State(component_id='email', component_property='value'),
#               State(component_id='password', component_property='value')]
#               )



# DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
#     "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
# con = sqlite3.connect(str(DB_FILE))
# statement = f"SELECT password FROM login WHERE email='{email}' ;"
# df = pd.read_sql_query(statement, con)
# print(df.loc[0,'password'] == password)
# if df.loc[0,'password'] == password:
#     return '/trader'
#
# else:
#     return '/login'




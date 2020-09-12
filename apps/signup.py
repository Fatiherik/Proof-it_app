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


layout = html.Div([
            html.H4("Create an Account!", id="account"),
            dcc.Input(id='first-name', type='text', placeholder='First name...'),
            dcc.Input(id='last-name', type='text', placeholder='Last name...'),
            dcc.Input(id='email', type='text', placeholder='Enter e-mail address...'),
            dcc.Input(id='password', type='text', placeholder='Password...'),
            dcc.Input(id='password-again', type='text', placeholder='Repeat Password...'),
            html.A('Register', href='/login',id='register-button'),
            html.A('Forget Password?', href='',id='forget-pass'),
            html.A('Already have an account? Login!', href='/login',id='have-account')
            ], id="signup-panel")


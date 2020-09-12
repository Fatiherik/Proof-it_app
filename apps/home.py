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
            html.Div([
                html.H1('Welcome to Proof-it...'),
                html.H5('Proof-it is a machine learning-model and a backtest algorithm that has been coded with Python. When you log in, you can;'),
                html.H5('- trade live,'),
                html.H5('- backtest your strategy,'),
                html.H5('- optimize it,'),
                html.H5('- run a simulation,'),
                html.H5('- make analysis,'),
                html.H5('- build a portfolio,'),
                html.H5('- predict prices,'),
                html.H5('- explore your previous works,'),
                html.H5('- and more... Are you excited, if so...'),
                html.Button('Join us', id='joinus-button', n_clicks=0,
                        style={'backgroundColor': 'purple', 'color': 'white'})
            ], id="up-left", className="six columns"),
            html.Img(id="pic", src="https://image.freepik.com/free-vector/finance-financial-performance-concept-illustration_53876-40450.jpg")
        ],id="up", className="twelve columns")

# https://t3.ftcdn.net/jpg/03/54/00/74/240_F_354007466_mm4QilA3n92YWPseqs82gbWxbb06R1i4.jpg
# https://img.freepik.com/free-photo/low-angle-view-skyscrapers_1359-825.jpg?size=626&ext=jpg&ga=GA1.2.984904818.1599737047
# https://t3.ftcdn.net/jpg/01/68/60/48/240_F_168604806_dfxzq0AHjywa56kPOeYjGrFD0HT4DECg.jpg
# https://t3.ftcdn.net/jpg/02/10/32/62/240_F_210326274_H5dvx33RhVmyBDM8xs4KBWC89u5oxi64.jpg
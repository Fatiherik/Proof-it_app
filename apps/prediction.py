import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input, State
import pandas_datareader.data as web
from datetime import datetime
import pathlib
import sqlite3
from app import app

layout = html.Div([
            html.Div([
                dcc.Input(
                    id='stock-input3',
                    type='text',
                    value='KOZAA',
                    placeholder='Select stock...',
                    className='stock-picker3'
                ),

                dcc.DatePickerSingle(
                    id='start_date3',
                    placeholder='Start date...',
                    date='2014-08-29'
                ),

                dcc.DatePickerSingle(
                    id='end_date3',
                    placeholder='End date...',
                    date='2019-09-01'
                ),

                dcc.Dropdown(
                    id='model',
                    options=[
                        {'label': 'Model-1', 'value': 'Model-1'},
                        {'label': 'Model-2', 'value': 'Model-2'},
                    ], value='Model-1', placeholder='Select prediction model...', className='model-picker'),

                dcc.Dropdown(
                    id='time',
                    options=[
                        {'label': '1 Month', 'value': '1 Month'},
                        {'label': '3 Month', 'value': '3 Month'},
                        {'label': '6 Month', 'value': '6 Month'},
                        {'label': '12 Month', 'value': '12 Month'}
                    ], value='1 Month', placeholder='Select prediction time...', className='time-picker'),

                html.Button('Execute', id='prediction-execute-button', n_clicks=0,
                            style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'})
            ], id='prediction_panel'),

            html.Div(id='prediction-chart', className='twelve columns'),

            html.Div(id='prediction-table', className='twelve columns'),


        ])

@app.callback(
    [Output(component_id='prediction-chart', component_property='children'),
    Output(component_id='prediction-table', component_property='children')],
    [Input(component_id='prediction-execute-button', component_property='nclicks')],
     [State(component_id='stock-input3', component_property='value'),
     State(component_id='start_date3', component_property='value'),
     State(component_id='end_date3', component_property='value'),
     State(component_id='model', component_property='value'),
     State(component_id='time', component_property='value')]
)

def prediction(n_clicks, stock, start_date, end_date, model, time):

    if n_clicks == None:

        DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
            "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
        con = sqlite3.connect(str(DB_FILE))
        # statement = f"SELECT * FROM {stock} WHERE Date BETWEEN '{start_date}' AND '{end_date}';"
        statement = f"SELECT * FROM KOZAA_daily WHERE Date BETWEEN '12/03/2012' AND '27/09/2019';"
        df = pd.read_sql_query(statement, con)
        df['Prediction'] = ['--' for i in range(len(df))]

        return [dcc.Graph(
            id='graph',
            figure={
                'data': [
                    {'x': df.Date, 'y': df.Close, 'type': 'line', 'color': 'blue', 'name': stock},
                ],
                'layout': {
                    'title': stock,
                    'height': 400,
                    # 'xaxis': {'tickformat': '%Y-%m-%d'}
                },


            }
        ), dash_table.DataTable(
            id='table',
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            style_cell={'textAlign': 'center', 'width': '98px', 'minWidth': '98px', 'maxWidth': '98px'},
            fixed_rows={'headers': True, 'data': 0},
            style_header={'fontWeight': 'bold', 'backgroundColor': 'rgb(66,196,247)'})]





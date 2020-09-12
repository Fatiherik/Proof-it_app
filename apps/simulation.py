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
from apps.calculation import *

from app import app

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__,
#               external_stylesheets=external_stylesheets)

df = pd.DataFrame()
df['Date'] = []
df['Hour'] = []
df['Open'] = []
df['High'] = []
df['Low'] = []
df['Close'] = []
df['MA'] = []

df1 = pd.DataFrame()
df1['1.Profit'] = ['--', '--']
df1['1.Stop'] = ['--', '--']


df3 = pd.DataFrame()
df3['#'] = []
df3['Position'] = []
df3['B.Date'] = []
df3['B.Lot'] = []
df3['B.Price'] = []
df3['B.Total'] = []
df3['S.Date'] = []
df3['S.Lot'] = []
df3['S.Price'] = []
df3['S.Total'] = []
df3['Commission'] = []
df3['Trans P/L'] = []
df3['Total P/L'] = []
df3['Balance'] = []

layout = html.Div([
            html.Div([
                html.Div([
                    html.Div(id='my-output-1'),
                    html.Div(id='my-output-3'),
                    html.Div([
                        html.Div([
                            dcc.DatePickerSingle(
                                id='start_date4',
                                placeholder='Start date...',
                                date='2014-08-29'
                            ),
                            dcc.DatePickerSingle(
                                id='end_date4',
                                placeholder='End date...',
                                date='2019-09-01'
                            )
                        ], className='date-picker'),

                        html.Div([
                            dcc.Input(id='commission-input4', type='number', placeholder='Commission', min=0, value=2),
                            dcc.Input(id='capital-input4', type='number', placeholder='Capital', min=0, value=10000),
                        ], className='commission-capital'),

                        html.Div([
                            dcc.Input(
                                id='stock-input4',
                                type='text',
                                value='KOZAA',
                                placeholder='Select stock...',
                                className='stock-picker4'),

                            dcc.Dropdown(
                                id='strategy4',
                                options=[
                                    {'label': 'Strategy-1', 'value': 'Strategy-1'},
                                    {'label': 'Strategy-2', 'value': 'Strategy-2'},
                                    {'label': 'Strategy-3', 'value': 'Strategy-3'},
                                    {'label': 'Strategy-4', 'value': 'Strategy-4'},
                                    {'label': 'Strategy-5', 'value': 'Strategy-5'}
                                ], value='Strategy-1', placeholder='Select strategy...', className='strategy-picker4'),
                        ], className='stock-strategy'),

                        dcc.RadioItems(
                            id='strategy-type4',
                            options=[
                                {'label': 'Long', 'value': 'Long'},
                                {'label': 'Short', 'value': 'Short'},
                                {'label': 'Long+Short', 'value': 'Long+Short'},
                            ],
                            value='Long'
                        ),

                        dash_table.DataTable(
                            id='table_ratio4',
                            data=df1.to_dict('records'),
                            columns=[{'id': c, 'name': c} for c in df1.columns],
                            style_cell={'textAlign': 'center', 'width': '100px', 'minWidth': '100px',
                                        'maxWidth': '100px'},
                            fixed_rows={'headers': True, 'data': 0},
                            style_header={'fontWeight': 'bold'},
                            style_table={'overflowX': 'auto'},
                            editable=True
                        ),

                        html.Button('Start / Stop', id='simulation-execute-button', n_clicks=0,
                                    style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'})

                    ], id='simulation'),

                    html.Div(id='my-output-7'),

                ], className='three columns'),

                html.Div([
                    html.Div([
                        html.Div([
                            dash_table.DataTable(
                                id='dynamic-table',
                                data=df.to_dict('records'),
                                columns=[{'id': c, 'name': c} for c in df.columns],
                                style_cell={'textAlign': 'center', 'width': '60px', 'minWidth': '60px', 'maxWidth': '60px'},
                                fixed_rows={'headers': True, 'data': 0},
                                style_header={'fontWeight': 'bold', 'backgroundColor': 'rgb(66,196,247)'},
                                page_size=5,
                                style_data_conditional=[]
                            )
                        ], className='nine columns'),

                        html.Div([
                            html.Div(id='my-output-4'),
                            html.Div(id='my-output-5'),
                            html.Div(id='my-output-6'),
                        ], id='results_panel', className='three columns'),

                    ], className='twelve columns'),

                    html.Div(id='dynamic-graph-2', className='twelve columns'),

                ], className='nine columns')

            ], id='dynamic-top-part', className='twelve columns'),

            html.Div([
                dash_table.DataTable(
                    id='dynamic-table-3',
                    data=df3.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in df3.columns],
                    style_cell={'textAlign': 'center', 'width': '60px', 'minWidth': '60px', 'maxWidth': '60px'},
                    fixed_rows={'headers': True, 'data': 0},
                    style_header={'fontWeight': 'bold', 'backgroundColor': 'rgb(66,196,247)'},
                    page_size=5,
                    style_data_conditional=[]
                )
            ], className='twelve columns'),

            dcc.Interval(
                id='interval-component',
                interval=1*10, # in milliseconds
                n_intervals=0,
                disabled=True
            )

        ])

@app.callback(
             [Output(component_id='dynamic-table', component_property='data'),
              Output(component_id='dynamic-table', component_property='style_data_conditional'),
              Output(component_id='dynamic-table-3', component_property='data'),
              Output(component_id='dynamic-table-3', component_property='style_data_conditional'),
              Output(component_id='table_ratio4', component_property='data'),
              Output(component_id='dynamic-graph-2', component_property='children'),
              Output(component_id='my-output-1', component_property='children'),
              Output(component_id='my-output-3', component_property='children'),
              Output(component_id='my-output-4', component_property='children'),
              Output(component_id='my-output-5', component_property='children'),
              Output(component_id='my-output-6', component_property='children'),
              Output(component_id='my-output-7', component_property='children'),
              Output(component_id='interval-component', component_property='disabled')],
             [Input(component_id='simulation-execute-button', component_property='n_clicks'),
             Input(component_id='interval-component', component_property='n_intervals')],
             [State(component_id='start_date4', component_property='date'),
             State(component_id='end_date4', component_property='date'),
             State(component_id='stock-input4', component_property='value'),
             State(component_id='commission-input4', component_property='value'),
             State(component_id='strategy4', component_property='value'),
             State(component_id='strategy-type4', component_property='value'),
             State(component_id='capital-input4', component_property='value')]
            )

def update_table(n_clicks, n, start_date, end_date, stock, commission, strategy, strategy_type, capital):

    global position, balance, df3, data1, style_data_conditional, data3, style_data_conditional_2, data2,\
    graph_2, output1, output3, output4, output5, output6, output7, a1, b1, b2, df_reverse

    # formule strategy ve strategy type ekleyeceksin!!!!

    DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
        "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
    con = sqlite3.connect(str(DB_FILE))
    statement2 = f"SELECT * FROM my_works WHERE Instrument='{stock}';"
    df_ = pd.read_sql_query(statement2, con)
    df_x = df1.copy()
    df_x['1.Profit'] = [df_['1.Profit Dec.'], df_['1.Profit Inc.']]
    df_x['1.Stop'] = [df_['1.Stop Dec.'], df_['1.Stop Inc.']]
    data2 = df_x.to_dict('records')

    if n_clicks == 0:
        output1 = 'Balance: {}'.format('--')
        output3 = 'Total P/L: {}'.format('--')
        output4 = 'Buy Price: {}'.format('--')
        output5 = 'Take Profit Price: {}'.format('--')
        output6 = 'Stop Loss Price: {}'.format('--')
        output7 = '--'
        return [], [], [], [], data2, '', output1, output3, output4, output5, output6, output7, True

    elif n_clicks % 2 == 1:

        DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
            "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
        con = sqlite3.connect(str(DB_FILE))
        if n == 0:
            statement = f"SELECT * FROM {stock} WHERE (id<={n+2}) AND (Date BETWEEN '{start_date}' AND '{end_date}');"
        else:
            statement = f"SELECT * FROM {stock} WHERE (id={n + 2}) AND (Date BETWEEN '{start_date}' AND '{end_date}');"

        df = pd.read_sql_query(statement, con)
        df.Date = df.Date.str[:10]
        df['Combine'] = df.Date+df.Hour
        if n == 0:
            df_reverse = pd.DataFrame()
            df = df[::-1]
        df_reverse = pd.concat([df, df_reverse], axis=0, ignore_index=True)[:5]
        data1 = df_reverse.to_dict('records')


        if df_reverse.loc[0,'Close'] > df_reverse.loc[1,'Close']:
            style_data_conditional = [{'if': {'row_index': 0},
                                     'backgroundColor': 'green'}]
        elif df_reverse.loc[0,'Close'] < df_reverse.loc[1,'Close']:
            style_data_conditional = [{'if': {'row_index': 0},
                                        'backgroundColor': 'red'}]
        else:
            style_data_conditional = [{'if': {'row_index': 0},
                                        'backgroundColor': 'white'}]


        if n == 0 or (position == 0 and df_reverse.Date[0] != df_reverse.Date[1]):
            position = 1
            if n == 0:
                balance = capital

            df_trade = pd.DataFrame()
            df_trade.loc[0,'#'] = len(df3) + 1
            df_trade.loc[0,'Position'] = 'Long'
            df_trade.loc[0,'B.Date'] = df_reverse.loc[1,'Date']
            df_trade.loc[0,'B.Lot'] = round((1-commission/10000)*balance/df_reverse.loc[1,'Close'])-1
            df_trade.loc[0,'B.Price'] = df_reverse.loc[1,'Close']
            df_trade.loc[0,'B.Total'] = round(df_trade.loc[0,'B.Lot']*df_trade.loc[0,'B.Price'],2)
            df_trade.loc[0,'Commission'] = round(df_trade.loc[0,'B.Total']*commission/10000, 2)
            df_trade.loc[0,'Balance'] = round(balance - df_trade.loc[0,'B.Total'] - df_trade.loc[0,'Commission'],2)

            df_trade.loc[0,'S.Date'] = '--'
            df_trade.loc[0,'S.Lot'] = '--'
            df_trade.loc[0,'S.Price'] = '--'
            df_trade.loc[0,'S.Total'] = '--'
            df_trade.loc[0,'Trans P/L'] = '--'

            if len(df3) == 0:
                df_trade.loc[0,'Total P/L'] = '--'
            else:
                df_trade.loc[0,'Total P/L'] = df3.loc[0,'Total P/L']

            df3 = pd.concat([df_trade, df3], axis=0, ignore_index=True)

            a1 = df3.loc[0, 'B.Price']

            if df_reverse.loc[1,'MA'] > df_reverse.loc[1,'Close']:
                b1 = rounder(a1 * (1+df_x.loc[0, '1.Stop']), False)
                b2 = rounder(a1 * (1+df_x.loc[0, '1.Profit']), True)

            else:
                b1 = rounder(a1 * (1+df_x.loc[1, '1.Stop']), False)
                b2 = rounder(a1 * (1+df_x.loc[1, '1.Profit']), True)

                
        elif position == 1:

            lot1 = df3.loc[0, 'B.Lot']

            if df_reverse.Low[1] > b1 and df_reverse.High[1] < b2:
                pass
            elif df_reverse.Date[1] != df_reverse.Date[2] and df_reverse.Open[1] <= b1:
                position = 0
                df3.loc[0,'S.Date'] = df_reverse.loc[1, 'Date']
                df3.loc[0,'S.Lot'] = lot1
                df3.loc[0,'S.Price'] = df_reverse.loc[1, 'Open']
                df3.loc[0,'S.Total'] = round(lot1*df_reverse.loc[1, 'Open'], 2)
                df3.loc[0,'Commission'] = round(df3.loc[0,'Commission'] + df3.loc[0,'S.Total']*commission/10000, 2)
                df3.loc[0,'Trans P/L'] = round(df3.loc[0,'S.Total'] - df3.loc[0,'B.Total'] - df3.loc[0,'Commission'], 2)
                if len(df3) == 1:
                    df3.loc[0,'Total P/L'] = df3.loc[0,'Trans P/L']
                else:
                    df3.loc[0, 'Total P/L'] = round(df3.loc[0, 'Trans P/L'] + df3.loc[0, 'Total P/L'],2)
                df3.loc[0,'Balance'] = round(capital + df3.loc[0, 'Total P/L'], 2)
                balance = df3.loc[0, 'Balance']

            elif df_reverse.Date[1] != df_reverse.Date[2] and df_reverse.Open[1] >= b2:
                position = 0
                df3.loc[0,'S.Date'] = df_reverse.loc[1, 'Date']
                df3.loc[0,'S.Lot'] = lot1
                df3.loc[0,'S.Price'] = df_reverse.loc[1, 'Open']
                df3.loc[0,'S.Total'] = round(lot1 * df_reverse.loc[1, 'Open'], 2)
                df3.loc[0,'Commission'] = round(df3.loc[0,'Commission'] + df3.loc[0,'S.Total']*commission/10000, 2)
                df3.loc[0,'Trans P/L'] = round(df3.loc[0,'S.Total'] - df3.loc[0,'B.Total'] - df3.loc[0,'Commission'], 2)
                if len(df3) == 1:
                    df3.loc[0,'Total P/L'] = df3.loc[0,'Trans P/L']
                else:
                    df3.loc[0, 'Total P/L'] = round(df3.loc[0, 'Trans P/L'] + df3.loc[0, 'Total P/L'],2)
                df3.loc[0, 'Balance'] = round(capital + df3.loc[0, 'Total P/L'], 2)
                balance = df3.loc[0, 'Balance']

            elif df_reverse.Low[1] <= b1:
                position = 0
                df3.loc[0,'S.Date'] = df_reverse.loc[1, 'Date']
                df3.loc[0,'S.Lot'] = lot1
                df3.loc[0,'S.Price'] = b1
                df3.loc[0,'S.Total'] = round(lot1 * b1, 2)
                df3.loc[0,'Commission'] = round(df3.loc[0,'Commission'] + df3.loc[0,'S.Total']*commission/10000, 2)
                df3.loc[0,'Trans P/L'] = round(df3.loc[0,'S.Total'] - df3.loc[0,'B.Total'] - df3.loc[0,'Commission'], 2)
                if len(df3) == 1:
                    df3.loc[0,'Total P/L'] = df3.loc[0,'Trans P/L']
                else:
                    df3.loc[0, 'Total P/L'] = round(df3.loc[0, 'Trans P/L'] + df3.loc[0, 'Total P/L'],2)
                df3.loc[0, 'Balance'] = round(capital + df3.loc[0, 'Total P/L'], 2)
                balance = df3.loc[0, 'Balance']

            elif df_reverse.High[1] >= b2:
                position = 0
                df3.loc[0,'S.Date'] = df_reverse.loc[1, 'Date']
                df3.loc[0,'S.Lot'] = lot1
                df3.loc[0,'S.Price'] = b2
                df3.loc[0,'S.Total'] = round(lot1 * b2, 2)
                df3.loc[0,'Commission'] = round(df3.loc[0,'Commission'] + df3.loc[0,'S.Total']*commission/10000, 2)
                df3.loc[0,'Trans P/L'] = round(df3.loc[0,'S.Total'] - df3.loc[0,'B.Total'] - df3.loc[0,'Commission'], 2)
                if len(df3) == 1:
                    df3.loc[0,'Total P/L'] = df3.loc[0,'Trans P/L']
                else:
                    df3.loc[0, 'Total P/L'] = round(df3.loc[0, 'Trans P/L'] + df3.loc[0, 'Total P/L'],2)
                df3.loc[0, 'Balance'] = round(capital + df3.loc[0, 'Total P/L'], 2)
                balance = df3.loc[0, 'Balance']


        elif position == 0 and df_reverse.Date[0] == df_reverse.Date[1]:
            pass

        data3 = df3.to_dict('records')

        graph_2 = dcc.Graph(
            id='graph',
            figure={
                'data': [
                    {'x': df3['S.Date'], 'y': df3['Total P/L'], 'type': 'line', 'color': 'blue', 'name': stock},
                ],
                'layout': {
                    'title': 'Profit/Loss',
                    'height': 400
                }
            })


        if df3.loc[0,'Trans P/L'] == '--' or df3.loc[0,'Trans P/L'] == 0:
            style_data_conditional_2 = [{'if': {'row_index': 0},
                                     'backgroundColor': 'white'}]
        elif df3.loc[0,'Trans P/L'] <0:
            style_data_conditional_2 = [{'if': {'row_index': 0},
                                        'backgroundColor': 'red'}]
        else:
            style_data_conditional_2 = [{'if': {'row_index': 0},
                                        'backgroundColor': 'green'}]
        output1 = 'Balance: {} $'.format(balance)

        pl = df3['Total P/L'][0]
        if pl == '--' or pl >= 0:
            output3 = 'Total P/L: {} $ profit'.format(pl)
        else:
            output3 = 'Total P/L: {} $ loss'.format(-pl)


        if position == 1:
            output4 = 'Buy Price: {}'.format(a1)
            output5 = 'Take Profit Price: {}'.format(b2)
            output6 = 'Stop Loss Price: {}'.format(b1)

        else:
            output4 = 'Buy Price: {}'.format('--')
            output5 = 'Take Profit Price: {}'.format('--')
            output6 = 'Stop Loss Price: {}'.format('--')


        if position == 1:
            output7 = 'Buy order is executed. Sell order is sent.'
        else:
            output7 = 'Sell order is executed. Buy order is sent.'
        return data1, style_data_conditional, data3, style_data_conditional_2, data2, graph_2, output1, output3, output4, output5, output6, output7, False

    else:
        output7 = 'Simulation is stopped !'
        return data1, style_data_conditional, data3, style_data_conditional_2, data2, graph_2, output1, output3, output4, output5, output6, output7, True

# if __name__ == '__main__':
#     app.run_server(debug=True)
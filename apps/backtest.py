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
from dash.exceptions import PreventUpdate
from apps.calculation import *


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__,
#               external_stylesheets=external_stylesheets)

from app import app

df1 = pd.DataFrame()
df1['1.Profit'] = ['--', '--']
df1['1.Stop'] = ['--', '--']

df3 = pd.DataFrame()
columns3 = ['Instrument', 'Strategy', 'Start', 'End', 'Stra. Type', 'Commis. Rate', '1.Profit Dec.', '1.Stop Dec.',
            '1.Profit Inc.', '1.Stop Inc.']
results3 = ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--']
for i in range(len(columns3)):
    df3[columns3[i]] = [results3[i]]

df4 = pd.DataFrame()
columns4 = ['Total Profit', 'Net Profit', 'Inc. Profit', 'Dec. Profit', '# trans.', 'Avr.Pro(trans)', '# days in pos.',
            'Avr.Pro(day)', 'Sharpe', 'Std. dev.']
results4 = ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--']
for i in range(len(columns4)):
    df4[columns4[i]] = [results4[i]]

layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                dcc.DatePickerSingle(
                    id='start_date',
                    placeholder='Start date...',
                    date='2014-08-29'
                ),
                dcc.DatePickerSingle(
                    id='end_date',
                    placeholder='End date...',
                    date='2019-09-01'
                )
            ], className='date-picker'),

            html.Div([
                dcc.Input(id='commission-input', type='number', placeholder='Commission', min=0, value=2),
                dcc.Input(id='capital-input', type='number', placeholder='Capital', min=0, value=10000),
            ], className='commission-capital'),

            html.Div([
                dcc.Input(
                    id='stock-input',
                    type='text',
                    value='KOZAA',
                    placeholder='Select stock...',
                    className='stock-picker'),

                html.Button('Bring data', id='bring-data-button', n_clicks=0,
                            style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'}),
            ], className='stock-picker-bring-data'),

            dcc.Dropdown(
                id='strategy',
                options=[
                    {'label': 'Strategy-1', 'value': 'Strategy-1'},
                    {'label': 'Strategy-2', 'value': 'Strategy-2'},
                    {'label': 'Strategy-3', 'value': 'Strategy-3'},
                    {'label': 'Strategy-4', 'value': 'Strategy-4'},
                    {'label': 'Strategy-5', 'value': 'Strategy-5'}
                ], value='Strategy-1', placeholder='Select strategy...', className='strategy-picker'),

            dcc.RadioItems(
                id='strategy-type',
                options=[
                    {'label': 'Long', 'value': 'Long'},
                    {'label': 'Short', 'value': 'Short'},
                    {'label': 'Long+Short', 'value': 'Long+Short'},
                ],
                value='Long'
            ),

            dash_table.DataTable(
                id='table_ratio',
                data=df1.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df1.columns],
                style_cell={'textAlign': 'center', 'width': '100px', 'minWidth': '100px', 'maxWidth': '100px'},
                fixed_rows={'headers': True, 'data': 0},
                style_header={'fontWeight': 'bold'},
                style_table={'overflowX': 'auto'},
                editable=True
            ),

            html.Div([

                dcc.Checklist(
                    id='colored-type',
                    options=[
                        {'label': 'Color', 'value': 'Clr'}
                    ],
                    value=['Clr']
                ),

                html.Button('Execute', id='execute-button', n_clicks=0,
                            style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'})

            ], className='execute-colored')

        ], id='backtest', className='three columns'),

        html.Div([
            html.Div(id='stock-chart'),
            dcc.Upload(
                id='datatable-upload',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%', 'height': '80px', 'lineHeight': '80px',
                    'borderWidth': '1px', 'borderStyle': 'dashed',
                    'textAlign': 'center', 'margin-top': '15px', 'background-color': 'white'
                },
            )
        ], className='nine columns'),

        html.Div([
            dash_table.DataTable(
                id='table_feature',
                data=df3.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df3.columns],
                style_cell={'textAlign': 'center', 'width': '100px', 'minWidth': '100px', 'maxWidth': '100px'},
                fixed_rows={'headers': True, 'data': 0},
                style_header={'fontWeight': 'bold'},
                style_table={'overflowX': 'auto'},
                editable=True
            ),

            dash_table.DataTable(
                id='table_results',
                data=df4.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df4.columns],
                style_cell={'textAlign': 'center', 'width': '100px', 'minWidth': '100px', 'maxWidth': '100px'},
                fixed_rows={'headers': True, 'data': 0},
                style_header={'fontWeight': 'bold'},
                style_table={'overflowX': 'auto'},
                editable=True
            ),

            html.Button('Send to My works', id='send-results-button', n_clicks=0,
                        style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'}),
            html.Button('Send To Analysis', id='analysis-button', n_clicks=0,
                        style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'}),
            html.Progress(id="progress", value="70", max="100")

        ], className='twelve columns'),

    ], className='twelve columns'),

    html.Div(id='stock-table', className='twelve columns'),

    html.Div(id='hidden-div', style={'display': 'none'}),
])


@app.callback(
    Output(component_id='hidden-div', component_property='children'),
    [Input(component_id='send-results-button', component_property='n_clicks'),
     Input(component_id='analysis-button', component_property='n_clicks')],
     [State(component_id='table_feature', component_property='data'),
     State(component_id='table_results', component_property='data')]
            )
def send_db_and_analysis(n_clicks1, n_clicks2, data1, data2):
    ctx = dash.callback_context

    if (n_clicks1 == None) & (n_clicks2 == None):
        return ''

    else:
        pie = ctx.triggered[0]['prop_id'].split('.')[0]

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        save_date = dt_string[:10]
        save_time = dt_string[11:]

        df_data1 = pd.DataFrame(data1)
        df_data2 = pd.DataFrame(data2)


        df_sum = pd.concat([df_data1, df_data2], axis=1) # As a rule of thumb, it's not safe to change any variables outside of the scope of a callback function. You can read from global variables, but you can't write to them.
        df_sum['Save date'] = str(save_date)
        df_sum['Save time'] = str(save_time)
        df_sum['Status'] = 'Test'


        DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
            "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
        conn = sqlite3.connect(str(DB_FILE))

        if pie == 'send-results-button':
            df_sum.to_sql('my_works', conn, if_exists='append', index=False)

        elif pie == 'analysis-button':
            df_sum.to_sql('temporary_table', conn, if_exists='append', index=False)

        return 'it is ok'


@app.callback(
    [Output(component_id='stock-chart', component_property='children'),
     Output(component_id='stock-table', component_property='children'),
     Output(component_id='table_ratio', component_property='data'),
     Output(component_id='table_feature', component_property='data'),
     Output(component_id='table_results', component_property='data')],
    [Input(component_id='bring-data-button', component_property='n_clicks'),
     Input(component_id='execute-button', component_property='n_clicks')],
    [State(component_id='stock-input', component_property='value'),
     State(component_id='start_date', component_property='date'),
     State(component_id='end_date', component_property='date'),
     State(component_id='commission-input', component_property='value'),
     State(component_id='strategy', component_property='value'),
     State(component_id='strategy-type', component_property='value')]
)



def update_fig(n_clicks1, n_clicks2, stock, start_date, end_date, commission, strategy, strategy_type):

    ctx = dash.callback_context
    pie = ctx.triggered[0]['prop_id'].split('.')[0]

    stock_list = ['ARCLK', 'BIMAS', 'EREGL', 'FROTO', 'KOZAA', 'KOZAL', 'KRDMD', 'PETKM', 'PGSUS', 'SISE', 'SODA',
                  'TAVHL', 'TCELL', 'THYAO', 'TKFEN', 'TOASO', 'TTKOM', 'TUPRS']

    if stock in stock_list:

        DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
            "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
        con = sqlite3.connect(str(DB_FILE))
        statement = f"SELECT * FROM {stock} WHERE Date BETWEEN '{start_date}' AND '{end_date}';"
        df = pd.read_sql_query(statement, con)
        df.Date = df.Date.str[:10]
        # df['Combine'] = df.Date + df.Hour
        df = df.rename(columns={'id': '#'})
        df['Color'] = ['--' for i in range(len(df))]
        df['Position'] = ['--' for i in range(len(df))]
        df['Code'] = ['--' for i in range(len(df))]
        df['Profit'] = ['--' for i in range(len(df))]
        df['Net Profit'] = ['--' for i in range(len(df))]
        df['# trans'] = ['--' for i in range(len(df))]
        df['# days'] = ['--' for i in range(len(df))]


        # con = sqlite3.connect(str(DB_FILE))
        # statement_kkk = f"SELECT * FROM KOZAA_daily;"
        # df_kkk = pd.read_sql_query(statement_kkk, con)
        # # df_kkk['Date'] = pd.to_datetime(df_kkk['Date'])
        # # df_kkk['Date'] = df_kkk['Date'].dt.strftime("%Y-%m-%d")
        # print(df_kkk)

        statement2 = f"SELECT * FROM my_works WHERE Instrument='{stock}';"
        df_ = pd.read_sql_query(statement2, con)
        df_x = df1.copy()
        df_x['1.Profit'] = [df_['1.Profit Dec.'], df_['1.Profit Inc.']]
        df_x['1.Stop'] = [df_['1.Stop Dec.'], df_['1.Stop Inc.']]
        data = df_x.to_dict('records')


    else:

        df = web.DataReader(stock, 'yahoo', start_date, end_date).reset_index()
        df['#'] = [i for i in range(1, len(df) + 1)]
        df.Date = df.Date.map(lambda x: str(x)[:10])
        df = df[['#', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

        df_x = df1.copy()
        data = df_x.to_dict('records')

    if ((n_clicks1 == 0) & (n_clicks2 == 0)) or (pie == 'bring-data-button'):

        DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
            "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
        con = sqlite3.connect(str(DB_FILE))
        cur = con.cursor()
        statement3 = f"SELECT * FROM temporary_table;"
        dff = pd.read_sql_query(statement3, con)

        if not dff.empty:
            data1 = dff[dff.columns[1:11]].to_dict('records')
            data2 = dff[dff.columns[11:21]].to_dict('records')

            statement2 = f"DELETE FROM temporary_table;"
            cur.execute(statement2)
            con.commit()


        else:
            data1 = df3.copy().to_dict('records')
            data2 = df4.copy().to_dict('records')


        return [dcc.Graph(
            id='graph',
            figure={
                'data': [
                    {'x': df.Date, 'y': df.Close, 'type': 'line', 'color':'blue','name': stock},
                    # {'x': df.Date, 'y': df_kkk['MA(19)'], 'type': 'line', 'color':'red', 'name': '19d-MA'}
                ],
                'layout': {
                    'title': stock,
                    'height': 400,
                }
            }
        ), dash_table.DataTable(
            id='table',
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            style_cell={'textAlign': 'center', 'width': '98px', 'minWidth': '98px', 'maxWidth': '98px'},
            fixed_rows={'headers': True, 'data': 0},
            style_header={'fontWeight': 'bold', 'backgroundColor': 'rgb(66,196,247)'}

        ), data, data1, data2]

    elif pie == 'execute-button':

        DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
            "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
        con = sqlite3.connect(str(DB_FILE))
        statement = f"SELECT * FROM my_works WHERE Instrument='{stock}';"
        df_k = pd.read_sql_query(statement, con)

        df_y = df3.copy()
        df_y['1.Profit Dec.'] = [df_k['1.Profit Dec.']][0]
        df_y['1.Stop Dec.'] = [df_k['1.Stop Dec.']][0]
        df_y['1.Profit Inc.'] = [df_k['1.Profit Inc.']][0]
        df_y['1.Stop Inc.'] = [df_k['1.Stop Inc.']][0]
        df_y['Instrument'] = str(stock)
        df_y['Strategy'] = str(strategy)
        df_y['Start'] = str(start_date)
        df_y['End'] = str(end_date)
        df_y['Stra. Type'] = str(strategy_type)
        df_y['Commis. Rate'] = int(commission)

        statement2 = f"SELECT * FROM {stock} WHERE Date BETWEEN '{start_date}' AND '{end_date}';"
        df = pd.read_sql_query(statement2, con)
        df.Date = df.Date.str[:10]
        df = df.rename(columns={'id': '#'})
        df['Color'] = ['--' for i in range(len(df))]
        df['Position'] = ['--' for i in range(len(df))]
        df['Code'] = ['--' for i in range(len(df))]
        df['Profit'] = ['--' for i in range(len(df))]
        df['Net Profit'] = ['--' for i in range(len(df))]
        df['# trans'] = ['--' for i in range(len(df))]
        df['# days'] = ['--' for i in range(len(df))]

        df_x = df4.copy()

        if strategy == 'Strategy-1':
            start = datetime.now()
            kar, net_kar, net_kar1, net_kar2, isl_say, pro_trans, df = strategy_1(df, df_y, commission)
            print(datetime.now()-start)


        df_x['Total Profit'] = kar
        df_x['Net Profit'] = net_kar
        df_x['Inc. Profit'] = net_kar2
        df_x['Dec. Profit'] = net_kar1
        df_x['# trans.'] = isl_say
        df_x['Avr.Pro(trans)'] = pro_trans
        df_x['# days in pos.'] = 0
        df_x['Avr.Pro(day)'] = 0
        df_x['Sharpe'] = 0
        df_x['Std. dev.'] = 0

        data1 = df_y.to_dict('records')
        data2 = df_x.to_dict('records')

        df_temp2 = df[['Date','Profit']][:-1]
        df_temp2['Cumulative'] = np.cumsum(df['Profit'][:-1])
        df_temp2['Name'] = str(stock)

        statementt = f"SELECT * FROM temporary_table_2;"
        dfft = pd.read_sql_query(statementt, con)
        if not dfft.empty:
            cur = con.cursor()
            statementy = f"DELETE FROM temporary_table_2;"
            cur.execute(statementy)
            con.commit()
            df_temp2.to_sql('temporary_table_2', con, if_exists='append', index=False)
        else:
            df_temp2.to_sql('temporary_table_2', con, if_exists='append', index=False)

        return [dcc.Graph(
            id='graph',
            figure={
                'data': [
                    {'x': df.Date, 'y': df.Close, 'type': 'line', 'name': stock}
                ],
                'layout': {
                    'title': stock,
                    'height': 400
                }
            }
        ), dash_table.DataTable(
            id='table',
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            style_cell={'textAlign': 'center', 'width': '98px', 'minWidth': '98px', 'maxWidth': '98px'},
            fixed_rows={'headers': True, 'data': 0},
            style_header={'fontWeight': 'bold', 'backgroundColor': 'rgb(66,196,247)'}

        ), data, data1, data2]


# if __name__ == '__main__':
#     app.run_server(debug=True)

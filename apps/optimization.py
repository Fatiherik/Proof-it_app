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
from apps.backtest import df3, df4
from apps.calculation import *
from app import app

df33 = df3.copy()
df44 = df4.copy()

layout = html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.DatePickerSingle(
                                id='start_date2',
                                placeholder='Start date...',
                                date='2014-08-29'
                            ),
                            dcc.DatePickerSingle(
                                id='end_date2',
                                placeholder='End date...',
                                date='2019-09-01'
                            )
                        ], className='date-picker2'),

                        html.Div([
                            dcc.Input(id='commission-input2', type='number', placeholder='Commission', min=0, value=2),
                            dcc.Input(id='capital-input2', type='number', placeholder='Capital', min=0, value=10000),
                        ], className='commission-capital2'),

                        html.Div([
                            dcc.Input(
                                id='stock-input2',
                                type='text',
                                value='KOZAA',
                                placeholder='Select stock...',
                                className='stock-picker2'),

                            html.Button('Bring data', id='bring-data-button2', n_clicks=0, style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'}),
                        ], className='stock-picker-bring-data2'),

                        dcc.Dropdown(
                            id='strategy2',
                            options=[
                                {'label': 'Strategy-1', 'value': 'Strategy-1'},
                                {'label': 'Strategy-2', 'value': 'Strategy-2'},
                                {'label': 'Strategy-3', 'value': 'Strategy-3'},
                                {'label': 'Strategy-4', 'value': 'Strategy-4'},
                                {'label': 'Strategy-5', 'value': 'Strategy-5'}
                                ], value='Strategy-1', placeholder='Select strategy...', className='strategy-picker2'),

                        html.Div([
                            html.Label('Make all ratio'),
                            dcc.Input(id='ratio', type='number', placeholder='this value', min=0, value=0.01)
                        ], className='about-ratios-ratio')

                    ], id='optimization-1', className='three columns'),

                    html.Div([

                        html.Div([
                            dcc.Input(id='first-var-no', type='number', placeholder='Var No', min=0, value=''),
                            dcc.Input(id='second-var-no', type='number', placeholder='Var No', min=0, value=''),
                            dcc.Input(id='third-var-no', type='number', placeholder='Var No', min=0, value='')
                        ], className='var-no-input'),

                        html.Div([
                            html.Label('1.Range'),
                            html.Label('2.Range'),
                            html.Label('3.Range')
                        ], className='range-value-label'),

                        html.Div([
                            dcc.Input(id='first-range-from', type='number', placeholder='From', min=0, value=''),
                            dcc.Input(id='second-range-from', type='number', placeholder='From', min=0, value=''),
                            dcc.Input(id='third-range-from', type='number', placeholder='From', min=0, value='')
                        ], className='input-from'),

                        html.Div([
                            dcc.Input(id='first-range-to', type='number', placeholder='To', min=0, value=''),
                            dcc.Input(id='second-range-to', type='number', placeholder='To', min=0, value=''),
                            dcc.Input(id='third-range-to', type='number', placeholder='To', min=0, value=''),
                        ], className='input-to'),

                        dcc.Input(id='step-input', type='number', placeholder='Step', min=0, value=''),

                    ], id='optimization-2', className='three columns'),

                    html.Div([

                        dcc.RadioItems(
                            id='criteria',
                            options=[
                                {'label': 'Net Profit', 'value': 'NP'},
                                {'label': 'Sharpe', 'value': 'SRP'},
                                {'label': 'Net Pro/Inc', 'value': 'NPI'},
                                {'label': 'Sharpe/Inc', 'value': 'SRPI'},
                                {'label': 'Net Pro/Dec', 'value': 'NPD'},
                                {'label': 'Sharpe/Dec', 'value': 'SRPD'},

                            ],
                            value='NP',
                            labelStyle={'margin-top':'10px','display': 'inline-block', 'margin-right':'30px'}
                        ),

                        dcc.RadioItems(
                            id='strategy-type2',
                            options=[
                                {'label': 'Long', 'value': 'Lng'},
                                {'label': 'Short', 'value': 'Sht'},
                                {'label': 'Long+Short', 'value': 'Lng+Sht'},
                            ],
                            value='Lng'
                        ),

                        dcc.RadioItems(
                            id='colored-type2',
                            options=[
                                {'label': 'Color', 'value': 'Clr'}
                            ],
                            value='Clr',
                        ),

                        html.Button('Execute', id='execute-button2', n_clicks=0, style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'})

                    ], id='optimization-3',className='three columns')

                ], id='back-opt'),

                html.Div([

                    dash_table.DataTable(
                        id='table_feature2',
                        data=df33.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df3.columns],
                        style_cell={'textAlign': 'center', 'width':'100px','minWidth': '100px', 'maxWidth': '100px'},
                        fixed_rows={'headers': True, 'data': 0},
                        style_header={'fontWeight': 'bold'},
                        style_table={'overflowX': 'auto'},
                        editable=True
                        ),

                    dash_table.DataTable(
                        id='table_results2',
                        data=df44.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df4.columns],
                        style_cell={'textAlign': 'center', 'width':'100px','minWidth': '100px', 'maxWidth': '100px'},
                        fixed_rows={'headers': True, 'data': 0},
                        style_header={'fontWeight': 'bold'},
                        style_table={'overflowX': 'auto'},
                        editable=True
                        ),

                    html.Button('Send to My works', id='send-results-button-2', n_clicks=0, style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'}),
                    html.Button('Send to Backtest', id='send-backtest-button', n_clicks=0, style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'}),
                ], className='twelve columns'),

                html.Div(id='hidden-div-2', style={'display': 'none'}),
            ])


@app.callback(
            Output(component_id='hidden-div-2',component_property='children'),
            [Input(component_id='send-results-button-2',component_property='n_clicks'),
             Input(component_id='send-backtest-button',component_property='n_clicks')],
            [State(component_id='table_feature2', component_property='data'),
            State(component_id='table_results2', component_property='data')]
            )

def save_db_and_backtest (n_clicks1,n_clicks2, data1, data2):

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

        df_sum = pd.concat([df_data1, df_data2], axis=1)      # As a rule of thumb, it's not safe to change any variables outside of the scope of a callback function. You can read from global variables, but you can't write to them.
        df_sum['Save date'] = save_date
        df_sum['Save time'] = save_time
        df_sum['Status'] = 'Optimum'

        conn = sqlite3.connect("/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db")

        if pie == 'send-results-button-2':
            df_sum.to_sql('my_works', conn, if_exists='append', index=False)

        elif pie == 'send-backtest-button':
            df_sum.to_sql('temporary_table', conn, if_exists='append', index=False)

        return 'it is ok'

@app.callback(
    [Output(component_id='table_feature2', component_property='data'),
     Output(component_id='table_results2', component_property='data')],
    [Input(component_id='execute-button2', component_property='n_clicks')],
    [State(component_id='start_date2', component_property='date'),
     State(component_id='end_date2', component_property='date'),
     State(component_id='commission-input2', component_property='value'),
     State(component_id='stock-input2', component_property='value'),
     State(component_id='strategy2', component_property='value'),
     State(component_id='ratio',component_property='value'),
    State(component_id='first-var-no', component_property='value'),
    State(component_id='second-var-no', component_property='value'),
    State(component_id='third-var-no', component_property='value'),
    State(component_id='first-range-from', component_property='value'),
    State(component_id='second-range-from', component_property='value'),
    State(component_id='third-range-from', component_property='value'),
    State(component_id='first-range-to', component_property='value'),
    State(component_id='second-range-to', component_property='value'),
    State(component_id='third-range-to', component_property='value'),
    State(component_id='step-input', component_property='value'),
    State(component_id='criteria', component_property='value'),
    State(component_id='strategy-type2', component_property='value'),
     ]
)
def calculation(n_clicks, start_date, end_date, commission, stock, strategy, ratio, var_no1, var_no2, var_no3, var_from1, var_from2, var_from3,
                var_to1,var_to2,var_to3, step, criteria, strategy_type):

    if n_clicks == 0:

        data1 = df33.copy().to_dict('records')
        data2 = df44.copy().to_dict('records')
        return data1, data2


    else:
        DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
            "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
        con = sqlite3.connect(str(DB_FILE))
        statement = f"SELECT * FROM my_works WHERE Instrument='{stock}';"
        df_ = pd.read_sql_query(statement, con)

        df_y = df33.copy()

        df_y['Instrument'] = str(stock)
        df_y['Strategy'] = str(strategy)
        df_y['Start'] = str(start_date)
        df_y['End'] = str(end_date)
        df_y['Stra. Type'] = str(strategy_type)
        df_y['Commis. Rate'] = int(commission)
        df_y['1.Profit Dec.'] = ratio
        df_y['1.Stop Dec.'] = ratio
        df_y['1.Profit Inc.'] = ratio
        df_y['1.Stop Inc.'] = ratio


        df_x = df4.copy()
        ab = 55
        df_x['Total Profit'] = ab

        data1 = df_y.to_dict('records')
        data2 = df_x.to_dict('records')

        return data1, data2




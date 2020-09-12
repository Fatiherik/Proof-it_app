import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input, State
from datetime import datetime
import pathlib
import sqlite3
from apps.backtest import df3, df4

# external_stylesheets = [dbc.themes.BOOTSTRAP]
# app = dash.Dash(__name__,
#               external_stylesheets=external_stylesheets)


from app import app

layout = html.Div([

            html.Div([
                    dash_table.DataTable(
                        id='table_feature3',
                        data=df3.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df3.columns],
                        style_cell={'textAlign': 'center', 'width':'100px','minWidth': '100px', 'maxWidth': '100px'},
                        fixed_rows={'headers': True, 'data': 0},
                        style_header={'fontWeight': 'bold'},
                        style_table={'overflowX': 'auto'},
                        editable=True
                        ),

                    dash_table.DataTable(
                        id='table_results3',
                        data=df4.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df4.columns],
                        style_cell={'textAlign': 'center', 'width':'100px','minWidth': '100px', 'maxWidth': '100px'},
                        fixed_rows={'headers': True, 'data': 0},
                        style_header={'fontWeight': 'bold'},
                        style_table={'overflowX': 'auto'},
                        editable=True
                        )
            ]),

            html.Div([
                html.Button('Return-1', id='return-1', n_clicks=0,
                                        style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'}),
                html.Button('Return-2', id='return-2', n_clicks=0,
                                        style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'}),
                html.Button('Return-3', id='return-3', n_clicks=0,
                                        style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'}),
                html.Button('Return-4', id='return-4', n_clicks=0,
                                        style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'}),
                    ], id='panel', className='twelve columns'),

            html.Div([
                html.Div(id='stock_chart31', className='six columns'),
                html.Div(id='stock_chart32', className='six columns')
            ], id='first-two-graph', className='twelve columns'),

            html.Div([
                html.Div(id='stock_chart33', className='six columns'),
                html.Div(id='stock_chart34', className='six columns')
            ], id='second-two-graph', className='twelve columns'),

            html.Div([
                html.Div(id='stock_chart35', className='six columns'),
                html.Div(id='stock_chart36', className='six columns')
            ], id='third-two-graph', className='twelve columns'),


            html.Div(id='hidden-div3', style={'display': 'none'})

        ])

@app.callback(
            [Output(component_id='table_feature3', component_property='data'),
             Output(component_id='table_results3', component_property='data'),
             Output(component_id='stock_chart31', component_property='children'),
             Output(component_id='stock_chart32', component_property='children')],
            [Input(component_id='url', component_property='pathname')]
            )

def show_all_results(pathname):

    DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
        "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
    con = sqlite3.connect(str(DB_FILE))
    cur = con.cursor()
    statement = f"SELECT * FROM temporary_table;"
    df = pd.read_sql_query(statement, con)

    statement2 = f"SELECT * FROM temporary_table_2;"
    df2 = pd.read_sql_query(statement2, con)
    stock = df2.loc[0,'Name']
    start_date = df2.loc[0,'Date']
    end_date = df2.loc[len(df2)-1,'Date']


    statement3 = f"SELECT * FROM {stock} WHERE Date BETWEEN '{start_date}' AND '{end_date}';"
    df_k = pd.read_sql_query(statement3, con)
    df_k.Date = df_k.Date.str[:10]

    graph1 = dcc.Graph(
        id='graph',
        figure={
            'data': [
                {'x': df_k.Date, 'y': df_k.Close, 'type': 'line', 'name': stock}
            ],
            'layout': {
                'title': stock,
                'height': 390
            }
        }
    ),
    df_table = pd.DataFrame()
    df_table['Feature 1'] = ['# of days','+ closed days', '- closed days', 'notr closed days','','First Price','Last Price','% Total change','% Annual change','% Monthly change','% Daily change']
    df_table['Value 1'] = ['--','--','--','--','','--','--','--','--','--','--']
    df_table['Feature 2'] = ['Corr(str ret-market ret)', 'Corr(str ret-stock ret)','','Sharpe(Monthly)','Std dev(Monthly)','Capital turnover','','Target Price(1 month)','Target Price(6 months)','Target Price(Year)','']
    df_table['Value 2'] = ['--', '--','', '--', '--', '--','','--','--','--','']
    df_table['Feature 3'] = ['# of split','alfa','beta','Volatiliy','','Most corr stock','Least corr stock','','Daily High Time','Daily Low Time','']
    df_table['Value 3'] = ['--', '--','--','--','', '--', '--', '','--','--','']


    table1 = dash_table.DataTable(
            id='table',
            data=df_table.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df_table.columns],
            style_cell={'textAlign': 'center', 'width': '80px', 'minWidth': '80px', 'maxWidth': '80px'},
            fixed_rows={'headers': True, 'data': 0},
            style_header={'fontWeight': 'bold'}
            )

    if not df.empty:

        data1 = df.to_dict('records')
        data2 = df.to_dict('records')

        statement4 = f"DELETE FROM temporary_table;"
        cur.execute(statement4)
        con.commit()

        return data1, data2, graph1, table1

    else:
        data1 = df3.to_dict('records')
        data2 = df4.to_dict('records')

        return data1, data2, graph1, table1


@app.callback(
            Output(component_id='stock_chart33', component_property='children'),
            [Input(component_id='return-1', component_property='n_clicks')]
            )

def show_graphs2(n_clicks1):

    ctx = dash.callback_context
    pie = ctx.triggered[0]['prop_id'].split('.')[0]

    DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
        "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
    con = sqlite3.connect(str(DB_FILE))
    statement2 = f"SELECT * FROM temporary_table_2;"
    df2 = pd.read_sql_query(statement2, con)


    df22 = df2[['Date','Profit']]
    pd.to_datetime(df22.Date)
    df22['Year'] = df22['Date'].apply(lambda x: x.split("-")[0])
    df22['Month'] = df22['Date'].apply(lambda x: x.split("-")[1])
    df22_m_y = df22.groupby(['Month', 'Year']).sum()
    df22_m_y = df22_m_y.round(2)
    ###### Aylik grafik ######
    piv = pd.pivot_table(df22_m_y, values='Profit', index='Month',
                           columns='Year', aggfunc=np.sum, fill_value='--')
    flattened = pd.DataFrame(piv.to_records())
    flattened = flattened.drop(['Month'], axis=1)
    df22_m_y_ = pd.DataFrame()
    df22_m_y_['Month'] = ['January','February','March','April','May','June','July','August','September','October','November','December']
    flattened = pd.concat([df22_m_y_, flattened], axis=1)
    ###### Yillik grafik #####
    df22_y = df22.groupby(['Year']).sum()


    if (n_clicks1 == 0):

        return dash_table.DataTable(
            id='table',
            data=flattened.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in flattened.columns],
            style_cell={'textAlign': 'center', 'width': '80px', 'minWidth': '80px', 'maxWidth': '80px'},
            fixed_rows={'headers': True, 'data': 0},
            style_header={'fontWeight': 'bold', 'backgroundColor': 'rgb(66,196,247)'})

    else:

        if pie == 'return-1':
            return dash_table.DataTable(
            id='table',
            data=flattened.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in flattened.columns],
            style_cell={'textAlign': 'center', 'width': '80px', 'minWidth': '80px', 'maxWidth': '80px'},
            fixed_rows={'headers': True, 'data': 0},
            style_header={'fontWeight': 'bold', 'backgroundColor': 'rgb(66,196,247)'})


@app.callback(
    Output(component_id='stock_chart34', component_property='children'),
    [Input(component_id='return-2', component_property='n_clicks')]
)
def show_graphs3(n_clicks2):
    ctx = dash.callback_context
    pie = ctx.triggered[0]['prop_id'].split('.')[0]

    DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
        "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
    con = sqlite3.connect(str(DB_FILE))
    statement2 = f"SELECT * FROM temporary_table_2;"
    df2 = pd.read_sql_query(statement2, con)


    df22 = df2[['Date', 'Profit']]
    pd.to_datetime(df22.Date)
    df22['Year'] = df22['Date'].apply(lambda x: x.split("-")[0])
    df22['Month'] = df22['Date'].apply(lambda x: x.split("-")[1])
    df22_m_y = df22.groupby(['Month', 'Year']).sum()
    ###### Aylik grafik ######
    piv = pd.pivot_table(df22_m_y, values='Profit', index='Month',
                         columns='Year', aggfunc=np.sum, fill_value='--')
    flattened = pd.DataFrame(piv.to_records())
    flattened = flattened.drop(['Month'], axis=1)
    df22_m_y_ = pd.DataFrame()
    df22_m_y_['Month'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                          'October', 'November', 'December']
    flattened = pd.concat([df22_m_y_, flattened], axis=1)
    ###### Yillik grafik #####
    df22_y = df22.groupby(['Year']).sum()

    if (n_clicks2 == 0):

        return dcc.Graph(
                        id='graph',
                        figure={
                            'data': [
                                {'x': df2.Date, 'y': df2['Cumulative'], 'type': 'line', 'name': ''}
                            ],
                            'layout': {
                                'title': 'Total Return',
                                'height': 390
                            }
                        })

    else:

        if pie == 'return-2':
            return dcc.Graph(
                        id='graph',
                        figure={
                            'data': [
                                {'x': df2.Date, 'y': df2['Cumulative'], 'type': 'line', 'name': ''}
                            ],
                            'layout': {
                                'title': 'Total Return',
                                'height': 390
                            }
                        })


@app.callback(
    Output(component_id='stock_chart35', component_property='children'),
    [Input(component_id='return-3', component_property='n_clicks')]
)
def show_graphs4(n_clicks3):
    ctx = dash.callback_context
    pie = ctx.triggered[0]['prop_id'].split('.')[0]

    DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
        "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
    con = sqlite3.connect(str(DB_FILE))
    statement2 = f"SELECT * FROM temporary_table_2;"
    df2 = pd.read_sql_query(statement2, con)


    df22 = df2[['Date', 'Profit']]
    pd.to_datetime(df22.Date)
    df22['Year'] = df22['Date'].apply(lambda x: x.split("-")[0])
    df22['Month'] = df22['Date'].apply(lambda x: x.split("-")[1])
    df22_m_y = df22.groupby(['Month', 'Year']).sum()
    ###### Aylik grafik ######
    piv = pd.pivot_table(df22_m_y, values='Profit', index='Month',
                         columns='Year', aggfunc=np.sum, fill_value='--')
    flattened = pd.DataFrame(piv.to_records())
    flattened = flattened.drop(['Month'], axis=1)
    df22_m_y_ = pd.DataFrame()
    df22_m_y_['Month'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                          'October', 'November', 'December']
    flattened = pd.concat([df22_m_y_, flattened], axis=1)
    ###### Yillik grafik #####
    df22_y = df22.groupby(['Year']).sum()

    if (n_clicks3 == 0):

        return dcc.Graph(
                        id='graph',
                        figure={
                            'data': [
                                {'x': df2.Date, 'y': df2['Profit'], 'type': 'bar', 'name': ''}
                            ],
                            'layout': {
                                'title': 'Daily return',
                                'height': 390
                            }
                        })

    else:

        if pie == 'return-3':
            return dcc.Graph(
                        id='graph',
                        figure={
                            'data': [
                                {'x': df2.Date, 'y': df2['Profit'], 'type': 'bar', 'name': ''}
                            ],
                            'layout': {
                                'title': 'Daily return',
                                'height': 390
                            }
                        })


@app.callback(
    Output(component_id='stock_chart36', component_property='children'),
    [Input(component_id='return-4', component_property='n_clicks')]
)
def show_graphs5(n_clicks4):
    ctx = dash.callback_context
    pie = ctx.triggered[0]['prop_id'].split('.')[0]

    DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
        "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
    con = sqlite3.connect(str(DB_FILE))
    statement2 = f"SELECT * FROM temporary_table_2;"
    df2 = pd.read_sql_query(statement2, con)


    df22 = df2[['Date', 'Profit']]
    pd.to_datetime(df22.Date)
    df22['Year'] = df22['Date'].apply(lambda x: x.split("-")[0])
    df22['Month'] = df22['Date'].apply(lambda x: x.split("-")[1])
    df22_m_y = df22.groupby(['Month', 'Year']).sum()
    ###### Aylik grafik ######
    piv = pd.pivot_table(df22_m_y, values='Profit', index='Month',
                         columns='Year', aggfunc=np.sum, fill_value='--')
    flattened = pd.DataFrame(piv.to_records())
    flattened = flattened.drop(['Month'], axis=1)
    df22_m_y_ = pd.DataFrame()
    df22_m_y_['Month'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                          'October', 'November', 'December']
    flattened = pd.concat([df22_m_y_, flattened], axis=1)
    ###### Yillik grafik #####
    df22_y = df22.groupby(['Year']).sum()

    if (n_clicks4 == 0):

        return dcc.Graph(
                        id='graph',
                        figure={
                            'data': [
                                {'x': df22_y.index, 'y': df22_y['Profit'], 'type': 'bar', 'name': ''}
                            ],
                            'layout': {
                                'title': 'Annual Return',
                                'height': 390
                            }
                        })

    else:

        if pie == 'return-4':
            return dcc.Graph(
                        id='graph',
                        figure={
                            'data': [
                                {'x': df22_y.index, 'y': df22_y['Profit'], 'type': 'bar', 'name': ''}
                            ],
                            'layout': {
                                'title': 'Annual Return',
                                'height': 390
                            }
                        })


# if __name__ == '__main__':
#     app.run_server(debug=True)
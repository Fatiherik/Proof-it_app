import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Output, Input, State
from datetime import datetime
import pathlib
import sqlite3
from apps.backtest import df3, df4

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__,
#               external_stylesheets=external_stylesheets)

from app import app

DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath("/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
con = sqlite3.connect(str(DB_FILE))
statement = f"SELECT * FROM my_works;"
df = pd.read_sql_query(statement, con)

layout = html.Div([
            dash_table.DataTable(
                id='all-result-table',
                data=df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df.columns],
                style_cell={'textAlign': 'center','width':'100px','minWidth': '100px', 'maxWidth': '100px'},
                fixed_rows={'headers': True, 'data': 0},
                style_header={'fontWeight': 'bold'},
                row_selectable='multi',
                selected_rows=[]
            ),
            html.Div([
                html.A(html.Button('Delete', id='delete-button', n_clicks=0, style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'}),href='/my_works'),
                html.Button('Send to Backtest', id='send-backtest-button2', n_clicks=0, style={'backgroundColor': 'rgba(255, 0, 0, 0.8)', 'color': 'white'})
            ], className='buttons-my-works'),

            html.Div(id='hidden-div6', style={'display': 'none'}),
        ])


@app.callback(
            Output(component_id='all-result-table', component_property='data'),
            [Input(component_id='delete-button', component_property='n_clicks'),
            Input(component_id='send-backtest-button2',component_property='n_clicks')],
            [State(component_id='all-result-table', component_property='selected_row_ids')]
            )

def delete_row_and_show_all_results (n_clicks1, n_clicks2, selected_row_ids):

    ctx = dash.callback_context

    DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
        "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
    con = sqlite3.connect(str(DB_FILE))
    statement = f"SELECT * FROM my_works;"
    df = pd.read_sql_query(statement, con)
    data = df.to_dict('records')

    if (n_clicks1 == 0) & (n_clicks2 == 0):

        return data

    else:

        pie = ctx.triggered[0]['prop_id'].split('.')[0]

        if pie == 'delete-button':

            if not selected_row_ids is None:

                DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
                    "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
                con = sqlite3.connect(str(DB_FILE))
                cur = con.cursor()
                for i in selected_row_ids:
                    cur.execute("DELETE FROM my_works WHERE id=?", (i,))
                    con.commit()

                statement = f"SELECT * FROM my_works;"
                df = pd.read_sql_query(statement, con)
                data = df.to_dict('records')

                return data

        elif pie == 'send-backtest-button2':

            if not selected_row_ids is None:

                DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(
                    "/Users/hackyourfuture/PycharmProjects/dash-project/database/stock_data.db").resolve()
                con = sqlite3.connect(str(DB_FILE))
                cur = con.cursor()
                for i in selected_row_ids:
                    cur.execute("SELECT * FROM my_works WHERE id=?", (i,))

                    data1 = cur.fetchall()
                    columns = ['id','Instrument', 'Strategy', 'Start', 'End', 'Total Profit','Net Profit','Inc. Profit',
                               'Dec. Profit','# trans.','Avr.Pro(trans)','# days in pos.','Avr.Pro(day)','Sharpe','Std. dev.',
                               'Stra. Type', 'Commis. Rate', '1.Profit Dec.', '1.Stop Dec.', '1.Profit Inc.', '1.Stop Inc.',
                               'Save date', 'Save time', 'Status']
                    df = pd.DataFrame(data=data1, columns=columns)
                    df.to_sql('temporary_table', con, if_exists='append', index=False)

                    return data


# if __name__ == '__main__':
#     app.run_server(debug=True)
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from app import server
from app import app
from apps import home, trader, backtest, simulation, optimization, analysis, portfolio, prediction, my_works, more, calculation, login, signup

# VALID_USERNAME_PASSWORD_PAIRS = {
#     'hello': 'world'
# }
#
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

app.layout = html.Div([
                dcc.Location(id='url', refresh=False),
                html.Div([
                    html.Div([
                        #html.Img(src='/assets/icons8-p-64.png'),
                        html.A(html.H1('Proof-it'), href='/home')
                    ]),
                    html.Div([
                        html.Ul([
                            html.Li(html.A('Sign Up', href='/signup',className='catA'),className='cat'),
                            html.Li(html.A('Log In', href='/login',className='catA'),className='cat'),
                        ], className='categories')
                    ])
                ], className='banner'),
                html.Ul([
                    html.Li(html.A('Trader', href='/trader', className='catA-2'), className='cat'),
                    html.Li(html.A('Backtest', href='/backtest', className='catA-2'), className='cat'),
                    html.Li(html.A('Simulation', href='/simulation', className='catA-2'), className='cat'),
                    html.Li(html.A('Optimization', href='/optimization', className='catA-2'), className='cat'),
                    html.Li(html.A('Analysis', href='/analysis', className='catA-2'), className='cat'),
                    html.Li(html.A('Portfolio', href='/portfolio', className='catA-2'), className='cat'),
                    html.Li(html.A('Prediction', href='/prediction', className='catA-2'), className='cat'),
                    html.Li(html.A('My Works', href='/my_works', className='catA-2'), className='cat'),
                    html.Li(html.A('More', href='/more', className='catA-2'), className='cat'),
                ],id="main-app", className='categories-2', style={'display': 'none'}),

                html.Div(id='page-content')
            ])

@app.callback (
              [Output('page-content', 'children'),
              Output('main-app', 'style')],
              [Input('url', 'pathname')]
              )

def display_page(pathname):

    style1 = {'display': 'none'}
    style2 = {'display': 'flex'}

    if pathname == '/login':
        return login.layout, style1
    elif pathname == '/signup':
        return signup.layout, style1
    elif pathname == '/trader':
        return trader.layout, style2
    elif pathname == '/backtest':
        return backtest.layout, style2
    elif pathname == '/simulation':
        return simulation.layout, style2
    elif pathname == '/optimization':
        return optimization.layout, style2
    elif pathname == '/analysis':
        return analysis.layout, style2
    elif pathname == '/portfolio':
        return portfolio.layout, style2
    elif pathname == '/prediction':
        return prediction.layout, style2
    elif pathname == '/my_works':
        return my_works.layout, style2
    elif pathname == '/more':
        return more.layout, style2
    else:
        return home.layout, style1


if __name__ == '__main__':
    app.run_server(debug=True)
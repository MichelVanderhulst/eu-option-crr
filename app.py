# Dash app libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import base64

# Importing app header, body and graphs from the other .py scripts
from appBody import body, graphs
from appHeader import header

# Rep strat math script
from EU_Option_CRR_GRW import *
from inputDescriptions import list_input


# Allowing excel export
import os
import pandas as pd
import io
from dash_extensions import Download
from dash_extensions.snippets import send_bytes


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], #modern-looking buttons, sliders, etc
	                      external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML', "./assets/mathjax.js"], #LaTeX in app
	                      meta_tags=[{"content": "width=device-width"}] #app width adapts itself to user device
	                      )
server = app.server


# Building the app from imports
app.layout = html.Div(
                id='main_page',
                children=[
                    dcc.Store(id='memory-output'),
                    header(),
                    body(),
                    graphs(),
                         ],
                     )

# App interactivity: calling the replication strategy function everytime the user changes an input
@app.callback(
  Output('memory-output', 'data'),
  [Input('CallOrPut', 'value'),
     Input("S","value"),
     Input("K", "value"),
     Input("Rf", "value"),
     Input("T","value"),
     Input("mu","value"),
     Input("vol", "value"),
     Input("tree_periods", "value")])
def get_rep_strat_data(CallOrPut, S, K, Rf,T,mu,vol,tree_periods):
  nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods = RepStrat_EU_Option_CRR_GRW(CallOrPut, S, K, Rf, T, mu, vol, tree_periods)
                                
  return nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods

# Plot of stock simulation
@app.callback(
    Output('stock_simul', 'figure'),
    [Input('memory-output', 'data'),
     Input("GraphType","value")])
def graph_stock_simul(data, value):
  nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods = data
  
  if value == "tree": 
    return{'layout': go.Layout(title={'yref':"paper",
                                      'y':1,
                                      "yanchor":"bottom"},
                              #margin={"t":15},
                              margin=dict(
                                      l=0,
                                      #r=50,
                                      #b=100,
                                      t=15,
                                      #pad=4
                                  ),
                              # showlegend=False,
                              xaxis={'showgrid': False, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': False,},  # numbers below}
                              yaxis={'showgrid': False, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': False,},  # numbers below}
                              legend=dict(
                                  x=0,
                                  y=1,
                                  traceorder='normal',
                                  bgcolor='rgba(0,0,0,0)'),
                                ),
          'data': [go.Scatter(x=edge_x,
                              y=edge_y,
                              mode='lines',
                              line=dict(width=0.5),
                              hoverinfo='none',
                              showlegend=False,
                              ),
                   go.Scatter(
                            x=node_x,
                            y=node_y,
                            mode='markers+text',
                            marker=dict(size=40),
                            text=[round(num, 2) for num in stocksLabel],
                            showlegend=False,
                            hoverinfo='none',
                            ),
                   go.Scatter(
                            x=[None],
                            y=[None],
                            mode='markers',
                            name=f'Up factor: {u}'
                            ),
                   go.Scatter(
                            x=[None],
                            y=[None],
                            mode='markers',
                            name=f'Down factor: {d}'
                            ),
                    go.Scatter(
                            x=[None],
                            y=[None],
                            mode='markers',
                            name=f'Prob up: {probUp}'
                            ),
                   go.Scatter(
                            x=[None],
                            y=[None],
                            mode='markers',
                            name=f'Prob down: {probDown}'
                            ),
                  ],
        }
  else:
    return{'layout': go.Layout(title={'yref':"paper", 
                                  'y':1, 
                                  "yanchor":"bottom"},
                               margin=dict(l=0, t=15),
                              xaxis={'showgrid': True, 
                                     'zeroline': False, 
                                     'visible': True,
                                     "title":"Periods"}, 
                              yaxis={'showgrid': True, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': True,
                                     "autorange":True,
                                     "ticks":"outside",
                                     "title":"USD"},  # numbers below}
                               legend=dict(x=0,
                                           y=1,
                                          traceorder='normal', 
                                          bgcolor='rgba(0,0,0,0)'
                                          ),
                               hovermode="closest",
                              ),
          'data': [go.Scatter(x=edge_x,
                              y=edge_y_Stock, 
                              mode='lines',
                              line=dict(width=0.5),
                              hoverinfo='none',
                              showlegend=False,
                             ),
                   go.Scatter(x=node_x,
                              y=node_y_Stock,
                              mode='markers+text',
                              marker=dict(size=40),
                              text=[round(num, 2) for num in stocksLabel],
                              showlegend=False,
                              hoverinfo="none",
                             ),
              go.Scatter( 
                x=[None],
                y=[None],
                mode='markers',
                name=f'Up factor: {u}'
                ),
            go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                name=f'Down factor: {d}'
                ),
            go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                name=f'Prob up: {probUp}'
                ),
            go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                name=f'Prob down: {probDown}'
                ),
          ],
    }


# Plot of rep strat portfolio
@app.callback(
    Output('port_details', 'figure'),
    [Input('memory-output', 'data'),
     Input("GraphType","value")])
def graph_portfolio(data, value):
  nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods = data
  
  if value == "tree": 
    return{'layout': go.Layout(title={'yref':"paper",
                                      'y':1,
                                      "yanchor":"bottom"},
                              showlegend=False,
                              margin=dict(
                                      l=0,
                                      #r=50,
                                      #b=100,
                                      t=15,
                                      #pad=4
                                  ),
                              xaxis={'showgrid': False, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': False,
                                     "title":"Periods"},  # numbers below}
                              yaxis={'showgrid': False, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': False,
                                     "title":"USD"},  # numbers below}}  # numbers below}
                              ),
           'data': [go.Scatter(x=edge_x,
                               y=edge_y,
                               mode='lines',
                               line=dict(width=0.5),
                               hoverinfo='none',
                               ),
                    go.Scatter(x=node_x,
                               y=node_y,
                               mode='markers+text',
                               marker=dict(size=40),
                               text=[round(num, 2) for num in portfolioLabel],
                               hoverinfo='none',
                               ),
                    ],
          }
  else:
    return{'layout': go.Layout(title={'yref':"paper", 
                                      'y':1, 
                                      "yanchor":"bottom"},
                               margin=dict(l=0, t=15),
                               xaxis={'showgrid': True, 
                                     'zeroline': False, 
                                     'visible': True,
                                     "title":"Periods"}, 
                               yaxis={'showgrid': True, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': True,
                                     "autorange":True,
                                     "ticks":"outside",
                                     "title":"USD"},  # numbers below}
                               legend=dict(x=0,
                                           y=1,
                                          traceorder='normal', 
                                          bgcolor='rgba(0,0,0,0)'
                                          ),
                               hovermode="closest",
                              ),
          'data': [go.Scatter(x=edge_x,
                              y=edge_y_Portfolio, 
                              mode='lines',
                              line=dict(width=0.5),
                              hoverinfo='none',
                              showlegend=False,
                             ),
                   go.Scatter(x=node_x,
                              y=node_y_Portfolio,
                              mode='markers+text',
                              marker=dict(size=40),
                              text=[round(num, 2) for num in portfolioLabel],
                              showlegend=False,
                              hoverinfo="none",
                             ),
          ],
    }

# Plot of number of shares to hold
@app.callback(
    Output('nbr_shares', 'figure'),
    [Input('memory-output', 'data'),
     Input("GraphType","value")])
def graph_numberShares(data, value):
  nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods = data
  
  if value == "tree": 
    return{'layout': go.Layout(title={'yref':"paper",
                                      'y':1,
                                      "yanchor":"bottom"},
                              showlegend=False,
                              margin=dict(l=0,
                                          #r=50,
                                          #b=100,
                                          t=15,
                                          #pad=4
                                          ),
                              xaxis={'showgrid': False, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': False,
                                     "title":"Periods"},  # numbers below}
                              yaxis={'showgrid': False, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': False,
                                     "title":"Periods"}  # numbers below}
                             ),
            'data': [go.Scatter(x=edge_x,
                                y=edge_y,
                                mode='lines',
                                line=dict(width=0.5),
                                hoverinfo='none',
                               ),
                     go.Scatter(x=node_x,
                                y=node_y,
                                mode='markers+text',
                                marker=dict(size=40),
                                text=[round(num, 2) for num in nbrofsharesLabel],
                                hoverinfo='none',
                                ),
                      ],
        }
  else:
    return{'layout': go.Layout(title={'yref':"paper", 
                                      'y':1, 
                                      "yanchor":"bottom"},
                               margin=dict(l=0, t=15),
                               xaxis={'showgrid': True, 
                                     'zeroline': False, 
                                     'visible': True,
                                     "title":"Periods"}, 
                               yaxis={'showgrid': True, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': True,
                                     "autorange":True,
                                     "ticks":"outside",
                                     "title":"# Shares"},  # numbers below}
                               legend=dict(x=0,
                                           y=1,
                                          traceorder='normal', 
                                          bgcolor='rgba(0,0,0,0)'
                                          ),
                               hovermode="closest",
                              ),
          'data': [go.Scatter(x=edge_x,
                              y=edge_y_NbrOfShares, 
                              mode='lines',
                              line=dict(width=0.5),
                              hoverinfo='none',
                              showlegend=False,
                             ),
                   go.Scatter(x=node_x,
                              y=node_y_NbrOfShares,
                              mode='markers+text',
                              marker=dict(size=40),
                              text=[round(num, 2) for num in nbrofsharesLabel],
                              showlegend=False,
                              hoverinfo="none",
                             ),
          ],
    }


# Plot of cash account
@app.callback(
    Output('cash_acc', 'figure'),
    [Input('memory-output', 'data'),
     Input("GraphType","value")])
def graph_cashAccount(data, value):
  nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods = data
  
  if value == "tree":
    return{'layout': go.Layout(title={'yref':"paper",
                                      'y':1,
                                      "yanchor":"bottom"},
                              showlegend=False,
                              margin=dict(l=0,
                                          #r=50,
                                          #b=100,
                                          t=15,
                                          #pad=4
                                         ),
                              xaxis={'showgrid': False, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': False,
                                     "title":"Periods"},  # numbers below}
                              yaxis={'showgrid': False, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': False,
                                     "title":"USD"}  # numbers below}
                              ),
            'data': [go.Scatter(x=edge_x,
                                y=edge_y,
                                mode='lines',
                                line=dict(width=0.5),
                                hoverinfo='none',
                                ),
                     go.Scatter(x=node_x,
                                y=node_y,
                                mode='markers+text',
                                marker=dict(size=40),
                                text=[round(num, 2) for num in cashLabel],
                                hoverinfo='none',
                                ),
                    ],
        }
  else:
    return{'layout': go.Layout(title={'yref':"paper", 
                                      'y':1, 
                                      "yanchor":"bottom"},
                               margin=dict(l=0, t=15),
                               xaxis={'showgrid': True, 
                                     'zeroline': False, 
                                     'visible': True,
                                     "title":"Periods"}, 
                               yaxis={'showgrid': True, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': True,
                                     "autorange":True,
                                     "ticks":"outside",
                                     "title":"USD"},  # numbers below}
                               legend=dict(x=0,
                                           y=1,
                                          traceorder='normal', 
                                          bgcolor='rgba(0,0,0,0)'
                                          ),
                               hovermode="closest",
                              ),
          'data': [go.Scatter(x=edge_x,
                              y=edge_y_Cash, 
                              mode='lines',
                              line=dict(width=0.5),
                              hoverinfo='none',
                              showlegend=False,
                             ),
                   go.Scatter(x=node_x,
                              y=node_y_Cash,
                              mode='markers+text',
                              marker=dict(size=40),
                              text=[round(num, 2) for num in cashLabel],
                              showlegend=False,
                              hoverinfo="none",
                             ),
          ],
    }


# Plot of option price
@app.callback(
    Output('option_price', 'figure'),
    [Input('memory-output', 'data'),
     Input("GraphType", "value")])
def graph_option_pricee(data, value):
  nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods = data
  
  if value == "tree":
    return{'layout': go.Layout(title={'yref':"paper",
                                        'y':1,
                                        "yanchor":"bottom"},
                                  showlegend=False,
                                  margin=dict(l=0,
                                              #r=50,
                                              #b=100,
                                              t=15,
                                              #pad=4
                                              ),
                                  xaxis={'showgrid': False, # thin lines in the background
                                         'zeroline': False, # thick line at x=0
                                         'visible': False,
                                         "title":"Periods"},  # numbers below}
                                  yaxis={'showgrid': False, # thin lines in the background
                                         'zeroline': False, # thick line at x=0
                                         'visible': False,
                                         "title":"USD"}  # numbers below}
                                  ),
               'data': [go.Scatter(x=edge_x,
                                   y=edge_y,
                                   mode='lines',
                                   line=dict(width=0.5),
                                   hoverinfo='none',
                                   ),
                        go.Scatter(x=node_x,
                                   y=node_y,
                                   mode='markers+text',
                                   marker=dict(size=40),
                                   text=[round(num, 2) for num in optionpriceLabel],
                                   hoverinfo='none',
                                  ),
                       ],
            }
  else:
    return{'layout': go.Layout(title={'yref':"paper", 
                                      'y':1, 
                                      "yanchor":"bottom"},
                               margin=dict(l=0, t=15),
                               xaxis={'showgrid': True, 
                                     'zeroline': False, 
                                     'visible': True,
                                     "title":"Periods"}, 
                               yaxis={'showgrid': True, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': True,
                                     "autorange":True,
                                     "ticks":"outside",
                                     "title":"USD"},  # numbers below}
                               legend=dict(x=0,
                                           y=1,
                                          traceorder='normal', 
                                          bgcolor='rgba(0,0,0,0)'
                                          ),
                               hovermode="closest",
                              ),
          'data': [go.Scatter(x=edge_x,
                              y=edge_y_Portfolio, 
                              mode='lines',
                              line=dict(width=0.5),
                              hoverinfo='none',
                              showlegend=False,
                             ),
                   go.Scatter(x=node_x,
                              y=node_y_Optionprice,
                              mode='markers+text',
                              marker=dict(size=40),
                              text=[round(num, 2) for num in optionpriceLabel],
                              showlegend=False,
                              hoverinfo="none",
                             ),
          ],
    }



# Plot of option intrinsic value
@app.callback(
    Output('option_intrinsic', 'figure'),
    [Input('memory-output', 'data'),
     Input("GraphType", "value")])
def graph_optionIntrinsicValue(data,value):
  nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods = data
    
  if value == "tree":
    return{'layout': go.Layout(title={'yref':"paper",
                                        'y':1,
                                        "yanchor":"bottom"},
                                  showlegend=False,
                                  margin=dict(l=0,
                                              #r=50,
                                              #b=100,
                                              t=15,
                                              #pad=4
                                              ),
                                  xaxis={'showgrid': False, # thin lines in the background
                                         'zeroline': False, # thick line at x=0
                                         'visible': False,
                                         "title":"Periods"},  # numbers below}
                                  yaxis={'showgrid': False, # thin lines in the background
                                         'zeroline': False, # thick line at x=0
                                         'visible': False,
                                         "title":"USD"}  # numbers below}
                                  ),
            'data': [go.Scatter(x=edge_x,
                                y=edge_y, 
                                mode='lines',
                                line=dict(width=0.5),
                                hoverinfo='none',
                                showlegend=False,
                               ),
                     go.Scatter(x=node_x,
                                y=node_y,
                                mode='markers+text',
                                marker=dict(size=40),
                                text=[round(num, 2) for num in intrinsicLabel],
                                showlegend=False,
                                hoverinfo="none",
                               ),
            ],
      }

  else:
    return{'layout': go.Layout(title={'yref':"paper", 
                                      'y':1, 
                                      "yanchor":"bottom"},
                               margin=dict(l=0, t=15),
                               xaxis={'showgrid': True, 
                                     'zeroline': False, 
                                     'visible': True,
                                     "title":"Periods"}, 
                               yaxis={'showgrid': True, # thin lines in the background
                                     'zeroline': False, # thick line at x=0
                                     'visible': True,
                                     "autorange":True,
                                     "ticks":"outside",
                                     "title":"USD"},  # numbers below}
                               legend=dict(x=0,
                                           y=1,
                                          traceorder='normal', 
                                          bgcolor='rgba(0,0,0,0)'
                                          ),
                               hovermode="closest",
                              ),
          'data': [go.Scatter(x=edge_x,
                              y=edge_y_Intrinsic, 
                              mode='lines',
                              line=dict(width=0.5),
                              hoverinfo='none',
                              showlegend=False,
                             ),
                   go.Scatter(x=node_x,
                              y=node_y_Intrinsic,
                              mode='markers+text',
                              marker=dict(size=40),
                              text=[round(num, 2) for num in intrinsicLabel],
                              showlegend=False,
                              hoverinfo="none",
                             ),
          ],
    }

# User input checks
@app.callback(Output('message_S', 'children'),
              [Input('S', 'value')])
def check_input_S(S):
    if S<0:
        return f'Cannot be lower than 0.'
    else:
        return ""

@app.callback(Output('message_K', 'children'),
              [Input('K', 'value')])
def check_input_K(K):
    if K<0:
        return f'Cannot be lower than 0.'
    else:
        return ""

@app.callback(Output('message_tree', 'children'),
              [Input('tree_periods', 'value')])
def check_input_K(tree__periods):
    if tree__periods<1:
        return f'Cannot be lower than 1.'
    else:
        return ""

# Input visuals
@app.callback(Output('drift', 'children'),
              [Input('mu', 'value')])
def display_value(value):
    return f': {int(value*100)}%'

@app.callback(Output('sigma', 'children'),
              [Input('vol', 'value')])
def display_value2(value):
    return f': {int(value*100)}%'

@app.callback(Output('riskfree', 'children'),
              [Input('Rf', 'value')])
def display_value3(value):
    return f': {int(value*100)}%'

@app.callback(Output('matu', 'children'),
              [Input('T', 'value')])
def display_value4(value):
    if value==0.25 or value==0.5 or value==0.75:
        return f": {int(value*12)} months"
    elif value == 1:
        return f': {value} year'
    else:
        return f': {value} years'


# Excel export
@app.callback(Output("download", "data"), 
             [Input("btn", "n_clicks")],
             [State('memory-output', 'data')])
def generate_xlsx(n_clicks, data):
    nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods = data
    nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel = np.array(nbrofsharesLabel), np.array(cashLabel), np.array(portfolioLabel), np.array(optionpriceLabel), np.array(intrinsicLabel), np.array(stocksLabel)

    list_of_outputs = (stocksLabel, intrinsicLabel, portfolioLabel, optionpriceLabel, nbrofsharesLabel, cashLabel)
    list_of_names = ["Stock simulation", "Option intrinsic value", "Portfolio", "Option price", "Number of shares", "Cash account"]

    endbis, startbis = [0], [0]
    endstep, startstep = np.arange(2,tree__periods+2), np.arange(1,tree__periods+1)

    for i in range(len(endstep)):
      endbis.append(endbis[i]+endstep[i])

    for i in range(len(startstep)):
      startbis.append(startbis[i]+startstep[i])

    def to_xlsx(bytes_io):
        counter = 0
        xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")
        for output in list_of_outputs:
          temp = pd.DataFrame(index=np.arange(0,tree__periods+1))
          temp.loc[:,0] = pd.Series(output[0])
          for j in range(1, tree__periods+1):
            temp.loc[:, j] = pd.Series(output[startbis[j]:endbis[j]+1])
          temp.index = np.arange(1, tree__periods+2)
          temp.to_excel(xslx_writer, sheet_name=f"{list_of_names[counter]}")
          counter += 1

        xslx_writer.save()

    return send_bytes(to_xlsx, "rawdata.xlsx")



# Opening/Closing top-right About button
@app.callback(
    Output("popover", "is_open"),
    [Input("popover-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


# Main function, runs the app
if __name__ == '__main__':
    app.run_server(debug=True)

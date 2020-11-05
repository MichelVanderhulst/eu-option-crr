import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from EU_Option_CRR_GRW_V5 import *
from descriptions import list_input
import base64

from layout_body_graphs import body, graphs
from header import header
import os
import pandas as pd
import io
from dash_extensions import Download
from dash_extensions.snippets import send_bytes


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML', "./assets/mathjax.js"])
server = app.server



app.layout = html.Div(
                id='main_page',
                children=[
                    dcc.Store(id='memory-output'),
                    header(),
                    body(),
                    graphs(),
                         ],
                     )




@app.callback(
  Output('memory-output', 'data'),
  [Input('CallOrPut', 'value'),
     Input("S","value"),
     Input("K", "value"),
     Input("Rf", "value"),
     Input("T","value"),
     Input("mu","value"),
     Input("vol", "value"),
     Input("tree_periods", "value"),])
def get_rep_strat_data(CallOrPut, S, K, Rf,T,mu,vol,tree_periods):
  nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods = RepStrat_EU_Option_CRR_GRW_V5(CallOrPut, S, K, Rf, T, mu, vol, tree_periods)
                                
  return nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods

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



@app.callback(
    Output('port_details', 'figure'),
    [Input('memory-output', 'data'),
     Input("GraphType","value")])
def graph_stock_simul(data, value):
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


@app.callback(
    Output('nbr_shares', 'figure'),
    [Input('memory-output', 'data'),
     Input("GraphType","value")])
def graph_stock_simul(data, value):
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



@app.callback(
    Output('cash_acc', 'figure'),
    [Input('memory-output', 'data'),
     Input("GraphType","value")])
def graph_stock_simul(data, value):
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




@app.callback(
    Output('option_intrinsic', 'figure'),
    [Input('memory-output', 'data'),
     Input("GraphType", "value")])
def graph_option_pricee(data,value):
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



## WORKS LOCALLY, NOT ONLINE

# @app.callback(Output('download-link', 'href'), 
#              [Input('memory-output', 'data')])
# def update_download_link(data):
#     nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods = data
#     nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel = np.array(nbrofsharesLabel), np.array(cashLabel), np.array(portfolioLabel), np.array(optionpriceLabel), np.array(intrinsicLabel), np.array(stocksLabel)

#     list_of_outputs = (stocksLabel, intrinsicLabel, portfolioLabel, optionpriceLabel, nbrofsharesLabel, cashLabel)
#     list_of_names = ["Stock simulation", "Option intrinsic value", "Portfolio", "Option price", "Number of shares", "Cash account"]
#     counter = 0

#     endbis, startbis = [0], [0]
#     endstep, startstep = np.arange(2,tree__periods+2), np.arange(1,tree__periods+1)

#     for i in range(len(endstep)):
#       endbis.append(endbis[i]+endstep[i])

#     for i in range(len(startstep)):
#       startbis.append(startbis[i]+startstep[i])

#     strIO = io.BytesIO()
#     excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")

#     for output in list_of_outputs:
#       temp = pd.DataFrame(index=np.arange(0,tree__periods+1))
#       temp.loc[:,0] = pd.Series(output[0])
#       for j in range(1, tree__periods+1):
#         temp.loc[:, j] = pd.Series(output[startbis[j]:endbis[j]+1])

#       temp.index = np.arange(1, tree__periods+2)
#       temp.to_excel(excel_writer, sheet_name=f"{list_of_names[counter]}")
#       counter += 1

#     excel_writer.save()
#     strIO.seek(0)

#     # https://en.wikipedia.org/wiki/Data_URI_scheme
#     media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#     data = base64.b64encode(strIO.read()).decode("utf-8")
#     href_data_downloadable = f'data:{media_type};base64,{data}'
#     return href_data_downloadable 


## WORKS LOCALLY, NOT ONLINE

# @app.callback(Output('download-link', 'href'), 
#              [Input('memory-output', 'data')])
# def update_href(data):
#     nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods = data
#     nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel = np.array(nbrofsharesLabel), np.array(cashLabel), np.array(portfolioLabel), np.array(optionpriceLabel), np.array(intrinsicLabel), np.array(stocksLabel)

#     list_of_outputs = (stocksLabel, intrinsicLabel, portfolioLabel, optionpriceLabel, nbrofsharesLabel, cashLabel)
#     list_of_names = ["Stock simulation", "Option intrinsic value", "Portfolio", "Option price", "Number of shares", "Cash account"]
#     counter = 0

#     endbis, startbis = [0], [0]
#     endstep, startstep = np.arange(2,tree__periods+2), np.arange(1,tree__periods+1)

#     for i in range(len(endstep)):
#       endbis.append(endbis[i]+endstep[i])

#     for i in range(len(startstep)):
#       startbis.append(startbis[i]+startstep[i])

#     relative_filename = os.path.join('downloads','{}-download.xlsx'.format("data"))
#     absolute_filename = os.path.join(os.getcwd(), relative_filename)

#     writer = pd.ExcelWriter(absolute_filename)

#     for output in list_of_outputs:
#       temp = pd.DataFrame(index=np.arange(0,tree__periods+1))
#       temp.loc[:,0] = pd.Series(output[0])
#       for j in range(1, tree__periods+1):
#         temp.loc[:, j] = pd.Series(output[startbis[j]:endbis[j]+1])

#       temp.index = np.arange(1, tree__periods+2)
#       temp.to_excel(writer, sheet_name=f"{list_of_names[counter]}")
#       counter += 1

#     writer.save()
#     return f'/{relative_filename}'


# @app.server.route('/downloads/<path:path>')
# def serve_static(path):
#     root_dir = os.getcwd()
#     return flask.send_from_directory(os.path.join(root_dir, 'downloads'), path)






# @app.callback(Output('download-link', 'href'), 
#              [Input('memory-output', 'data')])
# def update_download_link(data):
#     nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown, edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods = data
#     nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel = np.array(nbrofsharesLabel), np.array(cashLabel), np.array(portfolioLabel), np.array(optionpriceLabel), np.array(intrinsicLabel), np.array(stocksLabel)

#     list_of_outputs = (stocksLabel, intrinsicLabel, portfolioLabel, optionpriceLabel, nbrofsharesLabel, cashLabel)
#     list_of_names = ["Stock simulation", "Option intrinsic value", "Portfolio", "Option price", "Number of shares", "Cash account"]
#     counter = 0

#     endbis, startbis = [0], [0]
#     endstep, startstep = np.arange(2,tree__periods+2), np.arange(1,tree__periods+1)

#     for i in range(len(endstep)):
#       endbis.append(endbis[i]+endstep[i])

#     for i in range(len(startstep)):
#       startbis.append(startbis[i]+startstep[i])

#     strIO = io.BytesIO()
#     excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")
#     df = pdf.DataFrame({"test":[0],"test2":[5]})

#     # for output in list_of_outputs:
#     #   temp = pd.DataFrame(index=np.arange(0,tree__periods+1))
#     #   temp.loc[:,0] = pd.Series(output[0])
#     #   for j in range(1, tree__periods+1):
#     #     temp.loc[:, j] = pd.Series(output[startbis[j]:endbis[j]+1])

#     #   temp.index = np.arange(1, tree__periods+2)
#     #   temp.to_excel(excel_writer, startrow=(tree__periods+4)*counter)
#     #   counter += 1
    
#     excel_writer.save()
#     strIO.seek(0)
#     # https://en.wikipedia.org/wiki/Data_URI_scheme
#     media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#     media_type = 'application/vnd.ms-excel'
#     data = base64.b64encode(strIO.read()).decode("utf-8")
#     href_data_downloadable = f'data:{media_type};base64,{data}'
#     return href_data_downloadable 



@app.callback(Output("download", "data"), 
             [Input("btn", "n_clicks"),
             Input('memory-output', 'data')])
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

        #df.to_excel(xslx_writer, index=False, sheet_name="sheet1")
        xslx_writer.save()

    return send_bytes(to_xlsx, "rawdata.xlsx")































@app.callback(
    Output("popover", "is_open"),
    [Input("popover-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output, State
# import dash_bootstrap_components as dbc
# import plotly.graph_objs as go
# from EU_Option_CRR_GRW_V5 import *
# from descriptions import list_input
# import base64


# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML', "./assets/mathjax.js"])
# server = app.server

# bg_color="#506784",
# font_color="#F3F6FA"


# top_markdown_text = '''
# ### Call/Put Replication Strategy Tool - CRR model
# #### Michel Vanderhulst 
# #### Master's thesis - Louvain School of Management
# '''

# email = "michelvanderhulst@student.uclouvain.be"

# graph_stock_simul = ''' #### Stock simulation (GRW) '''
# graph_port_details_text = ''' #### Portfolio before/after rebalancing'''
# graph_nbr_shares = ''' #### Shares held before/after rebalancing'''
# graph_cash = ''' #### Cash account before/after rebalancing'''
# graph_option_price = ''' #### Option price'''
# graph_option_intrinsic = ''' #### Option intrinsic value'''



# def header():
#     return html.Div(
#                 id='app-page-header',
#                 children=[#html.Div(html.A(
#                       #            id='lsm-logo', 
#                       #            children=[html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open("output-onlinepngtools (1).png", 'rb').read()).decode()))],
#                       #            href="https://uclouvain.be/en/faculties/lsm",
#                       #            target="_blank", #open link in new tab
#                       #            style={'margin':'20px'}
#                       #              ), style={"display":"inline-block"}),
#                     #
#                     #
#                     # html.Div(
#                        #  html.A(
#                        #    id="nova-logo", 
#                        #    children=[html.Img(src="data:image/png;base64,{}".format(base64.b64encode(open("output-onlinepngtools (2).png",'rb').read()).decode()))],
#                        #    href="https://www2.novasbe.unl.pt/en/",
#                        #    style={"margin":"-45px"}
#                        #      ), style={"display":"inline-block"}),
#                     #
#                     #
#                     html.Div(children=[html.H3("European option replication strategy app"),
#                                        html.H4("Cox-Ross-Rubinstein model")
#                                       ],
#                              style={"display":"inline-block", "font-family":'sans-serif'}),
#                     #
#                     #
#                     html.Div(children=[dbc.Button("About", id="popover-target", outline=True, style={"color":"white", 'border': 'solid 1px white'}),
#                                        dbc.Popover(children=[dbc.PopoverHeader("About"),
#                                                              dbc.PopoverBody(["Michel Vanderhulst",                             
#                                                                               f"\n {email}", 
#                                                                               html.Hr(), 
#                                                                               "This app was built for my Master's Thesis, under the supervision of Prof. Frédéric Vrins (frederic.vrins@uclouvain.be)."]),],
#                                                    id="popover",
#                                                    is_open=False,
#                                                    target="popover-target"),
#                                        ],
#                               style={"display":"inline-block", "font-family":"sans-serif", 'marginLeft': '60%'}),
#                          ],
#                 style={
#                     'background': bg_color,
#                     'color': font_color,
#                     'padding':20,
#                     'margin':'-10px',
#                 }
#             )




# def body():
#     return html.Div(children=[
#             html.Div(id='left-column', children=[
#                 dcc.Tabs(
#                     id='tabs', value='The app',
#                     children=[
#                         dcc.Tab(
#                             label='The app',
#                             value='The app',
#                             children=html.Div(children=[
#                                 html.Br(),
#                                 html.H4('What is this app?', style={"text-align":"center"}),
#                                 html.P(
#                                     """
#                                     This app computes the replication strategy of vanilla European options on a set of given, comparing the Cox-Ross-Rubinstein model and strategy option price.
#                                     """
#                                 ),
#                                 html.P(
#                                     """
#                                     The goal is to showcase that the price is truly arbitrage-free, i.e. that both risk-neutral pricing and replicating strategy have the same values. 
#                                     """
#                                 ),
#                                 html.P(
#                                     """
#                                     Read more about options : 
#                                     https://en.wikipedia.org/wiki/Option_(finance)
                                    
#                                     """
#                                 ),
#                             ])
#                         ),
#                         dcc.Tab(
#                             label="Model",
#                             value="Model",
#                             children=[html.Div(children=[
#                                 html.Br(),
#                                 html.H4("The Cox-Ross-Rubinstein model", style={"text-align":"center"}),
#                                 html.P([
#                                     """
#                                     The Cox-Ross-Rubinstein model (CRR) is an example of a multi-period market model of the stock price.                                     
#                                     """]),
#                                 html.Hr(),
#                                 html.H4("Model assumptions", style={"text-align":"center"}),
#                                 "Its main assumptions are:",
#                                 html.Ul([html.Li("Does not consider dividends and transaction costs"), 
#                                          html.Li("The volatility and risk-free rate are assumed constant"),
#                                          html.Li("Fraction of shares can be traded"),
#                                          html.Li("The underlying asset can only either go 'up' by a fixed factor \(u<1\) or 'down' by \(0<d<1\)."),
#                                          html.Li("The log-returns are independent at all periods")]),
#                                 html.Hr(),
#                                 html.H4("Underlying asset dynamics", style={"text-align":"center"}),
#                                 html.P([
#                                     """Under CRR, the underlying asset follows a geometric random walk with 
#                                     drift \(\mu\delta\) and volatility \(\sigma\sqrt{\delta}\). The probability to go 'up' and 'down' are respectively \(p\) and \(1-p\) (under \(\mathcal{P}\)).
#                                     The stock price at period \(i\) can be modeled as a function of a binomial random variable, and the constant 'up' and 'down' factors
#                                     computed: $$u=e^{\mu\delta+\sigma\sqrt{\delta}}$$ $$d=e^{\mu\delta-\sigma\sqrt{\delta}}$$. The \(\mathcal{Q}\)-probability allowing the discounted
#                                     stock price to be a martingale amounts to the \(p\) value (under \(\mathcal{Q}\)) that leads to the martingale property: \(p=\\frac{e^{r}-d}{u-d}\).
#                                     """])
#                                 ])]),
#                         #
#                         #
#                         dcc.Tab(
#                             label="Approach",
#                             value="Methodology",
#                             children=[html.Div(children=[
#                                 html.Br(),
#                                 html.H4("Methodology followed", style={"text-align":"center"}),
#                                 html.P([
#                                     """
#                                     To prove that the risk-neutral price is arbitrage-free, let us try to perfectly replicate it with a strategy. If the strategy is successfull, then 
#                                     the price is unique and therefore arbitrage-free.
#                                     """]),
#                                 html.Hr(),
#                                 html.H4("Risk-neutral pricing", style={"text-align":"center"}),
#                                 html.P([
#                                     """
#                                     With the CRR, the stock tree and the option intrinsic value are easily computed at all nodes. Under the pricing measure, the option
#                                     price of a node is simply the discounted value of the two children nodes. The price tree is therefore filled backwards,
#                                     starting from the leaves (i.e. the payoff).
#                                     """]),
#                                 html.H4("Replicating portfolio", style={"text-align":"center"}),
#                                 html.P([
#                                     """
#                                     Then, if the price computed is truly arbitrage-free, a replication strategy can be based on this price: \(\pi_{0} = v_{0}\).
#                                      At the begining of each period, the number of shares to hold is \(\Delta_{i}^{j} = \\frac{v_{i+1}^{j}-v_{i+1}^{j+1}}{s_{i+1}^{j}-s_{i+1}^{j+1}}\). 
#                                      The initial amount of cash will be \(c_{0} = \pi_{0} - \Delta_{0}s_{0}\). At each node, a portfolio rebalancing is needed. Before the rebalancing, 
#                                      \(\Delta\) is the same from node to node \(\Delta_{i}^{j}=\Delta_{i-1}^{j}\), the cash account grew at the risk-free rate \(c_{i}^{j}=c_{i-1}^{j}e^{r}\), 
#                                      and the portfolio is the sum of both equity and cash positions \(\pi_{i}^{j}=c_{i}^{j}+\Delta_{i}^{j}s_{i}^{j}\). The rebalancing is done by updating the shares 
#                                      to hold \(\Delta_{i}^{j}=\\frac{v_{i+1}^{j}-v_{i+1}^{j+1}}{s_{i+1}^{j}-s_{i+1}^{j+1}}\) and ensuring the of value of the strategy before and after the rebalancing is 
#                                      the same \(c_{i}^{j}=\pi_{i}^{j}-(\Delta_{i-1}^{j}-\Delta_{i}^{j})s_{i}^{j}\). The tree is computed forward, and will at all times replicate with option price.
#                                       At the end of it we obtain the option payoff.
#                                     """]),
#                                 ])]),
#                         #
#                         #
#                         dcc.Tab(
#                             label='Input',
#                             value='Input',
#                             children=html.Div(children=[
#                                                 html.Br(),
#                                                 #
#                                                 html.P(
#                                                     """
#                                                     Hover your mouse over any input to get its definition.                           
#                                                     """
#                                                 ),
#                                                 dcc.Dropdown(
#                                                     id='CallOrPut',
#                                                     options=[{'label':'European Call option', 'value':"Call"},
#                                                              {'label':'European Put option', 'value':"Put"}],
#                                                     value='Call'),
#                                                 #
#                                                 html.Br(),
#                                                 #
#                                                 html.Div(children=[html.Label('Spot price', title=list_input["Spot price"], style={'font-weight': 'bold', "text-align":"center", "width":"25%",'display': 'inline-block'} ),
#                                                                    dcc.Input(id="S", value=100, type='number', style={"width":"16%", 'display': 'inline-block'}),
#                                                                    html.Label("Strike", title=list_input["Strike"], style={'font-weight': 'bold',"text-align":"center", "width":"25%",'display': 'inline-block'} ),
#                                                                    dcc.Input(id="K", value=100, type='number', style={"width":"16%", 'display': 'inline-block'}),
#                                                                   ],),                     
#                                                 #
#                                                 html.Div(children=[html.Label("Drift", title=list_input["Drift"], style={'font-weight': 'bold', 'display': 'inline-block'}),
#                                                                    html.Label(id="drift", style={'display': 'inline-block'}),
#                                                                   ]),
#                                                 #
#                                                 dcc.Slider(id='mu', min=-0.30, max=0.30, value=0.10, step=0.01, marks={-0.30: '-30%', 0.30: '30%'}),
#                                                 #
#                                                 html.Div([html.Label('Volatility', title=list_input["Volatility"], style={'font-weight': 'bold', "display":"inline-block"}),
#                                                           html.Label(id="sigma", style={"display":"inline-block"}),]),  
#                                                 #
#                                                 dcc.Slider(id='vol', min=0, max=1, step=0.01, value=0.20, marks={0:"0%", 1:"100%"}),
#                                                 #
#                                                 html.Div([html.Label('Risk-free rate', title=list_input["Risk-free rate"], style={'font-weight': 'bold', "display":"inline-block"}),
#                                                           html.Label(id="riskfree", style={"display":"inline-block"}),]),  
#                                                 dcc.Slider(id='Rf', min=0, max=0.1, step=0.01, value=0.05, marks={0:"0%", 0.1:"10%"}),
#                                                 #
#                                                 html.Div([html.Label('Maturity', title=list_input["Maturity"], style={'font-weight':'bold', "display":"inline-block"}),
#                                                           html.Label(id="matu", style={"display":"inline-block"}),]),                                        
#                                                 dcc.Slider(id='T', min=0.25, max=5, 
#                                                            marks={0.25:"3 months", 5:"5 years"}, step=0.25, value=3),
#                                                 #
#                                                 html.Br(),
#                                                 html.Div(children=[html.Label('Tree periods', title=list_input["Tree periods"], style={'font-weight': 'bold', "text-align":"center", "width":"25%",'display': 'inline-block'} ),
#                                                                    dcc.Input(id="tree_periods", value=4, type='number', style={"width":"16%", 'display': 'inline-block'}),
#                                                                   ],),
#                                                 ])),
#         ],),], style={'float': 'left', 'width': '25%', 'margin':"30px"}),
#     ])



# def graphs():
#     return html.Div(id='right-column', 
#                     children=[
#                         html.Br(),
#                         html.Div([
#                             html.Div(children=[dcc.Markdown(children=graph_option_intrinsic),
#                                                dcc.Graph(id='option_intrinsic'),],
#                                      style={"float":"right", "width":"45%", "display":"inline-block"}),
#                             html.Div(children=[dcc.Markdown(children=graph_stock_simul),
#                                                dcc.Graph(id='stock_simul'),],
#                                      style={"float":"right", "width":"55%", "display":"inline-block"}),
#                                 ]),
#                         html.Div([
#                             html.Div(children=[dcc.Markdown(children=graph_option_price),
#                                                dcc.Graph(id='option_price'),],
#                                      style={"float":"right", "width":"45%", "display":"inline-block"}),
#                             html.Div(children=[dcc.Markdown(children=graph_port_details_text),
#                                                dcc.Graph(id='port_details'),],
#                                      style={"float":"right", "width":"55%", "display":"inline-block"}),
#                                 ]),
#                         html.Div([
#                             html.Div(children=[dcc.Markdown(children=graph_cash),
#                                                dcc.Graph(id='cash_acc'),],
#                                      style={"float":"right", "width":"45%", "display":"inline-block"}),
#                             html.Div(children=[dcc.Markdown(children=graph_nbr_shares),
#                                                dcc.Graph(id='nbr_shares'),],
#                                      style={"float":"right", "width":"55%", "display":"inline-block"}),
#                                 ]),


#                              ], 
#                     style={'float': 'right', 'width': '70%'})



# app.layout = html.Div(
#                 id='main_page',
#                 children=[
#                     dcc.Store(id='memory-output'),
#                     header(),
#                     body(),
#                     graphs(),
#                          ],
#                      )




# @app.callback(
# 	Output('memory-output', 'data'),
# 	[Input('CallOrPut', 'value'),
#      Input("S","value"),
#      Input("K", "value"),
#      Input("Rf", "value"),
#      Input("T","value"),
#      Input("mu","value"),
#      Input("vol", "value"),
#      Input("tree_periods", "value"),])
# def get_rep_strat_data(CallOrPut, S, K, Rf,T,mu,vol,tree_periods):
# 	nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = RepStrat_EU_Option_CRR_GRW_V5(CallOrPut, S, K, Rf, T, mu, vol, tree_periods)
																
# 	return nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown

# @app.callback(
#     Output('stock_simul', 'figure'),
#     [Input('memory-output', 'data'),])
# def graph_stock_simul(data):
# 	nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data

# 	return{
#        'layout': go.Layout(
#         title={'yref':"paper",
#         		'y':1,
#         		"yanchor":"bottom"},
#         #margin={"t":15},
#         margin=dict(
#                 l=0,
#                 #r=50,
#                 #b=100,
#                 t=15,
#                 #pad=4
#             ),
#         # showlegend=False,
#         xaxis={'showgrid': False, # thin lines in the background
#     		   'zeroline': False, # thick line at x=0
#                'visible': False,},  # numbers below}
#         yaxis={'showgrid': False, # thin lines in the background
#     		   'zeroline': False, # thick line at x=0
#                'visible': False,},  # numbers below}
#         legend=dict(
#             x=0,
#             y=1,
#             traceorder='normal',
#             bgcolor='rgba(0,0,0,0)'),
#     ),
#     	'data': [
# 	        go.Scatter(
# 	            x=edge_x,
# 	            y=edge_y,
# 	            mode='lines',
# 	            line=dict(width=0.5),
# 	            hoverinfo='none',
# 	            showlegend=False,
# 	            ),
# 	        go.Scatter(
# 	        	x=node_x,
# 	        	y=node_y,
# 	        	mode='markers+text',
# 	        	marker=dict(size=40),
# 	        	text=stocksLabel,
# 	        	showlegend=False,
# 	        	hoverinfo='none',
# 	        	),
# 	        go.Scatter(
# 	        	x=[None],
# 	        	y=[None],
# 	        	mode='markers',
# 	        	name=f'Up factor: {u}'
# 	        	),
# 	     	go.Scatter(
# 	        	x=[None],
# 	        	y=[None],
# 	        	mode='markers',
# 	        	name=f'Down factor: {d}'
# 	        	),
# 	     	go.Scatter(
# 	        	x=[None],
# 	        	y=[None],
# 	        	mode='markers',
# 	        	name=f'Prob up: {probUp}'
# 	        	),
# 	     	go.Scatter(
# 	        	x=[None],
# 	        	y=[None],
# 	        	mode='markers',
# 	        	name=f'Prob down: {probDown}'
# 	        	),
# 	    ],
# }


# @app.callback(
#     Output('port_details', 'figure'),
#     [Input('memory-output', 'data'),])
# def graph_portf_details(data):
# 		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data

# 		return{
#        'layout': go.Layout(
#         title={'yref':"paper",
#         		'y':1,
#         		"yanchor":"bottom"},
#         showlegend=False,
#         margin=dict(
#                 l=0,
#                 #r=50,
#                 #b=100,
#                 t=15,
#                 #pad=4
#             ),
#         xaxis={'showgrid': False, # thin lines in the background
#     		   'zeroline': False, # thick line at x=0
#                'visible': False,},  # numbers below}
#         yaxis={'showgrid': False, # thin lines in the background
#     		   'zeroline': False, # thick line at x=0
#                'visible': False,}  # numbers below}
#     ),
#     	'data': [
# 	        go.Scatter(
# 	            x=edge_x,
# 	            y=edge_y,
# 	            mode='lines',
# 	            line=dict(width=0.5),
# 	            hoverinfo='none',
# 	            ),
# 	        go.Scatter(
# 	        	x=node_x,
# 	        	y=node_y,
# 	        	mode='markers+text',
# 	        	marker=dict(size=40),
# 	        	text=portfolioLabel,
# 	        	hoverinfo='none',
# 	        	),
# 	    ],
# }


# @app.callback(
#     Output('nbr_shares', 'figure'),
#     [Input('memory-output', 'data'),])
# def graph_nbr_of_shares(data):
# 		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data

# 		return{
#        'layout': go.Layout(
#         title={'yref':"paper",
#         		'y':1,
#         		"yanchor":"bottom"},
#         showlegend=False,
#         margin=dict(
#                 l=0,
#                 #r=50,
#                 #b=100,
#                 t=15,
#                 #pad=4
#             ),        xaxis={'showgrid': False, # thin lines in the background
#     		   'zeroline': False, # thick line at x=0
#                'visible': False,},  # numbers below}
#         yaxis={'showgrid': False, # thin lines in the background
#     		   'zeroline': False, # thick line at x=0
#                'visible': False,}  # numbers below}
#     ),
#     	'data': [
# 	        go.Scatter(
# 	            x=edge_x,
# 	            y=edge_y,
# 	            mode='lines',
# 	            line=dict(width=0.5),
# 	            hoverinfo='none',
# 				),
# 	        go.Scatter(
# 	        	x=node_x,
# 	        	y=node_y,
# 	        	mode='markers+text',
# 	        	marker=dict(size=40),
# 	        	text=nbrofsharesLabel,
# 	        	hoverinfo='none',
# 	        	),
# 	    ],
# }

# @app.callback(
#     Output('cash_acc', 'figure'),
#     [Input('memory-output', 'data'),])
# def graph_cash_account(data):
# 		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data
# 		return{
#        'layout': go.Layout(
#         title={'yref':"paper",
#         		'y':1,
#         		"yanchor":"bottom"},
#         showlegend=False,
#         margin=dict(
#                 l=0,
#                 #r=50,
#                 #b=100,
#                 t=15,
#                 #pad=4
#             ),
#         xaxis={'showgrid': False, # thin lines in the background
#     		   'zeroline': False, # thick line at x=0
#                'visible': False,},  # numbers below}
#         yaxis={'showgrid': False, # thin lines in the background
#     		   'zeroline': False, # thick line at x=0
#                'visible': False,}  # numbers below}
#     ),
#     	'data': [
# 	        go.Scatter(
# 	            x=edge_x,
# 	            y=edge_y,
# 	            mode='lines',
# 	            line=dict(width=0.5),
# 	            hoverinfo='none',
# 	            ),
# 	        go.Scatter(
# 	        	x=node_x,
# 	        	y=node_y,
# 	        	mode='markers+text',
# 	        	marker=dict(size=40),
# 	        	text=cashLabel,
# 	        	hoverinfo='none',
# 	        	),
# 	    ],
# }

# @app.callback(
#     Output('option_price', 'figure'),
#     [Input('memory-output', 'data'),])
# def graph_option_pricee(data):
# 		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data
# 		return{
#        'layout': go.Layout(
#         title={'yref':"paper",
#         		'y':1,
#         		"yanchor":"bottom"},
#         showlegend=False,
#         margin=dict(
#                 l=0,
#                 #r=50,
#                 #b=100,
#                 t=15,
#                 #pad=4
#             ),
#         xaxis={'showgrid': False, # thin lines in the background
#     		   'zeroline': False, # thick line at x=0
#                'visible': False,},  # numbers below}
#         yaxis={'showgrid': False, # thin lines in the background
#     		   'zeroline': False, # thick line at x=0
#                'visible': False,}  # numbers below}
#     ),
#     	'data': [
# 	        go.Scatter(
# 	            x=edge_x,
# 	            y=edge_y,
# 	            mode='lines',
# 	            line=dict(width=0.5),
# 	            hoverinfo='none',
# 	            ),
# 	        go.Scatter(
# 	        	x=node_x,
# 	        	y=node_y,
# 	        	mode='markers+text',
# 	        	marker=dict(size=40),
# 	        	text=optionpriceLabel,
# 	        	hoverinfo='none',
# 	        	),
# 	    ],
# }

# @app.callback(
#     Output('option_intrinsic', 'figure'),
#     [Input('memory-output', 'data'),])
# def graph_option_pricee(data):
# 		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data
# 		return{
#        'layout': go.Layout(
#         title={'yref':"paper",
#         		'y':1,
#         		"yanchor":"bottom"},
#         showlegend=False,
#         margin=dict(
#                 l=0,
#                 #r=50,
#                 #b=100,
#                 t=15,
#                 #pad=4
#             ),
#         xaxis={'showgrid': False, # thin lines in the background
#     		   'zeroline': False, # thick line at x=0
#                'visible': False,},  # numbers below}
#         yaxis={'showgrid': False, # thin lines in the background
#     		   'zeroline': False, # thick line at x=0
#                'visible': False,}  # numbers below}
#     ),
#     	'data': [
# 	        go.Scatter(
# 	            x=edge_x,
# 	            y=edge_y,
# 	            mode='lines',
# 	            line=dict(width=0.5),
# 	            hoverinfo='none',
# 	            ),
# 	        go.Scatter(
# 	        	x=node_x,
# 	        	y=node_y,
# 	        	mode='markers+text',
# 	        	marker=dict(size=40),
# 	        	text=intrinsicLabel,
# 	        	hoverinfo='none',
# 	        	),
# 	    ],
# }

# @app.callback(Output('drift', 'children'),
#               [Input('mu', 'value')])
# def display_value(value):
#     return f': {int(value*100)}%'

# @app.callback(Output('sigma', 'children'),
#               [Input('vol', 'value')])
# def display_value2(value):
#     return f': {int(value*100)}%'

# @app.callback(Output('riskfree', 'children'),
#               [Input('Rf', 'value')])
# def display_value3(value):
#     return f': {int(value*100)}%'

# @app.callback(Output('matu', 'children'),
#               [Input('T', 'value')])
# def display_value4(value):
#     if value==0.25 or value==0.5 or value==0.75:
#         return f": {int(value*12)} months"
#     elif value == 1:
#         return f': {value} year'
#     else:
#         return f': {value} years'

# @app.callback(
#     Output("popover", "is_open"),
#     [Input("popover-target", "n_clicks")],
#     [State("popover", "is_open")],
# )
# def toggle_popover(n, is_open):
#     if n:
#         return not is_open
#     return is_open


# if __name__ == '__main__':
#     app.run_server(debug=True)
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from EU_Option_CRR_GRW_V5 import *
from descriptions import list_input
import base64


def body():
    return html.Div(children=[
            html.Div(id='left-column', children=[
                dcc.Tabs(
                    id='tabs', value='The app',
                    children=[
                        dcc.Tab(
                            label='The app',
                            value='The app',
                            children=html.Div(children=[
                                html.Br(),
                                html.H4('What is this app?', style={"text-align":"center"}),
                                html.P(
                                    """
                                    This app computes the replication strategy of vanilla European options on a set of given, comparing the Cox-Ross-Rubinstein model and strategy option price.
                                    """
                                ),
                                html.P(
                                    """
                                    The goal is to showcase that the price is truly arbitrage-free, i.e. that both risk-neutral pricing and replicating strategy have the same values. 
                                    """
                                ),
                                html.P(
                                    """
                                    Read more about options : 
                                    https://en.wikipedia.org/wiki/Option_(finance)
                                    
                                    """
                                ),
                            ])
                        ),
                        dcc.Tab(
                            label="Model",
                            value="Model",
                            children=[html.Div(children=[
                                html.Br(),
                                html.H4("The Cox-Ross-Rubinstein model", style={"text-align":"center"}),
                                html.P([
                                    """
                                    The Cox-Ross-Rubinstein model (CRR) is an example of a multi-period market model of the stock price.                                     
                                    """]),
                                html.Hr(),
                                html.H4("Model assumptions", style={"text-align":"center"}),
                                "Its main assumptions are:",
                                html.Ul([html.Li("Does not consider dividends and transaction costs"), 
                                         html.Li("The volatility and risk-free rate are assumed constant"),
                                         html.Li("Fraction of shares can be traded"),
                                         html.Li("The underlying asset can only either go 'up' by a fixed factor \(u<1\) or 'down' by \(0<d<1\)."),
                                         html.Li("The log-returns are independent at all periods")]),
                                html.Hr(),
                                html.H4("Underlying asset dynamics", style={"text-align":"center"}),
                                html.P([
                                    """Under CRR, the underlying asset follows a geometric random walk with 
                                    drift \(\mu\delta\) and volatility \(\sigma\sqrt{\delta}\). The probability to go 'up' and 'down' are respectively \(p\) and \(1-p\) (under \(\mathcal{P}\)).
                                    The stock price at period \(i\) can be modeled as a function of a binomial random variable, and the constant 'up' and 'down' factors
                                    computed: $$u=e^{\mu\delta+\sigma\sqrt{\delta}}$$ $$d=e^{\mu\delta-\sigma\sqrt{\delta}}$$. The \(\mathcal{Q}\)-probability allowing the discounted
                                    stock price to be a martingale amounts to the \(p\) value (under \(\mathcal{Q}\)) that leads to the martingale property: \(p=\\frac{e^{r}-d}{u-d}\).
                                    """])
                                ])]),
                        #
                        #
                        dcc.Tab(
                            label="Approach",
                            value="Methodology",
                            children=[html.Div(children=[
                                html.Br(),
                                html.H4("Methodology followed", style={"text-align":"center"}),
                                html.P([
                                    """
                                    To prove that the risk-neutral price is arbitrage-free, let us try to perfectly replicate it with a strategy. If the strategy is successfull, then 
                                    the price is unique and therefore arbitrage-free.
                                    """]),
                                html.Hr(),
                                html.H4("Risk-neutral pricing", style={"text-align":"center"}),
                                html.P([
                                    """
                                    With the CRR, the stock tree and the option intrinsic value are easily computed at all nodes. Under the pricing measure, the option
                                    price of a node is simply the discounted value of the two children nodes. The price tree is therefore filled backwards,
                                    starting from the leaves (i.e. the payoff).
                                    """]),
                                html.H4("Replicating portfolio", style={"text-align":"center"}),
                                html.P([
                                    """
                                    Then, if the price computed is truly arbitrage-free, a replication strategy can be based on this price: \(\pi_{0} = v_{0}\).
                                     At the begining of each period, the number of shares to hold is \(\Delta_{i}^{j} = \\frac{v_{i+1}^{j}-v_{i+1}^{j+1}}{s_{i+1}^{j}-s_{i+1}^{j+1}}\). 
                                     The initial amount of cash will be \(c_{0} = \pi_{0} - \Delta_{0}s_{0}\). At each node, a portfolio rebalancing is needed. Before the rebalancing, 
                                     \(\Delta\) is the same from node to node \(\Delta_{i}^{j}=\Delta_{i-1}^{j}\), the cash account grew at the risk-free rate \(c_{i}^{j}=c_{i-1}^{j}e^{r}\), 
                                     and the portfolio is the sum of both equity and cash positions \(\pi_{i}^{j}=c_{i}^{j}+\Delta_{i}^{j}s_{i}^{j}\). The rebalancing is done by updating the shares 
                                     to hold \(\Delta_{i}^{j}=\\frac{v_{i+1}^{j}-v_{i+1}^{j+1}}{s_{i+1}^{j}-s_{i+1}^{j+1}}\) and ensuring the of value of the strategy before and after the rebalancing is 
                                     the same \(c_{i}^{j}=\pi_{i}^{j}-(\Delta_{i-1}^{j}-\Delta_{i}^{j})s_{i}^{j}\). The tree is computed forward, and will at all times replicate with option price.
                                      At the end of it we obtain the option payoff.
                                    """]),
                                ])]),
                        #
                        #
                        dcc.Tab(
                            label='Input',
                            value='Input',
                            children=html.Div(children=[
                                                html.Br(),
                                                #
                                                html.P(
                                                    """
                                                    Hover your mouse over any input to get its definition.                           
                                                    """
                                                ),
                                                dcc.Dropdown(
                                                    id='CallOrPut',
                                                    options=[{'label':'European Call option', 'value':"Call"},
                                                             {'label':'European Put option', 'value':"Put"}],
                                                    value='Call'),
                                                #
                                                html.Br(),
                                                #
                                                html.Div(children=[html.Label('Spot price', title=list_input["Spot price"], style={'font-weight': 'bold', "text-align":"center", "width":"25%",'display': 'inline-block'} ),
                                                                   dcc.Input(id="S", value=100, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                                                   html.Label("Strike", title=list_input["Strike"], style={'font-weight': 'bold',"text-align":"center", "width":"25%",'display': 'inline-block'} ),
                                                                   dcc.Input(id="K", value=100, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                                                  ],),                     
                                                #
                                                html.Div(children=[html.Label("Drift", title=list_input["Drift"], style={'font-weight': 'bold', 'display': 'inline-block'}),
                                                                   html.Label(id="drift", style={'display': 'inline-block'}),
                                                                  ]),
                                                #
                                                dcc.Slider(id='mu', min=-0.30, max=0.30, value=0.10, step=0.01, marks={-0.30: '-30%', 0.30: '30%'}),
                                                #
                                                html.Div([html.Label('Volatility', title=list_input["Volatility"], style={'font-weight': 'bold', "display":"inline-block"}),
                                                          html.Label(id="sigma", style={"display":"inline-block"}),]),  
                                                #
                                                dcc.Slider(id='vol', min=0, max=1, step=0.01, value=0.20, marks={0:"0%", 1:"100%"}),
                                                #
                                                html.Div([html.Label('Risk-free rate', title=list_input["Risk-free rate"], style={'font-weight': 'bold', "display":"inline-block"}),
                                                          html.Label(id="riskfree", style={"display":"inline-block"}),]),  
                                                dcc.Slider(id='Rf', min=0, max=0.1, step=0.01, value=0.05, marks={0:"0%", 0.1:"10%"}),
                                                #
                                                html.Div([html.Label('Maturity', title=list_input["Maturity"], style={'font-weight':'bold', "display":"inline-block"}),
                                                          html.Label(id="matu", style={"display":"inline-block"}),]),                                        
                                                dcc.Slider(id='T', min=0.25, max=5, 
                                                           marks={0.25:"3 months", 5:"5 years"}, step=0.25, value=3),
                                                #
                                                html.Br(),
                                                html.Div(children=[html.Label('Tree periods: ', title=list_input["Tree periods"], style={'font-weight': 'bold', "text-align":"left", "width":"30%",'display': 'inline-block'} ),
                                                                   dcc.Input(id="tree_periods", value=4, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                                                  ],),
                                                html.Div(children=[html.Label("Graph type: ", style={'font-weight': 'bold', "text-align":"center",'display': 'inline-block'} ),
                                                                   dcc.RadioItems(id="GraphType",
                                                                                  options=[{'label': 'Spatial', 'value': 'spatial'},
                                                                                           {'label': 'Tree', 'value': 'tree'}
                                                                                          ],
                                                                                  value='spatial',
                                                                                  labelStyle={'padding':5, 'font-weight': 'bold', 'display': 'inline-block'},
                                                                                  style={'font-weight': 'bold', "text-align":"center",'display': 'inline-block'}
                                                                                 ), 
                                                                  ]),
                                                html.P("""Note that some errors are possible due to rounding decimals when displaying the values in the chart. Refer to 'Download the data' if you wish to check. """),
                                                html.Br(),
                                                html.A('Download Data', id='download-link', download="rawdata.xlsx",)# href="", target="_blank"),
                                                html.P("""Note: requires excel decimal separator to be a dot.""", style={"font-size":12}),

                                                ])),
        ],),], style={'float': 'left', 'width': '25%', 'margin':"30px"}),
    ])



def graphs():
    return html.Div(id='right-column', 
                    children=[
                        html.Br(),
                        html.Div([
                            html.Div(children=[dcc.Markdown(children=''' #### Option intrinsic value'''),
                                               dcc.Graph(id='option_intrinsic'),],
                                     style={"float":"right", "width":"45%", "display":"inline-block"}),
                            html.Div(children=[dcc.Markdown(children=''' #### Stock simulation '''),
                                               dcc.Graph(id='stock_simul'),],
                                     style={"float":"right", "width":"55%", "display":"inline-block"}),
                                ]), 
                        html.Div([
                            html.Div(children=[dcc.Markdown(children=''' #### Option price'''),
                                               dcc.Graph(id='option_price'),],
                                     style={"float":"right", "width":"45%", "display":"inline-block"}),
                            html.Div(children=[dcc.Markdown(children=''' #### Portfolio after rebalancing'''),
                                               dcc.Graph(id='port_details'),],
                                     style={"float":"right", "width":"55%", "display":"inline-block"}),
                                ]),
                        html.Div([
                            html.Div(children=[dcc.Markdown(children=''' #### Cash account after rebalancing'''),
                                               dcc.Graph(id='cash_acc'),],
                                     style={"float":"right", "width":"45%", "display":"inline-block"}),
                            html.Div(children=[dcc.Markdown(children=''' #### Shares held after rebalancing'''),
                                               dcc.Graph(id='nbr_shares'),],
                                     style={"float":"right", "width":"55%", "display":"inline-block"}),
                                ]),


                             ], 
                    style={'float': 'right', 'width': '70%'})
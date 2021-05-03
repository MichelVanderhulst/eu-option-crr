import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from EU_Option_CRR_GRW_V5 import *
from descriptions import list_input
import base64
from dash_extensions import Download

def body():
    return html.Div(children=[
            html.Div(id='left-column', children=[
                dcc.Tabs(
                    id='tabs', value='The app',
                    children=[
                        dcc.Tab(
                            label='About this App',
                            value='About this App',
                            children=html.Div(children=[
                                html.Br(),
                                html.H4('What is this app?', style={"text-align":"center"}),
                                html.P(f"""This app computes the replication strategy of European options on a set of given inputs, in the Cox-Ross-Rubinstein framework"""),
                                html.P(f"""The goal is to showcase that under the Cox-Ross-Rubinstein model assumptions (see "Model" tab), the price \(V_0\) given by the pricing formula is "arbitrage-free". 
                                           Indeed, we show that in this case, it is possible to build a strategy that"""),
                                html.Ul([html.Li("Can be initiated with \(V_0\) cash at time \(0\)."), 
                                         html.Li('Is self-financing (i.e., no need to "feed" the strategy  with extra cash later'),
                                         html.Li("Will deliver exactly the payoff of the option at maturity")
                                       ]),
                                html.Hr(),
                                html.P(["""
                                	    The considered options are European options paying \(\psi(S_T)\) at maturity \(T\) where \(\psi(X)\) is the payoff function. 
						   				For a call, the payoff function is \(\psi(S_T)=max(0,S_T-K)\) and for a put \(\psi(S_T)=max(0,K-S_T)\) where K is the strike price."""]),
                                html.Hr(),
                                html.P("""Read more about options: https://en.wikipedia.org/wiki/Option_(finance)"""),
                            ])
                        ),
                        dcc.Tab(
                            label="Model",
                            value="Model",
                            children=[html.Div(children=[
                                html.Br(),
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
                                    """
                                    Under CRR, the underlying asset follows a geometric random walk with drift \(\mu\delta\) and volatility \(\sigma\sqrt{\delta}\). The probability to go 
                					'up' and 'down' are respectively \(p\) and \(q=1-p\) (under \(\mathcal{P}\)).The stock price at period \(i\) can be modeled as a function of a binomial 
                					random variable, and the constant 'up' and 'down' factors computed: $$u=e^{\mu\delta+\sigma\sqrt{\delta}}$$ $$d=e^{\mu\delta-\sigma\sqrt{\delta}}$$ 
                					The \(\mathcal{Q}\)-probability allowing the discounted stock price to be a martingale amounts to the \(\\tilde{p}\) value (under \(\mathcal{Q}\)) 
                					that leads to the martingale property: \(\\tilde{p}=\\frac{e^{r}-d}{u-d}\).
                                    """]),
                                html.Hr(),
                                html.H4("Option price", style={"text-align":"center"}),
                                html.P(["""
										With the CRR, the stock tree and the option intrinsic value are easily computed at all nodes. Under the pricing measure \(\mathcal{Q}\), 
               							the option price of a node is simply the discounted value of the two children nodes. The price tree is therefore filled backwards, starting from the leaves (i.e. the payoff).
               							The pricing formula is thus $$V_i=e^{-r\\delta}(V_{i+1}\\tilde{p}+V_{i+1}\\tilde{q})$$
                                		"""]),
                                html.Hr(),
                                html.H4("Academic references", style={"text-align":"center"}),
                                html.Ul([html.Li("Vrins, F.  (2020). Course notes for LLSM2225:  Derivatives Pricing. (Financial Engineering Program, Louvain School of Management, Université catholique de Louvain)"), 
                                         html.Li("Shreve, S. E. (2004). Stochastic Calculus for Finance I The Binomial Asset Pricing Model (2nd ed.). Springer Finance.")
                                       ]),                                
                                ])]),
                        #
                        #
                        dcc.Tab(
                            label="Appro-ach",
                            value="Methodology",
                            children=[html.Div(children=[
                                html.Br(),
                                html.H4("Methodology followed", style={"text-align":"center"}),
                                html.P([
                                    """
                                    To prove that the CRR option price is arbitrage-free, let us try to perfectly replicate it with a strategy. 
                                    If the strategy is successful, then the option price is unique and therefore arbitrage-free.
                                    """]),
                                html.Hr(),
                                html.H4("Replicating portfolio", style={"text-align":"center"}),
                                html.P([
                                    """
									Let us start a replication strategy based on the option price: \(\Pi_{0} = V_{0}\). The portfolio is composed of a cash account and a equity account. 
									At the begining of each period, the number of shares to hold is given by $$\Delta_{i}^{j} = \\frac{v_{i+1}^{j}-v_{i+1}^{j+1}}{s_{i+1}^{j}-s_{i+1}^{j+1}}$$ 
									The initial amount of cash will thus be \(c_{0} = \Pi_{0} - \Delta_{0}s_{0}\). At each node, a portfolio rebalancing is needed to ensure that the portfolio value is 
									equal to the option price. Before the rebalancing, \(\Delta\) is the same from node to node. Mathematically speaking, we have that $$\Delta_{i}^{j}=\Delta_{i-1}^{j}$$ 
									The cash account grew at the risk-free rate \(c_{i}^{j}=c_{i-1}^{j}e^{r}\), and the portfolio is the sum of both equity and cash positions $$\pi_{i}^{j}=c_{i}^{j}+\Delta_{i}^{j}s_{i}^{j}$$ 
									The rebalancing is done by updating the number of shares to hold $$\Delta_{i}^{j}=\\frac{v_{i+1}^{j}-v_{i+1}^{j+1}}{s_{i+1}^{j}-s_{i+1}^{j+1}}$$ 
									and ensuring the of value of the strategy before and after the rebalancing is the same $$c_{i}^{j}=\pi_{i}^{j}-(\Delta_{i-1}^{j}-\Delta_{i}^{j})s_{i}^{j}$$ 
									The tree is computed forward, and will at all times replicate with option price. At the end of it we obtain the option payoff.
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
                                               html.Div(children=[html.Label('Spot price', title=list_input["Spot price"], style={'font-weight': 'bold', "text-align":"left", "width":"25%",'display': 'inline-block'} ),
                                                                  dcc.Input(id="S", value=100, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                                                  html.P("",id="message_S", style={"font-size":12, "color":"red", "padding":5, 'width': '55%', "text-align":"left", 'display': 'inline-block'})
                                                                  ]
                                                        ),

                                              html.Div(children=[html.Label("Strike", title=list_input["Strike"], style={'font-weight': 'bold',"text-align":"left", "width":"25%",'display': 'inline-block'} ),
                                                                 dcc.Input(id="K", value=100, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                                                 html.P("",id="message_K", style={"font-size":12, "color":"red", "padding":5, 'width': '55%', "text-align":"left", 'display': 'inline-block'})
                                                                ],
                                                      ),                   
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
                                                                   html.P("",id="message_tree", style={"font-size":12, "color":"red", "padding":5, 'width': '40%', "text-align":"left", 'display': 'inline-block'})
                                                                  ],
                                                        ),
                                                html.Div(children=[html.Label("Graph type: ", style={'font-weight': 'bold', "text-align":"center",'display': 'inline-block'} ),
                                                                   dcc.RadioItems(id="GraphType",
                                                                                  options=[{'label': 'Spatial', 'value': 'spatial'},
                                                                                           {'label': 'Tree', 'value': 'tree'}
                                                                                          ],
                                                                                  value='tree',
                                                                                  labelStyle={'padding':5, 'font-weight': 'bold', 'display': 'inline-block'},
                                                                                  style={'font-weight': 'bold', "text-align":"center",'display': 'inline-block'}
                                                                                 ), 
                                                                  ]),
                                                html.P("""Note that some errors are possible due to rounding decimals when displaying the values in the chart. Refer to 'Download the data' if you wish to check. """),
                                                html.Br(),
                                                # html.A('Download Data', id='download-link', target="_blank", href="", download="data"), 
                                                html.Div([html.Button("Download xlsx", id="btn", n_clicks=0), Download(id="download")]),
                                                html.P("""Note: requires excel decimal separator to be a dot.""", style={"font-size":12}),

                                                ])),
        ],),], style={'float': 'left', 'width': '25%', 'margin':"30px"}), #"border":"2px black solid" => have to add padding to that
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
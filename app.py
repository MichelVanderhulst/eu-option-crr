import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from EU_Option_CRR_GRW_V5 import *
from descriptions import list_input
import pandas 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

top_markdown_text = '''
### Call/Put Replication Strategy Tool - CRR model
#### Michel Vanderhulst 
#### Master's thesis - Louvain School of Management
'''

graph_stock_simul = ''' #### Stock simulation (GRW) '''
graph_port_details_text = ''' #### Portfolio before/after rebalancing'''
graph_nbr_shares = ''' #### Shares held before/after rebalancing'''
graph_cash = ''' #### Cash account before/after rebalancing'''
graph_option_price = ''' #### Option price'''
graph_option_intrinsic = ''' #### Option intrinsic value'''

app.layout = html.Div([
	dcc.Store(id='memory-output'),
    # HEADER
    dcc.Markdown(children=top_markdown_text),
    #
    # LEFT - CHOROPLETH MAP
    html.Div([
        dcc.Dropdown(
            id='CallOrPut',
            options=[{'label':'European Call option', 'value':"Call"},
            		 {'label':'European Put option', 'value':"Put"}],
            value='Call'),
        #
        html.Div([
        	html.Div([
            	html.Label('Spot price', title=list_input["Spot price"]),
            	dcc.Input(id="S", value=100, type='number')
        	], className="six columns"),

       		html.Div([
            	html.Label("Strike", title=list_input["Strike"]),
            	dcc.Input(id="K", value=100, type='number')
        	], className="six columns"),
    	], className="row"),
    	#
    	html.Label('Drift', title=list_input["Drift"]),
        html.Div(id='drift'),
    	dcc.Slider(
    		id='mu',
        	min=-0.30,
        	max=0.30,
        	value=0.10,
        	step=0.01),
    	#
        html.Label('Volatility', title=list_input["Volatility"]),
        html.Div(id='sigma'),
    	dcc.Slider(
    		id='vol',
        	min=0,
        	max=1,
        	step=0.01,
        	value=0.20),
    	#
    	dcc.Markdown(children=graph_stock_simul),
        dcc.Graph(id='stock_simul'),
    	#
    	dcc.Markdown(children=graph_option_price),
        dcc.Graph(id='option_price'),
        #
    	dcc.Markdown(children=graph_option_intrinsic),
        dcc.Graph(id='option_intrinsic'),


    ], style={'float': 'left', 'width': '50%'}),

    # RIGHT - SCATTERPLOT
    html.Div([
    	html.Label('Risk-free rate', title=list_input["Risk-free rate"]),
        html.Div(id='riskfree'),
    	dcc.Slider(
    		id='Rf',
        	min=0,
        	max=0.1,
        	step=0.01,
        	value=0.05),
    	html.Label('Maturity', title=list_input["Maturity"]),
    	dcc.Slider(
    		id='T',
        	min=1,
        	max=5,
        	marks={i: '{}'.format(i) for i in range(6)},
        	step=0.25,
        	updatemode='drag',
        	value=3),
    	#
    	html.Br(),
    	html.Label('Tree periods', title=list_input["Tree periods"]),
        dcc.Input(id="tree_periods", value=4, type='number'),
    	#
    	html.Br(),
    	html.Br(),
    	dcc.Markdown(children=graph_port_details_text),
        dcc.Graph(id='port_details'),
        #
        dcc.Markdown(children=graph_nbr_shares),
        dcc.Graph(id='nbr_shares'),
        #
        dcc.Markdown(children=graph_cash),
        dcc.Graph(id='cash_acc'),
    ], style={'float': 'right', 'width': '50%'}),


])



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
	nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = RepStrat_EU_Option_CRR_GRW_V5(CallOrPut, S, K, Rf, T, mu, vol, tree_periods)
																
	return nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown

@app.callback(
    Output('stock_simul', 'figure'),
    [Input('memory-output', 'data'),])
def graph_stock_simul(data):
	nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data

	return{
       'layout': go.Layout(
        title={'yref':"paper",
        		'y':1,
        		"yanchor":"bottom"},
        margin={"t":15},
        # showlegend=False,
        xaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,},  # numbers below}
        yaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,}  # numbers below}
    ),
    	'data': [
	        go.Scatter(
	            x=edge_x,
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
	        	text=stocksLabel,
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


@app.callback(
    Output('port_details', 'figure'),
    [Input('memory-output', 'data'),])
def graph_portf_details(data):
		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data

		return{
       'layout': go.Layout(
        title={'yref':"paper",
        		'y':1,
        		"yanchor":"bottom"},
        showlegend=False,
        margin={"t":15},
        xaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,},  # numbers below}
        yaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,}  # numbers below}
    ),
    	'data': [
	        go.Scatter(
	            x=edge_x,
	            y=edge_y,
	            mode='lines',
	            line=dict(width=0.5),
	            hoverinfo='none',
	            ),
	        go.Scatter(
	        	x=node_x,
	        	y=node_y,
	        	mode='markers+text',
	        	marker=dict(size=40),
	        	text=portfolioLabel,
	        	hoverinfo='none',
	        	),
	    ],
}


@app.callback(
    Output('nbr_shares', 'figure'),
    [Input('memory-output', 'data'),])
def graph_nbr_of_shares(data):
		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data

		return{
       'layout': go.Layout(
        title={'yref':"paper",
        		'y':1,
        		"yanchor":"bottom"},
        showlegend=False,
        margin={"t":15},
        xaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,},  # numbers below}
        yaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,}  # numbers below}
    ),
    	'data': [
	        go.Scatter(
	            x=edge_x,
	            y=edge_y,
	            mode='lines',
	            line=dict(width=0.5),
	            hoverinfo='none',
				),
	        go.Scatter(
	        	x=node_x,
	        	y=node_y,
	        	mode='markers+text',
	        	marker=dict(size=40),
	        	text=nbrofsharesLabel,
	        	hoverinfo='none',
	        	),
	    ],
}

@app.callback(
    Output('cash_acc', 'figure'),
    [Input('memory-output', 'data'),])
def graph_cash_account(data):
		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data
		return{
       'layout': go.Layout(
        title={'yref':"paper",
        		'y':1,
        		"yanchor":"bottom"},
        showlegend=False,
        margin={"t":15},
        xaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,},  # numbers below}
        yaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,}  # numbers below}
    ),
    	'data': [
	        go.Scatter(
	            x=edge_x,
	            y=edge_y,
	            mode='lines',
	            line=dict(width=0.5),
	            hoverinfo='none',
	            ),
	        go.Scatter(
	        	x=node_x,
	        	y=node_y,
	        	mode='markers+text',
	        	marker=dict(size=40),
	        	text=cashLabel,
	        	hoverinfo='none',
	        	),
	    ],
}

@app.callback(
    Output('option_price', 'figure'),
    [Input('memory-output', 'data'),])
def graph_option_pricee(data):
		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data
		return{
       'layout': go.Layout(
        title={'yref':"paper",
        		'y':1,
        		"yanchor":"bottom"},
        showlegend=False,
        margin={"t":15},
        xaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,},  # numbers below}
        yaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,}  # numbers below}
    ),
    	'data': [
	        go.Scatter(
	            x=edge_x,
	            y=edge_y,
	            mode='lines',
	            line=dict(width=0.5),
	            hoverinfo='none',
	            ),
	        go.Scatter(
	        	x=node_x,
	        	y=node_y,
	        	mode='markers+text',
	        	marker=dict(size=40),
	        	text=optionpriceLabel,
	        	hoverinfo='none',
	        	),
	    ],
}

@app.callback(
    Output('option_intrinsic', 'figure'),
    [Input('memory-output', 'data'),])
def graph_option_pricee(data):
		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data
		return{
       'layout': go.Layout(
        title={'yref':"paper",
        		'y':1,
        		"yanchor":"bottom"},
        showlegend=False,
        margin={"t":15},
        xaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,},  # numbers below}
        yaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,}  # numbers below}
    ),
    	'data': [
	        go.Scatter(
	            x=edge_x,
	            y=edge_y,
	            mode='lines',
	            line=dict(width=0.5),
	            hoverinfo='none',
	            ),
	        go.Scatter(
	        	x=node_x,
	        	y=node_y,
	        	mode='markers+text',
	        	marker=dict(size=40),
	        	text=intrinsicLabel,
	        	hoverinfo='none',
	        	),
	    ],
}

@app.callback(Output('drift', 'children'),
              [Input('mu', 'value')])
def display_value(value):
    return 'Selected value: {}'.format(value)

@app.callback(Output('sigma', 'children'),
			  [Input('vol', 'value')])
def display_value2(value):
    return 'Selected value: {}'.format(value)

@app.callback(Output('riskfree', 'children'),
			  [Input('Rf', 'value')])
def display_value3(value):
    return 'Selected value: {}'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
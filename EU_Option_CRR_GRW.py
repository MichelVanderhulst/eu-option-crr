import networkx as nx
from scipy.stats import norm
import numpy as np

#######################################################################################################################
### European Options
### CRR model
### Geometric Random Walk
###
### SOURCES:
## SYLLABUS Derivatives Pricing
# CRR model description, Part 1 : pages 91 -> 94
# Rep Strat CRR implementation, Part 2 pages: 45 -> 58
## Yuxing Yan Python for Finance 2nd edition -> the script for the binomial tree was adapted
#######################################################################################################################


def p_bs(spot_price, strike, riskfree_rate, T, volatility, phi):
    d1 = (np.log(spot_price / strike) + T * (riskfree_rate + 0.5 * volatility * volatility)) / (volatility * np.sqrt(T))
    d2 = (np.log(spot_price / strike) + T * (riskfree_rate - 0.5 * volatility * volatility)) / (volatility * np.sqrt(T))
    return phi * (spot_price * norm.cdf(phi * d1) - strike * np.exp(-riskfree_rate * T) * norm.cdf(phi * d2))


def RepStrat_EU_Option_CRR_GRW(CallOrPut, S, K, rf, T, mu, vol, tree__periods):

    ####################################################################################################################
    #####################  START derivative/model specifics, user input transformation             #####################

    arguments = [CallOrPut, S, K, rf, T, mu, vol, tree__periods] #TC skipped bc can just assume its 0
    for arg in arguments:
        if arg == None:
            return [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]

    if  S < 0 or K < 0  or tree__periods < 1:
        return [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]
    # nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, 
    #edge_x, edge_y, node_x, node_y, round(u,2), round(d,2), round(probUp,2), round(probDown,2), edge_y_Stock, 
    # node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, 
    # edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods :27 returns
    

    if CallOrPut == "Call":
        phi = 1
    elif CallOrPut == "Put":
        phi = -1

    #####################  END derivative/model specifics, user input transformation             #####################
    ####################################################################################################################


    ####################################################################################################################
    #####################                  START accounts initialization                           #####################

    G_Stock, G_Intrinsic, G_Price, G_Portfolio, G_CashAccount, G_Shares = nx.Graph(), nx.Graph(), nx.Graph(), \
                                                                          nx.Graph(), nx.Graph(), nx.Graph()

    stockprices, optionintrinsicvalue, optionprice, labelStocks, labelsIntrinsic, labelsOptionPrice, CashAccount, \
    NbrOfShares, Portfolio, labelPortfolio, labelCash, labelNbrOfShares, EquityAccount, \
    labelEquity = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

    ## For the spatial chart
    edge_Y_stock, edge_Y_intrinsic, edge_Y_optionprice, edge_Y_portfolio, edge_Y_cash, edge_Y_nbrofshares = {}, {}, {}, {}, {}, {}
    #####################                      END accounts initialization                         #####################
    ####################################################################################################################

    ####################################################################################################################
    #####################                  START replication strategy                              #####################
    #### dt, up factor, down factor, discounting factor, probUpFactor, probDownFact
    step = T / tree__periods
    u = np.exp(mu * step + vol * np.sqrt(step))
    d = np.exp(mu * step - vol * np.sqrt(step))

    discFact = np.exp(-rf * step)

    probUp = (np.exp(rf * step) - d) / (u - d)
    probDown = 1 - probUp

    stockprices[(0, 1)] = S
    stockprices[(1, 1)] = S * u
    stockprices[(1, 2)] = S * d

    # Create the edges, compute the stock price and option intrinsic value at all nodes
    for i in range(0, tree__periods + 1):
        for j in range(1, i + 2):
            if i < tree__periods:
                # CREATION OF THE EDGES
                G_Stock.add_edge((i, j), (i + 1, j))
                G_Stock.add_edge((i, j), (i + 1, j + 1))

                G_Intrinsic.add_edge((i, j), (i + 1, j))
                G_Intrinsic.add_edge((i, j), (i + 1, j + 1))

                G_Price.add_edge((i, j), (i + 1, j))
                G_Price.add_edge((i, j), (i + 1, j + 1))

                G_Portfolio.add_edge((i, j), (i + 1, j))
                G_Portfolio.add_edge((i, j), (i + 1, j + 1))

                G_CashAccount.add_edge((i, j), (i + 1, j))
                G_CashAccount.add_edge((i, j), (i + 1, j + 1))

                G_Shares.add_edge((i, j), (i + 1, j))
                G_Shares.add_edge((i, j), (i + 1, j + 1))

                # stock price and option intrinsic value at all nodes
                stockprices[(i, j)] = stockprices[(i, j)]
                stockprices[(i + 1, j)] = stockprices[(i, j)] * u
                stockprices[(i + 1, j + 1)] = stockprices[(i, j)] * d

                # labelStocks[(i, j)] = round(stockprices[(i, j)], 5)
                # labelStocks[(i + 1, j)] = round(stockprices[(i + 1, j)], 5)
                # labelStocks[(i + 1, j + 1)] = round(stockprices[(i + 1, j + 1)],5)

                # option intrinsic value at all nodes
                optionintrinsicvalue[(i, j)] = max(phi * (stockprices[(i, j)] - K), 0)
                optionintrinsicvalue[(i + 1, j)] = max(phi * (stockprices[(i + 1, j)] - K), 0)
                optionintrinsicvalue[(i + 1, j + 1)] = max(phi * (stockprices[(i + 1, j + 1)] - K), 0)

                # labelsIntrinsic[(i, j)] = round(optionintrinsicvalue[(i, j)], 5)
                # labelsIntrinsic[(i + 1, j)] = round(optionintrinsicvalue[(i + 1, j)], 5)
                # labelsIntrinsic[(i + 1, j + 1)] = round(optionintrinsicvalue[(i + 1, j + 1)], 5)

                # for the spatial chart
                # edge_Y_stock[(i,j),(i+1,j)] = (labelStocks[(i, j)],labelStocks[(i + 1, j)])
                # edge_Y_stock[(i, j), (i + 1, j + 1)] = (labelStocks[(i, j)],labelStocks[(i + 1, j + 1)])
                # edge_Y_intrinsic[(i, j), (i + 1, j)] = (labelsIntrinsic[(i, j)], labelsIntrinsic[(i + 1, j)])
                # edge_Y_intrinsic[(i, j), (i + 1, j + 1)] = (labelsIntrinsic[(i, j)], labelsIntrinsic[(i + 1, j + 1)])

                edge_Y_stock[(i,j),(i+1,j)] = (stockprices[(i, j)],stockprices[(i + 1, j)])
                edge_Y_stock[(i, j), (i + 1, j + 1)] = (stockprices[(i, j)],stockprices[(i + 1, j + 1)])
                edge_Y_intrinsic[(i, j), (i + 1, j)] = (optionintrinsicvalue[(i, j)], optionintrinsicvalue[(i + 1, j)])
                edge_Y_intrinsic[(i, j), (i + 1, j + 1)] = (optionintrinsicvalue[(i, j)], optionintrinsicvalue[(i + 1, j + 1)])



    # option price at all nodes
    for i in range(tree__periods, -1, -1):
        for j in range(1, i + 2):

            # values at maturity are not discounted given we start there
            if i == tree__periods:
                optionprice[(i, j)] = optionintrinsicvalue[(i, j)]
                # labelsOptionPrice[(i, j)] = round(optionprice[(i, j)], 5)


            # all the others, until price at t=0
            else:
                optionprice[(i, j)] = discFact * (probUp * optionprice[(i + 1, j)] + probDown * optionprice[(i + 1, j + 1)])
                # labelsOptionPrice[(i, j)] = round(optionprice[(i, j)], 5)

                # for the spatial chart
                # edge_Y_optionprice[(i, j), (i + 1, j)] = (labelsOptionPrice[(i, j)], labelsOptionPrice[(i + 1, j)])
                # edge_Y_optionprice[(i, j), (i + 1, j + 1)] = (labelsOptionPrice[(i, j)], labelsOptionPrice[(i + 1, j + 1)])

                edge_Y_optionprice[(i, j), (i + 1, j)] = (optionprice[(i, j)], optionprice[(i + 1, j)])
                edge_Y_optionprice[(i, j), (i + 1, j + 1)] = (optionprice[(i, j)], optionprice[(i + 1, j + 1)])





    Portfolio[(0, 1)] = optionprice[(0, 1)]
    # labelPortfolio[(0, 1)] = str(round(Portfolio[(0, 1)], 5))

    # changer l'algo qui tourne autour des nodes, car trop lent 
    for i in range(0, tree__periods + 1):
        for j in range(1, i + 2):
            if i < tree__periods:
                # print(i, j)
                # initialize / After Rebalancing
                NbrOfShares[(i, j)] = (optionprice[(i + 1, j)] - optionprice[(i + 1, j + 1)]) / (stockprices[(i + 1, j)] - stockprices[(i + 1, j + 1)])
                CashAccount[(i, j)] = Portfolio[(i, j)] - NbrOfShares[(i, j)] * stockprices[(i, j)]


                # Labels for the graph
                # if i == 0:
                #     labelCash[(i, j)] = str(round(CashAccount[(i, j)], 5))
                #     labelNbrOfShares[(i, j)] = str(round(NbrOfShares[(i, j)], 5))

                # labelCash[(i, j)] += f",{round(CashAccount[(i, j)], 2)}"
                # labelNbrOfShares[(i, j)] += f",{round(NbrOfShares[(i, j)], 2)}"
                # labelPortfolio[(i, j)] += f",{round(CashAccount[(i, j)] + NbrOfShares[(i, j)] * stockprices[(i, j)], 2)}"

                # labelCash[(i, j)] = f"{round(CashAccount[(i, j)], 5)}"
                # labelNbrOfShares[(i, j)] = f"{round(NbrOfShares[(i, j)], 5)}"
                # labelPortfolio[(i, j)] = f"{round(CashAccount[(i, j)] + NbrOfShares[(i, j)] * stockprices[(i, j)], 5)}"


                # Before Rebalancing
                NbrOfShares[(i + 1, j)] = NbrOfShares[(i, j)]
                CashAccount[(i + 1, j)] = CashAccount[(i, j)] * np.exp(rf * step)
                Portfolio[(i + 1, j)] = CashAccount[(i + 1, j)] + NbrOfShares[(i + 1, j)] * stockprices[(i + 1, j)]

                NbrOfShares[(i + 1, j + 1)] = NbrOfShares[(i, j)]
                CashAccount[(i + 1, j + 1)] = CashAccount[(i, j)] * np.exp(rf * step)
                Portfolio[(i + 1, j + 1)] = CashAccount[(i + 1, j + 1)] + NbrOfShares[(i + 1, j + 1)] * stockprices[(i + 1, j + 1)]

                # Labels for the graph
                # labelCash[(i + 1, j)] = f"{round(CashAccount[(i + 1, j)], 5)}"
                # labelCash[(i + 1, j + 1)] = f"{round(CashAccount[(i + 1, j + 1)], 5)}"

                # labelNbrOfShares[(i + 1, j)] = f"{round(NbrOfShares[(i + 1, j)], 5)}"
                # labelNbrOfShares[(i + 1, j + 1)] = f"{round(NbrOfShares[(i + 1, j + 1)], 5)}"

                # labelPortfolio[(i + 1, j + 1)] = f"{round(Portfolio[(i + 1, j + 1)], 5)}"
                # labelPortfolio[(i + 1, j)] = f"{round(Portfolio[(i + 1, j)], 5)}"

    # re-running the loop now that we have the values for the spatial chart
    for i in range(0, tree__periods + 1):
        for j in range(1, i + 2):
            if i < tree__periods:
                # edge_Y_portfolio[(i, j), (i + 1, j)] = (labelPortfolio[(i, j)], labelPortfolio[(i + 1, j)])
                # edge_Y_portfolio[(i, j), (i + 1, j + 1)] = (labelPortfolio[(i, j)], labelPortfolio[(i + 1, j + 1)])

                # edge_Y_cash[(i, j), (i + 1, j)] = (labelCash[(i, j)], labelCash[(i + 1, j)])
                # edge_Y_cash[(i, j), (i + 1, j + 1)] = (labelCash[(i, j)], labelCash[(i + 1, j + 1)])

                # edge_Y_nbrofshares[(i, j), (i + 1, j)] = (labelNbrOfShares[(i, j)], labelNbrOfShares[(i + 1, j)])
                # edge_Y_nbrofshares[(i, j), (i + 1, j + 1)] = (labelNbrOfShares[(i, j)], labelNbrOfShares[(i + 1, j + 1)])

                edge_Y_portfolio[(i, j), (i + 1, j)] = (Portfolio[(i, j)], Portfolio[(i + 1, j)])
                edge_Y_portfolio[(i, j), (i + 1, j + 1)] = (Portfolio[(i, j)], Portfolio[(i + 1, j + 1)])

                edge_Y_cash[(i, j), (i + 1, j)] = (CashAccount[(i, j)], CashAccount[(i + 1, j)])
                edge_Y_cash[(i, j), (i + 1, j + 1)] = (CashAccount[(i, j)], CashAccount[(i + 1, j + 1)])

                edge_Y_nbrofshares[(i, j), (i + 1, j)] = (NbrOfShares[(i, j)], NbrOfShares[(i + 1, j)])
                edge_Y_nbrofshares[(i, j), (i + 1, j + 1)] = (NbrOfShares[(i, j)], NbrOfShares[(i + 1, j + 1)])





    # print(optionprice[(0,1)])

    # creating the nodes itself in the networkx graph
    pos = {}
    for node in G_Stock.nodes():
        pos[node] = (node[0], tree__periods + 2 + node[0] - 2 * node[1])

    edge_x = []
    edge_y = []
    node_x = []
    node_y = []
    stocksLabel = []
    intrinsicLabel = []
    optionpriceLabel = []
    portfolioLabel = []
    cashLabel = []
    nbrofsharesLabel = []


    for edge in G_Stock.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)


    for node in pos:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        # stocksLabel.append(labelStocks[node])
        # intrinsicLabel.append(labelsIntrinsic[node])
        # optionpriceLabel.append(labelsOptionPrice[node])
        # portfolioLabel.append(labelPortfolio[node])
        # cashLabel.append(labelCash[node])
        # nbrofsharesLabel.append(labelNbrOfShares[node])

        stocksLabel.append(stockprices[node])
        intrinsicLabel.append(optionintrinsicvalue[node])
        optionpriceLabel.append(optionprice[node])
        portfolioLabel.append(Portfolio[node])
        cashLabel.append(CashAccount[node])
        nbrofsharesLabel.append(NbrOfShares[node])

    edge_y_Stock, edge_y_Intrinsic, edge_y_Optionprice, edge_y_Portfolio, edge_y_Cash, edge_y_NbrOfShares = [], [], [], [], [], []
    node_y_Stock, node_y_Intrinsic, node_y_Optionprice, node_y_Portfolio, node_y_Cash, node_y_NbrOfShares = node_y[:], node_y[:], node_y[:], node_y[:], node_y[:], node_y[:]

    # EDGES SPATIAL CHART
    for key, value in edge_Y_stock.items():
        edge_y_Stock.append(value[0])
        edge_y_Stock.append(value[1])
        edge_y_Stock.append(None)
    for key, value in edge_Y_intrinsic.items():
    	edge_y_Intrinsic.append(value[0])
    	edge_y_Intrinsic.append(value[1])
    	edge_y_Intrinsic.append(None)
    for key,value in edge_Y_optionprice.items():
    	edge_y_Optionprice.append(value[0])
    	edge_y_Optionprice.append(value[1])
    	edge_y_Optionprice.append(None)
    for key, value in edge_Y_portfolio.items():
    	edge_y_Portfolio.append(value[0])
    	edge_y_Portfolio.append(value[1])
    	edge_y_Portfolio.append(None)
    for key, value in edge_Y_cash.items():
    	edge_y_Cash.append(value[0])
    	edge_y_Cash.append(value[1])
    	edge_y_Cash.append(None)
    for key, value in edge_Y_nbrofshares.items():
    	edge_y_NbrOfShares.append(value[0])
    	edge_y_NbrOfShares.append(value[1])
    	edge_y_NbrOfShares.append(None)

    # NODES SPATIAL CHART
    for i in range(0, len(node_x)):
    	node_y_Stock[i]       = stocksLabel[i]
    	node_y_Intrinsic[i]   = intrinsicLabel[i]
    	node_y_Optionprice[i] = optionpriceLabel[i]
    	node_y_Portfolio[i]   = portfolioLabel[i]
    	node_y_Cash[i]        = cashLabel[i]
    	node_y_NbrOfShares[i] = nbrofsharesLabel[i]


    return nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, round(u,2), round(d,2), round(probUp,2), round(probDown,2), edge_y_Stock, node_y_Stock, edge_y_Intrinsic, node_y_Intrinsic, edge_y_Optionprice, node_y_Optionprice, edge_y_Portfolio, node_y_Portfolio, edge_y_Cash, node_y_Cash, edge_y_NbrOfShares, node_y_NbrOfShares, tree__periods
    
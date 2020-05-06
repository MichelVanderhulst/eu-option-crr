import matplotlib
import networkx as nx
import matplotlib.pyplot as plt
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
## Yuxing Yan Python for Finance 2nd edition -> the script for the binomial tree
#######################################################################################################################


def p_bs(spot_price, strike, riskfree_rate, T, volatility, phi):
    d1 = (np.log(spot_price / strike) + T * (riskfree_rate + 0.5 * volatility * volatility)) / (volatility * np.sqrt(T))
    d2 = (np.log(spot_price / strike) + T * (riskfree_rate - 0.5 * volatility * volatility)) / (volatility * np.sqrt(T))
    return phi * (spot_price * norm.cdf(phi * d1) - strike * np.exp(-riskfree_rate * T) * norm.cdf(phi * d2))


def RepStrat_EU_Option_CRR_GRW_V5(CallOrPut, S, K, rf, T, mu, vol, tree__periods):

    ####################################################################################################################
    #####################  START derivative/model specifics, user input transformation             #####################

    if CallOrPut == "Call":
        phi = 1
    elif CallOrPut == "Put":
        phi = -1

    #####################  START derivative/model specifics, user input transformation             #####################
    ####################################################################################################################


    ####################################################################################################################
    #####################                  START accounts initialization                           #####################

    G_Stock, G_Intrinsic, G_Price, G_Portfolio, G_CashAccount, G_Shares = nx.Graph(), nx.Graph(), nx.Graph(), \
                                                                          nx.Graph(), nx.Graph(), nx.Graph()

    stockprices, optionintrinsicvalue, optionprice, labelStocks, labelsIntrinsic, labelsOptionPrice, CashAccount, \
    NbrOfShares, Portfolio, labelPortfolio, labelCash, labelNbrOfShares, EquityAccount, \
    labelEquity = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}


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
    # this algorithm sorts through the video in my folder (in case I forget how it runs through the nodes)

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

                labelStocks[(i, j)] = round(stockprices[(i, j)], 2)
                labelStocks[(i + 1, j)] = round(stockprices[(i + 1, j)], 2)
                labelStocks[(i + 1, j + 1)] = round(stockprices[(i + 1, j + 1)], 2)

                # option intrinsic value at all nodes
                optionintrinsicvalue[(i, j)] = max(phi * (stockprices[(i, j)] - K), 0)
                optionintrinsicvalue[(i + 1, j)] = max(phi * (stockprices[(i + 1, j)] - K), 0)
                optionintrinsicvalue[(i + 1, j + 1)] = max(phi * (stockprices[(i + 1, j + 1)] - K), 0)

                labelsIntrinsic[(i, j)] = round(optionintrinsicvalue[(i, j)], 2)
                labelsIntrinsic[(i + 1, j)] = round(optionintrinsicvalue[(i + 1, j)], 2)
                labelsIntrinsic[(i + 1, j + 1)] = round(optionintrinsicvalue[(i + 1, j + 1)], 2)

    # option price at all nodes
    for i in range(tree__periods, -1, -1):
        for j in range(1, i + 2):

            # values at maturity are not discounted given we start there
            if i == tree__periods:
                optionprice[(i, j)] = optionintrinsicvalue[(i, j)]
                labelsOptionPrice[(i, j)] = round(optionprice[(i, j)], 2)

            # all the others, until price at t=0
            else:
                optionprice[(i, j)] = discFact * (probUp * optionprice[(i + 1, j)] + probDown * optionprice[(i + 1, j + 1)])
                labelsOptionPrice[(i, j)] = round(optionprice[(i, j)], 2)

    Portfolio[(0, 1)] = optionprice[(0, 1)]
    labelPortfolio[(0, 1)] = str(round(Portfolio[(0, 1)], 2))

    # changer l'algo qui tourne autour des nodes, car trop lent avec les nodes.
    for i in range(0, tree__periods + 1):
        for j in range(1, i + 2):
            if i < tree__periods:
                # print(i, j)
                # initialize / After Rebalancing
                NbrOfShares[(i, j)] = (optionprice[(i + 1, j)] - optionprice[(i + 1, j + 1)]) / (stockprices[(i + 1, j)] - stockprices[(i + 1, j + 1)])
                CashAccount[(i, j)] = Portfolio[(i, j)] - NbrOfShares[(i, j)] * stockprices[(i, j)]

                # Labels for the graph
                if i == 0:
                    labelCash[(i, j)] = str(round(CashAccount[(i, j)], 2))
                    labelNbrOfShares[(i, j)] = str(round(NbrOfShares[(i, j)], 2))

                labelCash[(i, j)] += f",{round(CashAccount[(i, j)], 2)}"
                labelNbrOfShares[(i, j)] += f",{round(NbrOfShares[(i, j)], 2)}"
                labelPortfolio[
                    (i, j)] += f",{round(CashAccount[(i, j)] + NbrOfShares[(i, j)] * stockprices[(i, j)], 2)}"

                # Before Rebalancing
                NbrOfShares[(i + 1, j)] = NbrOfShares[(i, j)]
                CashAccount[(i + 1, j)] = CashAccount[(i, j)] * np.exp(rf * step)
                Portfolio[(i + 1, j)] = CashAccount[(i + 1, j)] + NbrOfShares[(i + 1, j)] * stockprices[(i + 1, j)]

                NbrOfShares[(i + 1, j + 1)] = NbrOfShares[(i, j)]
                CashAccount[(i + 1, j + 1)] = CashAccount[(i, j)] * np.exp(rf * step)
                Portfolio[(i + 1, j + 1)] = CashAccount[(i + 1, j + 1)] + \
                                            NbrOfShares[(i + 1, j + 1)] * stockprices[(i + 1, j + 1)]

                # Labels for the graph
                labelCash[(i + 1, j)] = f"{round(CashAccount[(i + 1, j)], 2)}"
                labelCash[(i + 1, j + 1)] = f"{round(CashAccount[(i + 1, j + 1)], 2)}"

                labelNbrOfShares[(i + 1, j)] = f"{round(NbrOfShares[(i + 1, j)], 2)}"
                labelNbrOfShares[(i + 1, j + 1)] = f"{round(NbrOfShares[(i + 1, j + 1)], 2)}"

                labelPortfolio[(i + 1, j + 1)] = f"{round(Portfolio[(i + 1, j + 1)], 2)}"
                labelPortfolio[(i + 1, j)] = f"{round(Portfolio[(i + 1, j)], 2)}"

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
        stocksLabel.append(labelStocks[node])
        intrinsicLabel.append(labelsIntrinsic[node])
        optionpriceLabel.append(labelsOptionPrice[node])
        portfolioLabel.append(labelPortfolio[node])
        cashLabel.append(labelCash[node])
        nbrofsharesLabel.append(labelNbrOfShares[node])


    return nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, round(u,2), round(d,2), round(probUp,2), round(probDown,2)
    # plotting the networkx graphs through matplotlib
    # plt.ion()
    # plt.suptitle(f"Cox-Ross-Rubinstein (CRR) model, {CallOrPut} pricing & replication strategy")
    # plt.figtext(0.5, 0.95,
    #             f"Black-Scholes price check: {round(p_bs(S, K, rf, T, vol, phi), 2)}. At around ~20 periods, the tree converges to the BS price.",
    #             ha="center", va="top", fontsize=10)

    #return G_Stock, pos, labelStocks
    plt.subplot(3, 3, 1)
    fig1 = plt.figure()
    textstr = '\n'.join((
        r'up factor =%.2f' % (u,),
        r'down factor=%.3f' % (d,),
        r'prob up=%.2f' % (probUp,),
        r"prob down=%.2f" % (probDown)))
    plt.title("Stock price tree")
    nx.draw_networkx_labels(G_Stock, pos, labels=labelStocks)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(-0.07, 1, textstr)#, transform=ax.transAxes, verticalalignment='top', bbox=props, fontsize=10)
    nx.draw(G_Stock, pos=pos)
    plt.show()
                    # CallOrPut, S, K, rf, T, mu, vol, tree__periods)
#RepStrat_EU_Option_CRR_GRW_V5("Put", 100, 100, 0.05, 3, 0.1, 0.2, 5)

    # # plt.subplot(3, 3, 2)
    # fig2 = plt.figure()
    # plt.title(f"{CallOrPut} intrinsic value")
    # nx.draw_networkx_labels(G_Intrinsic, pos, labels=labelsIntrinsic)
    # nx.draw(G_Intrinsic, pos=pos)
    # move_figure(fig2, 500, 0)


    # # plt.subplot(3, 3, 3)
    # fig3 = plt.figure()
    # plt.title(f"{CallOrPut} backwards risk-neutral expectation pricing")
    # nx.draw_networkx_labels(G_Price, pos, labels=labelsOptionPrice)
    # nx.draw(G_Price, pos=pos)
    # move_figure(fig3, 1000, 0)

    # # plt.subplot(3, 3, 4)
    # fig4 = plt.figure()
    # plt.title("Portfolio before/after rebalancing")
    # nx.draw_networkx_labels(G_Portfolio, pos, labels=labelPortfolio, font_size=10)
    # nx.draw(G_Portfolio, pos=pos)
    # move_figure(fig4, 0, 300)


    # # plt.subplot(3, 3, 5)
    # fig5 = plt.figure()
    # plt.title("Cash account before/after rebalancing")
    # nx.draw_networkx_labels(G_CashAccount, pos, labels=labelCash, font_size=10)
    # nx.draw(G_CashAccount, pos=pos)
    # move_figure(fig5, 500, 300)


    # # plt.subplot(3, 3, 6)
    # fig6 = plt.figure()
    # plt.title("Held Shares before/after rebalancing")
    # nx.draw_networkx_labels(G_Shares, pos, labels=labelNbrOfShares, font_size=10)
    # nx.draw(G_Shares, pos=pos)
    # move_figure(fig6, 1000, 300)


    # # plt.subplot(3, 1, 3)
    # fig7 = plt.figure(figsize=(15, 4.8))
    # plt.title("Replication strategy description")
    # plt.plot(np.linspace(-np.pi, np.pi, 100),
    #          np.sin(np.linspace(-np.pi, np.pi, 100)) * np.cos(np.linspace(-np.pi, np.pi, 100)), color="w")
    # plt.xticks([])
    # plt.yticks([])
    # plt.axis("off")
    # textstr = '\n'.join((
    #     # "The CRR model modelizes the stock price as a geometric random walk with drift $\mu\delta$ and volatility $\sigma\sqrt{\delta}$. The model allows the following assumptions: first, at each step ",
    #     # "the stock can only go up or down by constant factors $u > 1$ (up) and $0 < d < 1$ (down) with probability $p$ and $1-p$ respectively (under P). Second, the log-returns are ",
    #     # "independent  at all periods, i.e. from one step to another. The stock price at period $i$ can be modelized as a function of a binomial random variable, and the constant up  ",
    #     # "and down factors computed : $u = e^{\mu\delta+\sigma\sqrt{\delta}}$ and $d = e^{\mu\delta-\sigma\sqrt{\delta}}$. The $Q$-probability allowing the discounted stock price to be a martingale amounts to the $p$ value (under Q) ",
    #     # r"which leads to the martingale property of $\tilde{S}$: $p = \frac{e^{Rf}-d}{u-d}$. ", From there, the stock tree can be computed, along the {CallOrPut} intrinsic value at all nodes.
    #     f"With the stock tree along the {CallOrPut} intrinsic value at all nodes, let's prove that the price is arbitrage-free. It will be priced in two different manners: by risk-neutral expectation",
    #     "and by replication. The former is fast: given that we are under the pricing measure, the price at all nodes is simply the discounted value of the two children nodes.",
    #     "The price tree is therefore filled backwards, starting from the leaves (i.e. the payoff). Then, if the price computed is truly abitrage-free, then a replication strategy can ",
    #     r"be based on this price: $\pi_{0} = v_{0}$. At the begining of each period, the number of shares to hold is $\Delta_{i}^{j} = \frac{v_{i+1}^{j}-v_{i+1}^{j+1}}{s_{i+1}^{j}-s_{i+1}^{j+1}}$. The initial amount of cash will be $c_{0} = \pi_{0} - \Delta_{0}s_{0}$. At each ",
    #     "node, a portfolio rebalancing is needed. Before the rebalancing, $\Delta$ is the same from node to node $\Delta_{i}^{j}=\Delta_{i-1}^{j}$, the cash account grew at the risk-free rate $c_{i}^{j}=c_{i-1}^{j}e^{Rf}$, and",
    #     r"the portfolio is the sum of both equity and cash positions $\pi_{i}^{j}=c_{i}^{j}+\Delta_{i}^{j}s_{i}^{j}$. The rebalancing is done by updating the shares to hold $\Delta_{i}^{j}=\frac{v_{i+1}^{j}-v_{i+1}^{j+1}}{s_{i+1}^{j}-s_{i+1}^{j+1}}$ and ensuring the of value of ",
    #     "the strategy before and after the rebalancing is the same $c_{i}^{j}=\pi_{i}^{j}-(\Delta_{i-1}^{j}-\Delta_{i}^{j})s_{i}^{j}$. The tree is computed forward, and at the end of it we obtain, at all nodes, the option payoff. "))
    # plt.text(-3.4, 0.5, textstr, verticalalignment='top')
    # move_figure(fig7, 0, 500)

    # plt.pause(2)
    # plt.show()

# RepStrat_EU_Option_CRR_GRW_V3(310, 320, -14, 31, 5, 2, 10, "Put")


# def move_figure(f, x, y):
#     """Move figure's upper left corner to pixel (x, y)"""
#     backend = matplotlib.get_backend()
#     if backend == 'TkAgg':
#         f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
#     elif backend == 'WXAgg':
#         f.canvas.manager.window.SetPosition((x, y))
#     else:
#         # This works for QT and GTK
#         # You can also use window.setGeometry
#         f.canvas.manager.window.move(x, y)


# def binomial_grid(n):
#     G = nx.Graph()
#     for i in range(0, n + 1):
#         for j in range(1, i + 2):
#             if i < n:
#                 G.add_edge((i, j), (i + 1, j))
#                 G.add_edge((i, j), (i + 1, j + 1))
#
#     posG = {}
#     for node in G.nodes():
#         posG[node] = (node[0], n + 2 + node[0] - 2 * node[1])
#
#     nx.draw(G, pos=posG)  # , with_labels=True)
#     plt.show()
# binomial_grid(9)

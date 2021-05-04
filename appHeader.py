# Dash app libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import base64


# Author parameters
bg_color="#506784",
font_color="#F3F6FA"
author = "Michel Vanderhulst"
emailAuthor = "michelvanderhulst@hotmail.com"
supervisor = "Prof. Frédéric Vrins"
emailSupervisor = "frederic.vrins@uclouvain.be"
logo1path = "./pictures/1200px-Louvain_School_of_Management_logo.svg.png"
logo1URL  = "https://uclouvain.be/en/faculties/lsm"
logo2path = "./pictures/1280px-NovaSBE_Logo.svg.png"
logo2URL  = "https://www2.novasbe.unl.pt/en/"

# Creating the app header
def header():
    return html.Div(
                id='app-page-header',
                children=[
                    html.Div(children=[html.A(id='lsm-logo', 
                                              children=[html.Img(style={'height':'6%', 'width':'6%'}, src='data:image/png;base64,{}'.format(base64.b64encode(open(f"{logo1path}", 'rb').read()).decode()))],
                                              href=f"{logo1URL}",
                                              target="_blank", #open link in new tab
                                              style={"margin-left":"10px"}
                                              ),

                                       html.Div(children=[html.H5("Asian option replication strategy app"),
                                                          html.H6("Cox-Ross-Rubinstein model")
                                                          ],
                                                 style={"display":"inline-block", "font-family":'sans-serif','transform':'translateY(+32%)', "margin-left":"10px"}),

                                       html.Div(children=[dbc.Button("About", id="popover-target", outline=True, style={"color":"white", 'border': 'solid 1px white'}),
                                                          dbc.Popover(children=[dbc.PopoverHeader("About"),
                                                                                dbc.PopoverBody([f"{author}",                             
                                                                                             f"\n {emailAuthor}", 
                                                                                               html.Hr(), 
                                                                                             f"This app was built for my Master's Thesis, under the supervision of {supervisor} ({emailSupervisor})."]),],
                                                                       id="popover",
                                                                       is_open=False,
                                                                       target="popover-target"),
                                                          ],
                                                 style={"display":"inline-block","font-family":"sans-serif","marginLeft":"55%", "margin-right":"10px"}),

                                     html.A(id="nova-logo",
                                            children=[html.Img(style={"height":"9%","width":"9%"}, src="data:image/png;base64,{}".format(base64.b64encode(open(f"{logo2path}","rb").read()).decode()))],
                                            href=f"{logo2URL}",
                                            target="_blank",                   
                                            style={}
                                            )                                       
                                      ]
                             ,style={"display":"inline-block"}),  
                         ],
                style={
                    'background': bg_color,
                    'color': font_color,
                    "padding-bottom": "10px",
                    "padding-top":"-10px"
                }
            )
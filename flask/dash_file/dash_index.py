from dash import Dash, html, dash_table, callback, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from . import data
import plotly.express as px

dash_index = Dash(
    requests_pathname_prefix="/dash/index/", external_stylesheets=[dbc.themes.BOOTSTRAP]
)
dash_index.title = "信用卡消費樣態"


dash_index.layout = html.Div(
    [
        dbc.Container(
            [
                html.Div(
                    [html.Div([html.H1("信用卡消費樣態")], className="col text-center")],
                    className="row",
                    style={"paddingTop": "2rem"},
                ),
                html.Div(
                    [dbc.Button("教育程度", color="primary", className="me-5", href="/dash/app/", external_link=True),
                    dbc.Button("年齡層", color="secondary", className="me-5", href="/dash/app1/", external_link=True),
                    dbc.Button("職業類別", color="success", className="me-5", href="/dash/app2/", external_link=True),
                    dbc.Button("兩性", color="warning", className="me-5", href="/dash/app3/", external_link=True),
                    dbc.Button("年收入", color="danger", className="me-5", href="/dash/app4/", external_link=True),],
                    className="d-flex justify-content-center",  # Center the buttons horizontally
                ),
                
            ]
        )
    ],
    className="container-lg",
)


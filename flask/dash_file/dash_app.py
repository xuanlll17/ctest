from dash import Dash, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from . import data

dash = Dash(
    requests_pathname_prefix="/dash/app/", external_stylesheets=[dbc.themes.BOOTSTRAP]
)
dash.title = "信用卡消費樣態"
lastest_data = data.lastest_datetime_data()


lastest_df = pd.DataFrame(
    lastest_data, columns=["年", "月", "地區", "產業別", "教育程度", "信用卡交易筆數", "信用卡交易金額"]
)


dash.layout = html.Div(
    [
        dbc.Container(
            [
                html.Div(
                    [html.Div([html.H1("信用卡消費樣態")], className="col text-center")],
                    className="row",
                    style={"paddingTop": "2rem"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dash_table.DataTable(
                                    data=lastest_df.to_dict("records"),
                                    columns=[
                                        {"id": column, "name": column}
                                        for column in lastest_df.columns
                                    ],
                                    page_size=20,
                                    fixed_rows={"headers": True},
                                    style_table={
                                        "height": "300px",
                                        "overflowY": "auto",
                                    },
                                    style_cell={
                                        "text_align": "center",
                                    },
                                ),
                            ],
                            className="col text-center",
                        )
                    ],
                    className="row",
                    style={"paddingTop": "2rem"},
                ),
            ]
        )
    ],
    className="container-lg",
)

from dash import Dash, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from . import data

dash1 = Dash(
    requests_pathname_prefix="/dash/app1/", external_stylesheets=[dbc.themes.BOOTSTRAP]
)
dash1.title = "信用卡消費樣態"
lastest_data = data.age_data()


lastest_df = pd.DataFrame(
    lastest_data, columns=["年", "月", "地區", "產業別", "年齡層", "信用卡交易筆數", "信用卡交易金額"]
)


dash1.layout = html.Div(
    [
        dbc.Container(
            [
                html.Div(
                    [html.Div([html.H1("各年齡層信用卡消費樣態")], className="col text-center")],
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
                html.Div(
                    [
                        html.Div(
                            [
                                html.P("來源："),
                                html.P("Data： 聯合信用卡處理中心Open API"),
                                html.P("Icon： Image by toffeomurice from Pixabay"),
                            ],
                            className="col",
                        )
                    ],
                    className="row",
                    style={
                        "paddingTop": "2rem",
                        "fontSize": "0.8rem",
                        "lineHeight": "0.3rem",
                    },
                ),
            ]
        )
    ],
    className="container-lg",
)

from dash import Dash, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from . import data2

dash1 = Dash(
    requests_pathname_prefix="/dash/app1/", external_stylesheets=[dbc.themes.BOOTSTRAP]
)
dash1.title = "信用卡消費樣態"
lastest_data = data2.lastest_datetime_data()
lastest_df = pd.DataFrame(
    lastest_data, columns=["年", "月", "地區", "產業別", "教育程度", "信用卡交易筆數", "信用卡交易金額"]
)
lastest_df1 = lastest_df.reset_index()
lastest_df1["站點名稱"] = lastest_df1["站點名稱"].map(lambda name: name[11:])

dash1.layout = html.Div(
    [
        dbc.Container(
            [
                # row
                html.Div(
                    [
                        html.Div(
                            [html.H1("台北市youbike及時資料")], className="col text-center"
                        )
                    ],
                    className="row",
                    style={"paddingTop": "2rem"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dash_table.DataTable(
                                    # 先轉list dict 才能輸出
                                    data=lastest_df1.to_dict("records"),
                                    columns=[
                                        {"id": column, "name": column}
                                        for column in lastest_df1.columns
                                    ],
                                    page_size=20,
                                    fixed_rows={"headers": True},
                                    style_table={
                                        "height": "300px",
                                        "overflowY": "auto",
                                    },
                                    style_cell_conditional=[
                                        {"if": {"column_id": "index"}, "width": "6%"},
                                        {"if": {"column_id": "站點名稱"}, "width": "25%"},
                                        {"if": {"column_id": "總數"}, "width": "5%"},
                                        {"if": {"column_id": "可借"}, "width": "5%"},
                                        {"if": {"column_id": "可還"}, "width": "5%"},
                                    ],
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
    className="container-lg",)
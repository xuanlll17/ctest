from dash import Dash, html, dash_table, callback, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from . import data

dash = Dash(
    requests_pathname_prefix="/dash/app/", external_stylesheets=[dbc.themes.BOOTSTRAP]
)
dash.title = "信用卡消費樣態"
lastest_data = data.edu_data()


lastest_df = pd.DataFrame(
    lastest_data, columns=["年", "月", "地區", "產業別", "教育程度", "信用卡交易筆數", "信用卡交易金額"]
)


dash.layout = html.Div(
    [
        dbc.Container(
            [
                html.Div(
                    [html.Div([html.H1("各教育程度信用卡消費樣態")], className="col text-center")],
                    className="row",
                    style={"paddingTop": "2rem"},
                ),
                html.Div([
                    dbc.DropdownMenu(
                        label="資料類別",
                        children=[
                            dbc.DropdownMenuItem(
                                "年齡層",
                                href="/dash/app1/",
                                external_link=True),
                            dbc.DropdownMenuItem(
                                "職業類別",
                                href="/dash/app2/",
                                external_link=True),
                            dbc.DropdownMenuItem(
                                "兩性",
                                href="/dash/app3/",
                                external_link=True),
                            dbc.DropdownMenuItem(
                                "年收入",
                                href="/dash/app4/",
                                external_link=True),
                        ],
                    ),
                    dbc.DropdownMenu(
                        label="月份",
                        children=[
                            dbc.DropdownMenuItem("1"),
                            dbc.DropdownMenuItem("2"),
                            dbc.DropdownMenuItem("3"),
                            dbc.DropdownMenuItem("4"),
                            dbc.DropdownMenuItem("5"),
                            dbc.DropdownMenuItem("6"),
                            dbc.DropdownMenuItem("7"),
                            dbc.DropdownMenuItem("8"),
                            dbc.DropdownMenuItem("9"),
                            dbc.DropdownMenuItem("ALL"),
                        ],
                    ),
                    dbc.DropdownMenu(
                        label="地區",
                        children=[
                            dbc.DropdownMenuItem("臺北市"),
                            dbc.DropdownMenuItem("新北市"),
                            dbc.DropdownMenuItem("桃園市"),
                            dbc.DropdownMenuItem("臺中市"),
                            dbc.DropdownMenuItem("臺南市"),
                            dbc.DropdownMenuItem("高雄市"),
                            dbc.DropdownMenuItem("ALL"),
                        ],
                    ),
                    dbc.DropdownMenu(
                        label="產業別",
                        children=[
                            dbc.DropdownMenuItem("食"),
                            dbc.DropdownMenuItem("衣"),
                            dbc.DropdownMenuItem("住"),
                            dbc.DropdownMenuItem("行"),
                            dbc.DropdownMenuItem("文教康樂"),
                            dbc.DropdownMenuItem("百貨"),
                            dbc.DropdownMenuItem("ALL"),
                        ],
                    ),
                ],
                className="row row-cols-auto align-items-end",
                style={"paddingTop":'2rem'}),
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
                    style={"paddingTop": "2rem","fontSize":"0.8rem","lineHeight":"0.3rem"},
                ),
            ]
        )
    ],
    className="container-lg",
)

from dash import Dash, html, dash_table, callback, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from . import data

dash2 = Dash(
    requests_pathname_prefix="/dash/app2/", external_stylesheets=[dbc.themes.BOOTSTRAP]
)
dash2.title = "信用卡消費樣態"
lastest_data = data.job_data()


lastest_df = pd.DataFrame(
    lastest_data, columns=["年", "月", "地區", "產業別", "職業類別", "信用卡交易筆數", "信用卡交易金額"]
)


dash2.layout = html.Div(
    [
        dbc.Container(
            [
                html.Div(
                    [html.Div([html.H1("各職業類別信用卡消費樣態")], className="col text-center")],
                    className="row",
                    style={"paddingTop": "2rem"},
                ),
                html.Div(
                    [
                        dbc.DropdownMenu(
                            label="資料類別",
                            children=[
                                dbc.DropdownMenuItem(
                                    "教育程度", href="/dash/app/", external_link=True
                                ),
                                dbc.DropdownMenuItem(
                                    "年齡層", href="/dash/app1/", external_link=True
                                ),
                                dbc.DropdownMenuItem(
                                    "兩性", href="/dash/app3/", external_link=True
                                ),
                                dbc.DropdownMenuItem(
                                    "年收入", href="/dash/app4/", external_link=True
                                ),
                            ],
                        ),
                        dbc.DropdownMenu(
                            id="area",
                            label="地區",
                            children=[
                                dbc.DropdownMenuItem(
                                    "臺北市",id="Taipei",n_clicks=None
                                ),
                                dbc.DropdownMenuItem(
                                    "新北市",id="NewTaipei",n_clicks=None
                                ),
                                dbc.DropdownMenuItem(
                                    "臺中市",id="Taichung",n_clicks=None
                                ),
                                dbc.DropdownMenuItem(
                                    "高雄市",id="Kaohsiung",n_clicks=None
                                ),
                            ],
                        ),
                        html.P(id="item-clicks", className="mt-3")               
                    ],
                    className="row row-cols-auto align-items-end",
                    style={"paddingTop": "2rem"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dash_table.DataTable(
                                    id="data",
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


@dash2.callback(
    Output("data", "data"),
    [Input("area", "value"), Input("month", "value"), Input("industry", "value")],
)
def update_table(selected_area, selected_month, selected_industry):
    print(selected_area, selected_industry, selected_month)
    filtered_data = [
        row
        for row in lastest_data
        if (selected_area is None or selected_area == "ALL" or row[2] == selected_area)
        and (selected_month is None or selected_month == "ALL" or str(row[1]) == selected_month)
        and (selected_industry is None or selected_industry == "ALL" or row[3] == selected_industry)
    ]

    update_df = pd.DataFrame(
        filtered_data, columns=["年", "月", "地區", "產業別", "職業類別", "信用卡交易筆數", "信用卡交易金額"]
    )

    print(update_df)
    return update_df.to_dict("records")

